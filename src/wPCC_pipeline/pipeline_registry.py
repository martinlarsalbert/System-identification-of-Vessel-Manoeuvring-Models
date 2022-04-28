"""Project pipelines."""
from typing import Dict
from functools import reduce
from operator import add

from kedro.pipeline import Pipeline
from kedro.pipeline.modular_pipeline import pipeline
import anyconfig
import os.path

from . import pipeline_ship
from .pipelines import kvlcc2
from .pipelines import vessel_manoeuvring_models
from .pipelines import system_matrixes
from . import pipeline_plot
from .pipelines import captive
from .pipelines import generic_data, generic_data2
from .pipelines import plot_filters


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    # Read configs:
    conf_path = os.path.join(
        os.path.split(os.path.split(os.path.dirname(__file__))[0])[0],
        "conf",
        "base",
    )

    runs_globals_path = os.path.join(
        conf_path,
        "runs_globals.yml",
    )
    runs_globals = anyconfig.load(runs_globals_path)
    model_test_ids = runs_globals["model_test_ids"]

    globals_path = os.path.join(
        conf_path,
        "globals.yml",
    )
    global_variables = anyconfig.load(globals_path)
    vmms = global_variables["vmms"]

    update_vmms = global_variables[
        "update_vmms"
    ]  # Disable update of vmm and system matrixes in globals.yml.
    ek_pipelines = {}
    if update_vmms:
        ## Vessel Manoeuvring Models (VMMs)
        vessel_manoeuvring_models_pipeline = vessel_manoeuvring_models.create_pipeline()

        ## Extended Kalman Filters
        for vmm in vmms:
            key = f"ek.{vmm}"
            ek_pipelines[key] = pipeline(
                system_matrixes.create_pipeline(),
                namespace=f"{vmm}",
                inputs={
                    "vmm": vmm,
                },
            )
    else:
        vessel_manoeuvring_models_pipeline = Pipeline([])  # Dummy pipiline
        ek_pipelines = {"dummy": Pipeline([])}

    ## Ships:
    inputs = {vmm: vmm for vmm in vmms}
    inputs.update({f"{vmm}.system_matrixes": f"{vmm}.system_matrixes" for vmm in vmms})
    pipeline_wpcc = pipeline(
        pipeline_ship.create_pipeline(model_test_ids=model_test_ids["wpcc"], vmms=vmms),
        namespace="wpcc",
        inputs=inputs,
        parameters={
            "params:thrust_channels": "params:wpcc.thrust_channels",
            "params:initial.ek_covariance_input": f"params:wpcc.updated.initial.ek_covariance_input",
            "params:initial.ek_covariance_input": f"params:wpcc.initial.ek_covariance_input",
            "params:updated.ek_covariance_input": f"params:wpcc.updated.ek_covariance_input",
            "params:motion_regression.exclude_parameters": "params:wpcc.motion_regression.exclude_parameters",
            "params:lowpass.cutoff": "params:wpcc.lowpass.cutoff",
            "params:lowpass.order": "params:wpcc.lowpass.order",
        },
    )

    pipeline_kvlcc2 = pipeline(
        kvlcc2.create_pipeline(model_test_ids=model_test_ids["kvlcc2"], vmms=vmms),
        namespace="kvlcc2",
        inputs=inputs,
        parameters={
            "params:thrust_channels": "params:kvlcc2.thrust_channels",
            "params:initial.ek_covariance_input": f"params:kvlcc2.initial.ek_covariance_input",
            "params:updated.ek_covariance_input": f"params:kvlcc2.updated.ek_covariance_input",
            "params:motion_regression.exclude_parameters": "params:kvlcc2.motion_regression.exclude_parameters",
            "params:lowpass.cutoff": "params:kvlcc2.lowpass.cutoff",
            "params:lowpass.order": "params:kvlcc2.lowpass.order",
        },
    )

    pipeline_tanker = pipeline(
        pipeline_ship.create_pipeline(
            model_test_ids=model_test_ids["tanker"], vmms=vmms
        ),
        namespace="tanker",
        inputs=inputs,
        parameters={
            "params:thrust_channels": "params:tanker.thrust_channels",
            "params:initial.ek_covariance_input": f"params:tanker.initial.ek_covariance_input",
            "params:updated.ek_covariance_input": f"params:tanker.updated.ek_covariance_input",
            "params:motion_regression.exclude_parameters": "params:tanker.motion_regression.exclude_parameters",
            "params:lowpass.cutoff": "params:tanker.lowpass.cutoff",
            "params:lowpass.order": "params:tanker.lowpass.order",
        },
    )

    pipeline_generic_kvlcc2 = pipeline(
        pipeline_ship.create_pipeline(
            model_test_ids=model_test_ids["generic_kvlcc2"], vmms=vmms
        ),
        namespace="generic_kvlcc2",
        inputs=inputs,
        parameters={
            "params:thrust_channels": "params:generic_kvlcc2.thrust_channels",
            "params:initial.ek_covariance_input": f"params:generic_kvlcc2.initial.ek_covariance_input",
            "params:updated.ek_covariance_input": f"params:generic_kvlcc2.updated.ek_covariance_input",
            "params:motion_regression.exclude_parameters": "params:generic_kvlcc2.motion_regression.exclude_parameters",
            "params:lowpass.cutoff": "generic_kvlcc2.params:lowpass.cutoff",
            "params:lowpass.order": "generic_kvlcc2.params:lowpass.order",
        },
    )

    pipeline_kvlcc2_captive = pipeline(captive.create_pipeline(), namespace="kvlcc2")

    return_dict = {}
    return_dict["__default__"] = (
        vessel_manoeuvring_models_pipeline
        + reduce(add, ek_pipelines.values())
        + pipeline_wpcc
        + pipeline_kvlcc2
    )

    return_dict["kvlcc2"] = (
        vessel_manoeuvring_models_pipeline
        + reduce(add, ek_pipelines.values())
        + pipeline_kvlcc2
    )

    return_dict["tanker"] = (
        vessel_manoeuvring_models_pipeline
        + reduce(add, ek_pipelines.values())
        + pipeline_tanker
    )

    return_dict["wpcc"] = (
        vessel_manoeuvring_models_pipeline
        + reduce(add, ek_pipelines.values())
        + pipeline_wpcc
    )

    return_dict["generic_kvlcc2"] = (
        vessel_manoeuvring_models_pipeline
        + reduce(add, ek_pipelines.values())
        + pipeline_generic_kvlcc2
    )

    for ship_name, model_test_ids_ in model_test_ids.items():
        return_dict[f"plot_{ship_name}"] = pipeline(
            pipeline_plot.create_pipeline(
                model_test_ids=model_test_ids_,
                vmms=vmms,
            ),
            namespace=ship_name,
        )

    for ship_name, model_test_ids_ in model_test_ids.items():
        return_dict[f"plot_filters_{ship_name}"] = pipeline(
            plot_filters.create_pipeline(
                model_test_ids=model_test_ids_,
                vmms=vmms,
            ),
            namespace=ship_name,
        )

    return_dict["kvlcc2_captive"] = pipeline_kvlcc2_captive

    return_dict["generic_data"] = generic_data.create_pipeline()
    return_dict["generic_data2"] = generic_data2.create_pipeline(
        model_test_ids=model_test_ids
    )

    return return_dict

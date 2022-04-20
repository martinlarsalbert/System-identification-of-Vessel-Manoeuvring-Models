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

    ## Vessel Manoeuvring Models (VMMs)
    vessel_manoeuvring_models_pipeline = vessel_manoeuvring_models.create_pipeline()

    ## Extended Kalman Filters
    ek_pipelines = {}
    for vmm in vmms:
        key = f"ek.{vmm}"
        ek_pipelines[key] = pipeline(
            system_matrixes.create_pipeline(),
            namespace=f"{vmm}",
            inputs={
                "vmm": vmm,
            },
        )

    ## Ships:
    inputs = {vmm: vmm for vmm in vmms}
    inputs.update({f"{vmm}.system_matrixes": f"{vmm}.system_matrixes" for vmm in vmms})
    pipeline_wpcc = pipeline(
        pipeline_ship.create_pipeline(model_test_ids=model_test_ids["wpcc"], vmms=vmms),
        namespace="wpcc",
        inputs=inputs,
        parameters={
            "params:thrust_channels": "params:wpcc.thrust_channels",
            "params:ek_covariance_input": "params:wpcc.ek_covariance_input",
            "params:motion_regression.exclude_parameters": "params:wpcc.motion_regression.exclude_parameters",
        },
    )

    pipeline_kvlcc2 = pipeline(
        kvlcc2.create_pipeline(model_test_ids=model_test_ids["kvlcc2"], vmms=vmms),
        namespace="kvlcc2",
        inputs=inputs,
        parameters={
            "params:thrust_channels": "params:kvlcc2.thrust_channels",
            "params:ek_covariance_input": "params:kvlcc2.ek_covariance_input",
            "params:motion_regression.exclude_parameters": "params:kvlcc2.motion_regression.exclude_parameters",
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

    return_dict["plot_wpcc"] = pipeline(
        pipeline_plot.create_pipeline(
            model_test_ids=model_test_ids["wpcc"],
            vmms=vmms,
        ),
        namespace="wpcc",
    )

    return_dict["plot_kvlcc2"] = pipeline(
        pipeline_plot.create_pipeline(
            model_test_ids=model_test_ids["kvlcc2"],
            vmms=vmms,
        ),
        namespace="kvlcc2",
    )

    return_dict["kvlcc2_captive"] = pipeline_kvlcc2_captive

    return return_dict

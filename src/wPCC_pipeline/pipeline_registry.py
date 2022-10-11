"""Project pipelines."""
from typing import Dict
from functools import reduce
from operator import add

from kedro.pipeline import Pipeline
from kedro.pipeline.modular_pipeline import pipeline
import anyconfig
import os.path

from pytest import param

from . import pipeline_ship
from .pipelines import vessel_manoeuvring_models
from .pipelines import system_matrixes
from . import pipeline_plot

from .pipelines import plot_filters

from .pipelines import load_hsva

from .pipelines import lowpass_filter_variation

#
## Full (slow)
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
    ship_names = [
        "wpcc",
        "kvlcc2_hsva",
        "USV",
    ]
    thrusts = {
        "wpcc": True,
        "kvlcc2_hsva": True,
        "USV": False,
    }
    ship_names = list(set(ship_names) & set(model_test_ids.keys()))
    ship_pipelines = {}
    for ship_name in ship_names:
        ship_pipelines[ship_name] = pipeline(
            pipeline_ship.create_pipeline(
                model_test_ids=model_test_ids[ship_name],
                vmms=vmms,
                thrust=thrusts[ship_name],
            ),
            namespace=ship_name,
            inputs=inputs,
            parameters={
                "params:thrust_channels": f"params:{ship_name}.thrust_channels",
                "params:initial.ek_covariance_input": f"params:{ship_name}.updated.initial.ek_covariance_input",
                "params:initial.ek_covariance_input": f"params:{ship_name}.initial.ek_covariance_input",
                "params:updated.ek_covariance_input": f"params:{ship_name}.updated.ek_covariance_input",
                "params:motion_regression.exclude_parameters": f"params:{ship_name}.motion_regression.exclude_parameters",
                "params:lowpass.cutoff": f"params:{ship_name}.lowpass.cutoff",
                "params:lowpass.order": f"params:{ship_name}.lowpass.order",
            },
        )

    return_dict = {}
    return_dict["__default__"] = (
        vessel_manoeuvring_models_pipeline
        + reduce(add, ek_pipelines.values())
        + ship_pipelines["wpcc"]
        + ship_pipelines["kvlcc2_hsva"]
    )
    for ship in ship_pipelines.keys():
        return_dict[ship] = (
            vessel_manoeuvring_models_pipeline
            + reduce(add, ek_pipelines.values())
            + ship_pipelines[ship]
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

    return_dict["kvlcc2_hsva_create"] = pipeline(
        load_hsva.create_pipeline(), namespace="kvlcc2_hsva"
    )
    # work_ships = ["wpcc", "LNG", "tanker2", "ropax", "LNG_tanker"]
    work_ships = [
        "wpcc",
        "kvlcc2_hsva",
        "USV",
    ]
    work_ships = list(set(work_ships) & set(model_test_ids.keys()))
    work = [return_dict[ship] for ship in work_ships]
    return_dict["work"] = reduce(add, work)
    plot = [return_dict[f"plot_{ship}"] for ship in work_ships]
    plot += [return_dict[f"plot_filters_{ship}"] for ship in work_ships]
    return_dict["plot"] = reduce(add, plot)
    lowpass_filter_variation_pipeline = pipeline(
        lowpass_filter_variation.create_pipeline(model_test_ids=model_test_ids["wpcc"]),
        namespace="wpcc",
        inputs={
            "vmm_martins_simple": "vmm_martins_simple",
            "ek": f"wpcc.vmm_martins_simple.ek",
        },
        parameters={
            "params:motion_regression.exclude_parameters": "params:wpcc.motion_regression.exclude_parameters"
        },
    )
    return_dict["lowpass_study"] = lowpass_filter_variation_pipeline
    return return_dict


## Faster...
# def register_pipelines() -> Dict[str, Pipeline]:
#    """Register the project's pipelines.
#
#    Returns:
#        A mapping from a pipeline name to a ``Pipeline`` object.
#    """
#
#    # Read configs:
#    conf_path = os.path.join(
#        os.path.split(os.path.split(os.path.dirname(__file__))[0])[0],
#        "conf",
#        "base",
#    )
#
#    runs_globals_path = os.path.join(
#        conf_path,
#        "runs_globals.yml",
#    )
#    runs_globals = anyconfig.load(runs_globals_path)
#    model_test_ids = runs_globals["model_test_ids"]
#
#    globals_path = os.path.join(
#        conf_path,
#        "globals.yml",
#    )
#    global_variables = anyconfig.load(globals_path)
#    vmms = global_variables["vmms"]
#
#    update_vmms = global_variables[
#        "update_vmms"
#    ]  # Disable update of vmm and system matrixes in globals.yml.
#
#    lowpass_filter_variation_pipeline = pipeline(
#        lowpass_filter_variation.create_pipeline(model_test_ids=model_test_ids["wpcc"]),
#        namespace="wpcc",
#        inputs={
#            "vmm_martins_simple": "vmm_martins_simple",
#            "ek": f"wpcc.vmm_martins_simple.ek",
#        },
#        parameters={
#            "params:motion_regression.exclude_parameters": "params:wpcc.motion_regression.exclude_parameters"
#        },
#    )
#
#    return_dict = {}
#    return_dict["lowpass_study"] = lowpass_filter_variation_pipeline
#
#    return return_dict

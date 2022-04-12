"""Project pipelines."""
from typing import Dict
from functools import reduce
from operator import add

from kedro.pipeline import Pipeline
from kedro.pipeline.modular_pipeline import pipeline
import anyconfig
import os.path

from . import pipeline_ship
from .pipelines import vessel_manoeuvring_models
from .pipelines import system_matrixes
from . import pipeline_plot


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

    join_globals_path = os.path.join(
        conf_path,
        "join_globals.yml",
    )
    joins = runs_globals["joins"]
    join_runs_dict = anyconfig.load(join_globals_path)

    join_runs_dict["joined"] = model_test_ids
    join_runs_dict = {join_name: join_runs_dict[join_name] for join_name in joins}
    dataset_names = list(join_runs_dict.keys())

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
        pipeline_ship.create_pipeline(ship="wpcc"),
        namespace="wpcc",
        inputs=inputs,
    )

    return_dict = {}
    return_dict["__default__"] = (
        vessel_manoeuvring_models_pipeline
        + reduce(add, ek_pipelines.values())
        + pipeline_wpcc
    )

    return_dict["plot"] = pipeline(
        pipeline_plot.create_pipeline(
            model_test_ids=model_test_ids["wpcc"],
            dataset_names=dataset_names,
            vmms=vmms,
        ),
        namespace="wpcc",
        # inputs={"ship_data": "wpcc.ship_data"},
    )

    return return_dict

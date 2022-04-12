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
    pipeline_wpcc = pipeline(
        pipeline_ship.create_pipeline(ship="wpcc"),
        namespace="wpcc",
        inputs={
            "vmm_martin": "vmm_martin",
            "vmm_martin.system_matrixes": "vmm_martin.system_matrixes",
            # "vmm_martin.ek":"vmm_martin.ek",
            # "vmm_martin.covariance_matrixes":"vmm_martin.covariance_matrixes",
        },
    )

    return_dict = {}
    return_dict["__default__"] = (
        vessel_manoeuvring_models_pipeline
        + reduce(add, ek_pipelines.values())
        + pipeline_wpcc
    )

    return return_dict

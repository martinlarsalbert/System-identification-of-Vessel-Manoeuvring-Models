"""Project pipelines."""
from typing import Dict
from functools import reduce
from operator import add

from kedro.pipeline import Pipeline
from kedro.pipeline.modular_pipeline import pipeline

from .pipelines import preprocess as preprocess
from .pipelines import brix as brix
from .pipelines import extended_kalman as extended_kalman
from .pipelines import filter_data_extended_kalman as filter_data_extended_kalman
from .pipelines import motion_regression as motion_regression
from .pipelines import prediction as prediction
from .pipelines import join_runs


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    ship_pipeline = pipeline(brix.create_pipeline() + extended_kalman.create_pipeline())

    # model_test_ids = [
    #    "22605",
    #    "22606",
    #    "22607",
    #    "22608",
    #    "22609",
    #    "22610",
    #    "22611",
    #    "22612",
    #    "22613",
    #    "22614",
    #    "22615",
    #    "22616",
    #    "22631",
    #    "22632",
    #    "22633",
    #    "22634",
    #    "22635",
    #    "22636",
    #    "22637",
    #    "22638",
    #    "22639",
    #    "22762",
    #    "22763",
    #    "22764",
    #    "22765",
    #    "22768",
    #    "22769",
    #    "22770",
    #    "22771",
    #    "22772",
    #    "22773",
    #    "22774",
    #    "22775",
    #    "22776",
    # ]
    model_test_ids = [
        "22773",
        "22774",
    ]

    model_pipelines = {}
    for model_test_id in model_test_ids:
        model_pipelines[model_test_id] = pipeline(
            preprocess.create_pipeline()
            + filter_data_extended_kalman.create_pipeline()
            + motion_regression.create_pipeline()
            + prediction.create_pipeline(),
            namespace=f"{model_test_id}",
            inputs={
                f"ek": "ek",  # (Overriding the namespace)
                f"ship_data": "ship_data",
                f"added_masses": "added_masses",
            },
        )

    jr = join_runs.create_pipeline(model_test_ids=model_test_ids)

    return_dict = {}
    return_dict["__default__"] = (
        ship_pipeline + reduce(add, model_pipelines.values()) + jr
    )
    return_dict.update(model_pipelines)
    return_dict["join_runs"] = jr

    return return_dict

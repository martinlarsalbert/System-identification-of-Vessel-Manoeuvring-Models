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


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    ship_pipeline = pipeline(brix.create_pipeline() + extended_kalman.create_pipeline())

    model_test_ids = ["22773", "22774"]
    model_pipelines = {}
    for model_test_id in model_test_ids:
        model_pipelines[model_test_id] = pipeline(
            preprocess.create_pipeline()
            + filter_data_extended_kalman.create_pipeline()
            + motion_regression.create_pipeline()
            + prediction.create_pipeline(),
            namespace=f"{model_test_id}",
            inputs={f"ek": "ek", f"ship_data": "ship_data"},
        )

    return_dict = {}
    return_dict["__default__"] = ship_pipeline + reduce(add, model_pipelines.values())
    return_dict.update(model_pipelines)

    return return_dict

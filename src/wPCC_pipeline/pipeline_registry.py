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
from .pipelines import force_regression


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

    runs_pipelines = {}
    for model_test_id in model_test_ids:
        runs_pipelines[model_test_id] = pipeline(
            preprocess.create_pipeline()
            + filter_data_extended_kalman.create_pipeline(),
            namespace=f"{model_test_id}",
            inputs={
                f"ek": "ek",  # (Overriding the namespace)
                f"ship_data": "ship_data",
                # f"added_masses": "added_masses",
            },
        )

    motion_regression_pipelines = {}
    for model_test_id in model_test_ids:
        p = pipeline(
            motion_regression.create_pipeline(),
            namespace=f"{model_test_id}",
            inputs={
                # f"ek": "ek",  # (Overriding the namespace)
                f"ship_data": "ship_data",
                f"added_masses": "added_masses",
            },
        )
        motion_regression_pipelines[model_test_id] = pipeline(
            p,
            namespace=f"motion_regression",
            inputs={
                # f"ek": "ek",  # (Overriding the namespace)
                f"ship_data": "ship_data",
                f"added_masses": "added_masses",
                f"{model_test_id}.data_ek_smooth": f"{model_test_id}.data_ek_smooth",
            },
        )

    # motion_regression_prediction_pipelines = {}
    # for model_test_id in model_test_ids:
    #    motion_regression_prediction_pipelines[model_test_id] = pipeline(
    #        prediction.create_pipeline(),
    #        namespace=f"motion_regression.{model_test_id}",
    #        inputs={
    #            # f"ek": "ek",  # (Overriding the namespace)
    #            f"ship_data": "ship_data",
    #        },
    #    )

    # joined_pipeline = pipeline(join_runs.create_pipeline(model_test_ids=model_test_ids))
    # joined_regression_pipeline = pipeline(
    #    motion_regression.create_pipeline(),
    #    inputs={
    #        f"ship_data": "ship_data",  # (Overriding the namespace)
    #        f"added_masses": "added_masses",
    #    },
    #    namespace="joined",
    # )
    #
    # joined_prediction_pipelines = {}
    # for model_test_id in model_test_ids:
    #    joined_prediction_pipelines[model_test_id] = pipeline(
    #        prediction.create_pipeline(),
    #        inputs={
    #            "motion_regression.model": "joined.motion_regression.model",
    #            f"ship_data": "ship_data",  # (Overriding the namespace)
    #            f"data_ek_smooth": f"{model_test_id}.data_ek_smooth",
    #        },
    #        namespace=f"joined.{model_test_id}",
    #    )
    #
    force_regression_pipeline = pipeline(
        force_regression.create_pipeline(),
        namespace="force_regression",
        inputs={
            f"ship_data": "ship_data",
            f"added_masses": "added_masses",
        },
    )
    #
    # force_regression_prediction_pipelines = {}
    # for model_test_id in model_test_ids:
    #    force_regression_prediction_pipelines[model_test_id] = pipeline(
    #        prediction.create_pipeline(),
    #        inputs={
    #            "motion_regression.model": "force_regression.model",
    #            f"ship_data": "ship_data",  # (Overriding the namespace)
    #            f"data_ek_smooth": f"{model_test_id}.data_ek_smooth",
    #        },
    #        namespace=f"force_regression.{model_test_id}",
    #    )

    return_dict = {}
    return_dict["__default__"] = (
        ship_pipeline
        + reduce(add, runs_pipelines.values())
        + reduce(add, motion_regression_pipelines.values())
        # + reduce(add, motion_regression_prediction_pipelines.values())
        # + joined_pipeline
        # + joined_regression_pipeline
        # + reduce(add, joined_prediction_pipelines.values())
        + force_regression_pipeline
        ## + reduce(add, force_regression_prediction_pipelines.values())
    )
    return_dict["motion_regression"] = reduce(add, motion_regression_pipelines.values())
    return_dict["force_regression"] = force_regression_pipeline
    # return_dict.update(motion_regression_pipelines)
    # return_dict["join_runs"] = joined_pipeline
    # return_dict["joined_regression"] = joined_regression_pipeline
    # return_dict["joined_prediction"] = reduce(add, joined_prediction_pipelines.values())
    # return_dict["force_regression"] = force_regression_pipeline
    # return_dict["force_regression_prediction"] = reduce(
    #    add, force_regression_prediction_pipelines.values()

    return return_dict

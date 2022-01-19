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
from .pipelines import vessel_manoeuvring_models
from .pipelines import vct_data
from wPCC_pipeline import pipelines


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    ship_pipeline = pipeline(
        brix.create_pipeline() + extended_kalman.create_pipeline(),
        inputs={
            "vmm": "vmm_martin",
        },
    )

    vct_data_pipeline = pipeline(
        vct_data.create_pipeline(), namespace="force_regression"
    )

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

    ## Preprocess model tests:
    runs_pipelines = {}
    for id in model_test_ids:
        runs_pipelines[id] = pipeline(
            preprocess.create_pipeline()
            + filter_data_extended_kalman.create_pipeline(),
            namespace=f"{id}",
            inputs={
                f"ek": "ek",  # (Overriding the namespace)
                f"ship_data": "ship_data",
            },
        )

    ## Join the tests:
    joined_pipeline = pipeline(join_runs.create_pipeline(model_test_ids=model_test_ids))

    ## Vessel Manoeuvring Models (VMMs)
    vessel_manoeuvring_models_pipeline = vessel_manoeuvring_models.create_pipeline()

    ## Motion regression pipeline:
    # "motion_regression"
    motion_regression_pipelines = {}
    motion_model_ids = model_test_ids + ["joined"]
    vmms = ["vmm_martin"]
    for vmm in vmms:
        for id in motion_model_ids:
            p = pipeline(
                motion_regression.create_pipeline(),
                namespace=f"{id}",
                inputs={
                    # f"ek": "ek",  # (Overriding the namespace)
                    f"ship_data": "ship_data",
                    f"added_masses": "added_masses",
                    f"vmm": vmm,
                },
            )
            p2 = pipeline(
                p,
                namespace=f"motion_regression",
                inputs={
                    # f"ek": "ek",  # (Overriding the namespace)
                    f"ship_data": "ship_data",
                    f"added_masses": "added_masses",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    vmm: vmm,
                },
            )
            motion_regression_pipelines[id] = pipeline(
                p2,
                namespace=vmm,
                inputs={
                    # f"ek": "ek",  # (Overriding the namespace)
                    f"ship_data": "ship_data",
                    f"added_masses": "added_masses",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    vmm: vmm,
                },
            )

    ## Force regression:
    # "force_regression"
    for vmm in vmms:
        force_regression_pipeline = pipeline(
            force_regression.create_pipeline(),
            namespace=f"{vmm}.force_regression",
            inputs={
                f"ship_data": "ship_data",
                f"added_masses": "added_masses",
                "vmm": vmm,
                "data_selected": "force_regression.data_selected",
            },
        )

    ## Predictions:
    # motion models:
    # model tests:
    prediction_pipelines = {}
    for vmm in vmms:
        for id in model_test_ids:
            p = pipeline(
                prediction.create_pipeline(),
                namespace=f"{id}",
                inputs={
                    f"ship_data": "ship_data",
                },
            )
            p2 = pipeline(
                p,
                namespace="motion_regression",
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                },
            )
            prediction_id = f"motion_regression.{id}"
            prediction_pipelines[prediction_id] = pipeline(
                p2,
                namespace=vmm,
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                },
            )
        # joined:
        for id in model_test_ids:
            p = pipeline(
                prediction.create_pipeline(),
                namespace=f"{id}",
                inputs={
                    f"ship_data": "ship_data",
                },
            )
            p2 = pipeline(
                p,
                namespace="motion_regression.joined",
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    f"{id}.model": f"{vmm}.motion_regression.joined.model",
                },
            )
            prediction_id = f"motion_regression.joined.{id}"
            prediction_pipelines[prediction_id] = pipeline(
                p2,
                namespace=vmm,
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    f"{vmm}.motion_regression.joined.model": f"{vmm}.motion_regression.joined.model",
                },
            )

        # force models:
        for id in model_test_ids:
            p = pipeline(
                prediction.create_pipeline(),
                namespace=f"{id}",
                inputs={
                    f"ship_data": "ship_data",
                },
            )
            p2 = pipeline(
                p,
                namespace="force_regression",
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    f"{id}.model": f"{vmm}.force_regression.model",
                },
            )
            prediction_id = f"force_regression.{id}"
            prediction_pipelines[prediction_id] = pipeline(
                p2,
                namespace=vmm,
                inputs={
                    f"ship_data": "ship_data",
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                    f"{vmm}.force_regression.model": f"{vmm}.force_regression.model",
                },
            )

    return_dict = {}
    return_dict["__default__"] = (
        ship_pipeline
        + reduce(add, runs_pipelines.values())
        + joined_pipeline
        + vessel_manoeuvring_models_pipeline
        + reduce(add, motion_regression_pipelines.values())
        + vct_data_pipeline
        + force_regression_pipeline
        + reduce(add, prediction_pipelines.values())
    )
    return_dict["ship"] = ship_pipeline
    return_dict["motion_regression"] = reduce(add, motion_regression_pipelines.values())
    return_dict["force_regression"] = force_regression_pipeline
    return_dict["join"] = joined_pipeline
    return_dict["predict"] = reduce(add, prediction_pipelines.values())
    return_dict["vmm"] = vessel_manoeuvring_models_pipeline

    return return_dict

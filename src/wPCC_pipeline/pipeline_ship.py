"""Project pipelines."""
from typing import Dict
from functools import reduce
from operator import add

from kedro.pipeline import Pipeline
from kedro.pipeline.modular_pipeline import pipeline


from .pipelines import preprocess as preprocess
from .pipelines import brix as brix
from .pipelines import filter_data_extended_kalman as filter_data_extended_kalman
from .pipelines import motion_regression as motion_regression
from .pipelines import prediction as prediction
from .pipelines import join_runs

from .pipelines import accuracy
from .pipelines import setup
from .pipelines import extended_kalman as extended_kalman


def create_pipeline(model_test_ids, vmms):
    """Creates a pipeline for one ship"""

    join_runs_dict = {}
    join_runs_dict["joined"] = model_test_ids
    dataset_names = list(join_runs_dict.keys())

    ########## Pipelines:

    ship_pipeline = brix.create_pipeline()
    setup_pipeline = setup.create_pipeline()

    ## Extended Kalman Filters
    ek_pipelines = {}
    for vmm in vmms:
        key = f"ek.{vmm}"
        ek_pipelines[key] = pipeline(
            extended_kalman.create_pipeline(),
            namespace=f"{vmm}",
            inputs={
                "vmm": vmm,
                "initial_parameters": "initial_parameters",
                "ship_data": "ship_data",
                "system_matrixes": f"{vmm}.system_matrixes",
            },
            parameters={"params:ek_covariance_input": "params:ek_covariance_input"},
        )

    ## Preprocess model tests:
    runs_pipelines = {}
    for id in model_test_ids:
        runs_pipelines[id] = pipeline(
            preprocess.create_pipeline(),
            namespace=f"{id}",
            inputs={
                f"ship_data": "ship_data",
            },
        )

    ## Filter:
    filter_pipelines = {}
    for id in model_test_ids:
        filter_pipelines[id] = pipeline(
            filter_data_extended_kalman.create_pipeline(),
            namespace=f"{id}",
            inputs={
                f"ek": "vmm_martin.ek",  # (Overriding the namespace)
                "covariance_matrixes": "vmm_martin.covariance_matrixes",
            },
        )

    ## Join the tests:
    joined_pipelines = {}

    # other selections:
    for dataset_name, runs_selection in join_runs_dict.items():
        joined_pipelines[dataset_name] = pipeline(
            join_runs.create_pipeline(model_test_ids=runs_selection),
            namespace=dataset_name,
            inputs={
                f"{run}.data_ek_smooth": f"{run}.data_ek_smooth"
                for run in runs_selection
            },
        )

    ## Motion regression pipeline:
    # "motion_regression"
    motion_regression_pipelines = []
    dataset_names = list(joined_pipelines.keys())

    for id in dataset_names:

        p = pipeline(
            motion_regression.create_pipeline(),
            namespace=id,
            inputs={
                f"ship_data": "ship_data",
                f"added_masses": "added_masses",
                f"vmm": "vmm",
                f"data_ek_smooth": f"{id}.data_ek_smooth",
            },
        )

        for vmm in vmms:
            p2 = pipeline(
                p,
                namespace=f"{vmm}",
                inputs={
                    f"ship_data": "ship_data",
                    f"added_masses": "added_masses",
                    "vmm": vmm,
                    f"{id}.data_ek_smooth": f"{id}.data_ek_smooth",
                },
            )

            motion_regression_pipelines.append(p2)
    #
    ## Predictions:
    # motion models:
    # model tests:
    prediction_pipelines = []

    for id in model_test_ids:

        p = pipeline(
            prediction.create_pipeline(),
            namespace=id,
            inputs={
                "data_ek_smooth": "data_ek_smooth",
                "model": f"model",
                "ek": "ek",
            },
        )

        for dataset_name in dataset_names:

            p2 = pipeline(
                p,
                namespace=dataset_name,
                inputs={
                    "data_ek_smooth": "data_ek_smooth",
                    "model": f"model",
                    "ek": "ek",
                },
            )

            for vmm in vmms:

                p3 = pipeline(
                    p2,
                    namespace=vmm,
                    inputs={
                        "data_ek_smooth": f"{id}.data_ek_smooth",
                        "model": f"{vmm}.{dataset_name}.model",
                        "ek": f"{vmm}.ek",
                    },
                )
                prediction_pipelines.append(p3)

    ## accuracy:
    accuracy_pipelines = {}

    for vmm in vmms:

        for dataset_name in join_runs_dict.keys():

            for id in model_test_ids:

                key = f"accuracy.{vmm}.{dataset_name}.{id}"
                accuracy_pipelines[key] = pipeline(
                    accuracy.create_pipeline(),
                    namespace=f"{vmm}.{dataset_name}.{id}",
                    inputs={
                        "data_ek_smooth": f"{id}.data_ek_smooth",
                        "ek": f"{vmm}.ek",
                        "model": f"{ vmm }.{ dataset_name }.model",
                        "ship_data": "ship_data",
                    },
                )

    pipeline_ship = (
        ship_pipeline
        + setup_pipeline
        + reduce(add, runs_pipelines.values())
        + reduce(add, filter_pipelines.values())
        + reduce(add, ek_pipelines.values())
        + reduce(add, joined_pipelines.values())
        + reduce(add, motion_regression_pipelines)
        + reduce(add, prediction_pipelines)
        + reduce(add, accuracy_pipelines.values())
    )

    return pipeline_ship

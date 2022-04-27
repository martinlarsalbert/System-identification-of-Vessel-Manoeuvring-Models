"""Project pipelines."""
from typing import Dict
from functools import reduce
from operator import add

from kedro.pipeline import Pipeline
from kedro.pipeline.modular_pipeline import pipeline


from .pipelines import preprocess as preprocess
from .pipelines import brix as brix

from .pipelines import prediction as prediction

from .pipelines import accuracy
from .pipelines import setup
from .pipelines import extended_kalman as extended_kalman
from . import pipeline_filter_join_regress


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

    ## initial parameters:
    inputs = {
        # "covariance_matrixes": "vmm_martin.initial.covariance_matrixes",
        f"hydrodynamic_derivatives": "initial_parameters",
        "vmm_martin.ek": "vmm_martin.ek",
        "ship_data": "ship_data",
        "added_masses": "added_masses",
    }
    inputs.update({f"{key}.data": f"{key}.data" for key in model_test_ids})
    inputs.update({f"{key}": f"{key}" for key in vmms})

    filter_join_regress_pipeline = pipeline(
        pipeline_filter_join_regress.create_pipeline(
            model_test_ids=model_test_ids, join_runs_dict=join_runs_dict, vmms=vmms
        ),
        namespace="initial",
        inputs=inputs,
        parameters={"params:ek_covariance_input": "params:initial.ek_covariance_input"},
    )

    ## updated parameters
    inputs = {
        # "covariance_matrixes": "vmm_martin.updated.covariance_matrixes",
        f"hydrodynamic_derivatives": "initial.vmm_martin.joined.derivatives",
        "vmm_martin.ek": "vmm_martin.ek",
        "ship_data": "ship_data",
        "added_masses": "added_masses",
    }
    inputs.update({f"{key}.data": f"{key}.data" for key in model_test_ids})
    inputs.update({f"{key}": f"{key}" for key in vmms})

    filter_join_regress_pipeline_updated_model = pipeline(
        pipeline_filter_join_regress.create_pipeline(
            model_test_ids=model_test_ids, join_runs_dict=join_runs_dict, vmms=vmms
        ),
        namespace="updated",
        inputs=inputs,
        parameters={"params:ek_covariance_input": "params:updated.ek_covariance_input"},
    )

    #
    ## Predictions:
    # motion models:
    # model tests:
    prediction_pipelines = []
    for update in ["initial", "updated"]:
        for id in model_test_ids:
            for dataset_name in dataset_names:
                for vmm in vmms:
                    p = pipeline(
                        prediction.create_pipeline(),
                        namespace=f"{update}.{vmm}.{dataset_name}.{id}",
                        inputs={
                            "data_ek_smooth": f"{update}.{id}.data_ek_smooth",
                            "model": f"{update}.{vmm}.{dataset_name}.model",
                            "ek": f"{vmm}.ek",
                        },
                    )
                    prediction_pipelines.append(p)

        pipeline_ship = (
            ship_pipeline
            + setup_pipeline
            + reduce(add, runs_pipelines.values())
            + reduce(add, ek_pipelines.values())
            + filter_join_regress_pipeline
            + filter_join_regress_pipeline_updated_model
            + reduce(add, prediction_pipelines)
        )

    return pipeline_ship

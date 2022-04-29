from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .pipelines import filter_data_extended_kalman
from .pipelines import join_runs
from functools import reduce
from operator import add
from .pipelines import motion_regression


def create_pipeline(
    model_test_ids, join_runs_dict, vmms, ek="vmm_abkowitz.ek", **kwargs
):

    ## Filter:
    filter_pipelines = {}
    for id in model_test_ids:
        filter_pipelines[id] = pipeline(
            filter_data_extended_kalman.create_pipeline(),
            namespace=f"{id}",
            inputs={
                # f"ek": "vmm_martin.ek",  # (Overriding the namespace)
                f"ek": ek,  # (Overriding the namespace)
                "hydrodynamic_derivatives": "hydrodynamic_derivatives",
            },
            parameters={"params:ek_covariance_input": "params:ek_covariance_input"},
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

    # Motion regression pipeline:
    "motion_regression"
    motion_regression_pipelines = []
    dataset_names = list(join_runs_dict.keys())
    for id in dataset_names:
        for vmm in vmms:
            p = pipeline(
                motion_regression.create_pipeline(),
                namespace=f"{vmm}.{id}",
                inputs={
                    f"ship_data": "ship_data",
                    f"added_masses": "added_masses",
                    "vmm": vmm,
                    f"data_ek_smooth": f"{id}.data_ek_smooth",
                },
            )
            motion_regression_pipelines.append(p)

    filter_join_regress_pipelines = (
        reduce(add, filter_pipelines.values())
        + reduce(add, joined_pipelines.values())
        + reduce(add, motion_regression_pipelines)
    )

    return filter_join_regress_pipelines

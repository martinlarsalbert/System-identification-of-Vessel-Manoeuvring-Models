from kedro.pipeline.modular_pipeline import pipeline
from .pipelines import plot as plot
from functools import reduce
from operator import add


def create_pipeline(model_test_ids, vmms):

    join_runs_dict = {}
    join_runs_dict["joined"] = model_test_ids
    dataset_names = list(join_runs_dict.keys())

    prediction_pipelines = []

    for id in model_test_ids:

        p = pipeline(
            plot.create_pipeline(),
            namespace=id,
            inputs={
                "data_ek_smooth": "data_ek_smooth",
                "raw_data": "raw_data",
                "data_resimulate": "data_resimulate",
                "ship_data": "ship_data",
            },
        )

        for dataset_name in dataset_names:

            p2 = pipeline(
                p,
                namespace=dataset_name,
                inputs={
                    "data_ek_smooth": "data_ek_smooth",
                    "raw_data": "raw_data",
                    "data_resimulate": "data_resimulate",
                    "ship_data": "ship_data",
                },
            )

            for vmm in vmms:

                p3 = pipeline(
                    p2,
                    namespace=vmm,
                    inputs={
                        "data_ek_smooth": f"{id}.data_ek_smooth",
                        "raw_data": f"{id}.raw_data",
                        "data_resimulate": f"{vmm}.{dataset_name}.{id}.data_resimulate",
                        "ship_data": "ship_data",
                    },
                )
                prediction_pipelines.append(p3)

    return reduce(add, prediction_pipelines)

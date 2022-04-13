"""
This is a boilerplate pipeline 'kvlcc2'
generated using Kedro 0.17.6
"""
from kedro.pipeline.modular_pipeline import pipeline
from kedro.pipeline import Pipeline, node
from wPCC_pipeline import pipeline_ship
from .nodes import load
from functools import reduce
from operator import add


def create_pipeline(model_test_ids, vmms, **kwargs):

    ## Trying to run kvlcc2 in the same pipeline by adding a simple preprocessor

    ship_pipeline = pipeline_ship.create_pipeline(
        model_test_ids=model_test_ids, vmms=vmms
    )

    preprocess = Pipeline(
        [
            node(
                func=load,
                inputs=["raw_data_unformated", "ship_data"],
                outputs="raw_data",
                name="transform_node",
                tags=["preprocess"],
            ),
        ]
    )

    preprocessors = []

    for id in model_test_ids:
        p = pipeline(preprocess, namespace=id, inputs={"ship_data": "ship_data"})
        preprocessors.append(p)

    return reduce(add, preprocessors) + ship_pipeline

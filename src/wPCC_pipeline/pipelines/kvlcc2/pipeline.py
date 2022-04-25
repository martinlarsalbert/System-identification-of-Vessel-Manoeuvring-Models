"""
This is a boilerplate pipeline 'kvlcc2'
generated using Kedro 0.17.6
"""
from kedro.pipeline.modular_pipeline import pipeline
from kedro.pipeline import Pipeline, node
from wPCC_pipeline import pipeline_ship
from .nodes import load, fit_propeller_characteristics, calculate_thrust
from functools import reduce
from operator import add


def create_pipeline(model_test_ids, vmms, **kwargs):

    ## Trying to run kvlcc2 in the same pipeline by adding a simple preprocessor

    ship_pipeline = pipeline_ship.create_pipeline(
        model_test_ids=model_test_ids, vmms=vmms
    )

    propeller = Pipeline(
        [
            node(
                func=fit_propeller_characteristics,
                inputs=["open_water_characteristics"],
                outputs="propeller_coefficients",
                name="fit_propeller_characteristics_node",
                tags=["preprocess"],
            ),
            node(
                func=fit_propeller_characteristics,
                inputs=["open_water_characteristics_captive"],
                outputs="propeller_coefficients_captive",
                name="fit_propeller_characteristics_captive_node",
                tags=["preprocess"],
            ),
        ]
    )

    preprocess = Pipeline(
        [
            node(
                func=load,
                inputs=["raw_data_unformated", "ship_data"],
                outputs="raw_data_",
                name="transform_node",
                tags=["preprocess", "filter"],
            ),
            node(
                func=calculate_thrust,
                inputs=["raw_data_", "ship_data", "propeller_coefficients"],
                outputs="raw_data",
                name="calculate_thrust_node",
                tags=["preprocess", "filter"],
            ),
        ]
    )

    preprocessors = []

    for id in model_test_ids:
        p = pipeline(
            preprocess,
            namespace=id,
            inputs={
                "ship_data": "ship_data",
                "propeller_coefficients": "propeller_coefficients",
            },
        )
        preprocessors.append(p)

    return propeller + reduce(add, preprocessors) + ship_pipeline

"""
This is a boilerplate pipeline 'captive'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node

from .nodes import load, prime2_derivatives_to_prime1


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=load,
                inputs=["captive_prime", "ship_data"],
                outputs="captive",
                name="captive_load_node",
                tags=["preprocess"],
            ),
            node(
                func=prime2_derivatives_to_prime1,
                inputs=["derivatives_prime2", "ship_data"],
                outputs="derivatives",
                name="prime2_derivatives_to_prime1_node",
                tags=["preprocess"],
            ),
        ]
    )

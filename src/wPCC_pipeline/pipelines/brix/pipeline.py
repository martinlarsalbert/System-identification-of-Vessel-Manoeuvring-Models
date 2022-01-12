"""
This is a boilerplate pipeline 'brix'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import initial_parameters


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=initial_parameters,
                inputs=["ship_data"],
                outputs="initial_parameters",
                name="initial_parameters_node",
            )
        ]
    )

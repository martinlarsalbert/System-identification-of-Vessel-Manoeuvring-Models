"""
This is a boilerplate pipeline 'prediction'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import simulate


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=simulate,
                inputs=["data", "model_motion_regression"],
                outputs="data_resimulate_model_motion",
                name="simulate_node",
            ),
        ]
    )

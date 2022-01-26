"""
This is a boilerplate pipeline 'ek'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    create_extended_kalman,
    guess_covariance_matrixes,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=create_extended_kalman,
                inputs=["initial_parameters", "ship_data", "vmm"],
                outputs="ek",
                name="create_extended_kalman_node",
            ),
            node(
                func=guess_covariance_matrixes,
                inputs=[],
                outputs="covariance_matrixes",
                name="guess_covariance_matrixes_node",
            ),
        ]
    )

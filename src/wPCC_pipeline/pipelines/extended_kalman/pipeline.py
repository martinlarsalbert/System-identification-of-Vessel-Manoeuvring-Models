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
                inputs=["initial_parameters", "ship_data", "vmm", "system_matrixes"],
                outputs="ek",
                name="create_extended_kalman_node",
                tags=["ek"],
            ),
            node(
                func=guess_covariance_matrixes,
                inputs=["params:ek_covariance_input"],
                outputs="covariance_matrixes",
                name="guess_covariance_matrixes_node",
                tags=["ek"],
            ),
        ]
    )

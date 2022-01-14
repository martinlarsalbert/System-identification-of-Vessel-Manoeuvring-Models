"""
This is a boilerplate pipeline 'ek'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    create_extended_kalman,
    resimulate_extended_kalman,
    extended_kalman_filter,
    extended_kalman_smoother,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=create_extended_kalman,
                inputs=["initial_parameters", "ship_data"],
                outputs="ek",
                name="create_extended_kalman_node",
            ),
            node(
                func=resimulate_extended_kalman,
                inputs=["ek", "data"],
                outputs="data_resimulate_extended_kalman",
                name="resimulate_extended_kalman_node",
            ),
            node(
                func=extended_kalman_filter,
                inputs=["ek", "data"],
                outputs=["ek_filtered", "data_ek_filter"],
                name="extended_kalman_filter_node",
            ),
            node(
                func=extended_kalman_smoother,
                inputs=["ek_filtered"],
                outputs=["ek_smooth", "data_ek_smooth"],
                name="extended_kalman_smoother_node",
            ),
        ]
    )

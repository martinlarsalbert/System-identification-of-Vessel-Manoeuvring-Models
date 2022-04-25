"""
This is a boilerplate pipeline 'filter_data_extended_kalman'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    resimulate_extended_kalman,
    initial_state,
    extended_kalman_filter,
    extended_kalman_smoother,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            # node(
            #    func=resimulate_extended_kalman,
            #    inputs=["ek", "data"],
            #    outputs="data_resimulate_extended_kalman",
            #    name="resimulate_extended_kalman_node",
            # ),
            node(
                func=initial_state,
                inputs=["data"],  # (data has the raw positions)
                outputs="x0",
                name="initial_state_node",
                tags=["ek", "filter"],
            ),
            node(
                func=extended_kalman_filter,
                inputs=[
                    "ek",
                    "data",
                    "covariance_matrixes",
                    "x0",
                    "hydrodynamic_derivatives",
                ],
                outputs=["ek_filtered", "data_ek_filter", "time_steps"],
                name="extended_kalman_filter_node",
                tags=["ek", "filter"],
            ),
            node(
                func=extended_kalman_smoother,
                inputs=[
                    "ek_filtered",
                    "data",  # (data has the raw positions)
                    "time_steps",
                    "covariance_matrixes",
                    "hydrodynamic_derivatives",
                ],
                outputs=["ek_smooth", "data_ek_smooth"],
                name="extended_kalman_smoother_node",
                tags=["ek", "filter"],
            ),
        ]
    )

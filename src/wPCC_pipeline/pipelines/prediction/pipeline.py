"""
This is a boilerplate pipeline 'prediction'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    simulate,
    simulate_with_time_out,
    simulate_euler,
    damping_forces,
    simulation_accuracy,
    monte_carlo,
)


def create_pipeline(**kwargs):

    return Pipeline(
        [
            node(
                func=simulate_euler,
                inputs=[
                    "data_ek_smooth",  # Which data to use here is not obvious...
                    "model",
                    "ek",
                ],
                outputs="data_resimulate",
                name="simulate_node",
                tags=["predict"],
            ),
            # node(
            #    func=damping_forces,
            #    inputs=[
            #        "force_regression.data_scaled_resistance_corrected",
            #        "model",
            #    ],
            #    outputs="data_damping_forces",
            #    name="damping_forces_node",
            #    tags=["predict"],
            # ),
            node(
                func=simulation_accuracy,
                # inputs=["data", "data_resimulate_model_motion"],
                inputs=["data_ek_smooth", "data_resimulate"],
                outputs="simulation_accuracy",
                name="simulation_accuracy_node",
            ),
        ]
    )

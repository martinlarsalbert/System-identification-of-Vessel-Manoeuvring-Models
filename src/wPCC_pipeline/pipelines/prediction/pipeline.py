"""
This is a boilerplate pipeline 'prediction'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    simulate,
    simulate_with_time_out,
    simulate_euler,
    track_plot,
    plot_timeseries,
    damping_forces,
    simulation_accuracy,
)


def create_pipeline(track_plot=True, data_name: str = "data_ek_smooth", **kwargs):

    items = [
        # node(
        #    func=simulate,
        #    # inputs=["data", "model_motion_regression"],
        #    inputs=[
        #        data_name,  # Which data to use here is not obvious...
        #        "model",
        #    ],
        #    outputs="data_resimulate",
        #    name="simulate_node",
        #    tags=["predict"],
        # ),
        node(
            func=simulate_euler,
            inputs=[
                data_name,  # Which data to use here is not obvious...
                "model",
                "ek",
            ],
            outputs="data_resimulate",
            name="simulate_node",
            tags=["predict"],
        ),
        node(
            func=damping_forces,
            inputs=[
                "force_regression.data_scaled_resistance_corrected",
                "model",
            ],
            outputs="data_damping_forces",
            name="damping_forces_node",
            tags=["predict"],
        ),
    ]

    if track_plot:
        items += [
            node(
                func=track_plot,
                # inputs=["data", "data_resimulate_model_motion", "ship_data"],
                inputs=[data_name, "data_resimulate", "ship_data"],
                outputs="track_plot_resimulate",
                name="resimulate_track_plot_node",
                tags=["plot", "track_plot"],
            ),
        ]

    items += [
        node(
            func=plot_timeseries,
            # inputs=["data", "data_resimulate_model_motion"],
            inputs=[data_name, "data_resimulate", "ship_data"],
            outputs="plot_resimulate",
            name="resimulate_plot_node",
            tags=["plot"],
        ),
        node(
            func=simulation_accuracy,
            # inputs=["data", "data_resimulate_model_motion"],
            inputs=[data_name, "data_resimulate"],
            outputs="simulation_accuracy",
            name="simulation_accuracy_node",
        ),
    ]

    return Pipeline(items)

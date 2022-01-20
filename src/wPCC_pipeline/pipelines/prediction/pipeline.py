"""
This is a boilerplate pipeline 'prediction'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import simulate, track_plot, plot_timeseries, damping_forces


def create_pipeline(data_name: str = "data_ek_smooth", **kwargs):
    return Pipeline(
        [
            node(
                func=simulate,
                # inputs=["data", "model_motion_regression"],
                inputs=[
                    data_name,  # Which data to use here is not obvious...
                    "model",
                ],
                outputs="data_resimulate",
                name="simulate_node",
            ),
            node(
                func=damping_forces,
                inputs=[
                    "force_regression.data_scaled",
                    "model",
                ],
                outputs="data_damping_forces",
                name="damping_forces_node",
            ),
            node(
                func=track_plot,
                # inputs=["data", "data_resimulate_model_motion", "ship_data"],
                inputs=[data_name, "data_resimulate", "ship_data"],
                outputs="track_plot_resimulate",
                name="resimulate_track_plot_node",
            ),
            node(
                func=plot_timeseries,
                # inputs=["data", "data_resimulate_model_motion"],
                inputs=[data_name, "data_resimulate"],
                outputs="plot_resimulate",
                name="resimulate_plot_node",
            ),
        ]
    )

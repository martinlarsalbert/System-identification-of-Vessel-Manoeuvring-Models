"""
This is a boilerplate pipeline 'prediction'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import simulate, track_plot, plot_timeseries


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=simulate,
                # inputs=["data", "model_motion_regression"],
                inputs=[
                    "data_ek_smooth",  # Which data to use here is not obvious...
                    "model_motion_regression",
                ],
                outputs="data_resimulate_model_motion",
                name="simulate_node",
            ),
            node(
                func=track_plot,
                # inputs=["data", "data_resimulate_model_motion", "ship_data"],
                inputs=["data_ek_smooth", "data_resimulate_model_motion", "ship_data"],
                outputs="track_plot_resimulate_model_motion",
                name="resimulate_track_plot_node",
            ),
            node(
                func=plot_timeseries,
                # inputs=["data", "data_resimulate_model_motion"],
                inputs=["data_ek_smooth", "data_resimulate_model_motion"],
                outputs="plot_resimulate_model_motion",
                name="resimulate_plot_node",
            ),
        ]
    )

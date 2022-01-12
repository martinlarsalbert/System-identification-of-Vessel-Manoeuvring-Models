"""
This is a boilerplate pipeline 'lowpass'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import load, track_plot, add_thrust, filter


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(func=load, inputs=["raw_data"], outputs="data", name="load_node"),
            node(
                func=add_thrust,
                inputs=["data", "params:thrust_channels"],
                outputs="data_with_thrust",
                name="add_thrust_node",
            ),
            node(
                func=track_plot,
                inputs=["data", "ship_data"],
                outputs="track_plot",
                name="track_plot_node",
            ),
            node(
                func=filter,
                inputs=["data_with_thrust", "params:lowpass"],
                outputs="data_lowpass",
                name="lowpass_filter_node",
            ),
        ]
    )

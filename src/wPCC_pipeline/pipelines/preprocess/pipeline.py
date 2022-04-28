"""
This is a boilerplate pipeline 'lowpass'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import load, track_plot, add_thrust, filter, assemble_data


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=load,
                inputs=["raw_data"],
                outputs="raw_data2",
                name="load_node",
                tags=["filter"],
            ),
            node(
                func=add_thrust,
                inputs=["raw_data2", "params:thrust_channels"],
                # outputs="data_with_thrust",
                outputs="data",
                name="add_thrust_node",
                tags=["filter"],
            ),
            node(
                func=track_plot,
                inputs=["raw_data2", "ship_data"],
                outputs="track_plot",
                name="track_plot_node",
                # tags=["filter"],
            ),
            node(
                func=filter,
                inputs=[
                    "data",
                    "params:lowpass.cutoff",
                    "params:lowpass.order",
                ],
                outputs="data_lowpass",
                name="lowpass_filter_node",
                tags=["filter"],
            ),
            # node(
            #    func=assemble_data,
            #    inputs=["data_lowpass", "raw_data"],
            #    outputs="data",
            #    name="assemble_data_node",
            #    tags=["filter"],
            # ),
        ]
    )

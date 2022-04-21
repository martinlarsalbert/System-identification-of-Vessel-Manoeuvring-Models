"""
This is a boilerplate pipeline 'plot'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    track_plot,
    plot_timeseries,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=track_plot,
                inputs=["raw_data", "data_resimulate", "ship_data"],
                outputs="track_plot_resimulate",
                name="resimulate_track_plot_node",
                tags=["plot", "track_plot"],
            ),
            node(
                func=plot_timeseries,
                # inputs=["data", "data_resimulate_model_motion"],
                inputs=["data_ek_smooth", "data_resimulate", "ship_data", "raw_data"],
                outputs="plot_resimulate",
                name="resimulate_plot_node",
                tags=["plot"],
            ),
        ]
    )

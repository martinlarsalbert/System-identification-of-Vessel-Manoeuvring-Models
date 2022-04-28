"""
This is a boilerplate pipeline 'plot_filters'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    plot_filters,
)


def create_pipeline(model_test_ids, **kwargs):

    nodes = []

    for id in model_test_ids:
        node_ = node(
            func=plot_filters,
            inputs=[
                f"initial.{id}.data_ek_smooth",
                f"updated.{id}.data_ek_smooth",
                f"{id}.data_lowpass",
            ],
            outputs=f"{id}.plot_filters",
            name=f"plot_filters_node_{id}",
            tags=["plot"],
        )
        nodes.append(node_)

    return Pipeline(nodes)

"""
This is a boilerplate pipeline 'generic_data'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import generate_data1, generate_data2, add_noise, get_ship_data


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=generate_data1,
                inputs=[],
                outputs="tanker.simulation1.true_data",
                name="generate_data_node1",
                tags=["generic_data"],
            ),
            node(
                func=add_noise,
                inputs=["tanker.simulation1.true_data", "params:tanker.noises"],
                outputs="tanker.simulation1.raw_data",
                name="add_noise_node1",
                tags=["generic_data"],
            ),
            node(
                func=generate_data2,
                inputs=[],
                outputs="tanker.simulation2.true_data",
                name="generate_data_node2",
                tags=["generic_data"],
            ),
            node(
                func=add_noise,
                inputs=["tanker.simulation2.true_data", "params:tanker.noises"],
                outputs="tanker.simulation2.raw_data",
                name="add_noise_node2",
                tags=["generic_data"],
            ),
            node(
                func=get_ship_data,
                inputs=[],
                outputs="tanker.ship_data",
                name="get_ship_data_node",
                tags=["generic_data"],
            ),
        ]
    )

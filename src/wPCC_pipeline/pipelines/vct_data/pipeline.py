"""
This is a boilerplate pipeline 'vct_data'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import select_vct_data


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=select_vct_data,
                inputs=["data"],
                outputs="data_selected",
                name="select_vct_data_node",
                tags=["force_regression"],
            ),
        ]
    )

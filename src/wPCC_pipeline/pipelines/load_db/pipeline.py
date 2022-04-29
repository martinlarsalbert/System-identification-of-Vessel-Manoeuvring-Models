"""
This is a boilerplate pipeline 'load_db'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import create_ship_data, load_runs


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=create_ship_data,
                inputs=[
                    "runs_meta_data_raw",
                ],
                outputs="ship_data",
                name="create_ship_data_node",
                tags=["create_ship"],
            ),
            node(
                func=load_runs,
                inputs=[
                    "runs_meta_data_raw",
                ],
                outputs="db_runs",
                name="load_runs_node",
                tags=["create_ship"],
            ),
        ]
    )

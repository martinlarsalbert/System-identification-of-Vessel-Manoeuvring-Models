"""
This is a boilerplate pipeline 'load_hsva'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    load_runs,
    create_run_yml,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=load_runs,
                inputs=[
                    "raw_data_hsva",
                ],
                outputs="db_runs",
                name="load_runs_node",
                tags=["create_ship"],
            ),
            node(
                func=create_run_yml,
                inputs=[
                    "raw_data_hsva",
                ],
                outputs="run_yml",
                name="create_run_yml_node",
                tags=["create_ship"],
            ),
        ]
    )

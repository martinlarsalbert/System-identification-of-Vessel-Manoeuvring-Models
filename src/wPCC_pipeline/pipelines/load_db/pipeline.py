"""
This is a boilerplate pipeline 'load_db'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    create_ship_data,
    load_runs,
    get_project_meta_data,
    select_runs,
    create_run_yml,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=get_project_meta_data,
                inputs=[
                    "params:ship",
                ],
                outputs="project_meta_data",
                name="get_project_meta_data_node",
                tags=["create_ship"],
            ),
            node(
                func=select_runs,
                inputs=[
                    "project_meta_data",
                ],
                outputs="runs_meta_data_raw",
                name="select_runs_node",
                tags=["create_ship"],
            ),
            node(
                func=create_ship_data,
                inputs=[
                    "runs_meta_data_raw",
                    "params:ship",
                ],
                outputs="ship_data",
                name="create_ship_data_node",
                tags=["create_ship"],
            ),
            node(
                func=load_runs,
                inputs=[
                    "runs_meta_data_raw",
                    "params:ship",
                ],
                outputs="db_runs",
                name="load_runs_node",
                tags=["create_ship"],
            ),
            node(
                func=create_run_yml,
                inputs=[
                    "runs_meta_data_raw",
                ],
                outputs="run_yml",
                name="create_run_yml_node",
                tags=["create_ship"],
            ),
        ]
    )

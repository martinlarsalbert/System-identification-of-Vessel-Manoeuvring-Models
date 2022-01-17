"""
This is a boilerplate pipeline 'join_runs'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import join


def create_pipeline(model_test_ids: list, **kwargs):
    return Pipeline(
        [
            node(
                func=join,
                inputs=[f"{run}.data_ek_smooth" for run in model_test_ids],
                outputs="data_ek_smooth_joined",
                name="join_node",
            ),
        ]
    )

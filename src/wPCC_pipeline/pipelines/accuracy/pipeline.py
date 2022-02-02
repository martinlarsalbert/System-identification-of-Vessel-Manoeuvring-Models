"""
This is a boilerplate pipeline 'accuracy'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    online_prediction,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=online_prediction,
                # inputs=["data", "model_motion_regression"],
                inputs=[
                    "data_ek_smooth",
                    "ek",
                ],
                outputs="data_online_predict",
                name="online_prediction_node",
                tags=["predict"],
            ),
        ]
    )

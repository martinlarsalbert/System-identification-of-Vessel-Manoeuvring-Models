"""
This is a boilerplate pipeline 'accuracy'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    online_prediction,
    online_acceleration_prediction,
    online_prediction_rmse,
    online_acceleration_prediction_rmse,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=online_acceleration_prediction,
                inputs=[
                    "data_ek_smooth",
                    "ek",
                    "model",
                ],
                outputs="data_online_predict",
                name="online_prediction_node",
                tags=["accuracy"],
            ),
            node(
                func=online_acceleration_prediction_rmse,
                inputs=["data_online_predict", "data_ek_smooth", "ship_data"],
                outputs="online_prediction_rmse",
                name="online_prediction_rmse_node",
                tags=["accuracy"],
            ),
        ]
    )

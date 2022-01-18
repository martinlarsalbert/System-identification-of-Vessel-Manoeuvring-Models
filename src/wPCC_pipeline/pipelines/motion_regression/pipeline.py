"""
This is a boilerplate pipeline 'motion_regression'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    fit_motions,
    create_model_from_motion_regression,
    motion_regression_summaries,
    motion_regression_plots,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=fit_motions,
                inputs=["data_ek_smooth", "added_masses", "ship_data"],
                outputs=["motion_regression", "motion_regression.parameters"],
                name="fit_motions_node",
                tags=["motion_regression"],
            ),
            node(
                func=motion_regression_summaries,
                inputs=["motion_regression"],
                outputs=[
                    "motion_regression.summary_X",
                    "motion_regression.summary_Y",
                    "motion_regression.summary_N",
                ],
                name="motion_regression_summaries_node",
                tags=["motion_regression"],
            ),
            node(
                func=motion_regression_plots,
                inputs=["motion_regression"],
                outputs=[
                    "motion_regression.plot_X",
                    "motion_regression.plot_Y",
                    "motion_regression.plot_N",
                ],
                name="motion_regression_plots_node",
                tags=["motion_regression"],
            ),
            node(
                func=create_model_from_motion_regression,
                inputs=["motion_regression"],
                outputs="motion_regression.model",
                name="create_model_from_motion_regression_node",
                tags=["motion_regression"],
            ),
        ]
    )

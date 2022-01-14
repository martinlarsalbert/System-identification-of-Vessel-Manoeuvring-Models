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
                outputs=["motion_regression", "motion_regression_parameters"],
                name="fit_motions_node",
            ),
            node(
                func=motion_regression_summaries,
                inputs=["motion_regression"],
                outputs=[
                    "motion_regression_summary_X",
                    "motion_regression_summary_Y",
                    "motion_regression_summary_N",
                ],
                name="motion_regression_summaries_node",
            ),
            node(
                func=motion_regression_plots,
                inputs=["motion_regression"],
                outputs=[
                    "motion_regression_plot_X",
                    "motion_regression_plot_Y",
                    "motion_regression_plot_N",
                ],
                name="motion_regression_plots_node",
            ),
            node(
                func=create_model_from_motion_regression,
                inputs=["motion_regression"],
                outputs="model_motion_regression",
                name="create_model_from_motion_regression_node",
            ),
        ]
    )

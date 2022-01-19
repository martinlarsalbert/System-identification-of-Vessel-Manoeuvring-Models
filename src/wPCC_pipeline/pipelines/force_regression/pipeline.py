"""
This is a boilerplate pipeline 'force_regression'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    select_vct_data,
    fit_forces,
    create_model_from_force_regression,
    force_regression_summaries,
    force_regression_plots,
)


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
            node(
                func=fit_forces,
                inputs=["data_selected", "added_masses", "ship_data", "vmm"],
                outputs=["regression", "derivatives"],
                name="fit_forces_node",
                tags=["force_regression"],
            ),
            node(
                func=force_regression_summaries,
                inputs=["regression"],
                outputs=[
                    "summary_X",
                    "summary_Y",
                    "summary_N",
                ],
                name="force_regression_summaries_node",
                tags=["force_regression"],
            ),
            node(
                func=force_regression_plots,
                inputs=["regression"],
                outputs=[
                    "plot_X",
                    "plot_Y",
                    "plot_N",
                ],
                name="force_regression_plots_node",
                tags=["force_regression"],
            ),
            node(
                func=create_model_from_force_regression,
                inputs=["regression"],
                outputs="model",
                name="create_model_from_force_regression_node",
                tags=["force_regression"],
            ),
        ]
    )

"""
This is a boilerplate pipeline 'force_regression'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    fit_forces,
    create_model_from_force_regression,
    force_regression_summaries,
    force_regression_plots,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=fit_forces,
                inputs=["data_vct", "added_masses", "ship_data"],
                outputs=["force_regression", "force_regression.parameters"],
                name="fit_forces_node",
                tags=["force_regression"],
            ),
            node(
                func=force_regression_summaries,
                inputs=["force_regression"],
                outputs=[
                    "force_regression.summary_X",
                    "force_regression.summary_Y",
                    "force_regression.summary_N",
                ],
                name="force_regression_summaries_node",
                tags=["force_regression"],
            ),
            node(
                func=force_regression_plots,
                inputs=["force_regression"],
                outputs=[
                    "force_regression.plot_X",
                    "force_regression.plot_Y",
                    "force_regression.plot_N",
                ],
                name="force_regression_plots_node",
                tags=["force_regression"],
            ),
            node(
                func=create_model_from_force_regression,
                inputs=["force_regression"],
                outputs="force_regression.model",
                name="create_model_from_force_regression_node",
                tags=["force_regression"],
            ),
        ]
    )

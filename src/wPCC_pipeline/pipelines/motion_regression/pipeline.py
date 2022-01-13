"""
This is a boilerplate pipeline 'motion_regression'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import fit_motions


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=fit_motions,
                inputs=["data_ek_smooth", "added_masses", "ship_data"],
                outputs=["motion_regression", "motion_regression_parameters"],
                name="fit_motions_node",
            ),
        ]
    )

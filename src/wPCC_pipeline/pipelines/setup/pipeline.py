"""
This is a boilerplate pipeline 'setup'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import add_run_description, fit_propeller_characteristics


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=add_run_description,
                inputs="runs_meta_data_raw",
                outputs="runs_meta_data",
                name="add_run_description_node",
            ),
            node(
                func=fit_propeller_characteristics,
                inputs="open_water_characteristics",
                outputs="propeller_coefficients",
                name="fit_propeller_characteristics_node",
                tags=["setup"],
            ),
        ]
    )

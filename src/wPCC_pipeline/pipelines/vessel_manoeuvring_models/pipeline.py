"""
This is a boilerplate pipeline 'vessel_manoeuvring_models'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node

from .nodes import martins_model


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=martins_model,
                inputs=[],
                outputs="vmm_martin",
                name="martins_model_node",
                tags=["vessel_manoeuvring_models"],
            ),
        ]
    )

"""
This is a boilerplate pipeline 'vmm'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    martins_model,
    vmm_linear,
    vmm_martins_simple_model,
    vmm_abkowitz_model,
    vmm_abkowitz_expanded,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=martins_model,
                inputs=[],
                outputs="vmm_martin",
                name="martins_model_node",
                tags=["vmm"],
            ),
            node(
                func=vmm_linear,
                inputs=[],
                outputs="vmm_linear",
                name="vmm_linear_node",
                tags=["vmm"],
            ),
            node(
                func=vmm_martins_simple_model,
                inputs=[],
                outputs="vmm_martins_simple",
                name="vmm_martins_simple_model_node",
                tags=["vmm"],
            ),
            node(
                func=vmm_abkowitz_model,
                inputs=[],
                outputs="vmm_abkowitz",
                name="vmm_abkowitz_model_node",
                tags=["vmm"],
            ),
            node(
                func=vmm_abkowitz_expanded,
                inputs=[],
                outputs="vmm_abkowitz_expanded",
                name="vmm_abkowitz_expanded_node",
                tags=["vmm"],
            ),
        ]
    )

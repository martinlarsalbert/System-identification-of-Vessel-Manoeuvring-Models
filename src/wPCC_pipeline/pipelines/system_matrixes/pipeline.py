"""
This is a boilerplate pipeline 'system_matrixes'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    create_system_matrixes,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=create_system_matrixes,
                inputs=["vmm"],
                outputs="system_matrixes",
                name="create_system_matrixes_node",
                tags=["ek", "vmm"],
            ),
        ]
    )

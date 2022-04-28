"""
This is a boilerplate pipeline 'generic_data2'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import add_noise


def create_pipeline(model_test_ids, **kwargs):

    pipeline = []
    for id in model_test_ids["kvlcc2"]:
        node_ = node(
            func=add_noise,
            inputs=[
                f"kvlcc2.updated.vmm_abkowitz.joined.{id}.data_resimulate",
                "params:generic_kvlcc2.noises",
            ],
            outputs=[
                f"generic_kvlcc2.{id}.true_data",
                f"generic_kvlcc2.{id}.raw_data",
            ],
            name=f"{id}_add_noise_node",
        )

        pipeline.append(node_)

    return Pipeline(pipeline)

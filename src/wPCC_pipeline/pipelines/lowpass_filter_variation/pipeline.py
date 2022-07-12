"""
This is a boilerplate pipeline 'lowpass_filter_variation'
generated using Kedro 0.17.6
"""

from kedro.pipeline import Pipeline, node
from .nodes import (
    vary_cuttoff,
    join,
    regression,
    simulate,
    dataset_dummy,
    accuracy,
    accuracy_ekf,
)


def create_pipeline(model_test_ids: dict, **kwargs):

    datasets_raw = {id: f"{ id }.data" for id in model_test_ids}
    datasets_ek_smooth = {id: f"updated.{ id }.data_ek_smooth" for id in model_test_ids}
    datas_resimulate = {
        id: f"updated.vmm_martins_simple.joined.{ id }.data_resimulate"
        for id in model_test_ids
    }

    return Pipeline(
        [
            node(
                func=vary_cuttoff,
                inputs=datasets_raw,
                outputs="lowpass_variation",
                tags=["lowpass"],
            ),
            node(
                func=join,
                inputs="lowpass_variation",
                outputs="lowpass_variation_joined",
                tags=["lowpass", "join"],
            ),
            node(
                func=regression,
                inputs=[
                    "lowpass_variation_joined",
                    "added_masses",
                    "ship_data",
                    "vmm_martins_simple",
                    "params:motion_regression.exclude_parameters",
                ],
                outputs=["lowpass_regression", "lowpass_model"],
                tags=["lowpass", "regression"],
            ),
            node(
                func=dataset_dummy,
                inputs=datasets_ek_smooth,
                outputs="datasets_ek_smooth",
                tags=["lowpass", "simulate", "dummy"],
            ),
            node(
                func=simulate,
                inputs=[
                    "lowpass_model",
                    "datasets_ek_smooth",
                    "ek",
                ],
                outputs="lowpass_simulation",
                tags=["lowpass", "simulate"],
            ),
            node(
                func=dataset_dummy,
                inputs=datasets_raw,
                outputs="raw_data_all",
                tags=["lowpass", "accuracy", "dummy"],
            ),
            node(
                func=accuracy,
                inputs=["lowpass_simulation", "raw_data_all"],
                outputs="r2_lowpass",
                tags=["lowpass", "accuracy", "dummy"],
            ),
            node(
                func=dataset_dummy,
                inputs=datas_resimulate,
                outputs="ekf_simulation",
                tags=["lowpass", "accuracy", "dummy"],
            ),
            node(
                func=accuracy_ekf,
                inputs=["ekf_simulation", "raw_data_all"],
                outputs="r2_EKF",
                tags=["lowpass", "accuracy", "dummy"],
            ),
        ]
    )

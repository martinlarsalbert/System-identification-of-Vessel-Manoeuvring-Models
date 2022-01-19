"""
This is a boilerplate pipeline 'vct_data'
generated using Kedro 0.17.6
"""
import pandas as pd

from src.vct_scaling import scale_force_to_model_scale, scale_moment_to_model_scale


def select_vct_data(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("model_name").get_group("V2_5_MDL_modelScale")


def vct_scaling(data: pd.DataFrame, ship_data: dict) -> pd.DataFrame:

    data_scaled = data.copy()

    keys_forces = ["fx", "fy", "fz"]
    scale_factor = ship_data["scale_factor"]
    forces = data_scaled[keys_forces]
    data_scaled[keys_forces] = scale_force_to_model_scale(
        forces=forces, scale_factor=scale_factor, **data_scaled
    )
    keys_moments = ["mx", "my", "mz"]
    data_scaled[keys_moments] = scale_force_to_model_scale(
        data_scaled[keys_moments], scale_factor=scale_factor, **data_scaled
    )

    return data_scaled

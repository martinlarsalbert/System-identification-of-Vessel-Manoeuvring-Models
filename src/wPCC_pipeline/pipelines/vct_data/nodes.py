"""
This is a boilerplate pipeline 'vct_data'
generated using Kedro 0.17.6
"""
import pandas as pd
import numpy as np

from src.vct_scaling import scale_force_to_model_scale, scale_moment_to_model_scale
from scipy.optimize import least_squares


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
    data_scaled[keys_moments] = scale_moment_to_model_scale(
        data_scaled[keys_moments], scale_factor=scale_factor, **data_scaled
    )

    data_scaled[["u", "v", "V"]] /= np.sqrt(scale_factor)
    data_scaled[["r"]] *= np.sqrt(scale_factor)
    data_scaled[["thrust"]] /= scale_factor ** 3

    return data_scaled


def res(x, u):

    r = x * u ** 2

    return r


def error(x, y, u):

    r = res(x, u)
    e = r - y
    return e


def vct_resistance_correction(
    data: pd.DataFrame, data_TT_MDL: pd.DataFrame
) -> pd.DataFrame:
    """The resistance from VCT is totally wrong (no wave resistance and scale effects)
    Instead resistance is taken from TT model test (rescaled to MDL scale)

    Parameters
    ----------
    data : pd.DataFrame
        vct data
    data_TT_MDL : pd.DataFrame
        resistance table for the MDL tests
        vm [m/s], Rm [N]

    Returns
    -------
    pd.DataFrame
        VCT data with corrected resistance
    """
    df_resistance = data.groupby(by="test type").get_group("resistance")
    result1 = least_squares(
        fun=error, x0=[0], kwargs={"y": df_resistance["fx"], "u": df_resistance["u"]}
    )

    data["fx"] -= res(result1.x, u=data["u"])

    R_m = data_TT_MDL["Rm [N]"]
    fx = -R_m
    result2 = least_squares(
        fun=error,
        x0=result1.x,
        kwargs={"y": fx, "u": fx.index},
    )

    R_factor = 1.14
    data["fx"] += R_factor * res(result2.x, u=data["u"])

    return data

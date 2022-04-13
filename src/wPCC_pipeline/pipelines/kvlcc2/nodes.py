"""
This is a boilerplate pipeline 'kvlcc2'
generated using Kedro 0.17.6
"""

import pandas as pd
import numpy as np


def load(df: pd.DataFrame, ship_data: dict) -> pd.DataFrame:
    """load kvlcc2 data and transform it

    Parameters
    ----------
    df : pd.DataFrame
        kvlcc2 data

    Returns
    -------
    pd.DataFrame
        With correct column naming and radians etc.
    """

    df.dropna(how="all", inplace=True)

    scale_factor = ship_data["scale_factor"]

    dt = 0.135 / np.sqrt(scale_factor)
    df["time"] = np.arange(0, len(df) * dt, dt)

    df.set_index("time", inplace=True)
    df.sort_index(inplace=True)
    angles = ["phi", "psi", "r", "delta"]
    df[angles] = np.deg2rad(df[angles])

    ## To model scale:
    df["x0"] /= scale_factor
    df["y0"] /= scale_factor
    df["u"] /= np.sqrt(scale_factor)
    df["v"] /= np.sqrt(scale_factor)
    df["p"] *= np.sqrt(scale_factor)
    df["r"] *= np.sqrt(scale_factor)
    df["rev"] *= 1 / 60 * np.sqrt(scale_factor)  # [rps]
    df["thrust"] = 0  # not true...

    return df

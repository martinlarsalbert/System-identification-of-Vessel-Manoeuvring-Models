"""
This is a boilerplate pipeline 'lowpass'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.visualization import plot
import matplotlib.pyplot as plt

from numpy import cos as cos
from numpy import sin as sin
import numpy as np
from src.data.lowpass_filter import lowpass_filter


def load(df: pd.DataFrame) -> pd.DataFrame:

    df.index -= df.index[0]
    df["x0"] -= df.iloc[0]["x0"]
    df["y0"] -= df.iloc[0]["y0"]
    df["psi"] -= df.iloc[0]["psi"]

    return df


def add_thrust(df: pd.DataFrame, thrust_channels: list) -> pd.DataFrame:

    assert isinstance(thrust_channels, list), "'thrust_channels' should be a list"

    if len(thrust_channels) > 0:
        df["thrust"] = df[thrust_channels].sum(axis=1)

    return df


def track_plot(df: pd.DataFrame, ship_data: dict):

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)
    plot.track_plot(
        df=df,
        lpp=ship_data["L"],
        x_dataset="x0",
        y_dataset="y0",
        psi_dataset="psi",
        beam=ship_data["B"],
        ax=ax,
    )

    return fig


def filter(df: pd.DataFrame, cutoff: float, order=1) -> pd.DataFrame:
    """Lowpass filter and calculate velocities and accelerations with numeric differentiation

    Parameters
    ----------
    df : pd.DataFrame
        [description]
    cutoff : float
        Cut off frequency of the lowpass filter [Hz]
    order : int, optional
        order of the filter, by default 1

    Returns
    -------
    pd.DataFrame
        lowpassfiltered positions, velocities and accelerations
    """

    df_lowpass = df.copy()
    t = df_lowpass.index
    ts = np.mean(np.diff(t))
    fs = 1 / ts

    position_keys = ["x0", "y0", "psi"]
    for key in position_keys:
        df_lowpass[key] = lowpass_filter(data=df_lowpass[key], fs=fs, cutoff=1, order=1)

    df_lowpass["x01d_gradient"] = x1d_ = np.gradient(df_lowpass["x0"], t)
    df_lowpass["y01d_gradient"] = y1d_ = np.gradient(df_lowpass["y0"], t)
    df_lowpass["r"] = r_ = np.gradient(df_lowpass["psi"], t)

    psi_ = df_lowpass["psi"]

    df_lowpass["u"] = x1d_ * cos(psi_) + y1d_ * sin(psi_)
    df_lowpass["v"] = -x1d_ * sin(psi_) + y1d_ * cos(psi_)

    velocity_keys = ["u", "v", "r"]
    for key in velocity_keys:
        df_lowpass[key] = lowpass_filter(data=df_lowpass[key], fs=fs, cutoff=1, order=1)

    return df_lowpass

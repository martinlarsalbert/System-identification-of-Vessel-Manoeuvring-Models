"""
This is a boilerplate pipeline 'lowpass'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.visualization import plot
import matplotlib.pyplot as plt


def load(df: pd.DataFrame) -> pd.DataFrame:

    df.index -= df.index[0]
    df["x0"] -= df.iloc[0]["x0"]
    df["y0"] -= df.iloc[0]["y0"]
    df["psi"] -= df.iloc[0]["psi"]

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

"""
This is a boilerplate pipeline 'prediction'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.models.vmm import ModelSimulator
import matplotlib.pyplot as plt
import src.visualization.plot as plot

import logging

log = logging.getLogger("kedro.pipeline")


def simulate(data: pd.DataFrame, model: ModelSimulator) -> pd.DataFrame:

    try:
        results = model.simulate(df_=data)
    except Exception as e:
        df = pd.DataFrame(
            index=data.index, columns=["x0", "y0", "psi", "u", "v", "r", "delta"]
        )
        log.warning(e)
    else:
        df = results.result

    return df


def track_plot(
    data: pd.DataFrame, results: pd.DataFrame, ship_data: dict
) -> plt.figure:

    if results["x0"].isnull().all():
        fig, ax = plt.subplots()
        return fig

    dataframes = {"model test": data, "simulation": results}
    ax = plot.track_plots(
        dataframes=dataframes, lpp=ship_data["L"], beam=ship_data["B"]
    )

    return ax.get_figure()


def plot_timeseries(data: pd.DataFrame, results: pd.DataFrame) -> plt.figure:

    if results["x0"].isnull().all():
        fig, ax = plt.subplots()
        return fig

    dataframes = {"model test": data, "simulation": results}
    ax = plot.plot(dataframes=dataframes, keys=["y0", "psi", "u", "v", "r", "delta"])

    return ax.get_figure()

"""
This is a boilerplate pipeline 'plot'
generated using Kedro 0.17.6
"""

import pandas as pd
import matplotlib.pyplot as plt
import src.visualization.plot as plot


def track_plot(
    data: pd.DataFrame, results: pd.DataFrame, ship_data: dict
) -> plt.figure:

    if results["x0"].isnull().all():
        fig, ax = plt.subplots()
        return fig

    dataframes = {"model test": data, "simulation": results}
    ax = plot.track_plots(
        dataframes=dataframes,
        lpp=ship_data["L"],
        beam=ship_data["B"],
        N=7,
    )

    return ax.get_figure()


def plot_timeseries(
    data: pd.DataFrame,
    results: pd.DataFrame,
    ship_data: dict,
    raw_data: pd.DataFrame,
) -> plt.figure:

    if results["x0"].isnull().all():
        fig, ax = plt.subplots()
        return fig

    dataframes = {"model test": data, "simulation": results, "raw": raw_data}
    ax = plot.plot(
        dataframes=dataframes, keys=["thrust", "psi", "u", "v", "r", "delta"]
    )

    return ax.get_figure()

"""
This is a boilerplate pipeline 'plot_filters'
generated using Kedro 0.17.6
"""
"""
This is a boilerplate pipeline 'plot'
generated using Kedro 0.17.6
"""

import pandas as pd
import matplotlib.pyplot as plt
import vessel_manoeuvring_models.visualization.plot as plot


def plot_filters(
    data_ek_smooth1: pd.DataFrame,
    data_ek_smooth2: pd.DataFrame,
    data_lowpass: pd.DataFrame,
) -> plt.figure:

    dataframes = {
        "lowpass": data_lowpass,
        "smooth1": data_ek_smooth1,
        "smooth2": data_ek_smooth2,
    }
    ax = plot.plot(dataframes=dataframes, keys=["psi", "u", "v", "r"])

    return ax.get_figure()

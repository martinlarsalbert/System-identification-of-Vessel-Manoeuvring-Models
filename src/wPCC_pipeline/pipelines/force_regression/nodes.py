"""
This is a boilerplate pipeline 'force_regression'
generated using Kedro 0.17.6
"""

import pandas as pd
from typing import Union
from src.models.vmm import ModelSimulator
from src.models.regression import ForceRegression
import matplotlib.pyplot as plt
from src.models.vmm import VMM


def fit_forces(
    data: pd.DataFrame, added_masses: dict, ship_data: dict, vmm: VMM
) -> Union[ForceRegression, pd.DataFrame]:
    """Fit damping force parameters in a dynamic model to ship FORCE measurements

    Parameters
    ----------
    data : pd.DataFrame
        Measured forces as function of state (from captive test or Virtual Captive Tests)
    added_masses : dict
        ship added masses in prime-system
    ship_data : dict
        Ship parameters in SI-units.
    vmm : VMM object
        Vessel Manoeuvring Model (defining the equation of motions and damping forces)


    Returns
    -------
    Union[ForceRegression, pd.DataFrame]
        ForceRegression object
        Dataframe with regressed parameters and their confidence intervals etc.
    """

    interesting = ["u", "v", "r", "delta", "thrust", "fx", "fy", "mz"]
    data = data[interesting].copy()

    regression = ForceRegression(
        vmm=vmm,
        data=data,
        added_masses=added_masses,
        ship_parameters=ship_data,
    )

    parameters = pd.DataFrame(regression.parameters)
    return regression, parameters


def force_regression_summaries(regression: ForceRegression) -> Union[str, str, str]:
    return (
        regression.model_X.summary().as_text(),
        regression.model_Y.summary().as_text(),
        regression.model_N.summary().as_text(),
    )


def force_regression_plots(
    regression: ForceRegression,
) -> Union[plt.figure, plt.figure, plt.figure]:
    return (
        regression.plot_pred_X().get_figure(),
        regression.plot_pred_Y().get_figure(),
        regression.plot_pred_N().get_figure(),
    )


def create_model_from_force_regression(regression: ForceRegression) -> ModelSimulator:

    model = regression.create_model(
        control_keys=["delta", "thrust"],
    )

    return model

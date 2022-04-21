"""
This is a boilerplate pipeline 'force_regression'
generated using Kedro 0.17.6
"""

import pandas as pd
from typing import Union
from src.models.vmm import ModelSimulator
from src.models.regression import Regression
import matplotlib.pyplot as plt
from src.models.vmm import VMM


def fit_forces(
    data: pd.DataFrame,
    added_masses: dict,
    ship_data: dict,
    vmm: VMM,
    exclude_parameters: dict = {},
) -> Union[Regression, pd.DataFrame]:
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
    exclude_parameters : dict, optional
            Exclude some parameters from the regression by instead providing their value.
            Ex:
            exclude_parameters = {'Xthrust':0.95}
            means that Xthrust parameter will not be regressed, instead a value of 0.95 will be used.

    Returns
    -------
    Union[Regression, pd.DataFrame]
        Regression object
        Dataframe with regressed parameters and their confidence intervals etc.
    """

    interesting = ["u", "v", "r", "delta", "thrust", "fx", "fy", "mz"]
    data = data[interesting].copy()

    regression = Regression(
        vmm=vmm,
        data=data,
        added_masses=added_masses,
        ship_parameters=ship_data,
        exclude_parameters=exclude_parameters,
    )

    parameters = pd.DataFrame(regression.parameters)
    return regression, parameters


def force_regression_summaries(regression: Regression) -> Union[str, str, str]:
    return (
        regression.model_X.summary().as_text(),
        regression.model_Y.summary().as_text(),
        regression.model_N.summary().as_text(),
    )


def force_regression_plots(
    regression: Regression,
) -> Union[plt.figure, plt.figure, plt.figure]:
    return (
        regression.plot_pred_X().get_figure(),
        regression.plot_pred_Y().get_figure(),
        regression.plot_pred_N().get_figure(),
    )


def create_model_from_force_regression(regression: Regression) -> ModelSimulator:

    model = regression.create_model(
        control_keys=["delta", "thrust"],
    )

    return model

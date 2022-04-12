"""
This is a boilerplate pipeline 'motion_regression'
generated using Kedro 0.17.6
"""

from src.models.regression import Regression
import pandas as pd
import src.prime_system as prime_system
from src.models.vmm import VMM
import src.symbols as s
from typing import Union
from src.models.vmm import ModelSimulator
import matplotlib.pyplot as plt
from src.models.force_from_motion import predict_force


def fit_motions(
    data: pd.DataFrame,
    added_masses: dict,
    ship_data: dict,
    vmm: VMM,
    exclude_parameters: dict = {},
) -> Union[Regression, pd.DataFrame]:
    """Fit damping force parameters in a dynamic model to ship MOTION measurements

    Parameters
    ----------
    data : pd.DataFrame
        Measurements of forces predicted from motions : positions, velocities and accelerations
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
    Union[MotionRegression, pd.DataFrame]
        MotionRegression object
        Dataframe with regressed parameters and their confidence intervals etc.
    """

    ps = prime_system.PrimeSystem(**ship_data)  # model

    regression = Regression(
        vmm=vmm,
        data=data,
        added_masses=added_masses,
        ship_parameters=ship_data,
        prime_system=ps,
        base_features=[s.u, s.v, s.r, s.delta, s.thrust],
        exclude_parameters=exclude_parameters,
    )

    parameters = pd.DataFrame(regression.parameters)
    return regression, parameters


def motion_regression_summaries(regression: Regression) -> Union[str, str, str]:
    return (
        regression.model_X.summary().as_text(),
        regression.model_Y.summary().as_text(),
        regression.model_N.summary().as_text(),
    )


def motion_regression_plots(
    regression: Regression,
) -> Union[plt.figure, plt.figure, plt.figure]:
    return (
        regression.plot_pred_X().get_figure(),
        regression.plot_pred_Y().get_figure(),
        regression.plot_pred_N().get_figure(),
    )


def create_model_from_motion_regression(regression: Regression) -> ModelSimulator:

    model = regression.create_model(
        control_keys=["delta", "thrust"],
    )

    return model

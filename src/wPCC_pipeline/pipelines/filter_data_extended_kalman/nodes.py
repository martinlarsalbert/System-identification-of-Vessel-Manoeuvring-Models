"""
This is a boilerplate pipeline 'filter_data_extended_kalman'
generated using Kedro 0.17.6
"""
from src.extended_kalman_vmm import ExtendedKalman
import numpy as np
import pandas as pd


def resimulate_extended_kalman(ek: ExtendedKalman, data) -> pd.DataFrame:

    E = np.array(
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
    )

    df_sim = ek.simulate(data=data, input_columns=["delta", "thrust"], E=E)

    return df_sim


def initial_state(
    data: pd.DataFrame, state_columns=["x0", "y0", "psi", "u", "v", "r"]
) -> np.ndarray:
    # x0 = data.iloc[0][state_columns].values
    x0 = data.iloc[0:5][state_columns].mean()

    return {key: float(value) for key, value in x0.items()}


def extended_kalman_filter(
    ek: ExtendedKalman,
    data: pd.DataFrame,
    covariance_matrixes: dict,
    x0: list,
    input_columns=["delta", "thrust"],
):
    """Filter with existing Extended Kalman filter

    Parameters
    ----------
    ek : ExtendedKalman
        ekxtended kalman filter object
    data : pd.DataFrame
        data to be filtered
    P_prd : np.ndarray
            initial covariance matrix (no_states x no_states)
        Qd : np.ndarray
            Covariance matrix of the process model (no_hidden_states x no_hidden_states)
        Rd : float
            Covariance matrix of the measurement (no_measurement_states x no_measurement_states)

    Returns
    -------
    [type]
        extended kalman filter, filtered data
    """

    # Initial state guess:
    # x0 = np.concatenate((data.iloc[0][["x0", "y0", "psi"]].values, [0, 0, 0]))

    # Ed = h * E

    P_prd = np.array(covariance_matrixes["P_prd"])
    Qd = np.array(covariance_matrixes["Qd"])
    Rd = np.array(covariance_matrixes["Rd"])

    Cd = np.array(
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
        ]
    )

    E = np.array(
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
    )

    x0_ = pd.Series(x0)[["x0", "y0", "psi", "u", "v", "r"]].values
    time_steps = ek.filter(
        data=data,
        P_prd=P_prd,
        Qd=Qd,
        Rd=Rd,
        E=E,
        Cd=Cd,
        input_columns=input_columns,
        x0_=x0_,
    )

    return ek, ek.df_kalman, time_steps


def extended_kalman_smoother(
    ek: ExtendedKalman, data: pd.DataFrame, time_steps, covariance_matrixes: dict
):

    E = np.array(
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
    )

    ek.Qd = covariance_matrixes["Qd"]
    ek.E = E

    ek.smoother(time_steps=time_steps)
    ek.data = data

    return ek, ek.df_smooth

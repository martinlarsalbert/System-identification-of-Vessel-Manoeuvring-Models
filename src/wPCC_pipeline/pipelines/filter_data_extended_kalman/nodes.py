"""
This is a boilerplate pipeline 'filter_data_extended_kalman'
generated using Kedro 0.17.6
"""
from src.extended_kalman_vmm import ExtendedKalman
import numpy as np
import pandas as pd
import inspect


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
    hydrodynamic_derivatives: dict,
    input_columns=["delta", "thrust", "U"],
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
    parameters: dict
        hydrodynamic derivatives used in the VMM in the extended kalman filter.

    Returns
    -------
    [type]
        extended kalman filter, filtered data
    """

    ## Update parameters
    ek = ek.copy()
    if isinstance(hydrodynamic_derivatives, pd.DataFrame):
        ek.parameters.update(hydrodynamic_derivatives["regressed"])
    else:
        ek.parameters.update(hydrodynamic_derivatives)

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

    arguments = list(inspect.signature(ek._lambda_f).parameters.keys())
    input_columns = list(set(arguments) & set(input_columns))
    if "U" in input_columns:
        data["U"] = np.sqrt(data["u"] ** 2 + data["v"] ** 2)

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

    df = ek.df_kalman
    if "thrust" in data:
        df["thrust"] = data["thrust"].values

    return ek, df, time_steps


def extended_kalman_smoother(
    ek: ExtendedKalman,
    data: pd.DataFrame,
    time_steps,
    covariance_matrixes: dict,
    hydrodynamic_derivatives: dict,
):

    ## Update parameters
    ek = ek.copy()
    if isinstance(hydrodynamic_derivatives, pd.DataFrame):
        ek.parameters.update(hydrodynamic_derivatives["regressed"])
    else:
        ek.parameters.update(hydrodynamic_derivatives)

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

    ek.Qd = np.array(covariance_matrixes["Qd"])
    ek.E = E

    ek.smoother(time_steps=time_steps)
    ek.data = data

    df = ek.df_smooth
    if "thrust" in data:
        df["thrust"] = data["thrust"].values

    return ek, df


def guess_covariance_matrixes(ek_covariance_input: dict, data: pd.DataFrame) -> dict:

    process_variance = ek_covariance_input["process_variance"]
    variance_u = process_variance["u"]
    variance_v = process_variance["v"]
    variance_r = np.deg2rad(process_variance["r"])

    h = np.mean(np.diff(data.index))

    Qd = np.diag([variance_u, variance_v, variance_r]) * h  # process variances: u,v,r

    measurement_error_max = ek_covariance_input["measurement_error_max"]
    error_max_pos = measurement_error_max["positions"]
    sigma_pos = error_max_pos / 3
    variance_pos = sigma_pos ** 2

    error_max_psi = np.deg2rad(measurement_error_max["psi"])
    sigma_psi = error_max_psi / 3
    variance_psi = sigma_psi ** 2

    Rd = np.diag([variance_pos, variance_pos, variance_psi])

    P_prd = np.diag(
        [
            variance_pos,
            variance_pos,
            variance_psi,
            variance_u * h,
            variance_v * h,
            variance_r * h,
        ]
    )

    covariance_matrixes = {
        "P_prd": P_prd.tolist(),
        "Qd": Qd.tolist(),
        "Rd": Rd.tolist(),
    }

    return covariance_matrixes

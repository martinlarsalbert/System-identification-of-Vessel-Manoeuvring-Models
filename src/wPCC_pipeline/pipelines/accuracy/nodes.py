"""
This is a boilerplate pipeline 'accuracy'
generated using Kedro 0.17.6
"""

import numpy as np
import pandas as pd
from src.extended_kalman_vmm import ExtendedKalman
from src.models.vmm import ModelSimulator
from inspect import signature
from sklearn.metrics import mean_squared_error


def online_prediction(
    df: pd.DataFrame,
    ek: ExtendedKalman,
    model: ModelSimulator,
    state_columns=["x0", "y0", "psi", "u", "v", "r"],
):
    data = df[state_columns]
    x = df[state_columns].values.T

    t = df.index
    h = t[1] - t[0]

    df["U"] = np.sqrt(df["u"] ** 2 + df["v"] ** 2)

    input_columns = model.control_keys + ["U"]
    s = signature(ek._lambda_f)
    input_columns = list(set(input_columns) & set(s.parameters.keys()))
    input = df[input_columns]

    ek = ek.copy()
    ek.parameters = model.parameters  # Update the parameters!!!

    x_dot = ek.lambda_f(x, input).T

    x_dot = np.concatenate((np.zeros((0, len(state_columns))), x_dot))

    dx_data = x_dot * h
    dx = pd.DataFrame(dx_data, columns=state_columns)

    df_predict = data + dx.values

    return df_predict


def calculate_V_FP(df: pd.DataFrame, lpp: float) -> pd.Series:
    """Calculate velocity at forward perpendicular in ship fix coordinate system

    Parameters
    ----------
    df : pd.DataFrame
        [description]
    lpp : float
        length between perpendiculars [m]

    Returns
    -------
    pd.Series
        velocity at forward perpendicular
    """
    u = df["u"]
    v = df["v"]
    r = df["r"]
    V_FP = np.sqrt(u ** 2 + (v + lpp / 2 * r) ** 2)
    return V_FP


def online_prediction_rmse(
    df_pred: pd.DataFrame,
    data: pd.DataFrame,
    ship_data: dict,
    keys=["u", "v", "r"],
):

    df_pred["V_FP"] = calculate_V_FP(df=df_pred, lpp=ship_data["L"])
    data["V_FP"] = calculate_V_FP(df=data, lpp=ship_data["L"])
    keys += ["V_FP"]

    accuracies = {
        key: np.sqrt(mean_squared_error(y_true=data[key], y_pred=df_pred[key]))
        for key in keys
        if df_pred[key].notnull().all() and len(data[key]) == len(df_pred[key])
    }
    return accuracies


def online_acceleration_prediction(
    df: pd.DataFrame,
    ek: ExtendedKalman,
    model: ModelSimulator,
    state_columns=["x0", "y0", "psi", "u", "v", "r"],
):

    df["U"] = np.sqrt(df["u"] ** 2 + df["v"] ** 2)

    input_columns = model.control_keys + ["U"]
    s = signature(ek._lambda_f)
    input_columns = list(set(input_columns) & set(s.parameters.keys()))
    input = df[input_columns]

    ek = ek.copy()
    ek.parameters = model.parameters  # Update the parameters!!!

    return predict_acc(
        data=df, ek=ek, input_columns=input_columns, state_columns=state_columns
    )


def predict_acc(
    data,
    ek,
    input_columns=["delta", "thrust"],
    state_columns=["x0", "y0", "psi", "u", "v", "r"],
):

    input = data[input_columns]
    X = data[state_columns].values
    x_dot = ek.lambda_f(X.T, input).T
    df_predict = pd.DataFrame(
        data=x_dot[:, 3:], columns=["u1d", "v1d", "r1d"], index=data.index
    )

    return df_predict


def calculate_A_FP(df: pd.DataFrame, lpp: float) -> pd.Series:
    """Calculate acceleration at forward perpendicular in ship fix coordinate system

    Parameters
    ----------
    df : pd.DataFrame
        [description]
    lpp : float
        length between perpendiculars [m]

    Returns
    -------
    pd.Series
        velocity at forward perpendicular
    """
    u = df["u1d"]
    v = df["v1d"]
    r = df["r1d"]
    A_FP = np.sqrt(u ** 2 + (v.abs() + lpp / 2 * r.abs()) ** 2)
    return A_FP


def online_acceleration_prediction_rmse(
    df_pred: pd.DataFrame,
    data: pd.DataFrame,
    ship_data: dict,
    keys=["u1d", "v1d", "r1d"],
):

    df_pred["A_FP"] = calculate_A_FP(df=df_pred, lpp=ship_data["L"])
    data["A_FP"] = calculate_A_FP(df=data, lpp=ship_data["L"])
    keys += ["A_FP"]

    accuracies = {
        key: np.sqrt(mean_squared_error(y_true=data[key], y_pred=df_pred[key]))
        for key in keys
        if df_pred[key].notnull().all() and len(data[key]) == len(df_pred[key])
    }
    return accuracies

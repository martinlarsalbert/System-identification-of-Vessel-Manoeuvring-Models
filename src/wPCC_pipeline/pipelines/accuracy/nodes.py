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
    ek.parameters = model.parameters

    x_dot = ek.lambda_f(x, input).T

    x_dot = np.concatenate((np.zeros((0, len(state_columns))), x_dot))

    dx_data = x_dot * h
    dx = pd.DataFrame(dx_data, columns=state_columns)

    df_predict = data + dx.values

    return df_predict


def online_prediction_rmse(
    df_pred: pd.DataFrame, data: pd.DataFrame, keys=["u", "v", "r"]
):
    accuracies = {
        key: np.sqrt(mean_squared_error(y_true=data[key], y_pred=df_pred[key]))
        for key in keys
        if df_pred[key].notnull().all() and len(data[key]) == len(df_pred[key])
    }
    return accuracies

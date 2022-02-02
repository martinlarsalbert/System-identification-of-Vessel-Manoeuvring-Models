"""
This is a boilerplate pipeline 'accuracy'
generated using Kedro 0.17.6
"""

import numpy as np
import pandas as pd
from src.extended_kalman_vmm import ExtendedKalman


def online_prediction(
    df: pd.DataFrame,
    ek: ExtendedKalman,
    input_columns=["delta", "thrust"],
    state_columns=["x0", "y0", "psi", "u", "v", "r"],
):
    data = df[state_columns]
    x = df[state_columns].values.T

    t = df.index
    h = t[1] - t[0]

    df["U"] = np.sqrt(df["u"] ** 2 + df["v"] ** 2)

    input = df[input_columns]

    x_dot = ek.lambda_f(x, input).T
    x_dot = np.concatenate((np.zeros((0, len(state_columns))), x_dot))

    dx_data = x_dot * h
    dx = pd.DataFrame(dx_data, columns=state_columns)

    df_predict = data + dx.values

    return df_predict

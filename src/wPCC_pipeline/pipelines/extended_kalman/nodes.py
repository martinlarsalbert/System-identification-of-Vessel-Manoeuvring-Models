"""
This is a boilerplate pipeline 'ek'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.extended_kalman_vmm import ExtendedKalman
import src.models.vmm_martin as vmm
import numpy as np


def create_extended_kalman(parameters: dict, ship_data: dict) -> ExtendedKalman:

    ek = ExtendedKalman(vmm=vmm, parameters=parameters, ship_parameters=ship_data)

    return ek


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


def extended_kalman_filter(ek: ExtendedKalman, data: pd.DataFrame):

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

    P_prd = np.diag([0.1, 0.1, np.deg2rad(0.01), 0.01, 0.01, np.deg2rad(0.01)])
    Qd = np.diag([0.01, 0.01, np.deg2rad(0.01)])  # process variances: u,v,r

    error_max_pos = 0.1
    sigma_pos = error_max_pos / 3
    variance_pos = sigma_pos ** 2

    error_max_psi = np.deg2rad(0.1)
    sigma_psi = error_max_psi / 3
    variance_psi = sigma_psi ** 2

    Rd = np.diag([variance_pos, variance_pos, variance_psi])

    # Initial state guess:
    # x0 = np.concatenate((data.iloc[0][["x0", "y0", "psi"]].values, [0, 0, 0]))

    ek.filter(
        data=data,
        P_prd=P_prd,
        Qd=Qd,
        Rd=Rd,
        E=E,
        Cd=Cd,
        input_columns=["delta", "thrust"],
        # x0=x0,
    )

    return ek, ek.df_kalman


def extended_kalman_smoother(
    ek: ExtendedKalman,
):
    ek.smoother()

    return ek, ek.df_smooth

"""
This is a boilerplate pipeline 'captive'
generated using Kedro 0.17.6
"""

import pandas as pd
from vessel_manoeuvring_models.prime_system import PrimeSystem
import numpy as np


def load(df_prime: pd.DataFrame, ship_data: dict) -> pd.DataFrame:

    renames = {
        "delta(deg)": "delta",
        "beta(deg)": "beta",
        "Speed(m/s)": "V",
        "rps": "rev",
        "X'": "fx",
        "Y'": "fy",
        "N'": "mz",
        "RX'": "X_R",
        "RY'": "Y_R",
        "TX'": "thrust",
    }
    df_prime.rename(columns=renames, inplace=True)
    df_prime["delta"] = np.deg2rad(df_prime["delta"])
    df_prime["beta"] = np.deg2rad(df_prime["beta"])
    beta = df_prime["beta"]
    V = df_prime["V"]
    df_prime["u"] = V * np.cos(beta)
    df_prime["v"] = -V * np.sin(beta)

    # Convert from prime:

    # Unprime:
    force_keys = [
        "fx",
        "fy",
        "X_R",
        "Y_R",
        "thrust",
    ]
    df = df_prime.copy()
    rho = ship_data["rho"]
    T = ship_data["T"]
    L = ship_data["L"]
    U = df["V"]
    df[force_keys] = df[force_keys].mul(1 / 2 * rho * L ** 2 * U ** 2, axis=0)
    df["mz"] *= 1 / 2 * rho * L ** 3 * U ** 2

    return df


def prime2_derivatives_to_prime1(derivatives: dict, ship_data: dict) -> dict:

    derivatives_prime1 = derivatives.iloc[0].copy()
    keys = [
        "Xvv",
        "Xvr",
        "Xrr",
        "Xvvvv",
        "R0",
        "Yv",
        "Yr",
        "Yvvv",
        "Yvvr",
        "Yvrr",
        "Yrrr",
        "Nv",
        "Nr",
        "Nvvv",
        "Nvvr",
        "Nvrr",
        "Nrrr",
    ]
    derivatives_prime1[keys] *= ship_data["T"] / ship_data["L"]

    return {key: float(value) for key, value in derivatives_prime1.items()}

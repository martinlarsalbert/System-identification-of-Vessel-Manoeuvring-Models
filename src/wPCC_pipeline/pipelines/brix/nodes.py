"""
This is a boilerplate pipeline 'brix'
generated using Kedro 0.17.6
"""
from src.parameters import df_parameters
from src.substitute_dynamic_symbols import run
from src import prime_system
import pandas as pd


def calculate_prime(row, ship_parameters):
    return run(function=row["brix_lambda"], **ship_parameters)


def initial_parameters(ship_data: dict) -> dict:
    """Guess some initial prarameters with Brix

    Parameters
    ----------
    ship_data : dict
        [description]

    Returns
    -------
    dict
        [description]
    """

    mask = df_parameters["brix_lambda"].notnull()
    df_parameters.loc[mask, "brix_prime"] = df_parameters.loc[mask].apply(
        calculate_prime, ship_parameters=ship_data, axis=1
    )

    df_parameters["prime"] = df_parameters["brix_prime"]

    df_parameters.loc["Ydelta", "prime"] = 0.003  # Just guessing
    df_parameters.loc["Ndelta", "prime"] = (
        -df_parameters.loc["Ydelta", "prime"] / 2
    )  # Just guessing

    df_parameters.loc["Nu", "prime"] = 0
    df_parameters.loc["Nur", "prime"] = 0
    # df_parameters.loc["Xdelta", "prime"] = -0.001
    df_parameters.loc["Xr", "prime"] = 0
    df_parameters.loc["Xrr", "prime"] = 0.000
    df_parameters.loc["Xu", "prime"] = 0
    df_parameters.loc["Xuu", "prime"] = 0
    df_parameters.loc["Xv", "prime"] = 0
    df_parameters.loc["Xvr", "prime"] = 0
    df_parameters.loc["Yu", "prime"] = 0
    df_parameters.loc["Yur", "prime"] = 0.00

    df_parameters.loc["Nuv", "prime"] = 0.0
    df_parameters.loc["Xthrust", "prime"] = 1.0
    df_parameters.loc["Yrdeltadelta", "prime"] = 0.0
    df_parameters.loc["Xvdelta", "prime"] = 0.0
    df_parameters.loc["Xdeltadelta", "prime"] = 0.0
    df_parameters.loc["Yvdeltadelta", "prime"] = 0.0
    df_parameters.loc["Nrdeltadelta", "prime"] = 0.0
    df_parameters.loc["Yuv", "prime"] = 0.0
    df_parameters.loc["Nvdeltadelta", "prime"] = 0.0

    df_parameters.loc["Ythrustdelta", "prime"] = 0.0
    df_parameters.loc["Nthrustdelta", "prime"] = 0.0

    parameters = df_parameters["prime"].dropna().to_dict()

    return parameters


def extract_added_masses(parameters: dict) -> dict:
    return {key: value for key, value in parameters.items() if "dot" in key}

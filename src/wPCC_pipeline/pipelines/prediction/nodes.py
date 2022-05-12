"""
This is a boilerplate pipeline 'prediction'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.models.vmm import ModelSimulator
from src.extended_kalman_vmm import ExtendedKalman
import matplotlib.pyplot as plt
import src.visualization.plot as plot
from sklearn.metrics import r2_score, mean_squared_error
from inspect import signature
from scipy.stats import norm, multivariate_normal
from src.models.regression import Regression

import logging
import numpy as np
import multiprocessing
import dill

log = logging.getLogger("kedro.pipeline")


def simulate(data: pd.DataFrame, model: ModelSimulator) -> pd.DataFrame:
    """Resimulate model test data with a model

    Parameters
    ----------
    data : pd.DataFrame
        Model test time series
    model : ModelSimulator
        simulation model

    Returns
    -------
    pd.DataFrame
        resimulated data
    """

    try:
        results = model.simulate(df_=data)
    except Exception as e:
        df = pd.DataFrame(
            index=data.index, columns=["x0", "y0", "psi", "u", "v", "r", "delta"]
        )
        log.warning(e)
    else:
        df = results.result

    return df


def simulate_euler(
    data: pd.DataFrame,
    model: ModelSimulator,
    ek: ExtendedKalman,
    solver="euler",
) -> pd.DataFrame:
    """Resimulate model test data with a model

    Parameters
    ----------
    data : pd.DataFrame
        Model test time series
    model : ModelSimulator
        simulation model

    Returns
    -------
    pd.DataFrame
        resimulated data
    """

    ek = ek.copy()
    ek.parameters = model.parameters  # Update the parameters!!!

    data = data.copy()
    data["U"] = np.sqrt(data["u"] ** 2 + data["v"] ** 2)

    input_columns = model.control_keys + ["U"]
    s = signature(ek._lambda_f)
    input_columns = list(set(input_columns) & set(s.parameters.keys()))

    # The initial heading etc. is very important to get a good simulation:
    N = 3
    data.iloc[0][["psi", "u", "v"]] = data.iloc[0:N][["psi", "u", "v"]].mean()

    df = ek.simulate(data=data, input_columns=input_columns, solver=solver)

    return df


def worker(queue_input: multiprocessing.Queue, queue_output: multiprocessing.Queue):
    """_summary_

    Parameters
    ----------
    method : Method to run
    queue_input : multiprocessing.Queue with dictionary input
    queue_output : multiprocessing.Queue() with return value from method
        _description_
    """

    input = queue_input.get()

    input["model"] = dill.loads(input["model"])
    input["ek"] = dill.loads(input["ek"])

    return_values = simulate_euler(**input)

    queue_output.put(return_values)


def simulate_euler_with_timeout(
    data: pd.DataFrame,
    model: ModelSimulator,
    ek: ExtendedKalman,
    solver="Radau",
) -> pd.DataFrame:

    queue_input = multiprocessing.Queue()
    queue_output = multiprocessing.Queue()

    input = {
        "data": data,
        "model": dill.dumps(model),
        "ek": dill.dumps(ek),
        "solver": solver,
    }

    queue_input.put(input)

    p = multiprocessing.Process(target=worker, args=(queue_input, queue_output))
    p.start()

    p.join(timeout=100)

    if p.exitcode is None:
        log.error("The worker timed out.")
    else:
        return queue_output.get()


def damping_forces(data: pd.DataFrame, model: ModelSimulator):
    """Recalculate damping forces from VCT, or model test with captive or free model

    Parameters
    ----------
    data : pd.DataFrame
        * VCT data
        * captive model test data
        * model test time series
    model : ModelSimulator
        simulation model

    Returns
    -------
    pd.DataFrame
        recalculated damping forces
    """

    data = data[
        ["fx", "fy", "mz", "u", "v", "V", "r", "beta", "delta", "thrust", "test type"]
    ].copy()

    df_model = data.copy()
    df_model[["fx", "fy", "mz"]] = model.forces(inputs=df_model)
    return df_model


def simulation_accuracy(
    data: pd.DataFrame, results: pd.DataFrame, keys=["x0", "y0", "psi"]
) -> dict:

    accuracies = {
        key: np.sqrt(mean_squared_error(y_true=data[key], y_pred=results[key]))
        for key in keys
        if results[key].notnull().all() and len(data[key]) == len(results[key])
    }

    return accuracies


def monte_carlo(
    data: pd.DataFrame,
    regression: Regression,
    model: ModelSimulator,
    ek: ExtendedKalman,
    N=10,
    seed=42,
    solver="Radau",
) -> pd.DataFrame:
    """Monte carlo simulation with variation of hydrodynamic derivatives
       according to mean values and covariance matrix from regression.

    Parameters
    ----------
    data : pd.DataFrame
        Model test time series
    regression : Regression
        mean values ans covariance matrix
    model : ModelSimulator
        Not really used but is needed to get the "simulate_euler" to work
    ek : ExtendedKalman
        Is running the simulations (faster than model.simulate)
    N : int, optional
        Number of monte carlo simulations (parameter variations), by default 10
    seed : int
        seed used in the random
    Returns
    -------
    pd.DataFrame
        dataframe with simulation stacked and numbered with "realization" column.
    """

    means = regression.parameters["regressed"]
    cov = regression.covs.values

    rv = multivariate_normal(mean=means, cov=cov, allow_singular=True)
    np.random.seed(seed)

    df_parameter_variation = pd.DataFrame(data=rv.rvs(N), columns=means.index)

    dfs = []
    for index, parameters_ in df_parameter_variation.iterrows():
        model_ = model.copy()
        model_.parameters.update(parameters_)

        df_ = simulate_euler(data=data, model=model_, ek=ek, solver=solver)
        df_["realization"] = index

    df = pd.concat(dfs)
    return df

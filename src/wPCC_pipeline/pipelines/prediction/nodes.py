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
    solver="Radau",
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

    df = ek.simulate(data=data, input_columns=input_columns, solver=solver)

    return df


import multiprocessing as mp
import multiprocessing.queues as mpq


def sim_worker(q, data, model):
    df = simulate(data=data, model=model)
    q.put(df)


def simulate_with_time_out(
    data: pd.DataFrame, model: ModelSimulator, timeout=1000
) -> pd.DataFrame:

    # mp.set_start_method("spawn")
    q = mp.Queue()
    p = mp.Process(target=sim_worker, args=(q, data, model))
    p.start()

    try:
        res = q.get(timeout=timeout)
        print(res)
        p.join()

    except mpq.Empty as e:
        p.terminate()
        log.error("Timeout!")
        raise e


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


def track_plot(
    data: pd.DataFrame, results: pd.DataFrame, ship_data: dict
) -> plt.figure:

    if results["x0"].isnull().all():
        fig, ax = plt.subplots()
        return fig

    dataframes = {"model test": data, "simulation": results}
    ax = plot.track_plots(
        dataframes=dataframes,
        lpp=ship_data["L"],
        beam=ship_data["B"],
        N=7,
    )

    return ax.get_figure()


def plot_timeseries(
    data: pd.DataFrame, results: pd.DataFrame, ship_data: dict
) -> plt.figure:

    if results["x0"].isnull().all():
        fig, ax = plt.subplots()
        return fig

    dataframes = {"model test": data, "simulation": results}
    ax = plot.plot(
        dataframes=dataframes, keys=["thrust", "psi", "u", "v", "r", "delta"]
    )

    return ax.get_figure()


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

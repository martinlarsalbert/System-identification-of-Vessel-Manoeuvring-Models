"""
This is a boilerplate pipeline 'lowpass_filter_variation'
generated using Kedro 0.17.6
"""
from asyncio.log import logger
from wPCC_pipeline.pipelines.preprocess.nodes import filter, load
from wPCC_pipeline.pipelines.motion_regression.nodes import (
    predict_force,
    fit_motions,
    create_model_from_motion_regression,
)

from wPCC_pipeline.pipelines.prediction.nodes import simulate_euler
from src.extended_kalman_vmm import ExtendedKalman

import numpy as np
import pandas as pd
from pathlib import Path

from src.models.vmm import VMM
import logging

log = logging.getLogger(__name__)
from sklearn.metrics import r2_score, mean_squared_error


def vary_cuttoff(**datasets):

    cuttoffs = np.linspace(1.0, 10.0, 10)

    datas_lowpass = {}
    for id, raw_data in datasets.items():
        for cuttoff in cuttoffs:
            data = load(raw_data, replace_velocities=True)

            new_id = fr"{cuttoff}/{id}"
            datas_lowpass[new_id] = filter(data, cutoff=cuttoff, order=1)

    return datas_lowpass


def join(datas_lowpass: dict) -> dict:

    df_joins = {}

    for new_id, loader in datas_lowpass.items():
        data = loader()
        data["time"] = data.index

        path = Path(new_id)

        id = path.parts[-1]
        cuttoff = path.parts[-2]

        data["id"] = path.parts[-1]

        if not cuttoff in df_joins:
            df_joins[cuttoff] = data
        else:
            df_joins[cuttoff] = df_joins[cuttoff].append(data)

    return df_joins


def regression(
    df_joins: dict,
    added_masses: dict,
    ship_data: dict,
    vmm: VMM,
    exclude_parameters: dict,
):

    lowpass_model = {}
    regressions_lowpass = {}
    columns = ["u", "v", "r", "u1d", "v1d", "r1d", "delta", "thrust", "x0", "y0", "psi"]
    for cuttoff, loader in df_joins.items():
        data_lowpass = loader()
        datas_with_force = predict_force(
            data=data_lowpass[columns],
            added_masses=added_masses,
            ship_parameters=ship_data,
            vmm=vmm,
        )

        regressions_lowpass[cuttoff], parameters_lowpass = fit_motions(
            data=datas_with_force,
            added_masses=added_masses,
            ship_data=ship_data,
            vmm=vmm,
            exclude_parameters=exclude_parameters,
        )

        lowpass_model[cuttoff] = create_model_from_motion_regression(
            regression=regressions_lowpass[cuttoff]
        )

    return regressions_lowpass, lowpass_model


def dataset_dummy(**datasets):
    data_all = {}
    for id, df in datasets.items():
        data_all[id] = df
    return data_all


def simulate(lowpass_model: dict, data_all: dict, ek: ExtendedKalman) -> dict:

    lowpass_simulation = {}
    for cuttoff, loader in lowpass_model.items():
        model_ = loader()

        for id, data_ek_smooth in data_all.items():

            logger.info(f"Simulating cuttoff:{cuttoff} id:{id}")

            new_id = f"{cuttoff}/{id}"

            lowpass_simulation[new_id] = simulate_euler(
                data_ek_smooth, model=model_, ek=ek
            ).dropna()

    return lowpass_simulation


def accuracy(lowpass_simulation: dict, raw_data_all: dict) -> pd.DataFrame:

    # dofs = ["x0", "y0", "psi"]
    df_r2 = pd.DataFrame(columns=["RMSE"], index=lowpass_simulation.keys())

    for index, loader in lowpass_simulation.items():
        prediction = loader()

        id = Path(index).parts[-1]
        data = raw_data_all[id]

        # for dof in dofs:
        #    try:
        #        df_r2.loc[index, dof] = mean_squared_error(
        #            y_true=data[dof], y_pred=prediction[dof]
        #        )
        #    except:
        #        continue

        df_r2.loc[index, "RMSE"] = rmse(data, prediction)

    # df_r2["mean"] = df_r2.mean(axis=1)
    df_r2["id"] = [Path(index).parts[-1] for index in df_r2.index]
    df_r2["cuttoff"] = [Path(index).parts[-2] for index in df_r2.index]
    df_r2["filter"] = "low-pass"

    return df_r2


def accuracy_ekf(ekf_simulation: dict, raw_data_all: dict) -> pd.DataFrame:

    # dofs = ["x0", "y0", "psi"]
    df_r2 = pd.DataFrame(columns=["RMSE"], index=ekf_simulation.keys())

    for id, prediction in ekf_simulation.items():

        data = raw_data_all[id]

        # for dof in dofs:
        #    try:
        #        df_r2.loc[id, dof] = mean_squared_error(
        #            y_true=data[dof], y_pred=prediction[dof]
        #        )
        #    except:
        #        continue

        df_r2.loc[id, "RMSE"] = rmse(data, prediction)

    df_r2["filter"] = "EKF"

    return df_r2


def rmse(df_true, df_pred):

    dx = df_true["x0"] - df_pred["x0"]
    dy = df_true["y0"] - df_pred["y0"]
    epsilon_square = dx ** 2 + dy ** 2
    return np.sqrt(epsilon_square.sum() / len(df_true))

import tqdm
import sys
from wPCC_pipeline.pipelines.prediction.nodes import simulate_euler
from scipy.stats import norm, multivariate_normal
from vessel_manoeuvring_models.models.regression import Regression
from vessel_manoeuvring_models.extended_kalman_vmm import ExtendedKalman
import pandas as pd
import numpy as np


def parameter_variation(regression: Regression, N_=100, seed: int = None):

    models_ = {
        "X": regression.model_X,
        "Y": regression.model_Y,
        "N": regression.model_N,
    }

    means = {}
    covs = {}
    rvs = {}

    for dof, model_ in models_.items():
        mean = model_.params
        cov = pd.DataFrame(model_.cov_HC0, index=mean.index, columns=mean.index)
        means[dof] = mean
        covs[dof] = cov

        rv = multivariate_normal(mean=mean, cov=cov, allow_singular=True)
        rvs[dof] = rv

    if not seed is None:
        np.random.seed(seed)

    df_parameter_variations = []

    for dof, rv in rvs.items():
        mean = means[dof]
        df_parameter_variations.append(
            pd.DataFrame(data=rv.rvs(N_), columns=mean.index)
        )

    df_parameter_variations = pd.concat(df_parameter_variations, axis=1)

    return df_parameter_variations


def monte_carlo(
    data_smooth, df_parameter_variation, model, fast=True, ek: ExtendedKalman = None
):

    dataframes = {}
    with tqdm.tqdm(total=len(df_parameter_variation), file=sys.stdout) as pbar:
        for index, parameters_ in df_parameter_variation.iterrows():
            model_ = model.copy()
            model_.parameters.update(parameters_)

            if fast:
                dataframes[index] = simulate_euler(
                    data=data_smooth, model=model_, ek=ek, solver="Radau"
                )
            else:
                result = model_.simulate(data_smooth, include_accelerations=False)
                dataframes[index] = result.result.copy()

            pbar.update(1)

    return dataframes

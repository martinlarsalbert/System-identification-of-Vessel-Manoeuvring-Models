"""
This is a boilerplate pipeline 'generic_data2'
generated using Kedro 0.17.6
"""

import pandas as pd
import numpy as np


def add_noise(df: pd.DataFrame, noises: dict) -> pd.DataFrame:

    df_true = df.copy()

    for key, noise in noises.items():
        df[key] += np.random.normal(scale=noise, size=len(df))

    return df_true, df[["x0", "y0", "psi", "delta", "thrust"]]

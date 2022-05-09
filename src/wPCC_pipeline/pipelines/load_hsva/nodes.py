"""
This is a boilerplate pipeline 'load_hsva'
generated using Kedro 0.17.6
"""

import pandas as pd
import os
import numpy as np
from io import StringIO


def load_runs(runs: dict) -> dict:

    new_runs = {}
    for id, run in runs.items():
        name = os.path.splitext(id)[0]
        new_name = f"{name}.csv"

        df_ = run()

        try:
            new_runs[new_name] = transform(df_)
        except Exception:
            raise ValueError(f"id:{id}")

    return new_runs


def transform(df: pd.DataFrame) -> pd.DataFrame:

    df[["delta", "psi", "r"]] = np.deg2rad(df[["delta", "psi", "r"]])

    df.index -= df.index[0]

    return df


def create_run_yml(runs: dict) -> list:

    l = [f"{os.path.splitext(id)[0]}" for id in runs.keys()]

    return l

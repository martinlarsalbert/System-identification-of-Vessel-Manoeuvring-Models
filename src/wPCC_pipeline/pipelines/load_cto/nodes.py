"""
This is a boilerplate pipeline 'load_cto'
generated using Kedro 0.17.6
"""

import pandas as pd
import os
import numpy as np
from io import StringIO


def load_runs(runs: dict) -> dict:

    columns = [
        "time",
        "delta",
        "psi",
        "r",
        "phi",
        "thrust",
        "torque",
        "fy_R",
        "fx_R",
        "mz_R",
        "rev",
        # "x0",
        # "y0",
        "y0",
        "x0",
    ]

    new_runs = {}
    for id, run in runs.items():
        name = os.path.splitext(id)[0]
        new_name = f"{name}.csv"
        s = run()
        data = StringIO(s)

        df_ = pd.read_csv(
            data,
            sep=r"\t",
            index_col=0,
            header=1,
            names=columns,
        )

        try:
            new_runs[new_name] = transform(df_)
        except Exception:
            raise ValueError(f"id:{id}")

    return new_runs


def transform(df: pd.DataFrame) -> pd.DataFrame:

    df[["delta", "psi", "r", "phi"]] = np.deg2rad(df[["delta", "psi", "r", "phi"]])

    df = rotate(df)

    df.index -= df.index[0]

    return df


def rotate(df: pd.DataFrame) -> pd.DataFrame:

    # psi has been zeroed in the begining of the CTO data, so we need to guess the actual heading.
    mask = df.index < 0
    start = df.loc[mask]

    start["x0"] -= start.iloc[0]["x0"]
    start["y0"] -= start.iloc[0]["y0"]

    delta_psi = np.arctan(start["y0"] / start["x0"])
    df["psi"] += delta_psi.iloc[-1]

    return df


def create_run_yml(runs: dict) -> list:

    l = [f"'{os.path.splitext(id)[0]}'" for id in runs.keys()]

    return l

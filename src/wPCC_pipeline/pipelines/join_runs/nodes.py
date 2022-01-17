"""
This is a boilerplate pipeline 'join_runs'
generated using Kedro 0.17.6
"""
import pandas as pd


def join(*runs: list) -> pd.DataFrame:

    df = pd.DataFrame()
    for run in runs:
        df_ = run.copy()
        df_["time"] = df_.index
        df = df.append(df_, ignore_index=True)

    return df

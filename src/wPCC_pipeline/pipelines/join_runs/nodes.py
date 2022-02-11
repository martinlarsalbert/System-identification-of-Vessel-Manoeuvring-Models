"""
This is a boilerplate pipeline 'join_runs'
generated using Kedro 0.17.6
"""
import pandas as pd


def join(**runs: dict) -> pd.DataFrame:

    df = pd.DataFrame()
    for run_id, run in runs.items():
        df_ = run.copy()
        df_["time"] = df_.index
        df_["id"] = run_id
        df = df.append(df_, ignore_index=True)

    return df

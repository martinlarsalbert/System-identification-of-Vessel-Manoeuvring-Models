"""
This is a boilerplate pipeline 'vct_data'
generated using Kedro 0.17.6
"""
import pandas as pd


def select_vct_data(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("model_name").get_group("V2_5_MDL_modelScale")

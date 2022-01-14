"""
This is a boilerplate pipeline 'prediction'
generated using Kedro 0.17.6
"""

import pandas as pd
from src.models.vmm import ModelSimulator


def simulate(data: pd.DataFrame, model: ModelSimulator) -> pd.DataFrame:

    results = model.simulate(df_=data)

    return results.result

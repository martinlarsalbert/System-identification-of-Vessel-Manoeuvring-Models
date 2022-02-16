"""
This is a boilerplate pipeline 'setup'
generated using Kedro 0.17.6
"""

import pandas as pd
import numpy as np


def add_run_description(runs_meta_data: pd.DataFrame) -> pd.DataFrame:

    runs_meta_data_ = runs_meta_data.copy()

    mask = runs_meta_data_["test_type"] == "rodergrundvinkel"
    runs_meta_data_.loc[mask, "yaw rate counter"] = np.arange(mask.sum())

    runs_meta_data["description"] = runs_meta_data_.apply(func=description, axis=1)
    runs_meta_data.sort_values(by="description", inplace=True)

    return runs_meta_data


def description(row):
    test_type = row["test_type"]
    ship_speed = np.round(row["ship_speed"], decimals=1)

    if test_type == "rodergrundvinkel":
        yaw_rate_counter = int(row["yaw rate counter"])
        return f"Yaw rate {yaw_rate_counter}"

    if test_type == "reference speed":
        return f"Reference speed {ship_speed} m/s"

    if test_type == "zigzag":
        if pd.notnull(row["angle1"]):
            angle1 = int(row["angle1"])
            return f"ZigZag{angle1}/{angle1}"
        else:
            return "ZigZag"

    s = f"{test_type[0].upper()}{test_type[1:]}"

    return s

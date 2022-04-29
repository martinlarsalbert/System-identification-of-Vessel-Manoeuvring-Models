"""
This is a boilerplate pipeline 'load_db'
generated using Kedro 0.17.6
"""
from mdldb.run import Run
from mdldb.mdl_db import MDLDataBase
from mdldb.authenticate import authenticate

authenticate(dotenv_path=".env")
db = MDLDataBase()
import pandas as pd
from mdl_helpers.mdl_motions import add_MDL_motions, do_transforms


def create_ship_data(runs_meta_data: pd.DataFrame) -> dict:

    meta_data = runs_meta_data.iloc[0]

    volume = meta_data["Volume"]
    T = (meta_data["TA"] + meta_data["TF"]) / 2
    L = meta_data["lpp"]
    B = meta_data["beam"]
    rho = 1000
    m = rho * volume

    ship_data = {
        "T": T,
        "L": L,
        "CB": volume / (L * B * T),
        "B": B,
        "rho": rho,
        "x_G": meta_data["lcg"],
        "m": m,
        "I_z": meta_data["KZZ"] ** 2 * m,
        "volume": volume,
        "scale_factor": meta_data["scale_factor"],
    }

    return {key: float(value) for key, value in ship_data.items()}


def load_runs(runs_meta_data: pd.DataFrame) -> dict:

    datas = {}

    for id, row in runs_meta_data.iterrows():

        try:
            data = process_run(id=id)
        except ValueError:
            print("skipping empy run...")
            continue
        else:
            datas[f"{id}.csv"] = data

    return datas


def process_run(id):

    run = db.session.query(Run).get(id)
    ## Missing in db:

    run.xm = 0
    run.ym = 0
    run.zm = -0.199

    df = run.load()

    meta_data = {
        "ScaleFactor": run.model.scale_factor,
        "LCG": run.loading_condition.lcg,
        "KG": run.loading_condition.kg,
        "xm": run.xm,
        "ym": run.ym,
        "zm": run.zm,
    }
    meta_data = pd.Series(meta_data)

    df_ = do_transforms(df)

    units = {
        "MA/Roll": "rad",
        "MA/Pitch": "rad",
    }

    data, units = add_MDL_motions(df=df_, units=units, meta_data=meta_data)

    exclude_keys = ["Carriage", "MA"]
    selection = data.copy()
    for key in exclude_keys:
        mask = selection.columns.str.contains(key)
        selection = selection[selection.columns[~mask]].copy()

    selection.drop(columns=["våghöjd pg"], inplace=True)

    df_save = selection.copy()

    return df_save

"""
This is a boilerplate pipeline 'load_db'
generated using Kedro 0.17.6
"""
from mdldb.run import Run
from mdldb.mdl_db import MDLDataBase, Model, LoadingCondition, Project, Ship
from mdldb.authenticate import authenticate

authenticate(dotenv_path=".env")
db = MDLDataBase()
import pandas as pd
from mdl_helpers.mdl_motions import add_MDL_motions, do_transforms


def get_project_meta_data(project_number: int) -> pd.DataFrame:
    """Get a table over all the runs in a project

    Parameters
    ----------
    project_number : int
        _description_

    Returns
    -------
    pd.DataFrame
        _description_
    """

    project = db.session.query(Project).get(int(project_number))

    query = (
        db.session.query(Run, Model, LoadingCondition, Ship)
        .filter((Run.project == project))
        .join(Model, Run.model_number == Model.model_number)
        .join(LoadingCondition, Run.loading_condition_id == LoadingCondition.id)
        .join(Ship, Run.ship_name == Ship.name)
    )

    df_all = pd.read_sql(query.statement, db.engine)
    df_all.drop(
        columns=["model_number_1", "model_number_2", "id_1", "name_1", "ship_name_1"],
        inplace=True,
    )
    df_all.set_index("id", inplace=True)
    df_all.drop(columns=["Körfallstyp", "comment"], inplace=True)

    return df_all


def select_runs(
    df_all: pd.DataFrame,
    wanted_test_types=[
        "reference speed",
        "rodergrundvinkel",
        "zigzag",
        "turning circle",
        "spiral",
    ],
    loading_condition_no=0,
) -> pd.DataFrame:
    """Select the interesting runs

    Parameters
    ----------
    df_all : pd.DataFrame
        _description_
    wanted_test_types : list, optional
        _description_, by default [ "reference speed", "rodergrundvinkel", "zigzag", "turning circle", "spiral", ]
    loading_condition_no : int, optional
        _description_, by default 0 --> first loading condition

    Returns
    -------
    pd.DataFrame
        _description_
    """
    mask = df_all["test_type"].isin(wanted_test_types)
    df_select = df_all.loc[mask].copy()

    mask = (
        df_select["loading_condition_id"]
        == df_select["loading_condition_id"].unique()[loading_condition_no]
    )
    df_select = df_select.loc[mask].copy()

    return df_select


def create_run_yml(runs_meta_data: pd.DataFrame) -> list:
    l = [str(id) for id in runs_meta_data.index]

    return l


def create_ship_data(runs_meta_data: pd.DataFrame) -> dict:

    meta_data = runs_meta_data.iloc[0]

    scale_factor = meta_data["scale_factor"]
    volume = meta_data["Volume"]
    T = (meta_data["TA"] + meta_data["TF"]) / 2
    L = meta_data["lpp"]
    B = meta_data["beam"]
    rho = 1000
    m = rho * volume

    ship_data = {
        "T": T / scale_factor,
        "L": L / scale_factor,
        "CB": volume / (L * B * T),
        "B": B / scale_factor,
        "rho": rho,
        "x_G": meta_data["lcg"] / scale_factor,
        "m": m / (scale_factor ** 3),
        "I_z": meta_data["KZZ"] ** 2 * m / (scale_factor ** 5),
        "volume": volume / (scale_factor ** 3),
        "scale_factor": scale_factor,
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
        "TA": run.loading_condition.TA,
        "TF": run.loading_condition.TF,
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

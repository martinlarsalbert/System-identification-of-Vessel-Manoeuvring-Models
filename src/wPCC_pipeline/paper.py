from myst_nb import glue
import os
import pandas as pd


def glue_table(name: str, df: pd.DataFrame, build_path="_build"):
    """Glue and save table to excell

    Parameters
    ----------
    df : pd.DataFrame
        data to table
    name : str
        name of the table (used by glue and Excell)
    build_path : str, optional
        Where should the excell file be build?, by default "_build"
    """

    if not os.path.exists(build_path):
        os.mkdir(build_path)
    df.to_excel(os.path.join(build_path, f"{name}.xlsx"))

    glue(name, df)

from sympy import latex
from vessel_manoeuvring_models.parameters import df_parameters

p = df_parameters["symbol"]


def df_to_myst(df, title="This table title", name=None, include_index=True):

    if name is None:
        name = title.replace(" ", "_")

    if include_index:
        index_name = " " if df.index.name is None else df.index.name
        matrix = [[index_name] + df.columns.tolist()] + df.reset_index().values.tolist()
    else:
        matrix = [df.columns.tolist()] + df.values.tolist()

    s = ""

    for row in matrix:
        first = True
        for col in row:
            if first:
                first = False
                s_col = f"* - {col}\n"
            else:
                s_col = f"  - {col}\n"
            s += s_col

    s_wrapped = f"""
```{{list-table}} {title}
:header-rows: 1
:name: {name}
{s}
```
"""

    return s_wrapped


def parameter_to_latex(x):

    s = latex(p[x])

    if "dot" in s:
        s += "'"

    s = f"$ {s} $"
    s = s.replace(r"\delta", "delta")
    s = s.replace("delta", r"\delta")
    s = s.replace("thrust", r"T")

    return s

from myst_nb import glue
import pandas as pd
import sympy as sp
from sympy.printing.latex import latex, multiline_latex


class Appendix:
    def __init__(self, file_path: str, title=str):

        self.file_path = file_path
        self.title = title

        with open(file_path, mode="w") as file:
            file.write(f"## {title}")

    def add_figure(self, fig, name: str, caption: str, figwidth="800px", display=False):

        glue(name, fig, display=display)

        with open(self.file_path, mode="a") as file:

            markdown = f"""
```{{glue:figure}} {name}
:figwidth: {figwidth}
:name: "fig-{name}"

{caption}
```
"""
            file.write(markdown)

    def add_table(self, df: pd.DataFrame, name: str, caption: str, display=False):

        glue(name, df, display=display)

        with open(self.file_path, mode="a") as file:

            markdown = f"""
```{{glue:figure}} {name}
:name: "tbl:{name}"

{caption}
```
"""
            file.write(markdown)

    def add_markdown(self, markdown: str):

        with open(self.file_path, mode="a") as file:
            file.write(markdown)

    def add_equation_multiline(self, eq: sp.Eq, label: str, terms_per_line=6):

        s = multiline_latex(lhs=eq.lhs, rhs=eq.rhs, terms_per_line=terms_per_line)
        s = s.replace(r"\delta", r"delta")
        s = s.replace("delta", r"\delta")
        s = s.replace("thrust", r"T")

        markdown = template_eq.format(s=s, label=label)
        self.add_markdown(markdown)

    def add_header(self, text, level=2):
        self.add_markdown(f"\n{'#'*level} {text}")


template_eq = """

$$
{s}
$$ ({label})

"""


def multiline(eq: sp.Eq, terms_per_line=6) -> str:
    s = multiline_latex(lhs=eq.lhs, rhs=eq.rhs, terms_per_line=terms_per_line)
    s = s.replace(r"\begin{align*}", r"\begin{split}")
    s = s.replace(r"\end{align*}", r"\end{split}")

    s = s.replace(r"\delta", r"delta")
    s = s.replace("delta", r"\delta")
    s = s.replace("thrust", r"T")
    return s

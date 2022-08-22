import re

file_path = r"_build/latex/System identification of Vessel Manoeuvring Models.tex"

## Open
with open(file_path, mode="r") as file:
    s = file.read()

## Fix documentclass:
s = s.replace(
    r"\documentclass[letterpaper,10pt,english]{jupyterBook}",
    r"\documentclass[review]{elsarticle}",
)

## Fix equation ref:
s = s.replace(
    r"\usepackage{hyperref}",
    r"""
\usepackage{hyperref}
\def\equationautorefname~#1\null{Eq.#1\null}""",
)

## Fix equation and fig numbering:
s = s.replace(
    r"\usepackage[,numfigreset=2,mathnumfig]{sphinx}",
    r"\usepackage[,numfigreset=1,mathnumfig]{sphinx}",
)

"""
Change to \autoref:
from: {\hyperref[\detokenize{02.10_propeller_model:equation-eqbetap}]{\sphinxcrossref{(2.19)}}}
to: \autoref{equation:02.10_propeller_model:eqbetap}
"""

for result in re.finditer(
    r"\{\\hyperref\[\\detokenize\{([^}]+)}]{\\sphinxcrossref{[^}]+}}}", s
):

    if ":equation" in result.group(1):
        notebook_name = result.group(1).split(":")[0]
        eq_label = result.group(1).split("equation-")[-1]
        s2 = r"\autoref{equation:" + notebook_name + ":" + eq_label + "}"
        s = s.replace(result.group(0), s2)


## Add fontspec
s = s.replace(
    r"\begin{document}",
    "\\begin{document}\n\input{front}\n",
)

## \bibliographystyle{elsarticle-num}
s = s.replace(
    r"\begin{document}",
    "\\bibliographystyle{elsarticle-num}\n\\begin{document}",
)

## \section*{References}
s = s.replace(
    r"\end{document}",
    # "\\section*{References}\n\\bibliography{references}\n\\end{document}",
    "\\bibliography{references}\n\\end{document}",
)

## remove cite paranthesis
# Ex:
# from: \( \cite{he_nonparametric_2022} \)
# to: \cite{he_nonparametric_2022}
for result in re.finditer(pattern=r"\\\( *\\cite{([^}]+)} *\\\)", string=s):

    replace = f"\\cite{'{'}{result.group(1)}{'}'}"
    s = s.replace(result.group(0), replace)

## Remove Proof Index
s = re.sub(
    r"\\renewcommand{\\indexname}{Proof Index}.*\\end{sphinxtheindex}",
    "",
    s,
    flags=re.DOTALL,
)

s = s.replace(r"\author{Martin Alexandersson}", "")

## Save
with open(file_path, mode="w") as file:
    file.write(s)

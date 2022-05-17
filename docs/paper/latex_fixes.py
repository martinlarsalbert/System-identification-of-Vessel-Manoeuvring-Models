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

## Add fontspec
s = s.replace(
    r"\begin{document}",
    "\\begin{document}\n\input{front}\n",
)


## Save
with open(file_path, mode="w") as file:
    file.write(s)

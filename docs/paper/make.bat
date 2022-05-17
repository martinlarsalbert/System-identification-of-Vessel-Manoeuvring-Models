cd _build\latex

pandoc "System identification of Vessel Manoeuvring Models.tex" -o "System identification of Vessel Manoeuvring Models.docx" --bibliography=../../references.bib


set PDFLATEX=latexmk -pdf -dvi- -ps-
set "LATEXOPTS= "
set XINDYOPTS=-L english -C utf8  -M sphinx.xdy
set XINDYOPTS=%XINDYOPTS% -I xelatex
%PDFLATEX% %LATEXMKOPTS% "System identification of Vessel Manoeuvring Models.tex"
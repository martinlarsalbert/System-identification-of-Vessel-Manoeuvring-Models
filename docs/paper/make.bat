cd _build\latex


set PDFLATEX=latexmk -pdf -dvi- -ps-
set "LATEXOPTS= "
set XINDYOPTS=-L english -C utf8  -M sphinx.xdy
set XINDYOPTS=%XINDYOPTS% -I xelatex
%PDFLATEX% %LATEXMKOPTS% book.tex
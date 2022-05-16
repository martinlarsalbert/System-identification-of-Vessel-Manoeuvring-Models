@ECHO OFF

REM Command file for Sphinx documentation

python fix_ref.py latex	

pushd %~dp0

set PDFLATEX=latexmk -pdf -dvi- -ps-

set "LATEXOPTS= "

set XINDYOPTS=-L english -C utf8  -M sphinx.xdy
set XINDYOPTS=%XINDYOPTS% -I xelatex
if "%1" == "" goto all-pdf

if "%1" == "all-pdf" (
	:all-pdf
	echo fix ref
	cd /d latex
	REM for %%i in (*.tex) do (
	REM	%PDFLATEX% %LATEXMKOPTS% %%i
	REM )
	%PDFLATEX% %LATEXMKOPTS% book.tex
	goto end
)

if "%1" == "all-pdf-ja" (
	goto all-pdf
)

if "%1" == "clean" (
	del /q /s *.dvi *.log *.ind *.aux *.toc *.syn *.idx *.out *.ilg *.pla *.ps *.tar *.tar.gz *.tar.bz2 *.tar.xz *.fls *.fdb_latexmk
	goto end
)

:end
popd
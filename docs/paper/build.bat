@ECHO OFF

jb build . --builder latex
::jb build . --all --builder latex

python latex_fixes.py	
CALL make.bat

:: Open PDF
"System identification of Vessel Manoeuvring Models.pdf"
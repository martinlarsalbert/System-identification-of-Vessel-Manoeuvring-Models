@ECHO OFF

jb build . --all --builder latex
python latex_fixes.py	
CALL make.bat


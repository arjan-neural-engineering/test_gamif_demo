@ECHO OFF
SETLOCAL
REM CLANG2PY works with either python2 or python3 and produces identical output, so only need to generate once
SET PYTHON=python
SET CLANG2PY="%PYTHON3_BASE%\Lib\site-packages\ctypeslib\clang2py.py"
SET incPath=%~dp0
SET incPath=%incPath:~0,-1%
SET hConfigPath=%incPath%\climber_config.h
SET PyConfigPath=%incPath%\climber_config.py
REM translation message defs
%PYTHON% %CLANG2PY% -c -k cdefmstu -i -o %PyConfigPath% %hConfigPath%
REM add PyClimberConfig Functions
type %incPath%\PyClimberConfigFunctions.py >> %PyConfigPath%
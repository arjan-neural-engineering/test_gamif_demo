#!/bin/bash
PY_INTERP=python3
CLANG2PY=/usr/local/lib/python3.7/site-packages/ctypeslib/clang2py.py
incPath=~/git/climber/include/
hConfigPath=$incPath/climber_config.h
PyConfigPath=$incPath/climber_config.py
PyClimberConfigFunctions=$incPath/PyClimberConfigFunctions.py
# translate message defs
$PY_INTERP $CLANG2PY -c -k cdefmstu -i -o $PyConfigPath $hConfigPath
# add PyCLimberConfig functions
cat $PyClimberConfigFunctions >> $PyConfigPath
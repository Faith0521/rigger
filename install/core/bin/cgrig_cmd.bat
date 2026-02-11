
@echo off
set CGRIG_CORE_TEMP=%~dp0..\
if "%CGRIGTOOLS_PRO_ROOT%" == "" (

    set CGRIGTOOLS_PRO_ROOT=%~dp0..\
) else (
    echo Custom CgRigtools root specified %CGRIGTOOLS_PRO_ROOT%
)
if "%CGRIG_PYTHON_INTERPRETER%" == "" (
    set CGRIG_PYTHON_INTERPRETER="python"
) else (
    echo Custom python interpreter specified %CGRIG_PYTHON_INTERPRETER%
)

if EXIST "%CGRIG_CORE_TEMP%\scripts\cgrig_cmd.py" (
    REM echo "calling %CGRIG_CORE_TEMP%\scripts\cgrig_cmd.py"
    %CGRIG_PYTHON_INTERPRETER% "%CGRIG_CORE_TEMP%\scripts\cgrig_cmd.py" %*
) else (
    REM echo "calling %CGRIG_CORE_TEMP%\scripts\cgrig_cmd.pyc"
    %CGRIG_PYTHON_INTERPRETER% "%CGRIG_CORE_TEMP%\scripts\cgrig_cmd.pyc" %*
)

exit /b 0
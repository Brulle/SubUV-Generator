@echo off

REM Delete the REMOVE-ME.txt file if it exists
if exist "images\REMOVE-ME.txt" (
    del "images\REMOVE-ME.txt"
    echo Removed REMOVE-ME.txt.
)

echo Running SubUVGenerator...
python main.py

REM Check the exit code of the Python script
if %ERRORLEVEL% equ 0 (
    echo SubUV Generation Succeeded.
) else (
    echo SubUV Generation Failed. Check log.txt for details.
)

pause

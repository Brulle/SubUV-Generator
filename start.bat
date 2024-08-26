@echo off
echo Running SubUVGenerator...
python main.py

REM Check the exit code of the Python script
if %ERRORLEVEL% equ 0 (
    echo SubUV Generation Succeeded.
) else (
    echo SubUV Generation Failed. Check log.txt for details.
)

pause

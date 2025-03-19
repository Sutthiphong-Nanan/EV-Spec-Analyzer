@echo off

echo Installing Python...
winget install --id Python.Python.3.13 --accept-package-agreements --accept-source-agreements

if %errorlevel% == 0 (
    echo Install succeeded.
) else (
    echo Install failed.
)

echo Press any key to exit...
pause > nul

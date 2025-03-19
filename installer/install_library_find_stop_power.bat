@echo off

set "packages=pandas numpy colorama tqdm"

echo Installing packages...

for %%i in (%packages%) do (  
    echo Installing %%i...
    pip install %%i
    if %errorlevel% neq 0 (
        echo Failed to install %%i.
		pause
    ) else (
    echo %%i Installed!
	)
)

echo All packages installed successfully!

echo Press any key to exit...
pause > nul

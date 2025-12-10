@echo off
REM NumPy Repair Tool for Windows Users
REM Automatically repairs NumPy installation

echo.
echo ============================================================
echo   NumPy Repair Tool
echo ============================================================
echo.

python fix_numpy.py

if %errorlevel% neq 0 (
    echo.
    echo Error running NumPy repair tool.
    echo.
    echo Make sure Python is installed and in your PATH.
    echo Try: python --version
    echo.
    pause
    exit /b 1
)

pause

@echo off
REM Quick Fix Tool for Windows Users
REM Runs the interactive troubleshooting script

echo.
echo ============================================================
echo   3D Trajectory GUI - Quick Fix Tool
echo ============================================================
echo.

python quick_fix.py

if %errorlevel% neq 0 (
    echo.
    echo Error running quick fix tool.
    echo.
    echo Make sure Python is installed and in your PATH.
    echo Try: python --version
    echo.
    pause
    exit /b 1
)

pause

@echo off
REM Quick ONNX Fix - Choose your method
REM This script provides a menu for the user to select the best fix method

echo ============================================================
echo          ONNX INSTALLATION FIX - QUICK START
echo ============================================================
echo.
echo This script helps you fix ONNX build errors on Windows.
echo.
echo Choose your installation method:
echo.
echo [1] Conda (RECOMMENDED - 95%% success rate)
echo     - Most reliable for Windows
echo     - Requires Conda/Miniconda installed
echo.
echo [2] Ultimate Python Fix (tries everything)
echo     - Tries multiple pip versions
echo     - Falls back to conda if available
echo.
echo [3] Diagnostic Only
echo     - Checks your environment
echo     - Provides recommendations
echo.
echo [4] Exit
echo.

choice /C 1234 /N /M "Enter your choice (1-4): "

if errorlevel 4 goto :end
if errorlevel 3 goto :diagnostic
if errorlevel 2 goto :ultimate
if errorlevel 1 goto :conda

:conda
echo.
echo ============================================================
echo Running Conda Fix...
echo ============================================================
echo.

REM Check if conda is available
where conda >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Conda not found!
    echo.
    echo You need to install Miniconda or Anaconda first:
    echo https://docs.conda.io/en/latest/miniconda.html
    echo.
    echo After installing, run this script again from Anaconda Prompt.
    echo.
    pause
    goto :end
)

REM Run the conda fix script
call fix_onnx_conda.bat
goto :end

:ultimate
echo.
echo ============================================================
echo Running Ultimate Python Fix...
echo ============================================================
echo.

python fix_onnx_ultimate.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCESS!
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo Fix script encountered issues.
    echo See recommendations above.
    echo ============================================================
)
echo.
pause
goto :end

:diagnostic
echo.
echo ============================================================
echo Running Environment Diagnostic...
echo ============================================================
echo.

python diagnose_environment.py
echo.
pause
goto :end

:end
echo.
echo Thank you for using the ONNX fix tool!
echo.
echo For more help, see:
echo   - ONNX_WINDOWS_FIX_ULTIMATE.md
echo   - TROUBLESHOOTING_ONNX.md
echo.

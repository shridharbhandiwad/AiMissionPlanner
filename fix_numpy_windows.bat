@echo off
REM Fix for NumPy MINGW-W64 warnings on Windows
REM This script reinstalls NumPy with the proper Windows binary

echo ================================================
echo NumPy Windows Fix Script
echo ================================================
echo.
echo This script fixes the NumPy MINGW-W64 experimental build warnings.
echo.
echo The issue: NumPy was built with MINGW-W64 compiler which is
echo experimental and causes crashes on Windows.
echo.
echo The solution: Reinstall NumPy using the official Windows binary.
echo.

REM Check if we're in a virtual environment
if not defined VIRTUAL_ENV (
    echo WARNING: No virtual environment detected!
    echo.
    echo It's recommended to activate your virtual environment first:
    echo   venv\Scripts\activate
    echo.
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "%CONTINUE%"=="y" (
        echo Cancelled.
        pause
        exit /b 0
    )
    echo.
)

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 2: Uninstalling existing NumPy...
pip uninstall -y numpy
echo.

echo Step 3: Clearing pip cache for NumPy...
pip cache remove numpy
echo.

echo Step 4: Installing NumPy from official Windows wheel...
echo This will download the proper Windows binary (not MINGW-W64 build)
echo Note: Python 3.12+ requires NumPy 2.x
pip install --only-binary :all: "numpy>=2.0.0,<3.0.0"
if errorlevel 1 (
    echo.
    echo WARNING: Failed with --only-binary, trying --prefer-binary...
    pip install --prefer-binary "numpy>=2.0.0,<3.0.0"
    if errorlevel 1 (
        echo ERROR: Failed to install NumPy
        echo.
        echo Try installing manually:
        echo   pip install numpy
        pause
        exit /b 1
    )
)
echo   ✓ NumPy installed successfully
echo.

echo Step 5: Verifying NumPy installation...
python -c "import numpy; print('NumPy version:', numpy.__version__); print('NumPy file location:', numpy.__file__); import numpy.core._multiarray_umath; print('✓ NumPy working correctly!')"
if errorlevel 1 (
    echo.
    echo ERROR: NumPy verification failed!
    echo.
    echo The installation might be corrupted. Try:
    echo   1. Close all Python processes
    echo   2. Run this script again
    echo   3. If still failing, reinstall Python
    pause
    exit /b 1
)
echo.

echo ================================================
echo NumPy Fixed Successfully!
echo ================================================
echo.
echo NumPy should now work without MINGW-W64 warnings.
echo.
echo You can now run the trajectory GUI:
echo   python run_trajectory_gui.py
echo.
pause

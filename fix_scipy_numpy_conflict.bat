@echo off
REM Fix for NumPy/SciPy version conflict on Windows
REM This script resolves the incompatibility between numpy 2.3.5 and scipy 1.14.1

echo ================================================
echo NumPy/SciPy Compatibility Fix
echo ================================================
echo.
echo Issue: scipy 1.14.1 requires numpy^<2.3, but numpy 2.3.5 was installed
echo Solution: Reinstall numpy with version constraint compatible with scipy
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
pip cache remove numpy 2>nul
echo.

echo Step 4: Reinstalling numpy (ensuring Windows binary)...
echo Installing numpy version compatible with scipy 1.14.1
echo Version constraint: numpy^>=2.0.0,^<2.3
pip install --only-binary :all: "numpy>=2.0.0,<2.3"
if errorlevel 1 (
    echo.
    echo WARNING: Failed with --only-binary, trying --prefer-binary...
    pip install --prefer-binary "numpy>=2.0.0,<2.3"
    if errorlevel 1 (
        echo ERROR: Failed to install NumPy
        echo.
        echo Try installing manually:
        echo   pip install "numpy>=2.0.0,<2.3"
        pause
        exit /b 1
    )
)
echo   ✓ NumPy installed successfully
echo.

echo Step 5: Verifying installations...
python -c "import numpy; import scipy; print('NumPy version:', numpy.__version__); print('SciPy version:', scipy.__version__); print(''); print('✓ Both packages working correctly!')"
if errorlevel 1 (
    echo.
    echo ERROR: Verification failed!
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
echo Fix Applied Successfully!
echo ================================================
echo.
echo NumPy and SciPy are now compatible.
echo.
echo You can now run the trajectory GUI:
echo   python run_trajectory_gui.py
echo.
pause

@echo off
REM Fix matplotlib DLL import error on Windows
REM This script fixes: ImportError: DLL load failed while importing _c_internal_utils

echo ========================================
echo Matplotlib DLL Error Fix for Windows
echo ========================================
echo.
echo This will fix the error:
echo "ImportError: DLL load failed while importing _c_internal_utils"
echo.

REM Check if in virtual environment
if not defined VIRTUAL_ENV (
    echo ERROR: Virtual environment not activated!
    echo.
    echo Please activate your virtual environment first:
    echo   venv\Scripts\activate
    echo.
    echo Then run this script again.
    pause
    exit /b 1
)

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)
echo ✓ Pip upgraded successfully
echo.

echo Step 2: Uninstalling matplotlib and related packages...
pip uninstall -y matplotlib pillow kiwisolver contourpy cycler fonttools pyparsing
echo ✓ Packages uninstalled
echo.

echo Step 3: Clearing pip cache...
pip cache purge
echo ✓ Cache cleared
echo.

echo Step 4: Reinstalling numpy (ensuring Windows binary)...
pip uninstall -y numpy
pip install --only-binary :all: --force-reinstall "numpy>=2.0.0,<2.3"
if errorlevel 1 (
    echo ERROR: Failed to install numpy
    echo.
    echo This usually means:
    echo 1. Your Python version is incompatible (need 3.9-3.12)
    echo 2. Internet connection issue
    echo.
    pause
    exit /b 1
)
echo ✓ NumPy installed successfully
echo.

echo Step 5: Installing matplotlib dependencies...
pip install --only-binary :all: pillow kiwisolver contourpy cycler fonttools pyparsing packaging python-dateutil
if errorlevel 1 (
    echo WARNING: Some dependencies may have failed, continuing...
)
echo ✓ Dependencies installed
echo.

echo Step 6: Installing matplotlib...
pip install --only-binary :all: --force-reinstall matplotlib==3.9.0
if errorlevel 1 (
    echo ERROR: Failed to install matplotlib
    pause
    exit /b 1
)
echo ✓ Matplotlib installed successfully
echo.

echo Step 7: Verifying matplotlib import...
python -c "import matplotlib; import matplotlib.pyplot as plt; print('✓ Matplotlib working correctly!')"
if errorlevel 1 (
    echo.
    echo ====================================================
    echo WARNING: Matplotlib still has import issues
    echo ====================================================
    echo.
    echo This typically means you need to install Microsoft
    echo Visual C++ Redistributables.
    echo.
    echo Please download and install from:
    echo https://aka.ms/vs/17/release/vc_redist.x64.exe
    echo.
    echo After installing, restart your computer and try again.
    echo.
    echo Alternative: Try using Conda instead of pip:
    echo   conda install matplotlib
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ SUCCESS! Matplotlib is working!
echo ========================================
echo.
echo You can now run your script:
echo   python src/data_generator.py
echo.
pause

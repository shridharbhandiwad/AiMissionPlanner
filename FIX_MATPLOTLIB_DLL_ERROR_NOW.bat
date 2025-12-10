@echo off
REM Enhanced Matplotlib DLL Fix Script for Windows
REM Fixes: ImportError: DLL load failed while importing _c_internal_utils

echo ============================================================
echo   MATPLOTLIB DLL ERROR - COMPREHENSIVE FIX
echo ============================================================
echo.
echo This script will fix the error:
echo "ImportError: DLL load failed while importing _c_internal_utils"
echo.
echo Estimated time: 3-5 minutes
echo.

REM Check if in virtual environment
if not defined VIRTUAL_ENV (
    echo [ERROR] Virtual environment not activated!
    echo.
    echo Please run: venv\Scripts\activate
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo [1/9] Checking Python version...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo.

echo [2/9] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [WARNING] Pip upgrade had issues, continuing...
)
echo.

echo [3/9] Uninstalling matplotlib and all dependencies...
pip uninstall -y matplotlib pillow kiwisolver contourpy cycler fonttools pyparsing packaging python-dateutil
echo Done.
echo.

echo [4/9] Uninstalling numpy...
pip uninstall -y numpy
echo Done.
echo.

echo [5/9] Clearing pip cache...
pip cache purge
echo Done.
echo.

echo [6/9] Installing numpy (forcing Windows binary wheel)...
pip install --only-binary :all: --no-cache-dir "numpy>=2.0.0,<2.3"
if errorlevel 1 (
    echo [ERROR] Failed to install numpy.
    echo.
    echo This usually means one of the following:
    echo  - Your Python version is incompatible (requires Python 3.9-3.12)
    echo  - No internet connection
    echo  - Pip configuration issue
    echo.
    echo Please check your Python version with: python --version
    echo.
    pause
    exit /b 1
)
echo Done.
echo.

echo [7/9] Installing matplotlib dependencies...
pip install --only-binary :all: --no-cache-dir pillow kiwisolver contourpy cycler fonttools pyparsing packaging python-dateutil
if errorlevel 1 (
    echo [WARNING] Some dependencies may have issues, continuing...
)
echo Done.
echo.

echo [8/9] Installing matplotlib 3.9.0 (forcing Windows binary wheel)...
pip install --only-binary :all: --no-cache-dir matplotlib==3.9.0
if errorlevel 1 (
    echo [ERROR] Failed to install matplotlib.
    echo.
    echo Trying alternative version...
    pip install --only-binary :all: --no-cache-dir matplotlib==3.8.4
    if errorlevel 1 (
        echo [ERROR] Both versions failed.
        echo.
        echo Please try the manual fix steps below.
        pause
        exit /b 1
    )
)
echo Done.
echo.

echo [9/9] Testing matplotlib import...
python -c "import matplotlib; import matplotlib.pyplot as plt; import numpy as np; print('SUCCESS: Matplotlib imported successfully!')"
if errorlevel 1 (
    echo.
    echo ============================================================
    echo   ADDITIONAL STEPS REQUIRED
    echo ============================================================
    echo.
    echo The packages are installed but matplotlib still can't load.
    echo This means you need to install Microsoft Visual C++ Redistributables.
    echo.
    echo PLEASE FOLLOW THESE STEPS:
    echo.
    echo 1. Download Visual C++ Redistributables:
    echo    https://aka.ms/vs/17/release/vc_redist.x64.exe
    echo.
    echo 2. Install the downloaded file (vc_redist.x64.exe^)
    echo.
    echo 3. RESTART YOUR COMPUTER (this is required!)
    echo.
    echo 4. After restart, activate your venv and test:
    echo    venv\Scripts\activate
    echo    python src/data_generator.py
    echo.
    echo ============================================================
    echo   ALTERNATIVE: USE CONDA
    echo ============================================================
    echo.
    echo If the above doesn't work, Conda handles C dependencies better:
    echo.
    echo 1. Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
    echo 2. Create environment: conda create -n aimp python=3.11
    echo 3. Activate: conda activate aimp
    echo 4. Install packages: conda install matplotlib numpy scipy
    echo 5. Install others: pip install torch torchvision
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   SUCCESS! MATPLOTLIB IS WORKING!
echo ============================================================
echo.
echo You can now run your script:
echo   python src/data_generator.py
echo.
echo Press any key to run a quick test...
pause

echo.
echo Running quick test with data_generator.py import...
python -c "from src.data_generator import TrajectoryGenerator; print('All imports successful!')"
if errorlevel 1 (
    echo.
    echo [WARNING] Script imports had issues.
    echo Check if there are other missing dependencies.
    echo.
) else (
    echo.
    echo [SUCCESS] All imports working correctly!
    echo.
)

pause

@echo off
REM ONNX Installation Fix - Conda Method (Most Reliable for Windows)
REM This script uses Conda which has the highest success rate on Windows

echo ============================================================
echo ONNX Installation Fix - Conda Method
echo ============================================================
echo.
echo This is the MOST RELIABLE method for Windows!
echo.

REM Check if conda is available
where conda >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Conda is not installed or not in PATH
    echo.
    echo SOLUTION: Install Miniconda or Anaconda
    echo.
    echo 1. Download Miniconda from: https://docs.conda.io/en/latest/miniconda.html
    echo 2. Install it (choose "Add Conda to PATH" during installation)
    echo 3. Restart this command prompt
    echo 4. Run this script again
    echo.
    echo OR run this script from "Anaconda Prompt" if you already have Anaconda
    pause
    exit /b 1
)

echo [1/6] Conda detected: OK
conda --version
echo.

REM Check if we're in the trajectory environment
echo [2/6] Checking for existing trajectory environment...
conda env list | findstr trajectory >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Trajectory environment already exists
    choice /C YN /M "Do you want to recreate it (removes old environment)"
    if %ERRORLEVEL% EQU 1 (
        echo Removing old environment...
        conda env remove -n trajectory -y
    )
)
echo.

REM Create new conda environment with Python 3.11 or 3.13
echo [3/6] Creating conda environment with Python 3.11...
echo (Python 3.11 and 3.13 are both compatible with latest ONNX)
conda create -n trajectory python=3.11 -y
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create conda environment
    pause
    exit /b 1
)
echo.

REM Activate environment
echo [4/6] Activating trajectory environment...
call conda activate trajectory
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate environment
    echo Try running this from Anaconda Prompt
    pause
    exit /b 1
)
echo.

REM Install ONNX and ONNX Runtime from conda-forge
echo [5/6] Installing ONNX and ONNX Runtime from conda-forge...
echo This will install pre-built binaries (no compilation needed!)
conda install -c conda-forge onnx onnxruntime -y
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install ONNX via conda
    echo This is very unusual. Check your internet connection.
    pause
    exit /b 1
)
echo.

REM Verify installation
echo [6/6] Verifying installation...
python -c "import onnx; print('ONNX version:', onnx.__version__)"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ONNX import failed
    pause
    exit /b 1
)

python -c "import onnxruntime; print('ONNX Runtime version:', onnxruntime.__version__)"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ONNX Runtime import failed
    pause
    exit /b 1
)
echo.

echo ============================================================
echo SUCCESS! ONNX is installed correctly!
echo ============================================================
echo.
echo Next steps:
echo.
echo 1. Install PyTorch (choose CPU or GPU):
echo.
echo    For CPU:
echo    pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
echo.
echo    For GPU (CUDA 11.8):
echo    pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118
echo.
echo 2. Install remaining dependencies:
echo    pip install -r requirements.txt
echo.
echo 3. Verify everything works:
echo    python -c "import torch, onnx, onnxruntime; print('All OK!')"
echo.
echo 4. Start using the system:
echo    python src/data_generator.py
echo    python src/train.py
echo.
echo Remember to activate the environment before working:
echo    conda activate trajectory
echo.
pause

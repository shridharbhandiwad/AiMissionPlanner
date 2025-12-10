@echo off
REM Windows Installation Script for AI-Enabled Mission Trajectory Planner
REM This script handles the installation with pre-built wheels to avoid build errors

echo ================================================
echo AI-Enabled Mission Trajectory Planner
echo Windows Installation Script
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9-3.12 from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Checking Python version...
python --version
echo.

echo Step 2: Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)
echo.

echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

echo Step 4: Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip tools, continuing anyway...
)
echo.

echo Step 5: Installing dependencies with pre-built wheels...
echo This may take 5-10 minutes depending on your internet connection.
echo.

REM Install ONNX packages first with binary-only flag
echo Installing ONNX packages...
pip install --only-binary :all: onnx==1.18.0 onnxruntime==1.20.0
if errorlevel 1 (
    echo.
    echo WARNING: Failed to install ONNX with --only-binary flag
    echo Trying with --prefer-binary instead...
    pip install --prefer-binary onnx==1.18.0 onnxruntime==1.20.0
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install ONNX packages
        echo Please see ONNX_INSTALLATION_FIX.md for troubleshooting steps
        pause
        exit /b 1
    )
)
echo.

REM Install PyTorch (CPU version by default)
echo Installing PyTorch (CPU version)...
echo For GPU support, see README.md for CUDA installation instructions
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo ERROR: Failed to install PyTorch
    pause
    exit /b 1
)
echo.

REM Install remaining packages (numpy 2.x for Python 3.12+, constrained for scipy compatibility)
echo Installing remaining packages...
pip install "numpy>=2.0.0,<2.3" scipy==1.14.1 pandas==2.2.3 scikit-learn==1.5.2 matplotlib==3.9.0 seaborn==0.13.0 plotly==5.24.0 tensorboard==2.18.0 tqdm==4.66.1 fastapi==0.115.0 "uvicorn[standard]==0.30.0" pydantic==2.9.0 python-multipart==0.0.12 shapely==2.0.6 pytest==8.3.0
if errorlevel 1 (
    echo ERROR: Failed to install remaining packages
    pause
    exit /b 1
)
echo.

REM Install GUI packages
echo Installing GUI packages (PyQt5, PyQtGraph, PyOpenGL)...
pip install PyQt5==5.15.11 PyQtGraph==0.13.7 PyOpenGL==3.1.7 PyOpenGL_accelerate==3.1.7
if errorlevel 1 (
    echo WARNING: Failed to install GUI packages with accelerate
    echo Trying without PyOpenGL_accelerate...
    pip install PyQt5==5.15.11 PyQtGraph==0.13.7 PyOpenGL==3.1.7
    if errorlevel 1 (
        echo ERROR: Failed to install GUI packages
        echo The GUI will not work without these packages.
        pause
        exit /b 1
    )
)
echo.

echo ================================================
echo Installation completed successfully!
echo ================================================
echo.
echo Verifying installation...
python -c "import torch; import onnx; import onnxruntime; from PyQt5 import QtCore; import pyqtgraph; print('PyTorch:', torch.__version__); print('ONNX:', onnx.__version__); print('ONNX Runtime:', onnxruntime.__version__); print('PyQt5:', QtCore.QT_VERSION_STR); print('PyQtGraph:', pyqtgraph.__version__); print('\n✓ All packages installed successfully!')"
if errorlevel 1 (
    echo.
    echo WARNING: Verification failed. Some packages may not be installed correctly.
    echo.
    echo To diagnose and fix issues, run:
    echo   fix_all_dependencies.bat
    echo.
    echo Or see: WINDOWS_GUI_FIX.md
) else (
    echo.
    echo You can now use the system!
    echo.
    echo Quick start:
    echo   1. Run 3D Trajectory GUI:  python run_trajectory_gui.py
    echo   2. Generate dataset:       python src/data_generator.py
    echo   3. Train model:            python src/train.py
    echo   4. Generate trajectory:    python src/inference.py
    echo.
    echo For more information, see README.md
)
echo.
echo To activate the virtual environment in the future, run:
echo   venv\Scripts\activate
echo.
pause

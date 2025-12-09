@echo off
REM ONNX Build Error Fix Script for Windows
REM Run this if you encounter "Failed building wheel for onnx" error

echo ================================================
echo ONNX Build Error Fix for Windows
echo ================================================
echo.
echo This script will fix the ONNX installation error by:
echo 1. Upgrading pip and build tools
echo 2. Installing ONNX with pre-built wheels only
echo 3. Verifying the installation
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9-3.12 from https://www.python.org/
    pause
    exit /b 1
)

echo Current Python version:
python --version
echo.

REM Check if we're in a virtual environment
python -c "import sys; exit(0 if sys.prefix != sys.base_prefix else 1)" >nul 2>&1
if errorlevel 1 (
    echo WARNING: No virtual environment detected!
    echo.
    echo It's recommended to use a virtual environment.
    echo Do you want to create one now? (Y/N)
    set /p CREATE_VENV=
    if /i "%CREATE_VENV%"=="Y" (
        echo Creating virtual environment...
        python -m venv venv
        if errorlevel 1 (
            echo ERROR: Failed to create virtual environment
            pause
            exit /b 1
        )
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
        echo Virtual environment activated!
        echo.
    ) else (
        echo Proceeding without virtual environment...
        echo.
    )
) else (
    echo ✓ Virtual environment detected
    echo.
)

echo Step 1: Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip tools
    echo.
    echo Try running this script as Administrator:
    echo   Right-click Command Prompt -^> Run as administrator
    pause
    exit /b 1
)
echo ✓ pip tools upgraded successfully!
echo.

echo Step 2: Uninstalling any existing ONNX packages...
pip uninstall -y onnx onnxruntime 2>nul
echo.

echo Step 3: Installing ONNX with pre-built wheels...
echo Attempting to install ONNX 1.16.1 and ONNXRuntime 1.19.2
echo.

REM Try --only-binary first (most reliable)
echo Method 1: Installing with --only-binary flag...
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
if errorlevel 1 (
    echo.
    echo Method 1 failed. Trying Method 2...
    echo.
    
    REM Try --prefer-binary
    echo Method 2: Installing with --prefer-binary flag...
    pip install --prefer-binary onnx==1.16.1 onnxruntime==1.19.2
    if errorlevel 1 (
        echo.
        echo Method 2 failed. Trying Method 3...
        echo.
        
        REM Try older version with better wheel coverage
        echo Method 3: Installing older version (1.15.0) with better wheel coverage...
        pip install --only-binary :all: onnx==1.15.0 onnxruntime==1.16.3
        if errorlevel 1 (
            echo.
            echo ================================================
            echo ERROR: All automatic fix methods failed
            echo ================================================
            echo.
            echo This usually means:
            echo 1. Your Python version is too new (3.13+) or too old (^<3.8)
            echo 2. Your platform is not supported
            echo 3. Internet connection issues
            echo.
            echo Recommended solutions:
            echo.
            echo A. Use Python 3.11 or 3.10 (best compatibility)
            echo    Download from: https://www.python.org/
            echo.
            echo B. Use Anaconda/Miniconda:
            echo    conda install -c conda-forge onnx onnxruntime
            echo.
            echo C. Use Docker or WSL2 for Linux environment
            echo.
            echo See ONNX_INSTALLATION_FIX.md for detailed troubleshooting.
            echo.
            pause
            exit /b 1
        )
        echo ✓ ONNX 1.15.0 installed successfully!
        set ONNX_VERSION=1.15.0
    ) else (
        echo ✓ ONNX 1.16.1 installed successfully!
        set ONNX_VERSION=1.16.1
    )
) else (
    echo ✓ ONNX 1.16.1 installed successfully!
    set ONNX_VERSION=1.16.1
)
echo.

echo Step 4: Verifying installation...
python -c "import onnx; import onnxruntime; print('ONNX version:', onnx.__version__); print('ONNX Runtime version:', onnxruntime.__version__)"
if errorlevel 1 (
    echo.
    echo WARNING: Verification failed
    echo ONNX packages may not be properly installed.
    echo.
    pause
    exit /b 1
)
echo.

echo ================================================
echo ✓ ONNX installation fixed successfully!
echo ================================================
echo.
echo You can now proceed with installing other dependencies:
echo.
echo For CPU version:
echo   pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
echo   pip install -r requirements.txt
echo.
echo For GPU version (CUDA 11.8):
echo   pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118
echo   pip install -r requirements.txt
echo.
echo Or simply run:
echo   install_windows.bat
echo.
pause

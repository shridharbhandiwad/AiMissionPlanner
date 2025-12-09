@echo off
REM ============================================================
REM ONNX Installation Fix - Conda Method (Most Reliable)
REM ============================================================
REM This is the most reliable method for Windows users
REM
REM Prerequisites: Miniconda or Anaconda installed
REM Download from: https://docs.conda.io/en/latest/miniconda.html
REM ============================================================

echo.
echo ============================================================
echo ONNX Installation Fix - Conda Method
echo ============================================================
echo.
echo This is the MOST RELIABLE method for Windows!
echo.
echo Prerequisites Check:
echo - Miniconda or Anaconda must be installed
echo - If not installed, download from:
echo   https://docs.conda.io/en/latest/miniconda.html
echo.

REM Check if conda is available
where conda >nul 2>&1
if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Conda is not installed or not in PATH
    echo ============================================================
    echo.
    echo Please install Miniconda first:
    echo.
    echo 1. Download Miniconda from:
    echo    https://docs.conda.io/en/latest/miniconda.html
    echo.
    echo 2. Run the installer
    echo.
    echo 3. Restart Command Prompt
    echo.
    echo 4. Run this script again
    echo.
    echo ============================================================
    echo.
    echo Alternative: Use the regular pip fix instead
    echo   python fix_onnx.py
    echo.
    pause
    exit /b 1
)

echo ✓ Conda detected!
echo.
conda --version
echo.

echo ============================================================
echo Step 1: Creating conda environment 'trajectory'
echo ============================================================
echo.

REM Check if environment already exists
conda env list | findstr "trajectory" >nul 2>&1
if errorlevel 1 (
    echo Creating new environment with Python 3.11...
    conda create -n trajectory python=3.11 -y
    if errorlevel 1 (
        echo ERROR: Failed to create conda environment
        pause
        exit /b 1
    )
    echo ✓ Environment created successfully!
) else (
    echo Environment 'trajectory' already exists.
    echo.
    set /p RECREATE="Do you want to recreate it? (Y/N): "
    if /i "%RECREATE%"=="Y" (
        echo Removing existing environment...
        conda env remove -n trajectory -y
        echo Creating new environment with Python 3.11...
        conda create -n trajectory python=3.11 -y
        if errorlevel 1 (
            echo ERROR: Failed to create conda environment
            pause
            exit /b 1
        )
        echo ✓ Environment recreated successfully!
    ) else (
        echo Using existing environment.
    )
)
echo.

echo ============================================================
echo Step 2: Installing ONNX packages via conda
echo ============================================================
echo.
echo This is the most reliable installation method!
echo Installing from conda-forge channel...
echo.

call conda activate trajectory
if errorlevel 1 (
    echo ERROR: Failed to activate environment
    pause
    exit /b 1
)

echo Installing ONNX and ONNX Runtime...
conda install -c conda-forge onnx onnxruntime -y
if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Failed to install ONNX via conda
    echo ============================================================
    echo.
    echo This is unusual for conda. Possible causes:
    echo - Internet connection issues
    echo - Conda configuration problems
    echo.
    echo Try:
    echo 1. Check internet connection
    echo 2. Update conda: conda update conda
    echo 3. Clear conda cache: conda clean --all
    echo.
    pause
    exit /b 1
)

echo ✓ ONNX packages installed successfully!
echo.

echo ============================================================
echo Step 3: Verifying installation
echo ============================================================
echo.

python -c "import onnx; import onnxruntime; print('✓ ONNX version:', onnx.__version__); print('✓ ONNX Runtime version:', onnxruntime.__version__)"
if errorlevel 1 (
    echo.
    echo WARNING: Verification failed
    echo ONNX may not be properly installed.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✓ SUCCESS! ONNX is installed and working!
echo ============================================================
echo.

echo ============================================================
echo Step 4: Installing PyTorch
echo ============================================================
echo.
echo Choose PyTorch version:
echo.
echo [1] CPU version (smaller, works everywhere)
echo [2] GPU version (requires NVIDIA GPU with CUDA)
echo.
set /p PYTORCH_CHOICE="Enter choice (1 or 2): "

if "%PYTORCH_CHOICE%"=="2" (
    echo.
    echo Installing PyTorch with CUDA 11.8 support...
    pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118
) else (
    echo.
    echo Installing PyTorch CPU version...
    pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
)

if errorlevel 1 (
    echo.
    echo WARNING: PyTorch installation had issues
    echo You may need to install it manually later.
    echo.
) else (
    echo ✓ PyTorch installed successfully!
)
echo.

echo ============================================================
echo Step 5: Installing remaining dependencies
echo ============================================================
echo.

if exist requirements.txt (
    echo Installing from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo WARNING: Some dependencies may have failed to install
        echo Check the output above for details.
        echo.
    ) else (
        echo ✓ All dependencies installed!
    )
) else (
    echo requirements.txt not found in current directory
    echo Skipping...
)
echo.

echo ============================================================
echo Step 6: Final verification
echo ============================================================
echo.

python -c "import torch, onnx, onnxruntime; print('✓ All critical imports successful!'); print('  PyTorch:', torch.__version__); print('  ONNX:', onnx.__version__); print('  ONNX Runtime:', onnxruntime.__version__)"
if errorlevel 1 (
    echo.
    echo ============================================================
    echo WARNING: Some imports failed
    echo ============================================================
    echo.
    echo You may need to troubleshoot individual packages.
    echo.
) else (
    echo.
    echo ============================================================
    echo ✓✓✓ COMPLETE SUCCESS! ✓✓✓
    echo ============================================================
    echo.
    echo Your environment is ready to use!
    echo.
    echo Next steps:
    echo.
    echo 1. Activate the environment whenever you work on this project:
    echo    conda activate trajectory
    echo.
    echo 2. Run the training pipeline:
    echo    python src/train.py
    echo.
    echo 3. Generate data:
    echo    python src/data_generator.py
    echo.
    echo 4. Run inference:
    echo    python src/inference.py
    echo.
    echo 5. Start API server:
    echo    python api/app.py
    echo.
)

echo ============================================================
echo Environment Information
echo ============================================================
echo.
echo To use this environment:
echo   conda activate trajectory
echo.
echo To deactivate:
echo   conda deactivate
echo.
echo To list all conda environments:
echo   conda env list
echo.
echo To update packages:
echo   conda update --all
echo.
echo ============================================================
echo.

pause

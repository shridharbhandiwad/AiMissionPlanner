@echo off
REM Comprehensive fix script for all GUI and NumPy issues
REM This script fixes both NumPy MINGW-W64 issues and missing GUI packages

echo ================================================
echo All Dependencies Fix Script
echo ================================================
echo.
echo This script will:
echo   1. Fix NumPy MINGW-W64 issues
echo   2. Install/fix PyQt5
echo   3. Install/fix PyQtGraph
echo   4. Install/fix PyOpenGL
echo   5. Verify all installations
echo.

REM Check if we're in a virtual environment
if not defined VIRTUAL_ENV (
    echo WARNING: No virtual environment detected!
    echo.
    echo You should activate your virtual environment first:
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

echo Starting dependency fixes...
echo.

REM ============================================================
REM PART 1: Fix NumPy
REM ============================================================
echo ================================================
echo PART 1: Fixing NumPy (MINGW-W64 issue)
echo ================================================
echo.

echo Step 1.1: Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)
echo.

echo Step 1.2: Uninstalling existing NumPy...
pip uninstall -y numpy
echo.

echo Step 1.3: Clearing pip cache for NumPy...
pip cache remove numpy 2>nul
echo.

echo Step 1.4: Installing NumPy from official Windows wheel...
pip install --only-binary :all: numpy==1.26.4
if errorlevel 1 (
    echo WARNING: Failed with --only-binary, trying --prefer-binary...
    pip install --prefer-binary numpy==1.26.4
    if errorlevel 1 (
        echo ERROR: Failed to install NumPy
        pause
        exit /b 1
    )
)
echo   ✓ NumPy installed successfully
echo.

echo Step 1.5: Verifying NumPy...
python -c "import numpy; print('NumPy version:', numpy.__version__)"
if errorlevel 1 (
    echo ERROR: NumPy verification failed!
    pause
    exit /b 1
)
echo   ✓ NumPy verified successfully
echo.

REM ============================================================
REM PART 2: Install GUI Dependencies
REM ============================================================
echo ================================================
echo PART 2: Installing GUI Dependencies
echo ================================================
echo.

echo Step 2.1: Uninstalling old GUI packages...
pip uninstall -y PyQt5 PyQt5-Qt5 PyQt5-sip PyQtGraph PyOpenGL PyOpenGL-accelerate 2>nul
echo.

echo Step 2.2: Installing PyQt5...
pip install PyQt5==5.15.11
if errorlevel 1 (
    echo ERROR: Failed to install PyQt5
    pause
    exit /b 1
)
echo   ✓ PyQt5 installed
echo.

echo Step 2.3: Installing PyQtGraph...
pip install PyQtGraph==0.13.7
if errorlevel 1 (
    echo ERROR: Failed to install PyQtGraph
    pause
    exit /b 1
)
echo   ✓ PyQtGraph installed
echo.

echo Step 2.4: Installing PyOpenGL...
pip install PyOpenGL==3.1.7
if errorlevel 1 (
    echo ERROR: Failed to install PyOpenGL
    pause
    exit /b 1
)
echo   ✓ PyOpenGL installed
echo.

echo Step 2.5: Installing PyOpenGL accelerate (optional)...
pip install PyOpenGL_accelerate==3.1.7
if errorlevel 1 (
    echo   (Optional package - GUI will work without it)
)
echo.

REM ============================================================
REM PART 3: Comprehensive Verification
REM ============================================================
echo ================================================
echo PART 3: Verifying All Packages
echo ================================================
echo.

echo Verifying installations...
python -c "import numpy; from PyQt5 import QtWidgets, QtCore, QtGui; import pyqtgraph; import pyqtgraph.opengl as gl; print('\n✓ All packages verified successfully!\n'); print('NumPy:', numpy.__version__); print('PyQt5:', QtCore.QT_VERSION_STR); print('PyQtGraph:', pyqtgraph.__version__)"
if errorlevel 1 (
    echo.
    echo ERROR: Package verification failed!
    echo.
    echo Some packages may not be working correctly.
    echo Try running: python diagnose_gui_startup.py
    pause
    exit /b 1
)

echo.
echo ================================================
echo SUCCESS! All Dependencies Fixed
echo ================================================
echo.
echo All packages are now properly installed and verified.
echo.
echo You can now run the trajectory GUI with:
echo   python run_trajectory_gui.py
echo.
echo Or try the examples:
echo   python examples\trajectory_gui_examples.py
echo.
pause

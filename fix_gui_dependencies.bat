@echo off
REM Quick fix script for GUI dependencies
REM Run this if you're getting "No module named 'PyQt5'" or similar errors

echo ================================================
echo GUI Dependencies Fix Script
echo ================================================
echo.
echo This script will install/fix the GUI packages:
echo   - PyQt5
echo   - PyQtGraph
echo   - PyOpenGL
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

echo Step 2: Uninstalling old GUI packages (if any)...
pip uninstall -y PyQt5 PyQt5-Qt5 PyQt5-sip PyQtGraph PyOpenGL PyOpenGL-accelerate
echo.

echo Step 3: Installing PyQt5...
pip install PyQt5==5.15.11
if errorlevel 1 (
    echo ERROR: Failed to install PyQt5
    echo.
    echo Try installing manually:
    echo   pip install PyQt5
    pause
    exit /b 1
)
echo   ✓ PyQt5 installed successfully
echo.

echo Step 4: Installing PyQtGraph...
pip install PyQtGraph==0.13.7
if errorlevel 1 (
    echo ERROR: Failed to install PyQtGraph
    pause
    exit /b 1
)
echo   ✓ PyQtGraph installed successfully
echo.

echo Step 5: Installing PyOpenGL...
pip install PyOpenGL==3.1.7
if errorlevel 1 (
    echo ERROR: Failed to install PyOpenGL
    pause
    exit /b 1
)
echo   ✓ PyOpenGL installed successfully
echo.

echo Step 6: Installing PyOpenGL accelerate (optional)...
pip install PyOpenGL_accelerate==3.1.7
if errorlevel 1 (
    echo WARNING: Failed to install PyOpenGL_accelerate
    echo This is optional - the GUI will still work without it.
) else (
    echo   ✓ PyOpenGL_accelerate installed successfully
)
echo.

echo Step 7: Verifying installation...
python -c "from PyQt5 import QtWidgets, QtCore, QtGui; import pyqtgraph; import pyqtgraph.opengl; print('All GUI packages imported successfully!')"
if errorlevel 1 (
    echo.
    echo ERROR: Verification failed!
    echo The packages installed but cannot be imported.
    echo.
    echo This might indicate a compatibility issue with your Python version.
    echo Try using Python 3.9, 3.10, 3.11, or 3.12.
    pause
    exit /b 1
)
echo.

echo ================================================
echo GUI Dependencies Fixed Successfully!
echo ================================================
echo.
echo You can now run the trajectory GUI:
echo   python run_trajectory_gui.py
echo.
pause

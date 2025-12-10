@echo off
REM Windows batch script to run the 3D Trajectory Generator GUI

echo ============================================================
echo 3D Trajectory Generator GUI
echo ============================================================
echo.
echo Starting application...
echo.

REM Run the GUI application
python run_trajectory_gui.py

REM Check if it failed
if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Failed to start GUI
    echo ============================================================
    echo.
    echo Make sure you have installed the required dependencies:
    echo   pip install PyQt5 PyQtGraph PyOpenGL PyOpenGL_accelerate scipy
    echo.
    echo If you're in a conda environment, try:
    echo   conda install pyqt pyqtgraph
    echo   pip install PyOpenGL PyOpenGL_accelerate
    echo.
    pause
    exit /b 1
)

REM If we get here without error but window didn't appear, show message
echo.
echo If the window did not appear, press Ctrl+C and check:
echo   1. Your Python environment has all dependencies installed
echo   2. Your display drivers support OpenGL
echo   3. Try running: python run_trajectory_gui.py directly
echo.

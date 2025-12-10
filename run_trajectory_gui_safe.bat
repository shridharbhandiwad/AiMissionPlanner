@echo off
REM Safe launcher for Trajectory GUI that catches hard crashes

python run_trajectory_gui_safe.py

REM If Python exits immediately, pause to see error
if errorlevel 1 (
    echo.
    echo ============================================================
    echo Application exited with error
    echo ============================================================
    pause
)

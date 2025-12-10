@echo off
REM Test script to check if GUI can be displayed

echo ============================================================
echo GUI Display Diagnostic Test
echo ============================================================
echo.
echo This will test if PyQt5 can create windows on your system.
echo.

python test_gui_display.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo TEST FAILED
    echo ============================================================
    echo.
    echo There is a problem with your PyQt5 installation.
    echo.
    pause
    exit /b 1
)

echo.
echo Test completed.
pause

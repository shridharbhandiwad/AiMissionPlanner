@echo off
REM Quick diagnostic and fix menu for GUI issues

:MENU
cls
echo ============================================================
echo   TRAJECTORY GUI - DIAGNOSTIC AND FIX MENU
echo ============================================================
echo.
echo   Your Issue: App exits silently after "Checking NumPy..."
echo.
echo ============================================================
echo   CHOOSE AN OPTION:
echo ============================================================
echo.
echo   1. Run Safe Launcher (RECOMMENDED - catches crashes)
echo   2. Diagnose NumPy Issues
echo   3. Run Full GUI Diagnostics
echo   4. Test NumPy in Python REPL
echo   5. Run Regular Launcher
echo   6. Install/Reinstall NumPy
echo   7. View Quick Fix Guide
echo   8. Exit
echo.
echo ============================================================

set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto SAFE_LAUNCHER
if "%choice%"=="2" goto NUMPY_DIAG
if "%choice%"=="3" goto FULL_DIAG
if "%choice%"=="4" goto TEST_NUMPY
if "%choice%"=="5" goto REGULAR_LAUNCHER
if "%choice%"=="6" goto REINSTALL
if "%choice%"=="7" goto VIEW_GUIDE
if "%choice%"=="8" goto EXIT

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MENU

:SAFE_LAUNCHER
cls
echo ============================================================
echo   Running Safe Launcher...
echo ============================================================
echo.
python run_trajectory_gui_safe.py
echo.
echo ============================================================
pause
goto MENU

:NUMPY_DIAG
cls
echo ============================================================
echo   Running NumPy Diagnostics...
echo ============================================================
echo.
python diagnose_numpy.py
echo.
echo ============================================================
pause
goto MENU

:FULL_DIAG
cls
echo ============================================================
echo   Running Full GUI Diagnostics...
echo ============================================================
echo.
python diagnose_gui_startup.py
echo.
echo ============================================================
pause
goto MENU

:TEST_NUMPY
cls
echo ============================================================
echo   Testing NumPy in Python...
echo ============================================================
echo.
echo Type: import numpy
echo Then: print(numpy.__version__)
echo Then: quit() to exit
echo.
echo ============================================================
python
echo.
echo ============================================================
pause
goto MENU

:REGULAR_LAUNCHER
cls
echo ============================================================
echo   Running Regular Launcher...
echo ============================================================
echo.
python run_trajectory_gui.py
echo.
echo ============================================================
pause
goto MENU

:REINSTALL
cls
echo ============================================================
echo   Reinstalling NumPy...
echo ============================================================
echo.
echo Step 1: Uninstalling NumPy...
pip uninstall -y numpy
echo.
echo Step 2: Clearing cache...
pip cache purge
echo.
echo Step 3: Reinstalling NumPy...
pip install numpy
echo.
echo ============================================================
echo   NumPy reinstalled!
echo.
echo   Now try option 1 (Safe Launcher) to test if it works.
echo ============================================================
pause
goto MENU

:VIEW_GUIDE
cls
echo ============================================================
echo   Quick Fix Guide
echo ============================================================
echo.
type QUICK_FIX_SILENT_EXIT.md
echo.
echo ============================================================
echo   For full guide, open: FIX_SILENT_EXIT.md
echo   For overview, open: START_HERE_SILENT_EXIT_FIX.md
echo ============================================================
pause
goto MENU

:EXIT
cls
echo ============================================================
echo   Thank you for using the diagnostic tool!
echo.
echo   Quick tips:
echo   - Always try the Safe Launcher first (Option 1)
echo   - On Windows, install Visual C++ Redistributables
echo   - Use conda install for NumPy on Windows
echo.
echo   Documentation:
echo   - START_HERE_SILENT_EXIT_FIX.md
echo   - QUICK_FIX_SILENT_EXIT.md
echo   - FIX_SILENT_EXIT.md
echo.
echo ============================================================
exit /b 0

@echo off
cls
echo.
echo ========================================
echo    MATPLOTLIB DLL ERROR HELP
echo ========================================
echo.
echo You're seeing this error:
echo   ImportError: DLL load failed while importing _c_internal_utils
echo.
echo ========================================
echo    QUICK FIX OPTIONS
echo ========================================
echo.
echo [1] RUN AUTOMATIC FIX (Recommended)
echo     - Fixes the issue automatically
echo     - Takes 2-3 minutes
echo.
echo [2] VIEW QUICK INSTRUCTIONS
echo     - See simple 3-step guide
echo.
echo [3] VIEW DETAILED GUIDE
echo     - Complete troubleshooting documentation
echo.
echo [4] INSTALL VC++ REDISTRIBUTABLES
echo     - Opens download page in browser
echo     - Required if automatic fix doesn't work
echo.
echo [Q] Quit
echo.
echo ========================================
echo.
set /p choice="Enter your choice (1-4 or Q): "

if /i "%choice%"=="1" goto runfix
if /i "%choice%"=="2" goto quickguide
if /i "%choice%"=="3" goto detailedguide
if /i "%choice%"=="4" goto vcredist
if /i "%choice%"=="q" goto end

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto start

:runfix
cls
echo ========================================
echo   RUNNING AUTOMATIC FIX
echo ========================================
echo.
echo Please wait...
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please ensure you're in the correct directory:
    echo   D:\Zoppler Projects\AiMissionPlanner
    echo.
    echo And that your virtual environment folder is named "venv"
    echo.
    pause
    goto end
)

REM Activate venv and run fix
call venv\Scripts\activate.bat
call fix_matplotlib_dll_error.bat
goto end

:quickguide
cls
type FIX_MATPLOTLIB_NOW.txt
echo.
echo.
echo Press any key to return to menu...
pause >nul
cls
goto start

:detailedguide
cls
echo Opening detailed guide...
echo.
echo File: MATPLOTLIB_DLL_FIX.md
echo.
echo Opening in notepad...
start notepad MATPLOTLIB_DLL_FIX.md
timeout /t 2 >nul
goto end

:vcredist
cls
echo ========================================
echo   OPENING VC++ REDISTRIBUTABLES
echo ========================================
echo.
echo Opening download page in your browser...
echo.
echo IMPORTANT:
echo 1. Download and install the file
echo 2. RESTART YOUR COMPUTER (required!)
echo 3. Run this help menu again and choose option 1
echo.
start https://aka.ms/vs/17/release/vc_redist.x64.exe
timeout /t 3 >nul
goto end

:end
echo.
echo Press any key to exit...
pause >nul

@echo off
REM ════════════════════════════════════════════════════════════════
REM  WINDOWS BUILD FIX - Automatic Solution
REM ════════════════════════════════════════════════════════════════

color 0A
cls

echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo             WINDOWS BUILD FIX - AUTOMATIC SOLUTION
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo  Problem: Cannot find .exe files after running build.bat
echo  Cause:   Build folder contains Linux executables
echo  Solution: Clean and rebuild from scratch
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo  This script will:
echo    1. Delete the build folder (with confirmation)
echo    2. Download ONNX Runtime if needed
echo    3. Build your project properly for Windows
echo    4. Verify that .exe files are created
echo.
echo ════════════════════════════════════════════════════════════════
echo.

pause

echo.
echo Starting clean and build process...
echo.

call clean_and_build.bat

echo.
echo ════════════════════════════════════════════════════════════════
echo  Done! Check the output above for any errors.
echo ════════════════════════════════════════════════════════════════
echo.
pause

@echo off
REM Quick script to clean and rebuild from scratch

echo ==========================================
echo Clean and Build Script
echo ==========================================
echo.
echo This will:
echo 1. Delete the entire build folder
echo 2. Run a fresh build
echo.
echo WARNING: This will delete all files in the build folder!
echo.

set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Cancelled.
    exit /b 0
)

echo.
echo Cleaning build folder...
if exist "build" (
    rmdir /s /q build
    echo Build folder deleted.
) else (
    echo Build folder doesn't exist (nothing to clean).
)

echo.
echo Starting fresh build...
echo.

call build.bat

echo.
echo Done!

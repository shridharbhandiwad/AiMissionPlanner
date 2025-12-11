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
    REM Use multiple methods to ensure clean deletion
    echo Attempting to remove build folder...
    
    REM Method 1: Try standard rmdir
    rmdir /s /q build 2>nul
    
    REM Method 2: If that fails, try rd
    if exist "build" rd /s /q build 2>nul
    
    REM Method 3: If still exists, try removing contents first
    if exist "build" (
        del /f /s /q build\* 2>nul
        rmdir /s /q build 2>nul
    )
    
    if exist "build" (
        echo WARNING: Could not fully delete build folder.
        echo Please manually delete it or run: rmdir /s /q build
        echo.
        pause
        exit /b 1
    )
    
    echo Build folder deleted successfully.
) else (
    echo Build folder doesn't exist - nothing to clean.
)

echo.
echo Starting fresh build...
echo.

call build.bat

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Build failed! Check errors above.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Clean and Build Complete!
echo ==========================================
pause

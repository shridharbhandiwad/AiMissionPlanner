@echo off
REM ========================================================================
REM WINDOWS BUILD FIX - AUTOMATIC SOLUTION
REM ========================================================================
REM
REM Problem: Cannot find .exe files after running build.bat
REM Cause:   Build folder contains Linux executables
REM Solution: Clean and rebuild from scratch
REM
REM ========================================================================

echo.
echo ========================================================================
echo WINDOWS BUILD FIX - AUTOMATIC SOLUTION
echo ========================================================================
echo.
echo  Problem: Cannot find .exe files after running build.bat
echo  Cause:   Build folder contains Linux executables
echo  Solution: Clean and rebuild from scratch
echo.
echo ========================================================================
echo.
echo  This script will:
echo    1. Delete the build folder (with confirmation)
echo    2. Download ONNX Runtime if needed
echo    3. Build your project properly for Windows
echo    4. Verify that .exe files are created
echo.
echo ========================================================================
echo.

pause

echo Starting clean and build process...
echo.

REM Step 1: Check if build folder exists with Linux artifacts
if exist "build\trajectory_app" (
    if not exist "build\trajectory_app.exe" (
        echo [DETECTED] Linux build artifacts in build folder
        echo [ACTION] Removing build folder...
        echo.
    )
)

REM Step 2: Force clean using multiple methods
if exist "build" (
    echo Removing old build folder...
    echo.
    
    REM Method 1: Try to delete contents first
    if exist "build\*" (
        del /f /s /q "build\*" >nul 2>&1
    )
    
    REM Method 2: Remove subdirectories
    for /d %%d in (build\*) do (
        rmdir /s /q "%%d" >nul 2>&1
    )
    
    REM Method 3: Try PowerShell if available
    where powershell >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        powershell -Command "if (Test-Path 'build') { Remove-Item -Path 'build' -Recurse -Force -ErrorAction SilentlyContinue }" >nul 2>&1
    )
    
    REM Method 4: Standard rmdir
    if exist "build" (
        rmdir /s /q build >nul 2>&1
    )
    
    REM Give it a moment
    timeout /t 1 /nobreak >nul 2>&1
    
    REM Final check
    if exist "build" (
        echo WARNING: Could not fully remove build folder.
        echo Some files may be locked. Trying one more time...
        echo.
        timeout /t 2 /nobreak >nul 2>&1
        rmdir /s /q build >nul 2>&1
    )
    
    if exist "build" (
        echo.
        echo ERROR: Could not remove build folder automatically.
        echo Please:
        echo   1. Close any programs that might have files open in build folder
        echo   2. Try running this script as Administrator
        echo   3. Or manually delete: rmdir /s /q build
        echo.
        pause
        exit /b 1
    )
    
    echo [SUCCESS] Build folder removed successfully.
    echo.
)

REM Step 3: Run fresh build
echo ========================================================================
echo Running fresh build for Windows...
echo ========================================================================
echo.

call build.bat

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================================================
    echo BUILD FAILED!
    echo ========================================================================
    echo.
    echo Please check the error messages above.
    echo.
    echo Common issues:
    echo   1. CMake not installed: Download from https://cmake.org/download/
    echo   2. MinGW not installed: Download from https://www.mingw-w64.org/
    echo   3. Tools not in PATH: Add CMake and MinGW bin folders to PATH
    echo.
    pause
    exit /b 1
)

REM Step 4: Verify executables were created
echo.
echo ========================================================================
echo Verifying Windows executables...
echo ========================================================================
echo.

cd build
set found_exe=0

if exist "trajectory_app.exe" (
    echo [OK] trajectory_app.exe found
    set found_exe=1
) else (
    echo [ERROR] trajectory_app.exe NOT found
)

if exist "trajectory_demo.exe" (
    echo [OK] trajectory_demo.exe found
    set found_exe=1
) else (
    echo [ERROR] trajectory_demo.exe NOT found
)

echo.

if %found_exe%==1 (
    echo ========================================================================
    echo SUCCESS! Windows executables created.
    echo ========================================================================
    echo.
    echo Executables in build folder:
    dir /B *.exe
    echo.
    echo To run:
    echo   cd build
    echo   trajectory_app.exe --help
    echo   trajectory_demo.exe
    echo.
) else (
    echo ========================================================================
    echo WARNING: No .exe files found!
    echo ========================================================================
    echo.
    echo The build may have succeeded but no executables were created.
    echo This could mean:
    echo   1. CMake used wrong generator (should be MinGW Makefiles)
    echo   2. Build succeeded but executables in different location
    echo   3. Linker issues
    echo.
    echo Check the build output above for clues.
    echo.
)

cd ..
echo.
pause

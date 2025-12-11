@echo off
REM Force clean build folder - use this if clean_and_build.bat fails

echo ==========================================
echo FORCE CLEAN - Build Folder
echo ==========================================
echo.
echo This script will forcefully remove the build folder
echo using multiple methods.
echo.
echo WARNING: This will delete ALL files in the build folder!
echo.

set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Cancelled.
    exit /b 0
)

echo.
echo Attempting to clean build folder...
echo.

if not exist "build" (
    echo Build folder does not exist - nothing to clean.
    echo.
    pause
    exit /b 0
)

REM Method 1: Try standard rmdir
echo Method 1: Using rmdir /s /q...
rmdir /s /q build 2>nul
if not exist "build" (
    echo Success! Build folder removed.
    goto :success
)

REM Method 2: Try rd
echo Method 2: Using rd /s /q...
rd /s /q build 2>nul
if not exist "build" (
    echo Success! Build folder removed.
    goto :success
)

REM Method 3: Delete contents first
echo Method 3: Deleting contents first...
del /f /s /q build\* 2>nul
for /d %%p in (build\*) do rmdir /s /q "%%p" 2>nul
rmdir /s /q build 2>nul
if not exist "build" (
    echo Success! Build folder removed.
    goto :success
)

REM Method 4: Try using PowerShell
echo Method 4: Using PowerShell...
powershell -Command "if (Test-Path 'build') { Remove-Item -Path 'build' -Recurse -Force }" 2>nul
if not exist "build" (
    echo Success! Build folder removed.
    goto :success
)

REM If all methods fail
echo.
echo ==========================================
echo ERROR: Could not remove build folder!
echo ==========================================
echo.
echo The build folder may be locked by another process.
echo.
echo Please try one of the following:
echo   1. Close any programs that might be using files in build folder
echo   2. Restart your command prompt as Administrator
echo   3. Manually delete the build folder in File Explorer
echo   4. Run in Git Bash: rm -rf build
echo.
pause
exit /b 1

:success
echo.
echo ==========================================
echo Build folder cleaned successfully!
echo ==========================================
echo.
echo You can now run: build.bat
echo.
pause
exit /b 0

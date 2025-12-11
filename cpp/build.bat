@echo off
REM Build script for Trajectory Generator C++ application (Windows)

echo ==========================================
echo Building Trajectory Generator (Windows)
echo ==========================================
echo.

REM Check if build directory exists and contains Linux artifacts
if exist "build\trajectory_app" (
    if not exist "build\trajectory_app.exe" (
        echo WARNING: Found Linux build artifacts in build folder!
        echo This happens when you switch from Linux to Windows.
        echo.
        echo You need to clean the build folder first.
        echo Run one of these commands:
        echo   rmdir /s /q build
        echo   rm -rf build  (in Git Bash)
        echo.
        echo Then run build.bat again.
        echo.
        pause
        exit /b 1
    )
)

REM Check for ONNX Runtime
if "%ONNXRUNTIME_ROOT_DIR%"=="" (
    echo Warning: ONNXRUNTIME_ROOT_DIR not set
    echo Attempting to download ONNX Runtime for Windows...
    echo.
    
    REM Create libs directory
    if not exist "..\libs" mkdir "..\libs"
    cd ..\libs
    
    REM Download ONNX Runtime if not present
    if not exist "onnxruntime-win-x64-1.16.3" (
        echo Downloading ONNX Runtime 1.16.3 for Windows...
        curl -L -o onnxruntime-win-x64-1.16.3.zip https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-win-x64-1.16.3.zip
        if %ERRORLEVEL% NEQ 0 (
            echo Failed to download ONNX Runtime!
            cd ..\cpp
            exit /b 1
        )
        tar -xf onnxruntime-win-x64-1.16.3.zip
        del onnxruntime-win-x64-1.16.3.zip
        echo ONNX Runtime downloaded successfully!
    ) else (
        echo ONNX Runtime already present
    )
    echo.
    
    cd onnxruntime-win-x64-1.16.3
    set ONNXRUNTIME_ROOT_DIR=%CD%
    cd ..\..\cpp
) else (
    echo Using ONNX Runtime from: %ONNXRUNTIME_ROOT_DIR%
)

REM Clean old CMake cache if it exists
if exist "build\CMakeCache.txt" (
    echo Cleaning old CMake cache...
    del /F /Q build\CMakeCache.txt 2>nul
    rmdir /S /Q build\CMakeFiles 2>nul
)

REM Create build directory
if not exist "build" mkdir build
cd build

REM Run CMake
echo.
echo ==========================================
echo Step 1: Running CMake Configuration...
echo ==========================================
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release -DONNXRUNTIME_ROOT_DIR=%ONNXRUNTIME_ROOT_DIR% ..

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ==========================================
    echo ERROR: CMake configuration failed!
    echo ==========================================
    echo.
    echo Please ensure you have:
    echo   1. CMake installed (version 3.15 or higher)
    echo   2. MinGW or Visual Studio installed
    echo   3. CMake and MinGW/MSVC in your PATH
    echo.
    echo To check: cmake --version
    echo           mingw32-make --version
    echo.
    cd ..
    exit /b 1
)

REM Build
echo.
echo ==========================================
echo Step 2: Building executables...
echo ==========================================
cmake --build . --config Release

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ==========================================
    echo ERROR: Build failed!
    echo ==========================================
    echo.
    echo Check the error messages above.
    echo Common issues:
    echo   - Missing MinGW: Install from https://www.mingw-w64.org/
    echo   - Compiler not in PATH: Add MinGW bin folder to PATH
    echo   - Missing dependencies: Check CMakeLists.txt
    echo.
    cd ..
    exit /b 1
)

REM Check if executables were created
echo.
echo ==========================================
echo Step 3: Verifying build...
echo ==========================================
if exist "trajectory_app.exe" (
    echo [OK] trajectory_app.exe created successfully
) else (
    echo [ERROR] trajectory_app.exe not found!
)

if exist "trajectory_demo.exe" (
    echo [OK] trajectory_demo.exe created successfully
) else (
    echo [ERROR] trajectory_demo.exe not found!
)

echo.
echo ==========================================
echo Build complete!
echo ==========================================
echo.
echo Executables in build folder:
dir /B *.exe 2>nul
echo.
echo To run:
echo   trajectory_app.exe --help
echo   trajectory_demo.exe
echo.
echo To run the main application with the model:
echo   trajectory_app.exe --model ..\models\trajectory_model.onnx --demo
echo.

cd ..

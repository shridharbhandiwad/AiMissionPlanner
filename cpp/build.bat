@echo off
REM Build script for Trajectory Generator C++ application (Windows)

echo ==========================================
echo Building Trajectory Generator (Windows)
echo ==========================================

REM Check for ONNX Runtime
if "%ONNXRUNTIME_ROOT_DIR%"=="" (
    echo Warning: ONNXRUNTIME_ROOT_DIR not set
    echo Attempting to download ONNX Runtime for Windows...
    
    REM Create libs directory
    if not exist "..\libs" mkdir "..\libs"
    cd ..\libs
    
    REM Download ONNX Runtime if not present
    if not exist "onnxruntime-win-x64-1.16.3" (
        echo Downloading ONNX Runtime 1.16.3 for Windows...
        curl -L -o onnxruntime-win-x64-1.16.3.zip https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-win-x64-1.16.3.zip
        tar -xf onnxruntime-win-x64-1.16.3.zip
        del onnxruntime-win-x64-1.16.3.zip
        echo ONNX Runtime downloaded
    )
    
    cd onnxruntime-win-x64-1.16.3
    set ONNXRUNTIME_ROOT_DIR=%CD%
    cd ..\..\cpp
) else (
    echo Using ONNX Runtime from: %ONNXRUNTIME_ROOT_DIR%
)

REM Clean old CMake cache if it exists
if exist "build\CMakeCache.txt" (
    echo Cleaning old CMake cache...
    del /F /Q build\CMakeCache.txt
    rmdir /S /Q build\CMakeFiles 2>nul
)

REM Create build directory
if not exist "build" mkdir build
cd build

REM Run CMake
echo.
echo Running CMake...
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release -DONNXRUNTIME_ROOT_DIR=%ONNXRUNTIME_ROOT_DIR% ..

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo CMake configuration failed!
    echo.
    echo Please ensure you have:
    echo   1. CMake installed (version 3.15 or higher)
    echo   2. MinGW or Visual Studio installed
    echo   3. CMake and MinGW/MSVC in your PATH
    echo.
    cd ..
    exit /b 1
)

REM Build
echo.
echo Building...
cmake --build . --config Release

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Build failed!
    cd ..
    exit /b 1
)

echo.
echo ==========================================
echo Build complete!
echo ==========================================
echo.
echo Executables:
echo   - trajectory_app.exe  (Main application)
echo   - trajectory_demo.exe (Demo/test application)
echo.
echo To run:
echo   cd build
echo   trajectory_app.exe --help
echo.

cd ..

@echo off
REM Build script for Trajectory Generator C++ application (Windows)

echo ==========================================
echo Building Trajectory Generator (Windows)
echo ==========================================
echo.

REM Check for required tools
echo Checking for required build tools...
echo.

where cmake >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] CMake not found in PATH!
    echo.
    echo Please install CMake from: https://cmake.org/download/
    echo Make sure to add CMake to your system PATH during installation.
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('cmake --version') do (
        echo [OK] %%i
        goto :cmake_found
    )
    :cmake_found
)

where mingw32-make >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] MinGW Make found
    set MAKE_CMD=mingw32-make
) else (
    where make >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Make found
        set MAKE_CMD=make
    ) else (
        echo [WARNING] Neither mingw32-make nor make found in PATH!
        echo.
        echo Please install MinGW-w64 from: https://www.mingw-w64.org/
        echo Or install via MSYS2: https://www.msys2.org/
        echo Make sure to add MinGW's bin folder to your system PATH.
        echo.
        echo Example PATH entry: C:\msys64\mingw64\bin
        echo.
        pause
        exit /b 1
    )
)

where g++ >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] G++ compiler found
) else (
    echo [WARNING] G++ compiler not found in PATH!
    echo This is needed for building C++ code.
    echo.
)

echo.
echo All required tools found. Continuing with build...
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

REM Store the cpp directory path
set CPP_DIR=%~dp0
set CPP_DIR=%CPP_DIR:~0,-1%

REM Check for ONNX Runtime
if "%ONNXRUNTIME_ROOT_DIR%"=="" (
    echo Warning: ONNXRUNTIME_ROOT_DIR not set
    echo Attempting to use local copy or download ONNX Runtime for Windows...
    echo.
    
    REM Check if ONNX Runtime exists in cpp folder (user may have copied it)
    if exist "%CPP_DIR%\include\onnxruntime_cxx_api.h" (
        set "ONNXRUNTIME_ROOT_DIR=%CPP_DIR%"
        echo Found ONNX Runtime in cpp folder!
        goto :onnx_found
    )
    
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
    set "ONNXRUNTIME_ROOT_DIR=%CD%"
    cd "%CPP_DIR%"
)

:onnx_found
echo.
echo Using ONNX Runtime from: %ONNXRUNTIME_ROOT_DIR%
echo.

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
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release -DONNXRUNTIME_ROOT_DIR="%ONNXRUNTIME_ROOT_DIR%" ..

REM Check if CMakeLists.txt was processed (more reliable than ERRORLEVEL)
if not exist "CMakeCache.txt" (
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

echo CMake configuration completed successfully!
echo.

REM Build
echo.
echo ==========================================
echo Step 2: Building executables...
echo ==========================================
echo.

REM Try cmake --build first
cmake --build . --config Release
set BUILD_RESULT=%ERRORLEVEL%

REM If cmake --build fails, try mingw32-make directly
if %BUILD_RESULT% NEQ 0 (
    echo.
    echo CMake build command failed, trying mingw32-make directly...
    echo.
    mingw32-make
    set BUILD_RESULT=%ERRORLEVEL%
)

if %BUILD_RESULT% NEQ 0 (
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
    echo   - ONNX Runtime library not found
    echo.
    echo Attempting to show build log...
    if exist "CMakeFiles\CMakeError.log" (
        echo.
        echo === CMake Error Log ===
        type CMakeFiles\CMakeError.log
    )
    echo.
    cd ..
    exit /b 1
)

echo.
echo Build step completed successfully!

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

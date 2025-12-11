@echo off
REM Diagnostic script to check Windows build environment

echo ========================================================================
echo Windows Build Environment Diagnostic
echo ========================================================================
echo.
echo This script checks if you have all the required tools to build the
echo Trajectory Generator C++ application on Windows.
echo.
echo ========================================================================
echo.

set ALL_OK=1

REM Check CMake
echo Checking for CMake...
where cmake >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] CMake NOT FOUND
    echo     Download from: https://cmake.org/download/
    echo     Make sure to add CMake to PATH during installation
    echo.
    set ALL_OK=0
) else (
    cmake --version | findstr /C:"cmake version"
    echo [OK] CMake found
    echo.
)

REM Check MinGW Make
echo Checking for Make...
where mingw32-make >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where make >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [X] Make NOT FOUND
        echo     Install MinGW-w64 or MSYS2
        echo     MinGW-w64: https://www.mingw-w64.org/
        echo     MSYS2: https://www.msys2.org/
        echo.
        set ALL_OK=0
    ) else (
        make --version | findstr /C:"Make"
        echo [OK] Make found
        echo.
    )
) else (
    mingw32-make --version | findstr /C:"Make"
    echo [OK] MinGW Make found
    echo.
)

REM Check G++
echo Checking for G++ compiler...
where g++ >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] G++ compiler NOT FOUND
    echo     Install MinGW-w64 with G++
    echo     Or install via MSYS2: pacman -S mingw-w64-x86_64-gcc
    echo.
    set ALL_OK=0
) else (
    g++ --version | findstr /C:"g++"
    echo [OK] G++ compiler found
    echo.
)

REM Check for ONNX Runtime
echo Checking for ONNX Runtime...
if defined ONNXRUNTIME_ROOT_DIR (
    if exist "%ONNXRUNTIME_ROOT_DIR%\include\onnxruntime_cxx_api.h" (
        echo [OK] ONNX Runtime found at: %ONNXRUNTIME_ROOT_DIR%
        echo.
    ) else (
        echo [!] ONNXRUNTIME_ROOT_DIR is set but doesn't contain ONNX Runtime
        echo     Current value: %ONNXRUNTIME_ROOT_DIR%
        echo.
    )
) else (
    if exist "include\onnxruntime_cxx_api.h" (
        echo [OK] ONNX Runtime found in cpp folder
        echo.
    ) else (
        if exist "..\libs\onnxruntime-win-x64-1.16.3\include\onnxruntime_cxx_api.h" (
            echo [OK] ONNX Runtime found in libs folder
            echo.
        ) else (
            echo [!] ONNX Runtime NOT FOUND
            echo     The build script will attempt to download it automatically
            echo     Or download manually from: https://github.com/microsoft/onnxruntime/releases
            echo.
        )
    )
)

REM Check PATH
echo Checking PATH for build tools...
echo Current PATH entries with build tools:
echo.
echo %PATH% | findstr /I "cmake" >nul && echo   - CMake in PATH
echo %PATH% | findstr /I "mingw" >nul && echo   - MinGW in PATH
echo %PATH% | findstr /I "msys" >nul && echo   - MSYS in PATH
echo.

REM Final verdict
echo ========================================================================
if %ALL_OK%==1 (
    echo [SUCCESS] Your environment is ready to build!
    echo.
    echo Next steps:
    echo   1. Run: build.bat
    echo   2. Or run: FIX_WINDOWS_BUILD.bat (if you need to clean first)
    echo.
) else (
    echo [FAILED] Some required tools are missing!
    echo.
    echo Please install the missing tools listed above.
    echo.
    echo Quick setup guide:
    echo   1. Install CMake: https://cmake.org/download/
    echo      - Check "Add CMake to PATH" during installation
    echo.
    echo   2. Install MSYS2: https://www.msys2.org/
    echo      - After installation, run: pacman -S mingw-w64-x86_64-gcc
    echo      - Add to PATH: C:\msys64\mingw64\bin
    echo.
    echo   3. Restart your terminal/cmd after making PATH changes
    echo.
)
echo ========================================================================
echo.

pause

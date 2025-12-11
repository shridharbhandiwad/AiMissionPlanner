# Windows Build Guide

## Error: CMake Cache Mismatch

If you see an error like:
```
CMake Error: The current CMakeCache.txt directory D:/... is different than the directory /workspace/cpp/build where CMakeCache.txt was created.
```

This happens when the build directory was created in a different environment (e.g., Linux/WSL) and you're now trying to build on Windows.

## Quick Fix

### Option 1: Clean and Rebuild (Recommended)

1. **Delete the build directory:**
   ```bash
   # In Git Bash / PowerShell / CMD
   cd "D:/Zoppler Projects/AiMissionPlanner/cpp"
   rm -rf build    # Git Bash
   # OR
   rmdir /s /q build    # CMD
   # OR
   Remove-Item -Recurse -Force build    # PowerShell
   ```

2. **Use the Windows build script:**
   
   **PowerShell (Recommended):**
   ```powershell
   cd "D:/Zoppler Projects/AiMissionPlanner/cpp"
   .\build.ps1
   ```
   
   **OR Git Bash / CMD:**
   ```cmd
   cd "D:/Zoppler Projects/AiMissionPlanner/cpp"
   build.bat
   ```

### Option 2: Manual CMake Build

If you prefer to run CMake manually:

```powershell
# Clean build directory
cd "D:/Zoppler Projects/AiMissionPlanner/cpp"
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path build

# Configure
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DONNXRUNTIME_ROOT_DIR="D:/Zoppler Projects/AiMissionPlanner/libs/onnxruntime-win-x64-1.16.3" ..

# Build
cmake --build . --config Release
```

## Prerequisites

Before building on Windows, ensure you have:

1. **CMake** (version 3.15 or higher)
   - Download from: https://cmake.org/download/
   - Make sure to add CMake to your PATH during installation

2. **C++ Compiler** (one of the following):
   - **Visual Studio 2019/2022** with C++ Desktop Development workload (Recommended)
   - **MinGW-w64** (for GCC on Windows)
   - **LLVM/Clang** for Windows

3. **ONNX Runtime for Windows**
   - The build scripts will automatically download this
   - OR manually download from: https://github.com/microsoft/onnxruntime/releases

## Build Script Features

The Windows build scripts (`build.bat` and `build.ps1`) will:

1. ✓ Automatically download ONNX Runtime for Windows if needed
2. ✓ Clean old CMake cache to prevent conflicts
3. ✓ Configure CMake with proper Windows settings
4. ✓ Build the project
5. ✓ Provide helpful error messages

## Troubleshooting

### Error: "cmake is not recognized"
- Install CMake and add it to your PATH
- Restart your terminal after installation

### Error: "No CMAKE_CXX_COMPILER could be found"
- Install Visual Studio with C++ support, MinGW, or another C++ compiler
- Make sure the compiler is in your PATH

### Error: "Cannot find ONNX Runtime"
- Let the build script download it automatically, OR
- Set the ONNXRUNTIME_ROOT_DIR environment variable:
  ```powershell
  $env:ONNXRUNTIME_ROOT_DIR="D:/Zoppler Projects/AiMissionPlanner/libs/onnxruntime-win-x64-1.16.3"
  ```

## Important Notes

- **Do NOT use `build.sh` on Windows** - it's designed for Linux and downloads the Linux version of ONNX Runtime
- Use **`build.ps1`** (PowerShell) or **`build.bat`** (CMD/Git Bash) instead
- If switching between Windows and WSL/Linux, always clean the build directory first

## WSL (Windows Subsystem for Linux)

If you want to build on Linux within Windows:

1. Install WSL2
2. Open a WSL terminal
3. Use the Linux build script:
   ```bash
   cd /mnt/d/Zoppler\ Projects/AiMissionPlanner/cpp
   ./build.sh
   ```

Note: The executables built in WSL won't run in native Windows (and vice versa).

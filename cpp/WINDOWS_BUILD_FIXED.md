# Windows Build Issues - FIXED! 🎉

## What Was Fixed

The Windows build process has been improved to handle common issues and provide better error messages.

### Issues Addressed

1. **CMake warnings causing build failure** - The script now checks for actual build artifacts instead of relying on error codes
2. **Paths with spaces** - All paths are properly quoted to handle spaces in directory names
3. **Missing ONNX Runtime detection** - Better detection of ONNX Runtime in multiple locations
4. **Build tool verification** - Script now checks for required tools before attempting to build
5. **Better error messages** - Clear indication of what's wrong and how to fix it

## Quick Start

### Option 1: Check Your Environment First (Recommended)

```batch
check_build_environment.bat
```

This will verify you have all required tools installed. If anything is missing, it will tell you what to install.

### Option 2: Clean Build (If Previous Build Failed)

```batch
FIX_WINDOWS_BUILD.bat
```

This will:
1. Remove the old build folder
2. Check for required tools
3. Download ONNX Runtime if needed
4. Build the project
5. Verify .exe files were created

### Option 3: Normal Build

```batch
build.bat
```

Use this if your environment is already set up and you just want to rebuild.

## Required Tools

### 1. CMake (Version 3.15 or higher)

**Download:** https://cmake.org/download/

**Installation:**
- Download the Windows installer (cmake-X.XX.X-windows-x86_64.msi)
- Run the installer
- ✅ **IMPORTANT:** Check "Add CMake to the system PATH for all users" during installation

**Verify installation:**
```batch
cmake --version
```

### 2. MinGW-w64 (GCC compiler for Windows)

**Option A: Install via MSYS2 (Recommended)**

1. Download and install MSYS2: https://www.msys2.org/
2. Open MSYS2 terminal and run:
   ```bash
   pacman -S mingw-w64-x86_64-gcc
   pacman -S mingw-w64-x86_64-cmake
   pacman -S mingw-w64-x86_64-make
   ```
3. Add MinGW to your PATH:
   - Open System Environment Variables
   - Add to PATH: `C:\msys64\mingw64\bin`
   - Restart your terminal

**Option B: Install MinGW-w64 directly**

1. Download from: https://www.mingw-w64.org/
2. Install to `C:\mingw-w64\`
3. Add to PATH: `C:\mingw-w64\mingw64\bin`

**Verify installation:**
```batch
g++ --version
mingw32-make --version
```

### 3. ONNX Runtime

**Automatic:** The build script will download it automatically if not found.

**Manual download:**
1. Download from: https://github.com/microsoft/onnxruntime/releases
2. Get: `onnxruntime-win-x64-1.16.3.zip`
3. Extract to: `AiMissionPlanner\libs\onnxruntime-win-x64-1.16.3\`

## Troubleshooting

### "CMake not found"

**Problem:** CMake is not installed or not in PATH

**Solution:**
1. Install CMake from https://cmake.org/download/
2. Make sure to check "Add to PATH" during installation
3. Restart your terminal/cmd prompt

### "mingw32-make not found" or "g++ not found"

**Problem:** MinGW is not installed or not in PATH

**Solution:**
1. Install MSYS2 from https://www.msys2.org/
2. Run: `pacman -S mingw-w64-x86_64-gcc mingw-w64-x86_64-make`
3. Add `C:\msys64\mingw64\bin` to your PATH
4. Restart your terminal

### "ONNX Runtime not found"

**Problem:** ONNX Runtime is not available

**Solution:**
- Let the build script download it automatically, OR
- Download manually and extract to `libs\onnxruntime-win-x64-1.16.3\`

### "No .exe files created after build"

**Problem:** Build folder contains Linux artifacts

**Solution:**
```batch
FIX_WINDOWS_BUILD.bat
```

This will clean everything and rebuild from scratch.

### Build succeeds but executables don't run

**Problem:** Missing DLL files

**Solution:**
Copy these from ONNX Runtime to your build folder:
- `onnxruntime.dll`
- `onnxruntime_providers_shared.dll`

Or add ONNX Runtime's `lib` folder to your PATH.

## What the Scripts Do

### build.bat
1. ✅ Checks for required tools (CMake, Make, G++)
2. ✅ Detects or downloads ONNX Runtime
3. ✅ Runs CMake configuration with MinGW Makefiles
4. ✅ Builds the project
5. ✅ Verifies .exe files were created
6. ✅ Lists all executables

### FIX_WINDOWS_BUILD.bat
1. ✅ Removes old build folder completely
2. ✅ Calls build.bat
3. ✅ Verifies Windows executables were created
4. ✅ Provides helpful error messages if build fails

### check_build_environment.bat
1. ✅ Checks for CMake installation
2. ✅ Checks for Make installation
3. ✅ Checks for G++ compiler
4. ✅ Checks for ONNX Runtime
5. ✅ Reports what's missing with download links

## Expected Output

After a successful build, you should see:

```
build/
  ├── trajectory_app.exe       ← Main application
  ├── trajectory_demo.exe      ← Demo/example
  ├── libtrajectory_inference.a
  ├── libtrajectory_metrics.a
  └── libtrajectory_plotter.a
```

## Running the Application

```batch
cd build
trajectory_app.exe --help
trajectory_demo.exe
```

Or with the ONNX model:
```batch
trajectory_app.exe --model ..\models\trajectory_generator.onnx --demo
```

## Changes Made to Fix Issues

### build.bat
- Added tool verification before building
- Fixed path handling for spaces in directory names
- Improved CMake success detection (checks for CMakeCache.txt)
- Added fallback to direct mingw32-make if cmake --build fails
- Better error messages with specific solutions
- Quotes around ONNXRUNTIME_ROOT_DIR path

### FIX_WINDOWS_BUILD.bat
- More robust build folder deletion (multiple methods)
- Added timeouts to ensure files are released
- Better error handling for locked files
- Clearer progress messages

### New: check_build_environment.bat
- Comprehensive environment check
- Helpful guidance on what to install
- Quick way to verify setup without building

## Getting Help

If you're still having issues:

1. Run `check_build_environment.bat` to see what's missing
2. Check the error messages - they now include specific solutions
3. Make sure all tools are in your PATH
4. Restart your terminal after changing PATH
5. Try `FIX_WINDOWS_BUILD.bat` for a clean build

## Next Steps

After building successfully:

1. Test the executables:
   ```batch
   cd build
   trajectory_demo.exe
   ```

2. Run with your model:
   ```batch
   trajectory_app.exe --model ..\models\trajectory_generator.onnx
   ```

3. See the main README.md for more usage examples

---

**Note:** These scripts are designed to be robust and provide clear error messages. If you encounter any issues, the error messages will guide you to the solution.

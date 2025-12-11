# Windows Build Fix Guide

## Problem Summary

**Issue**: After running `build.bat`, no `.exe` files are found in the build folder.

**Root Cause**: The build folder contains Linux executables (files without `.exe` extension) from a previous Linux build. When CMake detects existing build artifacts, it may reuse the Linux configuration instead of creating Windows executables.

**Error Encountered**: `. was unexpected at this time.` - This occurs when the batch script tries to process files with unexpected characters or when the cleanup process fails.

---

## Solution Options

### Option 1: RECOMMENDED - Use FIX_WINDOWS_BUILD.bat

This is the **easiest and most automated solution**:

```batch
cd cpp
FIX_WINDOWS_BUILD.bat
```

This script will:
1. Automatically detect Linux build artifacts
2. Remove the build folder completely
3. Download ONNX Runtime if needed
4. Run a fresh Windows build
5. Verify that `.exe` files are created

---

### Option 2: Use clean_and_build.bat

If you want more control:

```batch
cd cpp
clean_and_build.bat
```

This will:
1. Ask for confirmation before cleaning
2. Remove the build folder using multiple methods
3. Run a fresh build

---

### Option 3: Manual Cleanup

If the automated scripts fail, do this manually:

#### In Command Prompt:
```batch
cd cpp
rmdir /s /q build
build.bat
```

#### In PowerShell:
```powershell
cd cpp
Remove-Item -Path build -Recurse -Force
.\build.bat
```

#### In Git Bash:
```bash
cd cpp
rm -rf build
./build.bat
```

---

## Why This Happens

1. **Cross-Platform Development**: The repository was previously built on Linux
2. **CMake Cache**: CMake caches build configuration in the build folder
3. **Platform Detection**: When switching from Linux to Windows, CMake may detect the existing artifacts and reuse the wrong platform configuration
4. **Executable Names**: Linux executables have no extension (e.g., `trajectory_app`), while Windows executables need `.exe` (e.g., `trajectory_app.exe`)

---

## Verification Steps

After building, verify the executables were created:

```batch
cd cpp\build
dir *.exe
```

You should see:
- `trajectory_app.exe`
- `trajectory_demo.exe`

If you see files without `.exe` extension (like `trajectory_app`), the build used Linux configuration by mistake.

---

## Running the Application

Once built successfully:

```batch
cd cpp\build

REM Show help
trajectory_app.exe --help

REM Run demo
trajectory_demo.exe

REM Run with model
trajectory_app.exe --model ..\..\models\trajectory_generator.onnx --demo
```

---

## Troubleshooting

### Problem: Scripts still fail to clean build folder

**Solution 1**: Run Command Prompt as Administrator
- Right-click Command Prompt → "Run as Administrator"
- Navigate to cpp folder
- Run `FORCE_CLEAN.bat`

**Solution 2**: Use PowerShell directly
```powershell
Remove-Item -Path cpp\build -Recurse -Force
```

**Solution 3**: Manually delete in Windows Explorer
- Open File Explorer
- Navigate to `cpp` folder
- Delete the `build` folder manually
- Run `build.bat`

### Problem: CMake not found

**Error**: `'cmake' is not recognized as an internal or external command`

**Solution**: Install CMake
1. Download from https://cmake.org/download/
2. During installation, select "Add CMake to system PATH"
3. Restart Command Prompt
4. Verify: `cmake --version`

### Problem: MinGW not found

**Error**: `'mingw32-make' is not recognized...`

**Solution**: Install MinGW
1. Download from https://www.mingw-w64.org/
2. Install to `C:\mingw64` (or similar)
3. Add to PATH: `C:\mingw64\bin`
4. Restart Command Prompt
5. Verify: `mingw32-make --version`

### Problem: ONNX Runtime download fails

**Error**: Failed to download ONNX Runtime

**Solution**: Manual download
1. Download from https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-win-x64-1.16.3.zip
2. Extract to `libs\onnxruntime-win-x64-1.16.3`
3. Run `build.bat` again

### Problem: Build succeeds but no .exe files

**Possible Causes**:
1. Wrong CMake generator (should be "MinGW Makefiles")
2. Visual Studio not properly configured
3. Linker issues

**Solution**: Check CMakeLists.txt configuration
```batch
cd cpp\build
cmake -G "MinGW Makefiles" ..
cmake --build .
```

---

## Prevention

To avoid this issue in the future:

1. **Always clean when switching platforms**:
   ```batch
   # When switching from Linux to Windows
   rm -rf cpp/build
   ```

2. **Use platform-specific build folders**:
   - Create `build-windows` for Windows
   - Create `build-linux` for Linux
   - Modify CMakeLists.txt to use separate folders

3. **Add to .gitignore**:
   ```
   cpp/build/
   cpp/build-*/
   ```

---

## Quick Reference

| Task | Command |
|------|---------|
| Automated fix | `FIX_WINDOWS_BUILD.bat` |
| Clean and rebuild | `clean_and_build.bat` |
| Just clean | `FORCE_CLEAN.bat` |
| Just build | `build.bat` |
| Manual clean | `rmdir /s /q build` |
| Run app | `build\trajectory_app.exe --help` |
| Run demo | `build\trajectory_demo.exe` |

---

## Additional Help

If you continue to have issues:

1. Check that you're in the `cpp` folder when running scripts
2. Try running as Administrator
3. Check that antivirus isn't blocking file operations
4. Ensure no programs are using files in the build folder
5. Try rebooting your computer if file locks persist

---

## Summary of New Files Created

- **FIX_WINDOWS_BUILD.bat** - Automated one-click solution
- **clean_and_build.bat** - Updated with better error handling
- **FORCE_CLEAN.bat** - Multiple cleanup methods if standard fails
- **WINDOWS_BUILD_FIX_GUIDE.md** - This guide

Choose **FIX_WINDOWS_BUILD.bat** for the easiest experience!

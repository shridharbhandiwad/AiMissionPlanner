# Solution: Executable Not Found in Build Folder

## Problem Summary

You ran `build.bat` in the `cpp` folder and CMake configured successfully, but you couldn't find the `.exe` files (`trajectory_app.exe` and `trajectory_demo.exe`) in the build folder.

## Root Cause

The `cpp/build` folder contains **Linux executables** (files without `.exe` extension) from a previous Linux build. This remote workspace runs on Linux, so when code is built here, it creates Linux binaries.

When you tried to build on your local Windows machine:
1. CMake configured successfully ✓
2. But the build step either:
   - Skipped compilation because it saw existing binaries
   - Failed silently due to platform conflicts
3. Result: No `.exe` files were created

## The Solution

You need to **clean the build folder** and rebuild from scratch on Windows.

### Quick Fix (Use This!)

I've created automated scripts to make this easy:

**In PowerShell:**
```powershell
cd "D:\Zoppler Projects\AiMissionPlanner\cpp"
.\clean_and_build.ps1
```

**In Command Prompt or Git Bash:**
```cmd
cd "D:\Zoppler Projects\AiMissionPlanner\cpp"
clean_and_build.bat
```

These scripts will:
1. Ask for confirmation
2. Delete the build folder
3. Run a fresh build
4. Verify that `.exe` files are created

### Manual Method

If you prefer to do it manually:

1. **Delete the build folder:**
   ```cmd
   cd "D:\Zoppler Projects\AiMissionPlanner\cpp"
   rmdir /s /q build
   ```

2. **Run the build script:**
   ```cmd
   build.bat
   ```
   OR (recommended)
   ```powershell
   .\build.ps1
   ```

## What I've Fixed

I've improved both `build.bat` and `build.ps1` to handle this issue better:

### New Features:

1. **✓ Automatic Detection**
   - The scripts now detect Linux artifacts before building
   - They'll warn you and stop if they find Linux executables
   - Prevents wasted time on builds that won't work

2. **✓ Clear Progress Messages**
   - Step 1: Running CMake Configuration
   - Step 2: Building executables
   - Step 3: Verifying build

3. **✓ Build Verification**
   - After building, the scripts check if `.exe` files were created
   - Shows `[OK]` or `[ERROR]` for each expected executable
   - Lists all executables in the build folder

4. **✓ Better Error Messages**
   - Clear explanations of what went wrong
   - Suggestions for common issues
   - Links to tools you need to install

### New Files Created:

1. **`clean_and_build.bat`** / **`clean_and_build.ps1`**
   - One-command solution to clean and rebuild

2. **`cpp/FIX_EXECUTABLE_NOT_FOUND.md`**
   - Detailed troubleshooting guide for this specific issue

3. **`cpp/build/README_BUILD_ISSUE.txt`**
   - Quick reference in the build folder itself

4. **Updated `cpp/WINDOWS_BUILD_GUIDE.md`**
   - Added this issue to the common problems section

## Expected Output After Fix

When you run the build script after cleaning, you should see:

```
==========================================
Step 3: Verifying build...
==========================================
[OK] trajectory_app.exe created successfully
[OK] trajectory_demo.exe created successfully

==========================================
Build complete!
==========================================

Executables in build folder:
trajectory_app.exe
trajectory_demo.exe
```

## Running Your Application

After successful build:

```cmd
cd build
trajectory_app.exe --help
trajectory_app.exe --model ..\models\trajectory_model.onnx --demo
```

## Why This Happens

This is a common issue when developing in a remote/cloud environment:

- **Remote Workspace**: Runs on Linux, creates Linux binaries
- **Your Local Machine**: Runs Windows, needs Windows binaries (`.exe`)
- **Mixed Builds**: Build artifacts are platform-specific and incompatible

**Key Rule**: Always clean the build folder when switching between Linux and Windows!

## Troubleshooting

### "cmake is not recognized"
**Solution**: Install CMake and add to PATH
- Download: https://cmake.org/download/
- Check installation: `cmake --version`

### "No CMAKE_CXX_COMPILER could be found"
**Solution**: Install a C++ compiler
- **Option 1**: Visual Studio 2022 (Community Edition is free)
- **Option 2**: MinGW-w64
- Check installation: `gcc --version` or `cl.exe`

### "ONNX Runtime not found"
**Solution**: The script downloads it automatically, but if it fails:
- Check your internet connection
- Download manually from: https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-win-x64-1.16.3.zip
- Extract to: `libs\onnxruntime-win-x64-1.16.3\`

### Build succeeds but still no executables
**Solution**: Run verbose build to see detailed output
```cmd
cd build
cmake --build . --config Release --verbose
```

## Summary

1. **Immediate Action**: Run `clean_and_build.bat` or `clean_and_build.ps1`
2. **Result**: You'll get working `.exe` files in the build folder
3. **Prevention**: Always clean build folder when switching between platforms
4. **Future Builds**: The improved scripts will detect and prevent this issue

## Need More Help?

- See `cpp/FIX_EXECUTABLE_NOT_FOUND.md` for detailed troubleshooting
- See `cpp/WINDOWS_BUILD_GUIDE.md` for general Windows build instructions
- Check `cpp/build/README_BUILD_ISSUE.txt` for quick reference

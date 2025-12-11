# Fix: Executable Not Found in Build Folder

## Problem

You ran `build.bat` and CMake configured successfully, but you can't find the `.exe` files in the build folder.

## Root Cause

The build folder contains **Linux build artifacts** (executables without `.exe` extension) from a previous build. When you try to build on Windows, CMake gets confused by the existing Linux files.

## Solution

### Quick Fix (3 Steps)

1. **Open Command Prompt or PowerShell** in your cpp folder:
   ```cmd
   cd "D:\Zoppler Projects\AiMissionPlanner\cpp"
   ```

2. **Delete the build folder completely:**
   
   **Option A - Command Prompt:**
   ```cmd
   rmdir /s /q build
   ```
   
   **Option B - PowerShell:**
   ```powershell
   Remove-Item -Recurse -Force build
   ```
   
   **Option C - Git Bash:**
   ```bash
   rm -rf build
   ```

3. **Run the build script again:**
   ```cmd
   build.bat
   ```

### What the Updated build.bat Does

The improved `build.bat` now:
- ✅ Detects Linux artifacts and warns you before proceeding
- ✅ Shows clearer progress messages (Step 1, 2, 3)
- ✅ Verifies that `.exe` files are actually created
- ✅ Lists all executables at the end
- ✅ Provides better error messages

### Expected Output

After cleaning and rebuilding, you should see:

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

## Why This Happens

This project exists in both:
- **Remote Linux workspace** (where I make changes)
- **Your local Windows machine** (where you build and run)

When the build folder contains Linux executables and you try to build on Windows:
- ❌ CMake sees existing targets and may skip compilation
- ❌ Make/MinGW gets confused by Linux binary formats
- ❌ No `.exe` files are created

**Solution**: Always clean the build folder when switching between Linux and Windows!

## Running the Application

Once built successfully:

```cmd
cd build
trajectory_app.exe --help
trajectory_app.exe --model ..\models\trajectory_model.onnx --demo
```

## Troubleshooting

### Issue: "cmake is not recognized"
**Solution**: Install CMake and add it to PATH
- Download: https://cmake.org/download/
- During installation, select "Add CMake to system PATH"

### Issue: "mingw32-make is not recognized"
**Solution**: Install MinGW-w64 and add it to PATH
- Download: https://www.mingw-w64.org/downloads/
- Add `C:\mingw64\bin` (or your installation path) to PATH

### Issue: "ONNX Runtime not found"
**Solution**: The build script downloads it automatically, but if it fails:
- Download manually: https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-win-x64-1.16.3.zip
- Extract to `libs\onnxruntime-win-x64-1.16.3`
- Run `build.bat` again

### Issue: Build succeeds but executables still missing
**Solution**: Check for compilation errors
```cmd
cd build
mingw32-make VERBOSE=1
```

This will show detailed compilation output to identify the issue.

## Alternative: Use PowerShell Script

For a better experience, use the PowerShell script instead:

```powershell
.\build.ps1
```

The PowerShell script provides better progress indicators and error handling.

# Trajectory GUI Silent Exit Fix

## Problem
The trajectory GUI application exits silently after printing "Checking dependencies..." without showing any error message or launching the GUI window.

## Root Cause
The application is likely encountering one of these issues:

1. **PyQtGraph OpenGL Import Failure**: The `pyqtgraph.opengl` module imports but fails during initialization
2. **OpenGL Driver Issues**: Missing or incompatible OpenGL drivers
3. **PyOpenGL Missing**: PyOpenGL package not installed or not working correctly
4. **Qt Platform Plugin Issues**: Missing Qt platform plugins or display configuration problems

## Diagnostic Steps

### Step 1: Run the Diagnostic Script
```bash
python diagnose_gui_startup.py
```

This will test each dependency individually and provide detailed error messages.

### Step 2: Test Basic PyQt5 (Optional)
```bash
python test_basic_gui.py
```

This tests if PyQt5 works without OpenGL components.

### Step 3: Check the Enhanced Error Messages
The updated `run_trajectory_gui.py` now provides more detailed error messages:
- Shows progress for each dependency check
- Catches both ImportError and runtime exceptions
- Provides specific error types and tracebacks

## Solutions

### Solution 1: Install Missing Dependencies

If PyOpenGL is missing or broken:
```bash
pip uninstall PyOpenGL PyOpenGL_accelerate
pip install PyOpenGL PyOpenGL_accelerate
```

If other packages are missing:
```bash
pip install PyQt5 pyqtgraph scipy numpy
```

### Solution 2: Update Graphics Drivers

**Windows:**
1. Open Device Manager
2. Expand "Display adapters"
3. Right-click your graphics card
4. Select "Update driver"
5. Choose "Search automatically for updated driver software"

**Alternative:** Download drivers directly from:
- NVIDIA: https://www.nvidia.com/Download/index.aspx
- AMD: https://www.amd.com/en/support
- Intel: https://downloadcenter.intel.com/product/80939/Graphics

### Solution 3: Reinstall PyQt5 and PyQtGraph

Sometimes packages get corrupted:
```bash
pip uninstall PyQt5 pyqtgraph
pip install PyQt5 pyqtgraph
```

### Solution 4: Use Software Rendering (If Hardware Acceleration Fails)

Set environment variable before running:

**Windows (Command Prompt):**
```cmd
set LIBGL_ALWAYS_SOFTWARE=1
python run_trajectory_gui.py
```

**Windows (PowerShell):**
```powershell
$env:LIBGL_ALWAYS_SOFTWARE=1
python run_trajectory_gui.py
```

### Solution 5: Check Python Version Compatibility

Ensure you're using Python 3.8-3.11. Python 3.12+ may have compatibility issues with some packages.

Check your version:
```bash
python --version
```

If using Python 3.12+, consider using Python 3.11:
```bash
conda create -n missionplannerenv python=3.11
conda activate missionplannerenv
pip install -r requirements.txt
```

## What Was Fixed

### Enhanced `run_trajectory_gui.py`

1. **Better Progress Reporting**: Shows [1/5], [2/5], etc. for each dependency check
2. **Exception Handling**: Catches both ImportError and generic exceptions
3. **Detailed Error Messages**: Shows error type, message, and full traceback
4. **Helpful Suggestions**: Provides next steps based on the error
5. **stdout Flushing**: Ensures all print statements appear immediately

### New Diagnostic Tools

1. **diagnose_gui_startup.py**: Comprehensive dependency testing
   - Tests each import individually
   - Attempts to create OpenGL widgets
   - Retrieves OpenGL driver information
   - Provides detailed error messages

2. **test_basic_gui.py**: Simple PyQt5 test
   - Tests basic PyQt5 without OpenGL
   - Helps isolate OpenGL-specific issues
   - Quick verification that PyQt5 works

## Expected Output After Fix

When running `python run_trajectory_gui.py`, you should see:

```
============================================================
3D Trajectory Generator GUI
============================================================

Starting application...

Features:
  - 12 different trajectory types
  - Real-time 3D visualization
  - Customizable physical constraints
  - Trajectory metrics calculation
  - Save/load functionality

============================================================

Checking dependencies...

  [1/5] Checking NumPy... ✓
  [2/5] Checking PyQt5... ✓
  [3/5] Checking PyQtGraph... ✓
  [4/5] Checking PyQtGraph OpenGL... ✓
  [5/5] Checking SciPy... ✓

All dependencies found!

Initializing GUI...
  - Importing trajectory_gui module...
  - Module imported successfully
  - Starting main GUI application...
Creating GUI window...
Showing window...
GUI window created successfully!
Starting event loop...

[GUI window opens]
```

## Common Error Messages and Fixes

### Error: "ModuleNotFoundError: No module named 'OpenGL'"
**Fix:** Install PyOpenGL
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### Error: "ImportError: DLL load failed while importing QtCore"
**Fix:** Reinstall PyQt5 or install Visual C++ Redistributable
```bash
pip uninstall PyQt5
pip install PyQt5
```
Or download: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Error: "Failed to create OpenGL context"
**Fix:** Update graphics drivers or use software rendering (see Solution 4)

### Error: "Could not find the Qt platform plugin 'windows'"
**Fix:** Reinstall PyQt5 and ensure Qt plugins are installed
```bash
pip uninstall PyQt5
pip cache purge
pip install PyQt5
```

## Testing the Fix

After applying solutions, run:
```bash
python run_trajectory_gui.py
```

The application should now:
1. Show progress for each dependency check
2. Either launch the GUI successfully OR
3. Show detailed error messages with next steps

## Additional Resources

- **PyQt5 Documentation**: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- **PyQtGraph Documentation**: https://pyqtgraph.readthedocs.io/
- **OpenGL Troubleshooting**: https://pyopengl.sourceforge.net/documentation/manual-3.0/

## Still Having Issues?

If problems persist after trying all solutions:

1. Run the diagnostic script and save output:
   ```bash
   python diagnose_gui_startup.py > diagnostic_output.txt
   ```

2. Check system information:
   - Operating System version
   - Python version (`python --version`)
   - Graphics card model
   - Available RAM

3. Try running with maximum verbosity:
   ```bash
   python -v run_trajectory_gui.py 2>&1 | tee verbose_output.txt
   ```

4. Share the diagnostic output for further assistance

## Summary

The silent exit issue was caused by unhandled exceptions during dependency checking. The fixes include:

✓ Enhanced error handling and reporting
✓ Detailed diagnostic tools
✓ Clear error messages with actionable solutions
✓ Multiple fallback options for different failure modes

The application should now either work correctly or provide clear information about what's wrong and how to fix it.

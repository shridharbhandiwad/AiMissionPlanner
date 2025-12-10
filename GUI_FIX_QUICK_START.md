# Quick Start: Fix GUI Silent Exit Issue

## The Problem
Your trajectory GUI exits immediately after "Checking dependencies..." with no error message.

## Quick Fix (Most Common)

### Fix #1: Install PyOpenGL (Most Likely Solution)
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

Then run:
```bash
python run_trajectory_gui.py
```

### Fix #2: Update Graphics Drivers
1. Go to Device Manager (Windows Key + X → Device Manager)
2. Expand "Display adapters"
3. Right-click your graphics card → "Update driver"
4. Restart computer
5. Try running the GUI again

### Fix #3: Use Software Rendering
If hardware acceleration is the issue:
```cmd
set LIBGL_ALWAYS_SOFTWARE=1
python run_trajectory_gui.py
```

## Diagnostic Tools

### Run This First
```bash
python diagnose_gui_startup.py
```
This will tell you exactly what's wrong.

### Test Basic PyQt5
```bash
python test_basic_gui.py
```
This tests if PyQt5 works at all.

## What Changed

The `run_trajectory_gui.py` file now:
- Shows detailed progress for each dependency
- Catches all types of errors (not just import errors)
- Prints helpful error messages with solutions
- Flushes output immediately so you can see what's happening

## Expected Output (Success)

```
============================================================
3D Trajectory Generator GUI
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
```

## If It Still Doesn't Work

1. Run diagnostic:
   ```bash
   python diagnose_gui_startup.py > error.txt
   ```

2. Check error.txt for detailed information

3. Try reinstalling everything:
   ```bash
   pip uninstall PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate
   pip install PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate
   ```

4. Make sure you're using Python 3.8-3.11 (not 3.12+):
   ```bash
   python --version
   ```

## Need More Help?

See the detailed guide: `TRAJECTORY_GUI_SILENT_EXIT_FIX.md`

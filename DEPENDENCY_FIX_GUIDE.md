# Dependency Fix Guide

## Problem

The trajectory GUI fails to start with missing dependencies:
- ✗ NumPy
- ✗ PyQtGraph
- ✗ PyOpenGL
- ✗ SciPy

## Solution

### Option 1: Quick Fix (Windows)

Run the automated fix script:

```bash
fix_dependencies.bat
```

This will automatically install all missing dependencies and verify they work.

### Option 2: Manual Installation (Windows)

Open Command Prompt or PowerShell in your `missionplannerenv` conda environment and run:

```bash
pip install numpy==1.26.4 scipy==1.14.1 PyQt5==5.15.11 PyQtGraph==0.13.7 PyOpenGL==3.1.7 PyOpenGL_accelerate
```

### Option 3: Install from requirements.txt

```bash
pip install -r requirements.txt
```

This installs all project dependencies at once.

## Verification

After installation, verify dependencies are working:

```bash
python diagnose_gui_startup.py
```

All checks should show ✓ (checkmark).

## Running the GUI

Once dependencies are installed:

```bash
python run_trajectory_gui_safe.py
```

Or use the standard launcher:

```bash
python src/trajectory_gui.py
```

## Troubleshooting

### If NumPy fails
- Make sure you're using Python 3.8 or higher
- Try: `pip install --upgrade numpy`

### If PyQt5 fails
- Windows: Install Visual C++ Redistributable
- Linux: `sudo apt-get install python3-pyqt5`

### If PyOpenGL fails
- Try: `pip install --upgrade PyOpenGL PyOpenGL_accelerate`
- On some systems, you may need system OpenGL libraries

### If you see "command not found: python"
- Use `python3` instead of `python`
- Or activate your conda environment: `conda activate missionplannerenv`

## Environment Check

Make sure you're in the correct conda environment:

```bash
# Check current environment
conda info --envs

# Activate missionplannerenv if needed
conda activate missionplannerenv
```

## Still Having Issues?

Run the full diagnostic:

```bash
python diagnose_environment.py
```

This provides detailed information about your Python environment and installed packages.

## Key Points

✅ The conda environment `missionplannerenv` must be active  
✅ All 5 dependencies must be installed: NumPy, SciPy, PyQt5, PyQtGraph, PyOpenGL  
✅ Use the same Python interpreter that has the packages installed  
✅ On Windows, use `python`; on Linux/Mac, use `python3`  

---

**Need more help?** See the related documentation:
- `GUI_TROUBLESHOOTING.md` - Comprehensive GUI troubleshooting
- `README.md` - Project overview
- `INSTALLATION_SUMMARY.md` - Complete installation guide

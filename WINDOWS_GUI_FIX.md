# Windows GUI Dependencies Fix

## Problem

You're seeing these errors when trying to run the trajectory GUI:

1. **NumPy MINGW-W64 Warnings**: NumPy was built with an experimental MINGW-W64 compiler causing crashes
2. **Missing PyQt5**: `ModuleNotFoundError: No module named 'PyQt5'`
3. **Missing PyQtGraph**: `ModuleNotFoundError: No module named 'pyqtgraph'`
4. **Missing PyOpenGL**: OpenGL support not installed

## Quick Fix (Recommended)

**Option 1: Fix Everything at Once**

Run this script to fix all issues automatically:

```batch
fix_all_dependencies.bat
```

This script will:
- ✓ Reinstall NumPy with the correct Windows binary
- ✓ Install PyQt5, PyQtGraph, and PyOpenGL
- ✓ Verify all installations

**After running the script, try:**
```batch
python run_trajectory_gui.py
```

---

## Individual Fixes

If you prefer to fix issues one at a time:

### Fix 1: NumPy MINGW-W64 Issue

Run:
```batch
fix_numpy_windows.bat
```

Or manually:
```batch
pip uninstall -y numpy
pip cache remove numpy
pip install --only-binary :all: "numpy>=2.0.0,<3.0.0"
```

**Note:** Python 3.12+ requires NumPy 2.x. Use `numpy==1.26.4` only if you're on Python 3.11 or earlier.

### Fix 2: Install GUI Dependencies

Run:
```batch
fix_gui_dependencies.bat
```

Or manually:
```batch
pip install PyQt5==5.15.11
pip install PyQtGraph==0.13.7
pip install PyOpenGL==3.1.7
pip install PyOpenGL_accelerate==3.1.7
```

---

## Verification

After applying the fixes, verify your installation:

```batch
python -c "import numpy; from PyQt5 import QtWidgets; import pyqtgraph; print('✓ All packages working!')"
```

Then run the GUI:
```batch
python run_trajectory_gui.py
```

---

## Complete Reinstallation

If the quick fixes don't work, do a complete reinstallation:

### Step 1: Clean Environment

```batch
# Deactivate virtual environment if active
deactivate

# Delete old virtual environment
rmdir /s /q venv
```

### Step 2: Reinstall Everything

```batch
# Run the updated installation script
install_windows.bat
```

The installation script now includes all GUI dependencies.

### Step 3: Run the GUI

```batch
# Activate virtual environment
venv\Scripts\activate

# Run the GUI
python run_trajectory_gui.py
```

---

## Troubleshooting

### If NumPy still has MINGW-W64 warnings:

1. Make sure you're using Python 3.9-3.12 (Python 3.13 has limited package support)
2. Check your Python installation: `python --version`
3. Try clearing ALL pip cache: `pip cache purge`
4. Reinstall NumPy: 
   - For Python 3.12+: `pip install --force-reinstall --no-cache-dir "numpy>=2.0.0,<3.0.0"`
   - For Python 3.11 or earlier: `pip install --force-reinstall --no-cache-dir numpy==1.26.4`

### If PyQt5 won't install:

1. Make sure you have Visual C++ Redistributables installed
   - Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Try a different Python version (3.10 or 3.11 work best with PyQt5)
3. Try without version pinning: `pip install PyQt5`

### If OpenGL issues persist:

1. Update your graphics drivers
2. Try software rendering mode (slower but more compatible):
   ```batch
   set QT_OPENGL=software
   python run_trajectory_gui.py
   ```

### If nothing works:

Run the diagnostic script to identify the exact issue:
```batch
python diagnose_gui_startup.py
```

---

## Alternative: Use Conda (Advanced)

If pip installations keep failing, try using Conda:

```batch
# Create conda environment
conda create -n trajectory python=3.11
conda activate trajectory

# Install packages from conda-forge
conda install -c conda-forge numpy scipy pandas matplotlib
conda install -c conda-forge pyqt pyqtgraph
pip install PyOpenGL PyOpenGL_accelerate

# Install project-specific packages
pip install torch torchvision onnx onnxruntime tqdm
```

---

## Support

If you're still having issues after trying these fixes:

1. Run: `python diagnose_gui_startup.py`
2. Check: `python --version` (should be 3.9-3.12)
3. Check: `pip list` (to see installed packages)

Common causes:
- Wrong Python version (use 3.9-3.12, NOT 3.13)
- Missing Visual C++ Redistributables
- Outdated pip (`python -m pip install --upgrade pip`)
- Conflicting conda and pip installations

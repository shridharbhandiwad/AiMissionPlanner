# Fix for Silent Exit Issue

## Problem
The trajectory GUI exits silently after printing "Checking NumPy..." without any error message or continuing to the next dependency check.

## What's Happening
When an application exits silently during an import, it usually means one of these:

1. **Hard crash during DLL loading** (Windows) - NumPy or one of its dependencies fails to load a required DLL
2. **Segmentation fault** - Low-level crash that Python can't catch
3. **Missing Visual C++ Redistributables** - Required by NumPy on Windows
4. **Corrupted package installation** - NumPy package files are damaged
5. **Incompatible Python version** - Python 3.12+ can have issues with some packages

## Solutions

### Quick Fix: Use the Safe Launcher

Try using the safe launcher which tests imports in subprocesses first:

```bash
python run_trajectory_gui_safe.py
```

Or on Windows, double-click:
```
run_trajectory_gui_safe.bat
```

This version will catch hard crashes and provide better error messages.

### Solution 1: Install Visual C++ Redistributables (Windows)

NumPy requires the Microsoft Visual C++ Redistributable. Download and install:

**Latest Version:**
https://aka.ms/vs/17/release/vc_redist.x64.exe

**Older Version (if latest doesn't work):**
https://aka.ms/vs/16/release/vc_redist.x64.exe

After installing, restart your computer and try again.

### Solution 2: Diagnose NumPy Specifically

Run the NumPy diagnostic tool:

```bash
python diagnose_numpy.py
```

Or on Windows, double-click:
```
diagnose_numpy.bat
```

This will test NumPy in isolation and identify the specific problem.

### Solution 3: Reinstall NumPy

Sometimes NumPy gets corrupted during installation. Reinstall it:

```bash
# Uninstall completely
pip uninstall -y numpy

# Clear pip cache
pip cache purge

# Reinstall
pip install numpy
```

### Solution 4: Use Conda NumPy (Recommended for Windows)

Conda packages often work better on Windows because they include all dependencies:

```bash
# If you're using conda
conda install -c conda-forge numpy

# Or reinstall your entire environment
conda create -n missionplannerenv python=3.11
conda activate missionplannerenv
conda install -c conda-forge numpy scipy pyqt
pip install pyqtgraph pyopengl pyopengl_accelerate
```

### Solution 5: Check Python Version

Ensure you're using Python 3.8-3.11 (not 3.12+):

```bash
python --version
```

If you have Python 3.12 or later, create a new environment with 3.11:

```bash
conda create -n missionplannerenv python=3.11
conda activate missionplannerenv
pip install -r requirements.txt
```

### Solution 6: Test NumPy Manually

Open a Python REPL and test NumPy:

```bash
python
```

Then in Python:

```python
>>> import sys
>>> print(f"Python: {sys.version}")
>>> print(f"Executable: {sys.executable}")
>>> import numpy
>>> print(f"NumPy: {numpy.__version__}")
>>> print(f"Location: {numpy.__file__}")
>>> arr = numpy.array([1, 2, 3])
>>> print(arr)
>>> quit()
```

If this fails, note the exact error message.

### Solution 7: Full Reinstall of Dependencies

Complete reinstall of all GUI dependencies:

```bash
# Uninstall everything
pip uninstall -y numpy scipy PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate

# Clear cache
pip cache purge

# Reinstall (use conda for NumPy on Windows)
conda install -c conda-forge numpy scipy
pip install PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate
```

## Diagnostic Steps

### Step 1: Check What Python You're Using

```bash
where python
python --version
```

Make sure you're using the Python from your conda environment.

### Step 2: Check NumPy Installation

```bash
pip show numpy
```

Look for:
- Version (should be 1.24.x or 1.26.x)
- Location (should be in your conda environment)

### Step 3: Run Enhanced Diagnostics

```bash
python diagnose_numpy.py > numpy_diagnostic.txt
```

This saves the full diagnostic output to a file you can review.

### Step 4: Check for DLL Issues (Windows)

Open Command Prompt as Administrator and run:

```bash
# Check if NumPy DLLs are accessible
python -c "import numpy; print(numpy.__file__)"

# Try to import NumPy with verbose output
python -v -c "import numpy" 2>&1 | findstr /i "error dll"
```

## Common Error Messages and Fixes

### "ImportError: DLL load failed"
**Fix:** Install Visual C++ Redistributables (Solution 1)

### "ImportError: No module named 'numpy'"
**Fix:** NumPy not installed in this environment
```bash
pip install numpy
```

### No error, just exits
**Fix:** Use safe launcher (Solution 1) or reinstall NumPy (Solution 3)

### "numpy.core.multiarray failed to import"
**Fix:** NumPy is corrupted, reinstall with:
```bash
pip uninstall -y numpy && pip cache purge && pip install numpy
```

### Windows error dialog about missing DLL
**Fix:** Install Visual C++ Redistributables

## Testing After Fix

After applying any solution, test:

1. **Test NumPy directly:**
   ```bash
   python -c "import numpy; print('NumPy OK:', numpy.__version__)"
   ```

2. **Run NumPy diagnostics:**
   ```bash
   python diagnose_numpy.py
   ```

3. **Run full GUI diagnostics:**
   ```bash
   python diagnose_gui_startup.py
   ```

4. **Try the safe launcher:**
   ```bash
   python run_trajectory_gui_safe.py
   ```

5. **If all pass, try the regular launcher:**
   ```bash
   python run_trajectory_gui.py
   ```

## Files Created to Help Debug

- `diagnose_numpy.py` - Comprehensive NumPy testing
- `diagnose_numpy.bat` - Windows launcher for NumPy diagnostics
- `run_trajectory_gui_safe.py` - Safe launcher that catches hard crashes
- `run_trajectory_gui_safe.bat` - Windows launcher for safe mode
- `run_trajectory_gui.py` - Enhanced with better error messages (updated)

## Still Having Issues?

If none of the above solutions work:

1. Run all diagnostics and save output:
   ```bash
   python --version > debug_info.txt
   python diagnose_numpy.py >> debug_info.txt
   python diagnose_gui_startup.py >> debug_info.txt
   pip list >> debug_info.txt
   ```

2. Check your system:
   - Windows version: `winver`
   - RAM: At least 4GB recommended
   - Graphics card: Check Device Manager
   - Available disk space: At least 1GB

3. Try a fresh conda environment:
   ```bash
   conda deactivate
   conda remove -n missionplannerenv --all
   conda create -n missionplannerenv python=3.11
   conda activate missionplannerenv
   conda install -c conda-forge numpy scipy pyqt
   pip install pyqtgraph pyopengl pyopengl_accelerate
   ```

## Next Steps

After fixing NumPy, you may encounter other dependency issues. The scripts will guide you through:
- PyQt5 installation
- PyQtGraph setup
- OpenGL driver configuration
- Graphics card compatibility

Each error will now be clearly reported with specific solutions.

---

**Quick Reference:**

| Problem | Solution |
|---------|----------|
| Silent exit at NumPy | Use `run_trajectory_gui_safe.py` |
| Missing DLL | Install Visual C++ Redistributables |
| NumPy not found | `pip install numpy` |
| Corrupted NumPy | `pip uninstall -y numpy && pip cache purge && pip install numpy` |
| Python 3.12+ | Downgrade to Python 3.11 |
| Conda environment | Use `conda install -c conda-forge numpy` |

---

**Remember:** The safe launcher (`run_trajectory_gui_safe.py`) tests all imports in subprocesses first, so it can catch crashes that the regular launcher can't. Always try it first when debugging!

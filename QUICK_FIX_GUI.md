# Quick Fix: GUI Not Opening

## Problem
Running `run_trajectory_gui.bat` completes but no window appears.

## Solution (5 Minutes)

### 1. Activate Environment
```bash
conda activate missionplannerenv
```

### 2. Install Missing Packages
```bash
pip install PyOpenGL PyOpenGL_accelerate scipy
```

### 3. Test Basic GUI
```bash
python test_gui_display.py
```
**Expected:** A test window appears → If YES, continue. If NO, reinstall PyQt5:
```bash
pip install --force-reinstall PyQt5
```

### 4. Test OpenGL
```bash
python test_opengl_display.py
```
**Expected:** 3D grid appears → If NO, update graphics drivers.

### 5. Run Main GUI
```bash
python run_trajectory_gui.py
```

## Still Not Working?

### Check Console Output
The updated script now shows exactly what's wrong:
- ✓ = Working
- ✗ = Failed (with details)

### Common Fixes

**"Module not found" error:**
```bash
pip install PyQt5 pyqtgraph PyOpenGL scipy numpy
```

**"DLL load failed" (Windows):**
- Install: https://aka.ms/vs/17/release/vc_redist.x64.exe

**OpenGL initialization failed:**
- Update graphics card drivers
- Check if graphics acceleration is enabled

**Window appears then closes:**
- Run from terminal to see error messages
- Check antivirus isn't blocking it

## Get More Help

- **Quick Guide:** `GUI_FIX_SUMMARY.md`
- **Detailed Guide:** `GUI_TROUBLESHOOTING.md`
- **Main Docs:** `START_HERE_GUI.md`

## Report Issue

If still failing, capture output:
```bash
python run_trajectory_gui.py > output.txt 2>&1
```

Then share `output.txt` with:
- Python version: `python --version`
- OS version
- Graphics card model

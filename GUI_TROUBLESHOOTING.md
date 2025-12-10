# GUI Troubleshooting Guide

## Problem: GUI Window Not Opening

If the `run_trajectory_gui.bat` script completes but the GUI window doesn't appear, follow these troubleshooting steps:

## Quick Diagnostic Steps

### Step 1: Test Basic GUI Display

Run the basic GUI test to check if PyQt5 works:

```bash
python test_gui_display.py
```

Or on Windows:
```bash
test_gui_display.bat
```

**Expected Result:** A simple test window should appear.

- ✓ **If the window appears**: PyQt5 is working, proceed to Step 2
- ✗ **If no window appears**: PyQt5 has issues, see [PyQt5 Installation Issues](#pyqt5-installation-issues)

### Step 2: Test OpenGL Support

Run the OpenGL test to check if 3D visualization works:

```bash
python test_opengl_display.py
```

**Expected Result:** A window with a 3D grid and red line should appear.

- ✓ **If 3D view appears**: OpenGL is working, proceed to Step 3
- ✗ **If error or no window**: OpenGL has issues, see [OpenGL Issues](#opengl-issues)

### Step 3: Run the Main GUI with Diagnostics

The updated launcher now includes detailed diagnostics:

```bash
python run_trajectory_gui.py
```

Or on Windows:
```bash
run_trajectory_gui.bat
```

This will check all dependencies and show detailed error messages if something fails.

## Common Issues and Solutions

### PyQt5 Installation Issues

**Symptoms:**
- No window appears
- Import errors for PyQt5
- `test_gui_display.py` fails

**Solutions:**

1. **Reinstall PyQt5:**
   ```bash
   pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip
   pip install PyQt5
   ```

2. **If using Conda:**
   ```bash
   conda install pyqt
   ```

3. **Check Python version:**
   - PyQt5 requires Python 3.6 or later
   - Python 3.13+ may have compatibility issues - use Python 3.8-3.12

### OpenGL Issues

**Symptoms:**
- Basic GUI test works, but OpenGL test fails
- Error: "OpenGL initialization failed"
- Black/blank window in 3D view

**Solutions:**

1. **Install/Update OpenGL packages:**
   ```bash
   pip install PyOpenGL PyOpenGL_accelerate
   ```

2. **Update Graphics Drivers:**
   - NVIDIA: Download latest drivers from nvidia.com
   - AMD: Download latest drivers from amd.com
   - Intel: Update through Windows Update or intel.com

3. **Check OpenGL Support:**
   - Right-click desktop → Display settings → Advanced display
   - Ensure graphics acceleration is enabled

4. **Alternative: Use Software Rendering:**
   
   If hardware OpenGL doesn't work, try software rendering:
   
   ```bash
   # Before running the GUI, set this environment variable:
   set PYOPENGL_PLATFORM=osmesa  # Windows CMD
   # or
   $env:PYOPENGL_PLATFORM="osmesa"  # Windows PowerShell
   ```

### Missing Dependencies

**Symptoms:**
- "Module not found" errors
- Import errors

**Solution:**

Install all required dependencies:

```bash
pip install PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate scipy numpy
```

Or if using Conda:

```bash
conda install pyqt pyqtgraph scipy numpy
pip install PyOpenGL PyOpenGL_accelerate
```

### Virtual Environment Issues

**Symptoms:**
- Works in base environment but not in virtual env
- DLL load errors on Windows

**Solutions:**

1. **Ensure environment is activated:**
   ```bash
   # Conda
   conda activate missionplannerenv
   
   # venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Reinstall packages in the environment:**
   ```bash
   pip install --force-reinstall PyQt5 pyqtgraph PyOpenGL
   ```

### Windows-Specific Issues

**Issue 1: DLL Load Failed**

```
ImportError: DLL load failed while importing QtCore
```

**Solution:**
- Install Visual C++ Redistributables from Microsoft
- Link: https://aka.ms/vs/17/release/vc_redist.x64.exe

**Issue 2: Display Scaling Issues**

If window appears but is tiny or huge:

1. Right-click `python.exe`
2. Properties → Compatibility
3. Check "Override high DPI scaling behavior"
4. Select "System (Enhanced)"

**Issue 3: Window Opens But Immediately Closes**

- Check if antivirus is blocking the application
- Try running Command Prompt as Administrator
- Check Windows Event Viewer for crash logs

## Advanced Diagnostics

### Check PyQt5 Version

```python
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
print(f"Qt version: {QT_VERSION_STR}")
print(f"PyQt version: {PYQT_VERSION_STR}")
```

Should show Qt 5.x and PyQt 5.x

### Check OpenGL Version

```python
from OpenGL.GL import glGetString, GL_VERSION
print(glGetString(GL_VERSION))
```

Should show OpenGL version (2.0+ required, 3.0+ recommended)

### Verbose Error Output

Run with Python in verbose mode:

```bash
python -v run_trajectory_gui.py
```

This shows all imports and can reveal hidden errors.

## Still Having Issues?

If none of the above solutions work:

1. **Capture the full error output:**
   ```bash
   python run_trajectory_gui.py > gui_output.txt 2>&1
   ```

2. **Check the generated `gui_output.txt` file for error details**

3. **System Information to Provide:**
   - Python version: `python --version`
   - OS version
   - Graphics card model
   - Output from test scripts
   - Full error message from `gui_output.txt`

## Alternative: Run Without 3D Visualization

If OpenGL continues to fail, you can modify the GUI to use 2D plots instead:

1. Replace PyQtGraph OpenGL with matplotlib
2. Use 2D projections of 3D trajectories
3. Contact support for a 2D-only version

## Success Indicators

When everything works correctly, you should see:

1. ✓ All dependency checks pass
2. ✓ "Creating GUI window..." message
3. ✓ "Showing window..." message  
4. ✓ "GUI window created successfully!" message
5. ✓ A window appears with control panels and 3D view
6. ✓ The window remains open and interactive

## Contact Information

For additional support:
- Check project README.md
- Review INSTRUCTIONS.md for setup details
- See HARDWARE_REQUIREMENTS.md for system requirements

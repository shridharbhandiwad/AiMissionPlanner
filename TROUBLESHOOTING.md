# Troubleshooting Guide

This guide helps resolve common issues when running the 3D Trajectory Generator GUI.

## Quick Diagnosis

Run the diagnostic scripts to identify issues:

```bash
# Test NumPy specifically
python diagnose_numpy.py

# Test all GUI dependencies
python diagnose_gui_startup.py

# Test basic PyQt5 functionality
python test_basic_gui.py
```

## Common Issues

### 1. Application Exits During NumPy Check

**Symptoms:**
- Program prints "[1/5] Checking NumPy..." and then exits
- No error message displayed
- Returns to command prompt immediately

**Cause:**
- NumPy has missing or incompatible DLL dependencies (common on Windows)
- Corrupted NumPy installation
- Missing Microsoft Visual C++ Redistributables

**Solutions:**

#### Option 1: Automatic Repair (Recommended)
```bash
python fix_numpy.py
```

#### Option 2: Manual Reinstall
```bash
# Uninstall
pip uninstall numpy

# Clear cache
pip cache purge

# Reinstall
pip install numpy
```

#### Option 3: Windows - Install VC++ Redistributables
1. Download and install: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Restart your computer
3. Reinstall NumPy: `pip install numpy`

#### Option 4: Use Conda
```bash
conda install numpy
```

### 2. PyQt5 Import Errors

**Solutions:**
```bash
pip install PyQt5
```

If that fails:
```bash
pip uninstall PyQt5
pip install PyQt5==5.15.9
```

### 3. OpenGL/PyQtGraph Errors

**Solutions:**
```bash
pip install PyOpenGL PyOpenGL_accelerate pyqtgraph
```

**Windows-specific:**
- Update graphics drivers
- Install DirectX End-User Runtime

**Linux-specific:**
```bash
sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev
```

### 4. Display/Platform Plugin Errors (Linux)

**Symptoms:**
- "Could not connect to display"
- "QT platform plugin error"

**Solutions:**
```bash
# Set display
export DISPLAY=:0

# Install Qt platform plugins
sudo apt-get install libxcb-xinerama0 libxcb-cursor0
```

### 5. Import Errors for scipy

**Solutions:**
```bash
pip install scipy
```

## Testing After Fixes

After applying fixes, test in order:

1. Test NumPy:
   ```bash
   python diagnose_numpy.py
   ```

2. Test all dependencies:
   ```bash
   python diagnose_gui_startup.py
   ```

3. Test basic GUI:
   ```bash
   python test_basic_gui.py
   ```

4. Run the full application:
   ```bash
   python run_trajectory_gui.py
   ```

## Clean Installation

If all else fails, try a clean virtual environment:

### Windows
```bash
# Create new virtual environment
python -m venv fresh_venv

# Activate
fresh_venv\Scripts\activate

# Install dependencies
pip install numpy PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate scipy

# Run application
python run_trajectory_gui.py
```

### Linux/Mac
```bash
# Create new virtual environment
python3 -m venv fresh_venv

# Activate
source fresh_venv/bin/activate

# Install dependencies
pip install numpy PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate scipy

# Run application
python run_trajectory_gui.py
```

## System Requirements

- Python 3.8 or higher
- Windows 10/11, Linux (Ubuntu 18.04+), or macOS 10.14+
- OpenGL 3.0+ capable graphics
- 4GB RAM minimum
- Display resolution: 1280x720 or higher

## Getting Help

If you continue to experience issues:

1. Run all diagnostic scripts and save the output
2. Note your system information:
   - OS version
   - Python version (`python --version`)
   - Package versions (`pip list`)
3. Check the error logs
4. Look for similar issues in the project documentation

## Advanced Troubleshooting

### Check Python Environment
```bash
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list

# Check for conflicts
pip check
```

### Verify NumPy Installation
```bash
python -c "import numpy; print(numpy.__version__); print(numpy.__file__)"
```

### Verify PyQt5 Installation
```bash
python -c "from PyQt5.QtCore import QT_VERSION_STR; print(QT_VERSION_STR)"
```

### Check OpenGL Support
```bash
python -c "from OpenGL.GL import *; print('OpenGL OK')"
```

## Platform-Specific Notes

### Windows
- Ensure you have admin rights for installation
- Some antivirus software may interfere with Python packages
- Use PowerShell or Command Prompt (not Git Bash for GUI apps)

### Linux
- May need to install additional system packages
- X11 or Wayland display server required
- Check display permissions: `xhost +local:`

### macOS
- May need to grant Terminal accessibility permissions
- Some Macs require Rosetta 2 for compatibility

## Known Issues

1. **NumPy 2.0+ compatibility**: Some packages may not be compatible with NumPy 2.0. Use `pip install "numpy<2.0"` if needed.

2. **PyQt5 on Apple Silicon**: May require conda installation instead of pip.

3. **OpenGL on Virtual Machines**: Limited or no OpenGL support in some VM configurations.

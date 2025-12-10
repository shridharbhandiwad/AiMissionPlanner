# Fix: Matplotlib DLL Import Error on Windows

## The Error

```
ImportError: DLL load failed while importing _c_internal_utils: The specified module could not be found.
```

This error occurs when matplotlib tries to import its C extension modules but can't find the required Windows DLL files.

## Quick Fix (Recommended)

### Option 1: Use the Fix Script

1. **Activate your virtual environment:**
   ```batch
   venv\Scripts\activate
   ```

2. **Run the fix script:**
   ```batch
   fix_matplotlib_dll_error.bat
   ```

3. **Test the fix:**
   ```batch
   python src/data_generator.py
   ```

This script will:
- ✓ Upgrade pip
- ✓ Uninstall matplotlib and dependencies
- ✓ Clear pip cache
- ✓ Reinstall numpy with proper Windows binary
- ✓ Reinstall matplotlib with all dependencies
- ✓ Verify matplotlib works correctly

**Time required:** 2-3 minutes

---

## Manual Fix (Alternative)

If the script doesn't work, try these manual steps:

### Step 1: Install Visual C++ Redistributables

**This is the most common cause of the error.**

Download and install Microsoft Visual C++ Redistributables:
- **Latest version (2015-2022)**: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install both x64 and x86 versions if unsure

**After installation, restart your computer.**

### Step 2: Reinstall Packages

Open your terminal with venv activated:

```batch
# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Uninstall problematic packages
pip uninstall -y matplotlib numpy pillow

# Clear pip cache
pip cache purge

# Reinstall with Windows binaries
pip install --only-binary :all: --force-reinstall "numpy>=2.0.0,<3.0.0"
pip install --only-binary :all: --force-reinstall matplotlib==3.9.0

# Test
python -c "import matplotlib.pyplot as plt; print('Success!')"
```

### Step 3: Verify Python Version

Check your Python version:
```batch
python --version
```

**Recommended versions:** Python 3.9, 3.10, 3.11, or 3.12

**Avoid:**
- Python 3.8 (deprecated by many packages)
- Python 3.13 (limited pre-built wheels)

If you have an incompatible version, install a compatible Python version.

---

## Why This Happens

The DLL error occurs for several reasons:

1. **Missing Visual C++ Redistributables** (90% of cases)
   - Matplotlib's C extensions require Microsoft Visual C++ runtime DLLs
   - These are not included with Python by default
   - Solution: Install VC++ Redistributables

2. **Incompatible Package Versions**
   - NumPy built with different compiler than matplotlib expects
   - Mixed 32-bit/64-bit packages
   - Solution: Force reinstall with `--only-binary :all:`

3. **Corrupted Installation**
   - Incomplete download or installation
   - Cached corrupted files
   - Solution: Clear cache and reinstall

4. **Wrong NumPy Build**
   - MINGW-W64 experimental build instead of official Windows binary
   - Solution: Use `--only-binary :all:` flag

---

## Alternative Solutions

### Option A: Use Conda (Recommended for Complex Environments)

If pip continues to have issues, Conda handles C dependencies better on Windows:

```batch
# Install Conda/Miniconda if you haven't
# Download from: https://docs.conda.io/en/latest/miniconda.html

# Create new environment
conda create -n aimp python=3.11
conda activate aimp

# Install packages
conda install numpy scipy matplotlib pandas scikit-learn
conda install pytorch torchvision -c pytorch
pip install -r requirements.txt
```

### Option B: Use Pre-compiled Wheels

Download pre-compiled wheels from Christoph Gohlke's repository:
- https://www.lfd.uci.edu/~gohlke/pythonlibs/

1. Download matplotlib wheel for your Python version
2. Install: `pip install path/to/downloaded/wheel.whl`

### Option C: Downgrade to Known Working Versions

Try these known-working combinations:

**For Python 3.11:**
```batch
pip install numpy==1.26.4
pip install matplotlib==3.8.4
```

**For Python 3.10:**
```batch
pip install numpy==1.24.3
pip install matplotlib==3.7.2
```

---

## Troubleshooting

### Issue: Still getting DLL error after fix script

**Solution:**
1. Install Visual C++ Redistributables: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Restart your computer (required!)
3. Run the fix script again

### Issue: "Could not find a version that satisfies the requirement"

**Solution:**
1. Check Python version: `python --version`
2. Upgrade Python to 3.9-3.12 if needed
3. Upgrade pip: `python -m pip install --upgrade pip`

### Issue: Import works but crashes when creating plots

**Solution:**
```batch
# Install GUI backend for matplotlib
pip install pyqt5
```

Then add to your script:
```python
import matplotlib
matplotlib.use('Qt5Agg')  # Use Qt5 backend
import matplotlib.pyplot as plt
```

### Issue: "ERROR: Failed to build wheel for matplotlib"

**Solution:**
Use pre-built binary only:
```batch
pip install --only-binary :all: matplotlib
```

If that fails, try Conda (Option A above).

---

## Verification

After applying the fix, verify everything works:

```batch
# Test 1: Import matplotlib
python -c "import matplotlib; print('✓ Matplotlib imports')"

# Test 2: Import pyplot
python -c "import matplotlib.pyplot as plt; print('✓ Pyplot imports')"

# Test 3: Create simple plot
python -c "import matplotlib.pyplot as plt; import numpy as np; x = np.linspace(0, 10, 100); plt.plot(x, x**2); print('✓ Plotting works')"

# Test 4: Run your script
python src/data_generator.py
```

All tests should pass without errors.

---

## Prevention

To avoid this issue in future installations:

1. **Always install Visual C++ Redistributables first**
   - Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
   - Install before creating Python virtual environment

2. **Use binary-only installation:**
   ```batch
   pip install --only-binary :all: numpy matplotlib
   ```

3. **Consider using Conda for Windows:**
   - Conda handles C dependencies automatically
   - Pre-compiled packages work better on Windows

4. **Keep packages updated:**
   ```batch
   pip install --upgrade numpy matplotlib scipy
   ```

---

## System Requirements

### Minimum Requirements:
- Windows 7 SP1 or later (Windows 10/11 recommended)
- Python 3.9 - 3.12
- Microsoft Visual C++ 2015-2022 Redistributable
- 64-bit Python (recommended)

### Recommended:
- Windows 10/11 (64-bit)
- Python 3.11 (best package support)
- Latest Visual C++ Redistributables
- At least 4GB RAM

---

## Additional Resources

- **Matplotlib Installation Guide**: https://matplotlib.org/stable/users/installing/index.html
- **Visual C++ Downloads**: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist
- **Python Windows FAQ**: https://docs.python.org/3/using/windows.html
- **Conda Documentation**: https://docs.conda.io/

---

## Quick Reference

| Problem | Solution |
|---------|----------|
| DLL load failed | Install VC++ Redistributables + restart |
| No matching distribution | Upgrade Python to 3.9-3.12 |
| Wheel build failed | Use `--only-binary :all:` flag |
| Still not working | Switch to Conda |

---

**Need immediate help?** Run: `fix_matplotlib_dll_error.bat`

**Still stuck?** Try: Conda installation (Option A)

**Last resort?** Reinstall Python + VC++ Redistributables + restart computer

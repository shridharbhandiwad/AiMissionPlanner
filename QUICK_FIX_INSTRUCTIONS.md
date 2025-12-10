# QUICK FIX: Matplotlib DLL Import Error

## Error You're Seeing

```
ImportError: DLL load failed while importing _c_internal_utils: The specified module could not be found.
```

## FASTEST FIX (Choose One)

---

### ⚡ Option 1: Run the Automated Fix Script (RECOMMENDED - 3 minutes)

1. **Open Command Prompt or PowerShell**

2. **Navigate to your project:**
   ```batch
   cd "D:\Zoppler Projects\AiMissionPlanner"
   ```

3. **Activate your virtual environment:**
   ```batch
   venv\Scripts\activate
   ```

4. **Run the fix script:**
   ```batch
   FIX_MATPLOTLIB_DLL_ERROR_NOW.bat
   ```

5. **Follow any additional instructions** if it prompts you to install Visual C++ Redistributables

---

### 🔧 Option 2: Manual Fix (5 minutes)

If the script doesn't work, do this manually:

#### Step 1: Install Visual C++ Redistributables (MOST IMPORTANT)

This is the #1 cause of the DLL error.

1. **Download from Microsoft:**
   - Direct link: https://aka.ms/vs/17/release/vc_redist.x64.exe
   
2. **Run the installer** (vc_redist.x64.exe)

3. **Restart your computer** (REQUIRED - don't skip this!)

#### Step 2: Reinstall Packages with Binary Wheels

After restarting, open Command Prompt and run:

```batch
cd "D:\Zoppler Projects\AiMissionPlanner"
venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Uninstall problematic packages
pip uninstall -y matplotlib numpy pillow

REM Clear cache
pip cache purge

REM Reinstall with binary wheels only
pip install --only-binary :all: "numpy>=2.0.0,<2.3"
pip install --only-binary :all: matplotlib==3.9.0

REM Test
python -c "import matplotlib.pyplot as plt; print('Success!')"
```

#### Step 3: Test Your Script

```batch
python src/data_generator.py
```

---

### 🐍 Option 3: Switch to Conda (MOST RELIABLE - 10 minutes)

Conda handles Windows DLL dependencies much better than pip.

1. **Download Miniconda:**
   - https://docs.conda.io/en/latest/miniconda.html
   - Choose Python 3.11 version for Windows

2. **Install Miniconda** (follow installer instructions)

3. **Create new environment:**
   ```batch
   conda create -n aimp python=3.11
   conda activate aimp
   ```

4. **Install packages:**
   ```batch
   cd "D:\Zoppler Projects\AiMissionPlanner"
   conda install numpy scipy matplotlib pandas scikit-learn
   conda install pytorch torchvision -c pytorch
   pip install -r requirements.txt
   ```

5. **Test:**
   ```batch
   python src/data_generator.py
   ```

---

## Why This Happens

The error occurs because matplotlib's C extension modules (`_c_internal_utils.pyd`) need specific Windows DLL files that aren't on your system:

1. **Missing Visual C++ Runtime DLLs** (90% of cases)
   - Matplotlib is compiled with Microsoft Visual C++
   - Requires `msvcp140.dll`, `vcruntime140.dll`, etc.
   - **Solution:** Install VC++ Redistributables

2. **Incompatible NumPy Build**
   - NumPy compiled with different compiler than matplotlib
   - **Solution:** Force reinstall with `--only-binary :all:`

3. **Corrupted Installation**
   - Incomplete download or cached corruption
   - **Solution:** Clear cache and reinstall

---

## Verification Steps

After fixing, verify everything works:

```batch
# Test 1: Import matplotlib
python -c "import matplotlib; print('✓ Matplotlib imports')"

# Test 2: Import pyplot
python -c "import matplotlib.pyplot as plt; print('✓ Pyplot imports')"

# Test 3: Test with numpy
python -c "import matplotlib.pyplot as plt; import numpy as np; x = np.linspace(0,10,100); plt.plot(x, x**2); print('✓ Plotting works')"

# Test 4: Run your script
python src/data_generator.py
```

All should pass without errors.

---

## Still Not Working?

### Check Python Version

```batch
python --version
```

**Required:** Python 3.9, 3.10, 3.11, or 3.12

If you have Python 3.8 (too old) or 3.13 (too new), install Python 3.11:
- Download: https://www.python.org/downloads/release/python-3119/
- Install and recreate your virtual environment

### Check System Architecture

```batch
python -c "import platform; print(platform.architecture())"
```

Should show: `('64bit', 'WindowsPE')`

If it shows 32-bit, you need 64-bit Python.

### Last Resort: Complete Reinstall

```batch
# Delete virtual environment
rmdir /s /q venv

# Create fresh virtual environment
python -m venv venv
venv\Scripts\activate

# Install packages fresh
python -m pip install --upgrade pip
pip install --only-binary :all: -r requirements.txt
```

---

## Quick Reference

| Problem | Solution |
|---------|----------|
| DLL load failed | Install VC++ Redistributables + restart |
| No matching distribution | Upgrade Python to 3.9-3.12 |
| Wheel build failed | Use `--only-binary :all:` |
| Still broken after everything | Switch to Conda |

---

## Need Help?

1. Check which step failed in the fix script output
2. Look for specific error messages
3. Verify Python version: `python --version`
4. Verify you're in virtual environment: `echo %VIRTUAL_ENV%`

## Most Common Solution

**90% of cases are fixed by:**
1. Installing Visual C++ Redistributables: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Restarting computer
3. Running the fix script

---

**Start Here:** Run `FIX_MATPLOTLIB_DLL_ERROR_NOW.bat` 

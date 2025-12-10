# Matplotlib DLL Error - Fix Summary

## Problem Identified

You're experiencing this error when running `python src/data_generator.py`:

```
ImportError: DLL load failed while importing _c_internal_utils: The specified module could not be found.
```

This is a **Windows-specific issue** where matplotlib cannot load its C extension DLLs.

## Root Causes

1. **Missing Microsoft Visual C++ Redistributables** (90% of cases)
   - Matplotlib requires Microsoft Visual C++ runtime DLLs
   - These are NOT included with Python
   - Must be installed separately on Windows

2. **Incompatible NumPy/Matplotlib versions**
   - Wrong build of NumPy (MINGW-W64 instead of official Windows binary)
   - Mixed 32-bit/64-bit packages

3. **Corrupted pip cache**
   - Previous failed installations cached
   - Corrupted package files

## Solutions Created

### 🚀 Quick Fix Script (RECOMMENDED)

**File:** `fix_matplotlib_dll_error.bat`

**What it does:**
1. Upgrades pip
2. Uninstalls matplotlib and dependencies
3. Clears pip cache
4. Reinstalls numpy with correct Windows binary
5. Reinstalls matplotlib with all dependencies
6. Verifies the installation works

**How to use:**
```batch
# 1. Activate virtual environment
cd "D:\Zoppler Projects\AiMissionPlanner"
venv\Scripts\activate

# 2. Run fix script
fix_matplotlib_dll_error.bat

# 3. Test
python src/data_generator.py
```

**Time:** 2-3 minutes

### 📖 Documentation Created

1. **FIX_MATPLOTLIB_NOW.txt**
   - Quick reference guide
   - 3-step fix instructions
   - What to do if script doesn't work

2. **MATPLOTLIB_DLL_FIX.md**
   - Comprehensive troubleshooting guide
   - Manual fix instructions
   - Alternative solutions (Conda, pre-built wheels)
   - System requirements
   - Prevention tips

3. **MATPLOTLIB_FIX_SUMMARY.md** (this file)
   - Overview of the problem and solutions

4. **Updated START_HERE.md**
   - Added matplotlib DLL error section
   - Quick fix instructions
   - Links to detailed guides

## Step-by-Step Instructions

### Option 1: Automatic Fix (Easiest)

1. **Open Command Prompt**
   
2. **Navigate to project:**
   ```batch
   cd "D:\Zoppler Projects\AiMissionPlanner"
   ```

3. **Activate virtual environment:**
   ```batch
   venv\Scripts\activate
   ```

4. **Run fix script:**
   ```batch
   fix_matplotlib_dll_error.bat
   ```

5. **Wait for completion** (2-3 minutes)

6. **Test:**
   ```batch
   python src/data_generator.py
   ```

### Option 2: Manual Fix (If Script Fails)

**Step 1: Install Visual C++ Redistributables**
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install the downloaded file
- **Restart your computer** (important!)

**Step 2: Reinstall packages**
```batch
# Activate venv
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Uninstall
pip uninstall -y matplotlib numpy pillow

# Clear cache
pip cache purge

# Reinstall
pip install --only-binary :all: "numpy>=2.0.0,<3.0.0"
pip install --only-binary :all: matplotlib==3.9.0

# Test
python -c "import matplotlib.pyplot as plt; print('Success!')"
```

### Option 3: Use Conda (Alternative)

If pip continues to fail, Conda handles Windows DLLs better:

```batch
# Download Miniconda from:
# https://docs.conda.io/en/latest/miniconda.html

# Create environment
conda create -n aimp python=3.11
conda activate aimp

# Install packages
conda install numpy scipy matplotlib pandas scikit-learn
conda install pytorch torchvision -c pytorch

# Install remaining requirements
pip install -r requirements.txt
```

## What to Do If Fix Doesn't Work

### 1. Install Visual C++ Redistributables

**This is the #1 solution if the script doesn't work.**

1. Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Run the installer
3. **Restart your computer** (required!)
4. Run `fix_matplotlib_dll_error.bat` again

### 2. Check Python Version

```batch
python --version
```

**Supported:** Python 3.9, 3.10, 3.11, 3.12
**Avoid:** Python 3.8 (old), Python 3.13 (too new)

If wrong version, install compatible Python version.

### 3. Try Conda

See Option 3 above. Conda is often more reliable on Windows.

## Verification

After applying fixes, run these tests:

```batch
# Test 1: Basic import
python -c "import matplotlib; print('✓ Matplotlib imports')"

# Test 2: Import pyplot
python -c "import matplotlib.pyplot as plt; print('✓ Pyplot imports')"

# Test 3: Your actual script
python src/data_generator.py
```

All should complete without errors.

## Files Created

```
fix_matplotlib_dll_error.bat    - Automatic fix script
FIX_MATPLOTLIB_NOW.txt         - Quick reference guide
MATPLOTLIB_DLL_FIX.md          - Comprehensive guide
MATPLOTLIB_FIX_SUMMARY.md      - This file
START_HERE.md (updated)        - Added matplotlib fix section
```

## Quick Reference

| Issue | Solution |
|-------|----------|
| DLL load failed | Run `fix_matplotlib_dll_error.bat` |
| Script didn't work | Install VC++ Redistributables + restart |
| Still failing | Try Conda installation |
| Wrong Python version | Install Python 3.9-3.12 |

## Additional Help

1. **Quick start:** `FIX_MATPLOTLIB_NOW.txt`
2. **Detailed guide:** `MATPLOTLIB_DLL_FIX.md`
3. **General help:** `START_HERE.md`
4. **Troubleshooting:** `TROUBLESHOOTING.md`

## Success Path

```
1. Run: fix_matplotlib_dll_error.bat
   ↓
2. If fails → Install VC++ Redistributables → Restart → Try again
   ↓
3. If still fails → Try Conda
   ↓
4. Success! Run: python src/data_generator.py
```

## Why This Is Common on Windows

Unlike Linux/Mac, Windows doesn't include C/C++ runtime libraries by default. Python packages with C extensions (like matplotlib, numpy, scipy) need these DLLs. The fix script ensures:

1. Correct DLLs are present (via VC++ Redistributables)
2. Correct package builds are installed (Windows binaries, not MINGW)
3. No corrupted cached files interfere

## Prevention

For future Python projects on Windows:

1. **Always install VC++ Redistributables first**
2. **Use `--only-binary :all:` when installing scientific packages**
3. **Consider using Conda for complex projects**
4. **Keep packages updated**

## Need More Help?

- **See:** `MATPLOTLIB_DLL_FIX.md` for complete troubleshooting
- **Try:** Conda installation if pip continues to fail
- **Check:** Your Python version is 3.9-3.12

---

## TL;DR - Just Do This

```batch
cd "D:\Zoppler Projects\AiMissionPlanner"
venv\Scripts\activate
fix_matplotlib_dll_error.bat
```

If that doesn't work:
1. Install: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Restart computer
3. Run fix script again

---

**Ready?** Run: `fix_matplotlib_dll_error.bat`

**Need details?** Read: `FIX_MATPLOTLIB_NOW.txt`

**Still stuck?** See: `MATPLOTLIB_DLL_FIX.md`

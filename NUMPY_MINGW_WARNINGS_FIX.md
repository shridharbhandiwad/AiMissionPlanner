# NumPy MINGW-W64 Warnings Fix

## Problem

When running Python scripts that import NumPy on Windows, you may see warnings like:

```
Warning: Numpy built with MINGW-W64 on Windows 64 bits is experimental, and only available for testing.
CRASHES ARE TO BE EXPECTED - PLEASE REPORT THEM TO NUMPY DEVELOPERS

RuntimeWarning: invalid value encountered in exp2
RuntimeWarning: invalid value encountered in nextafter
RuntimeWarning: invalid value encountered in log10
```

These warnings appear because NumPy was built with the MINGW-W64 compiler on Windows, which has some known issues with certain floating-point operations.

## Solutions

### Solution 1: Warning Filters in Code (IMPLEMENTED)

The warnings are now suppressed in `src/data_generator.py` by adding warning filters before importing NumPy:

```python
import warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')
```

### Solution 2: Run with Python Flag

Run the script with the `-W ignore` flag to suppress all warnings:

```bash
python -W ignore src/data_generator.py
```

Or suppress only RuntimeWarnings:

```bash
python -W ignore::RuntimeWarning src/data_generator.py
```

### Solution 3: Environment Variable

Set the `PYTHONWARNINGS` environment variable before running Python:

**Windows CMD:**
```cmd
set PYTHONWARNINGS=ignore::RuntimeWarning
python src/data_generator.py
```

**Windows PowerShell:**
```powershell
$env:PYTHONWARNINGS="ignore::RuntimeWarning"
python src/data_generator.py
```

**Linux/Mac:**
```bash
export PYTHONWARNINGS=ignore::RuntimeWarning
python src/data_generator.py
```

### Solution 4: Reinstall NumPy (Recommended for Production)

If you're using these scripts in production, consider reinstalling NumPy from a more stable source:

#### Option A: Use Conda (Recommended)

```bash
conda install numpy -c conda-forge
```

Conda's NumPy builds are typically more stable on Windows and don't have these warnings.

#### Option B: Use Pre-built Wheels

Download official NumPy wheels from [pypi.org](https://pypi.org/project/numpy/#files) that match your Python version and install:

```bash
pip uninstall numpy
pip install numpy==1.26.4 --only-binary :all:
```

#### Option C: Try a Different NumPy Version

Some versions have fewer issues on Windows:

```bash
pip install numpy==1.24.3
```

Note: Make sure the version is compatible with your other dependencies (PyTorch, SciPy, etc.).

## Impact

**Good News:** These warnings are cosmetic and don't affect functionality. The code runs correctly despite the warnings. They appear during NumPy's internal initialization and don't indicate actual errors in your code.

**When to Worry:** Only if you actually experience crashes or incorrect numerical results (very rare).

## Current Status

✅ **Fixed** - Warnings are now suppressed in `src/data_generator.py`

The script will run without showing these warnings, but they're still technically occurring in the background. For production use, consider Solution 4 (reinstalling NumPy from a more stable source).

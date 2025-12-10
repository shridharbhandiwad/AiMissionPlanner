# NumPy/SciPy Version Conflict Resolution

## Problem

When installing dependencies, you may encounter this error:

```
scipy 1.14.1 requires numpy<2.3,>=1.23.5, but you have numpy 2.3.5 which is incompatible.
```

## Root Cause

The dependency specifications allowed numpy to upgrade to 2.3.5, but scipy 1.14.1 has a maximum version constraint of numpy<2.3. This creates an incompatibility.

### Version Requirements:
- **Python 3.12+**: requires `numpy>=2.0.0`
- **scipy 1.14.1**: requires `numpy>=1.23.5,<2.3`
- **Original requirements**: specified `numpy>=2.0.0,<3.0.0` (too permissive)

## Solution

Update the numpy version constraint to satisfy both Python 3.12+ and scipy 1.14.1:

```
numpy>=2.0.0,<2.3
```

This ensures:
- ✓ Compatible with Python 3.12+ (requires numpy 2.x)
- ✓ Compatible with scipy 1.14.1 (requires numpy<2.3)
- ✓ Gets latest stable NumPy 2.2.x releases

## Quick Fix

### Windows
Run the automated fix script:
```batch
fix_scipy_numpy_conflict.bat
```

Or manually:
```batch
pip uninstall -y numpy
pip cache remove numpy
pip install "numpy>=2.0.0,<2.3"
```

### Linux/Mac
Run the automated fix script:
```bash
./fix_scipy_numpy_conflict.sh
```

Or manually:
```bash
pip uninstall -y numpy
pip cache remove numpy
pip install "numpy>=2.0.0,<2.3"
```

## Files Updated

All installation and requirement files have been updated with the correct numpy version constraint:

1. **requirements.txt** - Updated to `numpy>=2.0.0,<2.3`
2. **requirements-windows.txt** - Updated to `numpy>=2.0.0,<2.3`
3. **fix_numpy_windows.bat** - Updated installation commands
4. **fix_all_dependencies.bat** - Updated installation commands
5. **install_windows.bat** - Updated installation commands
6. **install_linux.sh** - Updated installation commands

## Verification

After applying the fix, verify both packages are working:

```python
python -c "import numpy; import scipy; print('NumPy:', numpy.__version__); print('SciPy:', scipy.__version__)"
```

Expected output:
```
NumPy: 2.2.x
SciPy: 1.14.1
```

## Alternative Solutions

If you still encounter issues, you can:

1. **Upgrade scipy** (if a newer version supporting numpy 2.3+ is available):
   ```bash
   pip install --upgrade scipy
   ```

2. **Use conda** (better dependency resolution):
   ```bash
   conda install numpy scipy
   ```

## Related Issues

This issue can also manifest as:
- Import errors when using scipy functions
- Runtime warnings about numpy version incompatibility
- Crashes in scientific computing operations

## Date Fixed
December 10, 2025

## Additional Notes

- NumPy 2.2.x is fully compatible with Python 3.12+ and all other project dependencies
- This constraint will remain valid until scipy releases a version supporting numpy 2.3+
- The issue was caused by the original requirements being too permissive with the numpy version range

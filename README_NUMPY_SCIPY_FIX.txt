================================================================================
NUMPY/SCIPY VERSION CONFLICT - QUICK FIX GUIDE
================================================================================

DATE: December 10, 2025
STATUS: RESOLVED

--------------------------------------------------------------------------------
PROBLEM
--------------------------------------------------------------------------------

You saw this error during pip installation:

  "scipy 1.14.1 requires numpy<2.3,>=1.23.5, but you have numpy 2.3.5 
   which is incompatible."

This means numpy 2.3.5 was installed, but scipy 1.14.1 only supports 
numpy versions below 2.3.

--------------------------------------------------------------------------------
SOLUTION - CHOOSE ONE:
--------------------------------------------------------------------------------

OPTION 1: Automated Fix (RECOMMENDED)
--------------------------------------

Windows:
  > fix_scipy_numpy_conflict.bat

Linux/Mac:
  $ ./fix_scipy_numpy_conflict.sh


OPTION 2: Manual Fix
--------------------

1. Uninstall numpy:
   pip uninstall -y numpy

2. Clear cache:
   pip cache remove numpy

3. Install compatible version:
   pip install "numpy>=2.0.0,<2.3"

4. Verify:
   python verify_numpy_scipy.py


OPTION 3: Complete Reinstall
-----------------------------

Windows:
  > install_windows.bat

Linux/Mac:
  $ ./install_linux.sh

--------------------------------------------------------------------------------
VERIFICATION
--------------------------------------------------------------------------------

Run this command to verify the fix:

  python verify_numpy_scipy.py

Or manually check versions:

  python -c "import numpy, scipy; print('NumPy:', numpy.__version__); print('SciPy:', scipy.__version__)"

Expected output:
  NumPy: 2.2.x (any version from 2.0.0 to 2.2.x)
  SciPy: 1.14.1

--------------------------------------------------------------------------------
WHY THIS HAPPENED
--------------------------------------------------------------------------------

- Python 3.12+ requires numpy >= 2.0.0
- scipy 1.14.1 requires numpy < 2.3
- Old requirements allowed numpy < 3.0 (too broad)
- pip installed numpy 2.3.5 (latest available)
- This created a version conflict

--------------------------------------------------------------------------------
WHAT WAS FIXED
--------------------------------------------------------------------------------

All dependency files now specify: numpy>=2.0.0,<2.3

Files updated:
  ✓ requirements.txt
  ✓ requirements-windows.txt
  ✓ All installation scripts (.bat and .sh)
  ✓ All fix scripts
  ✓ All documentation

New files created:
  ✓ fix_scipy_numpy_conflict.bat (Windows fix script)
  ✓ fix_scipy_numpy_conflict.sh (Linux/Mac fix script)
  ✓ verify_numpy_scipy.py (Verification script)
  ✓ SCIPY_NUMPY_CONFLICT_FIX.md (Detailed guide)
  ✓ DEPENDENCY_FIX_COMPLETE.md (Complete summary)

--------------------------------------------------------------------------------
NEED MORE HELP?
--------------------------------------------------------------------------------

See these files for detailed information:

  SCIPY_NUMPY_CONFLICT_FIX.md  - Complete troubleshooting guide
  DEPENDENCY_FIX_COMPLETE.md   - Full technical summary
  NUMPY_VERSION_FIX.md         - NumPy version information

Or run the diagnosis:
  python diagnose_numpy.py

--------------------------------------------------------------------------------
AFTER FIXING
--------------------------------------------------------------------------------

You can now run the trajectory GUI:
  python run_trajectory_gui.py

Or continue with your development work - all dependencies should now work
correctly together!

================================================================================

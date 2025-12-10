================================================================================
  SILENT EXIT FIX - QUICK REFERENCE
================================================================================

PROBLEM: App exits silently after "Checking NumPy..." with no error message

SOLUTION: Use the Safe Launcher to see the actual error!

================================================================================
  WHAT TO DO RIGHT NOW (Windows)
================================================================================

Double-click one of these:

  1. fix_gui.bat                      <- Interactive menu (EASIEST)
  2. run_trajectory_gui_safe.bat      <- Safe launcher
  3. diagnose_numpy.bat               <- NumPy diagnostics

================================================================================
  WHAT TO DO RIGHT NOW (Command Line)
================================================================================

Run one of these:

  1. python run_trajectory_gui_safe.py    <- Safe launcher (RECOMMENDED)
  2. python diagnose_numpy.py             <- NumPy diagnostics
  3. python diagnose_gui_startup.py       <- Full diagnostics

================================================================================
  MOST COMMON FIX (Windows)
================================================================================

Install Visual C++ Redistributables:
  https://aka.ms/vs/17/release/vc_redist.x64.exe

Then reinstall NumPy:
  pip uninstall -y numpy
  pip cache purge
  conda install -c conda-forge numpy

================================================================================
  DOCUMENTATION
================================================================================

Quick Start:    START_HERE_SILENT_EXIT_FIX.md
Quick Ref:      QUICK_FIX_SILENT_EXIT.md
Full Guide:     FIX_SILENT_EXIT.md
Technical:      SOLUTION_SILENT_EXIT.md

================================================================================
  NEW TOOLS CREATED
================================================================================

run_trajectory_gui_safe.py    <- Catches crashes (USE THIS!)
diagnose_numpy.py              <- Tests NumPy specifically
fix_gui.bat                    <- Interactive menu (Windows)

================================================================================
  QUICK TEST
================================================================================

Test if NumPy works:
  python -c "import numpy; print('NumPy OK:', numpy.__version__)"

If that works, run:
  python run_trajectory_gui_safe.py

================================================================================

TIP: The safe launcher tests imports in subprocesses so crashes don't
     kill the entire app. It will show you EXACTLY what's wrong!

================================================================================

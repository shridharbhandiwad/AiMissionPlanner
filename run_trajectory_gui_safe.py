#!/usr/bin/env python3
"""
Safe launcher script for 3D Trajectory Generator GUI
This version tests dependencies in subprocesses to catch hard crashes
"""

import sys
import os
import subprocess

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_import_safe(module_name, import_code):
    """
    Test an import in a subprocess to catch hard crashes
    Returns (success, error_message)
    """
    test_script = f"""
import sys
import warnings
warnings.filterwarnings('ignore')
try:
    {import_code}
    print("SUCCESS")
    sys.exit(0)
except Exception as e:
    print(f"ERROR: {{type(e).__name__}}: {{e}}")
    sys.exit(1)
"""
    
    try:
        result = subprocess.run(
            [sys.executable, '-c', test_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and "SUCCESS" in result.stdout:
            return True, None
        elif result.returncode != 0:
            error = result.stdout.strip() or result.stderr.strip()
            return False, error
        else:
            return False, "Unknown error"
    except subprocess.TimeoutExpired:
        return False, "Import timed out (possible hang)"
    except Exception as e:
        return False, f"Subprocess error: {e}"

if __name__ == '__main__':
    print("="*60)
    print("3D Trajectory Generator GUI (Safe Mode)")
    print("="*60)
    print("\nStarting application...")
    print("\nFeatures:")
    print("  - 12 different trajectory types")
    print("  - Real-time 3D visualization")
    print("  - Customizable physical constraints")
    print("  - Trajectory metrics calculation")
    print("  - Save/load functionality")
    print("\n" + "="*60 + "\n")
    
    print("Checking dependencies (safe mode)...")
    print("(Testing each dependency in isolated subprocess)\n")
    
    all_deps_ok = True
    
    # Test NumPy
    print("  [1/5] Checking NumPy...", end=" ")
    sys.stdout.flush()
    success, error = test_import_safe("numpy", "import numpy")
    if success:
        print("✓")
    else:
        print(f"✗\n  Error: {error}")
        all_deps_ok = False
    
    # Test PyQt5
    print("  [2/5] Checking PyQt5...", end=" ")
    sys.stdout.flush()
    success, error = test_import_safe("PyQt5", "from PyQt5 import QtWidgets, QtCore, QtGui")
    if success:
        print("✓")
    else:
        print(f"✗\n  Error: {error}")
        print("\n  Please install PyQt5:")
        print("    pip install PyQt5")
        all_deps_ok = False
    
    # Test PyQtGraph
    print("  [3/5] Checking PyQtGraph...", end=" ")
    sys.stdout.flush()
    success, error = test_import_safe("pyqtgraph", "import pyqtgraph")
    if success:
        print("✓")
    else:
        print(f"✗\n  Error: {error}")
        print("\n  Please install PyQtGraph:")
        print("    pip install pyqtgraph")
        all_deps_ok = False
    
    # Test PyQtGraph OpenGL
    print("  [4/5] Checking PyQtGraph OpenGL...", end=" ")
    sys.stdout.flush()
    success, error = test_import_safe("pyqtgraph.opengl", "import pyqtgraph.opengl")
    if success:
        print("✓")
    else:
        print(f"✗\n  Error: {error}")
        print("\n  Please install PyOpenGL:")
        print("    pip install PyOpenGL PyOpenGL_accelerate")
        all_deps_ok = False
    
    # Test SciPy
    print("  [5/5] Checking SciPy...", end=" ")
    sys.stdout.flush()
    success, error = test_import_safe("scipy", "from scipy.interpolate import CubicSpline")
    if success:
        print("✓")
    else:
        print(f"✗\n  Error: {error}")
        print("\n  Please install SciPy:")
        print("    pip install scipy")
        all_deps_ok = False
    
    print()
    
    if not all_deps_ok:
        print("="*60)
        print("DEPENDENCY CHECK FAILED")
        print("="*60)
        print("\nSome dependencies are missing or not working correctly.")
        print("\nTo diagnose specific issues, run:")
        print("  python diagnose_numpy.py        (for NumPy issues)")
        print("  python diagnose_gui_startup.py  (for all dependencies)")
        print("\nTo test basic PyQt5 functionality, run:")
        print("  python test_basic_gui.py")
        print("\n" + "="*60)
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("All dependencies found!")
    print()
    print("Now loading dependencies normally...")
    print()
    
    # Now import for real since tests passed
    try:
        print("  - Importing NumPy...")
        sys.stdout.flush()
        import numpy
        print("    ✓")
        
        print("  - Importing PyQt5...")
        sys.stdout.flush()
        from PyQt5 import QtWidgets, QtCore, QtGui
        print("    ✓")
        
        print("  - Importing PyQtGraph...")
        sys.stdout.flush()
        import pyqtgraph
        print("    ✓")
        
        print("  - Importing PyQtGraph OpenGL...")
        sys.stdout.flush()
        import pyqtgraph.opengl
        print("    ✓")
        
        print("  - Importing SciPy...")
        sys.stdout.flush()
        from scipy.interpolate import CubicSpline
        print("    ✓")
        
        print()
        print("Initializing GUI...")
        print("  - Importing trajectory_gui module...")
        sys.stdout.flush()
        
        from trajectory_gui import main
        print("  - Module imported successfully")
        print("  - Starting main GUI application...")
        sys.stdout.flush()
        main()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except SystemExit as e:
        if e.code == 0:
            print("\nApplication closed normally.")
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print("ERROR: Failed to start GUI")
        print(f"{'='*60}")
        print(f"\nError type: {type(e).__name__}")
        print(f"Error details: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        print(f"\n{'='*60}")
        print("\nPossible causes:")
        print("  1. OpenGL/graphics driver issue")
        print("  2. Display environment not configured (Linux)")
        print("  3. Missing Qt platform plugin")
        print("  4. Incompatible PyQt5/PyQtGraph versions")
        print("\nFor more diagnostics, run:")
        print("  python diagnose_gui_startup.py")
        print(f"\n{'='*60}")
        input("\nPress Enter to exit...")
        sys.exit(1)

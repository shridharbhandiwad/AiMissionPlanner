#!/usr/bin/env python3
"""
Launcher script for 3D Trajectory Generator GUI
"""

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings

# Filter warnings before NumPy import to suppress MINGW-W64 build warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == '__main__':
    print("="*60)
    print("3D Trajectory Generator GUI")
    print("="*60)
    print("\nStarting application...")
    print("\nFeatures:")
    print("  - 12 different trajectory types")
    print("  - Real-time 3D visualization")
    print("  - Customizable physical constraints")
    print("  - Trajectory metrics calculation")
    print("  - Save/load functionality")
    print("\n" + "="*60 + "\n")
    
    # Check dependencies
    print("Checking dependencies...")
    print()
    
    all_deps_ok = True
    
    try:
        print("  [1/5] Checking NumPy...", end=" ")
        sys.stdout.flush()
        import numpy
        print("✓")
        sys.stdout.flush()
    except ImportError as e:
        print(f"✗\n  Error: {e}")
        sys.stdout.flush()
        all_deps_ok = False
    except Exception as e:
        print(f"✗\n  Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        all_deps_ok = False
    
    try:
        print("  [2/5] Checking PyQt5...", end=" ")
        sys.stdout.flush()
        from PyQt5 import QtWidgets, QtCore, QtGui
        print("✓")
    except ImportError as e:
        print(f"✗\n  Error: {e}")
        print("\n  Please install PyQt5:")
        print("    pip install PyQt5")
        all_deps_ok = False
    except Exception as e:
        print(f"✗\n  Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        all_deps_ok = False
    
    try:
        print("  [3/5] Checking PyQtGraph...", end=" ")
        sys.stdout.flush()
        import pyqtgraph
        print("✓")
    except ImportError as e:
        print(f"✗\n  Error: {e}")
        print("\n  Please install PyQtGraph:")
        print("    pip install pyqtgraph")
        all_deps_ok = False
    except Exception as e:
        print(f"✗\n  Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        all_deps_ok = False
    
    try:
        print("  [4/5] Checking PyQtGraph OpenGL...", end=" ")
        sys.stdout.flush()
        import pyqtgraph.opengl
        print("✓")
    except ImportError as e:
        print(f"✗\n  Error: {e}")
        print("\n  Please install PyOpenGL:")
        print("    pip install PyOpenGL PyOpenGL_accelerate")
        all_deps_ok = False
    except Exception as e:
        print(f"✗\n  Unexpected error during OpenGL import: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("\n  This might be an OpenGL driver or compatibility issue.")
        print("  Try running: python diagnose_gui_startup.py")
        all_deps_ok = False
    
    try:
        print("  [5/5] Checking SciPy...", end=" ")
        sys.stdout.flush()
        from scipy.interpolate import CubicSpline
        print("✓")
    except ImportError as e:
        print(f"✗\n  Error: {e}")
        print("\n  Please install SciPy:")
        print("    pip install scipy")
        all_deps_ok = False
    except Exception as e:
        print(f"✗\n  Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        all_deps_ok = False
    
    print()
    
    if not all_deps_ok:
        print("="*60)
        print("DEPENDENCY CHECK FAILED")
        print("="*60)
        print("\nSome dependencies are missing or not working correctly.")
        print("\nTo diagnose the issue, run:")
        print("  python diagnose_gui_startup.py")
        print("\nTo test basic PyQt5 functionality, run:")
        print("  python test_basic_gui.py")
        print("\n" + "="*60)
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("All dependencies found!")
    print()
    print("Initializing GUI...")
    print("  - Importing trajectory_gui module...")
    sys.stdout.flush()
    
    try:
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

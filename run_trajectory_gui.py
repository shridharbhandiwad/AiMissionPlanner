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
    try:
        import numpy
        print("  ✓ NumPy installed")
    except ImportError as e:
        print(f"  ✗ NumPy not found: {e}")
        sys.exit(1)
    
    try:
        from PyQt5 import QtWidgets, QtCore, QtGui
        print("  ✓ PyQt5 installed")
    except ImportError as e:
        print(f"  ✗ PyQt5 not found: {e}")
        print("\nPlease install PyQt5:")
        print("  pip install PyQt5")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    try:
        import pyqtgraph
        print("  ✓ PyQtGraph installed")
    except ImportError as e:
        print(f"  ✗ PyQtGraph not found: {e}")
        print("\nPlease install PyQtGraph:")
        print("  pip install pyqtgraph")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    try:
        import pyqtgraph.opengl
        print("  ✓ PyQtGraph OpenGL support")
    except ImportError as e:
        print(f"  ✗ PyQtGraph OpenGL not found: {e}")
        print("\nPlease install PyOpenGL:")
        print("  pip install PyOpenGL PyOpenGL_accelerate")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    try:
        from scipy.interpolate import CubicSpline
        print("  ✓ SciPy installed")
    except ImportError as e:
        print(f"  ✗ SciPy not found: {e}")
        print("\nPlease install SciPy:")
        print("  pip install scipy")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("\nAll dependencies found!")
    print("\nInitializing GUI...")
    
    try:
        from trajectory_gui import main
        main()
    except Exception as e:
        print(f"\n{'='*60}")
        print("ERROR: Failed to start GUI")
        print(f"{'='*60}")
        print(f"\nError details: {e}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        print(f"\n{'='*60}")
        input("\nPress Enter to exit...")
        sys.exit(1)

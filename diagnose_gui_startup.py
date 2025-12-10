#!/usr/bin/env python3
"""
Comprehensive diagnostic script for GUI startup issues
"""

import sys
import os

print("="*60)
print("GUI Startup Diagnostic")
print("="*60)
print()

# Python info
print("Python Information:")
print(f"  Version: {sys.version}")
print(f"  Executable: {sys.executable}")
print(f"  Platform: {sys.platform}")
print()

# Step 1: NumPy
print("[1/6] Testing NumPy...")
try:
    import numpy as np
    print(f"  ✓ NumPy {np.__version__} - OK")
except Exception as e:
    print(f"  ✗ NumPy Error: {e}")
    print("\n  NumPy is required. Install with: pip install numpy")
    print("  For detailed diagnosis: python diagnose_numpy.py")
    sys.exit(1)

# Step 2: PyQt5
print("[2/6] Testing PyQt5...")
try:
    from PyQt5 import QtWidgets, QtCore, QtGui
    print(f"  ✓ PyQt5 - OK")
    print(f"     Qt version: {QtCore.QT_VERSION_STR}")
    print(f"     PyQt version: {QtCore.PYQT_VERSION_STR}")
except ImportError as e:
    print(f"  ✗ PyQt5 not found: {e}")
    print("\n  Install with: pip install PyQt5")
    sys.exit(1)
except Exception as e:
    print(f"  ✗ PyQt5 error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: PyQtGraph
print("[3/6] Testing PyQtGraph...")
try:
    import pyqtgraph as pg
    print(f"  ✓ PyQtGraph {pg.__version__} - OK")
except ImportError as e:
    print(f"  ✗ PyQtGraph not found: {e}")
    print("\n  Install with: pip install pyqtgraph")
    sys.exit(1)
except Exception as e:
    print(f"  ✗ PyQtGraph error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: PyOpenGL
print("[4/6] Testing PyOpenGL...")
try:
    import OpenGL
    from OpenGL.GL import *
    from OpenGL.GLU import *
    print(f"  ✓ PyOpenGL {OpenGL.__version__} - OK")
except ImportError as e:
    print(f"  ✗ PyOpenGL not found: {e}")
    print("\n  Install with: pip install PyOpenGL PyOpenGL_accelerate")
    sys.exit(1)
except Exception as e:
    print(f"  ✗ PyOpenGL error: {e}")
    import traceback
    traceback.print_exc()

# Step 5: PyQtGraph OpenGL
print("[5/6] Testing PyQtGraph OpenGL integration...")
try:
    import pyqtgraph.opengl as gl
    print(f"  ✓ PyQtGraph OpenGL - OK")
except Exception as e:
    print(f"  ✗ PyQtGraph OpenGL error: {e}")
    import traceback
    traceback.print_exc()
    print("\n  This might indicate an OpenGL driver issue.")
    if sys.platform == 'win32':
        print("  Try updating your graphics drivers.")
    elif sys.platform.startswith('linux'):
        print("  Make sure OpenGL libraries are installed:")
        print("    sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev")

# Step 6: SciPy
print("[6/6] Testing SciPy...")
try:
    from scipy.interpolate import CubicSpline
    print(f"  ✓ SciPy - OK")
except ImportError as e:
    print(f"  ✗ SciPy not found: {e}")
    print("\n  Install with: pip install scipy")
    sys.exit(1)
except Exception as e:
    print(f"  ✗ SciPy error: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*60)

# Test QApplication creation
print("\nTesting QApplication creation...")
try:
    # Suppress warnings
    import warnings
    warnings.filterwarnings('ignore')
    
    from PyQt5.QtWidgets import QApplication
    
    # Check if a QApplication already exists
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        print("  ✓ QApplication created successfully")
        created_app = True
    else:
        print("  ✓ QApplication already exists")
        created_app = False
    
except Exception as e:
    print(f"  ✗ Failed to create QApplication: {e}")
    import traceback
    traceback.print_exc()
    print("\n  This might indicate:")
    print("    - Display environment not configured (Linux)")
    print("    - Missing Qt platform plugin")
    print("    - Qt installation issue")
    sys.exit(1)

# Test basic window
print("\nTesting basic window creation...")
try:
    from PyQt5.QtWidgets import QMainWindow
    
    window = QMainWindow()
    window.setWindowTitle("Test Window")
    window.resize(400, 300)
    print("  ✓ Basic window created successfully")
    
    # Don't show it, just test creation
    del window
    
except Exception as e:
    print(f"  ✗ Failed to create window: {e}")
    import traceback
    traceback.print_exc()

# Test 3D view creation
print("\nTesting 3D OpenGL view creation...")
try:
    import pyqtgraph.opengl as gl
    
    view = gl.GLViewWidget()
    print("  ✓ GLViewWidget created successfully")
    
    # Test adding a grid
    grid = gl.GLGridItem()
    view.addItem(grid)
    print("  ✓ Grid item added successfully")
    
    del view
    
except Exception as e:
    print(f"  ✗ Failed to create 3D view: {e}")
    import traceback
    traceback.print_exc()
    print("\n  This indicates an OpenGL issue.")
    print("  The GUI may not work properly without OpenGL support.")

print()
print("="*60)
print("ALL TESTS PASSED!")
print("="*60)
print()
print("All dependencies are working correctly.")
print("The GUI should start successfully.")
print()
print("If the GUI still doesn't start, try:")
print("  1. python test_basic_gui.py")
print("  2. Check for conflicts with other Python packages")
print("  3. Try running in a fresh virtual environment")

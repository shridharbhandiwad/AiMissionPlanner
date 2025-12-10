#!/usr/bin/env python3
"""
Diagnostic script to identify GUI startup issues
"""

import sys
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

print("="*60)
print("GUI Startup Diagnostics")
print("="*60)
print()

def test_import(module_name, import_statement):
    """Test an import and report status"""
    print(f"Testing: {module_name}...")
    try:
        exec(import_statement)
        print(f"  ✓ SUCCESS: {module_name}")
        return True
    except ImportError as e:
        print(f"  ✗ IMPORT ERROR: {e}")
        return False
    except Exception as e:
        print(f"  ✗ RUNTIME ERROR: {type(e).__name__}: {e}")
        import traceback
        print("  Full traceback:")
        traceback.print_exc()
        return False

# Test each dependency
print("1. Testing NumPy...")
success_numpy = test_import("numpy", "import numpy")
print()

print("2. Testing PyQt5...")
success_pyqt5 = test_import("PyQt5", "from PyQt5 import QtWidgets, QtCore, QtGui")
print()

print("3. Testing PyQtGraph...")
success_pyqtgraph = test_import("pyqtgraph", "import pyqtgraph")
print()

print("4. Testing PyQtGraph OpenGL...")
success_pyqtgraph_gl = test_import("pyqtgraph.opengl", "import pyqtgraph.opengl as gl")
print()

if success_pyqtgraph_gl:
    print("5. Testing PyQtGraph OpenGL classes...")
    try:
        import pyqtgraph.opengl as gl
        print(f"  - GLViewWidget: {hasattr(gl, 'GLViewWidget')}")
        print(f"  - GLLinePlotItem: {hasattr(gl, 'GLLinePlotItem')}")
        print(f"  - GLScatterPlotItem: {hasattr(gl, 'GLScatterPlotItem')}")
        print(f"  - GLGridItem: {hasattr(gl, 'GLGridItem')}")
        
        # Try to create a QApplication and GLViewWidget
        print("\n  Testing GLViewWidget instantiation...")
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        view = gl.GLViewWidget()
        print(f"  ✓ GLViewWidget created successfully!")
        app.quit()
    except Exception as e:
        print(f"  ✗ ERROR during OpenGL testing: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
print()

print("6. Testing PyOpenGL...")
success_pyopengl = test_import("OpenGL", "import OpenGL.GL")
print()

print("7. Testing SciPy...")
success_scipy = test_import("scipy", "from scipy.interpolate import CubicSpline")
print()

print("="*60)
print("Summary")
print("="*60)
print(f"NumPy: {'✓' if success_numpy else '✗'}")
print(f"PyQt5: {'✓' if success_pyqt5 else '✗'}")
print(f"PyQtGraph: {'✓' if success_pyqtgraph else '✗'}")
print(f"PyQtGraph OpenGL: {'✓' if success_pyqtgraph_gl else '✗'}")
print(f"PyOpenGL: {'✓' if success_pyopengl else '✗'}")
print(f"SciPy: {'✓' if success_scipy else '✗'}")
print()

if all([success_numpy, success_pyqt5, success_pyqtgraph, success_pyqtgraph_gl, success_scipy]):
    print("All dependencies are working correctly!")
    print("\nThe issue might be with:")
    print("  1. OpenGL driver/hardware support")
    print("  2. Display environment variables (DISPLAY on Linux)")
    print("  3. PyQt5 platform plugin issues")
    print("\nTrying to get more information...")
    
    # Check OpenGL info
    try:
        print("\nOpenGL Information:")
        from PyQt5.QtWidgets import QApplication
        import pyqtgraph.opengl as gl
        app = QApplication(sys.argv)
        
        # Try to query OpenGL version
        import OpenGL.GL as ogl
        view = gl.GLViewWidget()
        view.show()
        
        # Force OpenGL context creation
        view.paintGL()
        
        print(f"  OpenGL Vendor: {ogl.glGetString(ogl.GL_VENDOR)}")
        print(f"  OpenGL Renderer: {ogl.glGetString(ogl.GL_RENDERER)}")
        print(f"  OpenGL Version: {ogl.glGetString(ogl.GL_VERSION)}")
        
        app.quit()
    except Exception as e:
        print(f"  Could not retrieve OpenGL info: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Some dependencies are missing or not working correctly.")
    print("Please install missing dependencies.")

print("\n" + "="*60)
print("Diagnostic complete!")
print("="*60)

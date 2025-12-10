#!/usr/bin/env python3
"""
Installation Verification Script
Tests all dependencies and provides a clear pass/fail report
"""

import sys
import subprocess

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")

def test_import(name, import_statement, version_statement=None):
    """Test if a package can be imported"""
    print(f"Testing {name}...", end=" ")
    sys.stdout.flush()
    
    try:
        # Test in subprocess to catch fatal errors
        result = subprocess.run(
            [sys.executable, '-c', import_statement],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print("✗ FAILED")
            if result.stderr:
                print(f"  Error: {result.stderr.strip()[:200]}")
            return False
        
        # Get version if requested
        version = "OK"
        if version_statement:
            result = subprocess.run(
                [sys.executable, '-c', version_statement],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
        
        print(f"✓ PASSED ({version})")
        return True
        
    except subprocess.TimeoutExpired:
        print("✗ TIMEOUT")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    print_header("Installation Verification")
    
    print("This script tests all required dependencies for the GUI.\n")
    
    results = {}
    
    # Test Python version
    print(f"Python Version: {sys.version}")
    python_version = sys.version_info
    if python_version.major == 3 and 9 <= python_version.minor <= 12:
        print("  ✓ Python version is compatible (3.9-3.12)")
        results['python'] = True
    elif python_version.major == 3 and python_version.minor == 13:
        print("  ⚠ Python 3.13 detected - some packages may have limited support")
        results['python'] = True
    else:
        print("  ⚠ Python version may have compatibility issues")
        results['python'] = False
    
    print("\n" + "-" * 70 + "\n")
    
    # Test core dependencies
    print("Testing Core Dependencies:\n")
    
    results['numpy'] = test_import(
        "NumPy",
        "import numpy",
        "import numpy; print(numpy.__version__)"
    )
    
    results['scipy'] = test_import(
        "SciPy",
        "from scipy.interpolate import CubicSpline",
        "import scipy; print(scipy.__version__)"
    )
    
    results['torch'] = test_import(
        "PyTorch",
        "import torch",
        "import torch; print(torch.__version__)"
    )
    
    # Test GUI dependencies
    print("\n" + "-" * 70 + "\n")
    print("Testing GUI Dependencies:\n")
    
    results['pyqt5'] = test_import(
        "PyQt5",
        "from PyQt5 import QtWidgets, QtCore, QtGui",
        "from PyQt5 import QtCore; print(QtCore.QT_VERSION_STR)"
    )
    
    results['pyqtgraph'] = test_import(
        "PyQtGraph",
        "import pyqtgraph",
        "import pyqtgraph; print(pyqtgraph.__version__)"
    )
    
    results['pyopengl'] = test_import(
        "PyOpenGL",
        "import OpenGL",
        "import OpenGL; print(OpenGL.__version__)"
    )
    
    results['pyqtgraph_gl'] = test_import(
        "PyQtGraph OpenGL",
        "import pyqtgraph.opengl as gl"
    )
    
    # Test visualization dependencies
    print("\n" + "-" * 70 + "\n")
    print("Testing Visualization Dependencies:\n")
    
    results['matplotlib'] = test_import(
        "Matplotlib",
        "import matplotlib",
        "import matplotlib; print(matplotlib.__version__)"
    )
    
    # Summary
    print("\n" + "=" * 70 + "\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Results: {passed}/{total} tests passed\n")
    
    if passed == total:
        print_header("✓ ALL TESTS PASSED!")
        print("Your installation is complete and working correctly.")
        print("\nYou can now run the trajectory GUI:")
        print("  python run_trajectory_gui.py")
        print("\nOr try the examples:")
        print("  python examples/trajectory_gui_examples.py")
        return 0
    else:
        print_header("✗ SOME TESTS FAILED")
        print("Your installation has issues that need to be fixed.\n")
        
        # Provide specific guidance
        failed = [name for name, passed in results.items() if not passed]
        
        print("Failed components:")
        for name in failed:
            print(f"  ✗ {name}")
        
        print("\nRecommended fixes:\n")
        
        if any(name in failed for name in ['pyqt5', 'pyqtgraph', 'pyopengl', 'pyqtgraph_gl']):
            print("GUI packages failed:")
            print("  Windows:  fix_gui_dependencies.bat")
            print("  Linux:    ./fix_gui_dependencies.sh")
            print("  Manual:   pip install PyQt5 PyQtGraph PyOpenGL")
            print()
        
        if 'numpy' in failed:
            print("NumPy failed:")
            print("  Windows:  fix_numpy_windows.bat")
            print("  Manual:   pip install --only-binary :all: numpy")
            print()
        
        if any(name in failed for name in ['scipy', 'torch', 'matplotlib']):
            print("Core packages failed:")
            print("  Windows:  install_windows.bat")
            print("  Linux:    ./install_linux.sh")
            print("  Manual:   pip install -r requirements.txt")
            print()
        
        print("For comprehensive fix:")
        print("  Windows:  fix_all_dependencies.bat")
        print("  See also: WINDOWS_GUI_FIX.md")
        
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)

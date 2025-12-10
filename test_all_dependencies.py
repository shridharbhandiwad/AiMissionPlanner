#!/usr/bin/env python3
"""
Comprehensive dependency test for trajectory GUI
Tests all required dependencies in safe, isolated manner
"""

import sys
import subprocess
import time

def test_import(module_name, import_statement, test_name):
    """Test a single import in isolated subprocess"""
    print(f"  Checking {test_name}...", end=' ')
    
    code = f"""
import sys
import warnings
warnings.filterwarnings('ignore')
{import_statement}
print('OK')
"""
    
    try:
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and 'OK' in result.stdout:
            print('✓')
            return True
        else:
            print('✗')
            if result.stderr:
                print(f"    Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print('✗ (timeout)')
        return False
    except Exception as e:
        print(f'✗ ({e})')
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("COMPREHENSIVE DEPENDENCY CHECK")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Test 1: NumPy
    if not test_import('numpy', 'import numpy; print(numpy.__version__)', 'NumPy'):
        all_passed = False
        print("    Install: pip install numpy")
    
    # Test 2: SciPy
    if not test_import('scipy', 'import scipy; print(scipy.__version__)', 'SciPy'):
        all_passed = False
        print("    Install: pip install scipy")
    
    # Test 3: PyQt5
    if not test_import('PyQt5', 'from PyQt5.QtWidgets import QApplication', 'PyQt5'):
        all_passed = False
        print("    Install: pip install PyQt5")
    
    # Test 4: PyQtGraph
    if not test_import('pyqtgraph', 'import pyqtgraph; print(pyqtgraph.__version__)', 'PyQtGraph'):
        all_passed = False
        print("    Install: pip install pyqtgraph")
    
    # Test 5: PyQtGraph OpenGL
    if not test_import('pyqtgraph.opengl', 'import pyqtgraph.opengl as gl', 'PyQtGraph OpenGL'):
        all_passed = False
        print("    Install: pip install PyOpenGL PyOpenGL_accelerate")
    
    # Test 6: SciPy interpolate
    if not test_import('scipy.interpolate', 'from scipy.interpolate import CubicSpline', 'SciPy interpolate'):
        all_passed = False
        print("    Install: pip install scipy")
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("✓ ALL DEPENDENCIES INSTALLED AND WORKING!")
        print("=" * 60)
        print()
        print("You can now run the GUI with:")
        print("  python3 src/trajectory_gui.py")
        print()
        print("Or use the helper script:")
        print("  ./run_trajectory_gui.sh")
        print()
        return 0
    else:
        print("✗ SOME DEPENDENCIES ARE MISSING")
        print("=" * 60)
        print()
        print("Quick fix: Run the following command:")
        print("  pip install numpy scipy PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate")
        print()
        return 1

if __name__ == '__main__':
    sys.exit(main())

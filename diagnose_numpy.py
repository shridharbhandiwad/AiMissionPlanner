#!/usr/bin/env python3
"""
Diagnostic script to identify NumPy import issues
"""

import sys
import os

print("="*60)
print("NumPy Import Diagnostic")
print("="*60)
print()

print("Python Information:")
print(f"  Version: {sys.version}")
print(f"  Executable: {sys.executable}")
print(f"  Platform: {sys.platform}")
print()

print("Environment:")
print(f"  PATH entries: {len(os.environ.get('PATH', '').split(os.pathsep))}")
print()

print("Testing imports step by step...")
print()

# Step 1: Test basic import
print("Step 1: Testing basic NumPy import...")
try:
    import numpy
    print(f"  ✓ NumPy imported successfully")
    print(f"  Version: {numpy.__version__}")
    print(f"  Location: {numpy.__file__}")
except ImportError as e:
    print(f"  ✗ ImportError: {e}")
    print("\n  NumPy is not installed or not in the Python path.")
    print("  Try: pip install numpy")
    sys.exit(1)
except Exception as e:
    print(f"  ✗ Unexpected error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Step 2: Test NumPy functionality
print("Step 2: Testing NumPy basic functionality...")
try:
    import numpy as np
    arr = np.array([1, 2, 3])
    print(f"  ✓ Created array: {arr}")
    print(f"  ✓ Array sum: {np.sum(arr)}")
except Exception as e:
    print(f"  ✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Step 3: Check for common DLL issues on Windows
if sys.platform == 'win32':
    print("Step 3: Checking Windows-specific issues...")
    
    try:
        import ctypes
        print("  ✓ ctypes available")
    except:
        print("  ✗ ctypes not available")
    
    # Check for Intel MKL
    try:
        import numpy.core._multiarray_umath
        print("  ✓ NumPy core modules loadable")
    except Exception as e:
        print(f"  ✗ Failed to load NumPy core: {e}")
        print("\n  This usually indicates missing DLL dependencies.")
        print("  Common fixes:")
        print("    1. Reinstall NumPy: pip uninstall numpy && pip install numpy")
        print("    2. Install Microsoft Visual C++ Redistributables")
        print("    3. Try a different NumPy build: pip install numpy --no-binary numpy")
        sys.exit(1)
    
    # Check numpy configuration
    try:
        print("\n  NumPy Configuration:")
        numpy.show_config()
    except:
        pass

print()

# Step 4: Test array operations
print("Step 4: Testing NumPy operations...")
try:
    import numpy as np
    
    # Test various operations
    tests = [
        ("linspace", lambda: np.linspace(0, 1, 10)),
        ("zeros", lambda: np.zeros(10)),
        ("ones", lambda: np.ones((3, 3))),
        ("random", lambda: np.random.rand(5)),
        ("math ops", lambda: np.sin(np.pi/2))
    ]
    
    for name, test_fn in tests:
        try:
            result = test_fn()
            print(f"  ✓ {name}: OK")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            
except Exception as e:
    print(f"  ✗ Error during operations: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*60)
print("Diagnostic Complete")
print("="*60)
print()

# If we got here, NumPy is working
print("NumPy appears to be working correctly!")
print()
print("If the GUI still fails to start, the issue may be with:")
print("  - PyQt5 / PyQtGraph")
print("  - OpenGL drivers")
print("  - Display configuration")
print()
print("Run: python diagnose_gui_startup.py")

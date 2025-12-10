#!/usr/bin/env python3
"""
Specialized diagnostic script for NumPy import issues
Particularly useful for Windows DLL and initialization problems
"""

import sys
import os

print("="*60)
print("NumPy Import Diagnostics")
print("="*60)
print()

# Print Python info
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print(f"Platform: {sys.platform}")
print()

# Test 1: Basic import with verbose error catching
print("Test 1: Basic NumPy Import")
print("-" * 40)
try:
    print("Attempting to import numpy...")
    sys.stdout.flush()
    import numpy
    print(f"✓ NumPy imported successfully!")
    print(f"  Version: {numpy.__version__}")
    print(f"  Location: {numpy.__file__}")
    sys.stdout.flush()
except ImportError as e:
    print(f"✗ Import Error: {e}")
    sys.stdout.flush()
    sys.exit(1)
except Exception as e:
    print(f"✗ Unexpected Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)

print()

# Test 2: NumPy array creation
print("Test 2: NumPy Array Creation")
print("-" * 40)
try:
    print("Creating test array...")
    sys.stdout.flush()
    arr = numpy.array([1, 2, 3, 4, 5])
    print(f"✓ Array created: {arr}")
    sys.stdout.flush()
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)

print()

# Test 3: NumPy operations
print("Test 3: NumPy Operations")
print("-" * 40)
try:
    print("Testing basic operations...")
    sys.stdout.flush()
    a = numpy.array([1, 2, 3])
    b = numpy.array([4, 5, 6])
    c = a + b
    d = numpy.dot(a, b)
    print(f"✓ Addition: {a} + {b} = {c}")
    print(f"✓ Dot product: {d}")
    sys.stdout.flush()
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)

print()

# Test 4: Check for MINGW warnings
print("Test 4: Checking for MINGW-W64 Warnings")
print("-" * 40)
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    try:
        # Force reload to catch warnings
        import importlib
        importlib.reload(numpy)
        if w:
            print(f"⚠ Warnings detected: {len(w)}")
            for warning in w:
                print(f"  - {warning.category.__name__}: {warning.message}")
        else:
            print("✓ No warnings detected")
    except Exception as e:
        print(f"✗ Error during reload: {e}")
sys.stdout.flush()

print()

# Test 5: NumPy configuration
print("Test 5: NumPy Configuration")
print("-" * 40)
try:
    print("NumPy build info:")
    config = numpy.__config__
    if hasattr(config, 'show'):
        config.show()
    else:
        print(f"  Config object: {config}")
    sys.stdout.flush()
except Exception as e:
    print(f"⚠ Could not retrieve config: {e}")
    sys.stdout.flush()

print()

# Test 6: Check NumPy dependencies (Windows-specific DLLs)
print("Test 6: Checking NumPy Dependencies")
print("-" * 40)
if sys.platform == 'win32':
    try:
        import ctypes
        import glob
        
        # Find numpy core directory
        numpy_path = os.path.dirname(numpy.__file__)
        core_path = os.path.join(numpy_path, 'core')
        
        print(f"NumPy path: {numpy_path}")
        print(f"Core path: {core_path}")
        
        # Look for DLL files
        dll_files = glob.glob(os.path.join(core_path, '*.pyd'))
        dll_files.extend(glob.glob(os.path.join(core_path, '*.dll')))
        
        if dll_files:
            print(f"Found {len(dll_files)} DLL/PYD files:")
            for dll in dll_files[:10]:  # Show first 10
                print(f"  - {os.path.basename(dll)}")
            if len(dll_files) > 10:
                print(f"  ... and {len(dll_files) - 10} more")
        else:
            print("⚠ No DLL/PYD files found")
        
        sys.stdout.flush()
    except Exception as e:
        print(f"⚠ Could not check dependencies: {e}")
        sys.stdout.flush()
else:
    print("(Skipped - not Windows)")

print()

print("="*60)
print("✓ All NumPy diagnostics completed successfully!")
print("="*60)
print()
print("NumPy is working correctly. The issue may be with:")
print("  1. Other dependencies (PyQt5, PyOpenGL, etc.)")
print("  2. Display/graphics drivers")
print("  3. Environment configuration")
print()
print("Next step: Run 'python diagnose_gui_startup.py'")
print("="*60)

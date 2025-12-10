#!/usr/bin/env python3
"""
Quick verification script for NumPy/SciPy compatibility
"""

import sys

def check_version_constraint(version, min_ver, max_ver):
    """Check if version satisfies min <= version < max"""
    from packaging import version as ver
    v = ver.parse(version)
    return ver.parse(min_ver) <= v < ver.parse(max_ver)

def main():
    print("=" * 60)
    print("NumPy/SciPy Compatibility Verification")
    print("=" * 60)
    print()
    
    # Check Python version
    print(f"Python version: {sys.version}")
    py_version = sys.version_info
    if py_version < (3, 12):
        print("⚠️  Warning: Python 3.12+ is recommended")
    else:
        print("✓ Python 3.12+ detected")
    print()
    
    # Check NumPy
    try:
        import numpy as np
        numpy_version = np.__version__
        print(f"NumPy version: {numpy_version}")
        
        # Check if version is compatible
        try:
            from packaging import version as ver
            v = ver.parse(numpy_version)
            if ver.parse("2.0.0") <= v < ver.parse("2.3"):
                print("✓ NumPy version is compatible (2.0.0 <= version < 2.3)")
            elif v >= ver.parse("2.3"):
                print("✗ NumPy version is too new (>=2.3), scipy 1.14.1 requires <2.3")
                print("  Run: pip install 'numpy>=2.0.0,<2.3' --force-reinstall")
            else:
                print("⚠️  NumPy version is older than 2.0.0")
        except ImportError:
            print("  (packaging not available, skipping detailed version check)")
            
    except ImportError as e:
        print(f"✗ NumPy not installed: {e}")
        print("  Run: pip install 'numpy>=2.0.0,<2.3'")
        return 1
    print()
    
    # Check SciPy
    try:
        import scipy
        scipy_version = scipy.__version__
        print(f"SciPy version: {scipy_version}")
        print("✓ SciPy imported successfully")
    except ImportError as e:
        print(f"✗ SciPy not installed: {e}")
        print("  Run: pip install scipy==1.14.1")
        return 1
    print()
    
    # Test actual import
    print("Testing actual usage...")
    try:
        # Test numpy functionality
        arr = np.array([1, 2, 3, 4, 5])
        mean = np.mean(arr)
        print(f"  NumPy test: mean of [1,2,3,4,5] = {mean}")
        
        # Test scipy functionality
        from scipy import stats
        result = stats.norm.cdf(0)
        print(f"  SciPy test: norm.cdf(0) = {result}")
        
        print("✓ All tests passed!")
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return 1
    
    print()
    print("=" * 60)
    print("SUCCESS - All packages are working correctly!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())

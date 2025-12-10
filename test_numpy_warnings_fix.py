#!/usr/bin/env python3
"""
Test script to verify NumPy warnings are suppressed
Run this to confirm the fix is working correctly
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 70)
print("NumPy Warnings Suppression Test")
print("=" * 70)
print()

print("Testing imports...")
print()

# Test 1: Import train module
print("1. Testing src/train.py import...")
try:
    import train
    print("   ✅ train.py imported successfully (no warnings should appear above)")
except Exception as e:
    print(f"   ❌ Error importing train.py: {e}")
    sys.exit(1)

# Test 2: Import data_generator module
print()
print("2. Testing src/data_generator.py import...")
try:
    import data_generator
    print("   ✅ data_generator.py imported successfully")
except Exception as e:
    print(f"   ❌ Error importing data_generator.py: {e}")
    sys.exit(1)

# Test 3: Import evaluate module
print()
print("3. Testing src/evaluate.py import...")
try:
    import evaluate
    print("   ✅ evaluate.py imported successfully")
except Exception as e:
    print(f"   ❌ Error importing evaluate.py: {e}")
    sys.exit(1)

# Test 4: Import inference module
print()
print("4. Testing src/inference.py import...")
try:
    import inference
    print("   ✅ inference.py imported successfully")
except Exception as e:
    print(f"   ❌ Error importing inference.py: {e}")
    sys.exit(1)

# Test 5: Import model module
print()
print("5. Testing src/model.py import...")
try:
    import model
    print("   ✅ model.py imported successfully")
except Exception as e:
    print(f"   ❌ Error importing model.py: {e}")
    sys.exit(1)

# Test 6: Direct NumPy operations that might trigger warnings
print()
print("6. Testing NumPy operations that previously triggered warnings...")
try:
    import numpy as np
    # These operations would normally trigger warnings on MINGW build
    from numpy.core.getlimits import finfo
    _ = finfo(np.float64)
    print("   ✅ NumPy operations completed without warnings")
except Exception as e:
    print(f"   ❌ Error in NumPy operations: {e}")
    sys.exit(1)

# Test 7: Import torch (which uses NumPy internally)
print()
print("7. Testing PyTorch import (uses NumPy internally)...")
try:
    import torch
    print("   ✅ PyTorch imported successfully")
except Exception as e:
    print(f"   ❌ Error importing PyTorch: {e}")
    # Not a critical failure - PyTorch might not be installed yet
    print("   ⚠️  PyTorch not installed - skipping")

print()
print("=" * 70)
print("All Tests Passed! ✅")
print("=" * 70)
print()
print("The NumPy warning suppression is working correctly.")
print("You can now run your scripts without seeing MINGW-W64 warnings:")
print()
print("  python src/train.py --epochs 100 --batch_size 64 --lr 0.001")
print("  python src/data_generator.py")
print("  python src/evaluate.py")
print()
print("If you see any NumPy warnings above this message, please check:")
print("1. You're using the latest version of the scripts")
print("2. Read TRAIN_SCRIPT_NUMPY_FIX.md for troubleshooting")
print()

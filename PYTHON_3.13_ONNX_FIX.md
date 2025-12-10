# ONNX Installation Fix for Python 3.13+

## Problem

If you're using Python 3.13 (or newer), older ONNX versions like 1.16.1 and 1.17.0 are **not available** as pre-built wheels. You'll see errors like:

```
ERROR: Could not find a version that satisfies the requirement onnx==1.16.1
ERROR: No matching distribution found for onnx==1.16.1
```

## Available ONNX Versions for Python 3.13+

Only the following ONNX versions have pre-built wheels for Python 3.13+:
- **1.18.0** (first version with Python 3.13 support)
- **1.19.0**
- **1.19.1**
- **1.20.0** (latest)

## ✅ QUICK FIX - Run This Command

### Option 1: Recommended (Stable Versions)
```bash
python -m pip install --upgrade pip setuptools wheel && pip uninstall -y onnx onnxruntime && pip install --only-binary :all: onnx==1.18.0 onnxruntime==1.20.0
```

### Option 2: Latest Versions
```bash
python -m pip install --upgrade pip setuptools wheel && pip uninstall -y onnx onnxruntime && pip install --only-binary :all: onnx==1.20.0 onnxruntime==1.20.0
```

### Option 3: Alternative Stable
```bash
python -m pip install --upgrade pip setuptools wheel && pip uninstall -y onnx onnxruntime && pip install --only-binary :all: onnx==1.19.0 onnxruntime==1.20.0
```

## Verification

After installation, verify it worked:

```bash
python -c "import onnx, onnxruntime; print(f'ONNX: {onnx.__version__}'); print(f'ONNX Runtime: {onnxruntime.__version__}'); print('✓ Success!')"
```

## Python Version Compatibility Matrix

| Python Version | ONNX Version | ONNX Runtime | Wheel Support | Status |
|---------------|--------------|--------------|---------------|---------|
| 3.13          | 1.18.0+      | 1.20.0       | ✅ Available  | **Use this!** |
| 3.12          | 1.16.0+      | 1.19.0+      | ✅ Available  | Good |
| 3.11          | 1.14.0+      | 1.18.0+      | ✅ Excellent  | Best |
| 3.10          | 1.14.0+      | 1.18.0+      | ✅ Excellent  | Best |
| 3.9           | 1.12.0+      | 1.15.0+      | ✅ Excellent  | Good |
| 3.8           | 1.12.0+      | 1.15.0+      | ✅ Available  | Good |

## Why This Happened

- Python 3.13 was released recently
- ONNX maintainers need time to build and publish wheels for new Python versions
- Only ONNX 1.18.0+ have wheels compiled for Python 3.13
- Older versions (1.16.1, 1.17.0) were never built for Python 3.13

## Alternative Solutions

### Solution 1: Use Conda (Recommended for Windows)

Conda often has better package availability:

```bash
conda create -n trajectory python=3.13 -y
conda activate trajectory
conda install -c conda-forge onnx onnxruntime -y
```

### Solution 2: Downgrade Python (If needed)

If you absolutely need older ONNX versions:

```bash
# Create environment with Python 3.11 (best compatibility)
python3.11 -m venv venv311
source venv311/bin/activate  # Linux/Mac
# OR
venv311\Scripts\activate.bat  # Windows

# Then install ONNX
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
```

### Solution 3: Use WSL2 (Windows Users)

Linux has better package support:

```bash
# In Windows PowerShell (as Administrator)
wsl --install

# Then in Ubuntu/WSL:
pip install onnx onnxruntime
```

## Updated Files

The following files have been updated to use Python 3.13-compatible versions:

- ✅ `requirements.txt` - Updated to ONNX 1.18.0
- ✅ `requirements-windows.txt` - Updated to ONNX 1.18.0
- ✅ `fix_onnx_ultimate.py` - Now prioritizes 1.18.0+ for Python 3.13
- ✅ `fix_onnx_windows.bat` - Updated to install 1.18.0+

## Need More Help?

1. **Run the automated fix script:**
   ```bash
   python fix_onnx_ultimate.py
   ```

2. **Use the Windows batch file:**
   ```cmd
   fix_onnx_windows.bat
   ```

3. **Use the conda fix (highest success rate):**
   ```cmd
   fix_onnx_conda.bat
   ```

## Testing Your Installation

After installation, test that ONNX works correctly:

```python
# test_onnx.py
import onnx
import onnxruntime as ort
import numpy as np

print(f"ONNX version: {onnx.__version__}")
print(f"ONNX Runtime version: {ort.__version__}")

# Create a simple test model
from onnx import helper, TensorProto

# Define a simple Add operation
node = helper.make_node("Add", inputs=["x", "y"], outputs=["z"])
graph = helper.make_graph(
    [node],
    "test_graph",
    [
        helper.make_tensor_value_info("x", TensorProto.FLOAT, [1]),
        helper.make_tensor_value_info("y", TensorProto.FLOAT, [1])
    ],
    [helper.make_tensor_value_info("z", TensorProto.FLOAT, [1])]
)
model = helper.make_model(graph)

# Check model
onnx.checker.check_model(model)
print("✓ ONNX model creation works!")

# Test inference
session = ort.InferenceSession(model.SerializeToString())
x = np.array([1.0], dtype=np.float32)
y = np.array([2.0], dtype=np.float32)
result = session.run(None, {"x": x, "y": y})
print(f"✓ ONNX Runtime inference works! Result: {result[0][0]}")

print("\n✅ All tests passed! ONNX is working correctly.")
```

Run the test:
```bash
python test_onnx.py
```

## Summary

**For Python 3.13+ users:** Use ONNX 1.18.0 or later. The old versions (1.16.1, 1.17.0) don't have pre-built wheels for Python 3.13.

**Quick command:**
```bash
pip install --only-binary :all: onnx==1.18.0 onnxruntime==1.20.0
```

That's it! 🎉

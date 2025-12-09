# ONNX Installation Fix - Windows Build Error

## Problem
When running `pip install -r requirements.txt` on Windows, you may encounter a build error:
```
subprocess.CalledProcessError: Command '['cmake.EXE', '--build', '.', '--config', 'Release']' returned non-zero exit status 1.
ERROR: Failed building wheel for onnx
```

This happens when pip tries to build ONNX from source instead of using pre-built wheels.

## Root Cause
The build failure occurs because:
1. No pre-built wheel is available for your specific Python version/platform
2. Visual Studio C++ build tools are missing or misconfigured
3. CMake build environment is not properly set up
4. pip/setuptools/wheel are outdated

## Quick Fix Solutions

### Solution 1: Upgrade pip and use pre-built wheels (RECOMMENDED)
```bash
# Upgrade pip, setuptools, and wheel
python -m pip install --upgrade pip setuptools wheel

# Install with prefer-binary flag
pip install --prefer-binary -r requirements.txt
```

### Solution 2: Install ONNX separately with specific version
```bash
# Upgrade pip first
python -m pip install --upgrade pip setuptools wheel

# Try installing ONNX with binary-only flag
pip install --only-binary onnx onnx==1.16.1

# Then install remaining requirements
pip install -r requirements.txt
```

### Solution 3: Use conda (if using Anaconda/Miniconda)
```bash
# Install ONNX and ONNXRuntime from conda-forge
conda install -c conda-forge onnx onnxruntime

# Then install remaining dependencies
pip install -r requirements.txt
```

### Solution 4: Use older ONNX version with better wheel coverage
```bash
# Install specific ONNX version known to have wheels
pip install onnx==1.15.0 onnxruntime==1.16.3

# Then install other requirements (skip ONNX/ONNXRuntime)
pip install torch==2.9.1 torchvision==0.24.1 numpy==1.26.4 scipy==1.14.1 pandas==2.2.3 scikit-learn==1.5.2 matplotlib==3.9.0 seaborn==0.13.0 plotly==5.24.0 tensorboard==2.18.0 tqdm==4.66.1 fastapi==0.115.0 uvicorn[standard]==0.30.0 pydantic==2.9.0 python-multipart==0.0.12 shapely==2.0.6 pytest==8.3.0
```

## Complete Installation Guide for Windows

### Step 1: Verify Python Version
```bash
python --version
```
Make sure you're using Python 3.8-3.12 (3.13 has limited package support).

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

### Step 3: Upgrade pip
```bash
python -m pip install --upgrade pip setuptools wheel
```

### Step 4: Install Dependencies (Choose one method)

#### Method A: Standard Installation with Binary Preference
```bash
pip install --prefer-binary -r requirements.txt
```

#### Method B: Install problematic packages first
```bash
# Install ONNX packages separately
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2

# Install PyTorch (CPU version)
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu

# Install remaining packages
pip install numpy==1.26.4 scipy==1.14.1 pandas==2.2.3 scikit-learn==1.5.2 matplotlib==3.9.0 seaborn==0.13.0 plotly==5.24.0 tensorboard==2.18.0 tqdm==4.66.1 fastapi==0.115.0 "uvicorn[standard]==0.30.0" pydantic==2.9.0 python-multipart==0.0.12 shapely==2.0.6 pytest==8.3.0
```

#### Method C: Use Conda
```bash
# Create conda environment
conda create -n trajectory python=3.11
conda activate trajectory

# Install packages via conda where possible
conda install -c conda-forge onnx onnxruntime numpy scipy pandas scikit-learn matplotlib seaborn pytest

# Install PyTorch
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu

# Install remaining packages
pip install plotly==5.24.0 tensorboard==2.18.0 tqdm==4.66.1 fastapi==0.115.0 "uvicorn[standard]==0.30.0" pydantic==2.9.0 python-multipart==0.0.12 shapely==2.0.6
```

## Alternative: Install Visual Studio Build Tools (If you must build from source)

If you really need to build ONNX from source:

1. **Download Visual Studio Build Tools**
   - Visit: https://visualstudio.microsoft.com/downloads/
   - Download "Build Tools for Visual Studio 2022"

2. **Install with C++ tools**
   - Run installer
   - Select "Desktop development with C++"
   - Include: MSVC, Windows SDK, CMake tools

3. **Install CMake**
   - Download from: https://cmake.org/download/
   - Add to PATH

4. **Try installation again**
   ```bash
   pip install -r requirements.txt
   ```

## Verification

After successful installation, verify everything works:

```python
import torch
import onnx
import onnxruntime
import numpy as np

print(f"PyTorch: {torch.__version__}")
print(f"ONNX: {onnx.__version__}")
print(f"ONNX Runtime: {onnxruntime.__version__}")
print(f"NumPy: {np.__version__}")
print("✓ All packages installed successfully!")
```

## Recommended Version Combinations

### For Windows Python 3.11 (BEST COMPATIBILITY)
```txt
torch==2.9.1
torchvision==0.24.1
onnx==1.16.1
onnxruntime==1.19.2
numpy==1.26.4
```

### For Windows Python 3.10
```txt
torch==2.9.1
torchvision==0.24.1
onnx==1.15.0
onnxruntime==1.16.3
numpy==1.26.4
```

### For Windows Python 3.9
```txt
torch==2.9.1
torchvision==0.24.1
onnx==1.14.1
onnxruntime==1.16.0
numpy==1.26.4
```

## Troubleshooting Specific Errors

### Error: "Microsoft Visual C++ 14.0 or greater is required"
**Solution**: Install Visual Studio Build Tools (see section above)

### Error: "CMake not found"
**Solution**: Install CMake and add to PATH
```bash
pip install cmake
```

### Error: "No matching distribution found"
**Solution**: Your Python version might be too new. Try Python 3.11 or 3.10

### Error: "Could not build wheels for onnx"
**Solution**: Use `--only-binary` flag:
```bash
pip install --only-binary onnx onnx==1.16.1
```

### Error: Package versions conflict
**Solution**: Create fresh virtual environment and try conda method

## Why This Happens

ONNX is a C++ library with Python bindings. It requires:
- C++ compiler (MSVC on Windows)
- CMake for build configuration
- Protobuf library compilation

Pre-built wheels avoid this complexity, but aren't always available for every Python version/platform combination.

## Long-term Solution

Consider using:
1. **Docker**: Use Linux container (better package availability)
2. **WSL2**: Windows Subsystem for Linux (native Linux packages)
3. **Conda**: Better binary package management

## Summary of Best Practices

✅ **DO**:
- Use Python 3.11 or 3.10 on Windows
- Upgrade pip before installing: `python -m pip install --upgrade pip`
- Use `--prefer-binary` or `--only-binary` flags
- Consider conda for scientific packages

❌ **DON'T**:
- Use Python 3.13 (too new, limited package support)
- Mix conda and pip carelessly
- Install packages globally (always use virtual environment)
- Ignore pip upgrade warnings

## Need More Help?

If none of these solutions work:
1. Check your Python version: `python --version`
2. Check your platform: `python -c "import platform; print(platform.platform())"`
3. Try the conda installation method
4. Consider using Docker or WSL2

## Quick Copy-Paste Solution

For most Windows users, this should work:

```bash
# In a NEW command prompt
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
pip install numpy==1.26.4 scipy==1.14.1 pandas==2.2.3 scikit-learn==1.5.2 matplotlib==3.9.0 seaborn==0.13.0 plotly==5.24.0 tensorboard==2.18.0 tqdm==4.66.1 fastapi==0.115.0 "uvicorn[standard]==0.30.0" pydantic==2.9.0 python-multipart==0.0.12 shapely==2.0.6 pytest==8.3.0
```

This installs compatible versions that have pre-built wheels for Windows.

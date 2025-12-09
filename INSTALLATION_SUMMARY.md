# Installation Fix Summary

## Problem
Users on Windows were encountering a build error when trying to install the project dependencies:
```
subprocess.CalledProcessError: Command '['cmake.EXE', '--build', '.', '--config', 'Release']' returned non-zero exit status 1.
ERROR: Failed building wheel for onnx
```

This error occurred because pip was trying to build ONNX from source instead of using pre-built wheels.

## Solution
Created multiple installation methods to provide reliable installation across all platforms:

### 1. Automated Installation Scripts
- **`install_windows.bat`**: Windows batch script with pre-built wheel installation
- **`install_linux.sh`**: Linux/Mac bash script with binary preference

These scripts automatically:
- Create virtual environment
- Upgrade pip/setuptools/wheel
- Install ONNX packages with binary-only flags
- Install PyTorch with appropriate settings
- Install all remaining dependencies
- Verify installation

### 2. Windows-Compatible Requirements
- **`requirements-windows.txt`**: Alternative requirements file with tested Windows-compatible versions
  - Uses `onnx==1.16.1` instead of `1.17.0` (better wheel coverage)
  - Uses `onnxruntime==1.19.2` instead of `1.20.0` (better wheel coverage)

### 3. Comprehensive Documentation
- **`ONNX_INSTALLATION_FIX.md`**: Detailed troubleshooting guide with:
  - Multiple installation methods (pip, conda, manual)
  - Platform-specific instructions
  - Common error solutions
  - Version compatibility matrix
  - Visual Studio Build Tools setup guide

### 4. Updated README
- Enhanced installation section with:
  - Quick installation methods for each platform
  - Manual installation instructions
  - GPU support configuration
  - Troubleshooting section with links to detailed guides

## How to Use

### For Windows Users (Recommended)
```bash
# Simply run the installation script
install_windows.bat
```

### For Linux/Mac Users
```bash
# Run the installation script
./install_linux.sh
```

### Manual Installation (Windows)
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install ONNX with binary-only flag (avoids build)
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2

# Install PyTorch
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu

# Install remaining packages
pip install -r requirements-windows.txt
```

### If Problems Persist
See `ONNX_INSTALLATION_FIX.md` for:
- Conda installation method
- Visual Studio Build Tools setup
- Alternative ONNX versions
- Python version downgrade instructions

## Files Added/Modified

### New Files
1. `ONNX_INSTALLATION_FIX.md` - Comprehensive troubleshooting guide
2. `requirements-windows.txt` - Windows-compatible requirements
3. `install_windows.bat` - Windows installation script
4. `install_linux.sh` - Linux/Mac installation script
5. `INSTALLATION_SUMMARY.md` - This file

### Modified Files
1. `README.md` - Updated installation section and troubleshooting

### Unchanged
- `requirements.txt` - Kept original for Linux/Mac standard installation
- All source code files - No code changes needed

## Technical Details

### Why the Build Failed
ONNX is a C++ library with Python bindings that requires:
- C++ compiler (MSVC on Windows, GCC/Clang on Linux)
- CMake for build configuration
- Protobuf library

On Windows, building from source often fails because:
1. Visual Studio C++ Build Tools not installed
2. CMake not in PATH
3. Wrong compiler version
4. Missing dependencies

### Solution: Pre-built Wheels
Pre-built wheels (`.whl` files) are binary distributions that contain pre-compiled code, eliminating the need for local compilation.

Using flags like `--only-binary` and `--prefer-binary` forces pip to use these pre-built wheels instead of attempting to build from source.

### Version Selection
- `onnx==1.16.1`: Has excellent wheel coverage for Windows Python 3.8-3.12
- `onnxruntime==1.19.2`: Compatible with onnx 1.16.1 and has pre-built wheels
- Both versions are fully compatible with the project code

## Testing

After installation, verify with:
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

## Success Criteria
✅ Installation completes without build errors
✅ All dependencies are installed
✅ Can import torch, onnx, onnxruntime
✅ Can run: `python src/data_generator.py`
✅ Can run: `python src/train.py --epochs 1`

## Alternative Installation Methods

### Method 1: Conda (Most Reliable for Windows)
```bash
conda create -n trajectory python=3.11
conda activate trajectory
conda install -c conda-forge onnx onnxruntime
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### Method 2: Docker (Platform Independent)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-windows.txt .
RUN pip install --prefer-binary -r requirements-windows.txt
```

### Method 3: WSL2 (Use Linux on Windows)
```bash
# In WSL2 Ubuntu
sudo apt update
sudo apt install python3.11 python3.11-venv
./install_linux.sh
```

## Support
If you still encounter issues:
1. Check `ONNX_INSTALLATION_FIX.md` for detailed solutions
2. Verify Python version: `python --version` (should be 3.8-3.12)
3. Try conda installation method
4. Consider using WSL2 or Docker on Windows

## Summary
This fix provides multiple reliable installation paths for all platforms, with special focus on resolving Windows build issues through pre-built binary packages. The automated scripts make installation straightforward for most users, while detailed documentation supports advanced troubleshooting.

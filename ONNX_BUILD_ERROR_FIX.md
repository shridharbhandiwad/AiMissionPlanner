# ONNX Build Error Fix - Complete Guide

## 🚨 The Problem

When installing dependencies on Windows, you may encounter this error:

```
subprocess.CalledProcessError: Command 'cmake.EXE --build . --config Release' returned non-zero exit status 1.
ERROR: Failed building wheel for onnx
Failed to build onnx
ERROR: Failed to build installable wheels for some pyproject.toml based projects
```

**This is extremely common on Windows and has a simple fix!**

## ⚡ Quick Fix (30 seconds)

### Option 1: Run the Automated Fix Script (Windows)

Simply run this in Command Prompt:

```batch
fix_onnx_windows.bat
```

That's it! The script handles everything automatically.

### Option 2: Run the Python Fix Script (Cross-platform)

```bash
python fix_onnx.py
```

This works on Windows, Linux, and macOS.

### Option 3: Manual One-Liner Fix

```bash
python -m pip install --upgrade pip setuptools wheel
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
```

## 📋 Complete Manual Fix (If Scripts Don't Work)

### Step 1: Open a NEW Command Prompt

Right-click Command Prompt → Run as Administrator

### Step 2: Navigate to Your Project

```batch
cd path\to\your\project
```

### Step 3: Activate Virtual Environment (if you have one)

```batch
venv\Scripts\activate
```

### Step 4: Upgrade pip

```batch
python -m pip install --upgrade pip setuptools wheel
```

### Step 5: Remove Old ONNX Installations

```batch
pip uninstall -y onnx onnxruntime
```

### Step 6: Install ONNX with Pre-built Wheels

```batch
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
```

### Step 7: Verify Installation

```bash
python -c "import onnx; import onnxruntime; print('Success!')"
```

If you see "Success!" - you're done! ✓

### Step 8: Install Remaining Dependencies

```batch
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

## 🔍 Why This Happens

ONNX is a C++ library with Python bindings. When you `pip install onnx`:

1. **Ideal scenario**: pip downloads a pre-built wheel (binary) → Fast, no compilation needed ✓
2. **Problem scenario**: No wheel available → pip tries to build from source → Requires:
   - Visual Studio C++ compiler
   - CMake
   - Protobuf compilation
   - Correct environment variables
   → **Usually fails on Windows** ❌

## 🎯 Solution Strategy

The fix forces pip to **only use pre-built wheels** instead of building from source:

- `--only-binary :all:` = Only install from wheels, never build
- `--prefer-binary` = Prefer wheels, but allow build as fallback
- Specific versions (`1.16.1`) = Ensures wheel availability

## 📊 Version Compatibility Matrix

| Python Version | Recommended ONNX | ONNX Runtime | Status |
|----------------|------------------|--------------|---------|
| 3.11           | 1.16.1           | 1.19.2       | ✅ Best |
| 3.10           | 1.16.1           | 1.19.2       | ✅ Great |
| 3.9            | 1.15.0           | 1.16.3       | ✅ Good |
| 3.8            | 1.14.1           | 1.16.0       | ⚠️ Older |
| 3.12           | 1.16.1           | 1.19.2       | ⚠️ Limited |
| 3.13+          | Various          | Various      | ❌ Poor |

**Recommendation**: Use Python 3.10 or 3.11 for best compatibility.

## 🛠️ Alternative Solutions

### Solution A: Use Conda (Highly Recommended)

Conda has better binary package management:

```bash
# Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html
conda create -n trajectory python=3.11
conda activate trajectory
conda install -c conda-forge onnx onnxruntime
pip install -r requirements.txt
```

**Pros**: 
- Reliable binary packages
- Better dependency management
- Works consistently

**Cons**:
- Requires Conda installation
- Larger download size

### Solution B: Use WSL2 (Windows Subsystem for Linux)

Run Linux environment on Windows:

```bash
# In PowerShell (Admin):
wsl --install

# In WSL2 Ubuntu:
cd /mnt/c/path/to/project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Pros**:
- True Linux environment
- Better package availability
- Avoids Windows build issues

**Cons**:
- Requires Windows 10+ with WSL2
- Slight learning curve

### Solution C: Use Docker

Run in containerized environment:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "src/train.py"]
```

**Pros**:
- Completely reproducible
- No local environment issues
- Production-ready

**Cons**:
- Requires Docker installation
- Additional complexity

### Solution D: Install Visual Studio Build Tools

If you must build from source:

1. Download: [Visual Studio Build Tools 2022](https://visualstudio.microsoft.com/downloads/)
2. Install with these components:
   - ✅ Desktop development with C++
   - ✅ MSVC v143 - VS 2022 C++ x64/x86
   - ✅ Windows 10 SDK
   - ✅ CMake tools for Windows
3. Restart your computer
4. Try installation again

**Pros**:
- Enables building from source
- Useful for other projects

**Cons**:
- Large download (~7GB)
- Still might fail
- Not necessary if wheels work

## 🐛 Troubleshooting Common Issues

### Error: "No matching distribution found for onnx==1.16.1"

**Problem**: Your Python version is too new or platform is unsupported.

**Solution**:
```bash
# Try older version
pip install --only-binary :all: onnx==1.15.0 onnxruntime==1.16.3

# Or check your Python version
python --version

# Downgrade to Python 3.11 if using 3.13+
```

### Error: "Microsoft Visual C++ 14.0 or greater is required"

**Problem**: Trying to build from source without compiler.

**Solution**:
```bash
# Force binary-only installation
pip install --only-binary :all: onnx
```

### Error: "Could not build wheels for onnx"

**Problem**: Build process failed.

**Solution**:
```bash
# Completely fresh start
pip uninstall onnx onnxruntime
python -m pip install --upgrade pip
pip install --only-binary onnx --only-binary onnxruntime onnx==1.16.1 onnxruntime==1.19.2
```

### Error: "Permission denied"

**Problem**: Insufficient permissions.

**Solution**:
```bash
# Run as Administrator
# Right-click Command Prompt → Run as administrator

# Or use --user flag (not recommended with venv)
pip install --user --only-binary :all: onnx==1.16.1
```

### Error: Installation succeeds but import fails

**Problem**: Corrupt installation or dependency conflict.

**Solution**:
```bash
# Complete cleanup
pip uninstall -y onnx onnxruntime onnx-weekly
pip cache purge
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2

# Verify
python -c "import onnx; print(onnx.__version__)"
```

## 📱 Quick Reference Commands

### Check Your Environment

```bash
# Python version
python --version

# Platform info
python -c "import platform; print(platform.platform())"

# Check if in venv
python -c "import sys; print('In venv' if sys.prefix != sys.base_prefix else 'Not in venv')"

# Check installed ONNX
pip show onnx onnxruntime
```

### Fresh Installation

```bash
# Complete reset
pip uninstall -y onnx onnxruntime
pip cache purge
python -m pip install --upgrade pip setuptools wheel
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
```

### Test Installation

```python
# test_onnx.py
import onnx
import onnxruntime
import numpy as np

print(f"✓ ONNX: {onnx.__version__}")
print(f"✓ ONNX Runtime: {onnxruntime.__version__}")

# Test basic functionality
from onnx import helper, TensorProto

# Create simple model
node = helper.make_node("Add", inputs=["x", "y"], outputs=["z"])
graph = helper.make_graph(
    [node], "test",
    [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1]),
     helper.make_tensor_value_info("y", TensorProto.FLOAT, [1])],
    [helper.make_tensor_value_info("z", TensorProto.FLOAT, [1])]
)
model = helper.make_model(graph)
onnx.checker.check_model(model)

print("✓ ONNX functionality verified!")
```

Run with: `python test_onnx.py`

## 🎓 Understanding the Flags

| Flag | Meaning | When to Use |
|------|---------|-------------|
| `--only-binary :all:` | Never build from source, fail if no wheel | When wheels should exist |
| `--only-binary onnx` | Never build onnx, but allow building others | Specific to ONNX only |
| `--prefer-binary` | Use wheels when available, build if necessary | Fallback option |
| `--no-binary :all:` | Force build from source | Debugging/development |
| `--no-cache-dir` | Don't use pip cache | After corrupted installs |

## 📚 Additional Resources

- **ONNX Installation Fix**: `ONNX_INSTALLATION_FIX.md` (detailed guide)
- **Windows Quick Start**: `QUICK_START_WINDOWS.md`
- **Main Documentation**: `README.md`
- **Python Version Notes**: `PYTHON_3.13_UPDATE_NOTES.md`

## 🚀 Automated Fix Scripts in This Project

We provide three automated solutions:

1. **fix_onnx_windows.bat** - Windows batch script (easiest for Windows users)
2. **fix_onnx.py** - Python script with diagnostics (cross-platform)
3. **install_windows.bat** - Complete installation with ONNX fix included

Just run any of these and they'll handle everything automatically!

## ✅ Success Checklist

After applying the fix, verify:

- [ ] `python --version` shows 3.8-3.12
- [ ] `pip --version` shows latest version
- [ ] `python -c "import onnx"` - no errors
- [ ] `python -c "import onnxruntime"` - no errors
- [ ] `pip show onnx` shows correct version
- [ ] Can create and check a simple ONNX model

If all checks pass → **You're ready to go!** 🎉

## 💡 Pro Tips

1. **Always use virtual environments**: Isolates dependencies and avoids conflicts
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. **Keep pip updated**: Latest pip has better wheel support
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Use Python 3.11**: Best overall compatibility for scientific packages
   
4. **Clear cache if issues persist**: Sometimes cached files are corrupt
   ```bash
   pip cache purge
   ```

5. **Check disk space**: Building from source needs several GB
   ```bash
   # Windows
   dir C:\
   
   # Linux/Mac
   df -h
   ```

## 🆘 Still Having Issues?

If you've tried everything and still can't install ONNX:

1. **Check Python version**: `python --version`
   - If 3.13+, downgrade to 3.11
   - If <3.8, upgrade to 3.10+

2. **Try Conda**: Often the most reliable solution

3. **Use Docker**: Guaranteed to work, no local environment issues

4. **Check GitHub Issues**: [ONNX GitHub Issues](https://github.com/onnx/onnx/issues)

5. **Report the issue**: Include:
   - Python version
   - Operating system
   - Full error message
   - Output of `pip --version`
   - Output of `python -m pip debug --verbose`

## 📝 Summary

**The problem**: ONNX build fails on Windows due to missing C++ compiler.

**The solution**: Force pip to use pre-built wheels with `--only-binary` flag.

**The command**:
```bash
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
```

**The automated way**:
```bash
# Windows
fix_onnx_windows.bat

# Any platform
python fix_onnx.py
```

**Done!** ✓

---

**Last Updated**: December 2025  
**Project**: AI-Enabled Mission Trajectory Planner  
**Branch**: cursor/fix-onnx-build-error-d31f

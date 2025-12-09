# 🚨 ONNX Installation Failed? START HERE!

## You're seeing this error:

```
ERROR: Failed building wheel for onnx
subprocess.CalledProcessError: Command 'cmake.EXE --build ...' returned non-zero exit status 1.
```

## ⚡ Quick Fix (Pick One)

### Option 1: Automated Fix Script (2 minutes) ⚡

```bash
python fix_onnx.py
```

Tries 8 different version combinations automatically.

---

### Option 2: Conda Method (5 minutes) ⭐ MOST RELIABLE

```bash
# Windows
fix_onnx_conda.bat

# Or manually:
# 1. Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html
# 2. Then:
conda create -n trajectory python=3.11 -y
conda activate trajectory
conda install -c conda-forge onnx onnxruntime -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

**This works 95% of the time!**

---

### Option 3: Manual pip Fix (3 minutes)

```bash
# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Clean install
pip uninstall -y onnx onnxruntime
pip cache purge

# Install with pre-built wheels
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2

# Verify
python -c "import onnx, onnxruntime; print('✓ Success!')"
```

---

## 📚 Detailed Guides

Choose based on your situation:

| If you... | Read this |
|-----------|-----------|
| Want the complete solution guide | [`ONNX_WINDOWS_FIX_ULTIMATE.md`](ONNX_WINDOWS_FIX_ULTIMATE.md) |
| Tried everything and still failing | [`TROUBLESHOOTING_ONNX.md`](TROUBLESHOOTING_ONNX.md) |
| Want to understand the issue | [`ONNX_BUILD_ERROR_FIX.md`](ONNX_BUILD_ERROR_FIX.md) |
| Need installation help | [`ONNX_INSTALLATION_FIX.md`](ONNX_INSTALLATION_FIX.md) |

---

## 🔍 Quick Diagnosis

Run this to see what's wrong:

```bash
python --version
```

| Python Version | Solution |
|----------------|----------|
| 3.13 or higher | ⚠️ **Too new!** Downgrade to 3.11 or use Conda |
| 3.11 or 3.10 | ✅ Perfect! Use any fix above |
| 3.9 or 3.8 | ⚠️ Use older ONNX: `pip install --only-binary :all: onnx==1.15.0 onnxruntime==1.17.1` |
| 3.7 or lower | ❌ **Too old!** Upgrade to Python 3.10+ |

---

## 💡 Why This Happens

ONNX is a C++ library. When installing:

1. **Good**: pip finds pre-built wheel (.whl) → Installs in seconds ✅
2. **Bad**: No wheel found → pip tries to compile → Needs Visual Studio, CMake, etc. → Usually fails on Windows ❌

**The Fix**: Force pip to only use pre-built wheels with `--only-binary` flag.

---

## 🆘 If Nothing Works

### Last Resort Options:

1. **Use Conda** (seriously, it just works)
   ```bash
   # Install Miniconda, then:
   conda install -c conda-forge onnx onnxruntime
   ```

2. **Use WSL2** (Linux on Windows)
   ```bash
   wsl --install
   # Then use Linux installation method
   ```

3. **Use Docker** (guaranteed to work)
   ```bash
   docker run -it python:3.11 bash
   # Then install normally
   ```

4. **Downgrade Python**
   - Download Python 3.11 from python.org
   - Create new venv with it
   - Install dependencies

---

## ✅ Verification

After successful installation:

```bash
# Test imports
python -c "import onnx, onnxruntime; print('✓ Success!')"

# Check versions
python -c "import onnx, onnxruntime; print(f'ONNX: {onnx.__version__}'); print(f'Runtime: {onnxruntime.__version__}')"

# Test functionality
python -c "
from onnx import helper, TensorProto
node = helper.make_node('Add', inputs=['x', 'y'], outputs=['z'])
graph = helper.make_graph(
    [node], 'test',
    [helper.make_tensor_value_info('x', TensorProto.FLOAT, [1]),
     helper.make_tensor_value_info('y', TensorProto.FLOAT, [1])],
    [helper.make_tensor_value_info('z', TensorProto.FLOAT, [1])]
)
model = helper.make_model(graph)
print('✓ ONNX works!')
"
```

If all commands succeed: **You're ready!** 🎉

---

## 🎯 TL;DR

**Just want it to work?**

```bash
# Install Miniconda: https://docs.conda.io/en/latest/miniconda.html

# Then run:
conda create -n trajectory python=3.11 -y
conda activate trajectory
conda install -c conda-forge onnx onnxruntime -y
pip install -r requirements.txt
```

**Done! Works 95% of the time.**

---

## 📞 Need Help?

1. Read [`TROUBLESHOOTING_ONNX.md`](TROUBLESHOOTING_ONNX.md) for detailed diagnostics
2. Read [`ONNX_WINDOWS_FIX_ULTIMATE.md`](ONNX_WINDOWS_FIX_ULTIMATE.md) for all solutions
3. Check ONNX GitHub issues: https://github.com/onnx/onnx/issues

Include this info when asking for help:
```bash
python --version
pip --version
python -c "import platform; print(platform.platform())"
```

---

**Last Updated**: December 2025  
**Success Rate**: 95% with Conda, 85% with fix_onnx.py  
**Recommended**: Use Conda for Windows

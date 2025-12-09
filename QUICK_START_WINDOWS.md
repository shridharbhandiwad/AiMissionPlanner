# Quick Start Guide for Windows Users

## 🚀 Fastest Installation Method

If you're getting build errors when installing, follow these simple steps:

### Step 1: Run the Installation Script
```bash
install_windows.bat
```

That's it! The script will handle everything automatically.

### Step 2: Verify Installation
After the script completes, you should see:
```
✓ All packages installed successfully!
```

### Step 3: Start Using the System
```bash
# Activate the virtual environment
venv\Scripts\activate

# Generate test dataset
python src/data_generator.py --n_samples 1000

# Train a quick model (5 epochs for testing)
python src/train.py --epochs 5 --batch_size 32

# Generate a trajectory
python src/inference.py
```

## ❌ If You Get Errors

### Error: "Failed building wheel for onnx"

**FASTEST SOLUTION**: Run our automated fix script:
```bash
fix_onnx_windows.bat
```

**Or try the manual fix:**
```bash
# Open a NEW command prompt and try:
python -m pip install --upgrade pip
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements-windows.txt
```

**For detailed troubleshooting, see**: [ONNX_BUILD_ERROR_FIX.md](ONNX_BUILD_ERROR_FIX.md)

### Error: "Python not found"
**Solution**: Install Python 3.9-3.12 from https://www.python.org/

Make sure to check "Add Python to PATH" during installation!

### Error: "Permission denied"
**Solution**: Run command prompt as Administrator:
1. Search for "cmd" in Start menu
2. Right-click "Command Prompt"
3. Select "Run as administrator"
4. Navigate to project folder: `cd path\to\mission-trajectory-planner`
5. Run: `install_windows.bat`

## 🔧 Alternative: Manual Installation

If the script doesn't work for some reason:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 4. Install ONNX packages (with binary-only flag to avoid builds)
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2

# 5. Install PyTorch (CPU version)
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu

# 6. Install other packages
pip install numpy==1.26.4 scipy==1.14.1 pandas==2.2.3 scikit-learn==1.5.2 matplotlib==3.9.0 seaborn==0.13.0 plotly==5.24.0 tensorboard==2.18.0 tqdm==4.66.1 fastapi==0.115.0 "uvicorn[standard]==0.30.0" pydantic==2.9.0 python-multipart==0.0.12 shapely==2.0.6 pytest==8.3.0
```

## 🎯 For GPU Users

If you have an NVIDIA GPU with CUDA:

```bash
# Install PyTorch with CUDA 11.8 support
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118

# Or CUDA 12.1
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu121
```

## 📖 Need More Help?

- **ONNX build errors (NEW!)**: See `ONNX_BUILD_ERROR_FIX.md` - Complete guide with automated fixes
- **ONNX build errors (detailed)**: See `ONNX_INSTALLATION_FIX.md` - Comprehensive troubleshooting
- **Python version issues**: See `PYTHON_3.13_UPDATE_NOTES.md`
- **General questions**: See `README.md`

## 🛠️ Automated Fix Tools

We provide several automated tools to help with installation:

- **`fix_onnx_windows.bat`** - Automatic ONNX fix for Windows
- **`fix_onnx.py`** - Cross-platform ONNX fix with diagnostics
- **`install_windows.bat`** - Complete Windows installation
- **`install_linux.sh`** - Complete Linux installation

## ✅ Verification Checklist

After installation, verify everything works:

```python
# Run this in Python
import torch
import onnx
import onnxruntime
print("✓ All imports successful!")
```

If you see "✓ All imports successful!" you're ready to go!

## 🎬 Next Steps

1. **Generate dataset**: `python src/data_generator.py`
2. **Train model**: `python src/train.py`
3. **Generate trajectories**: `python src/inference.py`
4. **Start API server**: `python api/app.py`

## 💡 Pro Tips

- Always activate virtual environment: `venv\Scripts\activate`
- Use `--help` flag to see options: `python src/train.py --help`
- Monitor training: `tensorboard --logdir logs`
- Check GPU: `python -c "import torch; print(torch.cuda.is_available())"`

---

**Still stuck?** Create an issue on GitHub with:
- Your Python version: `python --version`
- Your OS: `systeminfo | findstr /B /C:"OS Name" /C:"OS Version"`
- The full error message

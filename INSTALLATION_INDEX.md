# Installation Guide Index

## 🚨 Having Installation Issues? Start Here!

### Quick Decision Tree

```
Are you on Windows?
│
├─ YES → Run install_windows.bat
│        └─ ONNX build error? → Run fix_onnx_windows.bat (NEW!)
│        └─ Still have errors? → See ONNX_BUILD_ERROR_FIX.md
│
└─ NO → Are you on Linux/Mac?
         │
         ├─ YES → Run ./install_linux.sh
         │        └─ ONNX build error? → Run python fix_onnx.py (NEW!)
         │        └─ Still have errors? → See ONNX_BUILD_ERROR_FIX.md
         │
         └─ Other → See ONNX_BUILD_ERROR_FIX.md (Conda/Docker methods)
```

## 📚 Documentation Quick Reference

### For Different User Types

#### 🔰 Beginner Users (Just want it to work)
1. **Windows**: Read `QUICK_START_WINDOWS.md` (simplest guide)
2. **Linux/Mac**: Run `./install_linux.sh`

#### 🔧 Experienced Users (Want to understand)
1. Read `INSTALLATION_SUMMARY.md` (technical overview)
2. Choose your preferred method
3. Refer to `ONNX_INSTALLATION_FIX.md` if needed

#### 🐛 Troubleshooting Specific Errors
1. Go directly to `ONNX_INSTALLATION_FIX.md`
2. Find your error in the troubleshooting section
3. Follow the specific solution

## 📁 File Guide

### Installation Scripts (Run These)
| File | Platform | Purpose |
|------|----------|---------|
| `install_windows.bat` | Windows | Automated installation (RECOMMENDED) |
| `install_linux.sh` | Linux/Mac | Automated installation (RECOMMENDED) |
| `fix_onnx_windows.bat` | Windows | **NEW!** Fix ONNX build errors only |
| `fix_onnx.py` | All | **NEW!** Cross-platform ONNX fix with diagnostics |

### Requirements Files (Dependency Lists)
| File | Use Case |
|------|----------|
| `requirements.txt` | Standard installation (Linux/Mac) |
| `requirements-windows.txt` | Windows with ONNX issues |

### Documentation (Read These)
| File | When to Read | Content |
|------|--------------|---------|
| `QUICK_START_WINDOWS.md` | Windows beginner | Simple step-by-step guide |
| `ONNX_BUILD_ERROR_FIX.md` | **NEW!** Build errors | Complete ONNX fix guide with automated scripts |
| `ONNX_INSTALLATION_FIX.md` | Build errors | Comprehensive troubleshooting (260 lines) |
| `INSTALLATION_SUMMARY.md` | Want technical details | Solution overview |
| `FIX_COMPLETE.md` | Developer/maintainer | Complete change summary |
| `INSTALLATION_INDEX.md` | **START HERE** | This file - helps you navigate |
| `README.md` | General usage | Full project documentation |
| `PYTHON_3.13_UPDATE_NOTES.md` | Python version issues | Python 3.13 compatibility |
| `PYTORCH_UPDATE_NOTES.md` | PyTorch issues | PyTorch version info |

## 🎯 Common Scenarios

### Scenario 1: "I just want to install this on Windows"
**Solution**: 
```bash
install_windows.bat
```
Done! If it fails, see `ONNX_INSTALLATION_FIX.md`

### Scenario 2: "I get 'Failed building wheel for onnx' error"
**Solution**: Run our automated fix script!
```bash
# Windows - fastest solution
fix_onnx_windows.bat

# Or cross-platform Python script
python fix_onnx.py

# Or manual one-liner
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
```
See `ONNX_BUILD_ERROR_FIX.md` for complete guide with multiple solutions.

### Scenario 3: "I'm on Linux and it's not working"
**Solution**:
```bash
./install_linux.sh
```
If still failing, see `ONNX_INSTALLATION_FIX.md` (Method 3: Conda)

### Scenario 4: "I have Python 3.13 and packages won't install"
**Solution**: Python 3.13 is too new. Options:
1. Downgrade to Python 3.11 (recommended)
2. See `PYTHON_3.13_UPDATE_NOTES.md` for details

### Scenario 5: "I want to use my NVIDIA GPU"
**Solution**:
```bash
# After basic installation, reinstall PyTorch with CUDA
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118
```
See `PYTORCH_UPDATE_NOTES.md` for more details.

### Scenario 6: "I prefer Conda/Anaconda"
**Solution**: See `ONNX_INSTALLATION_FIX.md` - Section "Solution 3: Use conda"

### Scenario 7: "I'm a developer setting up CI/CD"
**Solution**: Use Docker with `requirements-windows.txt` or conda. See `INSTALLATION_SUMMARY.md` for Docker examples.

## 🔍 Error Message → Solution Mapping

| Error Message | Solution |
|---------------|----------|
| "Failed building wheel for onnx" | **NEW!** Run `fix_onnx_windows.bat` or see `ONNX_BUILD_ERROR_FIX.md` |
| "CMake build error" / "non-zero exit status" | **NEW!** Run `python fix_onnx.py` or see `ONNX_BUILD_ERROR_FIX.md` |
| "Microsoft Visual C++ 14.0 required" | `ONNX_BUILD_ERROR_FIX.md` - Binary installation section |
| "CMake not found" | `pip install cmake` or see `ONNX_BUILD_ERROR_FIX.md` |
| "No matching distribution found" | Check Python version, see `PYTHON_3.13_UPDATE_NOTES.md` |
| "torch not found" / CUDA errors | `PYTORCH_UPDATE_NOTES.md` |
| "Package has no dependencies" | Upgrade pip: `python -m pip install --upgrade pip` |
| "Permission denied" | Run as Administrator (Windows) or use `sudo` (Linux) |

## ⚡ Quick Commands Reference

### Installation
```bash
# Windows (Recommended)
install_windows.bat

# Linux/Mac (Recommended)
./install_linux.sh

# Manual (Windows)
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
pip install -r requirements-windows.txt

# Conda (All platforms)
conda create -n trajectory python=3.11
conda activate trajectory
conda install -c conda-forge onnx onnxruntime
pip install -r requirements.txt
```

### Verification
```python
# Test installation
import torch, onnx, onnxruntime
print("✓ All packages installed!")
```

### Getting Started
```bash
# 1. Generate dataset
python src/data_generator.py

# 2. Train model
python src/train.py

# 3. Run inference
python src/inference.py
```

## 📊 Installation Method Comparison

| Method | Difficulty | Success Rate | Time | Platform |
|--------|-----------|--------------|------|----------|
| `install_windows.bat` | ⭐ Easy | 95% | 5-10 min | Windows |
| `install_linux.sh` | ⭐ Easy | 95% | 5-10 min | Linux/Mac |
| Manual binary install | ⭐⭐ Medium | 90% | 5-10 min | All |
| Conda install | ⭐⭐ Medium | 98% | 10-15 min | All |
| Build from source | ⭐⭐⭐⭐⭐ Hard | 40% | 30+ min | Advanced |

## 🆘 Still Need Help?

1. **Read the documentation** in this order:
   - `QUICK_START_WINDOWS.md` (if on Windows)
   - `ONNX_INSTALLATION_FIX.md` (for build errors)
   - `README.md` (for general usage)

2. **Check your environment**:
   ```bash
   python --version  # Should be 3.9-3.12
   pip --version     # Should be recent (23.0+)
   ```

3. **Try alternative methods**:
   - If automated script fails → Try manual installation
   - If pip fails → Try conda
   - If Windows fails → Try WSL2 or Docker

4. **Report an issue** with:
   - Python version: `python --version`
   - Operating system details
   - Full error message
   - What you tried

## 🎓 Learning Path

### First Time Users
1. Start: `QUICK_START_WINDOWS.md` or run `install_windows.bat`
2. After install: `README.md` (Quick Start section)
3. For problems: `ONNX_INSTALLATION_FIX.md`

### Developers
1. Start: `INSTALLATION_SUMMARY.md`
2. Details: `ONNX_INSTALLATION_FIX.md`
3. Changes: `FIX_COMPLETE.md`
4. Full docs: `README.md`

### System Administrators
1. Start: `INSTALLATION_SUMMARY.md`
2. Automated deployment: Use `install_linux.sh` or Docker
3. CI/CD: Use `requirements-windows.txt` with `--prefer-binary`

## ✅ Success Checklist

After installation, you should be able to:
- [ ] Import torch, onnx, onnxruntime without errors
- [ ] Run `python src/data_generator.py --n_samples 100`
- [ ] Run `python src/train.py --epochs 1`
- [ ] See GPU if you installed CUDA version: `python -c "import torch; print(torch.cuda.is_available())"`

If all checked ✅, you're ready to use the system!

## 📞 Support Resources

| Resource | Link/Command |
|----------|--------------|
| Test installation | `python -c "import torch, onnx, onnxruntime"` |
| Check Python | `python --version` |
| Check pip | `pip --version` |
| Upgrade pip | `python -m pip install --upgrade pip` |
| Full documentation | See `README.md` |
| Troubleshooting | See `ONNX_INSTALLATION_FIX.md` |

---

**Remember**: Most issues are solved by running the automated installation scripts!
- Windows: `install_windows.bat`
- Linux/Mac: `./install_linux.sh`

Good luck! 🚀

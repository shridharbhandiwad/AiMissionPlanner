# Quick Fix: Missing Dependencies

## ⚡ Fastest Solution

**On Windows (in your `missionplannerenv` environment):**

```bash
pip install numpy scipy PyQt5 PyQtGraph PyOpenGL PyOpenGL_accelerate
```

Then verify:

```bash
python run_trajectory_gui_safe.py
```

---

## 📋 What Happened?

The GUI requires 5 core packages that weren't installed:

| Package | Purpose | Status |
|---------|---------|--------|
| NumPy | Numerical computations | ❌ Missing |
| SciPy | Scientific algorithms | ❌ Missing |
| PyQt5 | GUI framework | ✅ Available (but not installed) |
| PyQtGraph | 3D graphics | ❌ Missing |
| PyOpenGL | OpenGL bindings | ❌ Missing |

---

## 🔧 Step-by-Step Fix

### 1. Activate your conda environment

```bash
conda activate missionplannerenv
```

### 2. Install missing packages

```bash
pip install numpy==1.26.4 scipy==1.14.1 PyQt5==5.15.11 PyQtGraph==0.13.7 PyOpenGL==3.1.7 PyOpenGL_accelerate
```

### 3. Verify installation

```bash
python diagnose_gui_startup.py
```

**Expected output:**
```
NumPy: ✓
PyQt5: ✓
PyQtGraph: ✓
PyQtGraph OpenGL: ✓
PyOpenGL: ✓
SciPy: ✓
```

### 4. Run the GUI

```bash
python run_trajectory_gui_safe.py
```

---

## 🚀 Alternative: Install All Dependencies

To install all project dependencies (not just GUI):

```bash
pip install -r requirements.txt
```

---

## 🛠️ Automated Fix Script

**Windows:**
```bash
fix_dependencies.bat
```

**Linux/Mac:**
```bash
bash fix_dependencies.sh
```

---

## ❓ Common Issues

### "pip: command not found"
**Solution:** Make sure conda environment is activated:
```bash
conda activate missionplannerenv
```

### "python: command not found"
**Solution:** Use `python3` instead:
```bash
python3 run_trajectory_gui_safe.py
```

### Packages install but GUI still fails
**Solution:** Check if you're using the correct Python:
```bash
which python
pip list | grep -i "pyqt\|numpy\|scipy"
```

### PyOpenGL errors on import
**Solution:** This is normal in headless environments (servers without displays). The GUI should work fine on Windows with a display.

---

## ✅ Success Checklist

- [ ] Conda environment `missionplannerenv` is activated
- [ ] All 5 packages are installed (run `pip list` to verify)
- [ ] Diagnostic script shows all ✓ marks
- [ ] GUI launches without errors

---

## 📚 Related Documentation

- **[DEPENDENCY_FIX_GUIDE.md](DEPENDENCY_FIX_GUIDE.md)** - Detailed troubleshooting
- **[GUI_TROUBLESHOOTING.md](GUI_TROUBLESHOOTING.md)** - GUI-specific issues
- **[INSTALLATION_SUMMARY.md](INSTALLATION_SUMMARY.md)** - Full installation guide
- **[README.md](README.md)** - Project overview

---

**Still stuck?** Run the full diagnostic:
```bash
python diagnose_environment.py
```

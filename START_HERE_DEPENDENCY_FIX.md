# 🚀 START HERE: Dependency Fix

## ⚠️ Current Issue

Your trajectory GUI can't start because **5 packages are missing**:
- ❌ NumPy
- ❌ SciPy  
- ❌ PyQt5
- ❌ PyQtGraph
- ❌ PyOpenGL

---

## ✅ **FASTEST FIX** (30 seconds)

On your **Windows machine**, open Command Prompt and run:

```bash
cd "D:\Zoppler Projects\AiMissionPlanner"
conda activate missionplannerenv
pip install numpy scipy PyQt5 PyQtGraph PyOpenGL
python run_trajectory_gui_safe.py
```

**Done!** The GUI should now open.

---

## 🔧 Alternative: Automated Fix

Run the batch file:

```bash
fix_dependencies.bat
```

This will:
1. ✅ Install all missing packages automatically
2. ✅ Test each dependency
3. ✅ Show you if everything works
4. ✅ Tell you what to do next

---

## 📋 What the Fix Does

### Installs These Packages:
```
numpy==1.26.4          (18 MB) - Math and arrays
scipy==1.14.1          (41 MB) - Scientific algorithms  
PyQt5==5.15.11         (69 MB) - GUI framework
PyQtGraph==0.13.7      (2 MB)  - 3D graphics
PyOpenGL==3.1.7        (2 MB)  - OpenGL support
```

**Total:** ~132 MB | **Time:** 2-5 minutes

---

## ✅ Verify It Worked

Run the diagnostic:

```bash
python diagnose_gui_startup.py
```

**Success looks like:**
```
✓ NumPy
✓ PyQt5
✓ PyQtGraph
✓ PyQtGraph OpenGL
✓ PyOpenGL
✓ SciPy

All dependencies working correctly!
```

---

## 🎯 Then Launch the GUI

```bash
python run_trajectory_gui_safe.py
```

You should see:
- ✅ 3D visualization window
- ✅ Control panel with trajectory types
- ✅ Real-time parameter adjustments
- ✅ No error messages

---

## 📚 More Information

### Quick References
- **`FIX_INSTRUCTIONS.txt`** - Simple text instructions
- **`QUICK_FIX_DEPENDENCIES.md`** - Troubleshooting guide

### Detailed Guides  
- **`DEPENDENCY_FIX_COMPLETE.md`** - Comprehensive walkthrough
- **`DEPENDENCY_FIX_GUIDE.md`** - Step-by-step instructions
- **`GUI_TROUBLESHOOTING.md`** - GUI-specific problems

### Automation
- **`fix_dependencies.bat`** - Windows installer
- **`fix_dependencies.sh`** - Linux/Mac installer
- **`environment.yml`** - Conda environment file

---

## ❓ Common Questions

### Q: Why didn't these install automatically?
**A:** The `requirements.txt` lists them, but you need to run `pip install -r requirements.txt` to actually install them.

### Q: Will this affect my other Python projects?
**A:** No! You're in the isolated `missionplannerenv` conda environment.

### Q: How much disk space do I need?
**A:** ~200 MB free space (for packages + cache).

### Q: Can I use different versions?
**A:** The specified versions are tested and known to work together. Using different versions may cause conflicts.

---

## 🚨 Troubleshooting

### "conda: command not found"
```bash
# Use full path to Anaconda
C:\Users\YourUsername\Anaconda3\Scripts\activate.bat missionplannerenv
```

### "pip: command not found"  
Make sure conda environment is activated:
```bash
conda activate missionplannerenv
where pip
```

### Packages install but GUI still fails
```bash
# Check you're using the right Python
where python
python --version

# Verify packages are visible
pip list | findstr "PyQt numpy scipy"
```

### PyOpenGL errors
Try reinstalling with accelerate:
```bash
pip uninstall PyOpenGL
pip install PyOpenGL==3.1.7 PyOpenGL_accelerate
```

---

## 🎉 Success Checklist

- [ ] Opened Command Prompt on Windows
- [ ] Navigated to project directory
- [ ] Activated `missionplannerenv` 
- [ ] Ran `pip install` command
- [ ] All packages installed without errors
- [ ] Diagnostic shows all ✓ marks
- [ ] GUI launches and shows 3D window
- [ ] Can select trajectory types

---

## 🆘 Still Stuck?

Run the full environment diagnostic:

```bash
python diagnose_environment.py
```

This shows:
- Python version and path
- All installed packages
- System information
- Detailed error logs

---

## 💡 Pro Tip

Install all project dependencies at once:

```bash
pip install -r requirements.txt
```

This installs everything needed for:
- ✅ GUI (PyQt5, PyQtGraph, OpenGL)
- ✅ Training (PyTorch, TensorBoard)
- ✅ Data processing (NumPy, SciPy, Pandas)
- ✅ Visualization (Matplotlib, Plotly)
- ✅ Model export (ONNX)
- ✅ API service (FastAPI)

---

**Ready to fix it?** Just run those 4 commands and you're done! 🚀

# 📑 Dependency Fix Documentation Index

## 🎯 Start Here

**→ [START_HERE_DEPENDENCY_FIX.md](START_HERE_DEPENDENCY_FIX.md)** ⭐ **RECOMMENDED**  
Complete guide with fastest fix (30 seconds)

**→ [FIX_INSTRUCTIONS.txt](FIX_INSTRUCTIONS.txt)**  
Plain text quick reference

---

## 🚀 Quick Fixes

### For Busy People
1. Open Command Prompt on Windows
2. Run these 4 commands:
   ```bash
   cd "D:\Zoppler Projects\AiMissionPlanner"
   conda activate missionplannerenv
   pip install numpy scipy PyQt5 PyQtGraph PyOpenGL
   python run_trajectory_gui_safe.py
   ```
3. Done! ✅

### For Automation Lovers
```bash
fix_dependencies.bat
```
Installs everything automatically.

---

## 📚 Documentation Files

### Quick References (1-2 min read)
- **[FIX_INSTRUCTIONS.txt](FIX_INSTRUCTIONS.txt)** - Simple text version
- **[QUICK_FIX_DEPENDENCIES.md](QUICK_FIX_DEPENDENCIES.md)** - Fast troubleshooting

### Comprehensive Guides (5-10 min read)
- **[DEPENDENCY_FIX_COMPLETE.md](DEPENDENCY_FIX_COMPLETE.md)** - Full walkthrough
- **[DEPENDENCY_FIX_GUIDE.md](DEPENDENCY_FIX_GUIDE.md)** - Detailed instructions
- **[GUI_TROUBLESHOOTING.md](GUI_TROUBLESHOOTING.md)** - GUI-specific issues

### Reference Files
- **[environment.yml](environment.yml)** - Conda environment specification
- **[requirements.txt](requirements.txt)** - Complete Python dependencies

---

## 🔧 Automation Scripts

### Windows
- **[fix_dependencies.bat](fix_dependencies.bat)** - Auto-install all missing packages
- **[run_trajectory_gui.bat](run_trajectory_gui.bat)** - Launch GUI after fix
- **[diagnose_gui.bat](diagnose_gui.bat)** - Test dependencies

### Linux/Mac
- **[fix_dependencies.sh](fix_dependencies.sh)** - Auto-install all missing packages
- **[run_trajectory_gui.sh](run_trajectory_gui.sh)** - Launch GUI after fix

---

## 🔍 Diagnostic Tools

### Test Dependencies
```bash
python diagnose_gui_startup.py    # Test all GUI dependencies
python diagnose_numpy.py           # Test NumPy specifically
python diagnose_environment.py     # Full environment info
python test_basic_gui.py           # Test PyQt5 only
```

### Check Installation
```bash
pip list                           # Show all installed packages
pip show numpy pyqt5 scipy        # Show specific packages
conda env list                     # Show conda environments
```

---

## 📦 What Gets Installed

| Package | Version | Size | Purpose |
|---------|---------|------|---------|
| **NumPy** | 1.26.4 | 18 MB | Numerical arrays & math |
| **SciPy** | 1.14.1 | 41 MB | Scientific algorithms |
| **PyQt5** | 5.15.11 | 69 MB | GUI framework |
| **PyQtGraph** | 0.13.7 | 2 MB | Real-time 3D plotting |
| **PyOpenGL** | 3.1.7 | 2 MB | OpenGL bindings |

**Total:** ~132 MB | **Time:** 2-5 minutes

---

## 🎯 Decision Tree

### "Which guide should I read?"

```
Do you want the absolute fastest fix?
  YES → Read: START_HERE_DEPENDENCY_FIX.md (30 seconds)
  NO  → Continue below

Do you prefer automation?
  YES → Run: fix_dependencies.bat
  NO  → Continue below

Do you want detailed explanations?
  YES → Read: DEPENDENCY_FIX_COMPLETE.md
  NO  → Read: QUICK_FIX_DEPENDENCIES.md

Are you having specific issues?
  YES → Read: DEPENDENCY_FIX_GUIDE.md (Troubleshooting section)
  NO  → You're all set!
```

---

## ✅ Success Verification

### After Installing

1. **Test dependencies:**
   ```bash
   python diagnose_gui_startup.py
   ```
   
2. **Expected output:**
   ```
   NumPy: ✓
   PyQt5: ✓
   PyQtGraph: ✓
   PyQtGraph OpenGL: ✓
   PyOpenGL: ✓
   SciPy: ✓
   ```

3. **Launch GUI:**
   ```bash
   python run_trajectory_gui_safe.py
   ```

4. **Verify GUI works:**
   - ✅ 3D window opens
   - ✅ Control panel visible
   - ✅ Can select trajectory types
   - ✅ 3D visualization renders

---

## 🆘 Troubleshooting Workflow

### Step 1: Identify the Issue

```bash
python diagnose_gui_startup.py
```

### Step 2: Check Common Causes

| Symptom | Cause | Solution |
|---------|-------|----------|
| "command not found: python" | Wrong environment | `conda activate missionplannerenv` |
| "ModuleNotFoundError" | Packages not installed | Run `pip install` commands |
| Packages install but still fail | Wrong Python | Check `where python` |
| PyOpenGL import errors | No display/graphics | Normal on servers; works on Windows |

### Step 3: Get Detailed Help

Read the appropriate guide:
- **General issues** → DEPENDENCY_FIX_GUIDE.md
- **Installation problems** → DEPENDENCY_FIX_COMPLETE.md
- **GUI won't open** → GUI_TROUBLESHOOTING.md

### Step 4: Full Diagnostic

```bash
python diagnose_environment.py
```

Provides:
- Python version and location
- All installed packages
- System information
- Environment variables
- Detailed error traces

---

## 📞 Quick Support Reference

### Error: "No module named 'numpy'"
**Fix:** `pip install numpy==1.26.4`

### Error: "No module named 'PyQt5'"
**Fix:** `pip install PyQt5==5.15.11`

### Error: "No module named 'pyqtgraph'"
**Fix:** `pip install PyQtGraph==0.13.7`

### Error: "No module named 'OpenGL'"
**Fix:** `pip install PyOpenGL==3.1.7`

### Error: "No module named 'scipy'"
**Fix:** `pip install scipy==1.14.1`

### Install Everything at Once
**Fix:** `pip install -r requirements.txt`

---

## 🎓 Understanding the Problem

### Why It Happened

The conda environment `missionplannerenv` was created but the GUI packages were never installed. The project's `requirements.txt` lists all dependencies, but you must explicitly install them with:

```bash
pip install -r requirements.txt
```

### The Fix

Install the 5 missing packages:
- NumPy (math operations)
- SciPy (trajectory algorithms)
- PyQt5 (GUI framework)
- PyQtGraph (3D visualization)
- PyOpenGL (OpenGL support)

### Prevention

When setting up a new environment, always:
```bash
conda create -n myenv python=3.12
conda activate myenv
pip install -r requirements.txt
```

---

## 🔗 Related Documentation

### Installation Guides
- **[INSTALLATION_SUMMARY.md](INSTALLATION_SUMMARY.md)** - Full project setup
- **[README_INSTALLATION.md](README_INSTALLATION.md)** - Installation guide
- **[QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md)** - Windows-specific

### GUI Documentation
- **[TRAJECTORY_GUI_README.md](TRAJECTORY_GUI_README.md)** - GUI user guide
- **[TRAJECTORY_GUI_QUICK_START.md](TRAJECTORY_GUI_QUICK_START.md)** - Quick start
- **[GUI_TROUBLESHOOTING.md](GUI_TROUBLESHOOTING.md)** - GUI problems

### Project Documentation
- **[README.md](README.md)** - Main project documentation
- **[PROBLEM_FORMULATION.md](PROBLEM_FORMULATION.md)** - Technical details

---

## 💡 Pro Tips

### Tip 1: Use Virtual Environments
Always use conda/virtualenv to isolate project dependencies:
```bash
conda create -n projectname python=3.12
conda activate projectname
```

### Tip 2: Install from requirements.txt
Get all dependencies at once:
```bash
pip install -r requirements.txt
```

### Tip 3: Use the Batch File
For Windows, the `.bat` files automate everything:
```bash
fix_dependencies.bat
```

### Tip 4: Keep Dependencies Updated
Periodically update packages:
```bash
pip install --upgrade numpy scipy PyQt5 PyQtGraph PyOpenGL
```

### Tip 5: Document Your Environment
Export your working environment:
```bash
pip freeze > my_working_requirements.txt
conda env export > my_working_environment.yml
```

---

## 🎉 You're All Set!

Follow any of these paths to fix the issue:

**Fastest:** Run 4 commands from START_HERE_DEPENDENCY_FIX.md  
**Easiest:** Run `fix_dependencies.bat`  
**Thorough:** Read DEPENDENCY_FIX_COMPLETE.md  

Choose what works best for you! 🚀

---

**Questions?** All guides include troubleshooting sections.  
**Still stuck?** Run `python diagnose_environment.py` for detailed diagnostics.

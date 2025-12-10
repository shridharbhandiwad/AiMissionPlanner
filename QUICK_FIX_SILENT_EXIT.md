# Quick Fix: App Exiting Silently

## Your Issue
App exits after "Checking NumPy..." with no error message.

## Immediate Solutions (Try in Order)

### 1️⃣ Use Safe Launcher (RECOMMENDED)
Double-click this file on Windows:
```
run_trajectory_gui_safe.bat
```

Or run:
```bash
python run_trajectory_gui_safe.py
```

This will tell you exactly what's wrong!

---

### 2️⃣ Diagnose NumPy
Double-click:
```
diagnose_numpy.bat
```

Or run:
```bash
python diagnose_numpy.py
```

---

### 3️⃣ Install Visual C++ (Windows)
Download and install:
https://aka.ms/vs/17/release/vc_redist.x64.exe

Then restart your computer.

---

### 4️⃣ Reinstall NumPy
```bash
pip uninstall -y numpy
pip cache purge
pip install numpy
```

---

### 5️⃣ Use Conda NumPy (Best for Windows)
```bash
conda install -c conda-forge numpy
```

---

## Test if Fixed

```bash
python -c "import numpy; print('NumPy works!')"
```

If that works, try:
```bash
python run_trajectory_gui_safe.py
```

---

## Need More Help?

Read the detailed guide:
- **FIX_SILENT_EXIT.md** - Complete solutions
- **TRAJECTORY_GUI_SILENT_EXIT_FIX.md** - Troubleshooting guide

---

## What We Created

| File | What It Does |
|------|--------------|
| `run_trajectory_gui_safe.py` | Safe launcher that catches crashes |
| `run_trajectory_gui_safe.bat` | Windows shortcut for safe launcher |
| `diagnose_numpy.py` | Tests NumPy specifically |
| `diagnose_numpy.bat` | Windows shortcut for NumPy test |
| `FIX_SILENT_EXIT.md` | Complete troubleshooting guide |

---

**TL;DR:** Just run `run_trajectory_gui_safe.bat` and it will tell you what's wrong! 🎯

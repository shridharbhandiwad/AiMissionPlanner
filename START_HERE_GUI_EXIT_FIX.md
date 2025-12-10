# 🚀 START HERE - GUI Silent Exit Fix

## Your Problem
```
(missionplannerenv) (base) D:\Zoppler Projects\AiMissionPlanner>python run_trajectory_gui.py
...
Checking dependencies...

(missionplannerenv) (base) D:\Zoppler Projects\AiMissionPlanner>
```

The GUI exits immediately with no error message.

## ✅ FIXED! Try This Now

### Step 1: Run the GUI Again
```bash
python run_trajectory_gui.py
```

**It will now show you exactly what's wrong!**

### Step 2: Most Likely Fix
If it says PyOpenGL is missing:
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

Then run again:
```bash
python run_trajectory_gui.py
```

### Step 3: Still Not Working?
Run the diagnostic tool:
```bash
python diagnose_gui_startup.py
```

It will tell you exactly what to do next.

## What Changed?

The launcher (`run_trajectory_gui.py`) now:
- Shows progress: `[1/5] Checking NumPy... ✓`
- Catches ALL errors (not just import errors)
- Shows detailed error messages
- Suggests solutions
- Never exits silently

## Quick Fixes Reference

| Problem | Solution |
|---------|----------|
| PyOpenGL missing | `pip install PyOpenGL PyOpenGL_accelerate` |
| Graphics driver issue | Update drivers or set `LIBGL_ALWAYS_SOFTWARE=1` |
| PyQt5 broken | `pip uninstall PyQt5 && pip install PyQt5` |
| Python 3.12+ | Use Python 3.11: `conda create -n env python=3.11` |

## Expected Output (Success)

```
Checking dependencies...

  [1/5] Checking NumPy... ✓
  [2/5] Checking PyQt5... ✓
  [3/5] Checking PyQtGraph... ✓
  [4/5] Checking PyQtGraph OpenGL... ✓
  [5/5] Checking SciPy... ✓

All dependencies found!

Initializing GUI...
  - Importing trajectory_gui module...
  - Module imported successfully
  - Starting main GUI application...
Creating GUI window...
```

Then the GUI window opens! 🎉

## Need More Help?

1. **Quick Guide**: `GUI_FIX_QUICK_START.md`
2. **Detailed Guide**: `TRAJECTORY_GUI_SILENT_EXIT_FIX.md`
3. **Complete README**: `README_GUI_SILENT_EXIT_FIX.md`

## Diagnostic Tools

| Tool | What It Does |
|------|--------------|
| `python diagnose_gui_startup.py` | Tests everything, shows detailed errors |
| `python test_basic_gui.py` | Tests PyQt5 without OpenGL |
| `diagnose_gui.bat` | Windows batch version of diagnostics |

## Still Stuck?

Save diagnostic output:
```bash
python diagnose_gui_startup.py > error_log.txt
```

Check `error_log.txt` for detailed information.

---

**That's it!** Just run `python run_trajectory_gui.py` again and follow the on-screen instructions.

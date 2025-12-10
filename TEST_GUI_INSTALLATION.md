# GUI Installation Test Guide

This guide helps verify that your 3D Trajectory Generator GUI is properly installed and ready to use.

## Prerequisites Check

### 1. Python Version

```bash
python --version
# or
python3 --version

# Required: Python 3.8 or higher
```

### 2. Core Dependencies

Test if core dependencies are installed:

```bash
python3 -c "import numpy; print('✅ NumPy:', numpy.__version__)"
python3 -c "import scipy; print('✅ SciPy:', scipy.__version__)"
python3 -c "import matplotlib; print('✅ Matplotlib:', matplotlib.__version__)"
```

### 3. GUI Dependencies

Test if GUI dependencies are installed:

```bash
python3 -c "import PyQt5; print('✅ PyQt5:', PyQt5.Qt.PYQT_VERSION_STR)"
python3 -c "import pyqtgraph; print('✅ PyQtGraph:', pyqtgraph.__version__)"
python3 -c "import OpenGL; print('✅ PyOpenGL:', OpenGL.__version__)"
```

**If any test fails**, install the missing package:

```bash
pip install PyQt5 PyQtGraph PyOpenGL

# Or install all requirements
pip install -r requirements.txt
```

---

## Functionality Tests

### Test 1: Core Trajectory Generation (No GUI)

```bash
cd /workspace
python3 -c "
import sys
sys.path.insert(0, 'src')
from trajectory_gui import TrajectoryParameters, Advanced3DTrajectoryGenerator

gen = Advanced3DTrajectoryGenerator()
params = TrajectoryParameters()
traj = gen.generate_trajectory(params)
metrics = gen.calculate_metrics(traj, params)

print('✅ Core trajectory generation: PASSED')
print(f'  Generated {len(traj)} waypoints')
print(f'  Path length: {metrics[\"path_length\"]:.2f} m')
"
```

Expected output:
```
✅ Core trajectory generation: PASSED
  Generated 50 waypoints
  Path length: 1044.xx m
```

### Test 2: Multiple Trajectory Types

```bash
python3 -c "
import sys
sys.path.insert(0, 'src')
from trajectory_gui import TrajectoryParameters, Advanced3DTrajectoryGenerator

gen = Advanced3DTrajectoryGenerator()
params = TrajectoryParameters()

types = ['bezier', 'circular', 's_curve', 'helix', 'combat_maneuver']
for t in types:
    params.trajectory_type = t
    traj = gen.generate_trajectory(params)
    print(f'✅ {t:20s}: {len(traj)} waypoints')

print('✅ All trajectory types: PASSED')
"
```

Expected output:
```
✅ bezier              : 50 waypoints
✅ circular            : 50 waypoints
✅ s_curve             : 50 waypoints
✅ helix               : 50 waypoints
✅ combat_maneuver     : 50 waypoints
✅ All trajectory types: PASSED
```

### Test 3: Metrics Calculation

```bash
python3 -c "
import sys
sys.path.insert(0, 'src')
from trajectory_gui import TrajectoryParameters, Advanced3DTrajectoryGenerator

gen = Advanced3DTrajectoryGenerator()
params = TrajectoryParameters()
traj = gen.generate_trajectory(params)
metrics = gen.calculate_metrics(traj, params)

required_metrics = ['path_length', 'path_efficiency', 'avg_curvature', 
                   'max_curvature', 'max_g_force', 'min_altitude', 'max_altitude']

for key in required_metrics:
    if key in metrics:
        print(f'✅ {key}: {metrics[key]}')
    else:
        print(f'❌ Missing metric: {key}')

print('✅ Metrics calculation: PASSED')
"
```

### Test 4: Parameter Serialization

```bash
python3 -c "
import sys
import json
sys.path.insert(0, 'src')
from trajectory_gui import TrajectoryParameters

params = TrajectoryParameters()
params_dict = params.to_dict()

# Save to JSON
with open('/tmp/test_params.json', 'w') as f:
    json.dump(params_dict, f)

# Load from JSON
with open('/tmp/test_params.json', 'r') as f:
    loaded_dict = json.load(f)

new_params = TrajectoryParameters()
new_params.from_dict(loaded_dict)

print('✅ Parameter serialization: PASSED')
print(f'  Start point: {new_params.start_x}, {new_params.start_y}, {new_params.start_z}')
print(f'  End point: {new_params.end_x}, {new_params.end_y}, {new_params.end_z}')
"
```

---

## GUI Test (Visual)

### Test 5: Launch GUI

This test requires a display (X11, Wayland, or Windows GUI).

```bash
# Test if display is available
echo $DISPLAY  # Linux
# Should show ":0" or similar

# Launch GUI
python3 run_trajectory_gui.py
```

**Expected behavior**:
- Window opens with title "3D Trajectory Generator"
- Left panel shows tabbed controls
- Right panel shows 3D visualization with grid and axes
- No error messages in console

**If GUI doesn't open**:

1. Check display is available (Linux):
   ```bash
   echo $DISPLAY
   xhost +  # Allow X11 connections if needed
   ```

2. Test basic Qt functionality:
   ```bash
   python3 -c "from PyQt5.QtWidgets import QApplication; app = QApplication([]); print('✅ Qt works')"
   ```

3. Try headless mode (for servers):
   ```bash
   # Install virtual display
   sudo apt-get install xvfb  # Linux
   
   # Run with virtual display
   xvfb-run python3 run_trajectory_gui.py
   ```

### Test 6: GUI Functionality (Manual)

Once GUI is open, test these features:

- [ ] **Basic Tab**
  - [ ] Can modify start point X, Y, Z
  - [ ] Can modify end point X, Y, Z
  - [ ] Can adjust max altitude, speed, etc.

- [ ] **Advanced Tab**
  - [ ] Can adjust smoothness slider
  - [ ] Can modify banking angle, climb rate

- [ ] **Trajectory Type Tab**
  - [ ] Can select different trajectory types
  - [ ] Description updates when type changes

- [ ] **Generate Trajectory**
  - [ ] Click "Generate Trajectory" button
  - [ ] Trajectory appears in 3D view
  - [ ] Metrics update in Metrics tab
  - [ ] Can rotate 3D view with mouse
  - [ ] Can zoom with scroll wheel

- [ ] **Multiple Trajectories**
  - [ ] Generate first trajectory
  - [ ] Change parameters
  - [ ] Generate second trajectory
  - [ ] Both trajectories visible

- [ ] **Save/Load**
  - [ ] Click "Save Trajectory"
  - [ ] File dialog opens
  - [ ] Can save as .npy or .json
  - [ ] Click "Load Parameters"
  - [ ] Can load saved .json file

- [ ] **Clear**
  - [ ] Click "Clear All"
  - [ ] All trajectories disappear
  - [ ] Metrics reset

---

## Common Issues and Solutions

### Issue: PyQt5 not found

```bash
pip install PyQt5==5.15.11

# Or try system package (Linux)
sudo apt-get install python3-pyqt5

# Or use conda
conda install pyqt
```

### Issue: PyQtGraph not found

```bash
pip install pyqtgraph==0.13.7
```

### Issue: OpenGL errors

```bash
# Install OpenGL
pip install PyOpenGL PyOpenGL-accelerate

# Linux: Install system OpenGL
sudo apt-get install libgl1-mesa-glx libglu1-mesa

# Update graphics drivers
```

### Issue: "No module named 'trajectory_gui'"

```bash
# Make sure you're in the workspace directory
cd /workspace

# Run with correct Python path
python3 run_trajectory_gui.py

# Or explicitly add to path
export PYTHONPATH=/workspace/src:$PYTHONPATH
python3 run_trajectory_gui.py
```

### Issue: Display not available (Linux servers)

```bash
# Install virtual display
sudo apt-get install xvfb

# Run with virtual display
xvfb-run -a python3 run_trajectory_gui.py

# Or use VNC
vncserver :1
export DISPLAY=:1
python3 run_trajectory_gui.py
```

### Issue: GUI crashes on startup

```bash
# Check Qt platform plugin
export QT_DEBUG_PLUGINS=1
python3 run_trajectory_gui.py

# Try different Qt platform
export QT_QPA_PLATFORM=offscreen
python3 run_trajectory_gui.py
```

---

## Programmatic Testing

If you can't test the GUI visually, test programmatically:

```bash
cd /workspace
python3 examples/trajectory_gui_examples.py
```

This will:
- Generate 8 different trajectory types
- Save them as .npy files
- Create comparison visualization
- Print metrics for all trajectories

Expected output:
```
============================================================
Example 1: Basic Bezier Trajectory
============================================================
Generated 50 waypoints
Path length: 1044.xx m
...
All examples completed!
```

---

## Installation Summary

### Quick Install (All Requirements)

```bash
cd /workspace
pip install -r requirements.txt
```

### Minimal GUI Install

```bash
pip install PyQt5 PyQtGraph PyOpenGL numpy scipy matplotlib
```

### Verify Installation

```bash
# Test imports
python3 -c "import PyQt5, pyqtgraph, OpenGL; print('✅ All GUI packages installed')"

# Test trajectory generation
python3 -c "import sys; sys.path.insert(0, 'src'); from trajectory_gui import *; print('✅ Trajectory generator ready')"

# Run examples (no GUI)
python3 examples/trajectory_gui_examples.py
```

---

## Success Criteria

Your installation is successful if:

1. ✅ All Python imports work without errors
2. ✅ Core trajectory generation produces waypoints
3. ✅ All 12 trajectory types can be generated
4. ✅ Metrics calculation returns valid results
5. ✅ GUI launches (if display available)
6. ✅ 3D visualization renders correctly
7. ✅ Can generate and save trajectories

---

## Next Steps

Once all tests pass:

1. 📖 Read [TRAJECTORY_GUI_QUICK_START.md](TRAJECTORY_GUI_QUICK_START.md)
2. 🎮 Launch GUI: `python3 run_trajectory_gui.py`
3. 💻 Try examples: `python3 examples/trajectory_gui_examples.py`
4. 📚 Read full docs: [TRAJECTORY_GUI_README.md](TRAJECTORY_GUI_README.md)

---

**Good luck! 🚀**

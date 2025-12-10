# 🚀 Trajectory GUI - Quick Start Guide

**Get started in 3 minutes!**

---

## Step 1: Install Dependencies (1 minute)

```bash
# Install GUI packages
pip install PyQt5 PyQtGraph PyOpenGL

# Or install all requirements
pip install -r requirements.txt
```

---

## Step 2: Launch GUI (10 seconds)

### Windows:
```bash
run_trajectory_gui.bat
```

### Linux/Mac:
```bash
./run_trajectory_gui.sh
```

### Alternative:
```bash
python run_trajectory_gui.py
```

---

## Step 3: Create Your First Trajectory (1 minute)

### Quick Demo:

1. **Set Start Point** (Basic tab):
   - X: `0`
   - Y: `0`
   - Z: `100`

2. **Set End Point** (Basic tab):
   - X: `800`
   - Y: `600`
   - Z: `200`

3. **Choose Trajectory Type** (Trajectory Type tab):
   - Select: `Bezier` (smooth curve)

4. **Click Generate**:
   - Press the green "Generate Trajectory" button
   - Watch the 3D visualization appear!

5. **Interact with 3D View**:
   - **Rotate**: Left mouse drag
   - **Zoom**: Mouse scroll wheel
   - **Pan**: Right mouse drag

---

## Try Different Patterns

### 🔄 Circular Arc
```
Type: Circular
Turn Radius: 100m
```

### 🌀 Ascending Spiral
```
Type: Ascending Spiral
Turn Radius: 150m
Start Z: 100m
End Z: 500m
```

### ⚡ Combat Maneuver
```
Type: Combat Maneuver
Max G-Turn: 6.0
Max Speed: 300 m/s
```

### 🌊 S-Curve (Evasive)
```
Type: S-Curve
Smoothness: 0.9
Turn Radius: 120m
```

### 📐 L-Curve (Waypoint)
```
Type: L-Curve
Start: (0, 0, 100)
End: (500, 500, 150)
```

---

## Key Parameters Explained

### Basic Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| **Start/End Points** | 3D coordinates in meters | -5000 to 5000 |
| **Max Altitude** | Ceiling limit | 100-2000m |
| **Min Altitude** | Floor limit | 50-500m |
| **Max Speed** | Velocity limit | 100-500 m/s |
| **Max G-Turn** | Turn force limit | 2-8 g |
| **Turn Radius** | Minimum turn circle | 50-300m |
| **Waypoints** | Path resolution | 20-200 |

### Advanced Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| **Smoothness** | Path smoothness | 0.5-1.0 |
| **Banking Angle** | Roll angle in turns | 20-45° |
| **Climb Rate** | Ascent speed | 5-15 m/s |
| **Descent Rate** | Descent speed | 5-12 m/s |

---

## Common Use Cases

### ✈️ Commercial Flight Path
```
Start: (0, 0, 1000)      # Takeoff
End: (5000, 3000, 1500)  # Destination
Type: Bezier
Max Speed: 250 m/s
Max Altitude: 2000m
Smoothness: 0.9
```

### 🚁 Helicopter Patrol
```
Start: (0, 0, 50)
End: (1000, 1000, 80)
Type: Zigzag
Max Speed: 100 m/s
Min Altitude: 50m
```

### 🛩️ Aerobatic Display
```
Start: (0, 0, 200)
End: (500, 0, 300)
Type: Combat Maneuver
Max G-Turn: 6.0
Max Speed: 350 m/s
```

### 🎯 Tactical Approach
```
Start: (0, 0, 100)
End: (800, 600, 80)
Type: Terrain Following
Max Altitude: 150m
Min Altitude: 50m
```

---

## Save Your Work

### Save Trajectory:
1. Click "Save Trajectory" button
2. Choose format:
   - `.npy` - NumPy array (for Python)
   - `.json` - JSON format (with parameters)
3. Name your file

### Load Parameters:
1. Click "Load Parameters"
2. Select a `.json` file
3. Parameters automatically populate

---

## Generate Multiple Trajectories

Want to compare different paths?

1. Generate first trajectory
2. Change parameters (try different type)
3. Click "Generate Trajectory" again
4. Both trajectories display together!
5. Use "Clear All" to reset

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+G` | Generate Trajectory |
| `Ctrl+S` | Save Trajectory |
| `Ctrl+L` | Load Parameters |
| `Ctrl+C` | Clear All |
| `Esc` | Close Application |

*(Note: Implement in future version)*

---

## View Metrics

Check the **Metrics** tab to see:

- ✅ Path length vs. straight-line distance
- ✅ Path efficiency percentage
- ✅ Curvature analysis
- ✅ Estimated G-forces
- ✅ Altitude statistics

---

## Tips & Tricks

### 🎨 Better Visualization
- Generate 2-3 trajectories with different colors
- Compare circular vs. bezier vs. s-curve paths
- Rotate 3D view to see from different angles

### ⚡ Performance
- Use 50 waypoints for quick preview
- Use 100-200 waypoints for detailed paths
- More waypoints = smoother but slower

### 🎯 Realistic Paths
- Keep Max G-Turn under 6.0 for human pilots
- Match turn radius to speed (faster = larger radius)
- Use terrain following for low-altitude missions

### 🔄 Experimentation
- Start with Bezier (most versatile)
- Try Combat Maneuver for aggressive paths
- Use Spiral for climb/descent with lateral movement
- S-Curve is great for evasive maneuvers

---

## Troubleshooting

### GUI won't start?
```bash
# Install dependencies
pip install PyQt5 PyQtGraph PyOpenGL

# Check Python version (need 3.8+)
python --version
```

### 3D view is black?
```bash
# Update graphics drivers
# Or install OpenGL accelerate
pip install PyOpenGL-accelerate
```

### Trajectory looks weird?
- Check start/end are not too close (<50m)
- Verify min_altitude < max_altitude
- Ensure turn radius is reasonable (50-300m)

---

## Next Steps

📚 **Full Documentation**: See [TRAJECTORY_GUI_README.md](TRAJECTORY_GUI_README.md)

💻 **Programmatic Usage**: See [examples/trajectory_gui_examples.py](examples/trajectory_gui_examples.py)

🔬 **AI Training**: Use generated trajectories to train ML models

🚀 **Integration**: Export trajectories for simulation software

---

## Need Help?

1. Check [TRAJECTORY_GUI_README.md](TRAJECTORY_GUI_README.md)
2. Review [examples/trajectory_gui_examples.py](examples/trajectory_gui_examples.py)
3. See main [README.md](README.md) for project overview

---

**Happy trajectory designing! ✈️🚁🛩️**

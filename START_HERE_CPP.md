# 🚀 C++ Trajectory Generator - START HERE

## Welcome!

You now have a complete C++ application that:
- ✅ Receives **start and end points** as input
- ✅ Accepts **number of waypoints** as parameter
- ✅ Generates **top 5 trajectories** using AI
- ✅ **Plots them** in beautiful 3D

---

## ⚡ Quick Start (< 2 minutes)

```bash
# 1. Navigate to C++ directory
cd cpp

# 2. Build (auto-downloads dependencies)
./build.sh

# 3. Run with example
cd build
export LD_LIBRARY_PATH=../../libs/onnxruntime-linux-x64-1.16.3/lib:$LD_LIBRARY_PATH
./trajectory_app \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json \
    --start 0 0 100 \
    --end 800 600 200 \
    --csv
```

**Output:**
- `trajectories.png` - 3D plot of top 5 trajectories
- `trajectory_1.csv` through `trajectory_5.csv` - Data files
- Console statistics with quality rankings

---

## 📚 Documentation

### For Quick Start
👉 **[CPP_QUICK_START.md](CPP_QUICK_START.md)** (5 min read)
- One-command setup
- Common usage examples
- Quick troubleshooting

### For Complete Guide  
👉 **[CPP_APPLICATION_GUIDE.md](CPP_APPLICATION_GUIDE.md)** (15 min read)
- Full documentation
- All command-line options
- Performance benchmarks
- Integration guide
- API reference

### For Implementation Details
👉 **[CPP_IMPLEMENTATION_SUMMARY.md](CPP_IMPLEMENTATION_SUMMARY.md)** (10 min read)
- Architecture overview
- Feature list
- Quality metrics explained
- Customization guide

### For C++ API
👉 **[cpp/README.md](cpp/README.md)** (10 min read)
- Technical details
- API reference
- Build instructions
- Integration examples

---

## 🎯 What You Can Do

### Basic Usage

Generate trajectories between two points:
```bash
./trajectory_app --start 0 0 100 --end 800 600 200
```

### Custom Waypoints

Generate with more/fewer waypoints:
```bash
./trajectory_app --start 0 0 100 --end 800 600 200 --waypoints 75
```

### Export Data

Save trajectories to CSV:
```bash
./trajectory_app --start 0 0 100 --end 800 600 200 --csv
```

### No Plotting

Generate without visualization (faster):
```bash
./trajectory_app --start 0 0 100 --end 800 600 200 --no-plot --csv
```

---

## 🏗️ Project Structure

```
/workspace/
│
├── START_HERE_CPP.md           ← You are here! Start reading
│
├── CPP_QUICK_START.md          ← Quick start guide
├── CPP_APPLICATION_GUIDE.md    ← Complete documentation
├── CPP_IMPLEMENTATION_SUMMARY.md ← Technical summary
│
├── cpp/                        ← C++ application
│   ├── trajectory_app.cpp      ← Main application
│   ├── trajectory_inference.*  ← AI model inference
│   ├── trajectory_plotter.*    ← Visualization
│   ├── trajectory_metrics.*    ← Quality metrics
│   ├── build.sh                ← Build script
│   ├── run_example.sh          ← Example runner
│   ├── CMakeLists.txt          ← Build config
│   └── README.md               ← Technical docs
│
├── models/                     ← Trained AI model
│   ├── trajectory_generator.onnx
│   └── trajectory_generator_normalization.json
│
└── libs/                       ← Dependencies (auto-downloaded)
    └── onnxruntime-linux-x64-1.16.3/
```

---

## 💡 Example Scenarios

### Scenario 1: Short Mission

```bash
./trajectory_app \
    --start 0 0 50 \
    --end 200 150 80 \
    --waypoints 30 \
    --output short_mission.png
```

**Use case**: Local area planning

### Scenario 2: Long-Range Flight

```bash
./trajectory_app \
    --start -500 300 150 \
    --end 600 -400 250 \
    --waypoints 100 \
    --output long_range.png \
    --csv
```

**Use case**: Extended mission planning

### Scenario 3: Multiple Plans

```bash
# Plan A
./trajectory_app --start 0 0 100 --end 400 300 150 --output planA.png

# Plan B  
./trajectory_app --start 0 0 100 --end 400 -300 150 --output planB.png

# Plan C
./trajectory_app --start 0 0 100 --end -400 300 150 --output planC.png
```

**Use case**: Compare different routes

---

## 📊 Understanding Output

### Console Output

```
Top 5 Trajectories (ranked by quality):

 Rank   Length(m)  Smoothness  Efficiency       Score
-----------------------------------------------------
    1       938.8      0.9954       0.862      0.9564  ← BEST!
    2      2421.8      0.9435       0.080      0.5782
    3      3011.2      0.9494       0.083      0.5661
    4      4272.8      0.9692       0.098      0.5609
    5      4124.0      0.9694       0.089      0.5598
```

**What to look for:**
- **High Score** (> 0.9): Excellent trajectory
- **High Smoothness** (> 0.95): Very smooth path
- **High Efficiency** (> 0.8): Near-direct route

### Visualization

The PNG file shows:
- **Green dot**: Start point
- **Red dot**: End point
- **Colored lines**: Top 5 trajectories
- **Legend**: Trajectory rankings

### CSV Files

Each file contains waypoints:
```csv
Waypoint,X,Y,Z
0,0.00,0.00,100.00
1,15.35,12.42,105.67
...
```

Import into Excel, Python, MATLAB, etc.

---

## ⚙️ Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--start X Y Z` | Starting point | `--start 0 0 100` |
| `--end X Y Z` | Ending point | `--end 800 600 200` |
| `--waypoints N` | Number of points | `--waypoints 50` |
| `--output FILE` | Output PNG file | `--output result.png` |
| `--csv` | Save CSV files | `--csv` |
| `--no-plot` | Skip plotting | `--no-plot` |
| `--help` | Show help | `--help` |

---

## 🐛 Troubleshooting

### Build Fails

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake g++ gnuplot
```

### Model Not Found

Make sure model exists:
```bash
ls -lh /workspace/models/trajectory_generator.onnx
```

If missing, train it:
```bash
cd /workspace
python3 -m src.train --data_path data/trajectories.npz --save_dir models --epochs 20
python3 -m src.export_onnx --checkpoint models/best_model.pth --output models/trajectory_generator.onnx
```

### Library Error

Set library path:
```bash
export LD_LIBRARY_PATH=/workspace/libs/onnxruntime-linux-x64-1.16.3/lib:$LD_LIBRARY_PATH
```

### Gnuplot Missing

```bash
sudo apt-get install gnuplot
```

Or use without plotting:
```bash
./trajectory_app --no-plot --csv
```

---

## 🎓 Learn More

1. **Python Version**: See main `README.md` for Python implementation
2. **Model Training**: See `src/train.py` for training details
3. **ONNX Export**: See `src/export_onnx.py` for model export
4. **C++ Integration**: See `CPP_APPLICATION_GUIDE.md` for API usage

---

## 📞 Need Help?

1. ✅ Read `--help` output
2. ✅ Check error message in console
3. ✅ Review `CPP_QUICK_START.md`
4. ✅ See `CPP_APPLICATION_GUIDE.md`
5. ✅ Verify model files exist

---

## 🎉 You're Ready!

Everything is set up and ready to use. Choose your path:

- **Quick Test**: Run the example above
- **Learn More**: Read `CPP_QUICK_START.md`
- **Deep Dive**: Read `CPP_APPLICATION_GUIDE.md`
- **Integrate**: See API docs in `cpp/README.md`

---

## 📈 Next Steps

1. **Test it**: Run the quick start example
2. **Experiment**: Try different start/end points
3. **Analyze**: Load CSV files into your tools
4. **Integrate**: Use in your own projects
5. **Customize**: Modify ranking weights

---

## ✨ Features Summary

✅ **AI-Powered**: Uses trained neural network  
✅ **Fast**: < 1 second for complete workflow  
✅ **Quality-Ranked**: Best trajectories first  
✅ **Visualized**: Beautiful 3D plots  
✅ **Exportable**: CSV format for analysis  
✅ **Easy**: Simple command-line interface  
✅ **Documented**: Complete guides included  

---

## 🏆 Project Status

**Status**: ✅ READY TO USE  
**Build**: ✅ TESTED  
**Documentation**: ✅ COMPLETE  
**Performance**: ✅ OPTIMIZED  

---

**Let's generate some trajectories! 🚀**

```bash
cd cpp && ./build.sh && cd build && ./trajectory_app --start 0 0 100 --end 800 600 200 --csv
```

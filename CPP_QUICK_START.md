# C++ Trajectory Generator - Quick Start

## One-Command Setup and Run

```bash
# Clone or navigate to project
cd /workspace

# Build and run example
cd cpp && ./build.sh && cd build && \
export LD_LIBRARY_PATH=../../libs/onnxruntime-linux-x64-1.16.3/lib:$LD_LIBRARY_PATH && \
./trajectory_app \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json \
    --start 0 0 100 \
    --end 800 600 200 \
    --csv \
    --output my_trajectories.png
```

## What This Does

1. **Downloads ONNX Runtime** automatically
2. **Compiles** the C++ application
3. **Generates** 10 diverse trajectories using AI model
4. **Ranks** them by quality (smoothness, efficiency, length)
5. **Selects** top 5 best trajectories
6. **Plots** them in 3D (PNG image)
7. **Exports** to CSV files for analysis

## Output

You'll get:

```
✓ Generated 5 high-quality trajectories
✓ Average path length: 2953.7 m
✓ Trajectories saved to CSV files:
  - trajectory_1.csv
  - trajectory_2.csv
  - trajectory_3.csv
  - trajectory_4.csv
  - trajectory_5.csv
✓ Visualization saved to: my_trajectories.png
```

## Usage Examples

### Example 1: Different Start/End Points

```bash
./trajectory_app \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json \
    --start -500 300 150 \
    --end 600 -400 250 \
    --output example1.png \
    --csv
```

### Example 2: More Waypoints

```bash
./trajectory_app \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json \
    --start 0 0 100 \
    --end 1000 800 300 \
    --waypoints 75 \
    --output example2.png
```

### Example 3: CSV Only (No Plot)

```bash
./trajectory_app \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json \
    --start 0 0 50 \
    --end 400 300 150 \
    --waypoints 40 \
    --no-plot \
    --csv
```

## Requirements

- **Linux/Ubuntu** (tested on Ubuntu 20.04+)
- **C++ Compiler**: g++ 7+ (auto-installed by build.sh)
- **CMake**: 3.15+ (auto-installed by build.sh)
- **gnuplot**: For plotting (optional, auto-installed by build.sh)
- **ONNX Runtime**: Auto-downloaded by build.sh

## Troubleshooting

### Problem: Build fails

**Solution**: Install dependencies manually
```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake g++ gnuplot
```

### Problem: Model not found

**Solution**: Train the model first
```bash
cd /workspace
python3 -m src.train --data_path data/trajectories.npz --save_dir models --epochs 20
python3 -m src.export_onnx --checkpoint models/best_model.pth --output models/trajectory_generator.onnx
```

### Problem: Library error

**Solution**: Set library path
```bash
export LD_LIBRARY_PATH=/workspace/libs/onnxruntime-linux-x64-1.16.3/lib:$LD_LIBRARY_PATH
```

## Performance

- **Model loading**: ~200 ms
- **10 trajectories**: ~40 ms
- **Ranking**: ~1 ms
- **Plotting**: ~500 ms
- **Total**: **< 1 second**

## Command-Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--start X Y Z` | Starting coordinates | `--start 0 0 100` |
| `--end X Y Z` | Ending coordinates | `--end 800 600 200` |
| `--waypoints N` | Number of points (2-200) | `--waypoints 50` |
| `--output FILE` | Output image file | `--output result.png` |
| `--csv` | Save to CSV files | `--csv` |
| `--no-plot` | Skip plotting | `--no-plot` |
| `--help` | Show help | `--help` |

## Understanding the Output

### Trajectory Rankings

```
 Rank   Length(m)  Smoothness  Efficiency       Score
-----------------------------------------------------
    1       938.8      0.9954       0.862      0.9564  ← Best!
    2      2421.8      0.9435       0.080      0.5782
    3      3011.2      0.9494       0.083      0.5661
```

- **Rank 1** = Best trajectory (highest score)
- **Smoothness** = Less curvature is better (0-1 scale)
- **Efficiency** = Closer to straight line is better
- **Score** = Combined quality metric

### Quality Metrics Explained

- **Smoothness > 0.95**: Excellent, very smooth path
- **Smoothness 0.90-0.95**: Good, minor curves
- **Smoothness < 0.90**: Fair, noticeable curvature

- **Efficiency > 0.80**: Near-optimal path
- **Efficiency 0.50-0.80**: Moderate detour
- **Efficiency < 0.50**: Significant detour

## Next Steps

1. **Customize**: Modify scoring weights in `trajectory_app.cpp`
2. **Integrate**: Use in your own C++ project (see CPP_APPLICATION_GUIDE.md)
3. **Experiment**: Try different start/end points and waypoint counts
4. **Analyze**: Load CSV files into Excel, Python, or MATLAB

## Documentation

- **Quick Start**: This file (you are here!)
- **Full Guide**: `CPP_APPLICATION_GUIDE.md` - Complete documentation
- **API Reference**: `cpp/README.md` - C++ API details
- **Python Version**: `README.md` - Python implementation

## Support

Questions? Check:
1. `--help` output
2. Error messages in console
3. Documentation files
4. Example scripts

---

**Happy trajectory planning! 🚀**

*This application uses AI (CVAE model) to generate diverse, high-quality flight paths.*

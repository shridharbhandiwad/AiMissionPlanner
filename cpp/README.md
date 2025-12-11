# Trajectory Generator - C++ Application

A high-performance C++ application for generating and visualizing diverse 3D trajectories using a trained CVAE model via ONNX Runtime.

## Features

- 🚀 **Fast Trajectory Generation**: Generate multiple diverse trajectories in milliseconds
- 📊 **Intelligent Ranking**: Automatically ranks trajectories by quality metrics (smoothness, efficiency, path length)
- 📈 **3D Visualization**: Creates beautiful 3D plots using gnuplot
- 💾 **CSV Export**: Save trajectories to CSV files for further analysis
- ⚙️ **Flexible Configuration**: Command-line interface for easy customization
- 🔧 **Production-Ready**: Uses ONNX Runtime for efficient inference

## Requirements

### System Requirements
- C++17 compatible compiler (GCC 7+, Clang 5+, MSVC 2017+)
- CMake 3.15 or higher
- ONNX Runtime 1.16.0+
- gnuplot (optional, for plotting)

### Installation

#### Linux (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake wget gnuplot

# The build script will automatically download ONNX Runtime if not found
# Or manually set ONNX Runtime location:
export ONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime
```

#### macOS

```bash
# Install dependencies
brew install cmake gnuplot

# Download ONNX Runtime manually from:
# https://github.com/microsoft/onnxruntime/releases
export ONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime
```

## Building

### Quick Build

```bash
cd cpp
./build.sh
```

This script will:
1. Automatically download ONNX Runtime if needed
2. Configure the project with CMake
3. Build all executables

### Manual Build

```bash
cd cpp
mkdir build && cd build
cmake -DONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime ..
make -j$(nproc)
```

## Usage

### Basic Usage

```bash
cd cpp/build
./trajectory_app --start 0 0 100 --end 800 600 200
```

### Command-Line Options

```
Usage: trajectory_app [options]

Options:
  --start X Y Z          Starting point coordinates (default: 0 0 100)
  --end X Y Z            Ending point coordinates (default: 800 600 200)
  --waypoints N          Number of waypoints in trajectory (default: 50)
  --model PATH           Path to ONNX model
  --norm PATH            Path to normalization JSON
  --output FILE          Output plot filename (default: trajectories.png)
  --no-plot              Disable plotting (only generate trajectories)
  --csv                  Save trajectories to CSV files
  --help                 Show this help message
```

### Examples

#### Example 1: Simple Trajectory Generation

```bash
./trajectory_app \
    --start 0 0 100 \
    --end 800 600 200 \
    --waypoints 50 \
    --output my_trajectories.png
```

#### Example 2: Generate and Export to CSV

```bash
./trajectory_app \
    --start -500 300 150 \
    --end 600 -400 250 \
    --waypoints 75 \
    --csv \
    --output trajectories.png
```

#### Example 3: Custom Model Location

```bash
./trajectory_app \
    --model /path/to/model.onnx \
    --norm /path/to/normalization.json \
    --start 0 0 100 \
    --end 1000 800 300
```

#### Example 4: Generate Without Plotting

```bash
./trajectory_app \
    --start 0 0 100 \
    --end 800 600 200 \
    --no-plot \
    --csv
```

### Running Examples

A convenience script is provided to run multiple examples:

```bash
cd cpp
./run_example.sh
```

## Output

The application generates:

1. **Console Output**: Detailed statistics for each trajectory including:
   - Path length
   - Smoothness score
   - Efficiency
   - Overall quality score

2. **3D Visualization** (if gnuplot available):
   - PNG image showing top 5 trajectories
   - Start point (green)
   - End point (red)
   - Color-coded trajectory paths

3. **CSV Files** (if `--csv` flag used):
   - `trajectory_1.csv` to `trajectory_5.csv`
   - Format: `Waypoint,X,Y,Z`

## Architecture

### Components

```
trajectory_app
├── trajectory_inference.cpp    # ONNX model inference
├── trajectory_metrics.cpp      # Quality metrics computation
├── trajectory_plotter.cpp      # Visualization using gnuplot
└── trajectory_app.cpp          # Main application logic
```

### How It Works

1. **Model Loading**: Loads pre-trained CVAE model via ONNX Runtime
2. **Generation**: Samples from latent space to generate 10 candidate trajectories
3. **Ranking**: Computes quality metrics and ranks trajectories
4. **Selection**: Selects top 5 trajectories based on combined quality score
5. **Visualization**: Plots trajectories in 3D using gnuplot
6. **Export**: Optionally exports data to CSV format

### Quality Metrics

Trajectories are ranked using a weighted combination of:

- **Smoothness** (50%): Based on curvature analysis
- **Efficiency** (30%): Ratio of straight-line distance to path length
- **Path Length** (20%): Preference for shorter paths

```
Score = 0.5 * smoothness + 0.3 * efficiency + 0.2 * normalized_length
```

## Performance

Typical performance on modern hardware:

- Single trajectory generation: ~10-20 ms
- 10 trajectories generation: ~100-150 ms
- Ranking: ~1-2 ms
- Plotting: ~500-1000 ms

Total time: **< 2 seconds** for complete pipeline

## Troubleshooting

### ONNX Runtime Not Found

```bash
export ONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime
# Or let build.sh download it automatically
./build.sh
```

### Gnuplot Not Available

```bash
# Linux
sudo apt-get install gnuplot

# macOS
brew install gnuplot

# Or disable plotting
./trajectory_app --no-plot --csv
```

### Library Loading Errors

```bash
# Add ONNX Runtime lib to library path
export LD_LIBRARY_PATH=$ONNXRUNTIME_ROOT_DIR/lib:$LD_LIBRARY_PATH
./trajectory_app
```

### Model File Not Found

Make sure the model is trained and exported:

```bash
cd ..
python3 -m src.train --data_path data/trajectories.npz --save_dir models --epochs 20
python3 -m src.export_onnx --checkpoint models/best_model.pth --output models/trajectory_generator.onnx
```

## API Reference

### TrajectoryGenerator

```cpp
// Create generator
GeneratorConfig config("model.onnx");
config.latent_dim = 64;
config.seq_len = 50;
TrajectoryGenerator generator(config);

// Load normalization
generator.loadNormalization("normalization.json");

// Generate trajectories
Waypoint start(0, 0, 100);
Waypoint end(800, 600, 200);
auto trajectories = generator.generateMultiple(start, end, 5);
```

### TrajectoryPlotter

```cpp
// Create plotter
PlotConfig plot_config;
plot_config.output_file = "output.png";
plot_config.title = "Trajectories";
TrajectoryPlotter plotter(plot_config);

// Plot in 3D
plotter.plot3D(trajectories, start, end, labels);

// Save to CSV
plotter.saveToCSV(trajectories, "trajectory");
```

### Quality Metrics

```cpp
// Compute metrics
float length = computePathLength(trajectory);
float smoothness = computeSmoothnessScore(trajectory);
float curvature = computeAverageCurvature(trajectory);

// Print statistics
printTrajectoryStats(trajectory);
```

## Integration

### Using in Your Project

1. Include headers:
```cpp
#include "trajectory_inference.h"
#include "trajectory_plotter.h"
```

2. Link libraries:
```cmake
target_link_libraries(your_app
    trajectory_inference
    trajectory_plotter
    ${ONNXRUNTIME_LIBRARIES}
)
```

3. Use the API:
```cpp
TrajectoryGenerator generator(config);
auto trajectories = generator.generate(start, end);
```

## License

This project is part of the Trajectory Generation research framework.

## Citation

If you use this code in your research, please cite:

```bibtex
@software{trajectory_generator_cpp,
  title={Trajectory Generator C++ Application},
  author={Mission Planner Team},
  year={2024},
  note={CVAE-based trajectory generation with ONNX Runtime}
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Check the [Troubleshooting](#troubleshooting) section
- Open an issue on GitHub
- See the main README for Python implementation details

---

**Happy trajectory generation! 🚀**

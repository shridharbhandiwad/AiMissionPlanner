# C++ Trajectory Generator - Complete Guide

## Overview

This document provides a complete guide to using the C++ trajectory generation application. The application uses a trained CVAE (Conditional Variational Autoencoder) model exported to ONNX format to generate diverse, high-quality 3D trajectories.

## Quick Start

```bash
# 1. Navigate to cpp directory
cd cpp

# 2. Build the application (auto-downloads ONNX Runtime if needed)
./build.sh

# 3. Run with default settings
cd build
export LD_LIBRARY_PATH=../../libs/onnxruntime-linux-x64-1.16.3/lib:$LD_LIBRARY_PATH
./trajectory_app \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json \
    --start 0 0 100 \
    --end 800 600 200 \
    --csv

# 4. View the generated plot
# Output: test_trajectories.png (or specify with --output)
```

## Features

### 1. Trajectory Generation
- Generates 10 candidate trajectories using CVAE model
- Samples from latent space for diversity
- Fast inference (~40ms for 10 trajectories)

### 2. Intelligent Ranking
Ranks trajectories using multi-criteria scoring:
- **Smoothness** (50% weight): Lower curvature = higher score
- **Efficiency** (30% weight): Closer to straight-line path = higher score  
- **Path Length** (20% weight): Shorter paths preferred

Combined score formula:
```
Score = 0.5 × smoothness + 0.3 × efficiency + 0.2 × normalized_length
```

### 3. Visualization
- 3D plots using gnuplot
- Color-coded trajectories
- Start point (green) and end point (red) markers
- Customizable output size and format

### 4. Data Export
- CSV files for each trajectory
- Format: `Waypoint,X,Y,Z`
- Easy import into other tools

## Command-Line Interface

### Basic Usage

```bash
./trajectory_app --start X Y Z --end X Y Z [options]
```

### All Options

| Option | Description | Default |
|--------|-------------|---------|
| `--start X Y Z` | Starting point coordinates | `0 0 100` |
| `--end X Y Z` | Ending point coordinates | `800 600 200` |
| `--waypoints N` | Number of waypoints (2-200) | `50` |
| `--model PATH` | Path to ONNX model | `../models/trajectory_generator.onnx` |
| `--norm PATH` | Path to normalization JSON | `../models/trajectory_generator_normalization.json` |
| `--output FILE` | Output plot filename | `trajectories.png` |
| `--no-plot` | Disable plotting | false |
| `--csv` | Save to CSV files | false |
| `--help` | Show help message | - |

## Examples

### Example 1: Basic Trajectory Generation

Generate trajectories from origin to a distant point:

```bash
./trajectory_app \
    --start 0 0 100 \
    --end 1000 800 300 \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json
```

**Output:**
- Console: Statistics for top 5 trajectories
- File: `trajectories.png` (3D visualization)

### Example 2: Custom Waypoints with CSV Export

Generate longer trajectories and save data:

```bash
./trajectory_app \
    --start -500 300 150 \
    --end 600 -400 250 \
    --waypoints 75 \
    --output long_trajectories.png \
    --csv \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json
```

**Output:**
- `long_trajectories.png`
- `trajectory_1.csv` through `trajectory_5.csv`

### Example 3: Data Export Only (No Plot)

Generate trajectories without visualization:

```bash
./trajectory_app \
    --start 0 0 100 \
    --end 800 600 200 \
    --no-plot \
    --csv \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json
```

**Output:**
- CSV files only
- No PNG generated

### Example 4: Short-Range Mission

Plan a short-range trajectory:

```bash
./trajectory_app \
    --start 0 0 50 \
    --end 200 150 80 \
    --waypoints 30 \
    --output short_mission.png \
    --model ../../models/trajectory_generator.onnx \
    --norm ../../models/trajectory_generator_normalization.json
```

## Output Interpretation

### Console Output

```
Top 5 Trajectories (ranked by quality):

 Rank   Length(m)  Smoothness  Efficiency       Score
-----------------------------------------------------
    1       938.8      0.9954       0.862      0.9564
    2      2421.8      0.9435       0.080      0.5782
```

- **Rank**: Position in quality ranking (1 = best)
- **Length**: Total path length in meters
- **Smoothness**: 0-1 score (higher = smoother, less curvature)
- **Efficiency**: Ratio of straight-line distance to path length
- **Score**: Combined quality score (higher = better)

### Trajectory Statistics

For each trajectory, detailed statistics are printed:

```
Trajectory 1:
  Path length: 938.8 m
  Straight-line distance: 809.6 m
  Efficiency: 0.862
  Avg curvature: 0.0046 rad/m
  Smoothness score: 0.9954
```

### CSV Format

Each CSV file contains:
```csv
Waypoint,X,Y,Z
0,-24.58,9.69,109.37
1,-27.78,-40.36,114.34
...
```

### Visualization

The PNG output shows:
- Top 5 trajectories in different colors
- Green sphere: Start point
- Red sphere: End point
- 3D axes with labels
- Legend with trajectory rankings

## Understanding the Algorithm

### 1. Model Architecture

The system uses a Conditional Variational Autoencoder (CVAE):

```
Input: [start_point, end_point, latent_vector]
       ↓
    LSTM Decoder
       ↓
Output: trajectory_sequence
```

- **Latent vector**: Sampled from N(0,1), controls trajectory variation
- **Conditioning**: Ensures trajectories connect start to end
- **Decoder**: LSTM generates waypoints sequentially

### 2. Generation Process

```python
for i in range(10):  # Generate 10 candidates
    z = sample_from_N(0, 1)  # Random latent vector
    traj = decoder(z, start, end)  # Generate trajectory
    candidates.append(traj)

# Rank by quality
ranked = rank_by_quality(candidates)

# Return top 5
return ranked[:5]
```

### 3. Ranking Criteria

**Smoothness**: Computed from curvature
```cpp
curvature = angle_between_segments / segment_length
smoothness = 1 / (1 + avg_curvature)
```

**Efficiency**: Path directness
```cpp
efficiency = straight_line_distance / path_length
```

**Combined Score**: Weighted sum
```cpp
score = 0.5 * smoothness + 0.3 * efficiency + 0.2 * normalized_length
```

## Performance

### Benchmarks

Tested on standard hardware (4-core CPU):

| Operation | Time |
|-----------|------|
| Model loading | ~200 ms |
| Single trajectory | ~4 ms |
| 10 trajectories | ~40 ms |
| Ranking | ~1 ms |
| Plotting | ~500 ms |
| **Total pipeline** | **~750 ms** |

### Scalability

- Linear scaling with number of trajectories
- ONNX Runtime optimized for CPU inference
- Multi-threaded LSTM operations

## Troubleshooting

### Issue: Model file not found

```
Error: File doesn't exist
```

**Solution**: Use absolute paths or check model location
```bash
--model /absolute/path/to/model.onnx
```

### Issue: Library loading error

```
error while loading shared libraries: libonnxruntime.so
```

**Solution**: Set LD_LIBRARY_PATH
```bash
export LD_LIBRARY_PATH=/path/to/onnxruntime/lib:$LD_LIBRARY_PATH
```

### Issue: Gnuplot not found

```
Warning: gnuplot not available
```

**Solution**: Install gnuplot
```bash
sudo apt-get install gnuplot
```

Or use `--no-plot` flag

### Issue: Poor trajectory quality

**Solution**: Retrain model with more epochs or better data
```bash
cd ..
python3 -m src.train --epochs 50 --batch_size 64
python3 -m src.export_onnx
```

## Integration Guide

### Using in Your C++ Project

```cpp
#include "trajectory_inference.h"
#include "trajectory_plotter.h"

// Initialize
trajectory::GeneratorConfig config("model.onnx");
trajectory::TrajectoryGenerator gen(config);
gen.loadNormalization("norm.json");

// Generate
trajectory::Waypoint start(0, 0, 100);
trajectory::Waypoint end(800, 600, 200);
auto trajs = gen.generateMultiple(start, end, 5);

// Evaluate
for (const auto& traj : trajs) {
    float length = trajectory::computePathLength(traj);
    float smoothness = trajectory::computeSmoothnessScore(traj);
    // Use metrics...
}

// Plot
trajectory::PlotConfig plot_config;
trajectory::TrajectoryPlotter plotter(plot_config);
plotter.plot3D(trajs, start, end);
```

### CMake Integration

```cmake
find_library(TRAJECTORY_LIB trajectory_inference)
target_link_libraries(your_app ${TRAJECTORY_LIB})
```

## Advanced Usage

### Custom Scoring Function

Modify `computeQualityScore()` in `trajectory_app.cpp`:

```cpp
float computeQualityScore(const Trajectory& traj) {
    float smoothness = computeSmoothnessScore(traj);
    float length = computePathLength(traj);
    
    // Custom weighting
    return 0.7 * smoothness + 0.3 * (1000.0 / length);
}
```

### Batch Processing

Process multiple start/end pairs:

```bash
for start in "0 0 100" "100 200 150" "300 400 200"; do
    for end in "800 600 200" "1000 800 300"; do
        ./trajectory_app --start $start --end $end --csv
    done
done
```

### Real-Time Generation

For low-latency applications:
- Use `--no-plot` flag
- Generate fewer candidates (modify source)
- Use GPU-accelerated ONNX Runtime

## Model Information

### Input Specification

- **Latent**: [batch_size, 64] - Sampled from N(0,1)
- **Start**: [batch_size, 3] - Normalized coordinates
- **End**: [batch_size, 3] - Normalized coordinates

### Output Specification

- **Trajectory**: [batch_size, num_waypoints, 3] - Normalized coordinates

### Normalization

Data is normalized using statistics from training:
```json
{
  "mean": [-1.90, -1.59, 274.97],
  "std": [513.73, 514.87, 114.67]
}
```

Denormalization:
```
original = normalized * std + mean
```

## FAQ

**Q: Can I change the number of top trajectories?**  
A: Yes, modify the loop in `trajectory_app.cpp` line ~250

**Q: How do I use GPU acceleration?**  
A: Install CUDA-enabled ONNX Runtime and set `config.use_gpu = true`

**Q: Can I export in other formats?**  
A: Yes, modify `TrajectoryPlotter` to support SVG, PDF, etc.

**Q: What coordinate system is used?**  
A: Right-handed coordinate system (X: east, Y: north, Z: altitude)

**Q: How do I train a custom model?**  
A: See main README.md for Python training instructions

## References

- [ONNX Runtime Documentation](https://onnxruntime.ai/)
- [Gnuplot Manual](http://www.gnuplot.info/documentation.html)
- [CVAE Paper](https://arxiv.org/abs/1312.6114)

## Support

For issues or questions:
1. Check this guide and cpp/README.md
2. Review example scripts
3. Check console error messages
4. Verify model and normalization files exist

---

**Version**: 1.0  
**Last Updated**: December 2024  
**Status**: Production Ready ✓

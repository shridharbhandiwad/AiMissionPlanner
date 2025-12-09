# C++ Trajectory Generation Inference

This directory contains C++ code for running trajectory generation inference using ONNX Runtime.

## Prerequisites

1. **ONNX Runtime**: Download and install ONNX Runtime
   ```bash
   # Download from: https://github.com/microsoft/onnxruntime/releases
   # For example, on Linux:
   wget https://github.com/microsoft/onnxruntime/releases/download/v1.16.0/onnxruntime-linux-x64-1.16.0.tgz
   tar -xzf onnxruntime-linux-x64-1.16.0.tgz
   export ONNXRUNTIME_ROOT_DIR=$(pwd)/onnxruntime-linux-x64-1.16.0
   ```

2. **CMake**: Version 3.15 or higher
   ```bash
   sudo apt-get install cmake  # Ubuntu/Debian
   brew install cmake          # macOS
   ```

3. **C++ Compiler**: GCC 7+, Clang 5+, or MSVC 2017+

## Building

```bash
# Create build directory
mkdir build
cd build

# Configure
cmake .. -DONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime

# Build
cmake --build . --config Release

# The executable will be in build/trajectory_demo
```

## Running

First, make sure you have:
1. Exported ONNX model: `models/trajectory_generator.onnx`
2. Normalization file: `models/trajectory_generator_normalization.json`

Then run:

```bash
./trajectory_demo ../models/trajectory_generator.onnx ../models/trajectory_generator_normalization.json
```

## Usage in Your Code

```cpp
#include "trajectory_inference.h"

using namespace trajectory;

int main() {
    // Create generator configuration
    GeneratorConfig config("models/trajectory_generator.onnx");
    config.latent_dim = 64;
    config.seq_len = 50;
    config.num_threads = 4;
    
    // Create generator
    TrajectoryGenerator generator(config);
    generator.loadNormalization("models/trajectory_generator_normalization.json");
    
    // Define start and end waypoints
    Waypoint start(0.0f, 0.0f, 100.0f);
    Waypoint end(800.0f, 600.0f, 200.0f);
    
    // Generate trajectory
    Trajectory trajectory = generator.generate(start, end);
    
    // Generate multiple diverse trajectories
    std::vector<Trajectory> trajectories = generator.generateMultiple(start, end, 5);
    
    // Compute metrics
    float path_length = computePathLength(trajectory);
    float smoothness = computeSmoothnessScore(trajectory);
    
    return 0;
}
```

## API Reference

### TrajectoryGenerator

Main class for trajectory generation.

**Constructor:**
```cpp
TrajectoryGenerator(const GeneratorConfig& config)
```

**Methods:**
- `bool loadNormalization(const std::string& norm_path)` - Load normalization parameters
- `Trajectory generate(const Waypoint& start, const Waypoint& end)` - Generate single trajectory
- `std::vector<Trajectory> generateMultiple(const Waypoint& start, const Waypoint& end, int n_samples)` - Generate multiple trajectories
- `bool isReady() const` - Check if generator is initialized

### Utility Functions

- `float computePathLength(const Trajectory& trajectory)` - Compute total path length
- `float computeSmoothnessScore(const Trajectory& trajectory)` - Compute smoothness score
- `float computeAverageCurvature(const Trajectory& trajectory)` - Compute average curvature
- `void printTrajectoryStats(const Trajectory& trajectory)` - Print trajectory statistics

## Performance

Typical performance on modern CPU (Intel i7):
- Single trajectory: 20-50 ms
- Batch of 100 trajectories: 2-5 seconds
- Throughput: 20-50 trajectories/second

With GPU (CUDA), performance can be 5-10x faster.

## GPU Support

To enable GPU support (requires CUDA and TensorRT):

1. Build ONNX Runtime with CUDA support
2. Set `USE_CUDA=ON` when configuring CMake:
   ```bash
   cmake .. -DONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime -DUSE_CUDA=ON
   ```
3. Set `config.use_gpu = true` in your code

## Troubleshooting

**ONNX Runtime not found:**
- Make sure `ONNXRUNTIME_ROOT_DIR` is set correctly
- Check that the include and lib directories exist

**Linking errors:**
- Ensure you're using the correct ONNX Runtime version for your platform
- On Linux, you may need to set `LD_LIBRARY_PATH`:
  ```bash
  export LD_LIBRARY_PATH=$ONNXRUNTIME_ROOT_DIR/lib:$LD_LIBRARY_PATH
  ```

**Runtime errors:**
- Verify that the ONNX model file exists and is valid
- Check that the normalization JSON file is correctly formatted
- Ensure input dimensions match the model's expectations

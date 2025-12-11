#!/bin/bash
# Example script to run the trajectory generator

set -e

echo "=========================================="
echo "Running Trajectory Generator Example"
echo "=========================================="
echo ""

# Make sure we're in the cpp directory
cd "$(dirname "$0")"

# Check if built
if [ ! -f "build/trajectory_app" ]; then
    echo "Application not built yet. Building..."
    ./build.sh
fi

# Export LD_LIBRARY_PATH for ONNX Runtime
if [ -n "$ONNXRUNTIME_ROOT_DIR" ]; then
    export LD_LIBRARY_PATH=$ONNXRUNTIME_ROOT_DIR/lib:$LD_LIBRARY_PATH
elif [ -d "../libs/onnxruntime-linux-x64-1.16.3" ]; then
    export LD_LIBRARY_PATH=$(pwd)/../libs/onnxruntime-linux-x64-1.16.3/lib:$LD_LIBRARY_PATH
fi

# Check if gnuplot is installed
if ! command -v gnuplot &> /dev/null; then
    echo "⚠ Warning: gnuplot not found. Installing..."
    sudo apt-get update && sudo apt-get install -y gnuplot
fi

# Run the application
cd build

echo "Example 1: Simple trajectory generation"
echo "Start: (0, 0, 100), End: (800, 600, 200)"
echo ""
./trajectory_app \
    --start 0 0 100 \
    --end 800 600 200 \
    --waypoints 50 \
    --output trajectories_example1.png \
    --csv

echo ""
echo ""
echo "Example 2: Different start/end points"
echo "Start: (-500, 300, 150), End: (600, -400, 250)"
echo ""
./trajectory_app \
    --start -500 300 150 \
    --end 600 -400 250 \
    --waypoints 75 \
    --output trajectories_example2.png

echo ""
echo "=========================================="
echo "Examples complete!"
echo "=========================================="
echo ""
echo "Generated files:"
ls -lh *.png *.csv 2>/dev/null || echo "No output files found"

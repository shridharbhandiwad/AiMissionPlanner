#!/bin/bash
# Build script for Trajectory Generator C++ application

set -e  # Exit on error

echo "=========================================="
echo "Building Trajectory Generator"
echo "=========================================="

# Check for ONNX Runtime
if [ -z "$ONNXRUNTIME_ROOT_DIR" ]; then
    echo "⚠ Warning: ONNXRUNTIME_ROOT_DIR not set"
    echo "Attempting to download ONNX Runtime..."
    
    # Create libs directory
    mkdir -p ../libs
    cd ../libs
    
    # Download ONNX Runtime if not present
    if [ ! -d "onnxruntime-linux-x64-1.16.3" ]; then
        echo "Downloading ONNX Runtime 1.16.3..."
        wget -q https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-linux-x64-1.16.3.tgz
        tar -xzf onnxruntime-linux-x64-1.16.3.tgz
        rm onnxruntime-linux-x64-1.16.3.tgz
        echo "✓ ONNX Runtime downloaded"
    fi
    
    export ONNXRUNTIME_ROOT_DIR=$(pwd)/onnxruntime-linux-x64-1.16.3
    cd ../cpp
else
    echo "✓ Using ONNX Runtime from: $ONNXRUNTIME_ROOT_DIR"
fi

# Create build directory
mkdir -p build
cd build

# Run CMake
echo ""
echo "Running CMake..."
CC=gcc CXX=g++ cmake -DCMAKE_BUILD_TYPE=Release \
      -DONNXRUNTIME_ROOT_DIR=$ONNXRUNTIME_ROOT_DIR \
      ..

# Build
echo ""
echo "Building..."
make -j$(nproc)

echo ""
echo "=========================================="
echo "Build complete!"
echo "=========================================="
echo ""
echo "Executables:"
echo "  - trajectory_app  (Main application)"
echo "  - trajectory_demo (Demo/test application)"
echo ""
echo "To run:"
echo "  cd build"
echo "  ./trajectory_app --help"
echo ""

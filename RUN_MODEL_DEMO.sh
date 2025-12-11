#!/bin/bash

# Run Model Pipeline Demonstration
# This script demonstrates the complete model training, testing, and validation pipeline

echo "================================================================"
echo "  Trajectory Generation Model - Complete Pipeline Demo"
echo "================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found."
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo ""
echo "Checking dependencies..."
pip install torch numpy scipy matplotlib tqdm tensorboard --quiet --disable-pip-version-check 2>/dev/null || {
    echo "Installing dependencies..."
    pip install torch numpy scipy matplotlib tqdm tensorboard
}

echo ""
echo "================================================================"
echo "  Running Model Pipeline Demonstration"
echo "================================================================"
echo ""
echo "This will show you:"
echo "  1. Data preparation and normalization"
echo "  2. Model architecture (CVAE)"
echo "  3. Loss computation details"
echo "  4. Training iteration"
echo "  5. Validation process"
echo "  6. Inference with quality metrics"
echo ""
echo "All components are explained for C++ porting."
echo ""
read -p "Press Enter to continue..."
echo ""

# Run the demonstration
python3 model_pipeline_demo.py

echo ""
echo "================================================================"
echo "  Demonstration Complete!"
echo "================================================================"
echo ""
echo "Next steps:"
echo "  1. Review the output above"
echo "  2. Read CPP_PORTING_GUIDE.md for C++ implementation"
echo "  3. Read MODEL_ARCHITECTURE.md for detailed mathematics"
echo "  4. Check cpp/ directory for ready-to-use C++ code"
echo ""
echo "To train an actual model:"
echo "  python3 src/data_generator.py     # Generate dataset"
echo "  python3 src/train.py              # Train model"
echo "  python3 src/export_onnx.py        # Export to ONNX"
echo ""
echo "To build C++ inference:"
echo "  cd cpp && mkdir build && cd build"
echo "  cmake .. -DONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime"
echo "  cmake --build ."
echo ""

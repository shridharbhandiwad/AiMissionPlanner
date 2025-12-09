#!/bin/bash
# Quick Demo Script - Runs inference on pre-trained model
# Use this if you already have a trained model

set -e

echo "=========================================="
echo "Quick Demo - Trajectory Generation"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}[STEP $1]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Check if model exists
if [ ! -f "models/best_model.pth" ]; then
    echo -e "${RED}Error: Model not found!${NC}"
    echo "Please train the model first:"
    echo "  ./run_pipeline.sh"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
fi

print_step "1" "Running inference demo..."
python src/inference.py \
    --checkpoint models/best_model.pth \
    --n_samples 5
print_success "Inference completed"

print_step "2" "Generating visualizations..."
python -c "
from src.visualize import TrajectoryVisualizer
from src.inference import TrajectoryPredictor
import numpy as np

# Create predictor
predictor = TrajectoryPredictor('models/best_model.pth')

# Generate trajectories
start = np.array([0.0, 0.0, 100.0])
end = np.array([800.0, 600.0, 200.0])
trajectories = predictor.predict_single(start, end, n_samples=5)

# Visualize
viz = TrajectoryVisualizer()
viz.plot_multiple_trajectories(
    trajectories, start, end,
    title='Quick Demo: Generated Trajectories',
    save_path='demo_output.png',
    show=False
)
print('Visualization saved to demo_output.png')
"
print_success "Visualization generated"

print_step "3" "Testing C++ inference (if available)..."
if [ -f "cpp/build/trajectory_demo" ]; then
    if [ -f "models/trajectory_generator.onnx" ]; then
        ./cpp/build/trajectory_demo \
            models/trajectory_generator.onnx \
            models/trajectory_generator_normalization.json
        print_success "C++ demo completed"
    else
        echo "ONNX model not found, skipping C++ demo"
        echo "Run: python src/export_onnx.py --checkpoint models/best_model.pth"
    fi
else
    echo "C++ demo not built, skipping"
    echo "To build: cd cpp && mkdir build && cd build && cmake .. && make"
fi

echo ""
echo "=========================================="
echo "Quick Demo Completed!"
echo "=========================================="
echo ""
echo "Check demo_output.png for visualization"
echo ""

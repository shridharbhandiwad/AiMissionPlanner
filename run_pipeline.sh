#!/bin/bash
# Complete Pipeline Runner Script
# This script runs the entire trajectory generation pipeline

set -e  # Exit on error

echo "=========================================="
echo "Trajectory Generation Pipeline"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}[STEP $1]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_step "0" "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_step "0" "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install dependencies
print_step "1" "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
print_success "Dependencies installed"

# Generate dataset
if [ ! -f "data/trajectories.npz" ]; then
    print_step "2" "Generating dataset (this may take 5-10 minutes)..."
    python src/data_generator.py
    print_success "Dataset generated"
else
    echo "Dataset already exists, skipping generation"
fi

# Train model
if [ ! -f "models/best_model.pth" ]; then
    print_step "3" "Training model..."
    echo "This will take 2-4 hours on GPU or 8-12 hours on CPU"
    echo "You can interrupt with Ctrl+C and resume later"
    
    # Check if CUDA is available
    DEVICE="cpu"
    if python -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
        DEVICE="cuda"
        echo "Using GPU for training"
    else
        echo "Using CPU for training (slower)"
    fi
    
    python src/train.py \
        --epochs 100 \
        --batch_size 64 \
        --lr 0.001 \
        --device $DEVICE
    
    print_success "Model trained"
else
    echo "Model already exists, skipping training"
fi

# Run inference demo
print_step "4" "Running inference demo..."
python src/inference.py \
    --checkpoint models/best_model.pth \
    --n_samples 5
print_success "Inference demo completed"

# Evaluate model
print_step "5" "Evaluating model..."
python src/evaluate.py \
    --checkpoint models/best_model.pth \
    --data data/trajectories.npz \
    --output results/
print_success "Evaluation completed"

# Export to ONNX
if [ ! -f "models/trajectory_generator.onnx" ]; then
    print_step "6" "Exporting to ONNX..."
    python src/export_onnx.py \
        --checkpoint models/best_model.pth \
        --output models/trajectory_generator.onnx \
        --test
    print_success "ONNX export completed"
else
    echo "ONNX model already exists, skipping export"
fi

# Run visualization demo
print_step "7" "Generating visualizations..."
python src/visualize.py
print_success "Visualizations generated"

echo ""
echo "=========================================="
echo "Pipeline Completed Successfully!"
echo "=========================================="
echo ""
echo "Generated files:"
echo "  - data/trajectories.npz (dataset)"
echo "  - models/best_model.pth (trained model)"
echo "  - models/trajectory_generator.onnx (ONNX model)"
echo "  - results/ (evaluation results)"
echo "  - visualizations/ (plots)"
echo ""
echo "Next steps:"
echo "  1. Start API: python api/app.py"
echo "  2. Build C++: cd cpp && mkdir build && cd build && cmake .. && make"
echo "  3. View results: open visualizations/interactive_plot.html"
echo ""

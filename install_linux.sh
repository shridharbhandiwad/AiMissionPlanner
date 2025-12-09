#!/bin/bash
# Linux/Mac Installation Script for AI-Enabled Mission Trajectory Planner

set -e  # Exit on error

echo "================================================"
echo "AI-Enabled Mission Trajectory Planner"
echo "Linux/Mac Installation Script"
echo "================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

echo "Step 1: Checking Python version..."
python3 --version
echo ""

echo "Step 2: Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "Virtual environment created successfully!"
fi
echo ""

echo "Step 3: Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated!"
echo ""

echo "Step 4: Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel
echo ""

echo "Step 5: Installing dependencies..."
echo "This may take 5-10 minutes depending on your internet connection."
echo ""

# Try standard installation first
echo "Installing packages with binary preference..."
if pip install --prefer-binary -r requirements.txt; then
    echo "✓ Packages installed successfully!"
else
    echo ""
    echo "WARNING: Standard installation failed. Trying with compatible versions..."
    
    # Install ONNX packages with specific versions
    pip install --prefer-binary onnx==1.16.1 onnxruntime==1.19.2
    
    # Install PyTorch
    pip install torch==2.9.1 torchvision==0.24.1
    
    # Install remaining packages
    pip install numpy==1.26.4 scipy==1.14.1 pandas==2.2.3 scikit-learn==1.5.2 \
                matplotlib==3.9.0 seaborn==0.13.0 plotly==5.24.0 tensorboard==2.18.0 \
                tqdm==4.66.1 fastapi==0.115.0 uvicorn[standard]==0.30.0 pydantic==2.9.0 \
                python-multipart==0.0.12 shapely==2.0.6 pytest==8.3.0
    
    echo "✓ Packages installed with compatible versions!"
fi
echo ""

echo "================================================"
echo "Installation completed successfully!"
echo "================================================"
echo ""

echo "Verifying installation..."
python -c "
import torch
import onnx
import onnxruntime
print('PyTorch:', torch.__version__)
print('ONNX:', onnx.__version__)
print('ONNX Runtime:', onnxruntime.__version__)
print()
print('✓ All packages installed successfully!')
"

echo ""
echo "You can now use the system!"
echo ""
echo "Quick start:"
echo "  1. Generate dataset:     python src/data_generator.py"
echo "  2. Train model:          python src/train.py"
echo "  3. Generate trajectory:  python src/inference.py"
echo ""
echo "For more information, see README.md"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""

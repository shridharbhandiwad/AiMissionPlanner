#!/bin/bash
# Fix for NumPy/SciPy version conflict on Linux/Mac
# This script resolves the incompatibility between numpy 2.3.5 and scipy 1.14.1

set -e  # Exit on error

echo "================================================"
echo "NumPy/SciPy Compatibility Fix"
echo "================================================"
echo ""
echo "Issue: scipy 1.14.1 requires numpy<2.3, but numpy 2.3.5 was installed"
echo "Solution: Reinstall numpy with version constraint compatible with scipy"
echo ""

# Check if we're in a virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "WARNING: No virtual environment detected!"
    echo ""
    echo "It's recommended to activate your virtual environment first:"
    echo "  source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/N): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
    echo ""
fi

echo "Step 1: Upgrading pip..."
python -m pip install --upgrade pip
echo ""

echo "Step 2: Uninstalling existing NumPy..."
pip uninstall -y numpy
echo ""

echo "Step 3: Clearing pip cache for NumPy..."
pip cache remove numpy 2>/dev/null || true
echo ""

echo "Step 4: Reinstalling numpy..."
echo "Installing numpy version compatible with scipy 1.14.1"
echo "Version constraint: numpy>=2.0.0,<2.3"
pip install --prefer-binary "numpy>=2.0.0,<2.3"
echo "  ✓ NumPy installed successfully"
echo ""

echo "Step 5: Verifying installations..."
python -c "import numpy; import scipy; print('NumPy version:', numpy.__version__); print('SciPy version:', scipy.__version__); print(''); print('✓ Both packages working correctly!')"
echo ""

echo "================================================"
echo "Fix Applied Successfully!"
echo "================================================"
echo ""
echo "NumPy and SciPy are now compatible."
echo ""
echo "You can now run the trajectory GUI:"
echo "  python run_trajectory_gui.py"
echo ""

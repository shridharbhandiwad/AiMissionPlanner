#!/bin/bash
# Quick fix script for GUI dependencies on Linux/Mac
# Run this if you're getting "No module named 'PyQt5'" or similar errors

echo "================================================"
echo "GUI Dependencies Fix Script (Linux/Mac)"
echo "================================================"
echo ""
echo "This script will install/fix the GUI packages:"
echo "  - PyQt5"
echo "  - PyQtGraph"
echo "  - PyOpenGL"
echo ""

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "WARNING: No virtual environment detected!"
    echo ""
    echo "It's recommended to activate your virtual environment first:"
    echo "  source venv/bin/activate"
    echo ""
    read -p "Continue anyway? (y/N): " CONTINUE
    if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
        echo "Cancelled."
        exit 0
    fi
    echo ""
fi

echo "Step 1: Upgrading pip..."
python -m pip install --upgrade pip
echo ""

echo "Step 2: Uninstalling old GUI packages (if any)..."
pip uninstall -y PyQt5 PyQt5-Qt5 PyQt5-sip PyQtGraph PyOpenGL PyOpenGL-accelerate 2>/dev/null || true
echo ""

echo "Step 3: Installing PyQt5..."
pip install PyQt5==5.15.11
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install PyQt5"
    echo ""
    echo "Try installing manually:"
    echo "  pip install PyQt5"
    exit 1
fi
echo "  ✓ PyQt5 installed successfully"
echo ""

echo "Step 4: Installing PyQtGraph..."
pip install PyQtGraph==0.13.7
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install PyQtGraph"
    exit 1
fi
echo "  ✓ PyQtGraph installed successfully"
echo ""

echo "Step 5: Installing PyOpenGL..."
pip install PyOpenGL==3.1.7
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install PyOpenGL"
    exit 1
fi
echo "  ✓ PyOpenGL installed successfully"
echo ""

echo "Step 6: Installing PyOpenGL accelerate (optional)..."
pip install PyOpenGL_accelerate==3.1.7
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to install PyOpenGL_accelerate"
    echo "This is optional - the GUI will still work without it."
else
    echo "  ✓ PyOpenGL_accelerate installed successfully"
fi
echo ""

echo "Step 7: Verifying installation..."
python -c "from PyQt5 import QtWidgets, QtCore, QtGui; import pyqtgraph; import pyqtgraph.opengl; print('All GUI packages imported successfully!')"
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Verification failed!"
    echo "The packages installed but cannot be imported."
    echo ""
    echo "This might indicate:"
    echo "  - Missing system libraries (try: sudo apt-get install python3-pyqt5)"
    echo "  - Display/X11 issues"
    echo "  - OpenGL driver problems"
    exit 1
fi
echo ""

echo "================================================"
echo "GUI Dependencies Fixed Successfully!"
echo "================================================"
echo ""
echo "You can now run the trajectory GUI:"
echo "  python run_trajectory_gui.py"
echo ""

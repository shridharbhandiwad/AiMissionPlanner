#!/bin/bash
# ============================================================
# Fix Missing Dependencies for 3D Trajectory Generator GUI
# ============================================================

echo ""
echo "============================================================"
echo "Installing Missing Dependencies"
echo "============================================================"
echo ""
echo "This will install the required packages for the GUI:"
echo "  - NumPy"
echo "  - SciPy"
echo "  - PyQt5"
echo "  - PyQtGraph"
echo "  - PyOpenGL"
echo ""
echo "============================================================"
echo ""

# Install all required packages
python3 -m pip install --upgrade pip
python3 -m pip install numpy==1.26.4 scipy==1.14.1 PyQt5==5.15.11 PyQtGraph==0.13.7 PyOpenGL==3.1.7 PyOpenGL_accelerate

echo ""
echo "============================================================"
echo "Testing Dependencies"
echo "============================================================"
echo ""

python3 diagnose_gui_startup.py

echo ""
echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "If all tests passed, you can now run:"
echo "  python3 run_trajectory_gui_safe.py"
echo ""
echo "============================================================"
echo ""

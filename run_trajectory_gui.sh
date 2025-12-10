#!/bin/bash
# Linux/Mac shell script to run the 3D Trajectory Generator GUI

echo "============================================================"
echo "3D Trajectory Generator GUI"
echo "============================================================"
echo ""
echo "Starting application..."
echo ""

python3 run_trajectory_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to start GUI"
    echo ""
    echo "Make sure you have installed the required dependencies:"
    echo "  pip install PyQt5 PyQtGraph PyOpenGL"
    echo ""
fi

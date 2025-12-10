#!/bin/bash
# Linux/Mac shell script to run the 3D Trajectory Generator GUI

echo "============================================================"
echo "3D Trajectory Generator GUI"
echo "============================================================"
echo ""

# Check if running in headless environment
if [ -z "$DISPLAY" ]; then
    echo "No display detected - setting up virtual display..."
    
    # Check if Xvfb is available
    if command -v Xvfb >/dev/null 2>&1; then
        # Start Xvfb on display :99
        Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
        XVFB_PID=$!
        
        # Wait for Xvfb to start
        sleep 2
        
        # Export display
        export DISPLAY=:99
        echo "Virtual display configured on :99"
        echo ""
    else
        echo "WARNING: No display available and Xvfb not installed"
        echo "Install with: sudo apt-get install xvfb"
        echo ""
    fi
fi

echo "Starting application..."
echo ""

python3 src/trajectory_gui.py

EXIT_CODE=$?

# Kill Xvfb if we started it
if [ ! -z "$XVFB_PID" ]; then
    kill $XVFB_PID 2>/dev/null
fi

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to start GUI"
    echo ""
    echo "Make sure you have installed the required dependencies:"
    echo "  pip install numpy scipy PyQt5 pyqtgraph PyOpenGL PyOpenGL_accelerate"
    echo ""
fi

exit $EXIT_CODE

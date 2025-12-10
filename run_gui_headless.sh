#!/bin/bash
# Wrapper script to run GUI in headless environment

# Start Xvfb on display :99
Xvfb :99 -screen 0 1920x1080x24 &
XVFB_PID=$!

# Wait for Xvfb to start
sleep 2

# Export display
export DISPLAY=:99

# Run the GUI
python3 /workspace/src/trajectory_gui.py "$@"

# Capture exit code
EXIT_CODE=$?

# Kill Xvfb
kill $XVFB_PID 2>/dev/null

exit $EXIT_CODE

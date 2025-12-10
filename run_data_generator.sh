#!/bin/bash
# Run data_generator.py with warnings suppressed
# This script suppresses NumPy warnings if they occur

echo "Running Data Generator..."
echo

# Set Python warning suppression
export PYTHONWARNINGS=ignore::RuntimeWarning

# Run the data generator with warning suppression
python -W ignore src/data_generator.py

echo
echo "Data generation complete!"

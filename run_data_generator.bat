@echo off
REM Run data_generator.py with NumPy warnings suppressed
REM This script suppresses MINGW-W64 warnings on Windows

echo Running Data Generator...
echo.

REM Set Python warning suppression
set PYTHONWARNINGS=ignore::RuntimeWarning

REM Run the data generator
python -W ignore src/data_generator.py

echo.
echo Data generation complete!
pause

#!/usr/bin/env python3
"""
Script to fix common NumPy installation issues
"""

import sys
import subprocess
import os

print("="*60)
print("NumPy Installation Repair Tool")
print("="*60)
print()

def run_command(cmd, description):
    """Run a command and show output"""
    print(f"{description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print(f"  ✓ Success")
            if result.stdout.strip():
                print(f"  Output: {result.stdout.strip()[:200]}")
            return True
        else:
            print(f"  ✗ Failed (exit code {result.returncode})")
            if result.stderr.strip():
                print(f"  Error: {result.stderr.strip()[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

print("This script will attempt to fix NumPy installation issues.")
print()

# Check current installation
print("Step 1: Checking current NumPy installation...")
try:
    import numpy
    print(f"  Current version: {numpy.__version__}")
    print(f"  Location: {numpy.__file__}")
except ImportError:
    print("  NumPy is not currently installed")
except Exception as e:
    print(f"  NumPy import error: {e}")

print()

# Get user confirmation
response = input("Do you want to proceed with NumPy reinstallation? (yes/no): ").strip().lower()
if response not in ['yes', 'y']:
    print("Aborted by user.")
    sys.exit(0)

print()
print("="*60)
print("Starting repair process...")
print("="*60)
print()

# Step 1: Uninstall NumPy
print("Step 2: Uninstalling current NumPy...")
run_command(f'"{sys.executable}" -m pip uninstall -y numpy', "Uninstalling NumPy")

print()

# Step 2: Clear pip cache
print("Step 3: Clearing pip cache...")
run_command(f'"{sys.executable}" -m pip cache purge', "Clearing cache")

print()

# Step 3: Reinstall NumPy
print("Step 4: Installing NumPy...")
success = run_command(
    f'"{sys.executable}" -m pip install --no-cache-dir numpy',
    "Installing NumPy"
)

if not success:
    print()
    print("Installation failed. Trying alternative method...")
    
    # Try with explicit version
    success = run_command(
        f'"{sys.executable}" -m pip install --no-cache-dir "numpy<2.0"',
        "Installing NumPy (version < 2.0)"
    )

print()
print("="*60)
print("Testing installation...")
print("="*60)
print()

# Test the installation
print("Testing NumPy import...")
result = subprocess.run(
    [sys.executable, '-c', 'import numpy; print("NumPy version:", numpy.__version__)'],
    capture_output=True,
    text=True,
    timeout=10
)

if result.returncode == 0:
    print("  ✓ NumPy imported successfully!")
    print(f"  {result.stdout.strip()}")
    print()
    print("="*60)
    print("SUCCESS!")
    print("="*60)
    print()
    print("NumPy has been successfully installed and tested.")
    print("You can now try running the GUI again:")
    print("  python run_trajectory_gui.py")
else:
    print("  ✗ NumPy import still failing")
    if result.stderr:
        print(f"  Error: {result.stderr.strip()}")
    print()
    print("="*60)
    print("FAILED")
    print("="*60)
    print()
    print("NumPy installation could not be repaired automatically.")
    print()
    print("Additional troubleshooting steps:")
    print()
    if sys.platform == 'win32':
        print("  1. Install Microsoft Visual C++ Redistributables:")
        print("     https://aka.ms/vs/17/release/vc_redist.x64.exe")
        print()
        print("  2. Try installing from conda instead:")
        print("     conda install numpy")
        print()
        print("  3. Check your Python installation:")
        print("     python --version")
        print("     (Should be 3.8 or higher)")
    else:
        print("  1. Install system dependencies:")
        print("     Ubuntu/Debian: sudo apt-get install python3-dev build-essential")
        print("     CentOS/RHEL: sudo yum install python3-devel gcc")
        print()
        print("  2. Try with conda:")
        print("     conda install numpy")
    print()
    print("  For more diagnosis, run:")
    print("    python diagnose_numpy.py")

print()

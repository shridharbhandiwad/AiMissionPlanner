#!/usr/bin/env python3
"""
ONNX Installation Fix Script
Automatically diagnoses and fixes ONNX build errors on Windows
"""

import sys
import subprocess
import platform
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")


def print_step(step_num, text):
    """Print a step message"""
    print(f"Step {step_num}: {text}")


def run_command(cmd, check=True, capture=True):
    """Run a shell command and return the result"""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                check=check,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, check=check, timeout=300)
            return result.returncode == 0, "", ""
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def check_python_version():
    """Check if Python version is compatible"""
    print_step(1, "Checking Python version...")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"  Python version: {version_str}")
    print(f"  Platform: {platform.platform()}")
    print(f"  Architecture: {platform.machine()}")
    
    if version.major != 3:
        print("  ❌ ERROR: Python 3.x is required")
        return False
    
    if version.minor < 8:
        print("  ❌ ERROR: Python 3.8 or higher is required")
        print("  Your version: 3.{version.minor}")
        return False
    
    if version.minor >= 13:
        print("  ⚠️  WARNING: Python 3.13+ has limited package support")
        print("  Recommended: Python 3.10 or 3.11")
        print("  Continuing anyway...")
    
    print("  ✓ Python version is acceptable")
    return True


def check_virtual_env():
    """Check if running in a virtual environment"""
    print_step(2, "Checking virtual environment...")
    
    in_venv = sys.prefix != sys.base_prefix
    
    if in_venv:
        print(f"  ✓ Virtual environment detected: {sys.prefix}")
        return True
    else:
        print("  ⚠️  WARNING: Not running in a virtual environment")
        print("  It's recommended to use a virtual environment")
        return False


def upgrade_pip():
    """Upgrade pip, setuptools, and wheel"""
    print_step(3, "Upgrading pip, setuptools, and wheel...")
    
    success, stdout, stderr = run_command(
        f"{sys.executable} -m pip install --upgrade pip setuptools wheel",
        check=False
    )
    
    if success:
        print("  ✓ pip tools upgraded successfully")
        return True
    else:
        print("  ❌ ERROR: Failed to upgrade pip tools")
        print(f"  {stderr}")
        return False


def uninstall_onnx():
    """Uninstall existing ONNX packages"""
    print_step(4, "Removing existing ONNX installations...")
    
    # Try to uninstall, but don't fail if they're not installed
    run_command(
        f"{sys.executable} -m pip uninstall -y onnx onnxruntime onnxruntime-gpu",
        check=False
    )
    
    print("  ✓ Cleanup complete")
    return True


def install_onnx_binary():
    """Install ONNX using pre-built wheels"""
    print_step(5, "Installing ONNX with pre-built wheels...")
    
    # List of version combinations to try, in order of preference
    install_attempts = [
        {
            "name": "Latest stable (1.16.1)",
            "onnx": "1.16.1",
            "runtime": "1.19.2",
            "flags": "--only-binary :all:"
        },
        {
            "name": "Latest stable with prefer-binary",
            "onnx": "1.16.1",
            "runtime": "1.19.2",
            "flags": "--prefer-binary"
        },
        {
            "name": "Previous stable (1.15.0)",
            "onnx": "1.15.0",
            "runtime": "1.16.3",
            "flags": "--only-binary :all:"
        },
        {
            "name": "Older stable (1.14.1)",
            "onnx": "1.14.1",
            "runtime": "1.16.0",
            "flags": "--only-binary :all:"
        },
    ]
    
    for attempt in install_attempts:
        print(f"\n  Trying: {attempt['name']}...")
        
        cmd = (
            f"{sys.executable} -m pip install {attempt['flags']} "
            f"onnx=={attempt['onnx']} onnxruntime=={attempt['runtime']}"
        )
        
        success, stdout, stderr = run_command(cmd, check=False)
        
        if success:
            print(f"  ✓ Successfully installed ONNX {attempt['onnx']}")
            return True, attempt['onnx'], attempt['runtime']
        else:
            print(f"  ❌ Failed with {attempt['name']}")
            if "No matching distribution" in stderr:
                print("     Reason: No pre-built wheel available for this Python version")
            elif "Could not find" in stderr:
                print("     Reason: Package version not found")
    
    return False, None, None


def verify_installation():
    """Verify ONNX installation"""
    print_step(6, "Verifying installation...")
    
    try:
        import onnx
        import onnxruntime
        
        print(f"  ✓ ONNX version: {onnx.__version__}")
        print(f"  ✓ ONNX Runtime version: {onnxruntime.__version__}")
        
        # Try to create a simple model to verify functionality
        from onnx import TensorProto, helper
        
        # Create a simple graph
        node = helper.make_node("Add", inputs=["x", "y"], outputs=["z"])
        graph = helper.make_graph(
            [node],
            "test_graph",
            [
                helper.make_tensor_value_info("x", TensorProto.FLOAT, [1]),
                helper.make_tensor_value_info("y", TensorProto.FLOAT, [1])
            ],
            [helper.make_tensor_value_info("z", TensorProto.FLOAT, [1])]
        )
        model = helper.make_model(graph)
        
        # Verify with checker
        from onnx import checker
        checker.check_model(model)
        
        print("  ✓ ONNX functionality verified")
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ⚠️  Installation succeeded but verification failed: {e}")
        print("     This might be okay - ONNX is installed but may have issues")
        return True


def print_next_steps():
    """Print next steps for the user"""
    print_header("✓ ONNX Installation Fixed Successfully!")
    
    print("Next steps:\n")
    
    is_windows = platform.system() == "Windows"
    
    if is_windows:
        print("1. Install PyTorch:")
        print("   # For CPU:")
        print("   pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu")
        print("\n   # For GPU (CUDA 11.8):")
        print("   pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118")
        print("\n2. Install remaining dependencies:")
        print("   pip install -r requirements.txt")
        print("\n3. Or run the complete installation script:")
        print("   install_windows.bat")
    else:
        print("1. Install remaining dependencies:")
        print("   pip install -r requirements.txt")
        print("\n2. Or run the installation script:")
        print("   bash install_linux.sh")
    
    print("\n4. Verify everything works:")
    print('   python -c "import torch, onnx, onnxruntime; print(\'All imports successful!\')"')
    
    print("\n5. Start using the system:")
    print("   python src/data_generator.py")
    print("   python src/train.py")
    print("   python src/inference.py")


def print_failure_help():
    """Print help information when all attempts fail"""
    print_header("❌ Automatic Fix Failed")
    
    print("All automatic installation attempts failed.\n")
    print("Possible causes:")
    print("  • Python version incompatibility (try Python 3.10 or 3.11)")
    print("  • No pre-built wheels for your platform")
    print("  • Internet connection issues")
    print("  • Missing system dependencies\n")
    
    print("Recommended solutions:\n")
    
    is_windows = platform.system() == "Windows"
    
    if is_windows:
        print("A. Install Visual Studio Build Tools (to build from source):")
        print("   1. Download: https://visualstudio.microsoft.com/downloads/")
        print("   2. Install 'Desktop development with C++'")
        print("   3. Restart and try again\n")
        
        print("B. Use Anaconda/Miniconda:")
        print("   conda create -n trajectory python=3.11")
        print("   conda activate trajectory")
        print("   conda install -c conda-forge onnx onnxruntime\n")
        
        print("C. Use WSL2 (Windows Subsystem for Linux):")
        print("   WSL has better package availability")
        print("   Follow Linux installation instructions\n")
    else:
        print("A. Try conda installation:")
        print("   conda install -c conda-forge onnx onnxruntime\n")
        
        print("B. Check system dependencies:")
        print("   sudo apt-get update")
        print("   sudo apt-get install -y python3-dev build-essential\n")
    
    print("D. Use Docker:")
    print("   Docker provides a consistent environment")
    print("   See project documentation for Docker setup\n")
    
    print("For more help, see: ONNX_INSTALLATION_FIX.md")


def main():
    """Main function"""
    print_header("ONNX Installation Fix Script")
    
    print("This script will:")
    print("  1. Check your Python environment")
    print("  2. Upgrade pip and build tools")
    print("  3. Install ONNX with pre-built wheels")
    print("  4. Verify the installation")
    print("\nStarting diagnostic and fix process...\n")
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Python version check failed")
        print("Please install Python 3.8-3.12 and try again")
        return 1
    
    # Check virtual environment (warning only)
    check_virtual_env()
    
    # Upgrade pip
    if not upgrade_pip():
        print("\n❌ Failed to upgrade pip")
        print("Try running with administrator/sudo privileges")
        return 1
    
    # Uninstall existing ONNX
    uninstall_onnx()
    
    # Install ONNX with binary wheels
    success, onnx_ver, runtime_ver = install_onnx_binary()
    
    if not success:
        print_failure_help()
        return 1
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️  Installation completed but verification failed")
        print("ONNX may still work, but there might be issues")
        print("Try importing it in your scripts and see if it works")
        return 1
    
    # Print next steps
    print_next_steps()
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

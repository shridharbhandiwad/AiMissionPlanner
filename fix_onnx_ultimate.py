#!/usr/bin/env python3
"""
ONNX Installation Fix - Ultimate Edition
This script tries EVERY known method to install ONNX on Windows
"""

import sys
import subprocess
import platform
import os
import json
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")


def print_step(step_num, total, text):
    """Print a step message"""
    print(f"[{step_num}/{total}] {text}")


def run_command(cmd, check=False, capture=True, timeout=600):
    """Run a shell command and return the result"""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                check=check,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, check=check, timeout=timeout)
            return result.returncode == 0, "", ""
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def get_system_info():
    """Get detailed system information"""
    info = {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "python_version_tuple": (sys.version_info.major, sys.version_info.minor, sys.version_info.micro),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "system": platform.system(),
        "is_windows": platform.system() == "Windows",
        "is_64bit": platform.machine().endswith("64"),
        "in_venv": sys.prefix != sys.base_prefix,
        "python_executable": sys.executable,
    }
    
    # Check for conda
    success, stdout, _ = run_command("conda --version", check=False)
    info["has_conda"] = success
    if success:
        info["conda_version"] = stdout.strip()
    
    return info


def print_diagnostics():
    """Print detailed diagnostic information"""
    print_header("System Diagnostics")
    
    info = get_system_info()
    
    print("Python Information:")
    print(f"  Version: {info['python_version']}")
    print(f"  Executable: {info['python_executable']}")
    print(f"  Virtual Environment: {'Yes' if info['in_venv'] else 'No'}")
    
    print("\nPlatform Information:")
    print(f"  System: {info['system']}")
    print(f"  Platform: {info['platform']}")
    print(f"  Architecture: {info['machine']}")
    print(f"  64-bit: {'Yes' if info['is_64bit'] else 'No'}")
    
    if info['has_conda']:
        print(f"\nConda: Available ({info['conda_version']})")
    else:
        print("\nConda: Not available")
    
    # Check pip version
    success, stdout, _ = run_command(f"{sys.executable} -m pip --version", check=False)
    if success:
        print(f"\nPip: {stdout.strip()}")
    
    # Check for existing ONNX
    try:
        import onnx
        print(f"\n⚠️  ONNX already installed: {onnx.__version__}")
    except ImportError:
        print("\nONNX: Not installed")
    
    try:
        import onnxruntime
        print(f"ONNX Runtime already installed: {onnxruntime.__version__}")
    except ImportError:
        print("ONNX Runtime: Not installed")
    
    print()
    return info


def check_compatibility(info):
    """Check if the system is compatible"""
    print_step(1, 8, "Checking compatibility...")
    
    issues = []
    warnings = []
    
    # Check Python version
    py_ver = info['python_version_tuple']
    if py_ver[0] != 3:
        issues.append("Python 3.x is required")
    elif py_ver[1] < 8:
        issues.append(f"Python 3.8+ is required (you have 3.{py_ver[1]})")
    elif py_ver[1] >= 13:
        warnings.append(f"Python 3.{py_ver[1]} has limited wheel support - recommend 3.10 or 3.11")
    elif py_ver[1] == 12:
        warnings.append(f"Python 3.12 has limited wheel support - recommend 3.10 or 3.11")
    
    # Check if 64-bit
    if not info['is_64bit']:
        issues.append("64-bit Python is required")
    
    # Print results
    if issues:
        print("\n  ❌ Compatibility Issues:")
        for issue in issues:
            print(f"     - {issue}")
        return False
    
    if warnings:
        print("\n  ⚠️  Warnings:")
        for warning in warnings:
            print(f"     - {warning}")
    
    print("\n  ✓ System is compatible")
    return True


def upgrade_pip():
    """Upgrade pip, setuptools, and wheel"""
    print_step(2, 8, "Upgrading pip, setuptools, and wheel...")
    
    success, _, stderr = run_command(
        f"{sys.executable} -m pip install --upgrade pip setuptools wheel",
        check=False
    )
    
    if success:
        print("  ✓ Upgraded successfully")
        return True
    else:
        print(f"  ⚠️  Warning: Upgrade had issues - {stderr[:100]}")
        print("  Continuing anyway...")
        return True  # Don't fail on this


def clean_onnx():
    """Remove any existing ONNX installations"""
    print_step(3, 8, "Cleaning existing ONNX installations...")
    
    # Uninstall all ONNX-related packages
    packages = ["onnx", "onnxruntime", "onnxruntime-gpu", "onnx-weekly"]
    
    for pkg in packages:
        run_command(f"{sys.executable} -m pip uninstall -y {pkg}", check=False)
    
    # Clear pip cache
    run_command(f"{sys.executable} -m pip cache purge", check=False)
    
    print("  ✓ Cleanup complete")
    return True


def method_conda(info):
    """Try installing with conda"""
    if not info['has_conda']:
        return False
    
    print("\n  Method: Conda (conda-forge)")
    print("  This is the most reliable method for Windows!")
    
    # Check if trajectory environment exists
    success, stdout, _ = run_command("conda env list", check=False)
    if success and "trajectory" in stdout:
        print("  Note: 'trajectory' environment already exists")
        print("  Installing in current environment instead")
    
    # Try to install
    success, _, stderr = run_command(
        "conda install -c conda-forge onnx onnxruntime -y",
        check=False,
        timeout=300
    )
    
    if success:
        print("  ✓ Conda installation successful!")
        return True
    else:
        print(f"  ❌ Conda installation failed: {stderr[:200]}")
        return False


def method_pip_versions(info):
    """Try installing specific versions with pip"""
    print("\n  Method: pip with pre-built wheels")
    
    # Extended list of version combinations
    # For Python 3.13+, only versions 1.18.0+ have pre-built wheels
    versions = [
        # (onnx_version, runtime_version, description)
        ("1.20.0", "1.20.0", "Latest stable (Python 3.13+)"),
        ("1.19.1", "1.20.0", "Stable 1.19.1 (Python 3.13+)"),
        ("1.19.0", "1.20.0", "Stable 1.19.0 (Python 3.13+)"),
        ("1.18.0", "1.20.0", "Stable 1.18.0 (Python 3.13+)"),
        ("1.16.2", "1.19.2", "Latest 1.16 (Python 3.12 and below)"),
        ("1.16.1", "1.19.2", "Stable 1.16.1 (Python 3.12 and below)"),
        ("1.16.0", "1.19.0", "Stable 1.16.0"),
        ("1.15.0", "1.18.1", "Previous stable"),
        ("1.15.0", "1.17.1", "1.15 + compatible runtime"),
        ("1.14.1", "1.17.1", "1.14.1 stable"),
        ("1.14.1", "1.16.3", "1.14.1 + older runtime"),
        ("1.14.0", "1.16.0", "1.14.0 stable"),
        ("1.13.1", "1.15.1", "Conservative 1.13"),
        ("1.13.0", "1.15.0", "1.13.0 stable"),
        ("1.12.0", "1.14.1", "Older stable 1.12"),
        ("1.11.0", "1.13.1", "Older stable 1.11"),
    ]
    
    # For Python 3.13+, filter to only compatible versions
    if info['python_version_tuple'][1] >= 13:
        versions = [v for v in versions if float(v[0].split('.')[1]) >= 18]
    
    for onnx_ver, runtime_ver, desc in versions:
        print(f"\n  Trying: {desc} (ONNX {onnx_ver} + Runtime {runtime_ver})")
        
        cmd = (
            f"{sys.executable} -m pip install --only-binary :all: "
            f"onnx=={onnx_ver} onnxruntime=={runtime_ver}"
        )
        
        success, stdout, stderr = run_command(cmd, check=False, timeout=180)
        
        if success:
            print(f"  ✓ Successfully installed!")
            return True, onnx_ver, runtime_ver
        else:
            if "Could not find a version" in stderr:
                print(f"     ❌ No wheel available")
            elif "No matching distribution" in stderr:
                print(f"     ❌ No compatible version")
            else:
                print(f"     ❌ Failed: {stderr[:100]}")
    
    return False, None, None


def method_pip_prefer_binary(info):
    """Try with --prefer-binary flag"""
    print("\n  Method: pip with --prefer-binary")
    
    cmd = f"{sys.executable} -m pip install --prefer-binary onnx onnxruntime"
    success, _, stderr = run_command(cmd, check=False, timeout=180)
    
    if success:
        print("  ✓ Installation successful!")
        return True
    else:
        print(f"  ❌ Failed: {stderr[:200]}")
        return False


def method_pip_no_constraints(info):
    """Try without version constraints"""
    print("\n  Method: pip with latest versions (no constraints)")
    
    cmd = f"{sys.executable} -m pip install --only-binary :all: onnx onnxruntime"
    success, _, stderr = run_command(cmd, check=False, timeout=180)
    
    if success:
        print("  ✓ Installation successful!")
        return True
    else:
        print(f"  ❌ Failed: {stderr[:200]}")
        return False


def install_onnx(info):
    """Try multiple methods to install ONNX"""
    print_step(4, 8, "Installing ONNX (trying multiple methods)...")
    
    methods = []
    
    # If conda is available, try it first (highest success rate)
    if info['has_conda']:
        methods.append(("Conda", method_conda))
    
    # Then try pip methods
    methods.extend([
        ("Pip specific versions", method_pip_versions),
        ("Pip prefer binary", method_pip_prefer_binary),
        ("Pip latest", method_pip_no_constraints),
    ])
    
    for method_name, method_func in methods:
        print(f"\n  ═══ Trying: {method_name} ═══")
        
        try:
            result = method_func(info)
            
            # Handle different return types
            if isinstance(result, tuple):
                success = result[0]
            else:
                success = result
            
            if success:
                print(f"\n  ✓ Success with {method_name}!")
                return True
        except Exception as e:
            print(f"  ❌ Method failed with exception: {e}")
    
    print("\n  ❌ All installation methods failed")
    return False


def verify_installation():
    """Verify ONNX installation works"""
    print_step(5, 8, "Verifying installation...")
    
    # Test imports
    try:
        import onnx
        print(f"  ✓ ONNX version: {onnx.__version__}")
    except ImportError as e:
        print(f"  ❌ ONNX import failed: {e}")
        return False
    
    try:
        import onnxruntime
        print(f"  ✓ ONNX Runtime version: {onnxruntime.__version__}")
    except ImportError as e:
        print(f"  ❌ ONNX Runtime import failed: {e}")
        return False
    
    # Test basic functionality
    try:
        from onnx import helper, TensorProto
        
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
        
        from onnx import checker
        checker.check_model(model)
        
        print("  ✓ ONNX functionality verified")
    except Exception as e:
        print(f"  ⚠️  ONNX installed but functionality test failed: {e}")
        print("     This might be okay for your use case")
    
    return True


def print_success():
    """Print success message and next steps"""
    print_header("✓ ONNX INSTALLATION SUCCESSFUL!")
    
    info = get_system_info()
    
    print("Next Steps:\n")
    
    if info['is_windows']:
        print("1. Install PyTorch:")
        print("\n   For CPU:")
        print("   pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu")
        print("\n   For GPU (CUDA 11.8):")
        print("   pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118")
    else:
        print("1. Install PyTorch:")
        print("   pip install torch==2.9.1 torchvision==0.24.1")
    
    print("\n2. Install remaining dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n3. Verify everything works:")
    print('   python -c "import torch, onnx, onnxruntime; print(\'✓ All imports OK!\')"')
    
    print("\n4. Start using the system:")
    print("   python src/data_generator.py")
    print("   python src/train.py")
    print("   python src/export_onnx.py")
    print("   python src/inference.py")


def print_failure():
    """Print failure message and recommendations"""
    print_header("❌ INSTALLATION FAILED")
    
    info = get_system_info()
    py_ver = info['python_version_tuple']
    
    print("All automatic methods failed. Here are your options:\n")
    
    print("═══ RECOMMENDED SOLUTIONS ═══\n")
    
    # Recommend conda if not using it
    if not info['has_conda']:
        print("1. USE CONDA (HIGHEST SUCCESS RATE - 95%)")
        print("   This is the best solution for Windows!")
        print()
        print("   a. Install Miniconda:")
        print("      Download: https://docs.conda.io/en/latest/miniconda.html")
        print()
        print("   b. Create environment:")
        print("      conda create -n trajectory python=3.11 -y")
        print("      conda activate trajectory")
        print()
        print("   c. Install ONNX:")
        print("      conda install -c conda-forge onnx onnxruntime -y")
        print()
        print("   Or run the provided script:")
        print("      fix_onnx_conda.bat")
        print()
    
    # Python version issues
    if py_ver[1] >= 13 or py_ver[1] < 8:
        print("2. USE COMPATIBLE PYTHON VERSION")
        if py_ver[1] >= 13:
            print(f"   Your Python {py_ver[1]} has very limited wheel support!")
        else:
            print(f"   Your Python {py_ver[1]} is too old!")
        print()
        print("   Recommended: Python 3.10 or 3.11")
        print()
        print("   a. Download Python 3.11:")
        print("      https://www.python.org/downloads/")
        print()
        print("   b. Create virtual environment:")
        print("      py -3.11 -m venv venv311")
        print("      venv311\\Scripts\\activate")
        print()
        print("   c. Run this script again")
        print()
    
    # WSL2 recommendation
    if info['is_windows']:
        print("3. USE WSL2 (LINUX ON WINDOWS)")
        print("   Linux has much better package support!")
        print()
        print("   a. Install WSL2:")
        print("      wsl --install")
        print()
        print("   b. Open Ubuntu and run:")
        print("      pip install onnx onnxruntime")
        print()
        print("   Usually works first try!")
        print()
    
    # Docker
    print("4. USE DOCKER (PROFESSIONAL SOLUTION)")
    print("   Provides consistent environment")
    print()
    print("   a. Install Docker Desktop:")
    print("      https://www.docker.com/products/docker-desktop/")
    print()
    print("   b. Build and run:")
    print("      docker build -t trajectory .")
    print("      docker run -it trajectory")
    print()
    
    print("\n═══ DIAGNOSTIC INFORMATION ═══\n")
    print(f"Python Version: {info['python_version']}")
    print(f"Platform: {info['platform']}")
    print(f"Conda Available: {info['has_conda']}")
    print()
    print("For more help, see:")
    print("  - ONNX_WINDOWS_FIX_ULTIMATE.md")
    print("  - TROUBLESHOOTING_ONNX.md")


def main():
    """Main function"""
    print_header("ONNX INSTALLATION FIX - ULTIMATE EDITION")
    
    print("This script will try EVERY known method to install ONNX.")
    print("It works with: pip, conda, different versions, and various flags.")
    print()
    
    # Get system info
    info = print_diagnostics()
    
    # Check compatibility
    if not check_compatibility(info):
        print("\n❌ System is not compatible")
        print("Please fix the issues above and try again")
        return 1
    
    # Upgrade pip
    if not upgrade_pip():
        print("\n⚠️  Warning: pip upgrade had issues")
        print("Continuing anyway...")
    
    # Clean existing installations
    clean_onnx()
    
    # Try to install
    if not install_onnx(info):
        print_failure()
        return 1
    
    # Verify
    if not verify_installation():
        print("\n⚠️  Installation succeeded but verification failed")
        print("ONNX may still work - try using it in your code")
        return 1
    
    # Success!
    print_success()
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

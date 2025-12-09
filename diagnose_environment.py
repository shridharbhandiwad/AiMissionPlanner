#!/usr/bin/env python3
"""
Environment Diagnostic Tool
Checks your Python environment and provides specific recommendations
"""

import sys
import subprocess
import platform
import os


def run_command(cmd):
    """Run command and return success, stdout, stderr"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)


def print_section(title):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f" {title}")
    print(f"{'='*70}\n")


def check_python():
    """Check Python version"""
    print_section("PYTHON VERSION")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Version: {version_str}")
    print(f"Executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    
    # Check if version is good
    issues = []
    if version.major != 3:
        issues.append("❌ CRITICAL: Python 3.x required")
    elif version.minor < 8:
        issues.append(f"❌ CRITICAL: Python 3.8+ required (you have 3.{version.minor})")
    elif version.minor >= 13:
        issues.append(f"⚠️  WARNING: Python 3.{version.minor} has LIMITED wheel support")
        issues.append("   Recommendation: Use Python 3.10 or 3.11")
    elif version.minor == 12:
        issues.append(f"⚠️  WARNING: Python 3.12 has SOME wheel compatibility issues")
        issues.append("   Recommendation: Use Python 3.10 or 3.11 for best compatibility")
    else:
        issues.append(f"✓ Python {version_str} is compatible")
    
    for issue in issues:
        print(issue)
    
    return version.minor >= 8 and version.minor < 13


def check_virtual_env():
    """Check virtual environment"""
    print_section("VIRTUAL ENVIRONMENT")
    
    in_venv = sys.prefix != sys.base_prefix
    
    if in_venv:
        print("✓ Running in virtual environment")
        print(f"  Path: {sys.prefix}")
    else:
        print("⚠️  NOT in virtual environment")
        print("  Recommendation: Use virtual environment for cleaner installs")
        print()
        print("  Create one with:")
        print("    python -m venv venv")
        if platform.system() == "Windows":
            print("    venv\\Scripts\\activate")
        else:
            print("    source venv/bin/activate")
    
    return True


def check_pip():
    """Check pip version"""
    print_section("PIP")
    
    success, stdout, _ = run_command(f"{sys.executable} -m pip --version")
    
    if success:
        print(f"✓ pip installed: {stdout}")
        
        # Check if pip is up to date
        success2, stdout2, _ = run_command(
            f"{sys.executable} -m pip list --outdated --format=json"
        )
        if success2:
            try:
                import json
                outdated = json.loads(stdout2)
                pip_outdated = any(p['name'] == 'pip' for p in outdated)
                if pip_outdated:
                    print("⚠️  pip is outdated")
                    print(f"  Update with: {sys.executable} -m pip install --upgrade pip")
            except:
                pass
    else:
        print("❌ pip not found!")
        print(f"  Install with: {sys.executable} -m ensurepip --upgrade")
        return False
    
    return True


def check_conda():
    """Check conda availability"""
    print_section("CONDA")
    
    success, stdout, _ = run_command("conda --version")
    
    if success:
        print(f"✓ Conda available: {stdout}")
        
        # Check current environment
        success2, stdout2, _ = run_command("conda info --envs")
        if success2:
            print("\nAvailable environments:")
            for line in stdout2.split('\n'):
                if line.strip() and not line.startswith('#'):
                    # Highlight active environment
                    if '*' in line:
                        print(f"  → {line}")
                    else:
                        print(f"    {line}")
    else:
        print("⚠️  Conda not available")
        print()
        print("  Conda is HIGHLY RECOMMENDED for Windows!")
        print("  Success rate: ~95% vs ~70% with pip alone")
        print()
        print("  Install from: https://docs.conda.io/en/latest/miniconda.html")
    
    return success


def check_build_tools():
    """Check for C++ build tools (Windows)"""
    if platform.system() != "Windows":
        return True
    
    print_section("C++ BUILD TOOLS (Windows)")
    
    # Check for Visual Studio
    vs_paths = [
        "C:\\Program Files\\Microsoft Visual Studio",
        "C:\\Program Files (x86)\\Microsoft Visual Studio",
    ]
    
    vs_found = any(os.path.exists(path) for path in vs_paths)
    
    # Check for cl.exe (C++ compiler)
    success, _, _ = run_command("cl.exe")
    cl_found = success or "Microsoft" in _
    
    if vs_found or cl_found:
        print("✓ C++ build tools appear to be installed")
        if vs_found:
            print("  Visual Studio detected")
        if cl_found:
            print("  C++ compiler (cl.exe) found")
    else:
        print("⚠️  C++ build tools not detected")
        print()
        print("  These are only needed if building from source")
        print("  (Not needed if using pre-built wheels)")
        print()
        print("  If you need them:")
        print("  Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        print("  Select: 'Desktop development with C++'")
    
    return True


def check_existing_packages():
    """Check existing package installations"""
    print_section("EXISTING PACKAGES")
    
    packages = {
        "torch": "PyTorch",
        "onnx": "ONNX",
        "onnxruntime": "ONNX Runtime",
        "numpy": "NumPy",
        "scipy": "SciPy",
        "pandas": "Pandas",
        "matplotlib": "Matplotlib",
    }
    
    installed = []
    missing = []
    
    for pkg, name in packages.items():
        try:
            mod = __import__(pkg)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✓ {name}: {version}")
            installed.append(pkg)
        except ImportError:
            print(f"✗ {name}: Not installed")
            missing.append(pkg)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
    
    return len(installed) > 0


def check_internet():
    """Check internet connectivity"""
    print_section("INTERNET CONNECTIVITY")
    
    # Try to reach PyPI
    success, _, _ = run_command("ping -n 1 pypi.org" if platform.system() == "Windows" else "ping -c 1 pypi.org")
    
    if success:
        print("✓ Internet connection OK")
    else:
        print("⚠️  Cannot reach PyPI")
        print("  This might cause package installation issues")
        print("  Check your internet connection and firewall")
    
    return success


def provide_recommendations(checks):
    """Provide specific recommendations based on checks"""
    print_section("RECOMMENDATIONS")
    
    py_good, has_conda, pip_ok = checks
    
    if not py_good:
        print("🎯 ACTION REQUIRED: Python Version Issue")
        print()
        print("Your Python version has compatibility issues.")
        print()
        print("Best solution:")
        print("1. Download Python 3.11 from: https://www.python.org/downloads/")
        print("2. Install it")
        print("3. Create new virtual environment:")
        print("   py -3.11 -m venv venv311")
        if platform.system() == "Windows":
            print("   venv311\\Scripts\\activate")
        else:
            print("   source venv311/bin/activate")
        print("4. Run installation again")
        return
    
    if platform.system() == "Windows":
        if has_conda:
            print("🎯 RECOMMENDED: Use Conda (Most Reliable)")
            print()
            print("You have Conda installed - this is the best option for Windows!")
            print()
            print("Run this:")
            print("  fix_onnx_conda.bat")
            print()
            print("Or manually:")
            print("  conda create -n trajectory python=3.11 -y")
            print("  conda activate trajectory")
            print("  conda install -c conda-forge onnx onnxruntime -y")
        else:
            print("🎯 RECOMMENDED: Install Conda")
            print()
            print("Conda has 95% success rate vs 70% with pip alone on Windows")
            print()
            print("Steps:")
            print("1. Download Miniconda: https://docs.conda.io/en/latest/miniconda.html")
            print("2. Install it")
            print("3. Run: fix_onnx_conda.bat")
            print()
            print("OR try the ultimate fix script:")
            print("  python fix_onnx_ultimate.py")
    else:
        print("🎯 RECOMMENDED: Standard Installation")
        print()
        print("Linux has good wheel support. Try:")
        print("  pip install --upgrade pip")
        print("  pip install -r requirements.txt")
        print()
        print("If that fails:")
        print("  python fix_onnx_ultimate.py")
    
    print()
    print("═" * 70)
    print()
    print("Available fix scripts:")
    print("  • fix_onnx_conda.bat        - Conda installation (Windows)")
    print("  • fix_onnx_ultimate.py      - Tries all methods")
    print("  • fix_onnx.py               - Original fix script")
    print()
    print("Documentation:")
    print("  • ONNX_WINDOWS_FIX_ULTIMATE.md")
    print("  • TROUBLESHOOTING_ONNX.md")


def main():
    """Main diagnostic routine"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                 ENVIRONMENT DIAGNOSTIC TOOL                          ║
║                                                                      ║
║  This tool checks your Python environment and provides specific     ║
║  recommendations for installing ONNX and related packages.          ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run all checks
    py_good = check_python()
    check_virtual_env()
    pip_ok = check_pip()
    has_conda = check_conda()
    
    if platform.system() == "Windows":
        check_build_tools()
    
    check_existing_packages()
    check_internet()
    
    # Provide recommendations
    provide_recommendations((py_good, has_conda, pip_ok))
    
    print("\n" + "="*70)
    print("Diagnostic complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDiagnostic cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during diagnostic: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
Quick fix script - Interactive troubleshooting and repair
"""

import sys
import subprocess
import os

def run_check(command, description):
    """Run a diagnostic check"""
    print(f"\n{description}...", end=" ")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ OK")
            return True, result.stdout.strip()
        else:
            print("✗ FAILED")
            return False, result.stderr.strip()
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False, str(e)

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(text)
    print("="*60)

def main():
    print_header("3D Trajectory GUI - Quick Fix Tool")
    
    print("\nThis tool will diagnose and fix common issues.")
    print("\nPress Ctrl+C at any time to cancel.")
    
    # Step 1: Check Python
    print_header("Step 1: Checking Python")
    success, output = run_check(
        f'"{sys.executable}" --version',
        "Python installation"
    )
    if success:
        print(f"  {output}")
    else:
        print("\n✗ Python check failed. Please reinstall Python.")
        return 1
    
    # Step 2: Check pip
    success, output = run_check(
        f'"{sys.executable}" -m pip --version',
        "pip installation"
    )
    if not success:
        print("\n✗ pip is not working. Try: python -m ensurepip")
        return 1
    
    # Step 3: Check NumPy
    print_header("Step 2: Checking NumPy")
    success, output = run_check(
        f'"{sys.executable}" -c "import numpy; print(numpy.__version__)"',
        "NumPy import"
    )
    
    if not success:
        print("\n✗ NumPy is not working properly.")
        print("\nThis is the most common issue.")
        print("\nWould you like to:")
        print("  1. Run automatic NumPy repair (Recommended)")
        print("  2. See detailed NumPy diagnostics")
        print("  3. Continue checking other dependencies")
        print("  4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print("\nLaunching NumPy repair tool...")
            try:
                subprocess.run([sys.executable, 'fix_numpy.py'])
                return 0
            except:
                print("Failed to launch repair tool. Run manually: python fix_numpy.py")
                return 1
        elif choice == "2":
            print("\nLaunching NumPy diagnostics...")
            try:
                subprocess.run([sys.executable, 'diagnose_numpy.py'])
                return 0
            except:
                print("Failed to launch diagnostics. Run manually: python diagnose_numpy.py")
                return 1
        elif choice == "4":
            return 0
        # Otherwise continue
    else:
        print(f"  Version: {output}")
    
    # Step 4: Check PyQt5
    print_header("Step 3: Checking PyQt5")
    success, output = run_check(
        f'"{sys.executable}" -c "from PyQt5.QtCore import QT_VERSION_STR; print(QT_VERSION_STR)"',
        "PyQt5 import"
    )
    
    if not success:
        print("\n✗ PyQt5 is not installed or not working.")
        response = input("\nInstall PyQt5 now? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            print("\nInstalling PyQt5...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyQt5'])
            success, output = run_check(
                f'"{sys.executable}" -c "from PyQt5.QtCore import QT_VERSION_STR; print(QT_VERSION_STR)"',
                "Verifying PyQt5"
            )
            if not success:
                print("\n✗ PyQt5 installation failed.")
                return 1
    else:
        print(f"  Qt version: {output}")
    
    # Step 5: Check PyQtGraph
    print_header("Step 4: Checking PyQtGraph")
    success, output = run_check(
        f'"{sys.executable}" -c "import pyqtgraph; print(pyqtgraph.__version__)"',
        "PyQtGraph import"
    )
    
    if not success:
        print("\n✗ PyQtGraph is not installed.")
        response = input("\nInstall PyQtGraph now? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            print("\nInstalling PyQtGraph...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyqtgraph'])
    else:
        print(f"  Version: {output}")
    
    # Step 6: Check OpenGL
    print_header("Step 5: Checking OpenGL")
    success, output = run_check(
        f'"{sys.executable}" -c "import OpenGL; print(OpenGL.__version__)"',
        "PyOpenGL import"
    )
    
    if not success:
        print("\n✗ PyOpenGL is not installed.")
        response = input("\nInstall PyOpenGL now? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            print("\nInstalling PyOpenGL...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyOpenGL', 'PyOpenGL_accelerate'])
    else:
        print(f"  Version: {output}")
    
    # Step 7: Check SciPy
    print_header("Step 6: Checking SciPy")
    success, output = run_check(
        f'"{sys.executable}" -c "import scipy; print(scipy.__version__)"',
        "SciPy import"
    )
    
    if not success:
        print("\n✗ SciPy is not installed.")
        response = input("\nInstall SciPy now? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            print("\nInstalling SciPy...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'scipy'])
    else:
        print(f"  Version: {output}")
    
    # Summary
    print_header("Summary")
    print("\nRunning comprehensive diagnostics...\n")
    
    try:
        subprocess.run([sys.executable, 'diagnose_gui_startup.py'])
    except:
        print("Could not run full diagnostics. Try manually: python diagnose_gui_startup.py")
    
    print_header("Next Steps")
    print("\nIf all tests passed, try running the GUI:")
    print("  python run_trajectory_gui.py")
    print("\nFor more help, see:")
    print("  TROUBLESHOOTING.md")
    print()

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)

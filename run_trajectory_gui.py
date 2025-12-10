#!/usr/bin/env python3
"""
Launcher script for 3D Trajectory Generator GUI
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from trajectory_gui import main

if __name__ == '__main__':
    print("="*60)
    print("3D Trajectory Generator GUI")
    print("="*60)
    print("\nStarting application...")
    print("\nFeatures:")
    print("  - 12 different trajectory types")
    print("  - Real-time 3D visualization")
    print("  - Customizable physical constraints")
    print("  - Trajectory metrics calculation")
    print("  - Save/load functionality")
    print("\n" + "="*60 + "\n")
    
    main()

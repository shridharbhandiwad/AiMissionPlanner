#!/usr/bin/env python3
"""
Test PyQtGraph OpenGL display capabilities
"""

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings

# Filter warnings before NumPy import to suppress MINGW-W64 build warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

import sys

print("="*60)
print("PyQtGraph OpenGL Display Test")
print("="*60)
print()

# Test imports
print("Testing imports...")
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
    print("  ✓ PyQt5")
except ImportError as e:
    print(f"  ✗ PyQt5 FAILED: {e}")
    input("\nPress Enter to exit...")
    sys.exit(1)

try:
    import pyqtgraph as pg
    print("  ✓ PyQtGraph")
except ImportError as e:
    print(f"  ✗ PyQtGraph FAILED: {e}")
    print("\nPlease install: pip install pyqtgraph")
    input("\nPress Enter to exit...")
    sys.exit(1)

try:
    import pyqtgraph.opengl as gl
    print("  ✓ PyQtGraph OpenGL module")
except ImportError as e:
    print(f"  ✗ PyQtGraph OpenGL FAILED: {e}")
    print("\nPlease install: pip install PyOpenGL PyOpenGL_accelerate")
    input("\nPress Enter to exit...")
    sys.exit(1)

try:
    import numpy as np
    print("  ✓ NumPy")
except ImportError as e:
    print(f"  ✗ NumPy FAILED: {e}")
    input("\nPress Enter to exit...")
    sys.exit(1)

print("\nAll imports successful!")
print()

# Test OpenGL widget creation
print("Creating OpenGL test window...")
try:
    app = QApplication(sys.argv)
    
    class OpenGLTestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("OpenGL 3D View Test")
            self.setGeometry(100, 100, 800, 600)
            
            # Central widget
            central = QWidget()
            self.setCentralWidget(central)
            layout = QVBoxLayout()
            
            # Info label
            info = QLabel("Testing OpenGL 3D View...")
            layout.addWidget(info)
            
            try:
                # Create OpenGL view widget
                print("  Creating GLViewWidget...")
                self.view = gl.GLViewWidget()
                self.view.setBackgroundColor('w')
                
                # Add a simple grid
                print("  Adding grid...")
                grid = gl.GLGridItem()
                grid.scale(2, 2, 1)
                self.view.addItem(grid)
                
                # Add a simple line
                print("  Adding test line...")
                points = np.array([
                    [0, 0, 0],
                    [1, 1, 1],
                    [2, 1, 0]
                ])
                line = gl.GLLinePlotItem(pos=points, color=(1, 0, 0, 1), width=2)
                self.view.addItem(line)
                
                # Set camera
                self.view.setCameraPosition(distance=10)
                
                layout.addWidget(self.view)
                
                info.setText("✓ OpenGL 3D View Created Successfully!\n\n"
                           "You should see a 3D grid with a red line.\n"
                           "Use mouse to rotate the view.")
                info.setStyleSheet("color: green; font-weight: bold;")
                
            except Exception as e:
                print(f"  ✗ OpenGL initialization failed: {e}")
                import traceback
                traceback.print_exc()
                
                info.setText(f"✗ OpenGL FAILED\n\n"
                           f"Error: {e}\n\n"
                           f"Your system may not support OpenGL,\n"
                           f"or graphics drivers need updating.")
                info.setStyleSheet("color: red; font-weight: bold;")
            
            # Close button
            btn = QPushButton("Close Test")
            btn.clicked.connect(self.close)
            layout.addWidget(btn)
            
            central.setLayout(layout)
    
    print("  Showing window...")
    window = OpenGLTestWindow()
    window.show()
    window.raise_()
    window.activateWindow()
    
    print()
    print("="*60)
    print("If you see a 3D grid, OpenGL is working!")
    print("The trajectory GUI should work on your system.")
    print()
    print("If you see an error message in the window,")
    print("your system may not support OpenGL properly.")
    print("="*60)
    print()
    
    sys.exit(app.exec_())
    
except Exception as e:
    print(f"\n✗ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
    sys.exit(1)

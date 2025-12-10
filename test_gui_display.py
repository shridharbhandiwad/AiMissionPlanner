#!/usr/bin/env python3
"""
Simple test script to diagnose GUI display issues
"""

import sys

print("="*60)
print("GUI Display Diagnostic Test")
print("="*60)
print()

# Test 1: Check Python version
print("Test 1: Python Version")
print(f"  Python {sys.version}")
print()

# Test 2: Import PyQt5
print("Test 2: Import PyQt5")
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
    from PyQt5.QtCore import Qt
    print("  ✓ PyQt5 imported successfully")
except ImportError as e:
    print(f"  ✗ FAILED: {e}")
    print("\nPlease install PyQt5:")
    print("  pip install PyQt5")
    input("\nPress Enter to exit...")
    sys.exit(1)
print()

# Test 3: Create QApplication
print("Test 3: Create QApplication")
try:
    app = QApplication(sys.argv)
    print("  ✓ QApplication created")
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
    sys.exit(1)
print()

# Test 4: Create simple window
print("Test 4: Create and show simple window")
try:
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Test Window - GUI Display Working!")
            self.setGeometry(100, 100, 600, 400)
            
            # Central widget
            central = QWidget()
            self.setCentralWidget(central)
            
            layout = QVBoxLayout()
            
            # Add labels
            label1 = QLabel("✓ If you can see this window, PyQt5 is working!")
            label1.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
            label1.setAlignment(Qt.AlignCenter)
            
            label2 = QLabel("\nThis means the basic GUI framework is functional.")
            label2.setAlignment(Qt.AlignCenter)
            
            label3 = QLabel("\nThe 3D Trajectory GUI requires additional components:")
            label3.setAlignment(Qt.AlignCenter)
            
            label4 = QLabel("• PyQtGraph (for plotting)")
            label5 = QLabel("• PyOpenGL (for 3D visualization)")
            label6 = QLabel("• SciPy (for interpolation)")
            
            # Add button
            btn = QPushButton("Close Test")
            btn.clicked.connect(self.close)
            btn.setStyleSheet("padding: 10px; font-size: 14px;")
            
            layout.addWidget(label1)
            layout.addWidget(label2)
            layout.addWidget(label3)
            layout.addWidget(label4)
            layout.addWidget(label5)
            layout.addWidget(label6)
            layout.addStretch()
            layout.addWidget(btn)
            
            central.setLayout(layout)
    
    window = TestWindow()
    window.show()
    window.raise_()
    window.activateWindow()
    
    print("  ✓ Test window created and shown")
    print()
    print("="*60)
    print("If you see a window on your screen, PyQt5 is working!")
    print("Close the window to continue...")
    print("="*60)
    print()
    
    sys.exit(app.exec_())
    
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
    sys.exit(1)

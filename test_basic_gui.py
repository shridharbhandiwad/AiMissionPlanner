#!/usr/bin/env python3
"""
Simple test to verify basic PyQt5 functionality
"""

import sys
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

print("="*60)
print("Basic GUI Test")
print("="*60)
print()

print("Importing PyQt5...")
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
    from PyQt5.QtCore import Qt
    print("  ✓ PyQt5 imported")
except Exception as e:
    print(f"  ✗ Failed to import PyQt5: {e}")
    sys.exit(1)

print("Creating application...")
try:
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    print("  ✓ QApplication created")
except Exception as e:
    print(f"  ✗ Failed to create QApplication: {e}")
    sys.exit(1)

print("Creating window...")
try:
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("PyQt5 Test Window")
            self.setGeometry(100, 100, 400, 300)
            
            # Central widget
            central = QWidget()
            self.setCentralWidget(central)
            
            # Layout
            layout = QVBoxLayout()
            
            # Labels
            label1 = QLabel("PyQt5 is working!")
            label1.setAlignment(Qt.AlignCenter)
            label1.setStyleSheet("font-size: 18px; font-weight: bold; color: green;")
            
            label2 = QLabel("If you can see this window, PyQt5 is installed correctly.")
            label2.setAlignment(Qt.AlignCenter)
            
            # Button
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(self.close)
            
            layout.addStretch()
            layout.addWidget(label1)
            layout.addWidget(label2)
            layout.addStretch()
            layout.addWidget(close_btn)
            
            central.setLayout(layout)
    
    window = TestWindow()
    print("  ✓ Window created")
    
except Exception as e:
    print(f"  ✗ Failed to create window: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("="*60)
print("Showing window...")
print("="*60)
print()
print("A test window should appear.")
print("Close the window to exit.")
print()

try:
    window.show()
    window.raise_()
    window.activateWindow()
    sys.exit(app.exec_())
except KeyboardInterrupt:
    print("\nInterrupted by user")
    sys.exit(0)
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

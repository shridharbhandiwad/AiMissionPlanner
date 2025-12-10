#!/usr/bin/env python3
"""
Test basic PyQt5 GUI without OpenGL
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Test Window")
        self.setGeometry(100, 100, 400, 200)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        # Label
        label = QLabel("PyQt5 is working!")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Button
        button = QPushButton("Click Me")
        button.clicked.connect(self.on_click)
        layout.addWidget(button)
        
        central.setLayout(layout)
    
    def on_click(self):
        print("Button clicked! PyQt5 is responsive.")

if __name__ == '__main__':
    print("Testing basic PyQt5 functionality...")
    try:
        app = QApplication(sys.argv)
        window = TestWindow()
        window.show()
        print("Window created and shown successfully!")
        print("If you see a window, PyQt5 is working correctly.")
        print("Close the window to exit.")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

"""
3D Trajectory Generator GUI
PyQt5-based interactive GUI for generating and visualizing various trajectory types
"""

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings

# Filter warnings before NumPy import to suppress MINGW-W64 build warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

import sys
import numpy as np
from typing import List, Dict, Tuple, Optional
import json

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QGroupBox,
    QGridLayout, QDoubleSpinBox, QSpinBox, QCheckBox,
    QTabWidget, QTextEdit, QSplitter, QFileDialog, QMessageBox,
    QScrollArea, QSlider
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget, GLLinePlotItem, GLScatterPlotItem, GLGridItem, GLAxisItem


class TrajectoryParameters:
    """Parameters for trajectory generation"""
    def __init__(self):
        # Start and end points
        self.start_x = 0.0
        self.start_y = 0.0
        self.start_z = 100.0
        
        self.end_x = 800.0
        self.end_y = 600.0
        self.end_z = 200.0
        
        # Physical constraints
        self.max_altitude = 500.0
        self.min_altitude = 50.0
        self.max_speed = 250.0  # m/s
        self.max_acceleration = 50.0  # m/s^2
        self.max_g_turn = 4.0  # g's
        self.turn_radius = 100.0  # meters
        
        # Trajectory parameters
        self.n_waypoints = 50
        self.trajectory_type = "bezier"
        self.smoothness = 0.8
        self.curvature_limit = 0.01  # rad/m
        
        # Advanced parameters
        self.banking_angle = 30.0  # degrees
        self.climb_rate = 10.0  # m/s
        self.descent_rate = 8.0  # m/s
        
    def to_dict(self) -> Dict:
        """Convert parameters to dictionary"""
        return {
            'start': [self.start_x, self.start_y, self.start_z],
            'end': [self.end_x, self.end_y, self.end_z],
            'max_altitude': self.max_altitude,
            'min_altitude': self.min_altitude,
            'max_speed': self.max_speed,
            'max_acceleration': self.max_acceleration,
            'max_g_turn': self.max_g_turn,
            'turn_radius': self.turn_radius,
            'n_waypoints': self.n_waypoints,
            'trajectory_type': self.trajectory_type,
            'smoothness': self.smoothness,
            'curvature_limit': self.curvature_limit,
            'banking_angle': self.banking_angle,
            'climb_rate': self.climb_rate,
            'descent_rate': self.descent_rate
        }
    
    def from_dict(self, data: Dict):
        """Load parameters from dictionary"""
        self.start_x, self.start_y, self.start_z = data['start']
        self.end_x, self.end_y, self.end_z = data['end']
        self.max_altitude = data['max_altitude']
        self.min_altitude = data['min_altitude']
        self.max_speed = data['max_speed']
        self.max_acceleration = data['max_acceleration']
        self.max_g_turn = data['max_g_turn']
        self.turn_radius = data['turn_radius']
        self.n_waypoints = data['n_waypoints']
        self.trajectory_type = data['trajectory_type']
        self.smoothness = data['smoothness']
        self.curvature_limit = data['curvature_limit']
        self.banking_angle = data['banking_angle']
        self.climb_rate = data['climb_rate']
        self.descent_rate = data['descent_rate']


class Advanced3DTrajectoryGenerator:
    """Advanced trajectory generation with various patterns"""
    
    def __init__(self):
        self.gravity = 9.81  # m/s^2
    
    def generate_trajectory(self, params: TrajectoryParameters) -> np.ndarray:
        """Generate trajectory based on type"""
        start = np.array([params.start_x, params.start_y, params.start_z])
        end = np.array([params.end_x, params.end_y, params.end_z])
        
        trajectory_type = params.trajectory_type.lower()
        
        if trajectory_type == "bezier":
            return self.generate_bezier(start, end, params)
        elif trajectory_type == "circular":
            return self.generate_circular(start, end, params)
        elif trajectory_type == "ascending_spiral":
            return self.generate_ascending_spiral(start, end, params)
        elif trajectory_type == "descending_spiral":
            return self.generate_descending_spiral(start, end, params)
        elif trajectory_type == "s_curve":
            return self.generate_s_curve(start, end, params)
        elif trajectory_type == "l_curve":
            return self.generate_l_curve(start, end, params)
        elif trajectory_type == "zigzag":
            return self.generate_zigzag(start, end, params)
        elif trajectory_type == "helix":
            return self.generate_helix(start, end, params)
        elif trajectory_type == "figure_eight":
            return self.generate_figure_eight(start, end, params)
        elif trajectory_type == "parabolic":
            return self.generate_parabolic(start, end, params)
        elif trajectory_type == "combat_maneuver":
            return self.generate_combat_maneuver(start, end, params)
        elif trajectory_type == "terrain_following":
            return self.generate_terrain_following(start, end, params)
        else:
            return self.generate_bezier(start, end, params)
    
    def generate_bezier(self, start: np.ndarray, end: np.ndarray, 
                       params: TrajectoryParameters) -> np.ndarray:
        """Generate Bezier curve trajectory"""
        n = params.n_waypoints
        
        # Control points
        mid_point = (start + end) / 2
        direction = end - start
        perpendicular = np.array([-direction[1], direction[0], 0])
        if np.linalg.norm(perpendicular) > 0:
            perpendicular = perpendicular / np.linalg.norm(perpendicular)
        
        offset = params.turn_radius * params.smoothness
        control1 = start + direction * 0.25 + perpendicular * offset
        control2 = end - direction * 0.25 - perpendicular * offset
        
        # Clamp altitudes
        control1[2] = np.clip(control1[2], params.min_altitude, params.max_altitude)
        control2[2] = np.clip(control2[2], params.min_altitude, params.max_altitude)
        
        control_points = np.array([start, control1, control2, end])
        
        t = np.linspace(0, 1, n)
        trajectory = self._bezier_curve(control_points, t)
        
        return trajectory
    
    def generate_circular(self, start: np.ndarray, end: np.ndarray,
                         params: TrajectoryParameters) -> np.ndarray:
        """Generate circular arc trajectory"""
        n = params.n_waypoints
        
        center = (start + end) / 2
        radius = np.linalg.norm(end - start) / 2
        
        # Create circular path in XY plane
        angles = np.linspace(0, np.pi, n)
        
        # Direction vector
        direction = end - start
        direction_xy = direction[:2] / np.linalg.norm(direction[:2])
        
        trajectory = np.zeros((n, 3))
        for i, angle in enumerate(angles):
            offset = radius * np.array([np.cos(angle), np.sin(angle), 0])
            # Rotate offset to align with direction
            cos_theta = direction_xy[0]
            sin_theta = direction_xy[1]
            rotated_offset = np.array([
                offset[0] * cos_theta - offset[1] * sin_theta,
                offset[0] * sin_theta + offset[1] * cos_theta,
                offset[2]
            ])
            trajectory[i] = center + rotated_offset
            
            # Interpolate altitude
            alpha = i / (n - 1)
            trajectory[i, 2] = start[2] * (1 - alpha) + end[2] * alpha
        
        return trajectory
    
    def generate_ascending_spiral(self, start: np.ndarray, end: np.ndarray,
                                 params: TrajectoryParameters) -> np.ndarray:
        """Generate ascending spiral trajectory"""
        n = params.n_waypoints
        
        # Spiral parameters
        center_xy = (start[:2] + end[:2]) / 2
        radius = params.turn_radius
        n_turns = 2.0
        
        angles = np.linspace(0, 2 * np.pi * n_turns, n)
        
        trajectory = np.zeros((n, 3))
        for i, angle in enumerate(angles):
            alpha = i / (n - 1)
            
            # Spiral outward
            r = radius * (1 + alpha * 0.5)
            
            trajectory[i, 0] = center_xy[0] + r * np.cos(angle)
            trajectory[i, 1] = center_xy[1] + r * np.sin(angle)
            trajectory[i, 2] = start[2] + (end[2] - start[2]) * alpha
        
        return trajectory
    
    def generate_descending_spiral(self, start: np.ndarray, end: np.ndarray,
                                  params: TrajectoryParameters) -> np.ndarray:
        """Generate descending spiral trajectory"""
        n = params.n_waypoints
        
        center_xy = (start[:2] + end[:2]) / 2
        radius = params.turn_radius
        n_turns = 2.0
        
        angles = np.linspace(0, 2 * np.pi * n_turns, n)
        
        trajectory = np.zeros((n, 3))
        for i, angle in enumerate(angles):
            alpha = i / (n - 1)
            
            # Spiral inward
            r = radius * (1 - alpha * 0.3)
            
            trajectory[i, 0] = center_xy[0] + r * np.cos(angle)
            trajectory[i, 1] = center_xy[1] + r * np.sin(angle)
            trajectory[i, 2] = start[2] - (start[2] - end[2]) * alpha
        
        return trajectory
    
    def generate_s_curve(self, start: np.ndarray, end: np.ndarray,
                        params: TrajectoryParameters) -> np.ndarray:
        """Generate S-curve trajectory"""
        n = params.n_waypoints
        
        direction = end - start
        distance = np.linalg.norm(direction[:2])
        
        t = np.linspace(0, 1, n)
        
        # S-curve using sigmoid
        s_curve = 1 / (1 + np.exp(-12 * (t - 0.5)))
        
        trajectory = np.zeros((n, 3))
        for i in range(n):
            alpha = s_curve[i]
            
            # Linear interpolation along main direction
            trajectory[i] = start + direction * alpha
            
            # Add lateral S-curve
            lateral_offset = params.turn_radius * np.sin(t[i] * np.pi)
            perpendicular = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perpendicular) > 0:
                perpendicular = perpendicular / np.linalg.norm(perpendicular)
                trajectory[i, :2] += perpendicular[:2] * lateral_offset
        
        return trajectory
    
    def generate_l_curve(self, start: np.ndarray, end: np.ndarray,
                        params: TrajectoryParameters) -> np.ndarray:
        """Generate L-shaped curve trajectory"""
        n = params.n_waypoints
        
        # Corner point
        corner = np.array([end[0], start[1], (start[2] + end[2]) / 2])
        
        # Split into two segments
        n1 = n // 2
        n2 = n - n1
        
        # First segment: start to corner
        t1 = np.linspace(0, 1, n1)
        seg1 = np.zeros((n1, 3))
        for i, t in enumerate(t1):
            seg1[i] = start * (1 - t) + corner * t
        
        # Second segment: corner to end
        t2 = np.linspace(0, 1, n2)
        seg2 = np.zeros((n2, 3))
        for i, t in enumerate(t2):
            seg2[i] = corner * (1 - t) + end * t
        
        trajectory = np.vstack([seg1, seg2])
        
        # Smooth the corner
        from scipy.interpolate import CubicSpline
        indices = np.arange(len(trajectory))
        cs = CubicSpline(indices, trajectory, bc_type='natural')
        smooth_indices = np.linspace(0, len(trajectory) - 1, n)
        trajectory = cs(smooth_indices)
        
        return trajectory
    
    def generate_zigzag(self, start: np.ndarray, end: np.ndarray,
                       params: TrajectoryParameters) -> np.ndarray:
        """Generate zigzag trajectory"""
        n = params.n_waypoints
        n_zigs = 3
        
        direction = end - start
        perpendicular = np.array([-direction[1], direction[0], 0])
        if np.linalg.norm(perpendicular) > 0:
            perpendicular = perpendicular / np.linalg.norm(perpendicular)
        
        trajectory = np.zeros((n, 3))
        for i in range(n):
            alpha = i / (n - 1)
            
            # Base position
            trajectory[i] = start + direction * alpha
            
            # Zigzag offset
            zig_offset = params.turn_radius * np.sin(alpha * n_zigs * 2 * np.pi)
            trajectory[i, :2] += perpendicular[:2] * zig_offset
        
        return trajectory
    
    def generate_helix(self, start: np.ndarray, end: np.ndarray,
                      params: TrajectoryParameters) -> np.ndarray:
        """Generate helix trajectory"""
        n = params.n_waypoints
        n_turns = 3.0
        
        direction = end - start
        distance = np.linalg.norm(direction[:2])
        
        angles = np.linspace(0, 2 * np.pi * n_turns, n)
        
        trajectory = np.zeros((n, 3))
        for i, angle in enumerate(angles):
            alpha = i / (n - 1)
            
            # Helix around axis
            radius = params.turn_radius * 0.5
            
            # Direction along path
            trajectory[i] = start + direction * alpha
            
            # Add circular component
            perpendicular1 = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perpendicular1) > 0:
                perpendicular1 = perpendicular1 / np.linalg.norm(perpendicular1)
            
            perpendicular2 = np.cross(direction, perpendicular1)
            if np.linalg.norm(perpendicular2) > 0:
                perpendicular2 = perpendicular2 / np.linalg.norm(perpendicular2)
            
            offset = radius * (np.cos(angle) * perpendicular1 + np.sin(angle) * perpendicular2)
            trajectory[i] += offset
        
        return trajectory
    
    def generate_figure_eight(self, start: np.ndarray, end: np.ndarray,
                             params: TrajectoryParameters) -> np.ndarray:
        """Generate figure-eight trajectory"""
        n = params.n_waypoints
        
        center = (start + end) / 2
        radius = params.turn_radius
        
        t = np.linspace(0, 2 * np.pi, n)
        
        trajectory = np.zeros((n, 3))
        for i, angle in enumerate(t):
            # Lemniscate of Bernoulli
            scale = radius / (1 + np.sin(angle)**2)
            
            trajectory[i, 0] = center[0] + scale * np.cos(angle)
            trajectory[i, 1] = center[1] + scale * np.sin(angle) * np.cos(angle)
            
            # Altitude variation
            alpha = i / (n - 1)
            trajectory[i, 2] = start[2] * (1 - alpha) + end[2] * alpha
        
        return trajectory
    
    def generate_parabolic(self, start: np.ndarray, end: np.ndarray,
                          params: TrajectoryParameters) -> np.ndarray:
        """Generate parabolic trajectory (ballistic-like)"""
        n = params.n_waypoints
        
        trajectory = np.zeros((n, 3))
        for i in range(n):
            alpha = i / (n - 1)
            
            # Linear interpolation in XY
            trajectory[i, :2] = start[:2] * (1 - alpha) + end[:2] * alpha
            
            # Parabolic altitude
            peak_altitude = max(start[2], end[2]) + params.turn_radius
            trajectory[i, 2] = (start[2] * (1 - alpha) + end[2] * alpha + 
                               4 * peak_altitude * alpha * (1 - alpha))
            
            # Clamp altitude
            trajectory[i, 2] = np.clip(trajectory[i, 2], 
                                      params.min_altitude, params.max_altitude)
        
        return trajectory
    
    def generate_combat_maneuver(self, start: np.ndarray, end: np.ndarray,
                                params: TrajectoryParameters) -> np.ndarray:
        """Generate combat maneuver trajectory (Immelmann turn-like)"""
        n = params.n_waypoints
        
        # Split into climb and roll phases
        n_climb = n // 2
        n_roll = n - n_climb
        
        trajectory = np.zeros((n, 3))
        
        direction = end - start
        midpoint = start + direction * 0.5
        
        # Climb phase - vertical loop
        for i in range(n_climb):
            alpha = i / n_climb
            angle = alpha * np.pi
            
            radius = params.turn_radius
            
            trajectory[i, :2] = start[:2] + direction[:2] * alpha * 0.5
            trajectory[i, 2] = start[2] + radius * (1 - np.cos(angle))
        
        # Roll phase - horizontal to end
        for i in range(n_roll):
            alpha = i / n_roll
            idx = n_climb + i
            
            trajectory[idx] = midpoint * (1 - alpha) + end * alpha
            
            # Add rolling motion
            roll_offset = params.turn_radius * 0.3 * np.sin(alpha * 2 * np.pi)
            trajectory[idx, 1] += roll_offset
        
        return trajectory
    
    def generate_terrain_following(self, start: np.ndarray, end: np.ndarray,
                                  params: TrajectoryParameters) -> np.ndarray:
        """Generate terrain-following trajectory with altitude variations"""
        n = params.n_waypoints
        
        trajectory = np.zeros((n, 3))
        
        for i in range(n):
            alpha = i / (n - 1)
            
            # Linear interpolation in XY
            trajectory[i, :2] = start[:2] * (1 - alpha) + end[:2] * alpha
            
            # Simulated terrain following with sine waves
            base_altitude = start[2] * (1 - alpha) + end[2] * alpha
            
            # Multiple frequency terrain variation
            terrain_var = (30 * np.sin(alpha * 4 * np.pi) + 
                          20 * np.sin(alpha * 8 * np.pi + 0.5) +
                          10 * np.sin(alpha * 16 * np.pi))
            
            trajectory[i, 2] = base_altitude + terrain_var
            
            # Clamp altitude
            trajectory[i, 2] = np.clip(trajectory[i, 2],
                                      params.min_altitude, params.max_altitude)
        
        return trajectory
    
    def _bezier_curve(self, control_points: np.ndarray, t: np.ndarray) -> np.ndarray:
        """Evaluate Bezier curve"""
        n = len(control_points) - 1
        trajectory = np.zeros((len(t), 3))
        
        for i, t_val in enumerate(t):
            point = np.zeros(3)
            for j, cp in enumerate(control_points):
                bernstein = self._bernstein_poly(j, n, t_val)
                point += bernstein * cp
            trajectory[i] = point
        
        return trajectory
    
    def _bernstein_poly(self, i: int, n: int, t: float) -> float:
        """Bernstein polynomial"""
        from math import comb
        return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
    
    def calculate_metrics(self, trajectory: np.ndarray, params: TrajectoryParameters) -> Dict:
        """Calculate trajectory metrics"""
        # Path length
        path_length = 0.0
        for i in range(len(trajectory) - 1):
            path_length += np.linalg.norm(trajectory[i+1] - trajectory[i])
        
        # Curvature
        curvatures = []
        for i in range(1, len(trajectory) - 1):
            v1 = trajectory[i] - trajectory[i-1]
            v2 = trajectory[i+1] - trajectory[i]
            
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            
            if norm1 > 1e-6 and norm2 > 1e-6:
                cos_angle = np.dot(v1, v2) / (norm1 * norm2)
                cos_angle = np.clip(cos_angle, -1, 1)
                angle = np.arccos(cos_angle)
                curvature = angle / norm1
                curvatures.append(curvature)
        
        avg_curvature = np.mean(curvatures) if curvatures else 0.0
        max_curvature = np.max(curvatures) if curvatures else 0.0
        
        # G-forces (simplified)
        max_g_force = 0.0
        if len(curvatures) > 0:
            max_g_force = max_curvature * (params.max_speed ** 2) / self.gravity
        
        # Altitude stats
        altitudes = trajectory[:, 2]
        
        # Straight line distance
        straight_line = np.linalg.norm(trajectory[-1] - trajectory[0])
        
        return {
            'path_length': path_length,
            'straight_line_distance': straight_line,
            'path_efficiency': straight_line / max(path_length, 1.0),
            'avg_curvature': avg_curvature,
            'max_curvature': max_curvature,
            'max_g_force': max_g_force,
            'min_altitude': float(np.min(altitudes)),
            'max_altitude': float(np.max(altitudes)),
            'altitude_range': float(np.max(altitudes) - np.min(altitudes)),
            'n_waypoints': len(trajectory)
        }


class Visualizer3D(QWidget):
    """3D visualization widget using PyQtGraph"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.trajectories = []
        self.trajectory_items = []
        self.waypoint_items = []
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Create 3D view
        self.view = gl.GLViewWidget()
        self.view.setBackgroundColor('k')
        
        # Add grid
        self.grid = gl.GLGridItem()
        self.grid.scale(100, 100, 10)
        self.view.addItem(self.grid)
        
        # Add axes
        self.add_axes()
        
        # Set camera position
        self.view.setCameraPosition(distance=2000, elevation=30, azimuth=45)
        
        layout.addWidget(self.view)
        self.setLayout(layout)
    
    def add_axes(self):
        """Add coordinate axes"""
        # X axis (red)
        x_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [500, 0, 0]]),
            color=(1, 0, 0, 1),
            width=3
        )
        self.view.addItem(x_axis)
        
        # Y axis (green)
        y_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [0, 500, 0]]),
            color=(0, 1, 0, 1),
            width=3
        )
        self.view.addItem(y_axis)
        
        # Z axis (blue)
        z_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, 0], [0, 0, 500]]),
            color=(0, 0, 1, 1),
            width=3
        )
        self.view.addItem(z_axis)
    
    def add_trajectory(self, trajectory: np.ndarray, color=(0.5, 0.8, 1.0, 0.8)):
        """Add trajectory to visualization"""
        # Add trajectory line
        traj_item = gl.GLLinePlotItem(
            pos=trajectory,
            color=color,
            width=2,
            antialias=True
        )
        self.view.addItem(traj_item)
        self.trajectory_items.append(traj_item)
        
        # Add waypoint markers
        waypoint_item = gl.GLScatterPlotItem(
            pos=trajectory,
            color=color,
            size=5,
            pxMode=True
        )
        self.view.addItem(waypoint_item)
        self.waypoint_items.append(waypoint_item)
        
        # Add start and end markers
        start_marker = gl.GLScatterPlotItem(
            pos=trajectory[0:1],
            color=(0, 1, 0, 1),
            size=15,
            pxMode=True
        )
        self.view.addItem(start_marker)
        self.waypoint_items.append(start_marker)
        
        end_marker = gl.GLScatterPlotItem(
            pos=trajectory[-1:],
            color=(1, 0, 0, 1),
            size=15,
            pxMode=True
        )
        self.view.addItem(end_marker)
        self.waypoint_items.append(end_marker)
        
        self.trajectories.append(trajectory)
    
    def clear_trajectories(self):
        """Clear all trajectories"""
        for item in self.trajectory_items + self.waypoint_items:
            self.view.removeItem(item)
        
        self.trajectory_items.clear()
        self.waypoint_items.clear()
        self.trajectories.clear()


class TrajectoryGeneratorGUI(QMainWindow):
    """Main GUI window"""
    
    def __init__(self):
        super().__init__()
        
        self.params = TrajectoryParameters()
        self.generator = Advanced3DTrajectoryGenerator()
        self.current_trajectory = None
        
        self.init_ui()
        self.setWindowTitle("3D Trajectory Generator")
        self.setGeometry(100, 100, 1600, 900)
    
    def init_ui(self):
        """Initialize UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left panel - Controls
        left_panel = self.create_control_panel()
        
        # Right panel - 3D Visualization
        self.visualizer = Visualizer3D()
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.visualizer)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
    
    def create_control_panel(self) -> QWidget:
        """Create control panel"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Create tabs
        tabs = QTabWidget()
        
        # Tab 1: Basic Parameters
        basic_tab = self.create_basic_params_tab()
        tabs.addTab(basic_tab, "Basic")
        
        # Tab 2: Advanced Parameters
        advanced_tab = self.create_advanced_params_tab()
        tabs.addTab(advanced_tab, "Advanced")
        
        # Tab 3: Trajectory Type
        trajectory_tab = self.create_trajectory_type_tab()
        tabs.addTab(trajectory_tab, "Trajectory Type")
        
        # Tab 4: Metrics
        metrics_tab = self.create_metrics_tab()
        tabs.addTab(metrics_tab, "Metrics")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        generate_btn = QPushButton("Generate Trajectory")
        generate_btn.clicked.connect(self.generate_trajectory)
        generate_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
        
        save_btn = QPushButton("Save Trajectory")
        save_btn.clicked.connect(self.save_trajectory)
        
        load_btn = QPushButton("Load Parameters")
        load_btn.clicked.connect(self.load_parameters)
        
        button_layout.addWidget(generate_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(load_btn)
        
        layout.addLayout(button_layout)
        
        panel.setLayout(layout)
        return panel
    
    def create_basic_params_tab(self) -> QWidget:
        """Create basic parameters tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Scroll area for parameters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Start point group
        start_group = QGroupBox("Start Point")
        start_layout = QGridLayout()
        
        start_layout.addWidget(QLabel("X (m):"), 0, 0)
        self.start_x = QDoubleSpinBox()
        self.start_x.setRange(-5000, 5000)
        self.start_x.setValue(self.params.start_x)
        self.start_x.setSingleStep(10)
        start_layout.addWidget(self.start_x, 0, 1)
        
        start_layout.addWidget(QLabel("Y (m):"), 1, 0)
        self.start_y = QDoubleSpinBox()
        self.start_y.setRange(-5000, 5000)
        self.start_y.setValue(self.params.start_y)
        self.start_y.setSingleStep(10)
        start_layout.addWidget(self.start_y, 1, 1)
        
        start_layout.addWidget(QLabel("Z (m):"), 2, 0)
        self.start_z = QDoubleSpinBox()
        self.start_z.setRange(0, 2000)
        self.start_z.setValue(self.params.start_z)
        self.start_z.setSingleStep(10)
        start_layout.addWidget(self.start_z, 2, 1)
        
        start_group.setLayout(start_layout)
        scroll_layout.addWidget(start_group)
        
        # End point group
        end_group = QGroupBox("End Point")
        end_layout = QGridLayout()
        
        end_layout.addWidget(QLabel("X (m):"), 0, 0)
        self.end_x = QDoubleSpinBox()
        self.end_x.setRange(-5000, 5000)
        self.end_x.setValue(self.params.end_x)
        self.end_x.setSingleStep(10)
        end_layout.addWidget(self.end_x, 0, 1)
        
        end_layout.addWidget(QLabel("Y (m):"), 1, 0)
        self.end_y = QDoubleSpinBox()
        self.end_y.setRange(-5000, 5000)
        self.end_y.setValue(self.params.end_y)
        self.end_y.setSingleStep(10)
        end_layout.addWidget(self.end_y, 1, 1)
        
        end_layout.addWidget(QLabel("Z (m):"), 2, 0)
        self.end_z = QDoubleSpinBox()
        self.end_z.setRange(0, 2000)
        self.end_z.setValue(self.params.end_z)
        self.end_z.setSingleStep(10)
        end_layout.addWidget(self.end_z, 2, 1)
        
        end_group.setLayout(end_layout)
        scroll_layout.addWidget(end_group)
        
        # Constraints group
        constraints_group = QGroupBox("Physical Constraints")
        constraints_layout = QGridLayout()
        
        constraints_layout.addWidget(QLabel("Max Altitude (m):"), 0, 0)
        self.max_altitude = QDoubleSpinBox()
        self.max_altitude.setRange(50, 5000)
        self.max_altitude.setValue(self.params.max_altitude)
        self.max_altitude.setSingleStep(50)
        constraints_layout.addWidget(self.max_altitude, 0, 1)
        
        constraints_layout.addWidget(QLabel("Min Altitude (m):"), 1, 0)
        self.min_altitude = QDoubleSpinBox()
        self.min_altitude.setRange(0, 1000)
        self.min_altitude.setValue(self.params.min_altitude)
        self.min_altitude.setSingleStep(10)
        constraints_layout.addWidget(self.min_altitude, 1, 1)
        
        constraints_layout.addWidget(QLabel("Max Speed (m/s):"), 2, 0)
        self.max_speed = QDoubleSpinBox()
        self.max_speed.setRange(10, 1000)
        self.max_speed.setValue(self.params.max_speed)
        self.max_speed.setSingleStep(10)
        constraints_layout.addWidget(self.max_speed, 2, 1)
        
        constraints_layout.addWidget(QLabel("Max G-Turn:"), 3, 0)
        self.max_g_turn = QDoubleSpinBox()
        self.max_g_turn.setRange(1, 12)
        self.max_g_turn.setValue(self.params.max_g_turn)
        self.max_g_turn.setSingleStep(0.5)
        constraints_layout.addWidget(self.max_g_turn, 3, 1)
        
        constraints_layout.addWidget(QLabel("Turn Radius (m):"), 4, 0)
        self.turn_radius = QDoubleSpinBox()
        self.turn_radius.setRange(10, 1000)
        self.turn_radius.setValue(self.params.turn_radius)
        self.turn_radius.setSingleStep(10)
        constraints_layout.addWidget(self.turn_radius, 4, 1)
        
        constraints_layout.addWidget(QLabel("Number of Waypoints:"), 5, 0)
        self.n_waypoints = QSpinBox()
        self.n_waypoints.setRange(10, 500)
        self.n_waypoints.setValue(self.params.n_waypoints)
        self.n_waypoints.setSingleStep(10)
        constraints_layout.addWidget(self.n_waypoints, 5, 1)
        
        constraints_group.setLayout(constraints_layout)
        scroll_layout.addWidget(constraints_group)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget
    
    def create_advanced_params_tab(self) -> QWidget:
        """Create advanced parameters tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Advanced parameters group
        advanced_group = QGroupBox("Advanced Parameters")
        advanced_layout = QGridLayout()
        
        advanced_layout.addWidget(QLabel("Smoothness (0-1):"), 0, 0)
        self.smoothness = QDoubleSpinBox()
        self.smoothness.setRange(0, 1)
        self.smoothness.setValue(self.params.smoothness)
        self.smoothness.setSingleStep(0.1)
        advanced_layout.addWidget(self.smoothness, 0, 1)
        
        advanced_layout.addWidget(QLabel("Max Acceleration (m/s²):"), 1, 0)
        self.max_acceleration = QDoubleSpinBox()
        self.max_acceleration.setRange(1, 200)
        self.max_acceleration.setValue(self.params.max_acceleration)
        self.max_acceleration.setSingleStep(5)
        advanced_layout.addWidget(self.max_acceleration, 1, 1)
        
        advanced_layout.addWidget(QLabel("Banking Angle (°):"), 2, 0)
        self.banking_angle = QDoubleSpinBox()
        self.banking_angle.setRange(0, 90)
        self.banking_angle.setValue(self.params.banking_angle)
        self.banking_angle.setSingleStep(5)
        advanced_layout.addWidget(self.banking_angle, 2, 1)
        
        advanced_layout.addWidget(QLabel("Climb Rate (m/s):"), 3, 0)
        self.climb_rate = QDoubleSpinBox()
        self.climb_rate.setRange(1, 50)
        self.climb_rate.setValue(self.params.climb_rate)
        self.climb_rate.setSingleStep(1)
        advanced_layout.addWidget(self.climb_rate, 3, 1)
        
        advanced_layout.addWidget(QLabel("Descent Rate (m/s):"), 4, 0)
        self.descent_rate = QDoubleSpinBox()
        self.descent_rate.setRange(1, 50)
        self.descent_rate.setValue(self.params.descent_rate)
        self.descent_rate.setSingleStep(1)
        advanced_layout.addWidget(self.descent_rate, 4, 1)
        
        advanced_layout.addWidget(QLabel("Curvature Limit (rad/m):"), 5, 0)
        self.curvature_limit = QDoubleSpinBox()
        self.curvature_limit.setRange(0.001, 0.1)
        self.curvature_limit.setValue(self.params.curvature_limit)
        self.curvature_limit.setSingleStep(0.001)
        self.curvature_limit.setDecimals(4)
        advanced_layout.addWidget(self.curvature_limit, 5, 1)
        
        advanced_group.setLayout(advanced_layout)
        scroll_layout.addWidget(advanced_group)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget
    
    def create_trajectory_type_tab(self) -> QWidget:
        """Create trajectory type selection tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        type_group = QGroupBox("Trajectory Type")
        type_layout = QVBoxLayout()
        
        self.trajectory_type = QComboBox()
        trajectory_types = [
            "Bezier",
            "Circular",
            "Ascending Spiral",
            "Descending Spiral",
            "S-Curve",
            "L-Curve",
            "Zigzag",
            "Helix",
            "Figure Eight",
            "Parabolic",
            "Combat Maneuver",
            "Terrain Following"
        ]
        self.trajectory_type.addItems(trajectory_types)
        self.trajectory_type.setCurrentText("Bezier")
        type_layout.addWidget(self.trajectory_type)
        
        # Description label
        self.type_description = QTextEdit()
        self.type_description.setReadOnly(True)
        self.type_description.setMaximumHeight(150)
        self.update_trajectory_description()
        self.trajectory_type.currentTextChanged.connect(self.update_trajectory_description)
        type_layout.addWidget(QLabel("Description:"))
        type_layout.addWidget(self.type_description)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_metrics_tab(self) -> QWidget:
        """Create metrics display tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        metrics_group = QGroupBox("Trajectory Metrics")
        metrics_layout = QVBoxLayout()
        
        self.metrics_display = QTextEdit()
        self.metrics_display.setReadOnly(True)
        self.metrics_display.setPlainText("Generate a trajectory to see metrics...")
        
        metrics_layout.addWidget(self.metrics_display)
        metrics_group.setLayout(metrics_layout)
        
        layout.addWidget(metrics_group)
        widget.setLayout(layout)
        return widget
    
    def update_trajectory_description(self):
        """Update trajectory type description"""
        descriptions = {
            "Bezier": "Smooth curve using Bezier control points. Good for general-purpose smooth paths.",
            "Circular": "Circular arc connecting start and end points. Maintains constant turn rate.",
            "Ascending Spiral": "Spiral path gaining altitude. Useful for climb maneuvers with lateral displacement.",
            "Descending Spiral": "Spiral path losing altitude. Useful for descent maneuvers with controlled rate.",
            "S-Curve": "S-shaped lateral deviation while progressing to target. Good for evasive maneuvers.",
            "L-Curve": "L-shaped path with sharp corner. Useful for waypoint navigation.",
            "Zigzag": "Zigzag pattern with periodic lateral deviations. Useful for search patterns.",
            "Helix": "Helical path around axis of motion. Combines forward progress with circular motion.",
            "Figure Eight": "Figure-eight pattern in 3D space. Complex aerobatic maneuver.",
            "Parabolic": "Parabolic arc with peak altitude. Ballistic-style trajectory.",
            "Combat Maneuver": "Aggressive maneuver combining climb and roll. Immelmann turn-inspired.",
            "Terrain Following": "Path following simulated terrain variations. Low-altitude flight profile."
        }
        
        current_type = self.trajectory_type.currentText()
        description = descriptions.get(current_type, "No description available.")
        self.type_description.setPlainText(description)
    
    def update_parameters_from_ui(self):
        """Update parameters from UI controls"""
        # Start point
        self.params.start_x = self.start_x.value()
        self.params.start_y = self.start_y.value()
        self.params.start_z = self.start_z.value()
        
        # End point
        self.params.end_x = self.end_x.value()
        self.params.end_y = self.end_y.value()
        self.params.end_z = self.end_z.value()
        
        # Constraints
        self.params.max_altitude = self.max_altitude.value()
        self.params.min_altitude = self.min_altitude.value()
        self.params.max_speed = self.max_speed.value()
        self.params.max_g_turn = self.max_g_turn.value()
        self.params.turn_radius = self.turn_radius.value()
        self.params.n_waypoints = self.n_waypoints.value()
        
        # Advanced
        self.params.smoothness = self.smoothness.value()
        self.params.max_acceleration = self.max_acceleration.value()
        self.params.banking_angle = self.banking_angle.value()
        self.params.climb_rate = self.climb_rate.value()
        self.params.descent_rate = self.descent_rate.value()
        self.params.curvature_limit = self.curvature_limit.value()
        
        # Trajectory type
        self.params.trajectory_type = self.trajectory_type.currentText().replace(" ", "_").lower()
    
    def generate_trajectory(self):
        """Generate and visualize trajectory"""
        try:
            # Update parameters
            self.update_parameters_from_ui()
            
            # Generate trajectory
            trajectory = self.generator.generate_trajectory(self.params)
            self.current_trajectory = trajectory
            
            # Calculate metrics
            metrics = self.generator.calculate_metrics(trajectory, self.params)
            
            # Display metrics
            self.display_metrics(metrics)
            
            # Visualize
            self.visualizer.add_trajectory(trajectory)
            
            QMessageBox.information(self, "Success", 
                                   f"Generated trajectory with {len(trajectory)} waypoints!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate trajectory:\n{str(e)}")
    
    def display_metrics(self, metrics: Dict):
        """Display trajectory metrics"""
        text = "=== Trajectory Metrics ===\n\n"
        text += f"Path Length: {metrics['path_length']:.2f} m\n"
        text += f"Straight Line Distance: {metrics['straight_line_distance']:.2f} m\n"
        text += f"Path Efficiency: {metrics['path_efficiency']:.2%}\n"
        text += f"\nAverage Curvature: {metrics['avg_curvature']:.6f} rad/m\n"
        text += f"Maximum Curvature: {metrics['max_curvature']:.6f} rad/m\n"
        text += f"Estimated Max G-Force: {metrics['max_g_force']:.2f} g\n"
        text += f"\nMinimum Altitude: {metrics['min_altitude']:.2f} m\n"
        text += f"Maximum Altitude: {metrics['max_altitude']:.2f} m\n"
        text += f"Altitude Range: {metrics['altitude_range']:.2f} m\n"
        text += f"\nNumber of Waypoints: {metrics['n_waypoints']}\n"
        
        self.metrics_display.setPlainText(text)
    
    def clear_all(self):
        """Clear all trajectories"""
        self.visualizer.clear_trajectories()
        self.current_trajectory = None
        self.metrics_display.setPlainText("Generate a trajectory to see metrics...")
    
    def save_trajectory(self):
        """Save trajectory to file"""
        if self.current_trajectory is None:
            QMessageBox.warning(self, "Warning", "No trajectory to save!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Trajectory", "", "NumPy Files (*.npy);;JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                if filename.endswith('.npy'):
                    np.save(filename, self.current_trajectory)
                elif filename.endswith('.json'):
                    data = {
                        'trajectory': self.current_trajectory.tolist(),
                        'parameters': self.params.to_dict()
                    }
                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=2)
                else:
                    np.save(filename + '.npy', self.current_trajectory)
                
                QMessageBox.information(self, "Success", f"Trajectory saved to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save trajectory:\n{str(e)}")
    
    def load_parameters(self):
        """Load parameters from file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Parameters", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                if 'parameters' in data:
                    self.params.from_dict(data['parameters'])
                else:
                    self.params.from_dict(data)
                
                # Update UI
                self.update_ui_from_parameters()
                
                QMessageBox.information(self, "Success", "Parameters loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load parameters:\n{str(e)}")
    
    def update_ui_from_parameters(self):
        """Update UI controls from parameters"""
        self.start_x.setValue(self.params.start_x)
        self.start_y.setValue(self.params.start_y)
        self.start_z.setValue(self.params.start_z)
        
        self.end_x.setValue(self.params.end_x)
        self.end_y.setValue(self.params.end_y)
        self.end_z.setValue(self.params.end_z)
        
        self.max_altitude.setValue(self.params.max_altitude)
        self.min_altitude.setValue(self.params.min_altitude)
        self.max_speed.setValue(self.params.max_speed)
        self.max_g_turn.setValue(self.params.max_g_turn)
        self.turn_radius.setValue(self.params.turn_radius)
        self.n_waypoints.setValue(self.params.n_waypoints)
        
        self.smoothness.setValue(self.params.smoothness)
        self.max_acceleration.setValue(self.params.max_acceleration)
        self.banking_angle.setValue(self.params.banking_angle)
        self.climb_rate.setValue(self.params.climb_rate)
        self.descent_rate.setValue(self.params.descent_rate)
        self.curvature_limit.setValue(self.params.curvature_limit)


def main():
    """Main function"""
    try:
        # Create application
        app = QApplication(sys.argv)
        
        # Set style
        app.setStyle('Fusion')
        
        print("Creating GUI window...")
        
        # Create and show GUI
        gui = TrajectoryGeneratorGUI()
        
        print("Showing window...")
        gui.show()
        gui.raise_()
        gui.activateWindow()
        
        print("GUI window created successfully!")
        print("Starting event loop...\n")
        
        # Start event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"\nFATAL ERROR in main():")
        print(f"  {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    main()

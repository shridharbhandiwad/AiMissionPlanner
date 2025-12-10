"""
Advanced visualization utilities for trajectory generation
"""

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings

# Filter warnings before NumPy import to suppress MINGW-W64 build warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Optional, Dict
import os


class TrajectoryVisualizer:
    """Advanced visualization for trajectories"""
    
    def __init__(self, figsize=(12, 8)):
        self.figsize = figsize
        
    def plot_single_trajectory_3d(self, trajectory: np.ndarray, 
                                   start: Optional[np.ndarray] = None,
                                   end: Optional[np.ndarray] = None,
                                   obstacles: Optional[List[Dict]] = None,
                                   title: str = "3D Trajectory",
                                   save_path: Optional[str] = None,
                                   show: bool = True):
        """
        Plot a single trajectory in 3D
        
        Args:
            trajectory: Waypoints [seq_len, 3]
            start: Start point [3]
            end: End point [3]
            obstacles: List of obstacles [{center, radius}, ...]
            title: Plot title
            save_path: Path to save figure
            show: Whether to display the plot
        """
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot trajectory
        ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
               'b-', linewidth=2, label='Trajectory', alpha=0.8)
        
        # Plot waypoints
        ax.scatter(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
                  c='blue', s=20, alpha=0.5)
        
        # Plot start and end
        if start is not None:
            ax.scatter(*start, c='green', s=200, marker='o',
                      edgecolors='black', linewidths=2, label='Start', zorder=10)
        else:
            ax.scatter(*trajectory[0], c='green', s=200, marker='o',
                      edgecolors='black', linewidths=2, label='Start', zorder=10)
        
        if end is not None:
            ax.scatter(*end, c='red', s=200, marker='s',
                      edgecolors='black', linewidths=2, label='End', zorder=10)
        else:
            ax.scatter(*trajectory[-1], c='red', s=200, marker='s',
                      edgecolors='black', linewidths=2, label='End', zorder=10)
        
        # Plot obstacles
        if obstacles:
            for obs in obstacles:
                self._draw_sphere(ax, obs['center'], obs['radius'], alpha=0.3, color='red')
        
        ax.set_xlabel('X (m)', fontsize=12)
        ax.set_ylabel('Y (m)', fontsize=12)
        ax.set_zlabel('Z (m)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"✓ Saved to {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def plot_multiple_trajectories(self, trajectories: np.ndarray,
                                   start: np.ndarray,
                                   end: np.ndarray,
                                   ground_truth: Optional[np.ndarray] = None,
                                   title: str = "Multiple Trajectory Candidates",
                                   save_path: Optional[str] = None,
                                   show: bool = True):
        """
        Plot multiple trajectory candidates
        
        Args:
            trajectories: Multiple trajectories [n_samples, seq_len, 3]
            start: Start point [3]
            end: End point [3]
            ground_truth: Ground truth trajectory [seq_len, 3]
            title: Plot title
            save_path: Path to save
            show: Whether to display
        """
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot generated trajectories
        n_samples = len(trajectories)
        colors = plt.cm.rainbow(np.linspace(0, 1, n_samples))
        
        for i, (traj, color) in enumerate(zip(trajectories, colors)):
            ax.plot(traj[:, 0], traj[:, 1], traj[:, 2],
                   color=color, linewidth=2, alpha=0.6, label=f'Gen {i+1}')
        
        # Plot ground truth if provided
        if ground_truth is not None:
            ax.plot(ground_truth[:, 0], ground_truth[:, 1], ground_truth[:, 2],
                   'k--', linewidth=3, alpha=0.8, label='Ground Truth')
        
        # Plot start and end
        ax.scatter(*start, c='green', s=200, marker='o',
                  edgecolors='black', linewidths=3, label='Start', zorder=10)
        ax.scatter(*end, c='red', s=200, marker='s',
                  edgecolors='black', linewidths=3, label='End', zorder=10)
        
        ax.set_xlabel('X (m)', fontsize=12)
        ax.set_ylabel('Y (m)', fontsize=12)
        ax.set_zlabel('Z (m)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"✓ Saved to {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def plot_trajectory_metrics(self, trajectories: np.ndarray,
                               metrics: List[Dict],
                               save_path: Optional[str] = None,
                               show: bool = True):
        """
        Plot metrics comparison for multiple trajectories
        
        Args:
            trajectories: Multiple trajectories [n_samples, seq_len, 3]
            metrics: List of metric dictionaries
            save_path: Path to save
            show: Whether to display
        """
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Trajectory Metrics Comparison', fontsize=16, fontweight='bold')
        
        metric_keys = ['path_length', 'path_efficiency', 'avg_curvature', 
                      'smoothness_score', 'avg_altitude', 'avg_velocity']
        
        for idx, (ax, key) in enumerate(zip(axes.flat, metric_keys)):
            values = [m[key] for m in metrics]
            
            ax.bar(range(len(values)), values, color='steelblue', alpha=0.7)
            ax.set_xlabel('Trajectory ID', fontsize=10)
            ax.set_ylabel(key.replace('_', ' ').title(), fontsize=10)
            ax.set_title(key.replace('_', ' ').title(), fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Add value labels
            for i, v in enumerate(values):
                ax.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"✓ Saved to {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def plot_interactive_3d(self, trajectories: np.ndarray,
                           start: np.ndarray,
                           end: np.ndarray,
                           obstacles: Optional[List[Dict]] = None,
                           save_path: Optional[str] = None):
        """
        Create interactive 3D plot using Plotly
        
        Args:
            trajectories: Multiple trajectories [n_samples, seq_len, 3]
            start: Start point [3]
            end: End point [3]
            obstacles: List of obstacles
            save_path: Path to save HTML file
        """
        fig = go.Figure()
        
        # Add trajectories
        n_samples = len(trajectories) if trajectories.ndim == 3 else 1
        
        if trajectories.ndim == 2:
            trajectories = trajectories[np.newaxis, ...]
        
        colors = px.colors.qualitative.Plotly
        
        for i, traj in enumerate(trajectories):
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatter3d(
                x=traj[:, 0],
                y=traj[:, 1],
                z=traj[:, 2],
                mode='lines+markers',
                name=f'Trajectory {i+1}',
                line=dict(color=color, width=4),
                marker=dict(size=2)
            ))
        
        # Add start point
        fig.add_trace(go.Scatter3d(
            x=[start[0]],
            y=[start[1]],
            z=[start[2]],
            mode='markers',
            name='Start',
            marker=dict(size=15, color='green', symbol='circle')
        ))
        
        # Add end point
        fig.add_trace(go.Scatter3d(
            x=[end[0]],
            y=[end[1]],
            z=[end[2]],
            mode='markers',
            name='End',
            marker=dict(size=15, color='red', symbol='square')
        ))
        
        # Add obstacles
        if obstacles:
            for i, obs in enumerate(obstacles):
                # Create sphere mesh
                u = np.linspace(0, 2 * np.pi, 20)
                v = np.linspace(0, np.pi, 20)
                x = obs['radius'] * np.outer(np.cos(u), np.sin(v)) + obs['center'][0]
                y = obs['radius'] * np.outer(np.sin(u), np.sin(v)) + obs['center'][1]
                z = obs['radius'] * np.outer(np.ones(np.size(u)), np.cos(v)) + obs['center'][2]
                
                fig.add_trace(go.Surface(
                    x=x, y=y, z=z,
                    showscale=False,
                    opacity=0.3,
                    colorscale=[[0, 'red'], [1, 'red']],
                    name=f'Obstacle {i+1}'
                ))
        
        fig.update_layout(
            title='3D Trajectory Visualization',
            scene=dict(
                xaxis_title='X (m)',
                yaxis_title='Y (m)',
                zaxis_title='Z (m)',
                aspectmode='data'
            ),
            width=1000,
            height=800
        )
        
        if save_path:
            fig.write_html(save_path)
            print(f"✓ Interactive plot saved to {save_path}")
        else:
            fig.show()
    
    def create_animation(self, trajectory: np.ndarray,
                        start: np.ndarray,
                        end: np.ndarray,
                        save_path: str,
                        fps: int = 10):
        """
        Create animated visualization of trajectory
        
        Args:
            trajectory: Trajectory waypoints [seq_len, 3]
            start: Start point
            end: End point
            save_path: Path to save animation (GIF or MP4)
            fps: Frames per second
        """
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Set up plot limits
        all_points = np.vstack([trajectory, start[np.newaxis, :], end[np.newaxis, :]])
        margin = 0.1 * (all_points.max(axis=0) - all_points.min(axis=0))
        
        ax.set_xlim(all_points[:, 0].min() - margin[0], all_points[:, 0].max() + margin[0])
        ax.set_ylim(all_points[:, 1].min() - margin[1], all_points[:, 1].max() + margin[1])
        ax.set_zlim(all_points[:, 2].min() - margin[2], all_points[:, 2].max() + margin[2])
        
        # Plot start and end
        ax.scatter(*start, c='green', s=200, marker='o', label='Start')
        ax.scatter(*end, c='red', s=200, marker='s', label='End')
        
        # Initialize line
        line, = ax.plot([], [], [], 'b-', linewidth=2, label='Trajectory')
        point, = ax.plot([], [], [], 'bo', markersize=10)
        
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Trajectory Animation')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        def update(frame):
            # Update trajectory up to current frame
            line.set_data(trajectory[:frame, 0], trajectory[:frame, 1])
            line.set_3d_properties(trajectory[:frame, 2])
            
            # Update current position
            if frame > 0:
                point.set_data([trajectory[frame-1, 0]], [trajectory[frame-1, 1]])
                point.set_3d_properties([trajectory[frame-1, 2]])
            
            return line, point
        
        anim = FuncAnimation(fig, update, frames=len(trajectory)+1, 
                           interval=1000/fps, blit=True)
        
        # Save animation
        if save_path.endswith('.gif'):
            anim.save(save_path, writer='pillow', fps=fps)
        elif save_path.endswith('.mp4'):
            anim.save(save_path, writer='ffmpeg', fps=fps)
        else:
            anim.save(save_path + '.gif', writer='pillow', fps=fps)
        
        print(f"✓ Animation saved to {save_path}")
        plt.close()
    
    def _draw_sphere(self, ax, center, radius, alpha=0.3, color='red'):
        """Draw a sphere (obstacle) on 3D axis"""
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        
        x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
        y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
        
        ax.plot_surface(x, y, z, color=color, alpha=alpha)


def demo_visualization():
    """Demo visualization capabilities"""
    print("Trajectory Visualization Demo")
    print("="*60)
    
    # Create dummy data
    np.random.seed(42)
    
    start = np.array([0.0, 0.0, 100.0])
    end = np.array([800.0, 600.0, 200.0])
    
    # Generate dummy trajectory
    t = np.linspace(0, 1, 50)
    trajectory = np.column_stack([
        start[0] + (end[0] - start[0]) * t + 100 * np.sin(2*np.pi*t*2),
        start[1] + (end[1] - start[1]) * t + 100 * np.cos(2*np.pi*t*2),
        start[2] + (end[2] - start[2]) * t + 50 * np.sin(2*np.pi*t)
    ])
    
    # Generate multiple trajectories
    trajectories = []
    for i in range(5):
        traj = np.column_stack([
            start[0] + (end[0] - start[0]) * t + 100 * np.sin(2*np.pi*t*2 + i),
            start[1] + (end[1] - start[1]) * t + 100 * np.cos(2*np.pi*t*2 + i),
            start[2] + (end[2] - start[2]) * t + 50 * np.sin(2*np.pi*t + i*0.5)
        ])
        trajectories.append(traj)
    trajectories = np.array(trajectories)
    
    # Create obstacles
    obstacles = [
        {'center': np.array([400.0, 300.0, 150.0]), 'radius': 80.0},
        {'center': np.array([600.0, 400.0, 180.0]), 'radius': 60.0}
    ]
    
    # Create visualizer
    viz = TrajectoryVisualizer()
    
    # Create output directory
    os.makedirs('visualizations', exist_ok=True)
    
    # 1. Single trajectory
    print("\n1. Plotting single trajectory...")
    viz.plot_single_trajectory_3d(
        trajectory, start, end, obstacles,
        title="Single Trajectory with Obstacles",
        save_path='visualizations/single_trajectory.png',
        show=False
    )
    
    # 2. Multiple trajectories
    print("2. Plotting multiple trajectories...")
    viz.plot_multiple_trajectories(
        trajectories, start, end,
        title="Multiple Trajectory Candidates",
        save_path='visualizations/multiple_trajectories.png',
        show=False
    )
    
    # 3. Interactive plot
    print("3. Creating interactive 3D plot...")
    viz.plot_interactive_3d(
        trajectories, start, end, obstacles,
        save_path='visualizations/interactive_plot.html'
    )
    
    print("\n" + "="*60)
    print("✓ Visualization demo complete!")
    print("Check the 'visualizations/' directory for outputs")
    print("="*60)


if __name__ == '__main__':
    demo_visualization()

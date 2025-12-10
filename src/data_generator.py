"""
Trajectory Dataset Generation
Generates synthetic trajectories using various path planning algorithms
"""

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings

# Filter warnings before NumPy import to suppress MINGW-W64 build warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

import numpy as np
from typing import List, Tuple, Dict, Optional
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, BSpline, splrep, splev
from scipy.spatial.distance import euclidean
import pickle
from tqdm import tqdm
import json


class TrajectoryGenerator:
    """Generates diverse trajectories using multiple algorithms"""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        self.bounds = {
            'x': (-1000, 1000),
            'y': (-1000, 1000),
            'z': (50, 500)
        }
        
    def generate_random_waypoint(self) -> np.ndarray:
        """Generate random 3D waypoint within bounds"""
        x = np.random.uniform(*self.bounds['x'])
        y = np.random.uniform(*self.bounds['y'])
        z = np.random.uniform(*self.bounds['z'])
        return np.array([x, y, z])
    
    def generate_bezier_trajectory(self, start: np.ndarray, end: np.ndarray, 
                                   n_control_points: int = 3, n_samples: int = 50) -> np.ndarray:
        """
        Generate trajectory using Bézier curves
        
        Args:
            start: Starting waypoint [x, y, z]
            end: Ending waypoint [x, y, z]
            n_control_points: Number of intermediate control points
            n_samples: Number of waypoints in output trajectory
            
        Returns:
            trajectory: Array of shape (n_samples, 3)
        """
        # Generate random control points between start and end
        control_points = [start]
        
        for i in range(n_control_points):
            # Interpolate with random deviation
            alpha = (i + 1) / (n_control_points + 1)
            base_point = start * (1 - alpha) + end * alpha
            
            # Add random perturbation
            perturbation = np.random.randn(3) * 100
            perturbation[2] *= 0.5  # Less variation in z
            control_point = base_point + perturbation
            
            # Clamp to bounds
            control_point = np.clip(control_point, 
                                   [self.bounds['x'][0], self.bounds['y'][0], self.bounds['z'][0]],
                                   [self.bounds['x'][1], self.bounds['y'][1], self.bounds['z'][1]])
            control_points.append(control_point)
        
        control_points.append(end)
        control_points = np.array(control_points)
        
        # Evaluate Bézier curve
        t = np.linspace(0, 1, n_samples)
        trajectory = self._bezier_curve(control_points, t)
        
        return trajectory
    
    def _bezier_curve(self, control_points: np.ndarray, t: np.ndarray) -> np.ndarray:
        """Evaluate Bézier curve using De Casteljau's algorithm"""
        n = len(control_points) - 1
        trajectory = np.zeros((len(t), 3))
        
        for i, t_val in enumerate(t):
            # Bernstein polynomials
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
    
    def generate_spline_trajectory(self, start: np.ndarray, end: np.ndarray,
                                   n_waypoints: int = 5, n_samples: int = 50) -> np.ndarray:
        """
        Generate trajectory using cubic spline interpolation
        
        Args:
            start: Starting waypoint
            end: Ending waypoint
            n_waypoints: Number of intermediate waypoints
            n_samples: Number of points in output trajectory
            
        Returns:
            trajectory: Array of shape (n_samples, 3)
        """
        # Generate intermediate waypoints
        waypoints = [start]
        
        for i in range(n_waypoints):
            alpha = (i + 1) / (n_waypoints + 1)
            base_point = start * (1 - alpha) + end * alpha
            
            # Add controlled randomness
            noise = np.random.randn(3) * 50
            noise[2] *= 0.3
            waypoint = base_point + noise
            
            # Clamp to bounds
            waypoint = np.clip(waypoint,
                              [self.bounds['x'][0], self.bounds['y'][0], self.bounds['z'][0]],
                              [self.bounds['x'][1], self.bounds['y'][1], self.bounds['z'][1]])
            waypoints.append(waypoint)
        
        waypoints.append(end)
        waypoints = np.array(waypoints)
        
        # Create cubic spline
        t_waypoints = np.linspace(0, 1, len(waypoints))
        t_dense = np.linspace(0, 1, n_samples)
        
        cs_x = CubicSpline(t_waypoints, waypoints[:, 0])
        cs_y = CubicSpline(t_waypoints, waypoints[:, 1])
        cs_z = CubicSpline(t_waypoints, waypoints[:, 2])
        
        trajectory = np.column_stack([
            cs_x(t_dense),
            cs_y(t_dense),
            cs_z(t_dense)
        ])
        
        return trajectory
    
    def generate_dubins_like_trajectory(self, start: np.ndarray, end: np.ndarray,
                                        turn_radius: float = 100.0, n_samples: int = 50) -> np.ndarray:
        """
        Generate Dubins-like path (simplified for 3D)
        
        Args:
            start: Starting waypoint
            end: Ending waypoint
            turn_radius: Minimum turn radius
            n_samples: Number of samples
            
        Returns:
            trajectory: Array of shape (n_samples, 3)
        """
        # Simplified Dubins: straight line with smooth turns at ends
        direction = end - start
        distance = np.linalg.norm(direction)
        
        if distance < 2 * turn_radius:
            # Too close for proper Dubins, use direct spline
            return self.generate_spline_trajectory(start, end, n_waypoints=2, n_samples=n_samples)
        
        # Create path with turn-straight-turn pattern
        unit_dir = direction / distance
        
        # First turn waypoint
        turn1_center = start + unit_dir * turn_radius
        
        # Second turn waypoint
        turn2_center = end - unit_dir * turn_radius
        
        # Generate smooth path through these points
        waypoints = np.array([start, turn1_center, turn2_center, end])
        t_waypoints = np.linspace(0, 1, len(waypoints))
        t_dense = np.linspace(0, 1, n_samples)
        
        cs_x = CubicSpline(t_waypoints, waypoints[:, 0])
        cs_y = CubicSpline(t_waypoints, waypoints[:, 1])
        cs_z = CubicSpline(t_waypoints, waypoints[:, 2])
        
        trajectory = np.column_stack([
            cs_x(t_dense),
            cs_y(t_dense),
            cs_z(t_dense)
        ])
        
        return trajectory
    
    def generate_rrt_like_trajectory(self, start: np.ndarray, end: np.ndarray,
                                     obstacles: List[Dict], n_samples: int = 50) -> np.ndarray:
        """
        Generate RRT-like trajectory with obstacle avoidance
        
        Args:
            start: Starting waypoint
            end: Ending waypoint
            obstacles: List of obstacles [{center: [x,y,z], radius: r}, ...]
            n_samples: Number of samples
            
        Returns:
            trajectory: Array of shape (n_samples, 3)
        """
        # Simplified RRT: sample random points and connect collision-free
        max_iterations = 100
        step_size = 50.0
        
        tree = [start]
        
        for _ in range(max_iterations):
            # Sample random point (bias towards goal)
            if np.random.rand() < 0.2:
                random_point = end
            else:
                random_point = self.generate_random_waypoint()
            
            # Find nearest point in tree
            nearest = min(tree, key=lambda p: np.linalg.norm(p - random_point))
            
            # Step towards random point
            direction = random_point - nearest
            distance = np.linalg.norm(direction)
            
            if distance > step_size:
                new_point = nearest + (direction / distance) * step_size
            else:
                new_point = random_point
            
            # Check collision
            if not self._check_collision_segment(nearest, new_point, obstacles):
                tree.append(new_point)
                
                # Check if we reached goal
                if np.linalg.norm(new_point - end) < step_size:
                    tree.append(end)
                    break
        
        # If didn't reach goal, force connection
        if np.linalg.norm(tree[-1] - end) > step_size:
            tree.append(end)
        
        # Smooth the path using spline
        tree = np.array(tree)
        if len(tree) < 4:
            # Too few points, add intermediate
            tree = np.array([start, (start + end) / 2, end])
        
        t_waypoints = np.linspace(0, 1, len(tree))
        t_dense = np.linspace(0, 1, n_samples)
        
        cs_x = CubicSpline(t_waypoints, tree[:, 0], bc_type='clamped')
        cs_y = CubicSpline(t_waypoints, tree[:, 1], bc_type='clamped')
        cs_z = CubicSpline(t_waypoints, tree[:, 2], bc_type='clamped')
        
        trajectory = np.column_stack([
            cs_x(t_dense),
            cs_y(t_dense),
            cs_z(t_dense)
        ])
        
        return trajectory
    
    def _check_collision_segment(self, p1: np.ndarray, p2: np.ndarray,
                                 obstacles: List[Dict]) -> bool:
        """Check if line segment collides with obstacles"""
        n_checks = 10
        for alpha in np.linspace(0, 1, n_checks):
            point = p1 * (1 - alpha) + p2 * alpha
            for obs in obstacles:
                dist = np.linalg.norm(point - obs['center'])
                if dist < obs['radius']:
                    return True
        return False
    
    def generate_obstacles(self, n_obstacles: int, 
                          start: np.ndarray, end: np.ndarray) -> List[Dict]:
        """Generate random obstacles avoiding start/end regions"""
        obstacles = []
        safe_radius = 150.0  # Keep obstacles away from start/end
        
        for _ in range(n_obstacles):
            while True:
                center = self.generate_random_waypoint()
                
                # Check if too close to start or end
                if (np.linalg.norm(center - start) > safe_radius and 
                    np.linalg.norm(center - end) > safe_radius):
                    break
            
            radius = np.random.uniform(30, 80)
            obstacles.append({'center': center, 'radius': radius})
        
        return obstacles
    
    def compute_trajectory_metrics(self, trajectory: np.ndarray) -> Dict:
        """Compute metrics for a trajectory"""
        # Path length
        path_length = 0.0
        for i in range(len(trajectory) - 1):
            path_length += np.linalg.norm(trajectory[i+1] - trajectory[i])
        
        # Smoothness (average curvature)
        curvatures = []
        for i in range(1, len(trajectory) - 1):
            v1 = trajectory[i] - trajectory[i-1]
            v2 = trajectory[i+1] - trajectory[i]
            
            # Avoid division by zero
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            
            if norm1 > 1e-6 and norm2 > 1e-6:
                cos_angle = np.dot(v1, v2) / (norm1 * norm2)
                cos_angle = np.clip(cos_angle, -1, 1)
                angle = np.arccos(cos_angle)
                curvature = angle / norm1
                curvatures.append(curvature)
        
        avg_curvature = np.mean(curvatures) if curvatures else 0.0
        
        # Straight-line distance
        straight_line = np.linalg.norm(trajectory[-1] - trajectory[0])
        
        return {
            'path_length': path_length,
            'straight_line_distance': straight_line,
            'path_length_ratio': path_length / max(straight_line, 1.0),
            'avg_curvature': avg_curvature,
            'smoothness_score': 1.0 / (1.0 + avg_curvature),
            'altitude_range': (trajectory[:, 2].min(), trajectory[:, 2].max())
        }


class DatasetGenerator:
    """Generate complete dataset for training"""
    
    def __init__(self, n_samples: int = 50000, n_points: int = 50, seed: int = 42):
        self.n_samples = n_samples
        self.n_points = n_points
        self.generator = TrajectoryGenerator(seed=seed)
        
    def generate_dataset(self, output_path: str = 'data/trajectories.npz'):
        """
        Generate complete dataset
        
        Args:
            output_path: Path to save dataset
            
        Returns:
            dataset: Dictionary containing all data
        """
        print(f"Generating {self.n_samples} trajectories...")
        
        trajectories = []
        start_points = []
        end_points = []
        obstacles_list = []
        metrics_list = []
        method_types = []
        
        methods = [
            ('bezier', self.generator.generate_bezier_trajectory),
            ('spline', self.generator.generate_spline_trajectory),
            ('dubins', self.generator.generate_dubins_like_trajectory),
        ]
        
        for i in tqdm(range(self.n_samples)):
            # Generate random start and end
            start = self.generator.generate_random_waypoint()
            end = self.generator.generate_random_waypoint()
            
            # Ensure reasonable distance
            while np.linalg.norm(end - start) < 200:
                end = self.generator.generate_random_waypoint()
            
            # Generate obstacles (vary density)
            n_obstacles = np.random.randint(0, 15)
            obstacles = self.generator.generate_obstacles(n_obstacles, start, end)
            
            # Choose random method
            method_name, method_func = methods[i % len(methods)]
            
            # Generate trajectory with appropriate parameters
            if method_name == 'rrt':
                trajectory = self.generator.generate_rrt_like_trajectory(
                    start, end, obstacles, n_samples=self.n_points
                )
            else:
                trajectory = method_func(start, end, n_samples=self.n_points)
            
            # Compute metrics
            metrics = self.generator.compute_trajectory_metrics(trajectory)
            
            # Store
            trajectories.append(trajectory)
            start_points.append(start)
            end_points.append(end)
            obstacles_list.append(obstacles)
            metrics_list.append(metrics)
            method_types.append(method_name)
        
        # Convert to arrays
        trajectories = np.array(trajectories, dtype=np.float32)
        start_points = np.array(start_points, dtype=np.float32)
        end_points = np.array(end_points, dtype=np.float32)
        
        # Create dataset dictionary
        dataset = {
            'trajectories': trajectories,
            'start_points': start_points,
            'end_points': end_points,
            'n_samples': self.n_samples,
            'n_points': self.n_points,
            'method_types': method_types
        }
        
        # Save dataset
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        np.savez_compressed(output_path, **dataset)
        
        # Save metadata
        metadata = {
            'n_samples': self.n_samples,
            'n_points': self.n_points,
            'trajectory_shape': trajectories.shape,
            'methods_used': list(set(method_types)),
            'avg_metrics': {
                'path_length': np.mean([m['path_length'] for m in metrics_list]),
                'avg_curvature': np.mean([m['avg_curvature'] for m in metrics_list]),
                'smoothness_score': np.mean([m['smoothness_score'] for m in metrics_list])
            }
        }
        
        metadata_path = output_path.replace('.npz', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\nDataset saved to {output_path}")
        print(f"Metadata saved to {metadata_path}")
        print(f"Shape: {trajectories.shape}")
        
        # Save obstacles separately (can be large)
        obstacles_path = output_path.replace('.npz', '_obstacles.pkl')
        with open(obstacles_path, 'wb') as f:
            pickle.dump(obstacles_list, f)
        
        return dataset, metrics_list
    
    def visualize_samples(self, dataset: Dict, n_samples: int = 9, 
                         save_path: str = 'data/sample_trajectories.png'):
        """Visualize random trajectory samples"""
        trajectories = dataset['trajectories']
        start_points = dataset['start_points']
        end_points = dataset['end_points']
        
        fig = plt.figure(figsize=(15, 10))
        
        indices = np.random.choice(len(trajectories), n_samples, replace=False)
        
        for idx, i in enumerate(indices):
            ax = fig.add_subplot(3, 3, idx + 1, projection='3d')
            
            traj = trajectories[i]
            start = start_points[i]
            end = end_points[i]
            
            # Plot trajectory
            ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'b-', linewidth=2, alpha=0.7)
            
            # Plot start and end
            ax.scatter(*start, c='green', s=100, marker='o', label='Start')
            ax.scatter(*end, c='red', s=100, marker='s', label='End')
            
            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
            ax.set_zlabel('Z (m)')
            ax.set_title(f'Trajectory {i}')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved to {save_path}")
        plt.close()


def main():
    """Main function to generate dataset"""
    # Generate dataset
    generator = DatasetGenerator(n_samples=50000, n_points=50, seed=42)
    dataset, metrics = generator.generate_dataset('data/trajectories.npz')
    
    # Visualize samples
    generator.visualize_samples(dataset, n_samples=9, 
                               save_path='data/sample_trajectories.png')
    
    # Print statistics
    print("\n" + "="*60)
    print("Dataset Statistics")
    print("="*60)
    print(f"Total trajectories: {len(dataset['trajectories'])}")
    print(f"Trajectory shape: {dataset['trajectories'].shape}")
    print(f"Start points shape: {dataset['start_points'].shape}")
    print(f"End points shape: {dataset['end_points'].shape}")
    
    print("\nTrajectory Metrics:")
    avg_path_length = np.mean([m['path_length'] for m in metrics])
    avg_curvature = np.mean([m['avg_curvature'] for m in metrics])
    avg_smoothness = np.mean([m['smoothness_score'] for m in metrics])
    
    print(f"  Average path length: {avg_path_length:.2f} m")
    print(f"  Average curvature: {avg_curvature:.6f} rad/m")
    print(f"  Average smoothness score: {avg_smoothness:.4f}")
    print("="*60)


if __name__ == '__main__':
    main()

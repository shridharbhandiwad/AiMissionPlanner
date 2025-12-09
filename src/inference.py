"""
Inference utilities for trajectory generation
"""

import torch
import numpy as np
from typing import List, Tuple, Optional, Dict
import json

from model import create_model


class TrajectoryPredictor:
    """Wrapper for easy inference"""
    
    def __init__(self, checkpoint_path: str, device: str = 'cpu'):
        """
        Initialize predictor
        
        Args:
            checkpoint_path: Path to trained model checkpoint
            device: Device to run on ('cpu' or 'cuda')
        """
        self.device = torch.device(device)
        
        # Load checkpoint
        print(f"Loading model from {checkpoint_path}...")
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        
        # Extract model args
        model_args = checkpoint['args']
        
        # Create model
        self.model = create_model(
            latent_dim=model_args.get('latent_dim', 64),
            hidden_dim=model_args.get('hidden_dim', 256),
            num_layers=model_args.get('num_layers', 2),
            max_seq_len=50
        )
        
        # Load weights
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Load normalization parameters
        self.mean = torch.FloatTensor(checkpoint['normalization']['mean']).to(self.device)
        self.std = torch.FloatTensor(checkpoint['normalization']['std']).to(self.device)
        
        print(f"✓ Model loaded successfully")
        print(f"  Training loss: {checkpoint['train_loss']:.4f}")
        print(f"  Validation loss: {checkpoint['val_loss']:.4f}")
        print(f"  Epoch: {checkpoint['epoch']}")
    
    def normalize(self, data: torch.Tensor) -> torch.Tensor:
        """Normalize input data"""
        return (data - self.mean) / self.std
    
    def denormalize(self, data: torch.Tensor) -> torch.Tensor:
        """Denormalize output data"""
        return data * self.std + self.mean
    
    def predict_single(self, start: np.ndarray, end: np.ndarray,
                      n_samples: int = 1, seq_len: int = 50) -> np.ndarray:
        """
        Generate trajectories for a single start-end pair
        
        Args:
            start: Start waypoint [x, y, z]
            end: End waypoint [x, y, z]
            n_samples: Number of diverse trajectories to generate
            seq_len: Length of trajectory
            
        Returns:
            trajectories: Generated trajectories [n_samples, seq_len, 3]
        """
        # Convert to tensors
        start_tensor = torch.FloatTensor(start).unsqueeze(0).to(self.device)
        end_tensor = torch.FloatTensor(end).unsqueeze(0).to(self.device)
        
        # Normalize
        start_norm = self.normalize(start_tensor)
        end_norm = self.normalize(end_tensor)
        
        # Generate
        with torch.no_grad():
            trajectories_norm = self.model.generate(start_norm, end_norm, n_samples, seq_len)
            
            # Denormalize
            trajectories = self.denormalize(trajectories_norm)
        
        return trajectories.cpu().numpy()
    
    def predict_batch(self, starts: np.ndarray, ends: np.ndarray,
                     n_samples: int = 1, seq_len: int = 50) -> np.ndarray:
        """
        Generate trajectories for multiple start-end pairs
        
        Args:
            starts: Start waypoints [batch_size, 3]
            ends: End waypoints [batch_size, 3]
            n_samples: Number of diverse trajectories per pair
            seq_len: Length of trajectory
            
        Returns:
            trajectories: Generated trajectories [batch_size * n_samples, seq_len, 3]
        """
        # Convert to tensors
        starts_tensor = torch.FloatTensor(starts).to(self.device)
        ends_tensor = torch.FloatTensor(ends).to(self.device)
        
        # Normalize
        starts_norm = self.normalize(starts_tensor)
        ends_norm = self.normalize(ends_tensor)
        
        # Generate
        with torch.no_grad():
            trajectories_norm = self.model.generate(starts_norm, ends_norm, n_samples, seq_len)
            
            # Denormalize
            trajectories = self.denormalize(trajectories_norm)
        
        return trajectories.cpu().numpy()
    
    def predict_with_obstacles(self, start: np.ndarray, end: np.ndarray,
                               obstacles: List[Dict], n_candidates: int = 10,
                               seq_len: int = 50) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate multiple trajectories and rank by obstacle avoidance
        
        Args:
            start: Start waypoint [x, y, z]
            end: End waypoint [x, y, z]
            obstacles: List of obstacles [{center: [x,y,z], radius: r}, ...]
            n_candidates: Number of trajectories to generate
            seq_len: Length of trajectory
            
        Returns:
            trajectories: Ranked trajectories [n_candidates, seq_len, 3]
            scores: Safety scores for each trajectory
        """
        # Generate candidates
        trajectories = self.predict_single(start, end, n_candidates, seq_len)
        
        # Compute safety scores
        scores = []
        for traj in trajectories:
            score = self._compute_safety_score(traj, obstacles)
            scores.append(score)
        
        scores = np.array(scores)
        
        # Sort by score (higher is better)
        sorted_indices = np.argsort(scores)[::-1]
        trajectories = trajectories[sorted_indices]
        scores = scores[sorted_indices]
        
        return trajectories, scores
    
    def _compute_safety_score(self, trajectory: np.ndarray, 
                             obstacles: List[Dict]) -> float:
        """
        Compute safety score for trajectory
        
        Args:
            trajectory: Trajectory waypoints [seq_len, 3]
            obstacles: List of obstacles
            
        Returns:
            score: Safety score (higher is better)
        """
        if len(obstacles) == 0:
            return 1.0
        
        min_distance = float('inf')
        collision_penalty = 0.0
        
        for point in trajectory:
            for obs in obstacles:
                center = np.array(obs['center'])
                radius = obs['radius']
                
                dist = np.linalg.norm(point - center) - radius
                min_distance = min(min_distance, dist)
                
                if dist < 0:
                    collision_penalty += abs(dist)
        
        # Safety score based on minimum clearance and collisions
        if collision_penalty > 0:
            score = -collision_penalty  # Negative for collisions
        else:
            score = min_distance  # Positive clearance
        
        return score


def evaluate_trajectory_quality(trajectory: np.ndarray) -> Dict:
    """
    Evaluate trajectory quality metrics
    
    Args:
        trajectory: Trajectory waypoints [seq_len, 3]
        
    Returns:
        metrics: Dictionary of quality metrics
    """
    # Path length
    path_length = 0.0
    for i in range(len(trajectory) - 1):
        path_length += np.linalg.norm(trajectory[i+1] - trajectory[i])
    
    # Straight-line distance
    straight_line = np.linalg.norm(trajectory[-1] - trajectory[0])
    
    # Smoothness (curvature)
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
    
    # Velocity profile
    velocities = []
    for i in range(len(trajectory) - 1):
        velocity = np.linalg.norm(trajectory[i+1] - trajectory[i])
        velocities.append(velocity)
    
    avg_velocity = np.mean(velocities) if velocities else 0.0
    
    # Altitude analysis
    altitudes = trajectory[:, 2]
    
    metrics = {
        'path_length': float(path_length),
        'straight_line_distance': float(straight_line),
        'path_efficiency': float(straight_line / path_length if path_length > 0 else 0),
        'avg_curvature': float(avg_curvature),
        'max_curvature': float(max_curvature),
        'smoothness_score': float(1.0 / (1.0 + avg_curvature)),
        'avg_velocity': float(avg_velocity),
        'min_altitude': float(altitudes.min()),
        'max_altitude': float(altitudes.max()),
        'avg_altitude': float(altitudes.mean())
    }
    
    return metrics


def compare_trajectories(trajectories: np.ndarray, ground_truth: Optional[np.ndarray] = None) -> Dict:
    """
    Compare multiple generated trajectories
    
    Args:
        trajectories: Generated trajectories [n_samples, seq_len, 3]
        ground_truth: Optional ground truth trajectory [seq_len, 3]
        
    Returns:
        comparison: Dictionary of comparison metrics
    """
    n_samples = len(trajectories)
    
    # Compute metrics for each trajectory
    all_metrics = [evaluate_trajectory_quality(traj) for traj in trajectories]
    
    # Aggregate statistics
    avg_metrics = {}
    for key in all_metrics[0].keys():
        values = [m[key] for m in all_metrics]
        avg_metrics[f'mean_{key}'] = float(np.mean(values))
        avg_metrics[f'std_{key}'] = float(np.std(values))
    
    # Diversity: average pairwise distance
    diversity_scores = []
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            dist = np.mean(np.linalg.norm(trajectories[i] - trajectories[j], axis=1))
            diversity_scores.append(dist)
    
    avg_diversity = float(np.mean(diversity_scores)) if diversity_scores else 0.0
    
    comparison = {
        'n_samples': n_samples,
        'diversity': avg_diversity,
        **avg_metrics
    }
    
    # Compare with ground truth if provided
    if ground_truth is not None:
        reconstruction_errors = []
        for traj in trajectories:
            # Compute MSE
            mse = np.mean((traj - ground_truth) ** 2)
            reconstruction_errors.append(mse)
        
        comparison['avg_reconstruction_error'] = float(np.mean(reconstruction_errors))
        comparison['min_reconstruction_error'] = float(np.min(reconstruction_errors))
    
    return comparison


def main():
    """Demo inference"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run trajectory inference')
    parser.add_argument('--checkpoint', type=str, default='models/best_model.pth',
                       help='Path to model checkpoint')
    parser.add_argument('--device', type=str, default='cpu',
                       choices=['cpu', 'cuda'], help='Device to run on')
    parser.add_argument('--n_samples', type=int, default=5,
                       help='Number of trajectories to generate')
    
    args = parser.parse_args()
    
    # Create predictor
    predictor = TrajectoryPredictor(args.checkpoint, device=args.device)
    
    # Example: Generate trajectories
    print("\n" + "="*60)
    print("Example: Generate trajectories from random start/end")
    print("="*60)
    
    start = np.array([0.0, 0.0, 100.0])
    end = np.array([800.0, 600.0, 200.0])
    
    print(f"Start: {start}")
    print(f"End: {end}")
    print(f"Generating {args.n_samples} trajectories...")
    
    trajectories = predictor.predict_single(start, end, n_samples=args.n_samples)
    
    print(f"\nGenerated trajectories shape: {trajectories.shape}")
    
    # Evaluate each trajectory
    print("\nTrajectory Metrics:")
    print("-" * 60)
    for i, traj in enumerate(trajectories):
        metrics = evaluate_trajectory_quality(traj)
        print(f"\nTrajectory {i+1}:")
        print(f"  Path length: {metrics['path_length']:.2f} m")
        print(f"  Efficiency: {metrics['path_efficiency']:.3f}")
        print(f"  Smoothness: {metrics['smoothness_score']:.4f}")
        print(f"  Avg curvature: {metrics['avg_curvature']:.6f} rad/m")
    
    # Compare trajectories
    comparison = compare_trajectories(trajectories)
    print("\n" + "="*60)
    print("Comparison Metrics:")
    print("="*60)
    print(f"Diversity: {comparison['diversity']:.2f} m")
    print(f"Mean path length: {comparison['mean_path_length']:.2f} ± {comparison['std_path_length']:.2f} m")
    print(f"Mean smoothness: {comparison['mean_smoothness_score']:.4f} ± {comparison['std_smoothness_score']:.4f}")
    
    print("\n✓ Inference demo completed!")


if __name__ == '__main__':
    main()

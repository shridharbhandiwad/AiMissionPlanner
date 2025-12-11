"""
Comprehensive evaluation of trained model
"""

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings

# Filter warnings before NumPy import to suppress MINGW-W64 build warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

import torch
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import json
from typing import Dict, List
from tqdm import tqdm

from .inference import TrajectoryPredictor, evaluate_trajectory_quality, compare_trajectories
from .train import TrajectoryDataset


class ModelEvaluator:
    """Comprehensive model evaluation"""
    
    def __init__(self, checkpoint_path: str, data_path: str, device: str = 'cpu'):
        """
        Initialize evaluator
        
        Args:
            checkpoint_path: Path to model checkpoint
            data_path: Path to test dataset
            device: Device to run on
        """
        self.predictor = TrajectoryPredictor(checkpoint_path, device)
        
        # Load test dataset
        print(f"Loading test dataset from {data_path}...")
        self.dataset = TrajectoryDataset(data_path, normalize=False)
        
        # We'll manually normalize using predictor's normalization
        
    def evaluate_reconstruction(self, n_samples: int = 100) -> Dict:
        """
        Evaluate reconstruction quality on test set
        
        Args:
            n_samples: Number of samples to evaluate
            
        Returns:
            metrics: Reconstruction metrics
        """
        print(f"Evaluating reconstruction on {n_samples} samples...")
        
        indices = np.random.choice(len(self.dataset), min(n_samples, len(self.dataset)), replace=False)
        
        mse_errors = []
        mae_errors = []
        endpoint_errors = []
        
        for idx in tqdm(indices):
            sample = self.dataset[idx]
            
            gt_trajectory = sample['trajectory'].numpy()
            start = sample['start'].numpy()
            end = sample['end'].numpy()
            
            # Generate trajectory
            pred_trajectory = self.predictor.predict_single(start, end, n_samples=1, seq_len=len(gt_trajectory))
            pred_trajectory = pred_trajectory[0]
            
            # Compute errors
            mse = np.mean((pred_trajectory - gt_trajectory) ** 2)
            mae = np.mean(np.abs(pred_trajectory - gt_trajectory))
            endpoint_error = np.linalg.norm(pred_trajectory[-1] - gt_trajectory[-1])
            
            mse_errors.append(mse)
            mae_errors.append(mae)
            endpoint_errors.append(endpoint_error)
        
        metrics = {
            'mse': {
                'mean': float(np.mean(mse_errors)),
                'std': float(np.std(mse_errors)),
                'median': float(np.median(mse_errors))
            },
            'mae': {
                'mean': float(np.mean(mae_errors)),
                'std': float(np.std(mae_errors)),
                'median': float(np.median(mae_errors))
            },
            'endpoint_error': {
                'mean': float(np.mean(endpoint_errors)),
                'std': float(np.std(endpoint_errors)),
                'median': float(np.median(endpoint_errors))
            }
        }
        
        return metrics
    
    def evaluate_diversity(self, n_pairs: int = 50, n_samples: int = 10) -> Dict:
        """
        Evaluate diversity of generated trajectories
        
        Args:
            n_pairs: Number of start-end pairs
            n_samples: Number of trajectories per pair
            
        Returns:
            metrics: Diversity metrics
        """
        print(f"Evaluating diversity: {n_pairs} pairs × {n_samples} samples...")
        
        indices = np.random.choice(len(self.dataset), min(n_pairs, len(self.dataset)), replace=False)
        
        diversity_scores = []
        
        for idx in tqdm(indices):
            sample = self.dataset[idx]
            
            start = sample['start'].numpy()
            end = sample['end'].numpy()
            
            # Generate multiple trajectories
            trajectories = self.predictor.predict_single(start, end, n_samples=n_samples)
            
            # Compute pairwise diversity
            pair_distances = []
            for i in range(n_samples):
                for j in range(i + 1, n_samples):
                    dist = np.mean(np.linalg.norm(trajectories[i] - trajectories[j], axis=1))
                    pair_distances.append(dist)
            
            avg_diversity = np.mean(pair_distances) if pair_distances else 0.0
            diversity_scores.append(avg_diversity)
        
        metrics = {
            'diversity': {
                'mean': float(np.mean(diversity_scores)),
                'std': float(np.std(diversity_scores)),
                'median': float(np.median(diversity_scores))
            }
        }
        
        return metrics
    
    def evaluate_quality(self, n_samples: int = 100) -> Dict:
        """
        Evaluate quality metrics of generated trajectories
        
        Args:
            n_samples: Number of trajectories to evaluate
            
        Returns:
            metrics: Quality metrics
        """
        print(f"Evaluating quality on {n_samples} trajectories...")
        
        indices = np.random.choice(len(self.dataset), min(n_samples, len(self.dataset)), replace=False)
        
        all_metrics = []
        
        for idx in tqdm(indices):
            sample = self.dataset[idx]
            
            start = sample['start'].numpy()
            end = sample['end'].numpy()
            
            # Generate trajectory
            trajectory = self.predictor.predict_single(start, end, n_samples=1)[0]
            
            # Compute quality metrics
            metrics = evaluate_trajectory_quality(trajectory)
            all_metrics.append(metrics)
        
        # Aggregate
        aggregated = {}
        for key in all_metrics[0].keys():
            values = [m[key] for m in all_metrics]
            aggregated[key] = {
                'mean': float(np.mean(values)),
                'std': float(np.std(values)),
                'median': float(np.median(values)),
                'min': float(np.min(values)),
                'max': float(np.max(values))
            }
        
        return aggregated
    
    def visualize_samples(self, n_samples: int = 9, save_path: str = 'results/evaluation_samples.png'):
        """
        Visualize random trajectory samples
        
        Args:
            n_samples: Number of samples to visualize
            save_path: Path to save figure
        """
        print(f"Visualizing {n_samples} samples...")
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        indices = np.random.choice(len(self.dataset), min(n_samples, len(self.dataset)), replace=False)
        
        fig = plt.figure(figsize=(15, 10))
        
        for plot_idx, idx in enumerate(indices):
            sample = self.dataset[idx]
            
            gt_trajectory = sample['trajectory'].numpy()
            start = sample['start'].numpy()
            end = sample['end'].numpy()
            
            # Generate predictions (3 diverse trajectories)
            pred_trajectories = self.predictor.predict_single(start, end, n_samples=3)
            
            ax = fig.add_subplot(3, 3, plot_idx + 1, projection='3d')
            
            # Plot ground truth
            ax.plot(gt_trajectory[:, 0], gt_trajectory[:, 1], gt_trajectory[:, 2],
                   'g-', linewidth=2, alpha=0.8, label='Ground Truth')
            
            # Plot predictions
            colors = ['b', 'r', 'orange']
            for i, pred_traj in enumerate(pred_trajectories):
                ax.plot(pred_traj[:, 0], pred_traj[:, 1], pred_traj[:, 2],
                       f'{colors[i]}--', linewidth=1.5, alpha=0.6, label=f'Pred {i+1}')
            
            # Plot start and end
            ax.scatter(*start, c='green', s=100, marker='o', edgecolors='black', linewidths=2)
            ax.scatter(*end, c='red', s=100, marker='s', edgecolors='black', linewidths=2)
            
            ax.set_xlabel('X (m)', fontsize=8)
            ax.set_ylabel('Y (m)', fontsize=8)
            ax.set_zlabel('Z (m)', fontsize=8)
            ax.set_title(f'Sample {idx}', fontsize=10)
            
            if plot_idx == 0:
                ax.legend(fontsize=6)
            
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Visualization saved to {save_path}")
        plt.close()
    
    def visualize_diversity(self, n_trajectories: int = 10, save_path: str = 'results/diversity.png'):
        """
        Visualize diversity of generated trajectories for a single start-end pair
        
        Args:
            n_trajectories: Number of trajectories to generate
            save_path: Path to save figure
        """
        print(f"Visualizing diversity with {n_trajectories} trajectories...")
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Pick a random sample
        idx = np.random.randint(len(self.dataset))
        sample = self.dataset[idx]
        
        start = sample['start'].numpy()
        end = sample['end'].numpy()
        
        # Generate multiple trajectories
        trajectories = self.predictor.predict_single(start, end, n_samples=n_trajectories)
        
        # Create figure
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot all trajectories
        colors = plt.cm.rainbow(np.linspace(0, 1, n_trajectories))
        
        for i, (traj, color) in enumerate(zip(trajectories, colors)):
            ax.plot(traj[:, 0], traj[:, 1], traj[:, 2],
                   color=color, linewidth=2, alpha=0.7, label=f'Traj {i+1}')
        
        # Plot start and end
        ax.scatter(*start, c='green', s=200, marker='o', edgecolors='black', 
                  linewidths=3, label='Start', zorder=10)
        ax.scatter(*end, c='red', s=200, marker='s', edgecolors='black',
                  linewidths=3, label='End', zorder=10)
        
        ax.set_xlabel('X (m)', fontsize=12)
        ax.set_ylabel('Y (m)', fontsize=12)
        ax.set_zlabel('Z (m)', fontsize=12)
        ax.set_title(f'Trajectory Diversity: {n_trajectories} Samples', fontsize=14, fontweight='bold')
        
        # Add legend
        ax.legend(loc='upper left', fontsize=8, ncol=2)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Diversity visualization saved to {save_path}")
        plt.close()
    
    def run_full_evaluation(self, output_dir: str = 'results'):
        """
        Run complete evaluation suite
        
        Args:
            output_dir: Directory to save results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n" + "="*60)
        print("Running Full Model Evaluation")
        print("="*60)
        
        results = {}
        
        # 1. Reconstruction
        print("\n1. Reconstruction Evaluation")
        print("-" * 60)
        recon_metrics = self.evaluate_reconstruction(n_samples=200)
        results['reconstruction'] = recon_metrics
        
        print(f"MSE: {recon_metrics['mse']['mean']:.4f} ± {recon_metrics['mse']['std']:.4f}")
        print(f"MAE: {recon_metrics['mae']['mean']:.4f} ± {recon_metrics['mae']['std']:.4f}")
        print(f"Endpoint Error: {recon_metrics['endpoint_error']['mean']:.2f} ± {recon_metrics['endpoint_error']['std']:.2f} m")
        
        # 2. Diversity
        print("\n2. Diversity Evaluation")
        print("-" * 60)
        diversity_metrics = self.evaluate_diversity(n_pairs=50, n_samples=10)
        results['diversity'] = diversity_metrics
        
        print(f"Avg Diversity: {diversity_metrics['diversity']['mean']:.2f} ± {diversity_metrics['diversity']['std']:.2f} m")
        
        # 3. Quality
        print("\n3. Quality Evaluation")
        print("-" * 60)
        quality_metrics = self.evaluate_quality(n_samples=200)
        results['quality'] = quality_metrics
        
        print(f"Path Efficiency: {quality_metrics['path_efficiency']['mean']:.3f} ± {quality_metrics['path_efficiency']['std']:.3f}")
        print(f"Smoothness: {quality_metrics['smoothness_score']['mean']:.4f} ± {quality_metrics['smoothness_score']['std']:.4f}")
        print(f"Avg Curvature: {quality_metrics['avg_curvature']['mean']:.6f} ± {quality_metrics['avg_curvature']['std']:.6f}")
        
        # 4. Visualizations
        print("\n4. Generating Visualizations")
        print("-" * 60)
        self.visualize_samples(n_samples=9, save_path=f'{output_dir}/evaluation_samples.png')
        self.visualize_diversity(n_trajectories=10, save_path=f'{output_dir}/diversity.png')
        
        # Save results
        results_path = f'{output_dir}/evaluation_results.json'
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Results saved to {results_path}")
        
        print("\n" + "="*60)
        print("Evaluation Complete!")
        print("="*60)
        
        return results


def main():
    """Main evaluation script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Evaluate trajectory generation model')
    parser.add_argument('--checkpoint', type=str, default='models/best_model.pth',
                       help='Path to model checkpoint')
    parser.add_argument('--data', type=str, default='data/trajectories.npz',
                       help='Path to test dataset')
    parser.add_argument('--output', type=str, default='results',
                       help='Output directory for results')
    parser.add_argument('--device', type=str, default='cpu',
                       choices=['cpu', 'cuda'], help='Device to run on')
    
    args = parser.parse_args()
    
    # Create evaluator
    evaluator = ModelEvaluator(args.checkpoint, args.data, device=args.device)
    
    # Run evaluation
    evaluator.run_full_evaluation(output_dir=args.output)


if __name__ == '__main__':
    main()

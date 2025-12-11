"""
Split trajectory data into training, testing, and evaluation sets
and export to CSV format
"""

import numpy as np
import pandas as pd
import os
from pathlib import Path

def load_trajectory_data(data_path='data/trajectories.npz'):
    """Load the trajectory dataset"""
    print(f"Loading data from {data_path}...")
    data = np.load(data_path)
    
    trajectories = data['trajectories']
    start_points = data['start_points']
    end_points = data['end_points']
    method_types = data['method_types']
    
    print(f"Loaded {len(trajectories)} trajectories")
    print(f"Trajectory shape: {trajectories.shape}")
    print(f"  - {trajectories.shape[0]} samples")
    print(f"  - {trajectories.shape[1]} points per trajectory")
    print(f"  - {trajectories.shape[2]} dimensions (x, y, z)")
    
    return trajectories, start_points, end_points, method_types


def split_data(trajectories, start_points, end_points, method_types,
               train_ratio=0.7, test_ratio=0.15, eval_ratio=0.15, seed=42):
    """
    Split data into training, testing, and evaluation sets
    
    Args:
        train_ratio: Proportion for training (default 0.7 = 70%)
        test_ratio: Proportion for testing (default 0.15 = 15%)
        eval_ratio: Proportion for evaluation (default 0.15 = 15%)
        seed: Random seed for reproducibility
    """
    assert abs(train_ratio + test_ratio + eval_ratio - 1.0) < 1e-6, \
        "Ratios must sum to 1.0"
    
    n_samples = len(trajectories)
    np.random.seed(seed)
    
    # Create shuffled indices
    indices = np.arange(n_samples)
    np.random.shuffle(indices)
    
    # Calculate split points
    train_end = int(n_samples * train_ratio)
    test_end = train_end + int(n_samples * test_ratio)
    
    # Split indices
    train_idx = indices[:train_end]
    test_idx = indices[train_end:test_end]
    eval_idx = indices[test_end:]
    
    print(f"\nData split:")
    print(f"  Training:   {len(train_idx):6d} samples ({len(train_idx)/n_samples*100:.1f}%)")
    print(f"  Testing:    {len(test_idx):6d} samples ({len(test_idx)/n_samples*100:.1f}%)")
    print(f"  Evaluation: {len(eval_idx):6d} samples ({len(eval_idx)/n_samples*100:.1f}%)")
    
    # Split data
    data_splits = {
        'train': {
            'trajectories': trajectories[train_idx],
            'start_points': start_points[train_idx],
            'end_points': end_points[train_idx],
            'method_types': method_types[train_idx],
            'indices': train_idx
        },
        'test': {
            'trajectories': trajectories[test_idx],
            'start_points': start_points[test_idx],
            'end_points': end_points[test_idx],
            'method_types': method_types[test_idx],
            'indices': test_idx
        },
        'eval': {
            'trajectories': trajectories[eval_idx],
            'start_points': start_points[eval_idx],
            'end_points': end_points[eval_idx],
            'method_types': method_types[eval_idx],
            'indices': eval_idx
        }
    }
    
    return data_splits


def trajectories_to_csv(split_data, split_name, output_dir='data/csv'):
    """
    Convert trajectory data to CSV format
    
    Each trajectory is flattened into a single row with columns:
    - sample_id: Unique identifier
    - start_x, start_y, start_z: Starting point coordinates
    - end_x, end_y, end_z: Ending point coordinates
    - method_type: Generation method (bezier/spline/dubins)
    - point_0_x, point_0_y, point_0_z, ..., point_N_x, point_N_y, point_N_z: Trajectory points
    """
    print(f"\nConverting {split_name} data to CSV...")
    
    trajectories = split_data['trajectories']
    start_points = split_data['start_points']
    end_points = split_data['end_points']
    method_types = split_data['method_types']
    indices = split_data['indices']
    
    n_samples, n_points, n_dims = trajectories.shape
    
    # Create DataFrame with metadata columns
    data_dict = {
        'sample_id': indices,
        'start_x': start_points[:, 0],
        'start_y': start_points[:, 1],
        'start_z': start_points[:, 2],
        'end_x': end_points[:, 0],
        'end_y': end_points[:, 1],
        'end_z': end_points[:, 2],
        'method_type': method_types
    }
    
    # Add trajectory points as columns
    for i in range(n_points):
        data_dict[f'point_{i}_x'] = trajectories[:, i, 0]
        data_dict[f'point_{i}_y'] = trajectories[:, i, 1]
        data_dict[f'point_{i}_z'] = trajectories[:, i, 2]
    
    df = pd.DataFrame(data_dict)
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{split_name}_trajectories.csv')
    df.to_csv(output_path, index=False)
    
    print(f"  Saved to: {output_path}")
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"  File size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
    
    return df


def create_summary_csv(splits, output_dir='data/csv'):
    """
    Create a summary CSV with basic statistics for each trajectory
    """
    print("\nCreating summary statistics CSV...")
    
    summary_data = []
    
    for split_name, split_data in splits.items():
        trajectories = split_data['trajectories']
        start_points = split_data['start_points']
        end_points = split_data['end_points']
        method_types = split_data['method_types']
        indices = split_data['indices']
        
        for idx, traj, start, end, method in zip(indices, trajectories, 
                                                   start_points, end_points, 
                                                   method_types):
            # Calculate trajectory metrics
            path_length = np.sum(np.linalg.norm(np.diff(traj, axis=0), axis=1))
            straight_line_dist = np.linalg.norm(end - start)
            path_length_ratio = path_length / max(straight_line_dist, 1e-6)
            
            # Altitude statistics
            altitude_min = traj[:, 2].min()
            altitude_max = traj[:, 2].max()
            altitude_mean = traj[:, 2].mean()
            
            # Curvature (simplified)
            curvatures = []
            for i in range(1, len(traj) - 1):
                v1 = traj[i] - traj[i-1]
                v2 = traj[i+1] - traj[i]
                norm1 = np.linalg.norm(v1)
                norm2 = np.linalg.norm(v2)
                if norm1 > 1e-6 and norm2 > 1e-6:
                    cos_angle = np.dot(v1, v2) / (norm1 * norm2)
                    cos_angle = np.clip(cos_angle, -1, 1)
                    angle = np.arccos(cos_angle)
                    curvature = angle / norm1
                    curvatures.append(curvature)
            
            avg_curvature = np.mean(curvatures) if curvatures else 0.0
            smoothness = 1.0 / (1.0 + avg_curvature)
            
            summary_data.append({
                'sample_id': idx,
                'split': split_name,
                'method_type': method,
                'start_x': start[0],
                'start_y': start[1],
                'start_z': start[2],
                'end_x': end[0],
                'end_y': end[1],
                'end_z': end[2],
                'path_length': path_length,
                'straight_line_distance': straight_line_dist,
                'path_length_ratio': path_length_ratio,
                'altitude_min': altitude_min,
                'altitude_max': altitude_max,
                'altitude_mean': altitude_mean,
                'avg_curvature': avg_curvature,
                'smoothness_score': smoothness
            })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Save summary
    output_path = os.path.join(output_dir, 'trajectories_summary.csv')
    summary_df.to_csv(output_path, index=False)
    
    print(f"  Saved to: {output_path}")
    print(f"  Shape: {summary_df.shape[0]} rows × {summary_df.shape[1]} columns")
    print(f"  File size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
    
    return summary_df


def print_statistics(summary_df):
    """Print statistics for each split"""
    print("\n" + "="*70)
    print("DATASET STATISTICS BY SPLIT")
    print("="*70)
    
    for split_name in ['train', 'test', 'eval']:
        split_df = summary_df[summary_df['split'] == split_name]
        
        print(f"\n{split_name.upper()} SET:")
        print(f"  Samples: {len(split_df)}")
        print(f"  Method distribution:")
        for method, count in split_df['method_type'].value_counts().items():
            print(f"    {method}: {count} ({count/len(split_df)*100:.1f}%)")
        
        print(f"\n  Path statistics:")
        print(f"    Length:      mean={split_df['path_length'].mean():.2f} m, "
              f"std={split_df['path_length'].std():.2f} m")
        print(f"    Curvature:   mean={split_df['avg_curvature'].mean():.6f} rad/m, "
              f"std={split_df['avg_curvature'].std():.6f} rad/m")
        print(f"    Smoothness:  mean={split_df['smoothness_score'].mean():.4f}, "
              f"std={split_df['smoothness_score'].std():.4f}")
        print(f"    Altitude:    mean={split_df['altitude_mean'].mean():.2f} m, "
              f"range=[{split_df['altitude_min'].min():.2f}, {split_df['altitude_max'].max():.2f}] m")
    
    print("\n" + "="*70)


def main():
    """Main function"""
    print("="*70)
    print("TRAJECTORY DATA SPLITTING AND CSV EXPORT")
    print("="*70)
    
    # Load data
    trajectories, start_points, end_points, method_types = load_trajectory_data(
        'data/trajectories.npz'
    )
    
    # Split data (70% train, 15% test, 15% eval)
    splits = split_data(
        trajectories, start_points, end_points, method_types,
        train_ratio=0.7,
        test_ratio=0.15,
        eval_ratio=0.15,
        seed=42
    )
    
    # Convert each split to CSV
    output_dir = 'data/csv'
    for split_name, data in splits.items():
        trajectories_to_csv(data, split_name, output_dir)
    
    # Create summary CSV
    summary_df = create_summary_csv(splits, output_dir)
    
    # Print statistics
    print_statistics(summary_df)
    
    print("\n" + "="*70)
    print("CSV EXPORT COMPLETE")
    print("="*70)
    print(f"\nOutput directory: {output_dir}/")
    print("Files created:")
    print("  - train_trajectories.csv     (70% of data)")
    print("  - test_trajectories.csv      (15% of data)")
    print("  - eval_trajectories.csv      (15% of data)")
    print("  - trajectories_summary.csv   (statistics for all samples)")
    print("\nEach trajectory CSV contains:")
    print("  - Metadata: sample_id, start/end points, method_type")
    print("  - Full trajectory: 50 points × 3 coordinates (x, y, z)")
    print("\nSummary CSV contains computed metrics for all trajectories")
    print("="*70)


if __name__ == '__main__':
    main()

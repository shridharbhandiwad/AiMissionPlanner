"""
Example script demonstrating how to load and use the CSV trajectory data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def load_trajectory_from_csv(csv_path, sample_index=0):
    """
    Load a specific trajectory from CSV file
    
    Args:
        csv_path: Path to CSV file (train/test/eval)
        sample_index: Index of the trajectory to load (row number)
    
    Returns:
        trajectory: numpy array of shape (50, 3) with x, y, z coordinates
        metadata: dictionary with start, end, method_type, sample_id
    """
    df = pd.read_csv(csv_path)
    row = df.iloc[sample_index]
    
    # Extract trajectory points
    trajectory = np.zeros((50, 3))
    for i in range(50):
        trajectory[i, 0] = row[f'point_{i}_x']
        trajectory[i, 1] = row[f'point_{i}_y']
        trajectory[i, 2] = row[f'point_{i}_z']
    
    # Extract metadata
    metadata = {
        'sample_id': row['sample_id'],
        'start': np.array([row['start_x'], row['start_y'], row['start_z']]),
        'end': np.array([row['end_x'], row['end_y'], row['end_z']]),
        'method_type': row['method_type']
    }
    
    return trajectory, metadata


def load_all_trajectories(csv_path):
    """
    Load all trajectories from CSV file
    
    Args:
        csv_path: Path to CSV file
    
    Returns:
        trajectories: numpy array of shape (N, 50, 3)
        starts: numpy array of shape (N, 3)
        ends: numpy array of shape (N, 3)
        methods: list of method types
        sample_ids: list of sample IDs
    """
    df = pd.read_csv(csv_path)
    n_samples = len(df)
    
    trajectories = np.zeros((n_samples, 50, 3))
    starts = np.zeros((n_samples, 3))
    ends = np.zeros((n_samples, 3))
    
    # Extract trajectory points
    for i in range(50):
        trajectories[:, i, 0] = df[f'point_{i}_x']
        trajectories[:, i, 1] = df[f'point_{i}_y']
        trajectories[:, i, 2] = df[f'point_{i}_z']
    
    # Extract metadata
    starts[:, 0] = df['start_x']
    starts[:, 1] = df['start_y']
    starts[:, 2] = df['start_z']
    ends[:, 0] = df['end_x']
    ends[:, 1] = df['end_y']
    ends[:, 2] = df['end_z']
    
    methods = df['method_type'].tolist()
    sample_ids = df['sample_id'].tolist()
    
    return trajectories, starts, ends, methods, sample_ids


def visualize_trajectory(trajectory, metadata, save_path=None):
    """
    Visualize a single trajectory in 3D
    
    Args:
        trajectory: numpy array of shape (50, 3)
        metadata: dictionary with start, end, method_type, sample_id
        save_path: optional path to save figure
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot trajectory
    ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 
            'b-', linewidth=2, alpha=0.7, label='Trajectory')
    
    # Plot start and end points
    start = metadata['start']
    end = metadata['end']
    ax.scatter(*start, c='green', s=150, marker='o', label='Start', edgecolors='black')
    ax.scatter(*end, c='red', s=150, marker='s', label='End', edgecolors='black')
    
    # Labels and title
    ax.set_xlabel('X (m)', fontsize=12)
    ax.set_ylabel('Y (m)', fontsize=12)
    ax.set_zlabel('Z (m)', fontsize=12)
    ax.set_title(f"Trajectory {metadata['sample_id']} ({metadata['method_type']})", 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved to {save_path}")
    else:
        plt.show()
    
    plt.close()


def analyze_summary_statistics(summary_path='data/csv/trajectories_summary.csv'):
    """
    Analyze and print summary statistics from the summary CSV
    """
    df = pd.read_csv(summary_path)
    
    print("="*70)
    print("TRAJECTORY DATASET SUMMARY STATISTICS")
    print("="*70)
    
    for split in ['train', 'test', 'eval']:
        split_df = df[df['split'] == split]
        
        print(f"\n{split.upper()} SET ({len(split_df)} samples):")
        print("-" * 70)
        
        print("\nMethod Distribution:")
        for method, count in split_df['method_type'].value_counts().items():
            print(f"  {method:8s}: {count:5d} ({count/len(split_df)*100:5.1f}%)")
        
        print("\nPath Metrics:")
        print(f"  Length (m):           mean={split_df['path_length'].mean():8.2f}  "
              f"std={split_df['path_length'].std():8.2f}")
        print(f"  Straight distance (m): mean={split_df['straight_line_distance'].mean():8.2f}  "
              f"std={split_df['straight_line_distance'].std():8.2f}")
        print(f"  Path ratio:           mean={split_df['path_length_ratio'].mean():8.4f}  "
              f"std={split_df['path_length_ratio'].std():8.4f}")
        
        print("\nGeometric Metrics:")
        print(f"  Curvature (rad/m):    mean={split_df['avg_curvature'].mean():8.6f}  "
              f"std={split_df['avg_curvature'].std():8.6f}")
        print(f"  Smoothness score:     mean={split_df['smoothness_score'].mean():8.4f}  "
              f"std={split_df['smoothness_score'].std():8.4f}")
        
        print("\nAltitude Statistics:")
        print(f"  Mean altitude (m):    mean={split_df['altitude_mean'].mean():8.2f}  "
              f"std={split_df['altitude_mean'].std():8.2f}")
        print(f"  Min altitude (m):     min={split_df['altitude_min'].min():8.2f}  "
              f"max={split_df['altitude_min'].max():8.2f}")
        print(f"  Max altitude (m):     min={split_df['altitude_max'].min():8.2f}  "
              f"max={split_df['altitude_max'].max():8.2f}")
    
    print("\n" + "="*70)


def compare_methods(summary_path='data/csv/trajectories_summary.csv', split='train'):
    """
    Compare trajectory characteristics by generation method
    """
    df = pd.read_csv(summary_path)
    split_df = df[df['split'] == split]
    
    print(f"\n{'='*70}")
    print(f"METHOD COMPARISON - {split.upper()} SET")
    print("="*70)
    
    metrics = ['path_length', 'avg_curvature', 'smoothness_score', 'path_length_ratio']
    
    for metric in metrics:
        print(f"\n{metric.replace('_', ' ').title()}:")
        print("-" * 70)
        for method in ['bezier', 'spline', 'dubins']:
            method_df = split_df[split_df['method_type'] == method]
            mean_val = method_df[metric].mean()
            std_val = method_df[metric].std()
            print(f"  {method:8s}: mean={mean_val:10.4f}  std={std_val:10.4f}")
    
    print("="*70)


def main():
    """Main demonstration function"""
    print("\n" + "="*70)
    print("TRAJECTORY CSV DATA LOADING EXAMPLES")
    print("="*70 + "\n")
    
    # Example 1: Load a single trajectory
    print("Example 1: Loading a single trajectory from training data")
    print("-" * 70)
    trajectory, metadata = load_trajectory_from_csv('data/csv/train_trajectories.csv', 
                                                     sample_index=0)
    print(f"Loaded trajectory {metadata['sample_id']}")
    print(f"  Method: {metadata['method_type']}")
    print(f"  Start point: {metadata['start']}")
    print(f"  End point: {metadata['end']}")
    print(f"  Shape: {trajectory.shape}")
    print(f"  First point: {trajectory[0]}")
    print(f"  Last point: {trajectory[-1]}")
    
    # Example 2: Load all trajectories from test set
    print("\n\nExample 2: Loading all trajectories from test data")
    print("-" * 70)
    trajectories, starts, ends, methods, sample_ids = load_all_trajectories(
        'data/csv/test_trajectories.csv'
    )
    print(f"Loaded {len(trajectories)} trajectories")
    print(f"  Trajectories shape: {trajectories.shape}")
    print(f"  Starts shape: {starts.shape}")
    print(f"  Ends shape: {ends.shape}")
    print(f"  Methods (first 5): {methods[:5]}")
    
    # Example 3: Visualize a trajectory
    print("\n\nExample 3: Visualizing a trajectory")
    print("-" * 70)
    trajectory, metadata = load_trajectory_from_csv('data/csv/eval_trajectories.csv', 
                                                     sample_index=0)
    visualize_trajectory(trajectory, metadata, 
                        save_path='data/csv/example_trajectory.png')
    
    # Example 4: Analyze summary statistics
    print("\n\nExample 4: Summary statistics")
    print("-" * 70)
    analyze_summary_statistics()
    
    # Example 5: Compare methods
    print("\n\nExample 5: Method comparison")
    print("-" * 70)
    compare_methods(split='train')
    
    print("\n" + "="*70)
    print("Examples complete!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()

"""
Example scripts for using the 3D Trajectory Generator programmatically
Demonstrates various trajectory types and parameter configurations
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from trajectory_gui import Advanced3DTrajectoryGenerator, TrajectoryParameters


def example_1_basic_bezier():
    """Example 1: Generate a basic Bezier trajectory"""
    print("=" * 60)
    print("Example 1: Basic Bezier Trajectory")
    print("=" * 60)
    
    # Create generator
    generator = Advanced3DTrajectoryGenerator()
    
    # Set parameters
    params = TrajectoryParameters()
    params.start_x = 0
    params.start_y = 0
    params.start_z = 100
    params.end_x = 800
    params.end_y = 600
    params.end_z = 200
    params.trajectory_type = "bezier"
    params.n_waypoints = 50
    params.max_speed = 250.0
    params.max_g_turn = 4.0
    
    # Generate trajectory
    trajectory = generator.generate_trajectory(params)
    
    # Calculate metrics
    metrics = generator.calculate_metrics(trajectory, params)
    
    print(f"\nGenerated {len(trajectory)} waypoints")
    print(f"Path length: {metrics['path_length']:.2f} m")
    print(f"Path efficiency: {metrics['path_efficiency']:.2%}")
    print(f"Max G-force: {metrics['max_g_force']:.2f} g")
    print(f"Altitude range: {metrics['min_altitude']:.2f} - {metrics['max_altitude']:.2f} m")
    
    # Save trajectory
    np.save('trajectory_bezier.npy', trajectory)
    print("\nSaved to trajectory_bezier.npy")
    
    return trajectory, params


def example_2_combat_maneuver():
    """Example 2: Generate a combat maneuver trajectory"""
    print("\n" + "=" * 60)
    print("Example 2: Combat Maneuver (Immelmann Turn)")
    print("=" * 60)
    
    generator = Advanced3DTrajectoryGenerator()
    
    params = TrajectoryParameters()
    params.start_x = 0
    params.start_y = 0
    params.start_z = 150
    params.end_x = 500
    params.end_y = 0
    params.end_z = 400
    params.trajectory_type = "combat_maneuver"
    params.n_waypoints = 60
    params.max_speed = 300.0
    params.max_g_turn = 6.0
    params.turn_radius = 150.0
    
    trajectory = generator.generate_trajectory(params)
    metrics = generator.calculate_metrics(trajectory, params)
    
    print(f"\nGenerated {len(trajectory)} waypoints")
    print(f"Path length: {metrics['path_length']:.2f} m")
    print(f"Max G-force: {metrics['max_g_force']:.2f} g")
    print(f"Max altitude: {metrics['max_altitude']:.2f} m")
    
    np.save('trajectory_combat.npy', trajectory)
    print("\nSaved to trajectory_combat.npy")
    
    return trajectory, params


def example_3_spiral_descent():
    """Example 3: Generate a descending spiral trajectory"""
    print("\n" + "=" * 60)
    print("Example 3: Descending Spiral")
    print("=" * 60)
    
    generator = Advanced3DTrajectoryGenerator()
    
    params = TrajectoryParameters()
    params.start_x = 0
    params.start_y = 0
    params.start_z = 500
    params.end_x = 200
    params.end_y = 200
    params.end_z = 100
    params.trajectory_type = "descending_spiral"
    params.n_waypoints = 80
    params.max_speed = 150.0
    params.descent_rate = 8.0
    params.turn_radius = 100.0
    
    trajectory = generator.generate_trajectory(params)
    metrics = generator.calculate_metrics(trajectory, params)
    
    print(f"\nGenerated {len(trajectory)} waypoints")
    print(f"Path length: {metrics['path_length']:.2f} m")
    print(f"Altitude lost: {metrics['altitude_range']:.2f} m")
    print(f"Average curvature: {metrics['avg_curvature']:.6f} rad/m")
    
    np.save('trajectory_spiral_descent.npy', trajectory)
    print("\nSaved to trajectory_spiral_descent.npy")
    
    return trajectory, params


def example_4_terrain_following():
    """Example 4: Generate a terrain-following trajectory"""
    print("\n" + "=" * 60)
    print("Example 4: Terrain Following")
    print("=" * 60)
    
    generator = Advanced3DTrajectoryGenerator()
    
    params = TrajectoryParameters()
    params.start_x = 0
    params.start_y = 0
    params.start_z = 80
    params.end_x = 1000
    params.end_y = 500
    params.end_z = 90
    params.trajectory_type = "terrain_following"
    params.n_waypoints = 100
    params.max_altitude = 200.0
    params.min_altitude = 50.0
    params.max_speed = 200.0
    
    trajectory = generator.generate_trajectory(params)
    metrics = generator.calculate_metrics(trajectory, params)
    
    print(f"\nGenerated {len(trajectory)} waypoints")
    print(f"Path length: {metrics['path_length']:.2f} m")
    print(f"Altitude variation: {metrics['altitude_range']:.2f} m")
    print(f"Min altitude: {metrics['min_altitude']:.2f} m")
    print(f"Max altitude: {metrics['max_altitude']:.2f} m")
    
    np.save('trajectory_terrain.npy', trajectory)
    print("\nSaved to trajectory_terrain.npy")
    
    return trajectory, params


def example_5_s_curve_evasion():
    """Example 5: Generate an S-curve evasive trajectory"""
    print("\n" + "=" * 60)
    print("Example 5: S-Curve Evasive Maneuver")
    print("=" * 60)
    
    generator = Advanced3DTrajectoryGenerator()
    
    params = TrajectoryParameters()
    params.start_x = 0
    params.start_y = 0
    params.start_z = 200
    params.end_x = 600
    params.end_y = 400
    params.end_z = 250
    params.trajectory_type = "s_curve"
    params.n_waypoints = 60
    params.max_speed = 280.0
    params.turn_radius = 120.0
    params.smoothness = 0.9
    
    trajectory = generator.generate_trajectory(params)
    metrics = generator.calculate_metrics(trajectory, params)
    
    print(f"\nGenerated {len(trajectory)} waypoints")
    print(f"Path length: {metrics['path_length']:.2f} m")
    print(f"Path efficiency: {metrics['path_efficiency']:.2%}")
    print(f"Max curvature: {metrics['max_curvature']:.6f} rad/m")
    
    np.save('trajectory_s_curve.npy', trajectory)
    print("\nSaved to trajectory_s_curve.npy")
    
    return trajectory, params


def example_6_multiple_trajectories():
    """Example 6: Generate multiple trajectory types for comparison"""
    print("\n" + "=" * 60)
    print("Example 6: Multiple Trajectory Comparison")
    print("=" * 60)
    
    generator = Advanced3DTrajectoryGenerator()
    
    # Common parameters
    base_params = TrajectoryParameters()
    base_params.start_x = 0
    base_params.start_y = 0
    base_params.start_z = 100
    base_params.end_x = 600
    base_params.end_y = 400
    base_params.end_z = 150
    base_params.n_waypoints = 50
    
    trajectory_types = ["bezier", "circular", "s_curve", "helix", "parabolic"]
    trajectories = []
    
    for traj_type in trajectory_types:
        params = TrajectoryParameters()
        params.__dict__.update(base_params.__dict__)
        params.trajectory_type = traj_type
        
        trajectory = generator.generate_trajectory(params)
        metrics = generator.calculate_metrics(trajectory, params)
        
        trajectories.append((traj_type, trajectory, metrics))
        
        print(f"\n{traj_type.upper()}:")
        print(f"  Path length: {metrics['path_length']:.2f} m")
        print(f"  Efficiency: {metrics['path_efficiency']:.2%}")
        print(f"  Max G-force: {metrics['max_g_force']:.2f} g")
    
    # Save all trajectories
    for traj_type, trajectory, _ in trajectories:
        np.save(f'trajectory_{traj_type}.npy', trajectory)
    
    print("\n\nAll trajectories saved!")
    
    return trajectories


def visualize_trajectories_matplotlib(trajectories_data):
    """Visualize multiple trajectories using Matplotlib"""
    print("\n" + "=" * 60)
    print("Generating Matplotlib Visualization")
    print("=" * 60)
    
    fig = plt.figure(figsize=(15, 10))
    
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'cyan']
    
    # 3D plot
    ax1 = fig.add_subplot(121, projection='3d')
    
    for idx, (traj_type, trajectory, metrics) in enumerate(trajectories_data):
        color = colors[idx % len(colors)]
        
        # Plot trajectory
        ax1.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
                label=f"{traj_type} ({metrics['path_length']:.0f}m)",
                color=color, linewidth=2, alpha=0.7)
        
        # Plot start and end points
        ax1.scatter(trajectory[0, 0], trajectory[0, 1], trajectory[0, 2],
                   c='green', s=100, marker='o')
        ax1.scatter(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2],
                   c='red', s=100, marker='s')
    
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.set_title('3D Trajectory Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2D XY projection
    ax2 = fig.add_subplot(122)
    
    for idx, (traj_type, trajectory, metrics) in enumerate(trajectories_data):
        color = colors[idx % len(colors)]
        
        ax2.plot(trajectory[:, 0], trajectory[:, 1],
                label=f"{traj_type}",
                color=color, linewidth=2, alpha=0.7)
        
        ax2.scatter(trajectory[0, 0], trajectory[0, 1],
                   c='green', s=100, marker='o')
        ax2.scatter(trajectory[-1, 0], trajectory[-1, 1],
                   c='red', s=100, marker='s')
    
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_title('XY Projection')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.axis('equal')
    
    plt.tight_layout()
    plt.savefig('trajectory_comparison.png', dpi=150, bbox_inches='tight')
    print("\nVisualization saved to trajectory_comparison.png")
    plt.show()


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("3D Trajectory Generator - Programmatic Examples")
    print("=" * 60)
    
    # Run examples
    traj1, params1 = example_1_basic_bezier()
    traj2, params2 = example_2_combat_maneuver()
    traj3, params3 = example_3_spiral_descent()
    traj4, params4 = example_4_terrain_following()
    traj5, params5 = example_5_s_curve_evasion()
    
    # Generate multiple trajectories for comparison
    trajectories_data = example_6_multiple_trajectories()
    
    # Visualize
    print("\n" + "=" * 60)
    print("Creating visualization...")
    print("=" * 60)
    
    try:
        visualize_trajectories_matplotlib(trajectories_data)
    except Exception as e:
        print(f"Visualization error: {e}")
        print("Trajectories have been saved as .npy files")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - trajectory_bezier.npy")
    print("  - trajectory_combat.npy")
    print("  - trajectory_spiral_descent.npy")
    print("  - trajectory_terrain.npy")
    print("  - trajectory_s_curve.npy")
    print("  - trajectory_circular.npy")
    print("  - trajectory_helix.npy")
    print("  - trajectory_parabolic.npy")
    print("  - trajectory_comparison.png")
    print("\nTo load a trajectory:")
    print("  trajectory = np.load('trajectory_bezier.npy')")
    print("\nTo run the interactive GUI:")
    print("  python run_trajectory_gui.py")
    print("=" * 60)


if __name__ == '__main__':
    main()

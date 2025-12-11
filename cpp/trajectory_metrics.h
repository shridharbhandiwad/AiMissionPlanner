/**
 * @file trajectory_metrics.h
 * @brief Quality metrics for trajectory evaluation
 * @author Mission Planner Team
 * 
 * This file provides comprehensive quality metrics for evaluating
 * generated trajectories. All algorithms are documented with formulas
 * for easy understanding and porting.
 */

#ifndef TRAJECTORY_METRICS_H
#define TRAJECTORY_METRICS_H

#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>

namespace trajectory {

// Forward declare Waypoint and Trajectory from trajectory_inference.h
struct Waypoint;
using Trajectory = std::vector<Waypoint>;

/**
 * @brief Complete set of trajectory quality metrics
 */
struct TrajectoryMetrics {
    float path_length;           // Total path length (m)
    float straight_line_distance; // Direct distance start→end (m)
    float path_efficiency;       // straight_line / path_length [0,1]
    float avg_curvature;         // Average curvature (rad/m)
    float max_curvature;         // Maximum curvature (rad/m)
    float smoothness_score;      // Smoothness: 1/(1+avg_curvature) [0,1]
    float endpoint_error;        // Distance from actual end to expected end (m)
    float min_altitude;          // Minimum altitude (m)
    float max_altitude;          // Maximum altitude (m)
    float avg_altitude;          // Average altitude (m)
    float avg_velocity;          // Average velocity between waypoints (m)
    
    TrajectoryMetrics() 
        : path_length(0.0f), straight_line_distance(0.0f), 
          path_efficiency(0.0f), avg_curvature(0.0f), 
          max_curvature(0.0f), smoothness_score(0.0f),
          endpoint_error(0.0f), min_altitude(0.0f), 
          max_altitude(0.0f), avg_altitude(0.0f),
          avg_velocity(0.0f) {}
};

/**
 * @brief Compute total path length
 * 
 * Formula: L = Σ ||p[i+1] - p[i]|| for i = 0 to n-2
 * 
 * @param trajectory Input trajectory
 * @return Total path length in meters
 */
float computePathLength(const Trajectory& trajectory);

/**
 * @brief Compute straight-line distance from start to end
 * 
 * Formula: d = ||end - start||
 * 
 * @param trajectory Input trajectory
 * @return Straight-line distance in meters
 */
float computeStraightLineDistance(const Trajectory& trajectory);

/**
 * @brief Compute path efficiency (ratio of straight-line to path length)
 * 
 * Formula: η = straight_line_distance / path_length
 * Range: (0, 1] where 1.0 = perfect straight line
 * 
 * @param trajectory Input trajectory
 * @return Path efficiency
 */
float computePathEfficiency(const Trajectory& trajectory);

/**
 * @brief Compute curvature at each point
 * 
 * Formula:
 *   v1 = p[i] - p[i-1]
 *   v2 = p[i+1] - p[i]
 *   cos(θ) = (v1 · v2) / (||v1|| ||v2||)
 *   θ = arccos(cos(θ))
 *   κ = θ / ||v1||
 * 
 * @param trajectory Input trajectory
 * @return Vector of curvatures (rad/m) at each interior point
 */
std::vector<float> computeCurvatures(const Trajectory& trajectory);

/**
 * @brief Compute average curvature
 * 
 * Formula: κ_avg = (1/n) Σ κ[i]
 * Lower values indicate smoother paths
 * 
 * @param trajectory Input trajectory
 * @return Average curvature in rad/m
 */
float computeAverageCurvature(const Trajectory& trajectory);

/**
 * @brief Compute maximum curvature
 * 
 * @param trajectory Input trajectory
 * @return Maximum curvature in rad/m
 */
float computeMaxCurvature(const Trajectory& trajectory);

/**
 * @brief Compute smoothness score
 * 
 * Formula: S = 1 / (1 + κ_avg)
 * Range: (0, 1] where 1.0 = perfectly smooth
 * 
 * @param trajectory Input trajectory
 * @return Smoothness score
 */
float computeSmoothnessScore(const Trajectory& trajectory);

/**
 * @brief Compute endpoint error
 * 
 * Formula: E = ||trajectory.back() - expected_end||
 * 
 * @param trajectory Input trajectory
 * @param expected_end Expected end waypoint
 * @return Endpoint error in meters
 */
float computeEndpointError(const Trajectory& trajectory, 
                          const Waypoint& expected_end);

/**
 * @brief Compute average velocity between waypoints
 * 
 * Formula: v_avg = (1/n) Σ ||p[i+1] - p[i]||
 * 
 * @param trajectory Input trajectory
 * @return Average velocity in meters per step
 */
float computeAverageVelocity(const Trajectory& trajectory);

/**
 * @brief Compute second-order smoothness (acceleration penalty)
 * 
 * Formula: L_smooth = (1/n) Σ ||p[i+1] - 2*p[i] + p[i-1]||²
 * This is the same smoothness loss used in training
 * 
 * @param trajectory Input trajectory
 * @return Smoothness loss value
 */
float computeSecondOrderSmoothness(const Trajectory& trajectory);

/**
 * @brief Evaluate all quality metrics for a trajectory
 * 
 * Computes all available metrics in one pass for efficiency
 * 
 * @param trajectory Input trajectory
 * @param expected_end Expected end waypoint (for endpoint error)
 * @return Complete metrics structure
 */
TrajectoryMetrics evaluateTrajectory(const Trajectory& trajectory,
                                     const Waypoint& expected_end);

/**
 * @brief Print trajectory metrics in human-readable format
 * 
 * @param metrics Metrics to print
 */
void printMetrics(const TrajectoryMetrics& metrics);

/**
 * @brief Compare multiple trajectories and compute diversity
 * 
 * Diversity = average pairwise distance between trajectories
 * 
 * @param trajectories Vector of trajectories to compare
 * @return Average diversity score
 */
float computeDiversity(const std::vector<Trajectory>& trajectories);

/**
 * @brief Check if trajectory violates constraints
 * 
 * @param trajectory Input trajectory
 * @param max_curvature Maximum allowed curvature (rad/m)
 * @param min_altitude Minimum allowed altitude (m)
 * @param max_altitude Maximum allowed altitude (m)
 * @return True if trajectory is valid
 */
bool isTrajectoryValid(const Trajectory& trajectory,
                       float max_curvature = 0.1f,
                       float min_altitude = 50.0f,
                       float max_altitude = 1000.0f);

/**
 * @brief Rank trajectories by quality score
 * 
 * Quality score = w1*efficiency + w2*smoothness - w3*endpoint_error
 * 
 * @param trajectories Vector of trajectories
 * @param expected_end Expected end waypoint
 * @param w1 Weight for efficiency (default 0.3)
 * @param w2 Weight for smoothness (default 0.5)
 * @param w3 Weight for endpoint error (default 0.2)
 * @return Indices of trajectories sorted by quality (best first)
 */
std::vector<size_t> rankTrajectories(const std::vector<Trajectory>& trajectories,
                                     const Waypoint& expected_end,
                                     float w1 = 0.3f, float w2 = 0.5f, float w3 = 0.2f);

} // namespace trajectory

#endif // TRAJECTORY_METRICS_H

/**
 * @file trajectory_metrics.cpp
 * @brief Implementation of trajectory quality metrics
 */

#include "trajectory_metrics.h"
#include "trajectory_inference.h"
#include <iostream>
#include <iomanip>
#include <limits>

namespace trajectory {

float computePathLength(const Trajectory& trajectory) {
    if (trajectory.size() < 2) return 0.0f;
    
    float length = 0.0f;
    
    for (size_t i = 0; i < trajectory.size() - 1; ++i) {
        const Waypoint& p1 = trajectory[i];
        const Waypoint& p2 = trajectory[i + 1];
        
        float dx = p2.x - p1.x;
        float dy = p2.y - p1.y;
        float dz = p2.z - p1.z;
        
        length += std::sqrt(dx*dx + dy*dy + dz*dz);
    }
    
    return length;
}

float computeStraightLineDistance(const Trajectory& trajectory) {
    if (trajectory.size() < 2) return 0.0f;
    
    const Waypoint& start = trajectory.front();
    const Waypoint& end = trajectory.back();
    
    float dx = end.x - start.x;
    float dy = end.y - start.y;
    float dz = end.z - start.z;
    
    return std::sqrt(dx*dx + dy*dy + dz*dz);
}

float computePathEfficiency(const Trajectory& trajectory) {
    if (trajectory.size() < 2) return 1.0f;
    
    float straight_line = computeStraightLineDistance(trajectory);
    float path_length = computePathLength(trajectory);
    
    if (path_length < 1e-6f) return 0.0f;
    
    return straight_line / path_length;
}

std::vector<float> computeCurvatures(const Trajectory& trajectory) {
    std::vector<float> curvatures;
    
    if (trajectory.size() < 3) return curvatures;
    
    for (size_t i = 1; i < trajectory.size() - 1; ++i) {
        const Waypoint& p_prev = trajectory[i - 1];
        const Waypoint& p_curr = trajectory[i];
        const Waypoint& p_next = trajectory[i + 1];
        
        // v1 = current - previous
        float v1_x = p_curr.x - p_prev.x;
        float v1_y = p_curr.y - p_prev.y;
        float v1_z = p_curr.z - p_prev.z;
        float norm1 = std::sqrt(v1_x*v1_x + v1_y*v1_y + v1_z*v1_z);
        
        // v2 = next - current
        float v2_x = p_next.x - p_curr.x;
        float v2_y = p_next.y - p_curr.y;
        float v2_z = p_next.z - p_curr.z;
        float norm2 = std::sqrt(v2_x*v2_x + v2_y*v2_y + v2_z*v2_z);
        
        if (norm1 > 1e-6f && norm2 > 1e-6f) {
            // Dot product
            float dot = v1_x*v2_x + v1_y*v2_y + v1_z*v2_z;
            
            // Cosine of angle (clamp to avoid numerical issues)
            float cos_angle = dot / (norm1 * norm2);
            cos_angle = std::max(-1.0f, std::min(1.0f, cos_angle));
            
            // Angle in radians
            float angle = std::acos(cos_angle);
            
            // Curvature = angle / segment_length
            float curvature = angle / norm1;
            curvatures.push_back(curvature);
        }
    }
    
    return curvatures;
}

float computeAverageCurvature(const Trajectory& trajectory) {
    std::vector<float> curvatures = computeCurvatures(trajectory);
    
    if (curvatures.empty()) return 0.0f;
    
    float sum = std::accumulate(curvatures.begin(), curvatures.end(), 0.0f);
    return sum / curvatures.size();
}

float computeMaxCurvature(const Trajectory& trajectory) {
    std::vector<float> curvatures = computeCurvatures(trajectory);
    
    if (curvatures.empty()) return 0.0f;
    
    return *std::max_element(curvatures.begin(), curvatures.end());
}

float computeSmoothnessScore(const Trajectory& trajectory) {
    float avg_curvature = computeAverageCurvature(trajectory);
    return 1.0f / (1.0f + avg_curvature);
}

float computeEndpointError(const Trajectory& trajectory, 
                          const Waypoint& expected_end) {
    if (trajectory.empty()) return 0.0f;
    
    const Waypoint& actual_end = trajectory.back();
    
    float dx = actual_end.x - expected_end.x;
    float dy = actual_end.y - expected_end.y;
    float dz = actual_end.z - expected_end.z;
    
    return std::sqrt(dx*dx + dy*dy + dz*dz);
}

float computeAverageVelocity(const Trajectory& trajectory) {
    if (trajectory.size() < 2) return 0.0f;
    
    float total_velocity = 0.0f;
    
    for (size_t i = 0; i < trajectory.size() - 1; ++i) {
        const Waypoint& p1 = trajectory[i];
        const Waypoint& p2 = trajectory[i + 1];
        
        float dx = p2.x - p1.x;
        float dy = p2.y - p1.y;
        float dz = p2.z - p1.z;
        
        total_velocity += std::sqrt(dx*dx + dy*dy + dz*dz);
    }
    
    return total_velocity / (trajectory.size() - 1);
}

float computeSecondOrderSmoothness(const Trajectory& trajectory) {
    if (trajectory.size() < 3) return 0.0f;
    
    float smoothness_loss = 0.0f;
    
    for (size_t i = 1; i < trajectory.size() - 1; ++i) {
        const Waypoint& p_prev = trajectory[i - 1];
        const Waypoint& p_curr = trajectory[i];
        const Waypoint& p_next = trajectory[i + 1];
        
        // Second derivative: p[i+1] - 2*p[i] + p[i-1]
        float ax = p_next.x - 2.0f*p_curr.x + p_prev.x;
        float ay = p_next.y - 2.0f*p_curr.y + p_prev.y;
        float az = p_next.z - 2.0f*p_curr.z + p_prev.z;
        
        smoothness_loss += ax*ax + ay*ay + az*az;
    }
    
    return smoothness_loss / (trajectory.size() - 2);
}

TrajectoryMetrics evaluateTrajectory(const Trajectory& trajectory,
                                     const Waypoint& expected_end) {
    TrajectoryMetrics metrics;
    
    if (trajectory.empty()) return metrics;
    
    // Path metrics
    metrics.path_length = computePathLength(trajectory);
    metrics.straight_line_distance = computeStraightLineDistance(trajectory);
    metrics.path_efficiency = computePathEfficiency(trajectory);
    
    // Curvature metrics
    metrics.avg_curvature = computeAverageCurvature(trajectory);
    metrics.max_curvature = computeMaxCurvature(trajectory);
    metrics.smoothness_score = computeSmoothnessScore(trajectory);
    
    // Endpoint accuracy
    metrics.endpoint_error = computeEndpointError(trajectory, expected_end);
    
    // Velocity
    metrics.avg_velocity = computeAverageVelocity(trajectory);
    
    // Altitude statistics
    metrics.min_altitude = trajectory[0].z;
    metrics.max_altitude = trajectory[0].z;
    float sum_altitude = 0.0f;
    
    for (const auto& wp : trajectory) {
        metrics.min_altitude = std::min(metrics.min_altitude, wp.z);
        metrics.max_altitude = std::max(metrics.max_altitude, wp.z);
        sum_altitude += wp.z;
    }
    
    metrics.avg_altitude = sum_altitude / trajectory.size();
    
    return metrics;
}

void printMetrics(const TrajectoryMetrics& metrics) {
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Trajectory Quality Metrics:\n";
    std::cout << "  Path length:          " << metrics.path_length << " m\n";
    std::cout << "  Straight-line dist:   " << metrics.straight_line_distance << " m\n";
    std::cout << "  Path efficiency:      " << metrics.path_efficiency << "\n";
    std::cout << "  Avg curvature:        " << std::setprecision(6) 
              << metrics.avg_curvature << " rad/m\n";
    std::cout << "  Max curvature:        " << metrics.max_curvature << " rad/m\n";
    std::cout << "  Smoothness score:     " << std::setprecision(4) 
              << metrics.smoothness_score << "\n";
    std::cout << "  Endpoint error:       " << std::setprecision(2) 
              << metrics.endpoint_error << " m\n";
    std::cout << "  Altitude range:       [" << metrics.min_altitude 
              << ", " << metrics.max_altitude << "] m\n";
    std::cout << "  Avg altitude:         " << metrics.avg_altitude << " m\n";
    std::cout << "  Avg velocity:         " << metrics.avg_velocity << " m/step\n";
}

float computeDiversity(const std::vector<Trajectory>& trajectories) {
    if (trajectories.size() < 2) return 0.0f;
    
    float total_distance = 0.0f;
    int n_pairs = 0;
    
    for (size_t i = 0; i < trajectories.size(); ++i) {
        for (size_t j = i + 1; j < trajectories.size(); ++j) {
            const Trajectory& traj1 = trajectories[i];
            const Trajectory& traj2 = trajectories[j];
            
            // Compute average waypoint distance
            size_t min_len = std::min(traj1.size(), traj2.size());
            float distance = 0.0f;
            
            for (size_t k = 0; k < min_len; ++k) {
                float dx = traj1[k].x - traj2[k].x;
                float dy = traj1[k].y - traj2[k].y;
                float dz = traj1[k].z - traj2[k].z;
                distance += std::sqrt(dx*dx + dy*dy + dz*dz);
            }
            
            distance /= min_len;
            total_distance += distance;
            n_pairs++;
        }
    }
    
    return (n_pairs > 0) ? (total_distance / n_pairs) : 0.0f;
}

bool isTrajectoryValid(const Trajectory& trajectory,
                       float max_curvature,
                       float min_altitude,
                       float max_altitude) {
    if (trajectory.empty()) return false;
    
    // Check curvature constraint
    float traj_max_curvature = computeMaxCurvature(trajectory);
    if (traj_max_curvature > max_curvature) return false;
    
    // Check altitude constraints
    for (const auto& wp : trajectory) {
        if (wp.z < min_altitude || wp.z > max_altitude) {
            return false;
        }
    }
    
    return true;
}

std::vector<size_t> rankTrajectories(const std::vector<Trajectory>& trajectories,
                                     const Waypoint& expected_end,
                                     float w1, float w2, float w3) {
    std::vector<std::pair<float, size_t>> scores;
    
    for (size_t i = 0; i < trajectories.size(); ++i) {
        TrajectoryMetrics metrics = evaluateTrajectory(trajectories[i], expected_end);
        
        // Quality score = w1*efficiency + w2*smoothness - w3*endpoint_error
        // Normalize endpoint error by dividing by a typical scale (e.g., 100m)
        float score = w1 * metrics.path_efficiency 
                    + w2 * metrics.smoothness_score 
                    - w3 * (metrics.endpoint_error / 100.0f);
        
        scores.push_back({score, i});
    }
    
    // Sort by score (descending)
    std::sort(scores.begin(), scores.end(), 
              [](const auto& a, const auto& b) { return a.first > b.first; });
    
    std::vector<size_t> ranked_indices;
    for (const auto& pair : scores) {
        ranked_indices.push_back(pair.second);
    }
    
    return ranked_indices;
}

} // namespace trajectory

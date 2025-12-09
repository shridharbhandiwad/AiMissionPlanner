/**
 * @file trajectory_inference.h
 * @brief C++ inference for trajectory generation using ONNX Runtime
 * @author Mission Planner Team
 */

#ifndef TRAJECTORY_INFERENCE_H
#define TRAJECTORY_INFERENCE_H

#include <vector>
#include <string>
#include <memory>
#include <array>
#include <onnxruntime_cxx_api.h>

namespace trajectory {

/**
 * @brief 3D waypoint structure
 */
struct Waypoint {
    float x;
    float y;
    float z;
    
    Waypoint() : x(0.0f), y(0.0f), z(0.0f) {}
    Waypoint(float x_, float y_, float z_) : x(x_), y(y_), z(z_) {}
};

/**
 * @brief Trajectory represented as sequence of waypoints
 */
using Trajectory = std::vector<Waypoint>;

/**
 * @brief Normalization parameters for data preprocessing
 */
struct NormalizationParams {
    std::array<float, 3> mean;
    std::array<float, 3> std;
    
    NormalizationParams() 
        : mean({0.0f, 0.0f, 0.0f}), std({1.0f, 1.0f, 1.0f}) {}
};

/**
 * @brief Configuration for trajectory generator
 */
struct GeneratorConfig {
    std::string model_path;
    int latent_dim = 64;
    int seq_len = 50;
    int num_threads = 4;
    bool use_gpu = false;
    
    GeneratorConfig() = default;
    GeneratorConfig(const std::string& path) : model_path(path) {}
};

/**
 * @brief Main class for trajectory generation inference
 */
class TrajectoryGenerator {
public:
    /**
     * @brief Constructor
     * @param config Generator configuration
     */
    explicit TrajectoryGenerator(const GeneratorConfig& config);
    
    /**
     * @brief Destructor
     */
    ~TrajectoryGenerator();
    
    /**
     * @brief Load normalization parameters from JSON file
     * @param norm_path Path to normalization JSON file
     * @return True if successful
     */
    bool loadNormalization(const std::string& norm_path);
    
    /**
     * @brief Generate a single trajectory
     * @param start Starting waypoint
     * @param end Ending waypoint
     * @return Generated trajectory
     */
    Trajectory generate(const Waypoint& start, const Waypoint& end);
    
    /**
     * @brief Generate multiple diverse trajectories
     * @param start Starting waypoint
     * @param end Ending waypoint
     * @param n_samples Number of trajectories to generate
     * @return Vector of generated trajectories
     */
    std::vector<Trajectory> generateMultiple(const Waypoint& start, 
                                             const Waypoint& end,
                                             int n_samples);
    
    /**
     * @brief Check if model is loaded and ready
     * @return True if ready for inference
     */
    bool isReady() const { return session_ != nullptr; }
    
    /**
     * @brief Get sequence length of generated trajectories
     * @return Sequence length
     */
    int getSeqLen() const { return config_.seq_len; }

private:
    /**
     * @brief Normalize a waypoint
     */
    std::array<float, 3> normalize(const Waypoint& wp) const;
    
    /**
     * @brief Denormalize a waypoint
     */
    Waypoint denormalize(const std::array<float, 3>& normalized) const;
    
    /**
     * @brief Sample from standard normal distribution
     */
    std::vector<float> sampleLatent();
    
    /**
     * @brief Run ONNX inference
     */
    Trajectory runInference(const std::vector<float>& latent,
                           const Waypoint& start,
                           const Waypoint& end);

    GeneratorConfig config_;
    NormalizationParams norm_params_;
    
    // ONNX Runtime objects
    std::unique_ptr<Ort::Env> env_;
    std::unique_ptr<Ort::Session> session_;
    std::unique_ptr<Ort::SessionOptions> session_options_;
    Ort::MemoryInfo memory_info_;
    
    // Input/output names
    std::vector<const char*> input_names_;
    std::vector<const char*> output_names_;
    
    // Random number generator state
    unsigned int rng_state_;
};

/**
 * @brief Compute path length of trajectory
 * @param trajectory Input trajectory
 * @return Total path length in meters
 */
float computePathLength(const Trajectory& trajectory);

/**
 * @brief Compute smoothness score of trajectory
 * @param trajectory Input trajectory
 * @return Smoothness score (higher is smoother)
 */
float computeSmoothnessScore(const Trajectory& trajectory);

/**
 * @brief Compute average curvature of trajectory
 * @param trajectory Input trajectory
 * @return Average curvature in rad/m
 */
float computeAverageCurvature(const Trajectory& trajectory);

/**
 * @brief Print trajectory statistics
 * @param trajectory Input trajectory
 */
void printTrajectoryStats(const Trajectory& trajectory);

} // namespace trajectory

#endif // TRAJECTORY_INFERENCE_H

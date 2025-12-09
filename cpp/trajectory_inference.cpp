/**
 * @file trajectory_inference.cpp
 * @brief Implementation of trajectory generation inference
 */

#include "trajectory_inference.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <random>
#include <stdexcept>
#include <algorithm>
#include <numeric>

// JSON parsing (simple implementation for normalization params)
#include <regex>

namespace trajectory {

// Helper function to parse simple JSON (for normalization params)
static NormalizationParams parseNormalizationJSON(const std::string& filepath) {
    NormalizationParams params;
    
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open normalization file: " + filepath);
    }
    
    std::string content((std::istreambuf_iterator<char>(file)),
                        std::istreambuf_iterator<char>());
    
    // Simple regex parsing for mean and std arrays
    std::regex mean_regex(R"("mean"\s*:\s*\[([\d\.\-\s,]+)\])");
    std::regex std_regex(R"("std"\s*:\s*\[([\d\.\-\s,]+)\])");
    
    std::smatch match;
    
    // Parse mean
    if (std::regex_search(content, match, mean_regex)) {
        std::string values = match[1].str();
        std::istringstream iss(values);
        std::string token;
        int idx = 0;
        while (std::getline(iss, token, ',') && idx < 3) {
            params.mean[idx++] = std::stof(token);
        }
    }
    
    // Parse std
    if (std::regex_search(content, match, std_regex)) {
        std::string values = match[1].str();
        std::istringstream iss(values);
        std::string token;
        int idx = 0;
        while (std::getline(iss, token, ',') && idx < 3) {
            params.std[idx++] = std::stof(token);
        }
    }
    
    return params;
}

TrajectoryGenerator::TrajectoryGenerator(const GeneratorConfig& config)
    : config_(config)
    , memory_info_(Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault))
    , rng_state_(static_cast<unsigned int>(std::time(nullptr)))
{
    // Initialize ONNX Runtime environment
    env_ = std::make_unique<Ort::Env>(ORT_LOGGING_LEVEL_WARNING, "TrajectoryGenerator");
    
    // Create session options
    session_options_ = std::make_unique<Ort::SessionOptions>();
    session_options_->SetIntraOpNumThreads(config_.num_threads);
    session_options_->SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    
    // GPU support (if requested and available)
    if (config_.use_gpu) {
        // Note: Requires CUDA/TensorRT provider to be available
        // OrtCUDAProviderOptions cuda_options;
        // session_options_->AppendExecutionProvider_CUDA(cuda_options);
        std::cerr << "Warning: GPU support not implemented in this version" << std::endl;
    }
    
    // Load model
    try {
#ifdef _WIN32
        std::wstring model_path_w(config_.model_path.begin(), config_.model_path.end());
        session_ = std::make_unique<Ort::Session>(*env_, model_path_w.c_str(), *session_options_);
#else
        session_ = std::make_unique<Ort::Session>(*env_, config_.model_path.c_str(), *session_options_);
#endif
        
        // Get input/output names
        Ort::AllocatorWithDefaultOptions allocator;
        
        // Input names: latent, start, end
        input_names_.push_back("latent");
        input_names_.push_back("start");
        input_names_.push_back("end");
        
        // Output names: trajectory
        output_names_.push_back("trajectory");
        
        std::cout << "✓ ONNX model loaded successfully: " << config_.model_path << std::endl;
        
    } catch (const Ort::Exception& e) {
        throw std::runtime_error(std::string("Failed to load ONNX model: ") + e.what());
    }
}

TrajectoryGenerator::~TrajectoryGenerator() = default;

bool TrajectoryGenerator::loadNormalization(const std::string& norm_path) {
    try {
        norm_params_ = parseNormalizationJSON(norm_path);
        
        std::cout << "✓ Normalization loaded:" << std::endl;
        std::cout << "  Mean: [" << norm_params_.mean[0] << ", " 
                  << norm_params_.mean[1] << ", " << norm_params_.mean[2] << "]" << std::endl;
        std::cout << "  Std:  [" << norm_params_.std[0] << ", "
                  << norm_params_.std[1] << ", " << norm_params_.std[2] << "]" << std::endl;
        
        return true;
    } catch (const std::exception& e) {
        std::cerr << "Failed to load normalization: " << e.what() << std::endl;
        return false;
    }
}

std::array<float, 3> TrajectoryGenerator::normalize(const Waypoint& wp) const {
    return {
        (wp.x - norm_params_.mean[0]) / norm_params_.std[0],
        (wp.y - norm_params_.mean[1]) / norm_params_.std[1],
        (wp.z - norm_params_.mean[2]) / norm_params_.std[2]
    };
}

Waypoint TrajectoryGenerator::denormalize(const std::array<float, 3>& normalized) const {
    return Waypoint(
        normalized[0] * norm_params_.std[0] + norm_params_.mean[0],
        normalized[1] * norm_params_.std[1] + norm_params_.mean[1],
        normalized[2] * norm_params_.std[2] + norm_params_.mean[2]
    );
}

std::vector<float> TrajectoryGenerator::sampleLatent() {
    // Sample from standard normal distribution
    std::vector<float> latent(config_.latent_dim);
    
    // Simple Box-Muller transform for normal distribution
    std::mt19937 gen(rng_state_++);
    std::normal_distribution<float> dist(0.0f, 1.0f);
    
    for (int i = 0; i < config_.latent_dim; ++i) {
        latent[i] = dist(gen);
    }
    
    return latent;
}

Trajectory TrajectoryGenerator::runInference(const std::vector<float>& latent,
                                             const Waypoint& start,
                                             const Waypoint& end) {
    // Normalize inputs
    auto start_norm = normalize(start);
    auto end_norm = normalize(end);
    
    // Prepare input tensors
    std::vector<int64_t> latent_shape = {1, config_.latent_dim};
    std::vector<int64_t> waypoint_shape = {1, 3};
    
    // Create input tensors
    auto latent_tensor = Ort::Value::CreateTensor<float>(
        memory_info_, 
        const_cast<float*>(latent.data()), 
        latent.size(),
        latent_shape.data(), 
        latent_shape.size()
    );
    
    auto start_tensor = Ort::Value::CreateTensor<float>(
        memory_info_,
        const_cast<float*>(start_norm.data()),
        start_norm.size(),
        waypoint_shape.data(),
        waypoint_shape.size()
    );
    
    auto end_tensor = Ort::Value::CreateTensor<float>(
        memory_info_,
        const_cast<float*>(end_norm.data()),
        end_norm.size(),
        waypoint_shape.data(),
        waypoint_shape.size()
    );
    
    // Prepare inputs
    std::vector<Ort::Value> input_tensors;
    input_tensors.push_back(std::move(latent_tensor));
    input_tensors.push_back(std::move(start_tensor));
    input_tensors.push_back(std::move(end_tensor));
    
    // Run inference
    auto output_tensors = session_->Run(
        Ort::RunOptions{nullptr},
        input_names_.data(),
        input_tensors.data(),
        input_tensors.size(),
        output_names_.data(),
        output_names_.size()
    );
    
    // Extract output
    float* output_data = output_tensors[0].GetTensorMutableData<float>();
    auto output_shape = output_tensors[0].GetTensorTypeAndShapeInfo().GetShape();
    
    int seq_len = static_cast<int>(output_shape[1]);
    
    // Convert to trajectory
    Trajectory trajectory;
    trajectory.reserve(seq_len);
    
    for (int i = 0; i < seq_len; ++i) {
        std::array<float, 3> normalized = {
            output_data[i * 3 + 0],
            output_data[i * 3 + 1],
            output_data[i * 3 + 2]
        };
        
        trajectory.push_back(denormalize(normalized));
    }
    
    return trajectory;
}

Trajectory TrajectoryGenerator::generate(const Waypoint& start, const Waypoint& end) {
    if (!isReady()) {
        throw std::runtime_error("Generator not initialized");
    }
    
    // Sample latent vector
    auto latent = sampleLatent();
    
    // Run inference
    return runInference(latent, start, end);
}

std::vector<Trajectory> TrajectoryGenerator::generateMultiple(const Waypoint& start,
                                                              const Waypoint& end,
                                                              int n_samples) {
    if (!isReady()) {
        throw std::runtime_error("Generator not initialized");
    }
    
    std::vector<Trajectory> trajectories;
    trajectories.reserve(n_samples);
    
    for (int i = 0; i < n_samples; ++i) {
        trajectories.push_back(generate(start, end));
    }
    
    return trajectories;
}

// Utility functions

float computePathLength(const Trajectory& trajectory) {
    float length = 0.0f;
    
    for (size_t i = 1; i < trajectory.size(); ++i) {
        float dx = trajectory[i].x - trajectory[i-1].x;
        float dy = trajectory[i].y - trajectory[i-1].y;
        float dz = trajectory[i].z - trajectory[i-1].z;
        
        length += std::sqrt(dx*dx + dy*dy + dz*dz);
    }
    
    return length;
}

float computeAverageCurvature(const Trajectory& trajectory) {
    if (trajectory.size() < 3) return 0.0f;
    
    std::vector<float> curvatures;
    
    for (size_t i = 1; i < trajectory.size() - 1; ++i) {
        // Vectors
        float v1x = trajectory[i].x - trajectory[i-1].x;
        float v1y = trajectory[i].y - trajectory[i-1].y;
        float v1z = trajectory[i].z - trajectory[i-1].z;
        
        float v2x = trajectory[i+1].x - trajectory[i].x;
        float v2y = trajectory[i+1].y - trajectory[i].y;
        float v2z = trajectory[i+1].z - trajectory[i].z;
        
        float norm1 = std::sqrt(v1x*v1x + v1y*v1y + v1z*v1z);
        float norm2 = std::sqrt(v2x*v2x + v2y*v2y + v2z*v2z);
        
        if (norm1 > 1e-6f && norm2 > 1e-6f) {
            float dot = v1x*v2x + v1y*v2y + v1z*v2z;
            float cos_angle = dot / (norm1 * norm2);
            cos_angle = std::max(-1.0f, std::min(1.0f, cos_angle));
            
            float angle = std::acos(cos_angle);
            float curvature = angle / norm1;
            
            curvatures.push_back(curvature);
        }
    }
    
    if (curvatures.empty()) return 0.0f;
    
    float sum = std::accumulate(curvatures.begin(), curvatures.end(), 0.0f);
    return sum / curvatures.size();
}

float computeSmoothnessScore(const Trajectory& trajectory) {
    float avg_curvature = computeAverageCurvature(trajectory);
    return 1.0f / (1.0f + avg_curvature);
}

void printTrajectoryStats(const Trajectory& trajectory) {
    float path_length = computePathLength(trajectory);
    float avg_curvature = computeAverageCurvature(trajectory);
    float smoothness = computeSmoothnessScore(trajectory);
    
    // Compute straight-line distance
    float dx = trajectory.back().x - trajectory.front().x;
    float dy = trajectory.back().y - trajectory.front().y;
    float dz = trajectory.back().z - trajectory.front().z;
    float straight_dist = std::sqrt(dx*dx + dy*dy + dz*dz);
    
    float efficiency = straight_dist / path_length;
    
    std::cout << "Trajectory Statistics:" << std::endl;
    std::cout << "  Path length: " << path_length << " m" << std::endl;
    std::cout << "  Straight-line distance: " << straight_dist << " m" << std::endl;
    std::cout << "  Efficiency: " << efficiency << std::endl;
    std::cout << "  Avg curvature: " << avg_curvature << " rad/m" << std::endl;
    std::cout << "  Smoothness score: " << smoothness << std::endl;
}

} // namespace trajectory

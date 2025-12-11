# C++ Porting Guide for Trajectory Generation Model

## Table of Contents
1. [Overview](#overview)
2. [Model Architecture](#model-architecture)
3. [Mathematical Formulations](#mathematical-formulations)
4. [Inference Pipeline](#inference-pipeline)
5. [Quality Metrics Implementation](#quality-metrics-implementation)
6. [Complete C++ Code Examples](#complete-cpp-code-examples)
7. [Training Components (Optional)](#training-components-optional)

---

## Overview

This guide provides detailed algorithms and formulas for porting the trajectory generation model to C++. The system uses a **Conditional Variational Autoencoder (CVAE)** trained in Python/PyTorch, but inference can be performed in C++ using ONNX Runtime.

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Training (Python)                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐     │
│  │   Data   │───▶│  Train   │───▶│  Export to   │     │
│  │Generator │    │  Model   │    │     ONNX     │     │
│  └──────────┘    └──────────┘    └──────────────┘     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Inference (C++ Application)                │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐     │
│  │   ONNX   │───▶│ Generate │───▶│   Quality    │     │
│  │  Model   │    │Trajectory│    │   Metrics    │     │
│  └──────────┘    └──────────┘    └──────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## Model Architecture

### CVAE Components

#### 1. Encoder (Trajectory → Latent Space)
- **Input**: Trajectory sequence `[seq_len, 3]`
- **Architecture**: Bidirectional LSTM
- **Output**: `μ` (mean) and `log σ²` (log variance) of latent distribution `[latent_dim]`

```
Encoder:
  BiLSTM(input_dim=3, hidden_dim=256, layers=2)
    ↓
  Concatenate forward & backward hidden states
    ↓
  Linear(512 → 64) for μ
  Linear(512 → 64) for log σ²
```

#### 2. Reparameterization Trick
```cpp
// Sample z from N(μ, σ²)
z = μ + σ * ε
where:
  σ = exp(0.5 * log σ²)
  ε ~ N(0, 1)
```

#### 3. Decoder (Latent + Conditions → Trajectory)
- **Input**: Latent vector `z [64]`, start waypoint `[3]`, end waypoint `[3]`
- **Architecture**: LSTM with autoregressive generation
- **Output**: Trajectory sequence `[seq_len, 3]`

```
Decoder:
  For each timestep t in [0, seq_len):
    Input: [current_point, z, start, end]  # Concatenated
    LSTM step → hidden state
    Linear(256 → 3) → next point
```

---

## Mathematical Formulations

### Loss Function (Training Only)

The total loss is a weighted combination of four components:

```
L_total = L_recon + β·L_KL + λ_smooth·L_smooth + λ_boundary·L_boundary
```

#### 1. Reconstruction Loss
```cpp
L_recon = MSE(predicted, target)
        = (1/N) * Σ ||predicted[i] - target[i]||²
```

#### 2. KL Divergence
```cpp
L_KL = KL(q(z|x) || p(z))
     = -0.5 * Σ(1 + log σ² - μ² - σ²)
     = -0.5 * Σ(1 + logvar - μ² - exp(logvar))
```

#### 3. Smoothness Loss (Curvature Penalty)
```cpp
L_smooth = (1/N) * Σ ||trajectory[i+1] - 2*trajectory[i] + trajectory[i-1]||²
```
This is the second derivative (acceleration), penalizing sharp turns.

#### 4. Boundary Loss
```cpp
L_boundary = MSE(trajectory[0], start) + MSE(trajectory[-1], end)
```

**Hyperparameters**:
- β = 0.001 (KL weight)
- λ_smooth = 0.1 (smoothness weight)
- λ_boundary = 1.0 (boundary weight)

---

## Inference Pipeline

### Step-by-Step Inference (C++ Implementation)

#### Step 1: Data Normalization

```cpp
struct NormalizationParams {
    float mean_x, mean_y, mean_z;
    float std_x, std_y, std_z;
};

// Normalize a waypoint
Waypoint normalize(const Waypoint& wp, const NormalizationParams& params) {
    return Waypoint(
        (wp.x - params.mean_x) / params.std_x,
        (wp.y - params.mean_y) / params.std_y,
        (wp.z - params.mean_z) / params.std_z
    );
}

// Denormalize a waypoint
Waypoint denormalize(const Waypoint& wp, const NormalizationParams& params) {
    return Waypoint(
        wp.x * params.std_x + params.mean_x,
        wp.y * params.std_y + params.mean_y,
        wp.z * params.std_z + params.mean_z
    );
}
```

#### Step 2: Sample Latent Vector

```cpp
#include <random>

std::vector<float> sampleLatent(int latent_dim) {
    static std::mt19937 gen(std::random_device{}());
    std::normal_distribution<float> dist(0.0f, 1.0f);
    
    std::vector<float> z(latent_dim);
    for (int i = 0; i < latent_dim; ++i) {
        z[i] = dist(gen);
    }
    return z;
}
```

#### Step 3: Run ONNX Inference

```cpp
// Pseudo-code for ONNX inference
Trajectory runInference(
    const std::vector<float>& latent_z,
    const Waypoint& start_norm,
    const Waypoint& end_norm,
    Ort::Session& session
) {
    // Prepare input tensors
    // Input 1: latent vector [1, 64]
    // Input 2: start waypoint [1, 3]
    // Input 3: end waypoint [1, 3]
    
    // Run inference
    auto output_tensors = session.Run(...);
    
    // Extract trajectory [1, seq_len, 3]
    Trajectory trajectory = extractTrajectory(output_tensors);
    
    return trajectory;
}
```

#### Complete Inference Function

```cpp
Trajectory generateTrajectory(
    const Waypoint& start,
    const Waypoint& end,
    const NormalizationParams& norm_params,
    Ort::Session& session,
    int latent_dim = 64
) {
    // 1. Normalize inputs
    Waypoint start_norm = normalize(start, norm_params);
    Waypoint end_norm = normalize(end, norm_params);
    
    // 2. Sample latent vector
    std::vector<float> z = sampleLatent(latent_dim);
    
    // 3. Run ONNX inference
    Trajectory trajectory_norm = runInference(z, start_norm, end_norm, session);
    
    // 4. Denormalize output
    Trajectory trajectory;
    for (const auto& wp : trajectory_norm) {
        trajectory.push_back(denormalize(wp, norm_params));
    }
    
    return trajectory;
}
```

---

## Quality Metrics Implementation

### 1. Path Length

```cpp
float computePathLength(const Trajectory& trajectory) {
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
```

### 2. Path Efficiency

```cpp
float computePathEfficiency(const Trajectory& trajectory) {
    if (trajectory.size() < 2) return 1.0f;
    
    // Straight-line distance
    const Waypoint& start = trajectory.front();
    const Waypoint& end = trajectory.back();
    
    float dx = end.x - start.x;
    float dy = end.y - start.y;
    float dz = end.z - start.z;
    float straight_line = std::sqrt(dx*dx + dy*dy + dz*dz);
    
    // Actual path length
    float path_length = computePathLength(trajectory);
    
    if (path_length < 1e-6f) return 0.0f;
    
    return straight_line / path_length;
}
```

### 3. Average Curvature

```cpp
float computeAverageCurvature(const Trajectory& trajectory) {
    if (trajectory.size() < 3) return 0.0f;
    
    std::vector<float> curvatures;
    
    for (size_t i = 1; i < trajectory.size() - 1; ++i) {
        // Vectors
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
            
            // Cosine of angle
            float cos_angle = dot / (norm1 * norm2);
            cos_angle = std::max(-1.0f, std::min(1.0f, cos_angle));
            
            // Angle
            float angle = std::acos(cos_angle);
            
            // Curvature
            float curvature = angle / norm1;
            curvatures.push_back(curvature);
        }
    }
    
    if (curvatures.empty()) return 0.0f;
    
    float sum = 0.0f;
    for (float c : curvatures) sum += c;
    
    return sum / curvatures.size();
}
```

### 4. Smoothness Score

```cpp
float computeSmoothnessScore(const Trajectory& trajectory) {
    float avg_curvature = computeAverageCurvature(trajectory);
    return 1.0f / (1.0f + avg_curvature);
}
```

### 5. Maximum Curvature

```cpp
float computeMaxCurvature(const Trajectory& trajectory) {
    if (trajectory.size() < 3) return 0.0f;
    
    float max_curvature = 0.0f;
    
    for (size_t i = 1; i < trajectory.size() - 1; ++i) {
        const Waypoint& p_prev = trajectory[i - 1];
        const Waypoint& p_curr = trajectory[i];
        const Waypoint& p_next = trajectory[i + 1];
        
        float v1_x = p_curr.x - p_prev.x;
        float v1_y = p_curr.y - p_prev.y;
        float v1_z = p_curr.z - p_prev.z;
        float norm1 = std::sqrt(v1_x*v1_x + v1_y*v1_y + v1_z*v1_z);
        
        float v2_x = p_next.x - p_curr.x;
        float v2_y = p_next.y - p_curr.y;
        float v2_z = p_next.z - p_curr.z;
        float norm2 = std::sqrt(v2_x*v2_x + v2_y*v2_y + v2_z*v2_z);
        
        if (norm1 > 1e-6f && norm2 > 1e-6f) {
            float dot = v1_x*v2_x + v1_y*v2_y + v1_z*v2_z;
            float cos_angle = std::max(-1.0f, std::min(1.0f, dot / (norm1 * norm2)));
            float angle = std::acos(cos_angle);
            float curvature = angle / norm1;
            
            max_curvature = std::max(max_curvature, curvature);
        }
    }
    
    return max_curvature;
}
```

### 6. Endpoint Error

```cpp
float computeEndpointError(const Trajectory& trajectory, 
                          const Waypoint& expected_end) {
    if (trajectory.empty()) return 0.0f;
    
    const Waypoint& actual_end = trajectory.back();
    
    float dx = actual_end.x - expected_end.x;
    float dy = actual_end.y - expected_end.y;
    float dz = actual_end.z - expected_end.z;
    
    return std::sqrt(dx*dx + dy*dy + dz*dz);
}
```

### 7. Complete Quality Metrics Structure

```cpp
struct TrajectoryMetrics {
    float path_length;
    float path_efficiency;
    float avg_curvature;
    float max_curvature;
    float smoothness_score;
    float endpoint_error;
    float min_altitude;
    float max_altitude;
    float avg_altitude;
};

TrajectoryMetrics evaluateTrajectory(const Trajectory& trajectory,
                                     const Waypoint& expected_end) {
    TrajectoryMetrics metrics;
    
    metrics.path_length = computePathLength(trajectory);
    metrics.path_efficiency = computePathEfficiency(trajectory);
    metrics.avg_curvature = computeAverageCurvature(trajectory);
    metrics.max_curvature = computeMaxCurvature(trajectory);
    metrics.smoothness_score = computeSmoothnessScore(trajectory);
    metrics.endpoint_error = computeEndpointError(trajectory, expected_end);
    
    // Altitude statistics
    if (!trajectory.empty()) {
        metrics.min_altitude = trajectory[0].z;
        metrics.max_altitude = trajectory[0].z;
        float sum_altitude = 0.0f;
        
        for (const auto& wp : trajectory) {
            metrics.min_altitude = std::min(metrics.min_altitude, wp.z);
            metrics.max_altitude = std::max(metrics.max_altitude, wp.z);
            sum_altitude += wp.z;
        }
        
        metrics.avg_altitude = sum_altitude / trajectory.size();
    }
    
    return metrics;
}
```

---

## Complete C++ Code Examples

### Complete Header File (trajectory_metrics.h)

```cpp
#ifndef TRAJECTORY_METRICS_H
#define TRAJECTORY_METRICS_H

#include <vector>
#include <cmath>
#include <algorithm>

namespace trajectory {

struct Waypoint {
    float x, y, z;
    Waypoint() : x(0), y(0), z(0) {}
    Waypoint(float x_, float y_, float z_) : x(x_), y(y_), z(z_) {}
};

using Trajectory = std::vector<Waypoint>;

struct TrajectoryMetrics {
    float path_length;
    float path_efficiency;
    float avg_curvature;
    float max_curvature;
    float smoothness_score;
    float endpoint_error;
    float min_altitude;
    float max_altitude;
    float avg_altitude;
};

// Function declarations
float computePathLength(const Trajectory& trajectory);
float computePathEfficiency(const Trajectory& trajectory);
float computeAverageCurvature(const Trajectory& trajectory);
float computeMaxCurvature(const Trajectory& trajectory);
float computeSmoothnessScore(const Trajectory& trajectory);
float computeEndpointError(const Trajectory& trajectory, const Waypoint& expected_end);
TrajectoryMetrics evaluateTrajectory(const Trajectory& trajectory, const Waypoint& expected_end);

} // namespace trajectory

#endif // TRAJECTORY_METRICS_H
```

### Complete Implementation File (trajectory_metrics.cpp)

```cpp
#include "trajectory_metrics.h"
#include <numeric>

namespace trajectory {

float computePathLength(const Trajectory& trajectory) {
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

float computePathEfficiency(const Trajectory& trajectory) {
    if (trajectory.size() < 2) return 1.0f;
    
    const Waypoint& start = trajectory.front();
    const Waypoint& end = trajectory.back();
    
    float dx = end.x - start.x;
    float dy = end.y - start.y;
    float dz = end.z - start.z;
    float straight_line = std::sqrt(dx*dx + dy*dy + dz*dz);
    
    float path_length = computePathLength(trajectory);
    
    return (path_length > 1e-6f) ? (straight_line / path_length) : 0.0f;
}

float computeAverageCurvature(const Trajectory& trajectory) {
    if (trajectory.size() < 3) return 0.0f;
    
    std::vector<float> curvatures;
    
    for (size_t i = 1; i < trajectory.size() - 1; ++i) {
        const Waypoint& p_prev = trajectory[i - 1];
        const Waypoint& p_curr = trajectory[i];
        const Waypoint& p_next = trajectory[i + 1];
        
        float v1_x = p_curr.x - p_prev.x;
        float v1_y = p_curr.y - p_prev.y;
        float v1_z = p_curr.z - p_prev.z;
        float norm1 = std::sqrt(v1_x*v1_x + v1_y*v1_y + v1_z*v1_z);
        
        float v2_x = p_next.x - p_curr.x;
        float v2_y = p_next.y - p_curr.y;
        float v2_z = p_next.z - p_curr.z;
        float norm2 = std::sqrt(v2_x*v2_x + v2_y*v2_y + v2_z*v2_z);
        
        if (norm1 > 1e-6f && norm2 > 1e-6f) {
            float dot = v1_x*v2_x + v1_y*v2_y + v1_z*v2_z;
            float cos_angle = std::max(-1.0f, std::min(1.0f, dot / (norm1 * norm2)));
            float angle = std::acos(cos_angle);
            float curvature = angle / norm1;
            curvatures.push_back(curvature);
        }
    }
    
    if (curvatures.empty()) return 0.0f;
    
    return std::accumulate(curvatures.begin(), curvatures.end(), 0.0f) / curvatures.size();
}

float computeMaxCurvature(const Trajectory& trajectory) {
    if (trajectory.size() < 3) return 0.0f;
    
    float max_curvature = 0.0f;
    
    for (size_t i = 1; i < trajectory.size() - 1; ++i) {
        const Waypoint& p_prev = trajectory[i - 1];
        const Waypoint& p_curr = trajectory[i];
        const Waypoint& p_next = trajectory[i + 1];
        
        float v1_x = p_curr.x - p_prev.x;
        float v1_y = p_curr.y - p_prev.y;
        float v1_z = p_curr.z - p_prev.z;
        float norm1 = std::sqrt(v1_x*v1_x + v1_y*v1_y + v1_z*v1_z);
        
        float v2_x = p_next.x - p_curr.x;
        float v2_y = p_next.y - p_curr.y;
        float v2_z = p_next.z - p_curr.z;
        float norm2 = std::sqrt(v2_x*v2_x + v2_y*v2_y + v2_z*v2_z);
        
        if (norm1 > 1e-6f && norm2 > 1e-6f) {
            float dot = v1_x*v2_x + v1_y*v2_y + v1_z*v2_z;
            float cos_angle = std::max(-1.0f, std::min(1.0f, dot / (norm1 * norm2)));
            float angle = std::acos(cos_angle);
            float curvature = angle / norm1;
            max_curvature = std::max(max_curvature, curvature);
        }
    }
    
    return max_curvature;
}

float computeSmoothnessScore(const Trajectory& trajectory) {
    float avg_curvature = computeAverageCurvature(trajectory);
    return 1.0f / (1.0f + avg_curvature);
}

float computeEndpointError(const Trajectory& trajectory, const Waypoint& expected_end) {
    if (trajectory.empty()) return 0.0f;
    
    const Waypoint& actual_end = trajectory.back();
    float dx = actual_end.x - expected_end.x;
    float dy = actual_end.y - expected_end.y;
    float dz = actual_end.z - expected_end.z;
    
    return std::sqrt(dx*dx + dy*dy + dz*dz);
}

TrajectoryMetrics evaluateTrajectory(const Trajectory& trajectory,
                                     const Waypoint& expected_end) {
    TrajectoryMetrics metrics;
    
    metrics.path_length = computePathLength(trajectory);
    metrics.path_efficiency = computePathEfficiency(trajectory);
    metrics.avg_curvature = computeAverageCurvature(trajectory);
    metrics.max_curvature = computeMaxCurvature(trajectory);
    metrics.smoothness_score = computeSmoothnessScore(trajectory);
    metrics.endpoint_error = computeEndpointError(trajectory, expected_end);
    
    if (!trajectory.empty()) {
        metrics.min_altitude = trajectory[0].z;
        metrics.max_altitude = trajectory[0].z;
        float sum_altitude = 0.0f;
        
        for (const auto& wp : trajectory) {
            metrics.min_altitude = std::min(metrics.min_altitude, wp.z);
            metrics.max_altitude = std::max(metrics.max_altitude, wp.z);
            sum_altitude += wp.z;
        }
        
        metrics.avg_altitude = sum_altitude / trajectory.size();
    } else {
        metrics.min_altitude = 0.0f;
        metrics.max_altitude = 0.0f;
        metrics.avg_altitude = 0.0f;
    }
    
    return metrics;
}

} // namespace trajectory
```

---

## Training Components (Optional)

If you need to implement training in C++, you have several options:

### Option 1: Use LibTorch (PyTorch C++ API)

```cpp
#include <torch/torch.h>

// Define model
struct CVAEImpl : torch::nn::Module {
    // Define encoder, decoder, etc.
};

TORCH_MODULE(CVAE);

// Training loop
void train(CVAE model, torch::data::DataLoader<> dataloader) {
    torch::optim::Adam optimizer(model->parameters(), 0.001);
    
    for (auto& batch : dataloader) {
        // Forward pass
        auto [reconstructed, mu, logvar] = model->forward(batch.data);
        
        // Compute loss
        auto loss = compute_loss(reconstructed, batch.data, mu, logvar);
        
        // Backward pass
        optimizer.zero_grad();
        loss.backward();
        optimizer.step();
    }
}
```

### Option 2: Keep Training in Python

**Recommended approach**: Train in Python, export to ONNX, use in C++.

```bash
# Python side
python src/train.py --epochs 100
python src/export_onnx.py --checkpoint models/best_model.pth

# C++ side
./trajectory_app models/trajectory_generator.onnx
```

---

## Integration Checklist

- [ ] Export trained model to ONNX
- [ ] Build C++ inference engine (cpp/trajectory_inference.cpp)
- [ ] Implement quality metrics (trajectory_metrics.cpp)
- [ ] Load normalization parameters
- [ ] Test inference with known inputs
- [ ] Integrate into your application
- [ ] Add obstacle avoidance (if needed)
- [ ] Implement batch processing (if needed)
- [ ] Add multi-threading (if needed)
- [ ] Profile and optimize performance

---

## Performance Tips

1. **Batch Processing**: Generate multiple trajectories in one ONNX call
2. **Multi-threading**: Use multiple ONNX sessions for parallel inference
3. **GPU Acceleration**: Use ONNX Runtime with CUDA provider
4. **Memory Pool**: Reuse memory buffers for input/output tensors
5. **Model Quantization**: Quantize ONNX model to INT8 for faster inference

---

## References

1. **CVAE Paper**: Sohn et al., "Learning Structured Output Representation using Deep Conditional Generative Models"
2. **ONNX Runtime**: https://onnxruntime.ai/
3. **LibTorch**: https://pytorch.org/cppdocs/

---

## Support

For questions or issues:
1. Check existing Python implementation in `src/`
2. Review C++ examples in `cpp/`
3. Run demonstration: `python model_pipeline_demo.py`
4. Test inference: `python src/inference.py`

---

**Last Updated**: December 2025

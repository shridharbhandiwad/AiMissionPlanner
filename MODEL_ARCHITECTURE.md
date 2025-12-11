# Trajectory Generation Model: Complete Architecture Documentation

## Executive Summary

This document provides a comprehensive technical specification of the Conditional Variational Autoencoder (CVAE) model used for trajectory generation. It includes mathematical formulations, architecture diagrams, and implementation details suitable for porting to C++ or other platforms.

---

## Table of Contents

1. [Problem Formulation](#problem-formulation)
2. [Model Architecture](#model-architecture)
3. [Mathematical Framework](#mathematical-framework)
4. [Training Process](#training-process)
5. [Inference Process](#inference-process)
6. [Evaluation Metrics](#evaluation-metrics)
7. [Implementation Details](#implementation-details)

---

## Problem Formulation

### Objective

Generate smooth, safe, and efficient 3D trajectories between two waypoints (start and end).

### Inputs
- **Start waypoint**: `s = (x_s, y_s, z_s)` ∈ ℝ³
- **End waypoint**: `e = (x_e, y_e, z_e)` ∈ ℝ³

### Output
- **Trajectory**: `T = {p₀, p₁, ..., p_{n-1}}` where `pᵢ = (xᵢ, yᵢ, zᵢ)` ∈ ℝ³
- Constraints:
  - p₀ = s (start constraint)
  - p_{n-1} = e (end constraint)
  - Smooth transitions (minimize curvature)

### Challenges
1. **Diversity**: Generate multiple different trajectories for the same start-end pair
2. **Smoothness**: Avoid sharp turns and discontinuities
3. **Efficiency**: Balance path length vs. directness
4. **Safety**: Avoid obstacles (when present)
5. **Real-time**: Fast inference (<100ms per trajectory)

---

## Model Architecture

### Overview: Conditional Variational Autoencoder (CVAE)

```
                    Training Phase
┌──────────────────────────────────────────────────────┐
│                                                      │
│  Ground Truth    ┌─────────┐                        │
│  Trajectory ────▶│ Encoder │────▶ μ, log σ²         │
│  [seq_len, 3]    └─────────┘      [latent_dim]      │
│                        │                             │
│                        │ Reparameterization          │
│                        ▼                             │
│                    z = μ + σ·ε                       │
│                    [latent_dim]                      │
│                        │                             │
│  Conditions            │                             │
│  (start, end) ─────────┼────────▶┌─────────┐        │
│  [6]                   └────────▶│ Decoder │────▶   │
│                                   └─────────┘        │
│                                     │                │
│                                     ▼                │
│                            Reconstructed Trajectory  │
│                               [seq_len, 3]           │
│                                                      │
└──────────────────────────────────────────────────────┘

                    Inference Phase
┌──────────────────────────────────────────────────────┐
│                                                      │
│  Sample z ~ N(0, I)                                  │
│  [latent_dim]                                        │
│       │                                              │
│       │                                              │
│  Conditions                                          │
│  (start, end) ───────────┐                          │
│  [6]                     │                          │
│                          ▼                          │
│                   ┌─────────┐                        │
│                   │ Decoder │────▶ Generated         │
│                   └─────────┘      Trajectory        │
│                                    [seq_len, 3]      │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Component Details

#### 1. Encoder

**Purpose**: Map trajectory to latent distribution parameters

**Architecture**:
```
Input: Trajectory T = [seq_len, 3]
  ↓
Bidirectional LSTM
  - input_size: 3 (x, y, z)
  - hidden_size: 256
  - num_layers: 2
  - bidirectional: True
  ↓
Concatenate forward & backward final hidden states
  [hidden_size × 2] = [512]
  ↓
┌─────────────────────────────────┐
│ Linear Layer (512 → latent_dim) │ → μ [64]
└─────────────────────────────────┘
┌─────────────────────────────────┐
│ Linear Layer (512 → latent_dim) │ → log σ² [64]
└─────────────────────────────────┘
```

**Mathematical Formulation**:
```
h = BiLSTM(T)
μ = W_μ · h + b_μ
log σ² = W_σ · h + b_σ
```

#### 2. Reparameterization Trick

**Purpose**: Sample from learned distribution while maintaining differentiability

**Formula**:
```
z = μ + exp(0.5 · log σ²) · ε
  = μ + σ · ε

where:
  ε ~ N(0, I)  (standard normal)
  σ = exp(0.5 · log σ²)
```

**Why Log Variance?**
- Ensures σ² > 0 (variance must be positive)
- Numerically stable
- Easier optimization

#### 3. Decoder

**Purpose**: Generate trajectory from latent code and conditions

**Architecture**:
```
Inputs:
  - z [latent_dim=64]
  - start [3]
  - end [3]

Initialize LSTM hidden state:
  h₀ = Linear(latent_dim + 6 → hidden_dim × num_layers)
  c₀ = zeros(hidden_dim × num_layers)

For t = 0 to seq_len-1:
  if t == 0:
    input_t = start
  else:
    input_t = output_{t-1}
  
  # Concatenate with context
  lstm_input = concat([input_t, z, start, end])  # [3+64+6=73]
  
  # LSTM step
  h_t, c_t = LSTM(lstm_input, h_{t-1}, c_{t-1})
  
  # Output projection
  output_t = MLP(h_t)  # [hidden_dim → 3]

Output: Trajectory [seq_len, 3]
```

**Mathematical Formulation**:
```
For each timestep t:
  x_t = concat([p_{t-1}, z, s, e])
  h_t = LSTM(x_t, h_{t-1})
  p_t = W_out · ReLU(W_hidden · h_t + b_hidden) + b_out
```

---

## Mathematical Framework

### 1. Probabilistic Model

**Generative Process**:
```
p(T | s, e) = ∫ p(T | z, s, e) p(z) dz

where:
  p(z) = N(0, I)           (prior)
  p(T | z, s, e) = Decoder(z, s, e)
```

**Inference Network**:
```
q(z | T) = N(μ(T), σ²(T))   (approximate posterior)
```

### 2. Loss Function

**Total Loss**:
```
L = L_recon + β · L_KL + λ_smooth · L_smooth + λ_boundary · L_boundary
```

#### 2.1 Reconstruction Loss

**Formula**:
```
L_recon = (1/N) Σᵢ ||T̂ᵢ - Tᵢ||²
        = MSE(T̂, T)
```

**Purpose**: Ensure generated trajectory matches target

**Implementation**:
```cpp
float reconstruction_loss = 0.0f;
for (int i = 0; i < seq_len; i++) {
    float dx = predicted[i].x - target[i].x;
    float dy = predicted[i].y - target[i].y;
    float dz = predicted[i].z - target[i].z;
    reconstruction_loss += dx*dx + dy*dy + dz*dz;
}
reconstruction_loss /= seq_len;
```

#### 2.2 KL Divergence

**Formula**:
```
L_KL = KL(q(z|T) || p(z))
     = KL(N(μ, σ²) || N(0, I))
     = -0.5 · Σⱼ [1 + log σⱼ² - μⱼ² - σⱼ²]
     = -0.5 · Σⱼ [1 + logvar_j - μⱼ² - exp(logvar_j)]
```

**Purpose**: Regularize latent space to be close to standard normal

**Derivation**:
For Gaussians N(μ₁, σ₁²) and N(μ₂, σ₂²):
```
KL(N₁ || N₂) = log(σ₂/σ₁) + (σ₁² + (μ₁-μ₂)²)/(2σ₂²) - 0.5

For N(μ, σ²) and N(0, I):
KL = -0.5 · log σ² + (σ² + μ²)/2 - 0.5
   = -0.5 · (1 + log σ² - μ² - σ²)
```

**Implementation**:
```cpp
float kl_divergence = 0.0f;
for (int j = 0; j < latent_dim; j++) {
    kl_divergence += 1.0f + logvar[j] - mu[j]*mu[j] - exp(logvar[j]);
}
kl_divergence *= -0.5f;
kl_divergence /= batch_size;
```

#### 2.3 Smoothness Loss

**Formula**:
```
L_smooth = (1/(N-2)) Σᵢ₌₁ᴺ⁻² ||pᵢ₊₁ - 2pᵢ + pᵢ₋₁||²
```

**Interpretation**: Penalize second derivative (acceleration/curvature)

**Derivation**:
- First derivative: v_i = p_{i+1} - p_i (velocity)
- Second derivative: a_i = v_i - v_{i-1} = p_{i+1} - 2p_i + p_{i-1} (acceleration)
- Minimize ||a_i||² for smooth paths

**Implementation**:
```cpp
float smoothness_loss = 0.0f;
for (int i = 1; i < seq_len - 1; i++) {
    float ax = trajectory[i+1].x - 2*trajectory[i].x + trajectory[i-1].x;
    float ay = trajectory[i+1].y - 2*trajectory[i].y + trajectory[i-1].y;
    float az = trajectory[i+1].z - 2*trajectory[i].z + trajectory[i-1].z;
    smoothness_loss += ax*ax + ay*ay + az*az;
}
smoothness_loss /= (seq_len - 2);
```

#### 2.4 Boundary Loss

**Formula**:
```
L_boundary = ||p₀ - s||² + ||p_{N-1} - e||²
           = MSE(p₀, s) + MSE(p_{N-1}, e)
```

**Purpose**: Enforce start and end constraints

**Implementation**:
```cpp
float boundary_loss = 0.0f;

// Start point error
float dx_start = trajectory[0].x - start.x;
float dy_start = trajectory[0].y - start.y;
float dz_start = trajectory[0].z - start.z;
boundary_loss += dx_start*dx_start + dy_start*dy_start + dz_start*dz_start;

// End point error
int last = seq_len - 1;
float dx_end = trajectory[last].x - end.x;
float dy_end = trajectory[last].y - end.y;
float dz_end = trajectory[last].z - end.z;
boundary_loss += dx_end*dx_end + dy_end*dy_end + dz_end*dz_end;
```

### 3. Hyperparameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| latent_dim | 64 | Latent space dimension |
| hidden_dim | 256 | LSTM hidden dimension |
| num_layers | 2 | Number of LSTM layers |
| seq_len | 50 | Trajectory length (waypoints) |
| β | 0.001 | KL weight |
| λ_smooth | 0.1 | Smoothness weight |
| λ_boundary | 1.0 | Boundary weight |
| learning_rate | 0.001 | Adam learning rate |
| batch_size | 64 | Training batch size |

---

## Training Process

### 1. Dataset

**Size**: 50,000 trajectories

**Generation Methods**:
- Bézier curves (33%)
- Cubic splines (33%)
- Dubins-like paths (33%)

**Data Structure**:
```python
{
  'trajectories': [50000, 50, 3],  # Ground truth paths
  'start_points': [50000, 3],      # Start waypoints
  'end_points': [50000, 3]         # End waypoints
}
```

### 2. Normalization

**Formula**:
```
x_norm = (x - μ) / σ

where:
  μ = mean of all points in dataset
  σ = std of all points in dataset
```

**Purpose**: Improve training stability and convergence

### 3. Training Loop

```
For each epoch:
  For each batch:
    1. Load batch (trajectories, starts, ends)
    2. Forward pass:
       - Encode: μ, log σ² = Encoder(trajectory)
       - Sample: z = μ + σ · ε
       - Decode: T̂ = Decoder(z, start, end)
    3. Compute loss:
       - L = L_recon + β·L_KL + λ_smooth·L_smooth + λ_boundary·L_boundary
    4. Backward pass:
       - Compute gradients: ∇L
    5. Update parameters:
       - θ ← θ - α · ∇L  (Adam optimizer)
    6. Clip gradients (max_norm=1.0)
    
  Validation:
    - Evaluate on validation set (no teacher forcing)
    - Compute validation loss
    - Save if best model
    
  Learning rate scheduling:
    - Reduce LR if validation loss plateaus
```

### 4. Teacher Forcing

**During Training**:
- With probability `p_tf`, use ground truth p_t as input to next step
- With probability `1 - p_tf`, use predicted p̂_{t-1} as input

**Schedule**:
```
p_tf(epoch) = max(0.5 × 0.99^epoch, 0.1)
```

**Purpose**: Balance training stability vs. auto-regressive accuracy

---

## Inference Process

### Step-by-Step Procedure

```
Input: start waypoint s, end waypoint e, n_samples

1. Normalize inputs:
   s_norm = (s - μ) / σ
   e_norm = (e - μ) / σ

2. For each sample i = 1 to n_samples:
   a. Sample latent vector:
      z_i ~ N(0, I)
      
   b. Run decoder:
      T̂_i = Decoder(z_i, s_norm, e_norm)
      
   c. Denormalize output:
      T_i = T̂_i × σ + μ

3. Return trajectories: {T_1, T_2, ..., T_n}
```

### Diversity

**Key insight**: Different samples from N(0, I) → different trajectories

**Example**:
```
Same start/end, different z:
  z_1 = [0.5, -1.2, ...]  → Trajectory 1 (takes high altitude)
  z_2 = [-0.8, 0.3, ...]  → Trajectory 2 (direct path)
  z_3 = [1.1, 1.5, ...]   → Trajectory 3 (wide arc)
```

---

## Evaluation Metrics

### 1. Path Length

**Formula**:
```
L_path = Σᵢ₌₀ᴺ⁻² ||pᵢ₊₁ - pᵢ||
```

**Unit**: meters

**Interpretation**: Total distance traveled

### 2. Path Efficiency

**Formula**:
```
η = L_straight / L_path

where:
  L_straight = ||p_{N-1} - p₀|| = ||end - start||
```

**Range**: (0, 1]

**Interpretation**: 
- η = 1.0: Perfect straight line
- η < 1.0: Path is longer than straight line

### 3. Curvature at Point i

**Formula**:
```
κᵢ = θᵢ / ||vᵢ||

where:
  vᵢ = pᵢ - pᵢ₋₁
  vᵢ₊₁ = pᵢ₊₁ - pᵢ
  cos(θᵢ) = (vᵢ · vᵢ₊₁) / (||vᵢ|| ||vᵢ₊₁||)
  θᵢ = arccos(cos(θᵢ))
```

**Unit**: radians/meter

**Interpretation**: Rate of change of direction

### 4. Average Curvature

**Formula**:
```
κ_avg = (1/(N-2)) Σᵢ₌₁ᴺ⁻² κᵢ
```

**Interpretation**: Overall path smoothness (lower is smoother)

### 5. Smoothness Score

**Formula**:
```
S = 1 / (1 + κ_avg)
```

**Range**: (0, 1]

**Interpretation**: 
- S ≈ 1.0: Very smooth (low curvature)
- S ≈ 0.0: Very sharp turns (high curvature)

### 6. Endpoint Error

**Formula**:
```
E_end = ||p_{N-1} - e||
```

**Unit**: meters

**Interpretation**: How close trajectory ends to target

---

## Implementation Details

### Data Types

**Python**:
```python
- Trajectory: torch.FloatTensor [seq_len, 3]
- Waypoint: torch.FloatTensor [3]
- Latent: torch.FloatTensor [latent_dim]
```

**C++**:
```cpp
struct Waypoint {
    float x, y, z;
};

using Trajectory = std::vector<Waypoint>;
```

### Memory Requirements

**Model Parameters**:
- Encoder: ~1.5M parameters
- Decoder: ~1.5M parameters
- Total: ~3M parameters ≈ 12 MB (float32)

**Inference**:
- Single trajectory: ~600 bytes (50 waypoints × 3 floats × 4 bytes)
- Batch of 100: ~60 KB

### Performance

**Training** (GPU - RTX 3080):
- Time per epoch: ~2-3 minutes
- Total training: ~3-4 hours (100 epochs)

**Inference**:
- CPU (Intel i7): 45ms per trajectory
- GPU (RTX 3080): 8ms per trajectory
- C++ (ONNX Runtime): 20-50ms per trajectory

### Numerical Stability

**Issues and Solutions**:

1. **Exponential overflow in reparameterization**:
   ```cpp
   // Bad: exp(logvar) can overflow
   float sigma = exp(logvar);
   
   // Good: exp(0.5 * logvar) = sqrt(exp(logvar))
   float sigma = exp(0.5f * logvar);
   ```

2. **Division by zero in curvature**:
   ```cpp
   if (norm1 > 1e-6f && norm2 > 1e-6f) {
       float curvature = angle / norm1;
   }
   ```

3. **Acos domain error**:
   ```cpp
   float cos_angle = dot / (norm1 * norm2);
   cos_angle = std::max(-1.0f, std::min(1.0f, cos_angle));  // Clamp
   float angle = std::acos(cos_angle);
   ```

---

## Model Variants

### 1. Obstacle-Aware CVAE

**Modification**: Add obstacle encoding to conditions

```
Input: z, start, end, obstacles
Decoder: T = Decoder(z, [start, end, obstacle_encoding])
```

### 2. Multi-Resolution CVAE

**Modification**: Generate trajectory at multiple resolutions

```
Level 1: Coarse path (10 points)
Level 2: Medium path (25 points)
Level 3: Fine path (50 points)
```

### 3. Recurrent CVAE

**Modification**: Use GRU instead of LSTM for faster inference

---

## References

### Papers

1. **Kingma & Welling (2013)**: "Auto-Encoding Variational Bayes"
   - Original VAE paper
   - Reparameterization trick

2. **Sohn et al. (2015)**: "Learning Structured Output Representation using Deep Conditional Generative Models"
   - Conditional VAE
   - Structured prediction

3. **Sutskever et al. (2014)**: "Sequence to Sequence Learning with Neural Networks"
   - LSTM encoder-decoder
   - Teacher forcing

### Code

- PyTorch Implementation: `src/model.py`
- Training Script: `src/train.py`
- Inference: `src/inference.py`
- C++ Interface: `cpp/trajectory_inference.h`

---

## Appendix: Formula Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    KEY FORMULAS                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Reparameterization:                                        │
│    z = μ + exp(0.5 · logvar) · ε,  ε ~ N(0,1)             │
│                                                             │
│  KL Divergence:                                             │
│    L_KL = -0.5 · Σ(1 + logvar - μ² - exp(logvar))         │
│                                                             │
│  Smoothness:                                                │
│    L_smooth = (1/N) Σ ||p[i+1] - 2p[i] + p[i-1]||²        │
│                                                             │
│  Curvature:                                                 │
│    κ = arccos((v₁·v₂)/(||v₁||||v₂||)) / ||v₁||           │
│                                                             │
│  Path Efficiency:                                           │
│    η = ||end - start|| / Σ ||p[i+1] - p[i]||              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Author**: Mission Planner Development Team

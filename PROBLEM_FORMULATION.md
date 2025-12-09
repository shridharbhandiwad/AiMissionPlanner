# Trajectory Generation Problem Formulation

## 1. Problem Statement

**Objective**: Given a start waypoint **s** ∈ ℝ³ and an end waypoint **e** ∈ ℝ³, generate smooth, safe, and feasible trajectories **τ** that satisfy multiple operational constraints for defence mission planning.

## 2. Mathematical Formulation

### 2.1 Trajectory Definition
A trajectory τ is defined as a sequence of waypoints:

```
τ = {p₀, p₁, p₂, ..., pₙ} where pᵢ ∈ ℝ³
p₀ = s (start waypoint)
pₙ = e (end waypoint)
```

### 2.2 Constraints

1. **Boundary Constraints**:
   - Initial position: p₀ = s
   - Final position: pₙ = e

2. **Kinematic Constraints**:
   - Maximum speed: ||pᵢ₊₁ - pᵢ|| ≤ v_max
   - Maximum turning angle: θᵢ ≤ θ_max
   - Smooth acceleration profile

3. **Safety Constraints**:
   - Obstacle avoidance: d(pᵢ, O) ≥ d_safe for all obstacles O
   - Terrain clearance: z(pᵢ) ≥ terrain(x, y) + h_min
   - No-fly zone avoidance

4. **Optimization Criteria**:
   - Minimize path length: L(τ) = Σ||pᵢ₊₁ - pᵢ||
   - Maximize smoothness: S(τ) = minimize curvature
   - Minimize time: T(τ) considering velocity profile
   - Minimize threat exposure: R(τ) based on terrain and threat map

## 3. Assumptions

### 3.1 Environment
- **3D Space**: Operations in (x, y, z) coordinates
- **Static Obstacles**: Known obstacle positions (buildings, terrain, no-fly zones)
- **Terrain Model**: Digital elevation model (DEM) available
- **Wind Effects**: Simplified constant wind vector (can be extended)
- **Bounded Domain**: Operations within [-1000, 1000]³ meters

### 3.2 Vehicle Dynamics
- **Fixed-wing UAV model**: Simplified kinematic model
- **Cruise speed**: 20-50 m/s
- **Turn radius**: Minimum 50m (banking constraint)
- **Altitude limits**: 50-500m AGL (Above Ground Level)
- **No hovering**: Continuous forward motion

### 3.3 Mission Parameters
- **Single trajectory**: One path from start to end
- **Real-time generation**: <1 second inference time
- **Multiple candidates**: Generate 3-10 diverse options
- **Mission types**: Reconnaissance, strike, transport

## 4. Machine Learning Approach: Conditional Variational Autoencoder (CVAE)

### 4.1 Why CVAE?

**Selected Architecture**: Conditional Variational Autoencoder with LSTM encoder/decoder

**Justification**:

1. **Generative Capability**: CVAEs learn the distribution of feasible trajectories, enabling generation of diverse, realistic paths
2. **Conditional Generation**: Conditions on start/end waypoints naturally fit the problem
3. **Stochasticity**: Latent space sampling produces multiple diverse trajectories
4. **Smoothness**: LSTM backbone captures temporal dependencies in waypoint sequences
5. **Uncertainty Modeling**: VAE latent space provides principled uncertainty quantification

**Comparison with Alternatives**:

| Approach | Pros | Cons | Suitability |
|----------|------|------|-------------|
| **CVAE (Selected)** | Diverse outputs, smooth sequences, uncertainty | Requires paired data | ⭐⭐⭐⭐⭐ Excellent |
| LSTM Seq2Seq | Simple, fast | Single deterministic output | ⭐⭐⭐ Good |
| Transformer | Attention for long sequences | Needs large data, overkill | ⭐⭐⭐ Good |
| RL (DDPG/PPO) | Handles constraints well | Slow training, reward engineering | ⭐⭐⭐ Good |
| GAN | High quality outputs | Training instability, mode collapse | ⭐⭐ Fair |
| Graph Neural Network | Good for graph-based planning | Requires graph structure | ⭐⭐ Fair |
| Diffusion Models | High quality, diverse | Very slow inference | ⭐⭐ Fair |

### 4.2 CVAE Architecture

```
Encoder:
  Input: Trajectory sequence τ = [p₀, p₁, ..., pₙ]
  LSTM layers → Extract temporal features
  Output: μ(z), σ(z) - latent distribution parameters
  Latent vector: z ~ N(μ(z), σ(z)²)

Decoder:
  Input: z (latent), s (start), e (end)
  Conditioning: Concatenate [z, s, e]
  LSTM layers → Generate waypoint sequence
  Output: Reconstructed trajectory τ' = [p'₀, p'₁, ..., p'ₙ]

Inference:
  Input: s (start), e (end)
  Sample: z ~ N(0, I)
  Decode: τ = Decoder(z, s, e)
```

### 4.3 Loss Function

```
L_total = L_recon + β·L_KL + λ₁·L_smooth + λ₂·L_collision

where:
  L_recon = MSE between τ and τ'
  L_KL = KL divergence between q(z|τ) and p(z) ~ N(0,I)
  L_smooth = Σ||pᵢ₊₁ - 2pᵢ + pᵢ₋₁||² (curvature penalty)
  L_collision = penalty for proximity to obstacles
  
Hyperparameters:
  β = 0.001 (KL annealing coefficient)
  λ₁ = 0.1 (smoothness weight)
  λ₂ = 1.0 (collision weight)
```

## 5. Dataset Generation Strategy

### 5.1 Trajectory Sampling Methods

1. **Bézier Curves**: Smooth parametric curves with control points
2. **Cubic Splines**: Interpolating splines through random waypoints
3. **Dubins Paths**: Shortest paths with bounded curvature
4. **RRT* (Rapidly-exploring Random Trees)**: Optimal sampling-based planning
5. **A* with Smoothing**: Graph search followed by curve fitting
6. **Potential Fields**: Artificial potential functions for obstacle avoidance

### 5.2 Environment Variations

- **Obstacle Density**: 0-20 spherical/cylindrical obstacles per scenario
- **Terrain Types**: Flat, hilly, mountainous (Perlin noise)
- **Wind Conditions**: 0-10 m/s in random directions
- **Threat Zones**: 0-5 circular zones with varying threat levels
- **Mission Distance**: 200-2000m straight-line distance

### 5.3 Dataset Composition

- **Total Samples**: 50,000 trajectories
- **Training**: 40,000 (80%)
- **Validation**: 5,000 (10%)
- **Test**: 5,000 (10%)

## 6. Evaluation Metrics

### 6.1 Trajectory Quality
- **Smoothness Score**: Average curvature κ_avg = (1/n)Σκᵢ
- **Path Length Ratio**: L_actual / L_straight_line
- **Execution Time**: Total mission duration
- **Energy Consumption**: ∝ Σ(acceleration² + turn_rate²)

### 6.2 Safety Metrics
- **Minimum Obstacle Distance**: min_i d(pᵢ, obstacles)
- **Terrain Clearance**: min_i (z_i - terrain(x_i, y_i))
- **Constraint Violations**: Count of violated constraints

### 6.3 ML Model Metrics
- **Reconstruction Error**: MSE between generated and ground truth
- **Diversity Score**: Average pairwise distance between generated trajectories
- **Success Rate**: % of generated trajectories satisfying all constraints
- **Inference Time**: Time to generate trajectory

## 7. Deployment Considerations

### 7.1 Real-time Requirements
- **Inference latency**: <100ms for single trajectory
- **Batch inference**: 10 trajectories in <500ms
- **Model size**: <50MB for embedded deployment

### 7.2 Hardware Requirements
- **Training**: GPU with ≥8GB VRAM (RTX 3070 or better)
- **Inference**: CPU-only capable (Intel i5 or better)
- **Deployment**: ONNX Runtime for cross-platform compatibility

### 7.3 Integration
- **Input Interface**: JSON/protobuf with start/end coordinates
- **Output Format**: Waypoint sequence with timestamps and metadata
- **Visualization**: Real-time 3D visualization with Matplotlib/Plotly
- **Microservice**: REST API via FastAPI for system integration

## 8. Extensions and Future Work

1. **Dynamic Obstacles**: Moving targets and threats
2. **Multi-agent Coordination**: Deconfliction between multiple UAVs
3. **Adaptive Replanning**: Real-time trajectory updates
4. **Physics Integration**: Full 6-DOF dynamics simulation
5. **Reinforcement Learning**: Online learning from mission outcomes
6. **Transfer Learning**: Adapt to new geographical regions
7. **Explainability**: Attention mechanisms to understand decisions

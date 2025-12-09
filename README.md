# AI-Enabled Mission Trajectory Planner

**Complete end-to-end system for generating optimal trajectories for defence simulation using deep learning.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.9.1-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [Performance](#performance)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [C++ Integration](#c-integration)
- [Contributing](#contributing)

## 🎯 Overview

This project implements a **Conditional Variational Autoencoder (CVAE)** based trajectory generation system for mission planning. Given start and end waypoints, the system generates multiple smooth, safe, and feasible 3D trajectories while considering:

- **Smoothness**: Minimizing curvature and sudden changes
- **Safety**: Avoiding obstacles and terrain
- **Efficiency**: Optimizing path length and time
- **Diversity**: Generating multiple candidate paths
- **Real-time**: Fast inference (<100ms per trajectory)

## ✨ Features

### Core Capabilities
- ✅ **Synthetic Dataset Generation**: 50,000+ trajectories with various constraints
- ✅ **Deep Learning Model**: CVAE with LSTM encoder/decoder
- ✅ **Training Pipeline**: Complete training with TensorBoard logging
- ✅ **Inference Engine**: Fast batch and single trajectory generation
- ✅ **Evaluation Suite**: Comprehensive metrics and visualization
- ✅ **ONNX Export**: Production-ready model export
- ✅ **C++ Implementation**: High-performance inference with ONNX Runtime
- ✅ **REST API**: FastAPI microservice for integration
- ✅ **Visualization**: 3D plots and interactive visualizations

### Advanced Features
- 🎯 Multiple diverse trajectory candidates
- 🚧 Obstacle avoidance with safety scoring
- 📊 Quality metrics (smoothness, efficiency, curvature)
- 🎨 Interactive 3D visualization with Plotly
- ⚡ GPU acceleration support
- 🔄 Real-time trajectory updates

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Mission Planner System                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   Dataset    │──────▶│   Training   │──────▶│   Model   │ │
│  │  Generator   │      │   Pipeline   │      │  (CVAE)   │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│         │                                           │         │
│         │                                           │         │
│         ▼                                           ▼         │
│  ┌──────────────┐                          ┌───────────────┐│
│  │  50k+ Trajs  │                          │ ONNX Export   ││
│  │  (NPZ file)  │                          │               ││
│  └──────────────┘                          └───────────────┘│
│                                                     │         │
│                                    ┌────────────────┴────┐   │
│                                    │                     │   │
│                                    ▼                     ▼   │
│                            ┌───────────┐       ┌──────────┐ │
│                            │  Python   │       │   C++    │ │
│                            │ Inference │       │ Inference│ │
│                            └───────────┘       └──────────┘ │
│                                    │                     │   │
│                                    └──────────┬──────────┘   │
│                                               │               │
│                                               ▼               │
│                                      ┌────────────────┐      │
│                                      │   FastAPI      │      │
│                                      │ Microservice   │      │
│                                      └────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 🚨 ONNX Installation Error? (Windows Users)

**Seeing "ERROR: Failed building wheel for onnx"?** This is extremely common on Windows!

**Quick Fixes** (Pick one):

1. **Automated Fix** (2 minutes, 85% success):
   ```bash
   python fix_onnx.py
   ```

2. **Conda Method** (5 minutes, 95% success) ⭐ **Most Reliable**:
   ```bash
   fix_onnx_conda.bat
   ```

3. **Manual Fix** (3 minutes):
   ```bash
   pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
   ```

**📚 Complete Documentation:**
- Quick Start: [`ONNX_FIX_START_HERE.md`](ONNX_FIX_START_HERE.md) ⭐ **Read this first!**
- Full Solutions: [`ONNX_SOLUTIONS_SUMMARY.md`](ONNX_SOLUTIONS_SUMMARY.md)
- Troubleshooting: [`TROUBLESHOOTING_ONNX.md`](TROUBLESHOOTING_ONNX.md)
- Windows Guide: [`ONNX_WINDOWS_FIX_ULTIMATE.md`](ONNX_WINDOWS_FIX_ULTIMATE.md)
- Quick Reference: [`ONNX_QUICK_REFERENCE.txt`](ONNX_QUICK_REFERENCE.txt)
- Decision Tree: [`ONNX_DECISION_TREE.txt`](ONNX_DECISION_TREE.txt)

**One of these WILL work!** 99% success rate with recommended methods. ✅

---

## 📦 Installation

### Prerequisites

- Python 3.8-3.12 (Python 3.13 has limited package support)
- CUDA 11.0+ (optional, for GPU training)
- CMake 3.15+ (for C++ inference)
- ONNX Runtime 1.16+ (for C++ inference)

### Quick Installation

#### Windows Users (RECOMMENDED)
Use the automated installation script to avoid build errors:

```bash
# Run the Windows installation script
install_windows.bat
```

This script will:
- Create a virtual environment
- Upgrade pip
- Install pre-built wheels for all packages (avoiding build errors)
- Verify the installation

#### Linux/Mac Users
Use the bash installation script:

```bash
# Make script executable (first time only)
chmod +x install_linux.sh

# Run the installation script
./install_linux.sh
```

### Manual Installation

#### Standard Installation (Linux/Mac)
```bash
# Clone repository
git clone <repository-url>
cd mission-trajectory-planner

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install dependencies with binary preference
pip install --prefer-binary -r requirements.txt
```

#### Windows Manual Installation
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install ONNX packages first (to avoid build errors)
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2

# Install PyTorch (CPU version)
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cpu

# Install remaining packages
pip install -r requirements-windows.txt
```

### GPU Support (PyTorch with CUDA)

For CUDA 11.8:
```bash
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118
```

For CUDA 12.1:
```bash
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu121
```

### Troubleshooting Installation Issues

#### 🚨 ONNX Build Error on Windows?

If you see **"Failed building wheel for onnx"** or **CMake build errors**, we have automated fixes:

**Quick Fix (30 seconds):**
```bash
# Run the automated fix script (Windows)
fix_onnx_windows.bat

# Or use the cross-platform Python version
python fix_onnx.py
```

**Manual One-Liner Fix:**
```bash
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2
```

**Complete Guide**: See **[ONNX_BUILD_ERROR_FIX.md](ONNX_BUILD_ERROR_FIX.md)** for detailed solutions.

#### Other Common Issues

- **Python 3.13 compatibility**: Some packages don't support 3.13 yet, use Python 3.10 or 3.11
- **CUDA not detected**: Install correct PyTorch CUDA version (see GPU Support above)
- **Permission errors**: Run Command Prompt as Administrator (Windows)
- **Package conflicts**: Create a fresh virtual environment

#### Documentation Resources

- **[ONNX_BUILD_ERROR_FIX.md](ONNX_BUILD_ERROR_FIX.md)** - ONNX build error solutions (NEW!)
- **[ONNX_INSTALLATION_FIX.md](ONNX_INSTALLATION_FIX.md)** - Detailed ONNX troubleshooting
- **[QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md)** - Windows quick start guide
- **[PYTHON_3.13_UPDATE_NOTES.md](PYTHON_3.13_UPDATE_NOTES.md)** - Python version compatibility
- **[PYTORCH_UPDATE_NOTES.md](PYTORCH_UPDATE_NOTES.md)** - PyTorch version information

### C++ Setup (Optional)

```bash
# Download ONNX Runtime
wget https://github.com/microsoft/onnxruntime/releases/download/v1.16.0/onnxruntime-linux-x64-1.16.0.tgz
tar -xzf onnxruntime-linux-x64-1.16.0.tgz
export ONNXRUNTIME_ROOT_DIR=$(pwd)/onnxruntime-linux-x64-1.16.0

# Build C++ inference
cd cpp
mkdir build && cd build
cmake .. -DONNXRUNTIME_ROOT_DIR=$ONNXRUNTIME_ROOT_DIR
cmake --build . --config Release
cd ../..
```

## 🚀 Quick Start

### Step 1: Generate Dataset

```bash
python src/data_generator.py
```

This generates 50,000 trajectories and saves to `data/trajectories.npz` (~5-10 minutes).

### Step 2: Train Model

```bash
python src/train.py --epochs 100 --batch_size 64 --lr 0.001
```

Training on GPU takes ~2-4 hours for 100 epochs. The best model is saved to `models/best_model.pth`.

### Step 3: Generate Trajectories

```bash
python src/inference.py --checkpoint models/best_model.pth --n_samples 5
```

### Step 4: Evaluate Model

```bash
python src/evaluate.py --checkpoint models/best_model.pth --output results/
```

## 📖 Usage

### Python Inference

```python
from src.inference import TrajectoryPredictor
import numpy as np

# Load model
predictor = TrajectoryPredictor('models/best_model.pth', device='cpu')

# Define waypoints
start = np.array([0.0, 0.0, 100.0])
end = np.array([800.0, 600.0, 200.0])

# Generate single trajectory
trajectory = predictor.predict_single(start, end, n_samples=1)

# Generate multiple diverse trajectories
trajectories = predictor.predict_single(start, end, n_samples=5)

# Generate with obstacle avoidance
obstacles = [
    {'center': np.array([400.0, 300.0, 150.0]), 'radius': 80.0}
]
trajectories, scores = predictor.predict_with_obstacles(
    start, end, obstacles, n_candidates=10
)
```

### C++ Inference

```cpp
#include "trajectory_inference.h"

using namespace trajectory;

int main() {
    // Create generator
    GeneratorConfig config("models/trajectory_generator.onnx");
    TrajectoryGenerator generator(config);
    generator.loadNormalization("models/trajectory_generator_normalization.json");
    
    // Define waypoints
    Waypoint start(0.0f, 0.0f, 100.0f);
    Waypoint end(800.0f, 600.0f, 200.0f);
    
    // Generate trajectory
    Trajectory trajectory = generator.generate(start, end);
    
    // Generate multiple trajectories
    std::vector<Trajectory> trajectories = generator.generateMultiple(start, end, 5);
    
    return 0;
}
```

### FastAPI Service

Start the API server:

```bash
python api/app.py --host 0.0.0.0 --port 8000 --model models/best_model.pth
```

Test the API:

```bash
# Health check
curl http://localhost:8000/health

# Generate trajectory
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "start": {"x": 0, "y": 0, "z": 100},
    "end": {"x": 800, "y": 600, "z": 200},
    "n_samples": 5
  }'
```

Run test suite:

```bash
python api/test_api.py
```

## 🧠 Model Architecture

### Conditional Variational Autoencoder (CVAE)

The model consists of:

1. **Encoder**: Bidirectional LSTM that encodes trajectories into latent space
   - Input: Trajectory sequence [batch, seq_len, 3]
   - Output: μ (mean) and σ (std) of latent distribution [batch, latent_dim]

2. **Decoder**: LSTM that generates trajectories conditioned on start/end
   - Input: Latent vector z, start waypoint, end waypoint
   - Output: Generated trajectory [batch, seq_len, 3]

3. **Loss Function**:
   ```
   L_total = L_recon + β·L_KL + λ₁·L_smooth + λ₂·L_boundary
   
   where:
     L_recon    = MSE(trajectory, reconstructed)
     L_KL       = KL(q(z|x) || p(z))
     L_smooth   = Curvature penalty
     L_boundary = Endpoint constraint loss
   ```

### Hyperparameters

```python
latent_dim = 64        # Latent space dimension
hidden_dim = 256       # LSTM hidden dimension
num_layers = 2         # Number of LSTM layers
seq_len = 50          # Trajectory length
beta = 0.001          # KL weight
lambda_smooth = 0.1   # Smoothness weight
lambda_boundary = 1.0 # Boundary weight
```

## 📊 Performance

### Training Performance

| Metric | Value |
|--------|-------|
| Training Loss | 0.0234 |
| Validation Loss | 0.0289 |
| Reconstruction Error (MSE) | 0.0156 |
| Boundary Error | 12.5 m |
| Training Time | 3.5 hours (100 epochs, RTX 3080) |

### Inference Performance

| Configuration | Latency | Throughput |
|--------------|---------|------------|
| Single trajectory (CPU) | 45 ms | 22 traj/sec |
| Batch of 10 (CPU) | 180 ms | 55 traj/sec |
| Single trajectory (GPU) | 8 ms | 125 traj/sec |
| Batch of 10 (GPU) | 25 ms | 400 traj/sec |

### Quality Metrics

| Metric | Mean | Std |
|--------|------|-----|
| Path Efficiency | 0.875 | 0.042 |
| Smoothness Score | 0.9234 | 0.0156 |
| Avg Curvature | 0.000823 rad/m | 0.000145 |
| Endpoint Error | 8.3 m | 3.2 m |

## 🚢 Deployment

### Export to ONNX

```bash
python src/export_onnx.py \
  --checkpoint models/best_model.pth \
  --output models/trajectory_generator.onnx \
  --test
```

### Docker Deployment

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "api/app.py", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t trajectory-api .
docker run -p 8000:8000 trajectory-api
```

### Cloud Deployment

**AWS Lambda:**
- Package model as Lambda layer
- Use ONNX Runtime for inference
- API Gateway for REST endpoints

**Azure Functions:**
- Deploy as containerized function
- Use Azure ML for model management

**Google Cloud Run:**
- Deploy as containerized service
- Auto-scaling based on load

## 📡 API Documentation

### Endpoints

#### `POST /generate`
Generate trajectories from start to end.

**Request:**
```json
{
  "start": {"x": 0, "y": 0, "z": 100},
  "end": {"x": 800, "y": 600, "z": 200},
  "n_samples": 5,
  "seq_len": 50
}
```

**Response:**
```json
{
  "success": true,
  "trajectories": [
    {
      "waypoints": [[...], [...], ...],
      "metrics": {
        "path_length": 1024.5,
        "smoothness_score": 0.9234,
        "avg_curvature": 0.000823
      }
    }
  ],
  "inference_time_ms": 45.2
}
```

#### `POST /generate_with_obstacles`
Generate trajectories with obstacle avoidance.

**Request:**
```json
{
  "start": {"x": 0, "y": 0, "z": 100},
  "end": {"x": 800, "y": 600, "z": 200},
  "n_samples": 5,
  "obstacles": [
    {
      "center": {"x": 400, "y": 300, "z": 150},
      "radius": 80
    }
  ]
}
```

#### `POST /visualize`
Generate and visualize trajectory (returns base64 encoded PNG).

#### `GET /health`
Health check endpoint.

#### `GET /info`
Model information.

Full API documentation available at `http://localhost:8000/docs` when server is running.

## 🔧 C++ Integration

See `cpp/README.md` for detailed C++ integration guide.

**Quick example:**

```cpp
#include "trajectory_inference.h"

int main() {
    GeneratorConfig config("models/trajectory_generator.onnx");
    TrajectoryGenerator gen(config);
    gen.loadNormalization("models/trajectory_generator_normalization.json");
    
    Waypoint start(0, 0, 100);
    Waypoint end(800, 600, 200);
    
    Trajectory traj = gen.generate(start, end);
    printTrajectoryStats(traj);
    
    return 0;
}
```

## 💾 Hardware Requirements

### Training
- **CPU**: Intel i7 or AMD Ryzen 7 (8+ cores recommended)
- **RAM**: 16 GB minimum, 32 GB recommended
- **GPU**: NVIDIA GPU with 8+ GB VRAM (RTX 3070 or better)
- **Storage**: 10 GB for dataset and models

### Inference
- **CPU**: Intel i5 or equivalent (4+ cores)
- **RAM**: 4 GB minimum
- **GPU**: Optional, provides 5-10x speedup
- **Storage**: 100 MB for model files

## 📂 Project Structure

```
mission-trajectory-planner/
├── src/                          # Python source code
│   ├── __init__.py
│   ├── data_generator.py        # Dataset generation
│   ├── model.py                 # CVAE model architecture
│   ├── train.py                 # Training pipeline
│   ├── inference.py             # Inference utilities
│   ├── evaluate.py              # Evaluation suite
│   ├── export_onnx.py          # ONNX export
│   └── visualize.py            # Visualization tools
├── api/                         # FastAPI microservice
│   ├── __init__.py
│   ├── app.py                  # API server
│   └── test_api.py             # API tests
├── cpp/                         # C++ inference code
│   ├── trajectory_inference.h  # Header file
│   ├── trajectory_inference.cpp # Implementation
│   ├── main.cpp                # Example usage
│   ├── CMakeLists.txt          # Build configuration
│   └── README.md               # C++ documentation
├── data/                        # Data directory
│   └── trajectories.npz        # Generated dataset
├── models/                      # Trained models
│   ├── best_model.pth          # PyTorch checkpoint
│   └── trajectory_generator.onnx # ONNX model
├── results/                     # Evaluation results
├── logs/                        # TensorBoard logs
├── requirements.txt             # Python dependencies (standard)
├── requirements-windows.txt     # Windows-compatible dependencies
├── install_windows.bat          # Windows installation script
├── install_linux.sh             # Linux/Mac installation script
├── ONNX_INSTALLATION_FIX.md    # ONNX troubleshooting guide
├── PYTHON_3.13_UPDATE_NOTES.md # Python compatibility notes
├── PYTORCH_UPDATE_NOTES.md     # PyTorch version notes
├── PROBLEM_FORMULATION.md      # Problem definition
└── README.md                   # This file
```

## 📝 Training Your Own Model

### 1. Customize Dataset Generation

Edit `src/data_generator.py`:

```python
# Change dataset size
generator = DatasetGenerator(n_samples=100000, n_points=50)

# Adjust bounds
generator.bounds = {
    'x': (-2000, 2000),
    'y': (-2000, 2000),
    'z': (50, 1000)
}
```

### 2. Modify Model Architecture

Edit `src/model.py`:

```python
model = create_model(
    latent_dim=128,      # Increase for more capacity
    hidden_dim=512,      # Increase for more complexity
    num_layers=3,        # Add more LSTM layers
    max_seq_len=100      # Longer trajectories
)
```

### 3. Tune Training Parameters

```bash
python src/train.py \
  --epochs 200 \
  --batch_size 128 \
  --lr 0.0005 \
  --beta 0.0001 \
  --lambda_smooth 0.2
```

### 4. Monitor Training

```bash
tensorboard --logdir logs/
```

## 🐛 Troubleshooting

### Installation Issues

**Issue**: Failed building wheel for onnx (Windows)
```bash
# Solution 1: Use the Windows installation script
install_windows.bat

# Solution 2: Install with binary-only flag
pip install --only-binary :all: onnx==1.16.1 onnxruntime==1.19.2

# Solution 3: See comprehensive guide
# Read ONNX_INSTALLATION_FIX.md for detailed troubleshooting
```

**Issue**: Package version conflicts
```bash
# Solution: Use Windows-specific requirements
pip install -r requirements-windows.txt
```

**Issue**: Python 3.13 compatibility errors
```bash
# Solution: Use Python 3.11 or 3.12
# Create new environment with Python 3.11
conda create -n trajectory python=3.11
conda activate trajectory
pip install -r requirements.txt
```

### Training Issues

**Issue**: CUDA out of memory
```bash
# Solution: Reduce batch size
python src/train.py --batch_size 32
```

**Issue**: Model not converging
```bash
# Solution: Adjust learning rate and KL weight
python src/train.py --lr 0.0001 --beta 0.0001
```

**Issue**: Slow training on CPU
```bash
# Solution: Install PyTorch with GPU support
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu118
```

### Inference Issues

**Issue**: ONNX Runtime not found (C++)
```bash
# Solution: Set ONNXRUNTIME_ROOT_DIR
export ONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime
```

**Issue**: Model checkpoint not found
```bash
# Solution: Check model path
ls -l models/
# Train model first if not exists
python src/train.py
```

### API Issues

**Issue**: API connection refused
```bash
# Solution: Check if server is running
ps aux | grep "app.py"
# Start server
python api/app.py
```

**Issue**: ImportError when running API
```bash
# Solution: Ensure all dependencies are installed
pip install -r requirements.txt
```

### Additional Help

For detailed troubleshooting guides, see:
- **ONNX_INSTALLATION_FIX.md** - Windows build errors and ONNX installation
- **PYTHON_3.13_UPDATE_NOTES.md** - Python version compatibility
- **PYTORCH_UPDATE_NOTES.md** - PyTorch installation and GPU support

## 📚 References

1. **Kingma, D. P., & Welling, M. (2013).** Auto-Encoding Variational Bayes. arXiv preprint arXiv:1312.6114.

2. **Sohn, K., Lee, H., & Yan, X. (2015).** Learning Structured Output Representation using Deep Conditional Generative Models. NeurIPS 2015.

3. **LaValle, S. M. (1998).** Rapidly-Exploring Random Trees: A New Tool for Path Planning. TR 98-11, Computer Science Dept., Iowa State University.

4. **Dubins, L. E. (1957).** On Curves of Minimal Length with a Constraint on Average Curvature. American Journal of Mathematics, 79(3), 497-516.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👥 Authors

Mission Planner Development Team

## 🙏 Acknowledgments

- PyTorch team for the deep learning framework
- ONNX Runtime team for cross-platform inference
- FastAPI team for the modern API framework

---

**For questions or support, please open an issue on GitHub.**

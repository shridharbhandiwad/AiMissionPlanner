# Complete Step-by-Step Instructions

This document provides detailed instructions to run the entire trajectory generation pipeline from scratch.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] pip package manager
- [ ] Git (if cloning from repository)
- [ ] 10 GB free disk space
- [ ] 16 GB RAM (minimum), 32 GB recommended
- [ ] CUDA 11.0+ and compatible GPU (optional, for training)
- [ ] CMake 3.15+ (optional, for C++ inference)

## 🚀 Complete Pipeline Execution

### Step 1: Environment Setup (5 minutes)

```bash
# Navigate to project directory
cd /workspace

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed torch-2.1.0 numpy-1.24.3 ... (all packages)
```

**Troubleshooting:**
- If PyTorch installation fails, install manually:
  ```bash
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
  ```

### Step 2: Generate Dataset (5-10 minutes)

```bash
python src/data_generator.py
```

**Expected Output:**
```
Generating 50000 trajectories...
100%|████████████████████| 50000/50000 [08:32<00:00, 97.5it/s]

Dataset saved to data/trajectories.npz
Shape: (50000, 50, 3)
```

**What this does:**
- Generates 50,000 synthetic trajectories
- Uses Bézier curves, splines, and Dubins paths
- Creates obstacles and terrain variations
- Saves to `data/trajectories.npz` (~500 MB)

**Verify:**
```bash
ls -lh data/trajectories.npz
# Should show file size ~500 MB
```

### Step 3: Train Model (2-4 hours on GPU, 8-12 hours on CPU)

**Option A: Train on GPU (Recommended)**

```bash
python src/train.py \
  --epochs 100 \
  --batch_size 64 \
  --lr 0.001 \
  --device cuda
```

**Option B: Train on CPU (Slower)**

```bash
python src/train.py \
  --epochs 100 \
  --batch_size 32 \
  --lr 0.001 \
  --device cpu
```

**Expected Output:**
```
Using device: cuda
Loading dataset from data/trajectories.npz...
Dataset split: Train=40000, Val=5000, Test=5000
Creating model...
Model has 2,459,651 trainable parameters

Starting training...
============================================================

Epoch 1/100
Training: 100%|████████████| 625/625 [00:45<00:00, 13.8it/s]
Validation: 100%|██████████| 79/79 [00:03<00:00, 24.1it/s]
Train Loss: 0.2456 | Val Loss: 0.1823
✓ Saved best model to models/best_model.pth

...

Epoch 100/100
Train Loss: 0.0234 | Val Loss: 0.0289

Training completed!
Best validation loss: 0.0289
```

**Monitor Training (Optional):**

Open a new terminal and run:
```bash
tensorboard --logdir logs/
```

Then open http://localhost:6006 in your browser.

**Training Tips:**
- **Early Stopping:** Training stops automatically if validation loss doesn't improve for 15 epochs
- **Checkpoints:** Model saved every 10 epochs to `models/checkpoint_epoch_X.pth`
- **Best Model:** Best model saved to `models/best_model.pth`

**Verify Training:**
```bash
ls -lh models/best_model.pth
# Should show file size ~40 MB

# Check training logs
cat logs/*/events.*  # TensorBoard event files should exist
```

### Step 4: Test Inference (< 1 minute)

```bash
python src/inference.py \
  --checkpoint models/best_model.pth \
  --n_samples 5
```

**Expected Output:**
```
Loading model from models/best_model.pth...
✓ Model loaded successfully
  Training loss: 0.0234
  Validation loss: 0.0289
  Epoch: 100

============================================================
Example: Generate trajectories from random start/end
============================================================
Start: [  0.   0. 100.]
End: [800. 600. 200.]
Generating 5 trajectories...

Generated trajectories shape: (5, 50, 3)

Trajectory Metrics:
------------------------------------------------------------

Trajectory 1:
  Path length: 1024.53 m
  Efficiency: 0.875
  Smoothness: 0.9234
  Avg curvature: 0.000823 rad/m

Trajectory 2:
  Path length: 1042.18 m
  ...

✓ Inference demo completed!
```

### Step 5: Evaluate Model (2-5 minutes)

```bash
python src/evaluate.py \
  --checkpoint models/best_model.pth \
  --data data/trajectories.npz \
  --output results/
```

**Expected Output:**
```
============================================================
Running Full Model Evaluation
============================================================

1. Reconstruction Evaluation
------------------------------------------------------------
Evaluating reconstruction on 200 samples...
100%|████████████████████| 200/200 [00:15<00:00, 13.2it/s]
MSE: 0.0156 ± 0.0034
MAE: 0.0892 ± 0.0123
Endpoint Error: 8.32 ± 3.21 m

2. Diversity Evaluation
------------------------------------------------------------
Evaluating diversity: 50 pairs × 10 samples...
100%|████████████████████| 50/50 [00:42<00:00,  1.18it/s]
Avg Diversity: 145.67 ± 23.45 m

3. Quality Evaluation
------------------------------------------------------------
Evaluating quality on 200 trajectories...
100%|████████████████████| 200/200 [00:18<00:00, 10.8it/s]
Path Efficiency: 0.875 ± 0.042
Smoothness: 0.9234 ± 0.0156
Avg Curvature: 0.000823 ± 0.000145

4. Generating Visualizations
------------------------------------------------------------
Visualizing 9 samples...
✓ Visualization saved to results/evaluation_samples.png
✓ Diversity visualization saved to results/diversity.png

✓ Results saved to results/evaluation_results.json

============================================================
Evaluation Complete!
============================================================
```

**Check Results:**
```bash
ls -lh results/
# Should show:
# - evaluation_results.json
# - evaluation_samples.png
# - diversity.png

# View JSON results
cat results/evaluation_results.json | python -m json.tool
```

### Step 6: Export to ONNX (< 1 minute)

```bash
python src/export_onnx.py \
  --checkpoint models/best_model.pth \
  --output models/trajectory_generator.onnx \
  --test
```

**Expected Output:**
```
Loading model from models/best_model.pth...
✓ Model loaded successfully

Exporting generator to ONNX...
Output path: models/trajectory_generator.onnx
✓ ONNX model exported to models/trajectory_generator.onnx

Verifying ONNX model...
✓ ONNX model is valid
✓ Verification complete:
  Max difference: 0.000012
  Mean difference: 0.000003
  ✓ ONNX model matches PyTorch (excellent)

✓ Normalization parameters saved to models/trajectory_generator_normalization.json

Testing ONNX Inference
============================================================
Loaded normalization: mean=[...], std=[...]

Model inputs:
  latent: [1, 64] (tensor(float))
  start: [1, 3] (tensor(float))
  end: [1, 3] (tensor(float))

Model outputs:
  trajectory: [1, 50, 3] (tensor(float))

Generated trajectory shape: (1, 50, 3)
Start point: [  0.12  -0.08  99.87]
Expected start: [  0.   0. 100.]

Boundary errors:
  Start: 0.14 m
  End: 1.23 m

✓ ONNX inference test successful!

============================================================
Export Complete!
============================================================
```

### Step 7: C++ Inference (Optional, 5-10 minutes)

**Prerequisites:**
```bash
# Install ONNX Runtime
wget https://github.com/microsoft/onnxruntime/releases/download/v1.16.0/onnxruntime-linux-x64-1.16.0.tgz
tar -xzf onnxruntime-linux-x64-1.16.0.tgz
export ONNXRUNTIME_ROOT_DIR=$(pwd)/onnxruntime-linux-x64-1.16.0
```

**Build:**
```bash
cd cpp
mkdir -p build && cd build
cmake .. -DONNXRUNTIME_ROOT_DIR=$ONNXRUNTIME_ROOT_DIR
cmake --build . --config Release
```

**Expected Output:**
```
-- The C compiler identification is GNU 11.4.0
-- The CXX compiler identification is GNU 11.4.0
...
-- Build files written to: /workspace/cpp/build
[ 50%] Building CXX object CMakeFiles/trajectory_inference.dir/trajectory_inference.cpp.o
[100%] Linking CXX shared library libtrajectory_inference.so
[100%] Built target trajectory_inference
[100%] Built target trajectory_demo
```

**Run:**
```bash
# From cpp/build directory
./trajectory_demo ../../models/trajectory_generator.onnx ../../models/trajectory_generator_normalization.json
```

**Expected Output:**
```
========================================
Trajectory Generation - C++ Demo
========================================

Configuration:
  Model: ../../models/trajectory_generator.onnx
  Normalization: ../../models/trajectory_generator_normalization.json

--- Initializing Generator ---
✓ ONNX model loaded successfully: ../../models/trajectory_generator.onnx
✓ Normalization loaded:
  Mean: [...], Std: [...]

--- Example 1: Single Trajectory ---
Start: [0.00, 0.00, 100.00]
End: [800.00, 600.00, 200.00]

✓ Generated trajectory in 45 ms
Trajectory Statistics:
  Path length: 1024.5 m
  Efficiency: 0.875
  Avg curvature: 0.000823 rad/m
  Smoothness score: 0.9234

--- Example 2: Multiple Diverse Trajectories ---
...

========================================
Demo completed successfully!
========================================
```

### Step 8: Start API Service (< 1 minute)

```bash
# From project root
python api/app.py \
  --host 0.0.0.0 \
  --port 8000 \
  --model models/best_model.pth
```

**Expected Output:**
```
============================================================
Starting Trajectory Generation API
============================================================
Model path: models/best_model.pth
Device: cpu
Loading model from models/best_model.pth...
✓ Model loaded successfully
  Training loss: 0.0234
  Validation loss: 0.0289
  Epoch: 100
============================================================
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Test API (in a new terminal):**

```bash
# Health check
curl http://localhost:8000/health

# Generate trajectory
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "start": {"x": 0, "y": 0, "z": 100},
    "end": {"x": 800, "y": 600, "z": 200},
    "n_samples": 3
  }'
```

**Or run the test suite:**
```bash
# In a new terminal (keep API running)
python api/test_api.py
```

**Expected Test Output:**
```
============================================================
Trajectory Generation API - Test Suite
============================================================
API URL: http://localhost:8000

============================================================
Testing Health Endpoint
============================================================
Status Code: 200
✓ Health check passed

============================================================
Testing Single Trajectory Generation
============================================================
Status Code: 200
Response Time: 52.34 ms
Success: True
Inference Time: 45.21 ms
✓ Single trajectory generation passed

...

============================================================
✓ All tests passed!
============================================================
```

**Access API Documentation:**

Open http://localhost:8000/docs in your browser for interactive API documentation.

### Step 9: Visualization Demo (< 1 minute)

```bash
python src/visualize.py
```

**Expected Output:**
```
Trajectory Visualization Demo
============================================================

1. Plotting single trajectory...
✓ Saved to visualizations/single_trajectory.png

2. Plotting multiple trajectories...
✓ Saved to visualizations/multiple_trajectories.png

3. Creating interactive 3D plot...
✓ Interactive plot saved to visualizations/interactive_plot.html

============================================================
✓ Visualization demo complete!
Check the 'visualizations/' directory for outputs
============================================================
```

**View visualizations:**
```bash
# Open PNG images
xdg-open visualizations/single_trajectory.png  # Linux
open visualizations/single_trajectory.png      # macOS
start visualizations/single_trajectory.png     # Windows

# Open interactive HTML
xdg-open visualizations/interactive_plot.html  # Linux
open visualizations/interactive_plot.html      # macOS
start visualizations/interactive_plot.html     # Windows
```

## 🎯 Quick Command Reference

### Training Commands

```bash
# Quick training (10 epochs, for testing)
python src/train.py --epochs 10 --batch_size 32

# Full training (GPU)
python src/train.py --epochs 100 --batch_size 64 --device cuda

# Resume from checkpoint
python src/train.py --epochs 150 --resume models/checkpoint_epoch_100.pth
```

### Inference Commands

```bash
# Single trajectory
python -c "
from src.inference import TrajectoryPredictor
import numpy as np
pred = TrajectoryPredictor('models/best_model.pth')
traj = pred.predict_single(
    np.array([0, 0, 100]), 
    np.array([800, 600, 200]), 
    n_samples=1
)
print('Generated:', traj.shape)
"

# Multiple trajectories with obstacles
python -c "
from src.inference import TrajectoryPredictor
import numpy as np
pred = TrajectoryPredictor('models/best_model.pth')
obstacles = [{'center': np.array([400, 300, 150]), 'radius': 80}]
trajs, scores = pred.predict_with_obstacles(
    np.array([0, 0, 100]), 
    np.array([800, 600, 200]), 
    obstacles, 
    n_candidates=5
)
print('Generated:', trajs.shape, 'Best score:', scores[0])
"
```

### API Commands

```bash
# Start server
python api/app.py --host 0.0.0.0 --port 8000

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/info

# Generate trajectory (pretty print)
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"start": {"x": 0, "y": 0, "z": 100}, "end": {"x": 800, "y": 600, "z": 200}, "n_samples": 3}' \
  | python -m json.tool
```

## 📊 Expected File Sizes

After completing all steps:

```
data/
├── trajectories.npz                      # ~500 MB
├── trajectories_metadata.json            # ~5 KB
├── trajectories_obstacles.pkl            # ~100 MB
└── sample_trajectories.png               # ~500 KB

models/
├── best_model.pth                        # ~40 MB
├── trajectory_generator.onnx             # ~30 MB
├── trajectory_generator_normalization.json # ~1 KB
└── checkpoint_epoch_*.pth                # ~40 MB each

results/
├── evaluation_results.json               # ~50 KB
├── evaluation_samples.png                # ~1 MB
└── diversity.png                         # ~800 KB

logs/
└── <timestamp>/
    └── events.*                          # ~50 MB (100 epochs)

visualizations/
├── single_trajectory.png                 # ~500 KB
├── multiple_trajectories.png             # ~600 KB
└── interactive_plot.html                 # ~2 MB
```

**Total Disk Usage:** ~700 MB (without checkpoints), ~1.5 GB (with all checkpoints)

## ⚠️ Common Issues and Solutions

### Issue 1: Out of Memory During Training

**Symptoms:**
```
RuntimeError: CUDA out of memory
```

**Solution:**
```bash
# Reduce batch size
python src/train.py --batch_size 16 --device cuda

# Or train on CPU
python src/train.py --batch_size 32 --device cpu
```

### Issue 2: Model Not Converging

**Symptoms:**
- Loss stays high (>0.5) after 10 epochs
- Validation loss increases

**Solutions:**
```bash
# 1. Lower learning rate
python src/train.py --lr 0.0001

# 2. Adjust KL weight
python src/train.py --beta 0.0001

# 3. Increase smoothness penalty
python src/train.py --lambda_smooth 0.2
```

### Issue 3: ONNX Export Mismatch

**Symptoms:**
```
Max difference: 0.01  # Too large
```

**Solution:**
```bash
# Use CPU for export
python src/export_onnx.py --device cpu --checkpoint models/best_model.pth
```

### Issue 4: C++ Build Fails

**Symptoms:**
```
CMake Error: Could not find ONNX Runtime
```

**Solution:**
```bash
# Make sure ONNXRUNTIME_ROOT_DIR is set
export ONNXRUNTIME_ROOT_DIR=/path/to/onnxruntime

# Verify
echo $ONNXRUNTIME_ROOT_DIR
ls $ONNXRUNTIME_ROOT_DIR/lib  # Should show libonnxruntime.so

# Clean and rebuild
cd cpp/build
rm -rf *
cmake .. -DONNXRUNTIME_ROOT_DIR=$ONNXRUNTIME_ROOT_DIR
cmake --build .
```

### Issue 5: API Not Accessible

**Symptoms:**
```
curl: (7) Failed to connect to localhost port 8000
```

**Solutions:**
```bash
# 1. Check if server is running
ps aux | grep "app.py"

# 2. Check port is free
lsof -i :8000

# 3. Try different port
python api/app.py --port 8001

# 4. Check firewall
sudo ufw allow 8000  # Ubuntu
```

### Issue 6: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'torch'
```

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify
python -c "import torch; print(torch.__version__)"
```

## 🎓 Learning Resources

### Understanding the Code

1. **CVAE Architecture**: See `src/model.py`, class `CVAE_TrajectoryGenerator`
2. **Loss Functions**: See `src/model.py`, class `TrajectoryLoss`
3. **Training Loop**: See `src/train.py`, function `train_epoch`
4. **Data Generation**: See `src/data_generator.py`, class `TrajectoryGenerator`

### Modifying the System

1. **Change Trajectory Length:**
   - Edit `n_points` in `src/data_generator.py`
   - Edit `max_seq_len` in model creation

2. **Add New Loss Term:**
   - Add loss computation in `src/model.py:TrajectoryLoss.forward()`
   - Add weight hyperparameter

3. **Support Different Input Formats:**
   - Modify `TrajectoryDataset` in `src/train.py`
   - Update normalization logic

## 📞 Support

If you encounter issues:

1. Check this document for common solutions
2. Review logs in `logs/` directory
3. Check GitHub issues
4. Open a new issue with:
   - Error message
   - Command that failed
   - System info (OS, Python version, GPU)

---

**Congratulations! You've completed the full pipeline setup.** 🎉

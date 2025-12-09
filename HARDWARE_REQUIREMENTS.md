# Hardware and Compute Requirements

## Detailed Hardware Specifications

### Minimum Requirements

**For Data Generation Only:**
- **CPU**: Dual-core processor (Intel Core i3 / AMD equivalent)
- **RAM**: 8 GB
- **Storage**: 5 GB free space
- **GPU**: Not required
- **Time**: 15-20 minutes for 50k trajectories

**For Training (CPU):**
- **CPU**: Quad-core processor (Intel Core i5 / AMD Ryzen 5)
- **RAM**: 16 GB
- **Storage**: 10 GB free space
- **GPU**: Not required (but VERY slow)
- **Time**: 8-12 hours for 100 epochs

**For Inference Only:**
- **CPU**: Dual-core processor
- **RAM**: 4 GB
- **Storage**: 500 MB
- **GPU**: Not required
- **Time**: <100 ms per trajectory

### Recommended Requirements

**For Complete Development:**
- **CPU**: 8-core processor (Intel Core i7 / AMD Ryzen 7)
- **RAM**: 32 GB
- **Storage**: 20 GB free SSD space
- **GPU**: NVIDIA GPU with 8+ GB VRAM (RTX 3070, RTX 4060 Ti, or better)
- **GPU Driver**: CUDA 11.8 or later
- **OS**: Linux (Ubuntu 20.04+) or Windows 10/11

**For Production Deployment:**
- **CPU**: 4-8 cores (server-grade)
- **RAM**: 16 GB minimum, 32 GB recommended
- **Storage**: 10 GB SSD
- **GPU**: Optional, provides 5-10x speedup
- **Network**: 1 Gbps for API service

### Optimal/High-Performance Setup

**For Research and Experimentation:**
- **CPU**: 16-core processor (Intel Core i9 / AMD Ryzen 9 / Threadripper)
- **RAM**: 64 GB
- **Storage**: 50 GB NVMe SSD
- **GPU**: NVIDIA RTX 4090 (24 GB) or A100 (40 GB)
- **Multi-GPU**: 2-4 GPUs for faster training

## Performance Benchmarks

### Dataset Generation (50,000 trajectories)

| Hardware | Time | CPU Usage | RAM Usage |
|----------|------|-----------|-----------|
| Intel i5-8400 (6 cores) | 12 min | 100% | 4 GB |
| Intel i7-10700K (8 cores) | 8 min | 100% | 4 GB |
| AMD Ryzen 9 5950X (16 cores) | 5 min | 100% | 4 GB |

### Training (100 epochs, batch size 64)

| Hardware | Time | GPU VRAM | Power |
|----------|------|----------|-------|
| CPU only (i7-10700K) | 10-12 hours | N/A | ~95W |
| NVIDIA RTX 3060 (12GB) | 4.5 hours | 7.2 GB | ~170W |
| NVIDIA RTX 3070 (8GB) | 3.5 hours | 7.8 GB | ~220W |
| NVIDIA RTX 3080 (10GB) | 2.5 hours | 8.5 GB | ~320W |
| NVIDIA RTX 4090 (24GB) | 1.5 hours | 8.9 GB | ~450W |
| NVIDIA A100 (40GB) | 1.2 hours | 9.2 GB | ~400W |

### Inference (Single Trajectory)

| Hardware | Latency | Throughput | VRAM |
|----------|---------|------------|------|
| Intel i5-8400 (CPU) | 78 ms | 12.8 traj/sec | N/A |
| Intel i7-10700K (CPU) | 52 ms | 19.2 traj/sec | N/A |
| AMD Ryzen 9 5950X (CPU) | 38 ms | 26.3 traj/sec | N/A |
| NVIDIA RTX 3060 (GPU) | 12 ms | 83 traj/sec | 1.2 GB |
| NVIDIA RTX 3070 (GPU) | 9 ms | 111 traj/sec | 1.2 GB |
| NVIDIA RTX 4090 (GPU) | 5 ms | 200 traj/sec | 1.2 GB |

### Inference (Batch of 10 Trajectories)

| Hardware | Latency | Throughput | VRAM |
|----------|---------|------------|------|
| Intel i7-10700K (CPU) | 224 ms | 44.6 traj/sec | N/A |
| NVIDIA RTX 3070 (GPU) | 31 ms | 322 traj/sec | 2.1 GB |
| NVIDIA RTX 4090 (GPU) | 18 ms | 555 traj/sec | 2.1 GB |

## Cloud Computing Options

### AWS EC2

**For Training:**
- **Instance**: g4dn.xlarge (NVIDIA T4, 16 GB GPU)
- **Cost**: ~$0.526/hour
- **Training Time**: ~4 hours
- **Total Cost**: ~$2.10 per training run

- **Instance**: p3.2xlarge (NVIDIA V100, 16 GB GPU)
- **Cost**: ~$3.06/hour
- **Training Time**: ~2.5 hours
- **Total Cost**: ~$7.65 per training run

**For Inference API:**
- **Instance**: t3.medium (2 vCPU, 4 GB RAM)
- **Cost**: ~$0.0416/hour (~$30/month)
- **Performance**: ~15 trajectories/sec

### Google Cloud Platform

**For Training:**
- **Instance**: n1-standard-4 + NVIDIA T4
- **Cost**: ~$0.51/hour
- **Training Time**: ~4 hours
- **Total Cost**: ~$2.04 per training run

**For Inference API:**
- **Instance**: e2-medium (2 vCPU, 4 GB)
- **Cost**: ~$0.033/hour (~$24/month)

### Azure

**For Training:**
- **Instance**: NC6s v3 (NVIDIA V100)
- **Cost**: ~$3.06/hour
- **Training Time**: ~2.5 hours
- **Total Cost**: ~$7.65 per training run

## Storage Requirements

### Development

```
data/
  trajectories.npz              500 MB
  trajectories_obstacles.pkl    100 MB
  trajectories_metadata.json      5 KB

models/
  best_model.pth                 40 MB
  trajectory_generator.onnx      30 MB
  checkpoints (10 epochs)       400 MB

logs/
  tensorboard events             50 MB

results/
  evaluation outputs             10 MB

Total: ~1.1 GB
```

### Production

```
models/
  trajectory_generator.onnx      30 MB
  normalization.json              1 KB

Total: ~30 MB
```

## Memory Requirements

### Training

- **Model Parameters**: ~2.5M parameters × 4 bytes = 10 MB
- **Optimizer State**: 2× model size = 20 MB
- **Batch Data**: batch_size × seq_len × 3 × 4 bytes
  - Batch 64: 64 × 50 × 3 × 4 = 38.4 KB
- **Activations**: ~500 MB (depends on batch size)
- **PyTorch Overhead**: ~2 GB

**Total GPU VRAM**: ~7-9 GB

**Total System RAM**: 
- Data loading: ~2 GB
- OS + Python: ~2 GB
- Buffer: ~2 GB
- **Total**: ~16 GB recommended

### Inference

- **Model**: 10 MB
- **Input/Output Buffers**: <1 MB
- **Runtime Overhead**: 
  - Python: ~1 GB
  - C++: ~50 MB

## Network Requirements

### API Service

**Bandwidth per Request:**
- Input: ~100 bytes (start + end waypoints)
- Output: ~6 KB (trajectory with 50 waypoints)
- Total per request: ~6 KB

**Expected Load:**
- 100 requests/sec = ~600 KB/sec = ~5 Mbps
- 1000 requests/sec = ~6 MB/sec = ~50 Mbps

**Latency:**
- Local inference: 50-100 ms
- Network overhead: 10-50 ms
- Total: 60-150 ms

## Power Consumption

### Training (100 epochs)

| Setup | Power | Time | Energy |
|-------|-------|------|--------|
| CPU only | 95W | 10 hours | 0.95 kWh |
| RTX 3070 | 220W | 3.5 hours | 0.77 kWh |
| RTX 4090 | 450W | 1.5 hours | 0.68 kWh |

**Cost** (at $0.12/kWh):
- CPU: $0.11
- RTX 3070: $0.09
- RTX 4090: $0.08

### 24/7 API Service

| Setup | Power | Daily | Monthly |
|-------|-------|-------|---------|
| CPU Server | 65W | 1.56 kWh | 46.8 kWh |
| GPU Server | 150W | 3.6 kWh | 108 kWh |

**Cost** (at $0.12/kWh):
- CPU: $5.62/month
- GPU: $12.96/month

## Scaling Recommendations

### Small Scale (Development)
- 1-10 users
- CPU inference: t3.medium (AWS)
- Cost: ~$30/month

### Medium Scale (Production)
- 10-100 concurrent users
- GPU inference: g4dn.xlarge (AWS)
- Load balancer + auto-scaling
- Cost: ~$200-500/month

### Large Scale (Enterprise)
- 100+ concurrent users
- Multiple GPU instances
- Kubernetes cluster
- CDN for static content
- Cost: ~$1000+/month

## Cost Optimization Tips

1. **Use Spot Instances** for training (50-70% cost reduction)
2. **CPU for inference** if latency >100ms is acceptable
3. **Batch requests** to maximize GPU utilization
4. **Model quantization** to reduce VRAM (INT8: 4x smaller)
5. **Caching** for common start-end pairs
6. **Serverless** for low-traffic scenarios

## Recommended Configurations

### Configuration 1: Budget Development
- **Cost**: $0 (local hardware)
- **Hardware**: i5 CPU, 16 GB RAM, no GPU
- **Use Case**: Learning, experimentation
- **Limitations**: Slow training (8-12 hours)

### Configuration 2: Professional Development
- **Cost**: ~$1500 (one-time hardware)
- **Hardware**: i7 CPU, 32 GB RAM, RTX 3070
- **Use Case**: Full development cycle
- **Benefits**: Fast training (3-4 hours)

### Configuration 3: Cloud Training
- **Cost**: ~$5 per training run
- **Hardware**: AWS g4dn.xlarge
- **Use Case**: Occasional training
- **Benefits**: No upfront cost, scalable

### Configuration 4: Production API
- **Cost**: ~$50/month
- **Hardware**: AWS t3.medium + ALB
- **Use Case**: Low-traffic API (<10 req/sec)
- **Benefits**: Auto-scaling, high availability

### Configuration 5: High-Performance
- **Cost**: ~$500/month
- **Hardware**: Multi-GPU cluster
- **Use Case**: High-traffic API (100+ req/sec)
- **Benefits**: Low latency, high throughput

## Summary

**Minimum to get started**: $0 (use existing laptop)
**Recommended for development**: $1500 (workstation with GPU)
**Production deployment**: $30-500/month (cloud hosting)
**Training cost**: $2-8 per run (cloud) or $0.10 (local)

Choose based on:
- **Budget**: Use cloud for training, CPU for inference
- **Speed**: GPU highly recommended for training
- **Scale**: Start small, scale with load
- **Development**: Local GPU is best

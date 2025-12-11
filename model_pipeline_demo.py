"""
Complete Model Pipeline Demonstration
Shows training, validation, testing, and inference pipeline for C++ porting

This script demonstrates:
1. Dataset preparation and splitting
2. Model architecture and initialization
3. Training loop with validation
4. Testing and evaluation metrics
5. Inference with quality metrics

All components are explained for easy C++ porting.
"""

import warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np
import json
import os
from typing import Dict, Tuple, List
from tqdm import tqdm

from src.model import create_model, TrajectoryLoss, compute_kl_divergence, compute_smoothness_loss, compute_boundary_loss
from src.train import TrajectoryDataset
from src.inference import TrajectoryPredictor, evaluate_trajectory_quality


class ModelPipelineDemo:
    """
    Complete demonstration of the model training/testing pipeline
    
    This class shows all the key components you need to port to C++:
    1. Data normalization
    2. Model forward pass
    3. Loss computation
    4. Training iteration
    5. Validation
    6. Inference
    """
    
    def __init__(self, device: str = 'cpu'):
        self.device = torch.device(device)
        print(f"Initializing Model Pipeline Demo on {device}")
        print("=" * 80)
        
    def demonstrate_data_preparation(self, data_path: str = 'data/trajectories.npz'):
        """
        STEP 1: Data Preparation and Normalization
        
        For C++ Implementation:
        - Load trajectories from storage
        - Compute mean and std for normalization
        - Split into train/val/test sets
        """
        print("\n[STEP 1] DATA PREPARATION")
        print("-" * 80)
        
        # Load dataset
        dataset = TrajectoryDataset(data_path, normalize=True)
        
        print(f"Dataset size: {len(dataset)}")
        print(f"Normalization parameters:")
        print(f"  Mean: {dataset.mean.numpy()}")
        print(f"  Std:  {dataset.std.numpy()}")
        
        # Data split (80% train, 10% val, 10% test)
        n_total = len(dataset)
        n_train = int(0.8 * n_total)
        n_val = int(0.1 * n_total)
        n_test = n_total - n_train - n_val
        
        train_dataset, val_dataset, test_dataset = random_split(
            dataset, [n_train, n_val, n_test],
            generator=torch.Generator().manual_seed(42)
        )
        
        print(f"Split: Train={n_train}, Val={n_val}, Test={n_test}")
        
        # Show sample data structure
        sample = dataset[0]
        print(f"\nSample data structure:")
        print(f"  Trajectory shape: {sample['trajectory'].shape}  # [seq_len, 3]")
        print(f"  Start point: {sample['start'].numpy()}")
        print(f"  End point: {sample['end'].numpy()}")
        
        return dataset, train_dataset, val_dataset, test_dataset
    
    def demonstrate_model_architecture(self):
        """
        STEP 2: Model Architecture
        
        For C++ Implementation:
        - LSTM Encoder (bidirectional)
        - Latent space sampling (reparameterization trick)
        - LSTM Decoder
        - Loss function components
        """
        print("\n[STEP 2] MODEL ARCHITECTURE")
        print("-" * 80)
        
        # Create model
        model = create_model(
            latent_dim=64,
            hidden_dim=256,
            num_layers=2,
            max_seq_len=50
        )
        model = model.to(self.device)
        
        # Count parameters
        n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        print(f"Model created with {n_params:,} trainable parameters")
        
        print("\nModel components:")
        print("  1. Encoder (Trajectory → Latent Space)")
        print("     - Bidirectional LSTM: input_dim=3, hidden_dim=256, layers=2")
        print("     - Output: mu (mean) and logvar (log variance) of latent distribution")
        print("     - Latent dimension: 64")
        
        print("\n  2. Reparameterization Trick")
        print("     - z = mu + exp(0.5 * logvar) * epsilon")
        print("     - epsilon ~ N(0, 1)")
        
        print("\n  3. Decoder (Latent + Conditions → Trajectory)")
        print("     - Input: z (latent), start (3D), end (3D)")
        print("     - LSTM: input_dim=3+64+6, hidden_dim=256, layers=2")
        print("     - Output: trajectory sequence [seq_len, 3]")
        
        print("\n  4. Loss Function")
        print("     - Reconstruction Loss: MSE(predicted, target)")
        print("     - KL Divergence: KL(q(z|x) || p(z))")
        print("     - Smoothness Loss: Curvature penalty")
        print("     - Boundary Loss: Enforce start/end constraints")
        
        # Demonstrate forward pass
        print("\n  5. Forward Pass Demo")
        batch_size = 4
        seq_len = 50
        
        trajectory = torch.randn(batch_size, seq_len, 3).to(self.device)
        start = torch.randn(batch_size, 3).to(self.device)
        end = torch.randn(batch_size, 3).to(self.device)
        
        print(f"     Input trajectory: {trajectory.shape}")
        print(f"     Start waypoints: {start.shape}")
        print(f"     End waypoints: {end.shape}")
        
        with torch.no_grad():
            reconstructed, mu, logvar = model(trajectory, start, end, teacher_forcing_ratio=0.0)
        
        print(f"     Output reconstructed: {reconstructed.shape}")
        print(f"     Latent mu: {mu.shape}")
        print(f"     Latent logvar: {logvar.shape}")
        
        return model
    
    def demonstrate_loss_computation(self, model):
        """
        STEP 3: Loss Computation Details
        
        For C++ Implementation:
        - Each loss component calculation
        - Weighted combination
        """
        print("\n[STEP 3] LOSS COMPUTATION")
        print("-" * 80)
        
        # Create sample batch
        batch_size = 8
        seq_len = 50
        
        trajectory = torch.randn(batch_size, seq_len, 3).to(self.device)
        start = torch.randn(batch_size, 3).to(self.device)
        end = torch.randn(batch_size, 3).to(self.device)
        
        # Forward pass
        reconstructed, mu, logvar = model(trajectory, start, end, teacher_forcing_ratio=0.0)
        
        # Compute individual loss components
        print("Loss components:")
        
        # 1. Reconstruction loss
        recon_loss = nn.functional.mse_loss(reconstructed, trajectory)
        print(f"  1. Reconstruction Loss (MSE): {recon_loss.item():.6f}")
        print(f"     Formula: MSE = mean((predicted - target)^2)")
        
        # 2. KL divergence
        kl_loss = compute_kl_divergence(mu, logvar)
        print(f"\n  2. KL Divergence: {kl_loss.item():.6f}")
        print(f"     Formula: KL = -0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)")
        print(f"              where sigma^2 = exp(logvar)")
        
        # 3. Smoothness loss
        smooth_loss = compute_smoothness_loss(reconstructed)
        print(f"\n  3. Smoothness Loss (Curvature): {smooth_loss.item():.6f}")
        print(f"     Formula: mean(||trajectory[i+1] - 2*trajectory[i] + trajectory[i-1]||^2)")
        
        # 4. Boundary loss
        boundary_loss = compute_boundary_loss(reconstructed, start, end)
        print(f"\n  4. Boundary Loss: {boundary_loss.item():.6f}")
        print(f"     Formula: MSE(trajectory[0], start) + MSE(trajectory[-1], end)")
        
        # Combined loss
        criterion = TrajectoryLoss(beta=0.001, lambda_smooth=0.1, lambda_boundary=1.0)
        total_loss, loss_dict = criterion(reconstructed, trajectory, mu, logvar, start, end)
        
        print(f"\n  5. Total Loss (weighted sum):")
        print(f"     total = recon + 0.001*kl + 0.1*smooth + 1.0*boundary")
        print(f"     total = {total_loss.item():.6f}")
        
        return loss_dict
    
    def demonstrate_training_iteration(self, model, dataset):
        """
        STEP 4: Training Iteration
        
        For C++ Implementation:
        - Batch processing
        - Forward pass
        - Loss computation
        - Backpropagation (gradient descent)
        - Parameter update
        """
        print("\n[STEP 4] TRAINING ITERATION")
        print("-" * 80)
        
        # Create small dataloader
        dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
        
        # Setup optimizer
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        criterion = TrajectoryLoss(beta=0.001, lambda_smooth=0.1, lambda_boundary=1.0)
        
        model.train()
        
        print("Single training iteration:")
        
        # Get one batch
        batch = next(iter(dataloader))
        trajectory = batch['trajectory'].to(self.device)
        start = batch['start'].to(self.device)
        end = batch['end'].to(self.device)
        
        print(f"  Batch size: {trajectory.shape[0]}")
        
        # Forward pass
        print("  1. Forward pass...")
        reconstructed, mu, logvar = model(trajectory, start, end, teacher_forcing_ratio=0.5)
        
        # Compute loss
        print("  2. Compute loss...")
        loss, loss_dict = criterion(reconstructed, trajectory, mu, logvar, start, end)
        print(f"     Total loss: {loss.item():.6f}")
        
        # Backward pass
        print("  3. Backward pass (compute gradients)...")
        optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping
        print("  4. Gradient clipping (max_norm=1.0)...")
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        # Update parameters
        print("  5. Update parameters (Adam optimizer)...")
        optimizer.step()
        
        print("\n  Note for C++: You can use gradient-free optimization or")
        print("  export the trained model to ONNX for inference only.")
        
    def demonstrate_validation(self, model, val_dataset):
        """
        STEP 5: Validation
        
        For C++ Implementation:
        - No gradient computation
        - Evaluate on validation set
        - Compute metrics
        """
        print("\n[STEP 5] VALIDATION")
        print("-" * 80)
        
        model.eval()
        
        val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)
        criterion = TrajectoryLoss(beta=0.001, lambda_smooth=0.1, lambda_boundary=1.0)
        
        total_loss = 0.0
        n_batches = 0
        
        print("Running validation...")
        
        with torch.no_grad():
            for batch in val_loader:
                trajectory = batch['trajectory'].to(self.device)
                start = batch['start'].to(self.device)
                end = batch['end'].to(self.device)
                
                # Forward pass (no teacher forcing)
                reconstructed, mu, logvar = model(trajectory, start, end, teacher_forcing_ratio=0.0)
                
                # Compute loss
                loss, _ = criterion(reconstructed, trajectory, mu, logvar, start, end)
                
                total_loss += loss.item()
                n_batches += 1
                
                if n_batches >= 10:  # Just demo
                    break
        
        avg_loss = total_loss / n_batches
        print(f"Validation loss: {avg_loss:.6f}")
        print("\nNote: Validation uses no teacher forcing and no gradient computation")
    
    def demonstrate_inference(self, model, dataset):
        """
        STEP 6: Inference and Quality Metrics
        
        For C++ Implementation (THIS IS KEY FOR YOUR APPLICATION):
        - Generate trajectories from start/end waypoints
        - Sample from prior distribution
        - Decode to trajectory
        - Compute quality metrics
        """
        print("\n[STEP 6] INFERENCE AND QUALITY METRICS")
        print("-" * 80)
        
        model.eval()
        
        # Get sample start/end
        sample = dataset[0]
        start = sample['start'].to(self.device).unsqueeze(0)
        end = sample['end'].to(self.device).unsqueeze(0)
        
        print("Generating trajectories:")
        print(f"  Start: {start.cpu().numpy()[0]}")
        print(f"  End: {end.cpu().numpy()[0]}")
        
        # Generate multiple diverse trajectories
        n_samples = 5
        print(f"\n  Generating {n_samples} diverse trajectories...")
        
        with torch.no_grad():
            trajectories = model.generate(start, end, n_samples=n_samples, seq_len=50)
        
        print(f"  Generated shape: {trajectories.shape}  # [n_samples, seq_len, 3]")
        
        # Denormalize for analysis
        trajectories_denorm = trajectories * dataset.std.to(self.device) + dataset.mean.to(self.device)
        trajectories_np = trajectories_denorm.cpu().numpy()
        
        print("\n  Quality metrics for each trajectory:")
        print("  " + "-" * 76)
        
        for i, traj in enumerate(trajectories_np):
            metrics = evaluate_trajectory_quality(traj)
            
            print(f"\n  Trajectory {i+1}:")
            print(f"    Path length: {metrics['path_length']:.2f} m")
            print(f"    Path efficiency: {metrics['path_efficiency']:.3f}")
            print(f"    Smoothness score: {metrics['smoothness_score']:.4f}")
            print(f"    Avg curvature: {metrics['avg_curvature']:.6f} rad/m")
            print(f"    Altitude range: [{metrics['min_altitude']:.1f}, {metrics['max_altitude']:.1f}] m")
        
        # Show key algorithms for C++
        print("\n  Key algorithms for C++ implementation:")
        print("\n  1. Path Length:")
        print("     length = sum(||waypoint[i+1] - waypoint[i]|| for i in range(n-1))")
        
        print("\n  2. Path Efficiency:")
        print("     efficiency = straight_line_distance / path_length")
        
        print("\n  3. Curvature at point i:")
        print("     v1 = waypoint[i] - waypoint[i-1]")
        print("     v2 = waypoint[i+1] - waypoint[i]")
        print("     cos_angle = dot(v1, v2) / (||v1|| * ||v2||)")
        print("     angle = arccos(cos_angle)")
        print("     curvature = angle / ||v1||")
        
        print("\n  4. Smoothness Score:")
        print("     smoothness = 1.0 / (1.0 + avg_curvature)")
        
        return trajectories_np
    
    def demonstrate_complete_workflow(self, data_path: str = 'data/trajectories.npz'):
        """
        Run complete workflow demonstration
        """
        print("\n" + "=" * 80)
        print("COMPLETE MODEL PIPELINE DEMONSTRATION")
        print("For C++ Application Porting")
        print("=" * 80)
        
        # Check if data exists
        if not os.path.exists(data_path):
            print(f"\nError: Dataset not found at {data_path}")
            print("Please run: python src/data_generator.py")
            return
        
        # Step 1: Data preparation
        dataset, train_dataset, val_dataset, test_dataset = self.demonstrate_data_preparation(data_path)
        
        # Step 2: Model architecture
        model = self.demonstrate_model_architecture()
        
        # Step 3: Loss computation
        self.demonstrate_loss_computation(model)
        
        # Step 4: Training iteration
        self.demonstrate_training_iteration(model, train_dataset)
        
        # Step 5: Validation
        self.demonstrate_validation(model, val_dataset)
        
        # Step 6: Inference
        trajectories = self.demonstrate_inference(model, dataset)
        
        print("\n" + "=" * 80)
        print("SUMMARY FOR C++ IMPLEMENTATION")
        print("=" * 80)
        
        print("""
For C++ Application, you need to implement:

1. DATA STRUCTURES:
   - Waypoint: struct with x, y, z (float)
   - Trajectory: vector of Waypoints
   - NormalizationParams: mean and std arrays

2. INFERENCE ENGINE (Already provided in cpp/):
   - Load ONNX model
   - Normalize input waypoints
   - Sample latent vector from N(0,1)
   - Run ONNX inference
   - Denormalize output trajectory

3. QUALITY METRICS (Need to implement):
   - computePathLength()
   - computePathEfficiency()
   - computeAverageCurvature()
   - computeSmoothnessScore()
   - computeEndpointError()

4. TRAINING (Optional - can be done in Python):
   - If you need online learning in C++, consider:
     * Using LibTorch (PyTorch C++ API)
     * Or implement gradient descent manually
     * Or keep training in Python and export to ONNX

5. FILES YOU NEED:
   - models/trajectory_generator.onnx (exported model)
   - models/trajectory_generator_normalization.json (normalization params)
   
6. NEXT STEPS:
   - Export trained model: python src/export_onnx.py
   - Build C++ inference: cd cpp && mkdir build && cd build && cmake ..
   - Implement quality metrics in C++
   - Integrate into your application
        """)
        
        print("=" * 80)
        print("Demonstration complete!")
        print("=" * 80)


def main():
    """Run the demonstration"""
    demo = ModelPipelineDemo(device='cpu')
    demo.demonstrate_complete_workflow(data_path='data/trajectories.npz')


if __name__ == '__main__':
    main()

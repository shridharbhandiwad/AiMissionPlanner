"""
Training script for trajectory generation model
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter
import numpy as np
import os
import argparse
from tqdm import tqdm
import json
from typing import Dict, Tuple

from model import create_model, TrajectoryLoss


class TrajectoryDataset(Dataset):
    """PyTorch Dataset for trajectory data"""
    
    def __init__(self, data_path: str, normalize: bool = True):
        """
        Args:
            data_path: Path to .npz file
            normalize: Whether to normalize the data
        """
        # Load data
        data = np.load(data_path)
        
        self.trajectories = torch.FloatTensor(data['trajectories'])
        self.start_points = torch.FloatTensor(data['start_points'])
        self.end_points = torch.FloatTensor(data['end_points'])
        
        self.normalize = normalize
        
        if normalize:
            # Compute normalization statistics
            all_points = torch.cat([
                self.trajectories.reshape(-1, 3),
                self.start_points,
                self.end_points
            ], dim=0)
            
            self.mean = all_points.mean(dim=0)
            self.std = all_points.std(dim=0)
            
            # Normalize
            self.trajectories = (self.trajectories - self.mean) / self.std
            self.start_points = (self.start_points - self.mean) / self.std
            self.end_points = (self.end_points - self.mean) / self.std
            
            print(f"Data normalized - Mean: {self.mean}, Std: {self.std}")
        else:
            self.mean = torch.zeros(3)
            self.std = torch.ones(3)
    
    def __len__(self):
        return len(self.trajectories)
    
    def __getitem__(self, idx):
        return {
            'trajectory': self.trajectories[idx],
            'start': self.start_points[idx],
            'end': self.end_points[idx]
        }
    
    def denormalize(self, data: torch.Tensor) -> torch.Tensor:
        """Denormalize data back to original scale"""
        return data * self.std + self.mean


def train_epoch(model: nn.Module, dataloader: DataLoader, 
                criterion: nn.Module, optimizer: optim.Optimizer,
                device: torch.device, teacher_forcing_ratio: float = 0.5) -> Dict:
    """
    Train for one epoch
    
    Args:
        model: Trajectory generation model
        dataloader: Training data loader
        criterion: Loss function
        optimizer: Optimizer
        device: Device to train on
        teacher_forcing_ratio: Teacher forcing ratio
        
    Returns:
        metrics: Dictionary of training metrics
    """
    model.train()
    
    total_loss = 0.0
    loss_components = {
        'reconstruction': 0.0,
        'kl': 0.0,
        'smoothness': 0.0,
        'boundary': 0.0
    }
    
    n_batches = 0
    
    progress_bar = tqdm(dataloader, desc='Training')
    
    for batch in progress_bar:
        trajectory = batch['trajectory'].to(device)
        start = batch['start'].to(device)
        end = batch['end'].to(device)
        
        # Forward pass
        reconstructed, mu, logvar = model(trajectory, start, end, teacher_forcing_ratio)
        
        # Compute loss
        loss, loss_dict = criterion(reconstructed, trajectory, mu, logvar, start, end)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        
        # Accumulate metrics
        total_loss += loss.item()
        for k in loss_components:
            loss_components[k] += loss_dict[k]
        n_batches += 1
        
        # Update progress bar
        progress_bar.set_postfix({
            'loss': loss.item(),
            'recon': loss_dict['reconstruction'],
            'kl': loss_dict['kl']
        })
    
    # Average metrics
    metrics = {
        'loss': total_loss / n_batches,
        'reconstruction_loss': loss_components['reconstruction'] / n_batches,
        'kl_loss': loss_components['kl'] / n_batches,
        'smoothness_loss': loss_components['smoothness'] / n_batches,
        'boundary_loss': loss_components['boundary'] / n_batches
    }
    
    return metrics


def validate(model: nn.Module, dataloader: DataLoader,
            criterion: nn.Module, device: torch.device) -> Dict:
    """
    Validate model
    
    Args:
        model: Trajectory generation model
        dataloader: Validation data loader
        criterion: Loss function
        device: Device
        
    Returns:
        metrics: Dictionary of validation metrics
    """
    model.eval()
    
    total_loss = 0.0
    loss_components = {
        'reconstruction': 0.0,
        'kl': 0.0,
        'smoothness': 0.0,
        'boundary': 0.0
    }
    
    n_batches = 0
    
    with torch.no_grad():
        for batch in tqdm(dataloader, desc='Validation'):
            trajectory = batch['trajectory'].to(device)
            start = batch['start'].to(device)
            end = batch['end'].to(device)
            
            # Forward pass
            reconstructed, mu, logvar = model(trajectory, start, end, teacher_forcing_ratio=0.0)
            
            # Compute loss
            loss, loss_dict = criterion(reconstructed, trajectory, mu, logvar, start, end)
            
            # Accumulate metrics
            total_loss += loss.item()
            for k in loss_components:
                loss_components[k] += loss_dict[k]
            n_batches += 1
    
    # Average metrics
    metrics = {
        'loss': total_loss / n_batches,
        'reconstruction_loss': loss_components['reconstruction'] / n_batches,
        'kl_loss': loss_components['kl'] / n_batches,
        'smoothness_loss': loss_components['smoothness'] / n_batches,
        'boundary_loss': loss_components['boundary'] / n_batches
    }
    
    return metrics


def train_model(args):
    """
    Main training function
    
    Args:
        args: Command line arguments
    """
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Create directories
    os.makedirs(args.save_dir, exist_ok=True)
    os.makedirs(args.log_dir, exist_ok=True)
    
    # Load dataset
    print(f"Loading dataset from {args.data_path}...")
    full_dataset = TrajectoryDataset(args.data_path, normalize=True)
    
    # Split dataset
    n_total = len(full_dataset)
    n_train = int(0.8 * n_total)
    n_val = int(0.1 * n_total)
    n_test = n_total - n_train - n_val
    
    train_dataset, val_dataset, test_dataset = random_split(
        full_dataset, [n_train, n_val, n_test],
        generator=torch.Generator().manual_seed(args.seed)
    )
    
    print(f"Dataset split: Train={n_train}, Val={n_val}, Test={n_test}")
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        pin_memory=True if device.type == 'cuda' else False
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=True if device.type == 'cuda' else False
    )
    
    # Create model
    print("Creating model...")
    model = create_model(
        latent_dim=args.latent_dim,
        hidden_dim=args.hidden_dim,
        num_layers=args.num_layers,
        max_seq_len=50
    )
    model = model.to(device)
    
    # Count parameters
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Model has {n_params:,} trainable parameters")
    
    # Create loss and optimizer
    criterion = TrajectoryLoss(
        beta=args.beta,
        lambda_smooth=args.lambda_smooth,
        lambda_boundary=args.lambda_boundary
    )
    
    optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5, verbose=True
    )
    
    # TensorBoard
    writer = SummaryWriter(args.log_dir)
    
    # Training loop
    best_val_loss = float('inf')
    patience_counter = 0
    
    print("\nStarting training...")
    print("=" * 60)
    
    for epoch in range(args.epochs):
        print(f"\nEpoch {epoch + 1}/{args.epochs}")
        
        # Teacher forcing ratio decay
        teacher_forcing_ratio = max(0.5 * (0.99 ** epoch), 0.1)
        
        # Train
        train_metrics = train_epoch(
            model, train_loader, criterion, optimizer, device, teacher_forcing_ratio
        )
        
        # Validate
        val_metrics = validate(model, val_loader, criterion, device)
        
        # Learning rate scheduling
        scheduler.step(val_metrics['loss'])
        
        # Print metrics
        print(f"Train Loss: {train_metrics['loss']:.4f} | Val Loss: {val_metrics['loss']:.4f}")
        print(f"  Recon: {train_metrics['reconstruction_loss']:.4f} | {val_metrics['reconstruction_loss']:.4f}")
        print(f"  KL: {train_metrics['kl_loss']:.4f} | {val_metrics['kl_loss']:.4f}")
        print(f"  Smooth: {train_metrics['smoothness_loss']:.4f} | {val_metrics['smoothness_loss']:.4f}")
        print(f"  Boundary: {train_metrics['boundary_loss']:.4f} | {val_metrics['boundary_loss']:.4f}")
        
        # TensorBoard logging
        for k, v in train_metrics.items():
            writer.add_scalar(f'train/{k}', v, epoch)
        for k, v in val_metrics.items():
            writer.add_scalar(f'val/{k}', v, epoch)
        writer.add_scalar('learning_rate', optimizer.param_groups[0]['lr'], epoch)
        
        # Save best model
        if val_metrics['loss'] < best_val_loss:
            best_val_loss = val_metrics['loss']
            patience_counter = 0
            
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_metrics['loss'],
                'train_loss': train_metrics['loss'],
                'args': vars(args),
                'normalization': {
                    'mean': full_dataset.mean.numpy().tolist(),
                    'std': full_dataset.std.numpy().tolist()
                }
            }
            
            save_path = os.path.join(args.save_dir, 'best_model.pth')
            torch.save(checkpoint, save_path)
            print(f"✓ Saved best model to {save_path}")
        else:
            patience_counter += 1
        
        # Save latest model
        if (epoch + 1) % args.save_interval == 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_metrics['loss'],
                'train_loss': train_metrics['loss'],
                'args': vars(args),
                'normalization': {
                    'mean': full_dataset.mean.numpy().tolist(),
                    'std': full_dataset.std.numpy().tolist()
                }
            }
            
            save_path = os.path.join(args.save_dir, f'checkpoint_epoch_{epoch+1}.pth')
            torch.save(checkpoint, save_path)
            print(f"✓ Saved checkpoint to {save_path}")
        
        # Early stopping
        if patience_counter >= args.patience:
            print(f"\nEarly stopping triggered after {epoch + 1} epochs")
            break
    
    writer.close()
    print("\n" + "=" * 60)
    print("Training completed!")
    print(f"Best validation loss: {best_val_loss:.4f}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Train trajectory generation model')
    
    # Data
    parser.add_argument('--data_path', type=str, default='data/trajectories.npz',
                       help='Path to trajectory dataset')
    
    # Model
    parser.add_argument('--latent_dim', type=int, default=64,
                       help='Dimension of latent space')
    parser.add_argument('--hidden_dim', type=int, default=256,
                       help='Hidden dimension for LSTM')
    parser.add_argument('--num_layers', type=int, default=2,
                       help='Number of LSTM layers')
    
    # Loss weights
    parser.add_argument('--beta', type=float, default=0.001,
                       help='KL divergence weight')
    parser.add_argument('--lambda_smooth', type=float, default=0.1,
                       help='Smoothness loss weight')
    parser.add_argument('--lambda_boundary', type=float, default=1.0,
                       help='Boundary loss weight')
    
    # Training
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=64,
                       help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001,
                       help='Learning rate')
    parser.add_argument('--weight_decay', type=float, default=1e-5,
                       help='Weight decay')
    parser.add_argument('--patience', type=int, default=15,
                       help='Early stopping patience')
    
    # Misc
    parser.add_argument('--save_dir', type=str, default='models',
                       help='Directory to save models')
    parser.add_argument('--log_dir', type=str, default='logs',
                       help='Directory for TensorBoard logs')
    parser.add_argument('--save_interval', type=int, default=10,
                       help='Save checkpoint every N epochs')
    parser.add_argument('--num_workers', type=int, default=4,
                       help='Number of data loader workers')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed')
    
    args = parser.parse_args()
    
    # Set random seeds
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(args.seed)
    
    # Train
    train_model(args)


if __name__ == '__main__':
    main()

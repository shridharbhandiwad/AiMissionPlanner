"""
CVAE-based Trajectory Generation Model
Conditional Variational Autoencoder for generating diverse trajectories
"""

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings

# Filter warnings before NumPy import to suppress MINGW-W64 build warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional


class TrajectoryEncoder(nn.Module):
    """
    Encoder: Trajectory sequence → Latent distribution (μ, log_σ²)
    """
    
    def __init__(self, input_dim: int = 3, hidden_dim: int = 256, 
                 latent_dim: int = 64, num_layers: int = 2):
        super().__init__()
        
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # LSTM encoder
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0.0,
            bidirectional=True
        )
        
        # Project to latent distribution parameters
        self.fc_mu = nn.Linear(hidden_dim * 2, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim * 2, latent_dim)
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            x: Trajectory sequence [batch_size, seq_len, 3]
            
        Returns:
            mu: Mean of latent distribution [batch_size, latent_dim]
            logvar: Log variance of latent distribution [batch_size, latent_dim]
        """
        # LSTM encoding
        lstm_out, (hidden, cell) = self.lstm(x)
        
        # Use final hidden state (concatenate forward and backward)
        # hidden shape: [num_layers * 2, batch_size, hidden_dim]
        hidden_forward = hidden[-2, :, :]
        hidden_backward = hidden[-1, :, :]
        hidden_concat = torch.cat([hidden_forward, hidden_backward], dim=1)
        
        # Compute latent distribution parameters
        mu = self.fc_mu(hidden_concat)
        logvar = self.fc_logvar(hidden_concat)
        
        return mu, logvar


class TrajectoryDecoder(nn.Module):
    """
    Decoder: Latent vector + Conditions (start, end) → Trajectory sequence
    """
    
    def __init__(self, latent_dim: int = 64, condition_dim: int = 6,
                 hidden_dim: int = 256, output_dim: int = 3,
                 num_layers: int = 2, max_seq_len: int = 50):
        super().__init__()
        
        self.latent_dim = latent_dim
        self.condition_dim = condition_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_layers = num_layers
        self.max_seq_len = max_seq_len
        
        # Project latent + condition to hidden state
        self.fc_init = nn.Linear(latent_dim + condition_dim, hidden_dim * num_layers)
        
        # LSTM decoder
        self.lstm = nn.LSTM(
            input_size=output_dim + latent_dim + condition_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0.0
        )
        
        # Output projection
        self.fc_out = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim // 2, output_dim)
        )
        
    def forward(self, z: torch.Tensor, conditions: torch.Tensor,
                seq_len: int, teacher_forcing_trajectory: Optional[torch.Tensor] = None,
                teacher_forcing_ratio: float = 0.5) -> torch.Tensor:
        """
        Args:
            z: Latent vector [batch_size, latent_dim]
            conditions: Start and end waypoints [batch_size, 6] (start_xyz + end_xyz)
            seq_len: Length of trajectory to generate
            teacher_forcing_trajectory: Ground truth for teacher forcing [batch_size, seq_len, 3]
            teacher_forcing_ratio: Probability of using teacher forcing
            
        Returns:
            trajectory: Generated trajectory [batch_size, seq_len, 3]
        """
        batch_size = z.size(0)
        
        # Initialize hidden state
        init_hidden = self.fc_init(torch.cat([z, conditions], dim=1))
        init_hidden = init_hidden.view(batch_size, self.num_layers, self.hidden_dim)
        init_hidden = init_hidden.transpose(0, 1).contiguous()
        
        h = init_hidden
        c = torch.zeros_like(h)
        
        # Start with the start waypoint
        current_input = conditions[:, :3].unsqueeze(1)  # [batch_size, 1, 3] - start point
        
        outputs = []
        
        # Expand z and conditions for concatenation at each step
        z_expanded = z.unsqueeze(1)  # [batch_size, 1, latent_dim]
        conditions_expanded = conditions.unsqueeze(1)  # [batch_size, 1, 6]
        
        for t in range(seq_len):
            # Concatenate current input with latent and conditions
            lstm_input = torch.cat([current_input, z_expanded, conditions_expanded], dim=2)
            
            # LSTM step
            lstm_out, (h, c) = self.lstm(lstm_input, (h, c))
            
            # Generate output
            output = self.fc_out(lstm_out)
            outputs.append(output)
            
            # Teacher forcing
            use_teacher_forcing = (teacher_forcing_trajectory is not None and 
                                  torch.rand(1).item() < teacher_forcing_ratio)
            
            if use_teacher_forcing and t < seq_len - 1:
                current_input = teacher_forcing_trajectory[:, t:t+1, :]
            else:
                current_input = output
        
        # Concatenate all outputs
        trajectory = torch.cat(outputs, dim=1)
        
        return trajectory


class CVAE_TrajectoryGenerator(nn.Module):
    """
    Complete CVAE model for trajectory generation
    """
    
    def __init__(self, input_dim: int = 3, latent_dim: int = 64,
                 hidden_dim: int = 256, num_layers: int = 2,
                 max_seq_len: int = 50):
        super().__init__()
        
        self.latent_dim = latent_dim
        self.max_seq_len = max_seq_len
        
        # Encoder
        self.encoder = TrajectoryEncoder(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            latent_dim=latent_dim,
            num_layers=num_layers
        )
        
        # Decoder
        self.decoder = TrajectoryDecoder(
            latent_dim=latent_dim,
            condition_dim=6,  # start (3) + end (3)
            hidden_dim=hidden_dim,
            output_dim=input_dim,
            num_layers=num_layers,
            max_seq_len=max_seq_len
        )
        
    def reparameterize(self, mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
        """
        Reparameterization trick: z = μ + σ * ε, where ε ~ N(0,1)
        """
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        z = mu + eps * std
        return z
    
    def forward(self, trajectory: torch.Tensor, start: torch.Tensor, 
                end: torch.Tensor, teacher_forcing_ratio: float = 0.5) -> Tuple:
        """
        Forward pass during training
        
        Args:
            trajectory: Ground truth trajectory [batch_size, seq_len, 3]
            start: Start waypoints [batch_size, 3]
            end: End waypoints [batch_size, 3]
            teacher_forcing_ratio: Ratio for teacher forcing
            
        Returns:
            reconstructed: Reconstructed trajectory
            mu: Latent mean
            logvar: Latent log variance
        """
        # Encode
        mu, logvar = self.encoder(trajectory)
        
        # Reparameterize
        z = self.reparameterize(mu, logvar)
        
        # Decode
        conditions = torch.cat([start, end], dim=1)
        seq_len = trajectory.size(1)
        
        reconstructed = self.decoder(
            z, conditions, seq_len, 
            teacher_forcing_trajectory=trajectory,
            teacher_forcing_ratio=teacher_forcing_ratio
        )
        
        return reconstructed, mu, logvar
    
    def generate(self, start: torch.Tensor, end: torch.Tensor,
                 n_samples: int = 1, seq_len: Optional[int] = None) -> torch.Tensor:
        """
        Generate trajectories from start to end
        
        Args:
            start: Start waypoints [batch_size, 3]
            end: End waypoints [batch_size, 3]
            n_samples: Number of diverse trajectories to generate per start-end pair
            seq_len: Length of trajectory (default: max_seq_len)
            
        Returns:
            trajectories: Generated trajectories [batch_size * n_samples, seq_len, 3]
        """
        self.eval()
        
        with torch.no_grad():
            batch_size = start.size(0)
            seq_len = seq_len or self.max_seq_len
            
            # Repeat start and end for n_samples
            start_repeated = start.repeat_interleave(n_samples, dim=0)
            end_repeated = end.repeat_interleave(n_samples, dim=0)
            
            # Sample from prior
            z = torch.randn(batch_size * n_samples, self.latent_dim, device=start.device)
            
            # Decode
            conditions = torch.cat([start_repeated, end_repeated], dim=1)
            trajectories = self.decoder(z, conditions, seq_len)
            
        return trajectories
    
    def encode(self, trajectory: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Encode trajectory to latent space"""
        return self.encoder(trajectory)


def compute_smoothness_loss(trajectory: torch.Tensor) -> torch.Tensor:
    """
    Compute smoothness loss as curvature penalty
    
    Args:
        trajectory: [batch_size, seq_len, 3]
        
    Returns:
        smoothness_loss: Scalar loss
    """
    # Second derivative (acceleration)
    if trajectory.size(1) < 3:
        return torch.tensor(0.0, device=trajectory.device)
    
    # Compute second differences: p[i+1] - 2*p[i] + p[i-1]
    first_diff = trajectory[:, 1:, :] - trajectory[:, :-1, :]
    second_diff = first_diff[:, 1:, :] - first_diff[:, :-1, :]
    
    # L2 norm of second differences
    smoothness_loss = torch.mean(torch.sum(second_diff ** 2, dim=2))
    
    return smoothness_loss


def compute_boundary_loss(trajectory: torch.Tensor, start: torch.Tensor, 
                         end: torch.Tensor) -> torch.Tensor:
    """
    Enforce boundary conditions: trajectory[0] = start, trajectory[-1] = end
    
    Args:
        trajectory: [batch_size, seq_len, 3]
        start: [batch_size, 3]
        end: [batch_size, 3]
        
    Returns:
        boundary_loss: Scalar loss
    """
    start_loss = F.mse_loss(trajectory[:, 0, :], start)
    end_loss = F.mse_loss(trajectory[:, -1, :], end)
    
    return start_loss + end_loss


def compute_kl_divergence(mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
    """
    Compute KL divergence: KL(N(μ, σ²) || N(0, 1))
    
    Args:
        mu: Mean [batch_size, latent_dim]
        logvar: Log variance [batch_size, latent_dim]
        
    Returns:
        kl_loss: Scalar loss
    """
    # KL = -0.5 * sum(1 + log(σ²) - μ² - σ²)
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    kl_loss = kl_loss / mu.size(0)  # Average over batch
    
    return kl_loss


class TrajectoryLoss(nn.Module):
    """
    Combined loss for trajectory generation
    """
    
    def __init__(self, beta: float = 0.001, lambda_smooth: float = 0.1,
                 lambda_boundary: float = 1.0):
        super().__init__()
        self.beta = beta
        self.lambda_smooth = lambda_smooth
        self.lambda_boundary = lambda_boundary
        
    def forward(self, reconstructed: torch.Tensor, target: torch.Tensor,
                mu: torch.Tensor, logvar: torch.Tensor,
                start: torch.Tensor, end: torch.Tensor) -> Tuple:
        """
        Compute combined loss
        
        Args:
            reconstructed: Predicted trajectory [batch_size, seq_len, 3]
            target: Ground truth trajectory [batch_size, seq_len, 3]
            mu: Latent mean [batch_size, latent_dim]
            logvar: Latent log variance [batch_size, latent_dim]
            start: Start waypoints [batch_size, 3]
            end: End waypoints [batch_size, 3]
            
        Returns:
            total_loss: Combined loss
            loss_dict: Dictionary of individual losses
        """
        # Reconstruction loss
        recon_loss = F.mse_loss(reconstructed, target)
        
        # KL divergence
        kl_loss = compute_kl_divergence(mu, logvar)
        
        # Smoothness loss
        smooth_loss = compute_smoothness_loss(reconstructed)
        
        # Boundary loss
        boundary_loss = compute_boundary_loss(reconstructed, start, end)
        
        # Total loss
        total_loss = (recon_loss + 
                     self.beta * kl_loss + 
                     self.lambda_smooth * smooth_loss +
                     self.lambda_boundary * boundary_loss)
        
        loss_dict = {
            'total': total_loss.item(),
            'reconstruction': recon_loss.item(),
            'kl': kl_loss.item(),
            'smoothness': smooth_loss.item(),
            'boundary': boundary_loss.item()
        }
        
        return total_loss, loss_dict


def create_model(latent_dim: int = 64, hidden_dim: int = 256,
                num_layers: int = 2, max_seq_len: int = 50) -> CVAE_TrajectoryGenerator:
    """
    Factory function to create model
    
    Args:
        latent_dim: Dimension of latent space
        hidden_dim: Hidden dimension for LSTM
        num_layers: Number of LSTM layers
        max_seq_len: Maximum sequence length
        
    Returns:
        model: CVAE trajectory generator model
    """
    model = CVAE_TrajectoryGenerator(
        input_dim=3,
        latent_dim=latent_dim,
        hidden_dim=hidden_dim,
        num_layers=num_layers,
        max_seq_len=max_seq_len
    )
    
    return model


if __name__ == '__main__':
    # Test model
    print("Testing CVAE Trajectory Generator...")
    
    model = create_model(latent_dim=64, hidden_dim=256, num_layers=2, max_seq_len=50)
    
    # Create dummy data
    batch_size = 8
    seq_len = 50
    
    trajectory = torch.randn(batch_size, seq_len, 3)
    start = torch.randn(batch_size, 3)
    end = torch.randn(batch_size, 3)
    
    # Forward pass
    reconstructed, mu, logvar = model(trajectory, start, end)
    
    print(f"Input trajectory shape: {trajectory.shape}")
    print(f"Reconstructed trajectory shape: {reconstructed.shape}")
    print(f"Latent mu shape: {mu.shape}")
    print(f"Latent logvar shape: {logvar.shape}")
    
    # Test generation
    generated = model.generate(start, end, n_samples=3)
    print(f"Generated trajectories shape: {generated.shape}")
    
    # Test loss
    criterion = TrajectoryLoss()
    loss, loss_dict = criterion(reconstructed, trajectory, mu, logvar, start, end)
    print(f"\nLoss breakdown:")
    for k, v in loss_dict.items():
        print(f"  {k}: {v:.4f}")
    
    # Count parameters
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\nTotal trainable parameters: {n_params:,}")
    
    print("\n✓ Model test successful!")

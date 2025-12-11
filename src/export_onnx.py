"""
Export trained model to ONNX format for deployment
"""

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings

# Filter warnings before NumPy import to suppress MINGW-W64 build warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

import torch
import torch.onnx
import numpy as np
import onnx
import onnxruntime as ort
import argparse
import os

from .model import create_model


class ONNXExporter:
    """Export PyTorch model to ONNX"""
    
    def __init__(self, checkpoint_path: str, device: str = 'cpu'):
        """
        Initialize exporter
        
        Args:
            checkpoint_path: Path to PyTorch checkpoint
            device: Device to load model on
        """
        self.device = torch.device(device)
        
        # Load checkpoint
        print(f"Loading model from {checkpoint_path}...")
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        
        # Extract model args
        model_args = checkpoint['args']
        
        # Create model
        self.model = create_model(
            latent_dim=model_args.get('latent_dim', 64),
            hidden_dim=model_args.get('hidden_dim', 256),
            num_layers=model_args.get('num_layers', 2),
            max_seq_len=50
        )
        
        # Load weights
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Store normalization parameters
        self.normalization = checkpoint['normalization']
        
        print(f"✓ Model loaded successfully")
    
    def export_generator(self, output_path: str, seq_len: int = 50,
                        opset_version: int = 12):
        """
        Export the generator (decoder) part to ONNX
        
        Args:
            output_path: Path to save ONNX model
            seq_len: Sequence length for trajectories
            opset_version: ONNX opset version
        """
        print(f"\nExporting generator to ONNX...")
        print(f"Output path: {output_path}")
        print(f"Sequence length: {seq_len}")
        
        # Create dummy inputs
        batch_size = 1
        latent_dim = self.model.latent_dim
        
        z = torch.randn(batch_size, latent_dim, device=self.device)
        start = torch.randn(batch_size, 3, device=self.device)
        end = torch.randn(batch_size, 3, device=self.device)
        conditions = torch.cat([start, end], dim=1)
        
        # Prepare model for export
        class GeneratorWrapper(torch.nn.Module):
            """Wrapper for generator that's more ONNX-friendly"""
            
            def __init__(self, decoder, seq_len):
                super().__init__()
                self.decoder = decoder
                self.seq_len = seq_len
            
            def forward(self, z, start, end):
                conditions = torch.cat([start, end], dim=1)
                trajectory = self.decoder(z, conditions, self.seq_len)
                return trajectory
        
        wrapped_model = GeneratorWrapper(self.model.decoder, seq_len)
        wrapped_model.eval()
        
        # Export to ONNX (using legacy exporter for compatibility)
        with torch.no_grad():
            torch.onnx.export(
                wrapped_model,
                (z, start, end),
                output_path,
                export_params=True,
                opset_version=opset_version,
                do_constant_folding=True,
                input_names=['latent', 'start', 'end'],
                output_names=['trajectory'],
                dynamic_axes={
                    'latent': {0: 'batch_size'},
                    'start': {0: 'batch_size'},
                    'end': {0: 'batch_size'},
                    'trajectory': {0: 'batch_size'}
                },
                dynamo=False  # Use legacy JIT-based exporter
            )
        
        print(f"✓ ONNX model exported to {output_path}")
        
        # Verify the model
        self._verify_onnx_model(output_path, z, start, end)
        
        # Save normalization parameters alongside
        norm_path = output_path.replace('.onnx', '_normalization.json')
        import json
        with open(norm_path, 'w') as f:
            json.dump(self.normalization, f, indent=2)
        print(f"✓ Normalization parameters saved to {norm_path}")
    
    def _verify_onnx_model(self, onnx_path: str, z: torch.Tensor,
                          start: torch.Tensor, end: torch.Tensor):
        """Verify ONNX model by comparing outputs"""
        print("\nVerifying ONNX model...")
        
        # Load ONNX model
        onnx_model = onnx.load(onnx_path)
        onnx.checker.check_model(onnx_model)
        print("✓ ONNX model is valid")
        
        # Run inference with ONNX Runtime
        ort_session = ort.InferenceSession(onnx_path)
        
        # Prepare inputs
        ort_inputs = {
            'latent': z.cpu().numpy(),
            'start': start.cpu().numpy(),
            'end': end.cpu().numpy()
        }
        
        # Run ONNX inference
        ort_outputs = ort_session.run(None, ort_inputs)
        onnx_trajectory = ort_outputs[0]
        
        # Run PyTorch inference
        with torch.no_grad():
            conditions = torch.cat([start, end], dim=1)
            pytorch_trajectory = self.model.decoder(z, conditions, 50).cpu().numpy()
        
        # Compare
        max_diff = np.abs(onnx_trajectory - pytorch_trajectory).max()
        mean_diff = np.abs(onnx_trajectory - pytorch_trajectory).mean()
        
        print(f"✓ Verification complete:")
        print(f"  Max difference: {max_diff:.6f}")
        print(f"  Mean difference: {mean_diff:.6f}")
        
        if max_diff < 1e-4:
            print("  ✓ ONNX model matches PyTorch (excellent)")
        elif max_diff < 1e-3:
            print("  ✓ ONNX model matches PyTorch (good)")
        else:
            print("  ⚠ Warning: Large difference between ONNX and PyTorch")


def test_onnx_inference(onnx_path: str, normalization_path: str):
    """
    Test ONNX model inference
    
    Args:
        onnx_path: Path to ONNX model
        normalization_path: Path to normalization parameters
    """
    print("\n" + "="*60)
    print("Testing ONNX Inference")
    print("="*60)
    
    # Load normalization
    import json
    with open(normalization_path, 'r') as f:
        normalization = json.load(f)
    
    mean = np.array(normalization['mean'], dtype=np.float32)
    std = np.array(normalization['std'], dtype=np.float32)
    
    print(f"Loaded normalization: mean={mean}, std={std}")
    
    # Create ONNX Runtime session
    ort_session = ort.InferenceSession(onnx_path)
    
    # Get input/output info
    print("\nModel inputs:")
    for inp in ort_session.get_inputs():
        print(f"  {inp.name}: {inp.shape} ({inp.type})")
    
    print("\nModel outputs:")
    for out in ort_session.get_outputs():
        print(f"  {out.name}: {out.shape} ({out.type})")
    
    # Test inference
    print("\nRunning test inference...")
    
    # Create test inputs (unnormalized)
    start = np.array([[0.0, 0.0, 100.0]], dtype=np.float32)
    end = np.array([[800.0, 600.0, 200.0]], dtype=np.float32)
    
    # Normalize
    start_norm = (start - mean) / std
    end_norm = (end - mean) / std
    
    # Sample latent vector
    latent_dim = ort_session.get_inputs()[0].shape[1]
    z = np.random.randn(1, latent_dim).astype(np.float32)
    
    # Run inference
    ort_inputs = {
        'latent': z,
        'start': start_norm,
        'end': end_norm
    }
    
    ort_outputs = ort_session.run(None, ort_inputs)
    trajectory_norm = ort_outputs[0]
    
    # Denormalize
    trajectory = trajectory_norm * std + mean
    
    print(f"\nGenerated trajectory shape: {trajectory.shape}")
    print(f"Start point: {trajectory[0, 0, :]}")
    print(f"End point: {trajectory[0, -1, :]}")
    print(f"Expected start: {start[0]}")
    print(f"Expected end: {end[0]}")
    
    # Compute errors
    start_error = np.linalg.norm(trajectory[0, 0, :] - start[0])
    end_error = np.linalg.norm(trajectory[0, -1, :] - end[0])
    
    print(f"\nBoundary errors:")
    print(f"  Start: {start_error:.2f} m")
    print(f"  End: {end_error:.2f} m")
    
    print("\n✓ ONNX inference test successful!")


def main():
    """Main export script"""
    parser = argparse.ArgumentParser(description='Export model to ONNX')
    parser.add_argument('--checkpoint', type=str, default='models/best_model.pth',
                       help='Path to PyTorch checkpoint')
    parser.add_argument('--output', type=str, default='models/trajectory_generator.onnx',
                       help='Output ONNX file path')
    parser.add_argument('--seq_len', type=int, default=50,
                       help='Trajectory sequence length')
    parser.add_argument('--device', type=str, default='cpu',
                       choices=['cpu', 'cuda'], help='Device to use')
    parser.add_argument('--test', action='store_true',
                       help='Test ONNX model after export')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Export
    exporter = ONNXExporter(args.checkpoint, device=args.device)
    exporter.export_generator(args.output, seq_len=args.seq_len)
    
    # Test if requested
    if args.test:
        norm_path = args.output.replace('.onnx', '_normalization.json')
        test_onnx_inference(args.output, norm_path)
    
    print("\n" + "="*60)
    print("Export Complete!")
    print("="*60)
    print(f"\nONNX model: {args.output}")
    print(f"Normalization: {args.output.replace('.onnx', '_normalization.json')}")
    print("\nYou can now use this model with:")
    print("  - ONNX Runtime (Python/C++)")
    print("  - TensorRT")
    print("  - Other ONNX-compatible frameworks")
    print("="*60)


if __name__ == '__main__':
    main()

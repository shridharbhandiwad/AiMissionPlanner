"""
FastAPI Microservice for Trajectory Generation
Provides REST API for trajectory generation and evaluation
"""

# Suppress NumPy MINGW-W64 warnings on Windows
import warnings

# Filter warnings before NumPy import to suppress MINGW-W64 build warnings
warnings.filterwarnings('ignore', message='.*MINGW-W64.*')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')
warnings.filterwarnings('ignore', message='.*invalid value encountered.*')

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import numpy as np
import torch
import uvicorn
import os
import sys
import json
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.inference import TrajectoryPredictor, evaluate_trajectory_quality


# Pydantic models for API
class Waypoint(BaseModel):
    """3D waypoint"""
    x: float = Field(..., description="X coordinate in meters")
    y: float = Field(..., description="Y coordinate in meters")
    z: float = Field(..., description="Z coordinate in meters")


class Obstacle(BaseModel):
    """Obstacle definition"""
    center: Waypoint
    radius: float = Field(..., gt=0, description="Obstacle radius in meters")


class TrajectoryRequest(BaseModel):
    """Request for trajectory generation"""
    start: Waypoint
    end: Waypoint
    n_samples: int = Field(1, ge=1, le=20, description="Number of trajectories to generate")
    seq_len: int = Field(50, ge=10, le=100, description="Trajectory sequence length")
    obstacles: Optional[List[Obstacle]] = Field(None, description="Optional obstacles")


class TrajectoryMetrics(BaseModel):
    """Trajectory quality metrics"""
    path_length: float
    straight_line_distance: float
    path_efficiency: float
    avg_curvature: float
    max_curvature: float
    smoothness_score: float
    avg_velocity: float
    min_altitude: float
    max_altitude: float
    avg_altitude: float


class TrajectoryData(BaseModel):
    """Single trajectory data"""
    waypoints: List[List[float]]
    metrics: TrajectoryMetrics


class TrajectoryResponse(BaseModel):
    """Response containing generated trajectories"""
    success: bool
    trajectories: List[TrajectoryData]
    start: Waypoint
    end: Waypoint
    n_samples: int
    inference_time_ms: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    version: str


# Initialize FastAPI app
app = FastAPI(
    title="Trajectory Generation API",
    description="AI-powered trajectory generation for defence mission planning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global predictor instance
predictor: Optional[TrajectoryPredictor] = None
MODEL_PATH = os.getenv("MODEL_PATH", "models/best_model.pth")
DEVICE = os.getenv("DEVICE", "cpu")


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global predictor
    
    print("="*60)
    print("Starting Trajectory Generation API")
    print("="*60)
    print(f"Model path: {MODEL_PATH}")
    print(f"Device: {DEVICE}")
    
    try:
        if os.path.exists(MODEL_PATH):
            predictor = TrajectoryPredictor(MODEL_PATH, device=DEVICE)
            print("✓ Model loaded successfully")
        else:
            print(f"⚠ Warning: Model not found at {MODEL_PATH}")
            print("  API will start but trajectory generation will fail")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("  API will start but trajectory generation will fail")
    
    print("="*60)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return {
        "status": "running",
        "model_loaded": predictor is not None,
        "version": "1.0.0"
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy" if predictor is not None else "model_not_loaded",
        "model_loaded": predictor is not None,
        "version": "1.0.0"
    }


@app.post("/generate", response_model=TrajectoryResponse)
async def generate_trajectory(request: TrajectoryRequest):
    """
    Generate trajectory from start to end waypoint
    
    Args:
        request: Trajectory generation request
        
    Returns:
        Generated trajectories with metrics
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert to numpy arrays
        start = np.array([request.start.x, request.start.y, request.start.z])
        end = np.array([request.end.x, request.end.y, request.end.z])
        
        # Measure inference time
        import time
        t_start = time.time()
        
        # Generate trajectories
        trajectories = predictor.predict_single(
            start, end, 
            n_samples=request.n_samples,
            seq_len=request.seq_len
        )
        
        inference_time = (time.time() - t_start) * 1000  # Convert to ms
        
        # Process trajectories
        trajectory_data = []
        
        for traj in trajectories:
            # Compute metrics
            metrics = evaluate_trajectory_quality(traj)
            
            trajectory_data.append(TrajectoryData(
                waypoints=traj.tolist(),
                metrics=TrajectoryMetrics(**metrics)
            ))
        
        return TrajectoryResponse(
            success=True,
            trajectories=trajectory_data,
            start=request.start,
            end=request.end,
            n_samples=request.n_samples,
            inference_time_ms=inference_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/generate_with_obstacles")
async def generate_with_obstacles(request: TrajectoryRequest):
    """
    Generate trajectories avoiding obstacles
    
    Args:
        request: Trajectory request with obstacles
        
    Returns:
        Generated trajectories ranked by safety score
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not request.obstacles:
        # No obstacles, use regular generation
        return await generate_trajectory(request)
    
    try:
        # Convert to numpy arrays
        start = np.array([request.start.x, request.start.y, request.start.z])
        end = np.array([request.end.x, request.end.y, request.end.z])
        
        # Convert obstacles
        obstacles = [
            {
                'center': np.array([obs.center.x, obs.center.y, obs.center.z]),
                'radius': obs.radius
            }
            for obs in request.obstacles
        ]
        
        # Generate with obstacle avoidance
        import time
        t_start = time.time()
        
        trajectories, scores = predictor.predict_with_obstacles(
            start, end, obstacles,
            n_candidates=request.n_samples,
            seq_len=request.seq_len
        )
        
        inference_time = (time.time() - t_start) * 1000
        
        # Process trajectories
        trajectory_data = []
        
        for traj, score in zip(trajectories, scores):
            metrics = evaluate_trajectory_quality(traj)
            metrics['safety_score'] = float(score)
            
            trajectory_data.append({
                'waypoints': traj.tolist(),
                'metrics': metrics,
                'safety_score': float(score)
            })
        
        return {
            'success': True,
            'trajectories': trajectory_data,
            'start': request.start.dict(),
            'end': request.end.dict(),
            'n_samples': request.n_samples,
            'obstacles': [obs.dict() for obs in request.obstacles],
            'inference_time_ms': inference_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/visualize")
async def visualize_trajectory(request: TrajectoryRequest):
    """
    Generate and visualize trajectory
    
    Returns:
        Base64 encoded PNG image
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert to numpy arrays
        start = np.array([request.start.x, request.start.y, request.start.z])
        end = np.array([request.end.x, request.end.y, request.end.z])
        
        # Generate trajectory
        trajectories = predictor.predict_single(start, end, n_samples=request.n_samples)
        
        # Create visualization
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot trajectories
        colors = plt.cm.rainbow(np.linspace(0, 1, len(trajectories)))
        
        for traj, color in zip(trajectories, colors):
            ax.plot(traj[:, 0], traj[:, 1], traj[:, 2],
                   color=color, linewidth=2, alpha=0.7)
        
        # Plot start and end
        ax.scatter(*start, c='green', s=200, marker='o', label='Start')
        ax.scatter(*end, c='red', s=200, marker='s', label='End')
        
        # Plot obstacles if provided
        if request.obstacles:
            for obs in request.obstacles:
                u = np.linspace(0, 2 * np.pi, 20)
                v = np.linspace(0, np.pi, 20)
                
                center = np.array([obs.center.x, obs.center.y, obs.center.z])
                x = obs.radius * np.outer(np.cos(u), np.sin(v)) + center[0]
                y = obs.radius * np.outer(np.sin(u), np.sin(v)) + center[1]
                z = obs.radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
                
                ax.plot_surface(x, y, z, color='red', alpha=0.3)
        
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        ax.set_title('Generated Trajectories')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        # Encode to base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        return {
            'success': True,
            'image': img_base64,
            'format': 'png'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visualization failed: {str(e)}")


@app.get("/info")
async def model_info():
    """Get model information"""
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        'model_loaded': True,
        'device': DEVICE,
        'model_path': MODEL_PATH,
        'seq_len': predictor.model.max_seq_len,
        'latent_dim': predictor.model.latent_dim
    }


def main():
    """Run the API server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Trajectory Generation API Server')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                       help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000,
                       help='Port to bind to')
    parser.add_argument('--model', type=str, default='models/best_model.pth',
                       help='Path to model checkpoint')
    parser.add_argument('--device', type=str, default='cpu',
                       choices=['cpu', 'cuda'], help='Device to run on')
    parser.add_argument('--reload', action='store_true',
                       help='Enable auto-reload for development')
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ['MODEL_PATH'] = args.model
    os.environ['DEVICE'] = args.device
    
    # Run server
    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == '__main__':
    main()

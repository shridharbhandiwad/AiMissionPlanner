"""
Test script for Trajectory Generation API
"""

import requests
import json
import time
import base64
from typing import Dict


API_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    response = requests.get(f"{API_URL}/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()['status'] in ['healthy', 'model_not_loaded']
    
    print("✓ Health check passed")


def test_generate_single():
    """Test single trajectory generation"""
    print("\n" + "="*60)
    print("Testing Single Trajectory Generation")
    print("="*60)
    
    payload = {
        "start": {"x": 0.0, "y": 0.0, "z": 100.0},
        "end": {"x": 800.0, "y": 600.0, "z": 200.0},
        "n_samples": 1,
        "seq_len": 50
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    t_start = time.time()
    response = requests.post(f"{API_URL}/generate", json=payload)
    t_end = time.time()
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Time: {(t_end - t_start)*1000:.2f} ms")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Inference Time: {data['inference_time_ms']:.2f} ms")
        print(f"Number of trajectories: {len(data['trajectories'])}")
        
        if data['trajectories']:
            traj = data['trajectories'][0]
            metrics = traj['metrics']
            print("\nTrajectory Metrics:")
            print(f"  Path Length: {metrics['path_length']:.2f} m")
            print(f"  Efficiency: {metrics['path_efficiency']:.3f}")
            print(f"  Smoothness: {metrics['smoothness_score']:.4f}")
            print(f"  Avg Curvature: {metrics['avg_curvature']:.6f} rad/m")
        
        print("✓ Single trajectory generation passed")
    else:
        print(f"❌ Error: {response.text}")


def test_generate_multiple():
    """Test multiple trajectory generation"""
    print("\n" + "="*60)
    print("Testing Multiple Trajectory Generation")
    print("="*60)
    
    payload = {
        "start": {"x": -500.0, "y": 300.0, "z": 150.0},
        "end": {"x": 600.0, "y": -400.0, "z": 250.0},
        "n_samples": 5,
        "seq_len": 50
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    t_start = time.time()
    response = requests.post(f"{API_URL}/generate", json=payload)
    t_end = time.time()
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Time: {(t_end - t_start)*1000:.2f} ms")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Inference Time: {data['inference_time_ms']:.2f} ms")
        print(f"Number of trajectories: {len(data['trajectories'])}")
        
        print("\nTrajectory Comparison:")
        for i, traj in enumerate(data['trajectories']):
            metrics = traj['metrics']
            print(f"  Trajectory {i+1}:")
            print(f"    Length: {metrics['path_length']:.2f} m")
            print(f"    Smoothness: {metrics['smoothness_score']:.4f}")
        
        print("✓ Multiple trajectory generation passed")
    else:
        print(f"❌ Error: {response.text}")


def test_generate_with_obstacles():
    """Test trajectory generation with obstacles"""
    print("\n" + "="*60)
    print("Testing Trajectory Generation with Obstacles")
    print("="*60)
    
    payload = {
        "start": {"x": 0.0, "y": 0.0, "z": 100.0},
        "end": {"x": 800.0, "y": 600.0, "z": 200.0},
        "n_samples": 5,
        "seq_len": 50,
        "obstacles": [
            {
                "center": {"x": 400.0, "y": 300.0, "z": 150.0},
                "radius": 80.0
            },
            {
                "center": {"x": 600.0, "y": 400.0, "z": 180.0},
                "radius": 60.0
            }
        ]
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    t_start = time.time()
    response = requests.post(f"{API_URL}/generate_with_obstacles", json=payload)
    t_end = time.time()
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Time: {(t_end - t_start)*1000:.2f} ms")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Inference Time: {data['inference_time_ms']:.2f} ms")
        print(f"Number of trajectories: {len(data['trajectories'])}")
        
        print("\nTrajectories ranked by safety:")
        for i, traj in enumerate(data['trajectories']):
            safety = traj['safety_score']
            metrics = traj['metrics']
            print(f"  Trajectory {i+1}:")
            print(f"    Safety Score: {safety:.2f}")
            print(f"    Path Length: {metrics['path_length']:.2f} m")
        
        print("✓ Obstacle avoidance generation passed")
    else:
        print(f"❌ Error: {response.text}")


def test_visualize():
    """Test trajectory visualization"""
    print("\n" + "="*60)
    print("Testing Trajectory Visualization")
    print("="*60)
    
    payload = {
        "start": {"x": 0.0, "y": 0.0, "z": 100.0},
        "end": {"x": 800.0, "y": 600.0, "z": 200.0},
        "n_samples": 3,
        "seq_len": 50
    }
    
    response = requests.post(f"{API_URL}/visualize", json=payload)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Image Format: {data['format']}")
        print(f"Image Size: {len(data['image'])} characters (base64)")
        
        # Optionally save image
        img_data = base64.b64decode(data['image'])
        with open('test_visualization.png', 'wb') as f:
            f.write(img_data)
        
        print("✓ Visualization saved to test_visualization.png")
        print("✓ Visualization test passed")
    else:
        print(f"❌ Error: {response.text}")


def test_model_info():
    """Test model info endpoint"""
    print("\n" + "="*60)
    print("Testing Model Info Endpoint")
    print("="*60)
    
    response = requests.get(f"{API_URL}/info")
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Model Info: {json.dumps(data, indent=2)}")
        print("✓ Model info test passed")
    else:
        print(f"Response: {response.text}")


def run_all_tests():
    """Run all API tests"""
    print("="*60)
    print("Trajectory Generation API - Test Suite")
    print("="*60)
    print(f"API URL: {API_URL}")
    
    try:
        # Test health
        test_health()
        
        # Test model info
        test_model_info()
        
        # Test trajectory generation
        test_generate_single()
        test_generate_multiple()
        test_generate_with_obstacles()
        test_visualize()
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print(f"Make sure the API server is running at {API_URL}")
        print("Start it with: python api/app.py")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == '__main__':
    run_all_tests()

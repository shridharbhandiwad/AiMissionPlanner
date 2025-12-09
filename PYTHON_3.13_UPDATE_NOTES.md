# Python 3.13 Compatibility Updates

## Overview
The original `requirements.txt` had dependency conflicts with Python 3.13. This document outlines the changes made to ensure compatibility.

## Critical Issues Fixed

### 1. scipy Version Error
- **Problem**: `scipy==1.11.3` does not exist in PyPI
- **Solution**: Updated to `scipy==1.11.4` (the actual available version)

### 2. Python 3.13 Compatibility
Many packages specified in the original requirements had maximum Python version constraints (<3.13). Updated to versions with Python 3.13 support.

## Updated Packages

| Package | Old Version | New Version | Reason |
|---------|-------------|-------------|---------|
| scipy | 1.11.3 | 1.11.4 | Version 1.11.3 doesn't exist |
| pandas | 2.1.1 | 2.2.0 | Python 3.13 support |
| scikit-learn | 1.3.1 | 1.4.0 | Python 3.13 support |
| matplotlib | 3.8.0 | 3.9.0 | Python 3.13 support |
| plotly | 5.17.0 | 5.24.0 | Newer stable version |
| onnx | 1.14.1 | 1.17.0 | Python 3.13 support |
| onnxruntime | 1.16.0 | 1.20.0 | Python 3.13 support (1.19.0 not available) |
| fastapi | 0.104.0 | 0.115.0 | Python 3.13 support |
| uvicorn | 0.23.2 | 0.30.0 | Python 3.13 support |
| pydantic | 2.4.2 | 2.9.0 | Python 3.13 support |
| python-multipart | 0.0.6 | 0.0.12 | Newer stable version |
| shapely | 2.0.2 | 2.0.6 | Newer stable version |
| pytest | 7.4.2 | 8.3.0 | Python 3.13 support |

## Packages Unchanged

The following packages remain at their original versions as they are compatible with Python 3.13:
- torch==2.9.1
- torchvision==0.24.1
- numpy==1.26.4
- seaborn==0.13.0
- tensorboard==2.18.0
- tqdm==4.66.1

## Packages Removed

- **bezier==2023.7.28**: Removed due to Python 3.13 incompatibility (only supports up to 3.11). The package was not actually used in the codebase - `src/data_generator.py` contains a custom Bézier curve implementation using numpy's Bernstein polynomials.

## Installation Instructions

### For Windows (your environment)
```bash
pip install -r requirements.txt
```

### For Linux/Mac
```bash
pip install -r requirements.txt
```

### If you encounter issues
Try installing PyTorch separately first (especially if you need CUDA support):

**For CPU only:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

**For CUDA 11.8:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

**For CUDA 12.1:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

## Testing Compatibility

After installation, verify the packages work correctly:

```python
import torch
import numpy as np
import scipy
import pandas as pd
import sklearn
import matplotlib
import onnx
import onnxruntime

print(f"PyTorch: {torch.__version__}")
print(f"NumPy: {np.__version__}")
print(f"SciPy: {scipy.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Scikit-learn: {sklearn.__version__}")
print(f"Python: {import sys; sys.version}")
```

## Alternative: Use Python 3.11 or 3.12

If you encounter continued issues with Python 3.13, consider using Python 3.11 or 3.12, which have broader package support:

```bash
# Create new conda environment with Python 3.11
conda create -n missionplannerenv python=3.11
conda activate missionplannerenv
pip install -r requirements.txt
```

## Notes

- All version updates maintain backward compatibility with the project's API
- The updated versions include bug fixes and performance improvements
- PyTorch 2.9.1 has official Python 3.13 support for Windows

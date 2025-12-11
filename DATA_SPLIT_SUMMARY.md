# Trajectory Data Split - Summary Report

**Date**: December 11, 2025  
**Task**: Split trajectory data into training, testing, and evaluation sets in CSV format  
**Status**: ✅ Complete

---

## Overview

The trajectory dataset has been successfully split into three sets and exported to CSV format for easy access and analysis.

## Data Split Distribution

| Split      | Samples | Percentage | File Size |
|------------|---------|------------|-----------|
| Training   | 35,000  | 70%        | 52.24 MB  |
| Testing    | 7,500   | 15%        | 11.19 MB  |
| Evaluation | 7,500   | 15%        | 11.19 MB  |
| **Total**  | **50,000** | **100%** | **74.62 MB** |

Additional file: `trajectories_summary.csv` (7.57 MB) contains computed metrics for all trajectories.

---

## Output Files

All CSV files are located in: `/workspace/data/csv/`

### 1. Training Data
- **File**: `train_trajectories.csv`
- **Size**: 52.24 MB
- **Rows**: 35,000
- **Columns**: 158 (8 metadata + 150 trajectory points)

### 2. Testing Data
- **File**: `test_trajectories.csv`
- **Size**: 11.19 MB
- **Rows**: 7,500
- **Columns**: 158 (8 metadata + 150 trajectory points)

### 3. Evaluation Data
- **File**: `eval_trajectories.csv`
- **Size**: 11.19 MB
- **Rows**: 7,500
- **Columns**: 158 (8 metadata + 150 trajectory points)

### 4. Summary Statistics
- **File**: `trajectories_summary.csv`
- **Size**: 7.57 MB
- **Rows**: 50,000
- **Columns**: 17 (computed metrics for each trajectory)

---

## CSV File Structure

### Trajectory Files (train/test/eval_trajectories.csv)

Each row contains one complete 3D trajectory with the following columns:

#### Metadata (8 columns)
- `sample_id`: Unique identifier
- `start_x`, `start_y`, `start_z`: Starting coordinates (meters)
- `end_x`, `end_y`, `end_z`: Ending coordinates (meters)
- `method_type`: Generation method (bezier/spline/dubins)

#### Trajectory Points (150 columns)
- `point_0_x`, `point_0_y`, `point_0_z` through `point_49_x`, `point_49_y`, `point_49_z`
- Total: 50 waypoints × 3 dimensions = 150 columns

### Summary File (trajectories_summary.csv)

Contains computed metrics for each trajectory:
- Sample identification (id, split, method)
- Start/end coordinates
- Path metrics (length, straight-line distance, ratio)
- Geometric metrics (curvature, smoothness)
- Altitude statistics (min, max, mean)

---

## Dataset Statistics

### Training Set (35,000 samples)

| Metric                    | Mean     | Std Dev  |
|---------------------------|----------|----------|
| Path Length (m)           | 1,346.83 | 694.90   |
| Straight Distance (m)     | 1,074.38 | 477.36   |
| Path Length Ratio         | 1.26     | 0.32     |
| Average Curvature (rad/m) | 0.091    | 1.497    |
| Smoothness Score          | 0.9615   | 0.0891   |
| Mean Altitude (m)         | 274.76   | 91.41    |

**Method Distribution:**
- Bezier: 11,654 (33.3%)
- Spline: 11,669 (33.3%)
- Dubins: 11,677 (33.4%)

### Testing Set (7,500 samples)

| Metric                    | Mean     | Std Dev  |
|---------------------------|----------|----------|
| Path Length (m)           | 1,335.67 | 687.48   |
| Straight Distance (m)     | 1,067.27 | 473.41   |
| Path Length Ratio         | 1.26     | 0.31     |
| Average Curvature (rad/m) | 0.083    | 0.934    |
| Smoothness Score          | 0.9621   | 0.0876   |
| Mean Altitude (m)         | 276.02   | 90.86    |

**Method Distribution:**
- Bezier: 2,502 (33.4%)
- Spline: 2,514 (33.5%)
- Dubins: 2,484 (33.1%)

### Evaluation Set (7,500 samples)

| Metric                    | Mean     | Std Dev  |
|---------------------------|----------|----------|
| Path Length (m)           | 1,350.41 | 684.61   |
| Straight Distance (m)     | 1,078.26 | 470.46   |
| Path Length Ratio         | 1.26     | 0.31     |
| Average Curvature (rad/m) | 0.112    | 2.991    |
| Smoothness Score          | 0.9611   | 0.0905   |
| Mean Altitude (m)         | 274.88   | 91.76    |

**Method Distribution:**
- Bezier: 2,511 (33.5%)
- Spline: 2,484 (33.1%)
- Dubins: 2,505 (33.4%)

---

## Data Characteristics

### Spatial Bounds
- **X coordinate**: -1,000 to 1,000 meters
- **Y coordinate**: -1,000 to 1,000 meters  
- **Z coordinate (altitude)**: 50 to 500 meters (typical range)

### Trajectory Properties
- **Points per trajectory**: 50 waypoints
- **Dimensions**: 3D (x, y, z)
- **Generation methods**: Bezier curves, Cubic splines, Dubins-like paths

---

## Usage Examples

### Python (pandas)

```python
import pandas as pd
import numpy as np

# Load training data
train_df = pd.read_csv('data/csv/train_trajectories.csv')

# Get a single trajectory
sample = train_df.iloc[0]
sample_id = sample['sample_id']
method = sample['method_type']

# Extract trajectory points
trajectory = np.zeros((50, 3))
for i in range(50):
    trajectory[i] = [sample[f'point_{i}_x'], 
                     sample[f'point_{i}_y'], 
                     sample[f'point_{i}_z']]

# Load summary with metrics
summary_df = pd.read_csv('data/csv/trajectories_summary.csv')
train_summary = summary_df[summary_df['split'] == 'train']

# Analyze by method
print(train_summary.groupby('method_type')['path_length'].mean())
```

### R

```r
# Load data
train_data <- read.csv('data/csv/train_trajectories.csv')
summary_data <- read.csv('data/csv/trajectories_summary.csv')

# Filter by split
train_summary <- subset(summary_data, split == 'train')

# Summary by method
aggregate(path_length ~ method_type, data=train_summary, FUN=mean)
```

### Excel/Google Sheets

All CSV files can be opened directly in spreadsheet software. Note that large files (training set) may be slow to load.

---

## Files Created

### Main Scripts
1. **`split_data_to_csv.py`** - Main script that splits data and exports to CSV
2. **`examples/load_csv_data.py`** - Example script demonstrating how to load and use the CSV data

### Documentation
1. **`data/csv/README.md`** - Detailed documentation of CSV format and structure
2. **`DATA_SPLIT_SUMMARY.md`** - This summary document

### Data Files
1. **`data/csv/train_trajectories.csv`** - Training set (70%)
2. **`data/csv/test_trajectories.csv`** - Testing set (15%)
3. **`data/csv/eval_trajectories.csv`** - Evaluation set (15%)
4. **`data/csv/trajectories_summary.csv`** - Summary statistics for all trajectories
5. **`data/csv/example_trajectory.png`** - Example visualization

---

## Key Features

✅ **Reproducible Split**: Fixed random seed (42) ensures consistent splits across runs  
✅ **Balanced Distribution**: All three methods (bezier/spline/dubins) evenly distributed  
✅ **Standard Format**: CSV files compatible with all data analysis tools  
✅ **Complete Data**: Full trajectory coordinates plus start/end metadata  
✅ **Computed Metrics**: Summary file includes path length, curvature, smoothness, etc.  
✅ **Well-Documented**: Comprehensive README and examples included  

---

## Running the Scripts

### Split Data (if needed again)
```bash
python3 split_data_to_csv.py
```

### Load and Analyze Data
```bash
python3 examples/load_csv_data.py
```

---

## Technical Notes

### Data Quality
- All trajectories have exactly 50 waypoints
- No missing values
- All coordinates within specified bounds
- Methods evenly distributed across splits

### Reproducibility
- Random seed: 42
- Split ratios: 70% train, 15% test, 15% eval
- Shuffled before splitting to ensure randomness

### Performance
- CSV files are compressed (float precision optimized)
- Summary file provides quick access to metrics without loading full trajectories
- Pandas can efficiently load and process all files

---

## Next Steps

You can now use these CSV files for:
1. **Machine Learning**: Train models on trajectory data
2. **Data Analysis**: Analyze patterns across different generation methods
3. **Visualization**: Create plots and visualizations
4. **Export**: Share data with other tools/platforms
5. **Research**: Conduct experiments with standardized train/test/eval splits

---

## Questions?

Refer to:
- `/workspace/data/csv/README.md` for detailed CSV format documentation
- `/workspace/examples/load_csv_data.py` for usage examples
- `/workspace/src/data_generator.py` for data generation details

---

**Generated by**: `split_data_to_csv.py`  
**Original Data**: `/workspace/data/trajectories.npz`  
**Output Directory**: `/workspace/data/csv/`

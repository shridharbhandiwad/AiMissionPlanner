# Trajectory Dataset - CSV Format

## Overview

This directory contains the trajectory dataset split into training, testing, and evaluation sets in CSV format.

## Dataset Split

- **Training Set**: 35,000 samples (70%)
- **Testing Set**: 7,500 samples (15%)
- **Evaluation Set**: 7,500 samples (15%)
- **Total**: 50,000 trajectory samples

## Files

### 1. `train_trajectories.csv` (52.24 MB)
Training data containing 35,000 trajectories with full coordinate information.

### 2. `test_trajectories.csv` (11.19 MB)
Testing data containing 7,500 trajectories with full coordinate information.

### 3. `eval_trajectories.csv` (11.19 MB)
Evaluation data containing 7,500 trajectories with full coordinate information.

### 4. `trajectories_summary.csv` (7.57 MB)
Summary statistics and computed metrics for all 50,000 trajectories.

## Data Format

### Trajectory Files (train/test/eval)

Each row represents one complete trajectory with 158 columns:

#### Metadata Columns (8 columns)
- `sample_id`: Unique identifier for the trajectory
- `start_x`, `start_y`, `start_z`: Starting point coordinates (meters)
- `end_x`, `end_y`, `end_z`: Ending point coordinates (meters)
- `method_type`: Generation method (`bezier`, `spline`, or `dubins`)

#### Trajectory Points (150 columns = 50 points × 3 dimensions)
- `point_0_x`, `point_0_y`, `point_0_z`: First trajectory point
- `point_1_x`, `point_1_y`, `point_1_z`: Second trajectory point
- ...
- `point_49_x`, `point_49_y`, `point_49_z`: Last trajectory point (50th point)

Each trajectory consists of 50 waypoints in 3D space (x, y, z coordinates).

### Summary File

The `trajectories_summary.csv` file contains computed metrics for each trajectory:

#### Identification Columns
- `sample_id`: Unique identifier
- `split`: Dataset split (`train`, `test`, or `eval`)
- `method_type`: Generation method

#### Start/End Points
- `start_x`, `start_y`, `start_z`: Starting point coordinates
- `end_x`, `end_y`, `end_z`: Ending point coordinates

#### Computed Metrics
- `path_length`: Total length of the trajectory path (meters)
- `straight_line_distance`: Direct distance from start to end (meters)
- `path_length_ratio`: Ratio of path length to straight-line distance
- `altitude_min`: Minimum altitude along the trajectory (meters)
- `altitude_max`: Maximum altitude along the trajectory (meters)
- `altitude_mean`: Average altitude along the trajectory (meters)
- `avg_curvature`: Average curvature of the path (radians/meter)
- `smoothness_score`: Smoothness metric (0-1, higher is smoother)

## Data Characteristics

### Spatial Bounds
- **X coordinate**: -1000 to 1000 meters
- **Y coordinate**: -1000 to 1000 meters
- **Z coordinate (altitude)**: 50 to 500 meters

### Method Distribution (approximately equal across all splits)
- **Bezier curves**: ~33.3%
- **Cubic splines**: ~33.3%
- **Dubins-like paths**: ~33.4%

### Statistics by Split

#### Training Set (35,000 samples)
- Mean path length: 1,346.83 m
- Mean curvature: 0.091376 rad/m
- Mean smoothness: 0.9615
- Mean altitude: 274.76 m

#### Testing Set (7,500 samples)
- Mean path length: 1,335.67 m
- Mean curvature: 0.083390 rad/m
- Mean smoothness: 0.9621
- Mean altitude: 276.02 m

#### Evaluation Set (7,500 samples)
- Mean path length: 1,350.41 m
- Mean curvature: 0.111835 rad/m
- Mean smoothness: 0.9611
- Mean altitude: 274.88 m

## Usage Examples

### Python (pandas)

```python
import pandas as pd

# Load training data
train_df = pd.read_csv('train_trajectories.csv')

# Access trajectory points
sample = train_df.iloc[0]
start = [sample['start_x'], sample['start_y'], sample['start_z']]
end = [sample['end_x'], sample['end_y'], sample['end_z']]

# Extract all trajectory points
points = []
for i in range(50):
    x = sample[f'point_{i}_x']
    y = sample[f'point_{i}_y']
    z = sample[f'point_{i}_z']
    points.append([x, y, z])

# Load summary with metrics
summary_df = pd.read_csv('trajectories_summary.csv')
train_summary = summary_df[summary_df['split'] == 'train']
print(f"Average path length: {train_summary['path_length'].mean():.2f} m")
```

### R

```r
# Load training data
train_data <- read.csv('train_trajectories.csv')

# Load summary
summary_data <- read.csv('trajectories_summary.csv')
train_summary <- subset(summary_data, split == 'train')

# Analyze by method type
aggregate(path_length ~ method_type, data=train_summary, FUN=mean)
```

### Excel/Spreadsheet Software

All CSV files can be opened directly in:
- Microsoft Excel
- Google Sheets
- LibreOffice Calc
- Any spreadsheet software

**Note**: Due to large file sizes, spreadsheet software may be slow. Consider using programming tools (Python/R) for analysis.

## Data Generation

This dataset was generated using the `src/data_generator.py` script with various path planning algorithms:
- **Bezier curves**: Smooth curves using control points
- **Cubic splines**: Interpolation through waypoints
- **Dubins paths**: Turn-straight-turn patterns with minimum turn radius

Random obstacles were generated but avoided during path planning to create realistic trajectories.

## Reproducibility

The data split uses a fixed random seed (42) to ensure reproducibility. Running the split script multiple times will produce identical train/test/eval splits.

## Citation

If you use this dataset, please cite the original project and mention the data generation methodology.

## License

Same license as the parent project.

---

Generated on: December 11, 2025
Script: `split_data_to_csv.py`
Original data: `data/trajectories.npz`

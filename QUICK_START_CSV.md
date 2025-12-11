# Quick Start Guide - CSV Trajectory Data

## 📁 Where to Find Your Data

All CSV files are located in: **`/workspace/data/csv/`**

## 📊 Available Files

### 1️⃣ Training Data (70%)
```
data/csv/train_trajectories.csv
```
- 35,000 trajectories
- 52.24 MB

### 2️⃣ Testing Data (15%)
```
data/csv/test_trajectories.csv
```
- 7,500 trajectories
- 11.19 MB

### 3️⃣ Evaluation Data (15%)
```
data/csv/eval_trajectories.csv
```
- 7,500 trajectories
- 11.19 MB

### 4️⃣ Summary Statistics
```
data/csv/trajectories_summary.csv
```
- All 50,000 trajectories
- Includes computed metrics (path length, curvature, smoothness)
- 7.57 MB

## 🚀 Quick Usage

### Load in Python
```python
import pandas as pd

# Load training data
df = pd.read_csv('data/csv/train_trajectories.csv')

# Load summary
summary = pd.read_csv('data/csv/trajectories_summary.csv')
```

### Load in R
```r
train <- read.csv('data/csv/train_trajectories.csv')
summary <- read.csv('data/csv/trajectories_summary.csv')
```

### Open in Excel/Google Sheets
Just open the CSV files directly!

## 📖 Documentation

- **`data/csv/README.md`** - Detailed format documentation
- **`DATA_SPLIT_SUMMARY.md`** - Complete summary with statistics
- **`examples/load_csv_data.py`** - Working code examples

## 🔧 Scripts

Run example analyses:
```bash
python3 examples/load_csv_data.py
```

Re-split data (if needed):
```bash
python3 split_data_to_csv.py
```

## 📊 What's in Each CSV?

### Trajectory Files
Each row = one complete trajectory:
- `sample_id` - Unique ID
- `start_x, start_y, start_z` - Starting point
- `end_x, end_y, end_z` - Ending point
- `method_type` - bezier/spline/dubins
- `point_0_x` through `point_49_z` - 50 trajectory points

### Summary File
Each row = metrics for one trajectory:
- Sample identification
- Path metrics (length, curvature, smoothness)
- Altitude statistics
- Method type

## ✅ Data Quality

- ✅ 50,000 total trajectories
- ✅ 70/15/15 train/test/eval split
- ✅ Even distribution of generation methods
- ✅ No missing values
- ✅ Reproducible (seed=42)

## 🎯 Ready to Use!

Your data is split and ready for:
- Machine learning model training
- Statistical analysis
- Visualization
- Research and experiments

Enjoy! 🚀

# F1 Lap Time Prediction

A machine learning project to predict Formula 1 lap times using race data, telemetry, and track characteristics. This project analyzes F1 2025 season data to build models that estimate lap completion times based on various environmental and performance factors.

## Project Overview

The goal is to predict individual lap times in Formula 1 races given various features such as:
- Track conditions (temperature, rainfall, wind speed)
- Tire information (compound, age)
- Fuel levels
- Driver and team performance metrics
- Telemetry data (speed, throttle, brake usage, RPM)
- Track characteristics and relative gaps to other cars

The project uses the **Target variable** defined as: `LapTime / QualiBest`, where `QualiBest` is the fastest qualifying lap on each track. This normalization allows fair comparison across different circuits.

## Dataset

### Data Files

- **f1_data.csv**: Main race telemetry and session data
- **f1_quali_data.csv**: Qualifying session data (used to calculate QualiBest benchmark)
- **f1_telemetry_agg.csv**: Aggregated telemetry features by lap
- **f1_data_cleaned.csv**: Cleaned version of race data
- **f1_train.csv** / **f1_test.csv**: Pre-split training and testing sets (without telemetry)
- **track_metadata_2025.csv**: Track characteristics (length, traction, abrasion, etc.)

### Data Cleaning & Preprocessing

1. **Lap filtering**: Removed lap 1 (abnormally slow) and yellow/red flag laps
2. **Outlier removal**: Filtered extreme Target values (>1.30) and low speed readings (<240 km/h)
3. **Missing value handling**: 
   - Forward fill + backward fill for SpeedST
4. **Temporal split**: Training on rounds 1-19, testing on rounds 20+

## Features

### Base Features
- `DriverNumber`: Driver identifier (categorical)
- `LapNumber`: Lap number in the race
- `SpeedST`: Speed in speed trap (km/h)
- `Compound`: Tire type (SOFT, MEDIUM, HARD, INTERMEDIATE)
- `TyreLife`: Tire age in laps
- `TrackTemp`: Track temperature (°C)
- `Rainfall`: Rain indicator (0/1)
- `WindSpeed`: Wind speed (km/h)
- `FuelLevel`: Estimated remaining fuel (max_laps - current_lap)

### Engineered Features
- `DriverPower`: Median Target value per driver (driver performance proxy)
- `TeamPace`: Median Target value per team (team performance proxy)
- `CompoundRating`: Track-specific hardness rating for the tire compound (1-6 scale from Pirelli)
- `GapAhead`: Time gap to the car ahead (seconds)
- `GapBehind`: Time gap to the car behind (seconds)

### Track Characteristics (from Pirelli data)
- `Length`: Track length (km)
- `Traction`: Traction requirement (1-6)
- `Abrasion`: Tire abrasion level (1-6)
- `TrackEvolution`: Track improvement potential during race
- `TyreStress`: Stress on tires (1-6)
- `Lateral`: Lateral force requirement (1-6)
- `Downforce`: Downforce requirement (1-6)

### Telemetry Features (aggregated per lap)
- `AvgCorneringSpeed`: Average speed in corners (<150 km/h)
- `MaxSpeed`: Maximum speed achieved in lap
- `AvgRPM`: Average engine RPM
- `GearShifts`: Number of gear changes per lap
- `AvgThrottle`: Average throttle position (%)
- `BrakePct`: Percentage of lap spent braking

## Models

### Baseline
Simple mean prediction: always predicts the average Target value.
- **MAE**: ~2.72 (in seconds when converted to lap time)

### Random Forest
- **n_estimators**: 100
- **max_depth**: 15
- **min_samples_leaf**: 25
- **max_features**: sqrt
- **MAE**: ~0.78 seconds (on test set)

### Gradient Boosting (Final Model)
- **n_estimators**: 100-200
- **learning_rate**: 0.05
- **max_depth**: 3
- **Imputation**: SimpleImputer with median strategy

**Final Results (Leave-One-Group-Out Cross-Validation by round)**:
- **Baseline LOGO MAE**: 2.01 seconds
- **Model LOGO MAE**: 1.25 seconds

## Project Structure

```
F1-LapTime-Prediction/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── final.ipynb                        # Complete analysis & final model
├── download_data.py                   # Scripts to fetch F1 data
├── download_telemetry.py              # Scripts to fetch telemetry data
├── data/                              # Data directory
│   ├── f1_data.csv
│   ├── f1_quali_data.csv
│   ├── f1_data_cleaned.csv
│   ├── f1_telemetry_agg.csv
│   ├── f1_train.csv
│   ├── f1_test.csv
│   ├── full_f1_data.csv
│   └── track_metadata_2025.csv
├── notebooks/                         # Exploratory notebooks
│   ├── 01_eda_baseline.ipynb          # Initial EDA and baseline model
│   ├── 02_feature_engineering.ipynb   # Feature creation and engineering
│   ├── 03_telemetry_analysis.ipynb    # Telemetry data analysis
│   ├── 04_adding_telemetry.ipynb      # Integrating telemetry into main dataset
│   └── 05_models_test.ipynb           # Model testing and comparison
└── results/                           # Directory with summary of the project
```

## Notebooks

1. **01_eda_baseline.ipynb**: Data exploration, cleaning, correlation analysis, and baseline model evaluation
2. **02_feature_engineering.ipynb**: Creation of DriverPower, TeamPace, CompoundRating features and track metadata integration
3. **03_telemetry_analysis.ipynb**: Processing and analyzing high-frequency telemetry data, anomaly detection
4. **04_adding_telemetry.ipynb**: Merging telemetry features with main dataset and imputation
5. **05_models_test.ipynb**: Comprehensive model comparison and hyperparameter tuning

## Getting Started

### Requirements

- Python 3.8+
- pandas
- numpy
- scikit-learn
- matplotlib
- plotly
- pyarrow (for parquet files)

Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Analysis

1. Ensure all data files are present in the `data/` directory
2. Open `final.ipynb` in Jupyter Notebook or VS Code
3. Run cells sequentially to reproduce the analysis and model training
4. Alternatively, explore individual notebooks in the `notebooks/` folder for detailed analysis

## Key Insights

- **DriverPower** and **TeamPace** are strong predictors of lap time
- **Fuel level** has significant negative correlation with lap time (lighter cars are faster)
- **Tire compound** and its track-specific hardness rating influence lap times substantially
- **Telemetry features** (cornering speed, braking %) provide valuable predictive signal
- **Gaps to nearby cars** indicate competitive context and potential DRS effects
- **Track characteristics** vary significantly and require normalization through the Target variable

## Data Quality Notes

- Some sensor anomalies detected and corrected:
  - Round 4, Driver 63: Laps 45-57 (marked as NaN)
  - Round 16, Driver 23: Laps 2-11 (marked as NaN)
- Missing telemetry deleted as it imputing it only introduces more noise
- Outliers removed based on statistical analysis (percentiles, speed thresholds)

## Authors

Milena Oberzig, Tobiasz Adamczyk

# Mediterranean Seagrass Intelligence Panel 🌊🌿

A professional Streamlit dashboard for analyzing and visualizing Mediterranean seagrass distribution patterns using machine learning.

## 🚀 Live Application

**Access the interactive dashboard here:**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medseagrassdet.streamlit.app/)

🔗 Direct link: [https://medseagrassdet.streamlit.app/](https://medseagrassdet.streamlit.app/)

## Overview

This intelligence panel provides comprehensive analysis of seagrass presence detection in the Mediterranean Sea based on the methodology from:

**Effrosynidis, D., Arampatzis, A., & Sylaios, G. (2018).** *Seagrass detection in the Mediterranean: A supervised learning approach.* Ecological Informatics, 48, 158-175.

## Features

### 🏠 Presentation Layer
- General overview of the project and objectives
- Description of 5 Mediterranean seagrass species with images
- Dataset characteristics and key innovations
- Data distribution visualizations

### 📊 Variables & Statistics
- Comprehensive description of 217 environmental predictors
- Descriptive statistics (static and temporal variables)
- Correlation analysis with interactive heatmaps
- Geographic distribution maps
- Variable distribution analysis by presence/absence

### 🎯 Binary Classification
- Interactive model comparison (11 algorithms)
- Performance metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
- Stratified vs Spatial cross-validation comparison
- Feature importance analysis
- Top environmental predictors visualization

### 🔢 Multi-Class Classification
- Family-level detection (5 seagrass families)
- Class imbalance analysis
- Multi-metric performance comparison
- Spatial autocorrelation impact assessment
- Feature importance for family discrimination

### 📝 Conclusions & Future Steps
- Major achievements summary
- Key scientific insights
- Environmental drivers interpretation
- Methodological findings
- Recommendations for deployment and research extensions
- Conservation implications

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/med_seagrass.git
cd med_seagrass/panel
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Project Structure

```
panel/
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── page_modules/                   # Page modules
    ├── __init__.py
    ├── presentation.py             # Presentation page
    ├── variables.py                # Variables & statistics page
    ├── binary_classification.py    # Binary classification analysis
    ├── multiclass_classification.py # Multi-class classification analysis
    └── conclusions.py              # Conclusions & future steps
```

## Data

The panel uses the preprocessed dataset located at:
```
../data/pres_abs_merge_def.csv
```

Dataset includes:
- 3,055 observations (presence and pseudo-absence)
- 217 environmental predictors
- 5 seagrass families
- 8 geographic zones (Mediterranean-wide)

## Key Technologies

- **Streamlit**: Interactive web application framework
- **Plotly**: Interactive plotting and visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **SciPy**: Statistical analysis

## Features Highlights

### Interactive Visualizations
- Geographic maps with presence/absence overlay
- Correlation heatmaps
- Model performance comparisons
- Radar charts for multi-metric analysis
- Feature importance bar charts

### Filtering Options
- Cross-validation strategy selection (Stratified vs Spatial)
- Performance metric selection
- Model selection for detailed comparison
- Variable selection for distribution analysis

### Export Capabilities
- Download model results as CSV
- Download descriptive statistics
- All visualizations are interactive and can be saved

## Key Findings

- **Binary Classification**: Up to 99.3% accuracy (Stratified CV), 91.2% (Spatial CV)
- **Multi-Class Classification**: 97.4% accuracy (Stratified CV), 87.2% (Spatial CV)
- **Critical Insight**: Spatial cross-validation reveals 8-10% performance drop compared to stratified CV
- **Top Predictor**: Chlorophyll-α concentration is the most important environmental variable

## Credits

- **Original Research**: Effrosynidis et al. (2018)
- **Data Sources**: CMEMS (Copernicus Marine Environment Monitoring Service)
- **Development**: Mediterranean Seagrass Project Team

## License

This project is for educational and research purposes. Please cite the original paper when using this work.

## Contact

For questions or collaborations, please open an issue on GitHub.

---

**Built with ❤️ for Mediterranean seagrass conservation** 🌊🌿

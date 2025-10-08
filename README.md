# Mediterranean Seagrass Intelligence Panel 🌊🌿

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medseagrassdet.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**🚀 [Launch Live App](https://medseagrassdet.streamlit.app/)**

A professional, interactive web dashboard for analyzing and visualizing Mediterranean seagrass distribution patterns using machine learning and spatial analysis.

## Overview

This intelligence panel provides comprehensive analysis of seagrass presence detection in the Mediterranean Sea based on the methodology from:

**Effrosynidis, D., Arampatzis, A., & Sylaios, G. (2018).** *Seagrass detection in the Mediterranean: A supervised learning approach.* Ecological Informatics, 48, 158-175.
[DOI: 10.1016/j.ecoinf.2018.09.004](https://doi.org/10.1016/j.ecoinf.2018.09.004)

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
- Interactive model comparison (7 algorithms)
- Performance metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
- Stratified vs Spatial cross-validation comparison
- Best model: Random Forest (98.8% stratified, 88.0% spatial accuracy)
- Feature importance: Chlorophyll-α dominates (7 of top 10 features)

### 🔢 Multi-Class Classification
- Family-level detection (5 seagrass families)
- Class imbalance analysis with Macro F1 metric
- Multi-metric performance comparison
- Spatial autocorrelation impact assessment (19-64% performance drops)
- Feature importance: Water clarity (Secchi depth) dominates (7 of top 10 features)

### 📝 Conclusions & Future Steps
- Major achievements summary (corrected with actual results)
- Key scientific insights and environmental drivers
- Critical methodological findings on spatial CV
- Recommendations for:
  - Model improvements (hyperparameter tuning, neural networks)
  - Deployment strategies (API, GIS integration)
  - Research extensions (temporal dynamics, climate scenarios, remote sensing)
- Conservation implications and management priorities

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

- **Streamlit** ≥1.28.0: Interactive web application framework
- **Plotly** ≥5.17.0: Interactive plotting and visualizations
- **Pandas** ≥2.0.0: Data manipulation and analysis
- **NumPy** ≥1.24.0: Numerical computing
- **SciPy** ≥1.11.0: Statistical analysis
- **Scikit-learn** ≥1.3.0: Machine learning algorithms
- **PyCaret** ≥3.0.0: AutoML framework (for EDA notebook)
- **Matplotlib** & **Seaborn**: Additional visualization tools

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

### Binary Classification (Presence/Absence)
- **Best Model**: Random Forest
- **Performance**: 98.8% accuracy (Stratified CV), 88.0% (Spatial CV)
- **ROC-AUC**: 99.9% (Stratified), 95.6% (Spatial)
- **Performance Drop**: 10.8% accuracy decrease with spatial CV
- **Top Predictor**: Chlorophyll-α (7 of top 10 features are chlorophyll measures)

### Multi-Class Classification (Family Detection)
- **Best Stratified Model**: Random Forest (86.1% accuracy, 82.2% Macro F1)
- **Best Spatial Model**: K Neighbors (68.1% accuracy, 62.1% Macro F1)
- **Performance Drop**: 18.0% accuracy, 20.1% Macro F1 decrease with spatial CV
- **Top Predictor**: Water clarity - Secchi depth (7 of top 10 features)
- **Challenge**: Performance drops 19-64% across models with spatial CV

### Critical Methodological Insight
**Spatial cross-validation is essential** for realistic performance estimates in species distribution models. Traditional stratified CV significantly overestimates model performance due to spatial autocorrelation.

## 🚀 Live Demo

**🌐 Access the live application:** [https://medseagrassdet.streamlit.app/](https://medseagrassdet.streamlit.app/)

The app is fully interactive and deployed on Streamlit Cloud for easy access worldwide. No installation required!

## 📸 Screenshots

The application features:
- 🎨 Professional dark green sidebar with enhanced navigation
- 📊 Interactive Plotly visualizations with larger, readable fonts
- 📈 Real-time model comparison and filtering
- 🗺️ Geographic distribution maps
- 💾 Export capabilities for all results
- 📱 Responsive design for desktop and tablet viewing

## Credits & Acknowledgments

- **Original Research**: Effrosynidis, D., Arampatzis, A., & Sylaios, G. (2018)
- **Data Sources**: 
  - CMEMS (Copernicus Marine Environment Monitoring Service)
  - Original dataset: [Mendeley Data](https://data.mendeley.com/datasets/8nmh5grxp8/1)
- **Developer**: Guillem La Casta
- **Program**: CSIC Momentum Programme - "Develop your Digital Talent"
- **Institution**: ICMAN-CSIC (Instituto de Ciencias Marinas de Andalucía)

## Citation

If you use this work, please cite:

```
Effrosynidis, D., Arampatzis, A., & Sylaios, G. (2018). 
Seagrass detection in the Mediterranean: A supervised learning approach. 
Ecological Informatics, 48, 158-175. 
https://doi.org/10.1016/j.ecoinf.2018.09.004
```

## License

This project is for educational and research purposes. 

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions, suggestions, or collaborations:
- Open an issue on [GitHub](https://github.com/guillemlcg/med_seagrass)
- Visit the [live application](https://medseagrassdet.streamlit.app/)

---

**Built with ❤️ for Mediterranean seagrass conservation** 🌊🌿

*Protecting blue carbon ecosystems through data science and machine learning*

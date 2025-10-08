# Quick Start Guide 🚀

## Mediterranean Seagrass Intelligence Panel

### Getting Started in 3 Steps

#### Step 1: Install Dependencies

Open PowerShell in the `panel` folder and run:

```powershell
pip install -r requirements.txt
```

#### Step 2: Launch the App

**Option A - Using the batch file (easiest):**
Double-click `run.bat` in the panel folder

**Option B - Using command line:**
```powershell
streamlit run app.py
```

#### Step 3: Explore!

The app will automatically open in your browser at `http://localhost:8501`

---

## Navigation Guide

### 🏠 Presentation
Start here to understand:
- Project objectives
- Seagrass species (with images)
- Dataset characteristics
- Geographic distribution

### 📊 Variables & Statistics
Explore the data:
- 217 environmental predictors
- Descriptive statistics
- Correlation analysis
- Interactive geographic maps
- Variable distributions

### 🎯 Binary Classification
Analyze presence/absence models:
- Compare 11 different algorithms
- Select CV strategy (Stratified vs Spatial)
- Choose performance metrics
- View feature importance
- Compare model performance

### 🔢 Multi-Class Classification
Family-level detection:
- 5 seagrass families
- Class imbalance analysis
- Multi-metric comparison
- Spatial CV impact
- Feature importance for family discrimination

### 📝 Conclusions & Future Steps
Understand the findings:
- Major achievements
- Scientific insights
- Methodological discoveries
- Future recommendations
- Conservation implications

---

## Interactive Features

### Filters & Controls
- **CV Strategy**: Switch between Stratified and Spatial cross-validation
- **Metrics**: Choose from Accuracy, Precision, Recall, F1, ROC-AUC
- **Models**: Select specific models for detailed comparison
- **Variables**: Pick variables for distribution analysis

### Visualizations
- All charts are interactive (hover, zoom, pan)
- Click legend items to show/hide data
- Download plots as PNG images

### Data Export
- Download model results as CSV
- Export statistics tables
- Save filtered data

---

## Tips for Best Experience

1. **Start with Presentation**: Get context before diving into analysis
2. **Compare CV Strategies**: See how spatial autocorrelation affects performance
3. **Check Feature Importance**: Understand what drives predictions
4. **Use Filters**: Customize views to your interests
5. **Download Data**: Export results for further analysis

---

## Troubleshooting

### App won't start?
- Make sure you're in the `panel` folder
- Check that all dependencies are installed: `pip list | grep streamlit`
- Try: `python -m streamlit run app.py`

### Can't see images?
- Images should be in `../img/` folder
- Check that the folder contains: posidonia.jpg, cymodocea.jpg, zostera.jpg, halophila.jpg, ruppia.jpg

### Data not loading?
- Verify `../data/pres_abs_merge_def.csv` exists
- Check file path in `app.py` if you moved files

### Port already in use?
- Streamlit default port is 8501
- Use: `streamlit run app.py --server.port 8502`

---

## System Requirements

- **OS**: Windows, macOS, Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

---

## Performance Notes

- First load may take a few seconds (data caching)
- Subsequent page switches are fast (cached data)
- Large correlation matrices may take 2-3 seconds to render
- Geographic maps load from OpenStreetMap

---

## Need Help?

- Check the README.md for detailed documentation
- Review the original paper: Effrosynidis et al. (2018)
- Open an issue on GitHub

---

**Enjoy exploring Mediterranean seagrass data!** 🌊🌿

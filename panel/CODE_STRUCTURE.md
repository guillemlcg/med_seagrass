# 🛠️ App.py Code Structure Reference

## Quick Navigation Guide

```python
# ==================== IMPORTS ====================
Line 1-14:   Minimal essential imports only (streamlit, pandas, pathlib, base64)

# ==================== CONFIGURATION ====================
Line 16-22:  st.set_page_config() - Page metadata and layout

# ==================== CUSTOM CSS ====================
Line 24-268: All styling in one centralized location

# ==================== DATA LOADING ====================
Line 270-280: load_data() function with caching

# ==================== HELPER FUNCTIONS ====================
Line 283-310: Reusable utility functions
    - encode_image_to_base64()
    - create_styled_button_html()
    - convert_df_to_csv()

# ==================== INITIALIZE DATA ====================
Line 312-322: Data loading with error handling

# ==================== SIDEBAR CONFIGURATION ====================
Line 325-412: Complete sidebar setup
    - Title/Header
    - Navigation radio buttons
    - About section with paper image
    - Download buttons
    - Mendeley link

# ==================== PAGE ROUTING ====================
Line 414-428: if/elif page routing logic

# ==================== FOOTER ====================
Line 430-439: Sidebar footer with credits
```

---

## 🔧 How to Add New Features

### Adding a New Page:
```python
# 1. Create new file in page_modules/
page_modules/new_feature.py

# 2. Add to navigation (line ~333):
["🏠 Presentation", 
 "📊 Variables & Statistics", 
 "🎯 Binary Classification", 
 "🔢 Multi-Class Classification",
 "📝 Conclusions & Future Steps",
 "🆕 New Feature"]  # ADD THIS

# 3. Add routing (line ~428):
elif page == "🆕 New Feature":
    from page_modules import new_feature
    new_feature.show(df)
```

### Adding a New Sidebar Button:
```python
# Use the helper function (line ~290):
button_html = create_styled_button_html(
    url='https://example.com',
    text='Click Me',
    icon='🔗',
    is_download=False
)
st.sidebar.markdown(button_html, unsafe_allow_html=True)
```

### Modifying Styles:
All CSS is in lines 24-268. Find the selector and update:
```css
/* Main content text */
.stMarkdown p, .stMarkdown li {
    font-size: 18px !important;  /* Change this value */
    line-height: 1.7 !important;
}
```

---

## 📦 Dependencies Used

| Package | Usage |
|---------|-------|
| `streamlit` | Main framework |
| `pandas` | Data manipulation |
| `pathlib.Path` | File path handling |
| `base64` | Image encoding for HTML |

**Note**: Page modules may use additional packages (plotly, numpy, etc.)

---

## 🎨 Color Palette Reference

```css
/* Primary Green Shades */
--primary-dark:    #1a4d2e
--primary-medium:  #2E8B57
--primary-light:   #3CB371

/* Button Colors */
--button-bg:       #52b788
--button-border:   #40916c
--button-hover:    #40916c
--button-accent:   #95d5b2
--button-light:    #b7e4c7

/* Info Boxes */
--info-blue:       #2196F3
--warning-yellow:  #ffc107
--success-green:   #28a745

/* Backgrounds */
--sidebar-gradient: linear-gradient(180deg, rgba(26, 77, 46, 0.85), rgba(45, 106, 79, 0.85))
--button-gradient:  linear-gradient(90deg, #52b788, #40916c)
```

---

## ⚡ Performance Tips

### Caching Strategy:
```python
@st.cache_data  # Use for data loading/transformation
def load_data():
    return pd.read_csv(...)

@st.cache_data  # Use for expensive computations
def convert_df_to_csv(df):
    return df.to_csv(...)
```

### Import Optimization:
- ✅ Import page modules **inside** routing (lazy loading)
- ✅ Only import what you actually use
- ❌ Don't import at top if only used in one page

### Error Handling Best Practice:
```python
try:
    # Your code
except SpecificError as e:  # Catch specific errors first
    st.error(f"❌ Clear message: {e}")
except Exception as e:      # General fallback
    st.error(f"❌ Unexpected error: {e}")
    st.stop()
```

---

## 🐛 Common Issues & Solutions

### Issue: Import Error
**Problem**: `ModuleNotFoundError: No module named 'page_modules'`  
**Solution**: Check that page_modules/ has `__init__.py`

### Issue: Data Not Loading
**Problem**: FileNotFoundError  
**Solution**: Check relative path in `load_data()` (line ~275)

### Issue: CSS Not Applying
**Problem**: Styles not visible  
**Solution**: 
1. Check `unsafe_allow_html=True` is set
2. Clear browser cache (Ctrl+Shift+R)
3. Verify CSS selector names

### Issue: Sidebar Background Not Showing
**Problem**: Background image missing  
**Solution**: Verify GitHub URL in CSS (line ~61) is accessible

---

## 📚 Helper Functions Reference

### `encode_image_to_base64(image_path)`
Converts image file to base64 string for embedding in HTML.

**Parameters:**
- `image_path` (Path): Path to image file

**Returns:** 
- `str`: Base64 encoded image string

**Example:**
```python
img_path = Path('img/logo.png')
img_base64 = encode_image_to_base64(img_path)
```

---

### `create_styled_button_html(url, text, icon, is_download=False)`
Generates HTML for styled sidebar button with hover effects.

**Parameters:**
- `url` (str): URL to link to (or base64 data for downloads)
- `text` (str): Button text
- `icon` (str): Emoji or icon
- `is_download` (bool): If True, creates download link

**Returns:**
- `str`: HTML string for button

**Example:**
```python
# External link
button_html = create_styled_button_html(
    'https://example.com',
    'Visit Site',
    '🔗',
    is_download=False
)

# Download link
csv_b64 = base64.b64encode(csv_data).decode()
download_html = create_styled_button_html(
    csv_b64,
    'Download CSV',
    '📥',
    is_download=True
)
```

---

### `convert_df_to_csv(dataframe)`
Converts pandas DataFrame to CSV format with caching.

**Parameters:**
- `dataframe` (pd.DataFrame): DataFrame to convert

**Returns:**
- `bytes`: UTF-8 encoded CSV data

**Example:**
```python
csv_data = convert_df_to_csv(df)
csv_b64 = base64.b64encode(csv_data).decode()
```

---

## 🚀 Quick Start Development

### Run Locally:
```bash
cd panel
streamlit run app.py
```

### Before Committing:
```bash
# Check syntax
python -m py_compile app.py

# Format code (optional)
black app.py

# Check imports (optional)
pylint app.py
```

### Deploy to Streamlit Cloud:
1. Commit changes to GitHub
2. Push to main branch
3. Streamlit Cloud auto-deploys in 2-3 minutes
4. Access at: https://medseagrassdet.streamlit.app/

---

## 📊 File Structure

```
panel/
├── app.py                          # Main application (439 lines)
├── requirements.txt                # Python dependencies
├── OPTIMIZATION_SUMMARY.md         # This optimization guide
├── CODE_STRUCTURE.md              # This reference guide
├── page_modules/
│   ├── __init__.py                # Package marker
│   ├── presentation.py            # Home page
│   ├── variables.py               # Variables & statistics
│   ├── binary_classification.py   # Binary classification analysis
│   ├── multiclass_classification.py # Multi-class analysis
│   └── conclusions.py             # Conclusions & recommendations
└── __pycache__/                   # Python cache (auto-generated)
```

---

*Reference Guide Last Updated: October 9, 2025*  
*App Version: Optimized v2.0*

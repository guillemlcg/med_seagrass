"""
Mediterranean Seagrass Detection Intelligence Panel
====================================================
A professional Streamlit dashboard for seagrass presence detection analysis
Based on Effrosynidis et al. (2018) methodology

Author: Data Science Team
Date: 2024
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import base64

# Page configuration
st.set_page_config(
    page_title="Mediterranean Seagrass Intelligence Panel",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Global font size increase */
    html, body, [class*="css"] {
        font-size: 18px !important;
    }
    
    /* Main content text */
    .stMarkdown p, .stMarkdown li {
        font-size: 18px !important;
        line-height: 1.7 !important;
    }
    
    /* Headers */
    h1 { font-size: 2.8rem !important; }
    h2 { font-size: 2.2rem !important; }
    h3 { font-size: 1.8rem !important; }
    h4 { font-size: 1.5rem !important; }
    
    /* Sidebar styling with seagrass background */
    [data-testid="stSidebar"] {
        position: relative !important;
        background: #1a4d2e !important;
    }
    
    /* Sidebar background with image */
    [data-testid="stSidebar"]::before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        background-image: url('https://raw.githubusercontent.com/guillemlcg/med_seagrass/main/img/menu_background.jpg') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        opacity: 0.15 !important;
        filter: blur(2px) !important;
        z-index: 0 !important;
    }
    
    /* Overlay gradient on top of image */
    [data-testid="stSidebar"]::after {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(180deg, rgba(26, 77, 46, 0.85) 0%, rgba(45, 106, 79, 0.85) 100%) !important;
        z-index: 0 !important;
    }
    
    /* Ensure sidebar content appears above background */
    [data-testid="stSidebar"] > div {
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Sidebar text color and size */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-size: 17px !important;
    }
    
    /* Navigation header styling */
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        font-size: 1.6rem !important;
    }
    
    /* Radio button styling - navigation buttons */
    [data-testid="stSidebar"] .stRadio > label {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 14px 18px !important;
        margin: 6px 0 !important;
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
        cursor: pointer !important;
        font-size: 17px !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: #95d5b2 !important;
        transform: translateX(5px) !important;
    }
    
    /* Selected navigation button */
    [data-testid="stSidebar"] .stRadio > label[data-checked="true"] {
        background: linear-gradient(90deg, #52b788 0%, #40916c 100%) !important;
        border-color: #95d5b2 !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Radio button icons */
    [data-testid="stSidebar"] .stRadio input[type="radio"] {
        display: none !important;
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Sidebar links */
    [data-testid="stSidebar"] a {
        color: #95d5b2 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] a:hover {
        color: #b7e4c7 !important;
        text-decoration: underline !important;
    }
    
    /* Download button styling */
    [data-testid="stSidebar"] button[kind="secondary"] {
        background-color: #52b788 !important;
        color: white !important;
        border: 2px solid #40916c !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        background-color: #40916c !important;
        border-color: #2d6a4f !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #2E8B57, #3CB371);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
        font-size: 18px !important;
    }
    .metric-card p, .metric-card li {
        font-size: 18px !important;
        line-height: 1.7 !important;
    }
    .section-header {
        color: #2E8B57;
        border-bottom: 2px solid #3CB371;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 2rem !important;
    }
    .species-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        margin: 0.5rem 0;
        transition: transform 0.2s;
        font-size: 18px !important;
    }
    .species-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-left: 4px solid #2196F3;
        border-radius: 4px;
        margin: 1rem 0;
        font-size: 18px !important;
    }
    .info-box p, .info-box li {
        font-size: 18px !important;
        line-height: 1.7 !important;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-left: 4px solid #ffc107;
        border-radius: 4px;
        margin: 1rem 0;
        font-size: 18px !important;
    }
    .warning-box p, .warning-box li {
        font-size: 18px !important;
        line-height: 1.7 !important;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-left: 4px solid #28a745;
        border-radius: 4px;
        margin: 1rem 0;
        font-size: 18px !important;
    }
    .success-box p, .success-box li {
        font-size: 18px !important;
        line-height: 1.7 !important;
    }
    
    /* Plotly graph text size */
    .js-plotly-plot .plotly text {
        font-size: 16px !important;
    }
    
    /* Dataframe text size */
    .dataframe {
        font-size: 16px !important;
    }
    
    /* Streamlit metric labels and values */
    [data-testid="stMetricLabel"] {
        font-size: 18px !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
    }
    
    /* Table text */
    table {
        font-size: 16px !important;
    }
    
    /* Button text */
    button {
        font-size: 17px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================
@st.cache_data
def load_data():
    """Load the seagrass dataset with caching"""
    current_dir = Path(__file__).resolve().parent
    data_path = current_dir.parent / 'data' / 'pres_abs_merge_def.csv'
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found at: {data_path}")
    
    return pd.read_csv(data_path)


# ==================== HELPER FUNCTIONS ====================
def encode_image_to_base64(image_path):
    """Encode image to base64 string"""
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()


def create_styled_button_html(url, text, icon, is_download=False):
    """Generate HTML for styled sidebar button"""
    action = f"download='med_seagrass_data.csv'" if is_download else "target='_blank'"
    href = f"data:text/csv;base64,{url}" if is_download else url
    
    return f"""
    <div style='margin-top: 10px;'>
        <a href='{href}' {action}>
            <button style='width: 100%; padding: 0.5rem 1rem; 
                           background-color: #52b788; color: white; 
                           border: 2px solid #40916c; border-radius: 4px;
                           font-weight: 500; cursor: pointer;
                           transition: all 0.3s ease;'
                    onmouseover="this.style.backgroundColor='#40916c'; this.style.borderColor='#2d6a4f'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.3)';"
                    onmouseout="this.style.backgroundColor='#52b788'; this.style.borderColor='#40916c'; this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                {icon} {text}
            </button>
        </a>
    </div>
    """

# ==================== INITIALIZE DATA ====================
try:
    df = load_data()
except FileNotFoundError as e:
    st.error(f"❌ Data file not found: {e}")
    st.error("Please ensure 'data/pres_abs_merge_def.csv' exists in the project directory.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()


# ==================== SIDEBAR CONFIGURATION ====================
# Sidebar title (with circular seagrass logo if available)
logo_svg_path = Path(__file__).resolve().parent.parent / 'img' / 'logo_seagrass_circle.svg'
logo_img_html = ""
if logo_svg_path.exists():
    svg_b64 = encode_image_to_base64(logo_svg_path)
    logo_img_html = (
        f"<img src='data:image/svg+xml;base64,{svg_b64}' alt='Seagrass Logo' "
        "style='width:110px;height:110px;border-radius:50%;"
        "box-shadow:0 2px 6px rgba(0,0,0,0.25);margin-bottom:10px;'/>"
    )

st.sidebar.markdown(f"""
<div style='text-align: center; padding: 1.5rem 0.5rem; margin-bottom: 1rem;'>
    {logo_img_html}
    <h1 style='color: #ffffff; font-size: 1.5rem; margin: 0.5rem 0 0 0; font-weight: 700; 
               text-shadow: 2px 2px 4px rgba(0,0,0,0.3); line-height: 1.3;'>
        Mediterranean Seagrass<br>Intelligence Panel
    </h1>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Sidebar navigation
st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.radio(
    "",
    ["🏠 Presentation", 
     "📊 Variables & Statistics", 
     "🎯 Binary Classification", 
     "🔢 Multi-Class Classification",
     "📝 Conclusions & Future Steps"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# About section
st.sidebar.markdown("### 📚 About")
st.sidebar.markdown("""
Based on the methodology from:

**Effrosynidis et al. (2018)**  
*"Seagrass detection in the Mediterranean: A supervised learning approach"*

Published in *Ecological Informatics*
""")

# Article screenshot with link to DOI
paper_img_path = Path(__file__).resolve().parent.parent / 'img' / 'paper_thumbnail.jpg'
if paper_img_path.exists():
    img_base64 = encode_image_to_base64(paper_img_path)
    
    st.sidebar.markdown(f"""
    <div style='margin-top: 15px; margin-bottom: 10px;'>
        <a href='https://doi.org/10.1016/j.ecoinf.2018.09.004' target='_blank'>
            <img src='data:image/jpeg;base64,{img_base64}' 
                 style='width: 100%; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
                        cursor: pointer; transition: transform 0.2s;' 
                 onmouseover="this.style.transform='scale(1.02)'" 
                 onmouseout="this.style.transform='scale(1)'"/>
        </a>
    </div>
    <div style='text-align: center; margin-top: 8px; margin-bottom: 15px;'>
        <a href='https://doi.org/10.1016/j.ecoinf.2018.09.004' target='_blank' 
           style='font-size: 0.85rem; color: #2E8B57; text-decoration: none; font-weight: 500;'>
            📄 Read Full Article
        </a>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

# Download dataframe button
st.sidebar.markdown("### 💾 Download Data")

@st.cache_data
def convert_df_to_csv(dataframe):
    """Convert dataframe to CSV with caching"""
    return dataframe.to_csv(index=False).encode('utf-8')

csv_b64 = base64.b64encode(convert_df_to_csv(df)).decode()
st.sidebar.markdown(
    create_styled_button_html(csv_b64, "Download Preprocessed Dataset (CSV)", "📥", is_download=True) +
    "<div style='text-align: center; margin-top: 5px; font-size: 0.75rem; color: #666;'>" +
    "<em>Preprocessed dataset by the developer</em></div>",
    unsafe_allow_html=True
)

# Link to original data on Mendeley
st.sidebar.markdown("### 🔗 Original Data")
st.sidebar.markdown(
    create_styled_button_html('https://data.mendeley.com/datasets/8nmh5grxp8/1', 
                             "Access Original Data (Mendeley)", "🔗") +
    "<div style='text-align: center; margin-top: 5px; font-size: 0.75rem; color: #666;'>" +
    "<em>Raw data repository</em></div>",
    unsafe_allow_html=True
)

# ==================== PAGE ROUTING ====================
if page == "🏠 Presentation":
    from page_modules import presentation
    presentation.show(df)
elif page == "📊 Variables & Statistics":
    from page_modules import variables
    variables.show(df)
elif page == "🎯 Binary Classification":
    from page_modules import binary_classification
    binary_classification.show(df)
elif page == "🔢 Multi-Class Classification":
    from page_modules import multiclass_classification
    multiclass_classification.show(df)
elif page == "📝 Conclusions & Future Steps":
    from page_modules import conclusions
    conclusions.show(df)

# ==================== FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85rem; margin-top: 20px;'>
    <p style='margin: 5px 0; font-weight: 500;'>Developed by Guillem La Casta</p>
    <div style='margin-top: 10px;'>
        <a href='https://www.linkedin.com/in/guillemlcg' target='_blank' style='margin: 0 8px; text-decoration: none;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' alt='LinkedIn' style='width: 28px; height: 28px; vertical-align: middle;'/>
        </a>
        <a href='https://github.com/guillemlcg' target='_blank' style='margin: 0 8px; text-decoration: none;'>
            <img src='https://cdn-icons-png.flaticon.com/512/25/25231.png' alt='GitHub' style='width: 28px; height: 28px; vertical-align: middle;'/>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

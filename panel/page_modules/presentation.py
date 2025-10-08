"""
Presentation Page - Mediterranean Seagrass Intelligence Panel
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import plotly.graph_objects as go

def show(df):
    """Display the presentation/introduction page"""
    
    # Load background image
    bg_img_path = Path(__file__).resolve().parent.parent.parent / 'img' / 'menu_background.jpg'
    
    if bg_img_path.exists():
        with open(bg_img_path, 'rb') as img_file:
            bg_img_base64 = base64.b64encode(img_file.read()).decode()
        
        # Main header with background image
        st.markdown(f"""
        <div style="
            position: relative;
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(rgba(46, 139, 87, 0.85), rgba(60, 179, 113, 0.85)), 
                        url('data:image/jpeg;base64,{bg_img_base64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <h1 style="margin: 0; font-size: 2.8em; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                🌊 Mediterranean Seagrass Detection
            </h1>
            <h2 style="margin: 15px 0 0 0; font-size: 1.6em; font-weight: 300; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">
                Intelligence Panel & Analysis Dashboard
            </h2>
            <p style="margin: 15px 0 0 0; font-size: 1.1em; opacity: 0.95; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                Supervised Learning Approach for Seagrass Presence Detection
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback to original header if image not found
        st.markdown("""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 2.5em;">🌊 Mediterranean Seagrass Detection</h1>
            <h2 style="margin: 10px 0 0 0; font-weight: 300;">Intelligence Panel & Analysis Dashboard</h2>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">Supervised Learning Approach for Seagrass Presence Detection</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Executive Summary
    st.markdown("## 📋 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Observations", f"{len(df)}")
    with col2:
        st.metric("Environmental Predictors", "217")
    with col3:
        presence_count = df['Presence'].sum()
        st.metric("Seagrass Present", f"{presence_count}")
    with col4:
        st.metric("Geographic Zones", "8")
    
    # Study Case Summary
    st.markdown("## 📖 Study Case Summary")
    
    st.markdown("""
    <div class="info-box" style="background-color: #f0f8ff; border-left: 4px solid #2E8B57; padding: 1.5rem; margin: 1rem 0;">
        <p style="margin: 0 0 1rem 0;">
            This study addresses the critical need for accurate seagrass distribution mapping in the Mediterranean Sea, 
            where these marine ecosystems are threatened by human activities and climate change. Based on the research by 
            <strong>Effrosynidis, Arampatzis, and Sylaios (2018)</strong>, this work applies supervised machine learning 
            to predict seagrass presence and identify species using environmental predictors.
        </p>
        <p style="margin: 0 0 1rem 0;">
            <strong>Study Area:</strong> Mediterranean-wide coverage spanning diverse coastal environments, from shallow 
            coastal lagoons to deeper offshore meadows across 8 distinct geographic zones.
        </p>
        <p style="margin: 0 0 1rem 0;">
            <strong>Data Source:</strong> The dataset combines seagrass occurrence data with 217 environmental variables 
            derived from the Copernicus Marine Environment Monitoring Service (CMEMS), including oceanographic parameters 
            (temperature, salinity, chlorophyll-α, nutrients), physical characteristics (bathymetry, wave height), and 
            anthropogenic factors (distance to coastal infrastructure).
        </p>
        <p style="margin: 0 0 1rem 0;">
            <strong>Dataset Composition:</strong> The dataset includes 3055 observations combining <strong>1771 real seagrass 
            presence records</strong> with <strong>1284 artificial absence points</strong>. Since no publicly available absence 
            dataset exists, artificial absence records were generated using a rule-based methodology: for each presence 
            point, the nearest CMEMS grid cell not already marked as absent was selected, with the assumption that adjacent 
            areas were examined during field surveys and would have been recorded if seagrass were present. Additional 
            constraints ensured absence points remained within 10 km of the coast and followed coastal patterns, creating 
            a realistic absence dataset for binary classification while acknowledging the inherent uncertainty of artificial 
            absence data.
        </p>
        <p style="margin: 0;">
            <strong>Innovation:</strong> This research pioneer a novel approach to handle spatial autocorrelation by 
            clustering geographic coordinates into discrete zones, improving model generalization to new locations while 
            maintaining spatial context—a critical advancement for real-world conservation applications.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview section
    st.markdown("## 🎯 Research Objectives")
    
    st.markdown("""
    <div class="info-box">
        <h3 style="margin-top: 0;">Primary Goals</h3>
        <ul>
            <li><strong>Binary Classification:</strong> Detect seagrass presence/absence with >90% accuracy</li>
            <li><strong>Multi-Class Classification:</strong> Identify seagrass family when present (5 families)</li>
            <li><strong>Spatial Validation:</strong> Address spatial autocorrelation through geographic clustering</li>
            <li><strong>Feature Importance:</strong> Identify key environmental predictors of seagrass distribution</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Seagrass Species Section
    st.markdown("## 🌿 Mediterranean Seagrass Species")
    
    st.markdown("""
    Seagrasses are marine flowering plants that form extensive underwater meadows in coastal areas. 
    The Mediterranean Sea hosts five major seagrass families, each adapted to specific environmental conditions.
    """)
    
    # Species cards with images
    species_info = {
        'Posidonia': {
            'scientific': 'Posidonia oceanica',
            'common': 'Neptune Grass',
            'depth': '0-40m',
            'description': 'Endemic to Mediterranean. Forms dense meadows, critical for biodiversity.',
            'image': 'posidonia.jpg',
            'wiki_url': 'https://en.wikipedia.org/wiki/Posidonia_oceanica'
        },
        'Cymodocea': {
            'scientific': 'Cymodocea nodosa',
            'common': 'Little Neptune Grass',
            'depth': '0-30m',
            'description': 'Fast-growing, tolerates varying salinity and temperatures.',
            'image': 'cymodocea.jpg',
            'wiki_url': 'https://en.wikipedia.org/wiki/Cymodocea_nodosa'
        },
        'Zostera': {
            'scientific': 'Zostera noltii / Z. marina',
            'common': 'Eelgrass',
            'depth': '0-15m',
            'description': 'Prefers sheltered bays and estuaries with muddy/sandy substrates.',
            'image': 'zostera.jpg',
            'wiki_url': 'https://en.wikipedia.org/wiki/Zostera'
        },
        'Halophila': {
            'scientific': 'Halophila stipulacea',
            'common': 'Spoon Seagrass',
            'depth': '0-50m',
            'description': 'Invasive species from Red Sea, rapid colonizer.',
            'image': 'halophila.jpg',
            'wiki_url': 'https://en.wikipedia.org/wiki/Halophila_stipulacea'
        },
        'Ruppia': {
            'scientific': 'Ruppia spp.',
            'common': 'Widgeon Grass',
            'depth': '0-5m',
            'description': 'Tolerates extreme salinity variations in coastal lagoons.',
            'image': 'ruppia.jpg',
            'wiki_url': 'https://en.wikipedia.org/wiki/Ruppia'
        }
    }
    
    # Display species in rows of 3
    species_list = list(species_info.items())
    
    for i in range(0, len(species_list), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(species_list):
                family, info = species_list[i + j]
                with col:
                    # Try to load image with clickable link
                    img_path = Path(__file__).parent.parent.parent / 'img' / info['image']
                    if img_path.exists():
                        # Read and encode image for HTML display
                        with open(img_path, 'rb') as img_file:
                            img_data = base64.b64encode(img_file.read()).decode()
                        
                        # Create clickable circular image link centered
                        st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 15px;">
                            <a href="{info['wiki_url']}" target="_blank" style="display: inline-block;">
                                <img src="data:image/jpeg;base64,{img_data}" 
                                     style="width: 200px; height: 200px; object-fit: cover; border-radius: 50%; 
                                            transition: opacity 0.3s, transform 0.3s; 
                                            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                                            border: 4px solid #2E8B57;"
                                     onmouseover="this.style.opacity='0.8'; this.style.transform='scale(1.05)'" 
                                     onmouseout="this.style.opacity='1'; this.style.transform='scale(1)'"
                                     alt="{family}">
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="species-card" style="text-align: center;">
                        <h4 style="color: #2E8B57; margin: 0;">
                            <a href="{info['wiki_url']}" target="_blank" style="color: #2E8B57; text-decoration: none;">
                                {family} 🔗
                            </a>
                        </h4>
                        <p style="font-style: italic; margin: 5px 0; color: #666;">{info['scientific']}</p>
                        <p style="margin: 5px 0;"><strong>Common Name:</strong> {info['common']}</p>
                        <p style="margin: 5px 0;"><strong>Depth Range:</strong> {info['depth']}</p>
                        <p style="margin: 10px 0 0 0; font-size: 0.9em;">{info['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Dataset characteristics
    st.markdown("## 📊 Dataset Characteristics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0; color: #2E8B57;">Spatial Coverage</h3>
            <ul>
                <li><strong>Geographic Scope:</strong> Mediterranean-wide distribution</li>
                <li><strong>Regions:</strong> 8 distinct geographic zones</li>
                <li><strong>Clustering Method:</strong> K-Means spatial clustering</li>
                <li><strong>Purpose:</strong> Mitigate spatial autocorrelation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0; color: #2E8B57;">Environmental Variables</h3>
            <ul>
                <li><strong>Temporal Resolution:</strong> Monthly, seasonal, annual (2015)</li>
                <li><strong>Variable Categories:</strong> 
                    <ul>
                        <li>Chlorophyll-α concentration</li>
                        <li>Temperature (surface & depth)</li>
                        <li>Salinity profiles</li>
                        <li>Nutrient levels (Phosphate, Nitrate)</li>
                        <li>Wave height & bathymetry</li>
                        <li>Distance metrics (coast, rivers, cities, ports)</li>
                    </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Research context
    st.markdown("## 🔬 Main Purpose of This Panel")
    
    st.markdown("""
    <div class="success-box">
        <p style="margin: 0;"><strong>This intelligence panel provides:</strong></p>
        <ol style="margin: 10px 0 0 0; padding-left: 20px;">
            <li><strong>Comprehensive Data Exploration:</strong> Interactive visualizations of environmental predictors and their relationships</li>
            <li><strong>Model Performance Analysis:</strong> Detailed comparison of machine learning models for both binary and multi-class classification</li>
            <li><strong>Spatial Validation Insights:</strong> Understanding the impact of spatial autocorrelation on model generalization</li>
            <li><strong>Feature Importance Analysis:</strong> Identification of critical environmental factors driving seagrass distribution</li>
            <li><strong>Ecological Interpretation:</strong> Translation of statistical findings into actionable ecological insights</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Key innovation
    st.markdown("## 💡 Key Innovation: Geographic Zone Clustering")
    
    st.markdown("""
    <div class="warning-box">
        <h4 style="margin-top: 0;">Addressing Spatial Autocorrelation</h4>
        <p><strong>Problem:</strong> Using raw latitude/longitude as continuous predictors can cause models to:</p>
        <ul>
            <li>Memorize exact locations rather than learn environmental patterns</li>
            <li>Overfit to spatial structure in the training data</li>
            <li>Fail to generalize to new geographic locations</li>
        </ul>
        <p><strong>Solution:</strong> K-Means clustering (k=8) applied to coordinates:</p>
        <ul>
            <li>✅ Captures regional patterns without overfitting to exact positions</li>
            <li>✅ Reduces dimensionality from 2 continuous → 1 categorical variable</li>
            <li>✅ Maintains spatial information while improving model generalization</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Distribution of observations
    st.markdown("## 📍 Data Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Presence/Absence distribution
        presence_dist = df['Presence'].value_counts()
        fig_presence = go.Figure(data=[
            go.Pie(
                labels=['Presence', 'Absence'],
                values=presence_dist.values,
                hole=0.4,
                marker=dict(colors=['#2E8B57', '#DC143C']),
                textinfo='label+percent+value',
                textfont=dict(size=14)
            )
        ])
        fig_presence.update_layout(
            title="Seagrass Presence/Absence Distribution",
            height=400
        )
        st.plotly_chart(fig_presence, use_container_width=True)
    
    with col2:
        # Family distribution (for presence only)
        family_dist = df[df['Presence'] == True]['BIO_FAMILY'].value_counts()
        fig_family = go.Figure(data=[
            go.Bar(
                x=family_dist.index,
                y=family_dist.values,
                marker=dict(color='#3CB371'),
                text=family_dist.values,
                textposition='outside'
            )
        ])
        fig_family.update_layout(
            title="Seagrass Family Distribution (Presence Only)",
            xaxis_title="Family",
            yaxis_title="Count",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_family, use_container_width=True)
    
    # Footnote
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; color: #666; font-size: 0.9em;">
        <p style="margin: 0;">
            Developed by <strong>Guillem La Casta</strong><br>
            as part of the CSIC Momentum Programme: "Develop your Digital Talent"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logos footer
    logos_path = Path(__file__).resolve().parent.parent.parent / 'img' / 'logos_footnote.png'
    if logos_path.exists():
        with open(logos_path, 'rb') as img_file:
            logos_base64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <img src="data:image/png;base64,{logos_base64}" 
                 style="max-width: 100%; height: auto; margin: 0 auto;"
                 alt="Project Logos">
        </div>
        """, unsafe_allow_html=True)

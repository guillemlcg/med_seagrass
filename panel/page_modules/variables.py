"""
Variables & Statistics Page - Mediterranean Seagrass Intelligence Panel
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from pathlib import Path
import plotly.figure_factory as ff

def show(df):
    """Display variables and statistics page"""
    
    st.markdown('<h1 class="section-header">📊 Variables & Descriptive Statistics</h1>', 
                unsafe_allow_html=True)
    
    # Variable categories description
    st.markdown("## 📝 Variable Categories & Data Sources")
    
    st.markdown("""
    The dataset contains **217 environmental predictors** organized into the following categories:
    """)
    
    # Variable categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0; color: #2E8B57;">🌡️ Physical Variables</h3>
            <ul>
                <li><strong>Temperature (VOTEMPER):</strong> Monthly, seasonal, annual averages at surface and maximum depth
                    <br><em style="font-size: 0.9em; color: #666;">Original resolution: 1/12° (~8 km), daily temporal resolution</em>
                </li>
                <li><strong>Salinity (VOSALINE):</strong> Temporal series at multiple depths
                    <br><em style="font-size: 0.9em; color: #666;">Original resolution: 1/12° (~8 km), daily temporal resolution</em>
                </li>
                <li><strong>Wave Height (VHM0):</strong> Monthly variations and extremes
                    <br><em style="font-size: 0.9em; color: #666;">Original resolution: 1/24° (~4 km), 3-hourly temporal resolution</em>
                </li>
                <li><strong>Bathymetry:</strong> Mediterranean depth profile
                    <br><em style="font-size: 0.9em; color: #666;">Original resolution: 1/16° (~7 km), static variable</em>
                </li>
            </ul>
            <p><em>Source: CMEMS (Copernicus Marine Environment Monitoring Service)</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0; color: #2E8B57;">🧪 Chemical Variables</h3>
            <ul>
                <li><strong>Chlorophyll-α (CHL):</strong> Primary productivity indicator
                    <br><em style="font-size: 0.9em; color: #666;">Original resolution: 1 km, daily temporal resolution (satellite)</em>
                </li>
                <li><strong>Nitrate (NIT):</strong> Nitrogen nutrient availability
                    <br><em style="font-size: 0.9em; color: #666;">Original resolution: 1/12° (~8 km), daily temporal resolution</em>
                </li>
                <li><strong>Phosphate (PHO):</strong> Phosphorus nutrient levels
                    <br><em style="font-size: 0.9em; color: #666;">Original resolution: 1/12° (~8 km), daily temporal resolution</em>
                </li>
                <li><strong>Secchi Depth (ZSD):</strong> Water transparency measure
                    <br><em style="font-size: 0.9em; color: #666;">Original resolution: 1 km, daily temporal resolution (satellite)</em>
                </li>
            </ul>
            <p><em>Source: CMEMS Bio-Geo-Chemical models</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0; color: #2E8B57;">📍 Geographic Variables</h3>
            <ul>
                <li><strong>Distance to Coast:</strong> Proximity to coastline
                    <br><em style="font-size: 0.9em; color: #666;">Calculated using GIS spatial analysis, static variable</em>
                </li>
                <li><strong>Distance to Rivers:</strong> Major and complete river networks
                    <br><em style="font-size: 0.9em; color: #666;">Derived from OpenStreetMap, static variable</em>
                </li>
                <li><strong>Distance to Cities:</strong> Urban influence indicators
                    <br><em style="font-size: 0.9em; color: #666;">Derived from OpenStreetMap, static variable</em>
                </li>
                <li><strong>Distance to Ports:</strong> Maritime activity proximity
                    <br><em style="font-size: 0.9em; color: #666;">Derived from OpenStreetMap, static variable</em>
                </li>
                <li><strong>Geographic Zone:</strong> 8 discrete spatial clusters (K-Means)
                    <br><em style="font-size: 0.9em; color: #666;">Computed from coordinates, categorical variable</em>
                </li>
            </ul>
            <p><em>Source: GIS spatial analysis, OpenStreetMap</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0; color: #2E8B57;">🪨 Substrate Information</h3>
            <ul>
                <li><strong>Substrate Type:</strong> Categorical seabed classification
                    <br><em style="font-size: 0.9em; color: #666;">EUNIS habitat classification system, field validated</em>
                </li>
                <li>Sand, Fine mud, Muddy sand, Posidonia meadows, etc.</li>
            </ul>
            <p><em>Source: EUNIS habitat classification, field surveys</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Descriptive Statistics
    st.markdown("## 📈 Descriptive Statistics")
    
    # Select variable type for statistics
    var_type = st.radio(
        "Select Variable Type:",
        ["Static Variables", "Temporal Variables (Annual Averages)", "All Numerical Variables"],
        horizontal=True
    )
    
    # Identify variable groups
    static_cols = [
        'Med_bathym', 'Distance_to_Coast', 'Distance_to_Major_River',
        'Distance_to_Complete_River', 'Distance_to_Major_Cities',
        'Distance_to_Complete_Cities', 'Distance_to_Port'
    ]
    static_cols = [col for col in static_cols if col in df.columns]
    
    temporal_cols = [col for col in df.select_dtypes(include=np.number).columns 
                     if col not in static_cols and '_year' in col and 
                     'max' not in col.lower() and 'min' not in col.lower() and 
                     'maxDepth' not in col]
    
    all_numerical = df.select_dtypes(include=np.number).columns.tolist()
    
    # Select columns based on choice
    if var_type == "Static Variables":
        selected_cols = static_cols
    elif var_type == "Temporal Variables (Annual Averages)":
        selected_cols = temporal_cols
    else:
        selected_cols = all_numerical
    
    # Display statistics
    if selected_cols:
        stats_df = df[selected_cols].describe().T
        stats_df['range'] = stats_df['max'] - stats_df['min']
        stats_df['cv'] = (stats_df['std'] / stats_df['mean']) * 100  # Coefficient of variation
        
        st.dataframe(
            stats_df.style.format("{:.2f}").background_gradient(cmap='Greens', subset=['mean', 'std']),
            use_container_width=True,
            height=400
        )
        
        # Download button for statistics
        csv = stats_df.to_csv()
        st.download_button(
            label="📥 Download Statistics as CSV",
            data=csv,
            file_name=f"seagrass_{var_type.lower().replace(' ', '_')}_statistics.csv",
            mime="text/csv"
        )
    
    # Correlation Analysis
    st.markdown("## 🔗 Correlation Analysis")
    
    st.markdown("""
    <div class="info-box">
        <p><strong>Note:</strong> This analysis focuses on annual average variables at the sea surface 
        and static geographic variables to reduce multicollinearity and improve interpretability.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare correlation data
    correlation_vars = static_cols + temporal_cols
    if correlation_vars:
        corr_df = df[correlation_vars].corr(method='spearman')
        
        # Correlation heatmap
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_df.values,
            x=corr_df.columns,
            y=corr_df.columns,
            colorscale='RdBu_r',
            zmid=0,
            zmin=-1,
            zmax=1,
            text=np.round(corr_df.values, 2),
            texttemplate='%{text}',
            textfont={"size": 8},
            colorbar=dict(title="Correlation")
        ))
        
        fig_corr.update_layout(
            title="Spearman Correlation Matrix<br><sub>Annual Average & Static Variables</sub>",
            height=800,
            xaxis=dict(tickangle=-45),
            yaxis=dict(autorange='reversed')
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Highlight strong correlations
        st.markdown("### 🔍 Strong Correlations (|r| > 0.7)")
        
        # Extract strong correlations
        strong_corr = []
        for i in range(len(corr_df.columns)):
            for j in range(i+1, len(corr_df.columns)):
                if abs(corr_df.iloc[i, j]) > 0.7:
                    strong_corr.append({
                        'Variable 1': corr_df.columns[i],
                        'Variable 2': corr_df.columns[j],
                        'Correlation': corr_df.iloc[i, j]
                    })
        
        if strong_corr:
            strong_corr_df = pd.DataFrame(strong_corr).sort_values('Correlation', 
                                                                    key=abs, 
                                                                    ascending=False)
            st.dataframe(
                strong_corr_df.style.background_gradient(cmap='RdYlGn', subset=['Correlation']),
                use_container_width=True
            )
        else:
            st.info("No correlations with |r| > 0.7 found.")
    
    # Geographic Distribution
    st.markdown("## 🗺️ Geographic Distribution")
    
    st.markdown("""
    The dataset covers the Mediterranean Sea with observations clustered into **8 geographic zones** 
    to address spatial autocorrelation in modeling.
    """)
    
    # Zone distribution
    zone_counts = df['GEOGRAPHIC_ZONE'].value_counts().sort_index()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Zone distribution bar chart
        fig_zones = go.Figure(data=[
            go.Bar(
                x=[f"Zone {i}" for i in zone_counts.index],
                y=zone_counts.values,
                marker=dict(
                    color=zone_counts.values,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Count")
                ),
                text=zone_counts.values,
                textposition='outside'
            )
        ])
        
        fig_zones.update_layout(
            title="Observations per Geographic Zone",
            xaxis_title="Geographic Zone",
            yaxis_title="Number of Observations",
            height=400
        )
        
        st.plotly_chart(fig_zones, use_container_width=True)
    
    with col2:
        # Zone statistics table
        zone_stats = pd.DataFrame({
            'Zone': [f"Zone {i}" for i in zone_counts.index],
            'Count': zone_counts.values,
            'Percentage': (zone_counts.values / len(df) * 100).round(2)
        })
        
        st.markdown("### Zone Distribution Table")
        st.dataframe(zone_stats, use_container_width=True, height=400)
    
    # Interactive scatter map
    st.markdown("### 🌍 Interactive Geographic Map")
    
    # Map coloring option
    map_color_by = st.radio(
        "Color points by:",
        ["Geographic Zone", "Presence/Absence"],
        horizontal=True
    )
    
    # Create map based on selection
    if map_color_by == "Geographic Zone":
        # Create a color scale for geographic zones
        zone_colors = px.colors.qualitative.Set2
        
        # Create map colored by geographic zone
        df_map = df.copy()
        df_map['Zone Label'] = df_map['GEOGRAPHIC_ZONE'].apply(lambda x: f"Zone {x}")
        
        fig_map = px.scatter_mapbox(
            df_map,
            lat='LATITUDE',
            lon='LONGITUDE',
            color='Zone Label',
            hover_data=['BIO_FAMILY', 'Presence', 'Med_bathym'],
            color_discrete_sequence=zone_colors,
            labels={'Zone Label': 'Geographic Zone'},
            zoom=4,
            height=600
        )
        
        fig_map.update_traces(marker=dict(size=8, opacity=0.7))
        
    else:  # Presence/Absence
        fig_map = px.scatter_mapbox(
            df,
            lat='LATITUDE',
            lon='LONGITUDE',
            color='Presence',
            hover_data=['BIO_FAMILY', 'GEOGRAPHIC_ZONE', 'Med_bathym'],
            color_discrete_map={True: '#2E8B57', False: '#DC143C'},
            labels={'Presence': 'Seagrass Present'},
            zoom=4,
            height=600
        )
        
        fig_map.update_traces(marker=dict(size=8, opacity=0.7))
    
    fig_map.update_layout(
        mapbox_style="open-street-map",
        title=f"Mediterranean Seagrass Distribution - Colored by {map_color_by}",
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        legend=dict(
            title=dict(text=map_color_by, font=dict(size=14, color='black')),
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="gray",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Distribution Analysis
    st.markdown("## 📊 Variable Distributions")
    
    # Filters
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        # Variable type filter
        var_category = st.selectbox(
            "📂 Variable Type:",
            options=[
                "All Variables",
                "Geographic/Static",
                "Temperature",
                "Salinity", 
                "Chlorophyll-α",
                "Nutrients (Nitrate/Phosphate)",
                "Wave Height",
                "Water Transparency (Secchi)"
            ]
        )
    
    with col_filter2:
        # Temporal period filter
        temporal_period = st.selectbox(
            "📅 Temporal Period:",
            options=[
                "All Periods",
                "Annual (Year)",
                "Seasonal (Winter, Spring, Summer, Autumn)",
                "Monthly (Individual months)"
            ]
        )
    
    # Additional month filter (only shown when Monthly is selected)
    specific_months = None
    if temporal_period == "Monthly (Individual months)" and var_category not in ["Geographic/Static"]:
        specific_months = st.multiselect(
            "🗓️ Select Specific Month(s):",
            options=[
                "January (1)", "February (2)", "March (3)", "April (4)", 
                "May (5)", "June (6)", "July (7)", "August (8)", 
                "September (9)", "October (10)", "November (11)", "December (12)"
            ],
            default=None,
            help="Select one or more months to filter the variables"
        )
    
    # Filter variables based on selection
    filtered_vars = []
    
    # Apply variable type filter
    if var_category == "Geographic/Static":
        filtered_vars = [col for col in all_numerical if any(keyword in col for keyword in 
                        ['Distance', 'bathym', 'LATITUDE', 'LONGITUDE', 'GEOGRAPHIC_ZONE'])]
    elif var_category == "Temperature":
        filtered_vars = [col for col in all_numerical if 'VOTEMPER' in col or 'TEMP' in col.upper()]
    elif var_category == "Salinity":
        filtered_vars = [col for col in all_numerical if 'VOSALINE' in col or 'SAL' in col.upper()]
    elif var_category == "Chlorophyll-α":
        filtered_vars = [col for col in all_numerical if 'CHL' in col.upper()]
    elif var_category == "Nutrients (Nitrate/Phosphate)":
        filtered_vars = [col for col in all_numerical if any(keyword in col.upper() for keyword in ['NIT', 'PHO', 'NUTRIENT'])]
    elif var_category == "Wave Height":
        filtered_vars = [col for col in all_numerical if 'VHM0' in col or 'WAVE' in col.upper()]
    elif var_category == "Water Transparency (Secchi)":
        filtered_vars = [col for col in all_numerical if 'ZSD' in col or 'SECCHI' in col.upper()]
    else:  # All Variables
        filtered_vars = all_numerical.copy()
    
    # Apply temporal period filter
    if temporal_period != "All Periods" and var_category not in ["Geographic/Static", "All Variables"]:
        if temporal_period == "Annual (Year)":
            filtered_vars = [col for col in filtered_vars if '_year' in col.lower()]
        elif temporal_period == "Seasonal (Winter, Spring, Summer, Autumn)":
            filtered_vars = [col for col in filtered_vars if any(season in col.lower() 
                            for season in ['winter', 'spring', 'summer', 'autumn', 'fall'])]
        elif temporal_period == "Monthly (Individual months)":
            # If specific months are selected, filter by those
            if specific_months:
                # Create mapping of full month names to possible abbreviations/patterns
                # Support both underscore (_) and hyphen (-) separators
                month_patterns = {
                    'January (1)': ['january', 'jan_', 'jan-', 'jan', '_1_', '-1-', '_01_', '-01-', '_1', '-1'],
                    'February (2)': ['february', 'feb_', 'feb-', 'feb', '_2_', '-2-', '_02_', '-02-', '_2', '-2'],
                    'March (3)': ['march', 'mar_', 'mar-', 'mar', '_3_', '-3-', '_03_', '-03-', '_3', '-3'],
                    'April (4)': ['april', 'apr_', 'apr-', 'apr', '_4_', '-4-', '_04_', '-04-', '_4', '-4'],
                    'May (5)': ['may_', 'may-', 'may', '_5_', '-5-', '_05_', '-05-', '_5', '-5'],
                    'June (6)': ['june', 'jun_', 'jun-', 'jun', '_6_', '-6-', '_06_', '-06-', '_6', '-6'],
                    'July (7)': ['july', 'jul_', 'jul-', 'jul', '_7_', '-7-', '_07_', '-07-', '_7', '-7'],
                    'August (8)': ['august', 'aug_', 'aug-', 'aug', '_8_', '-8-', '_08_', '-08-', '_8', '-8'],
                    'September (9)': ['september', 'sep_', 'sep-', 'sep', 'sept', '_9_', '-9-', '_09_', '-09-', '_9', '-9'],
                    'October (10)': ['october', 'oct_', 'oct-', 'oct', '_10_', '-10-', '_10', '-10'],
                    'November (11)': ['november', 'nov_', 'nov-', 'nov', '_11_', '-11-', '_11', '-11'],
                    'December (12)': ['december', 'dec_', 'dec-', 'dec', '_12_', '-12-', '_12', '-12']
                }
                
                # Get patterns for selected months
                selected_patterns = []
                for month in specific_months:
                    selected_patterns.extend(month_patterns.get(month, []))
                
                # Filter columns that contain any of the selected month patterns
                filtered_vars = [col for col in filtered_vars 
                               if any(pattern in col.lower() for pattern in selected_patterns)]
            else:
                # If no specific months selected, show all monthly variables
                # Include both text month names and numeric patterns with _ or - separators
                months = ['january', 'february', 'march', 'april', 'may', 'june', 
                         'july', 'august', 'september', 'october', 'november', 'december',
                         'jan_', 'feb_', 'mar_', 'apr_', 'may_', 'jun_', 
                         'jul_', 'aug_', 'sep_', 'oct_', 'nov_', 'dec_',
                         'jan-', 'feb-', 'mar-', 'apr-', 'may-', 'jun-', 
                         'jul-', 'aug-', 'sep-', 'oct-', 'nov-', 'dec-',
                         '_1_', '_2_', '_3_', '_4_', '_5_', '_6_', 
                         '_7_', '_8_', '_9_', '_10_', '_11_', '_12_',
                         '-1-', '-2-', '-3-', '-4-', '-5-', '-6-',
                         '-7-', '-8-', '-9-', '-10-', '-11-', '-12-',
                         '_01_', '_02_', '_03_', '_04_', '_05_', '_06_',
                         '_07_', '_08_', '_09_',
                         '-01-', '-02-', '-03-', '-04-', '-05-', '-06-',
                         '-07-', '-08-', '-09-']
                filtered_vars = [col for col in filtered_vars if any(month in col.lower() for month in months)]
    
    # Remove duplicates and sort
    filtered_vars = sorted(list(set(filtered_vars)))
    
    # Debug: Show what we're looking for (temporary)
    if temporal_period == "Monthly (Individual months)" and specific_months and len(filtered_vars) == 0:
        st.warning("🔍 Debug: No variables found. Let me show you what's available...")
        
        # Show what patterns we searched for
        month_patterns = {
            'January (1)': ['january', 'jan_', 'jan-', 'jan', '_1_', '-1-', '_01_', '-01-', '_1', '-1'],
            'February (2)': ['february', 'feb_', 'feb-', 'feb', '_2_', '-2-', '_02_', '-02-', '_2', '-2'],
            'March (3)': ['march', 'mar_', 'mar-', 'mar', '_3_', '-3-', '_03_', '-03-', '_3', '-3'],
            'April (4)': ['april', 'apr_', 'apr-', 'apr', '_4_', '-4-', '_04_', '-04-', '_4', '-4'],
            'May (5)': ['may_', 'may-', 'may', '_5_', '-5-', '_05_', '-05-', '_5', '-5'],
            'June (6)': ['june', 'jun_', 'jun-', 'jun', '_6_', '-6-', '_06_', '-06-', '_6', '-6'],
            'July (7)': ['july', 'jul_', 'jul-', 'jul', '_7_', '-7-', '_07_', '-07-', '_7', '-7'],
            'August (8)': ['august', 'aug_', 'aug-', 'aug', '_8_', '-8-', '_08_', '-08-', '_8', '-8'],
            'September (9)': ['september', 'sep_', 'sep-', 'sep', 'sept', '_9_', '-9-', '_09_', '-09-', '_9', '-9'],
            'October (10)': ['october', 'oct_', 'oct-', 'oct', '_10_', '-10-', '_10', '-10'],
            'November (11)': ['november', 'nov_', 'nov-', 'nov', '_11_', '-11-', '_11', '-11'],
            'December (12)': ['december', 'dec_', 'dec-', 'dec', '_12_', '-12-', '_12', '-12']
        }
        selected_patterns = []
        for month in specific_months:
            selected_patterns.extend(month_patterns.get(month, []))
        
        st.write(f"**Searching for patterns:** {selected_patterns}")
        
        # Show sample column names to understand the pattern
        if var_category == "Temperature":
            sample_cols = [col for col in all_numerical if 'VOTEMPER' in col or 'TEMP' in col.upper()][:30]
        elif var_category == "Salinity":
            sample_cols = [col for col in all_numerical if 'VOSALINE' in col or 'SAL' in col.upper()][:30]
        elif var_category == "Chlorophyll-α":
            sample_cols = [col for col in all_numerical if 'CHL' in col.upper()][:30]
        else:
            sample_cols = [col for col in all_numerical][:30]
            
        with st.expander("View sample column names from your selection"):
            for col in sample_cols:
                st.code(col)
    
    # Display filter results
    st.info(f"📊 **{len(filtered_vars)} variables** match your filter criteria")
    
    # Select variable to visualize
    if filtered_vars:
        viz_var = st.selectbox(
            "Select a variable to visualize:",
            options=filtered_vars,
            index=0
        )
        
        if viz_var:
            col1, col2 = st.columns(2)
            
            with col1:
                # Histogram
                fig_hist = px.histogram(
                    df,
                    x=viz_var,
                    nbins=50,
                    color='Presence',
                    color_discrete_map={True: '#2E8B57', False: '#DC143C'},
                    labels={'Presence': 'Seagrass Present'},
                    title=f"Distribution of {viz_var}"
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Box plot by presence
                fig_box = px.box(
                    df,
                    x='Presence',
                    y=viz_var,
                    color='Presence',
                    color_discrete_map={True: '#2E8B57', False: '#DC143C'},
                    labels={'Presence': 'Seagrass Present'},
                    title=f"{viz_var} by Presence/Absence"
                )
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Statistics by presence
            st.markdown(f"### Statistics for {viz_var}")
            presence_stats = df.groupby('Presence')[viz_var].describe().T
            presence_stats.columns = ['Absence', 'Presence']
            st.dataframe(
                presence_stats.style.format("{:.2f}").background_gradient(cmap='RdYlGn', axis=1),
                use_container_width=True
            )
    else:
        st.warning("⚠️ No variables match the selected filter criteria. Please adjust your filters.")
    
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

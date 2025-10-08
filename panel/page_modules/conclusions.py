"""
Conclusions & Future Steps Page - Mediterranean Seagrass Intelligence Panel
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
from pathlib import Path

def show(df):
    """Display conclusions and future steps page"""
    
    st.markdown('<h1 class="section-header">📝 Conclusions & Future Steps</h1>', 
                unsafe_allow_html=True)
    
    # Major achievements
    st.markdown("## 🎯 Major Achievements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h3 style="margin-top: 0;">🏆 Binary Classification</h3>
            <ul>
                <li><strong>Exceptional Performance:</strong> 98.8% accuracy (Stratified CV)</li>
                <li><strong>Realistic Performance:</strong> 88.0% accuracy (Spatial CV)</li>
                <li><strong>Best Model:</strong> Random Forest with 99.9% ROC-AUC (Stratified), 95.6% (Spatial)</li>
                <li><strong>Performance Drop:</strong> 10.8 percentage points from Stratified to Spatial CV</li>
                <li><strong>Key Discovery:</strong> Chlorophyll-α is the most important predictor (7 of top 10)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
            <h3 style="margin-top: 0;">🔢 Multi-Class Classification</h3>
            <ul>
                <li><strong>High Accuracy:</strong> 86.1% accuracy (Stratified CV - Random Forest)</li>
                <li><strong>Spatial Reality:</strong> 68.1% accuracy (Spatial CV - K Neighbors)</li>
                <li><strong>Macro F1:</strong> 82.2% → 62.1% (19-64% drops across models)</li>
                <li><strong>Best Spatial Model:</strong> K Neighbors (62.1% Macro F1) most robust</li>
                <li><strong>Key Discovery:</strong> Water clarity (Secchi depth) dominates (7 of top 10 features)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance summary visualization
    st.markdown("## 📊 Overall Performance Summary")
    
    summary_data = {
        'Task': ['Binary - Stratified', 'Binary - Spatial', 
                 'Multi-Class - Stratified', 'Multi-Class - Spatial'],
        'Accuracy': [0.988, 0.880, 0.861, 0.681],
        'Primary Metric': [0.999, 0.956, 0.822, 0.621],
        'Model': ['Random Forest', 'Random Forest', 'Random Forest', 'K Neighbors']
    }
    
    fig_summary = go.Figure()
    
    fig_summary.add_trace(go.Bar(
        name='Accuracy',
        x=summary_data['Task'],
        y=summary_data['Accuracy'],
        text=[f"{v:.2%}" for v in summary_data['Accuracy']],
        textposition='outside',
        marker_color='#2E8B57'
    ))
    
    fig_summary.add_trace(go.Bar(
        name='F1 / ROC-AUC',
        x=summary_data['Task'],
        y=summary_data['Primary Metric'],
        text=[f"{v:.2%}" for v in summary_data['Primary Metric']],
        textposition='outside',
        marker_color='#3CB371'
    ))
    
    fig_summary.update_layout(
        title="Performance Comparison Across Tasks and CV Strategies",
        yaxis_title="Score",
        barmode='group',
        height=500,
        yaxis=dict(range=[0, 1.1]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_summary, use_container_width=True)
    
    # Key scientific insights
    st.markdown("## 🔬 Key Scientific Insights")
    
    st.markdown("""
    <div class="info-box">
        <h3 style="margin-top: 0;">Environmental Drivers of Seagrass Distribution</h3>
    </div>
    """, unsafe_allow_html=True)
    
    insights = [
        {
            'factor': '🌊 Chlorophyll-α (Primary Productivity)',
            'finding': 'Most important predictor for presence/absence detection',
            'ecological': 'Seagrasses thrive in areas with specific productivity levels - not too oligotrophic, not too eutrophic',
            'management': 'Water quality monitoring should prioritize chlorophyll measurements'
        },
        {
            'factor': '📍 Distance to Coast',
            'finding': 'Strong predictor, especially for shallow-water species',
            'ecological': 'Most Mediterranean seagrasses are coastal, within 0-5 km from shore',
            'management': 'Conservation efforts should focus on near-shore coastal zones'
        },
        {
            'factor': '🧂 Salinity',
            'finding': 'Critical for both presence and species-level discrimination',
            'ecological': 'Each family has specific salinity tolerance ranges',
            'management': 'Freshwater inputs (rivers, desalination) may alter seagrass distribution'
        },
        {
            'factor': '💧 Water Clarity (Secchi Depth)',
            'finding': 'Dominates family classification (7 of top 10 features are Secchi depth measures)',
            'ecological': 'Light availability is critical for seagrass photosynthesis and family distribution',
            'management': 'Reducing turbidity and maintaining water clarity essential for conservation'
        },
        {
            'factor': '🧪 Nutrients (Phosphate, Nitrate)',
            'finding': 'Moderate importance, with phosphate showing depth-dependent effects',
            'ecological': 'Seagrasses sensitive to eutrophication, prefer low-nutrient conditions',
            'management': 'Agricultural runoff and urban pollution are key threats'
        }
    ]
    
    for i, insight in enumerate(insights, 1):
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #2E8B57; margin-top: 0;">{i}. {insight['factor']}</h4>
            <p><strong>Statistical Finding:</strong> {insight['finding']}</p>
            <p><strong>Ecological Interpretation:</strong> {insight['ecological']}</p>
            <p><strong>Management Implication:</strong> {insight['management']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Critical methodological findings
    st.markdown("## ⚠️ Critical Methodological Findings")
    
    st.markdown("""
    <div class="warning-box">
        <h3 style="margin-top: 0;">Spatial Autocorrelation Impact</h3>
        <p><strong>Key Discovery:</strong> Cross-validation strategy has a <em>massive</em> impact on 
        performance estimates:</p>
        <ul>
            <li><strong>Binary Classification:</strong> 10.8% accuracy drop (Stratified → Spatial)</li>
            <li><strong>Multi-Class Classification:</strong> 18.0% accuracy drop, 20.1% Macro F1 drop</li>
        </ul>
        <p><strong>Why This Matters:</strong></p>
        <ol>
            <li><strong>Model Selection:</strong> Rankings can change between CV strategies</li>
            <li><strong>Performance Expectations:</strong> Stratified CV overestimates real-world performance</li>
            <li><strong>Geographic Generalization:</strong> Spatial CV reveals true predictive power for new regions</li>
            <li><strong>Research Validity:</strong> Many ecological studies may overestimate model accuracy</li>
        </ol>
        <p><strong>Recommendation:</strong> Always use spatial/geographic cross-validation for species 
        distribution models to obtain realistic performance estimates.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Future steps
    st.markdown("## 🚀 Recommendations for Next Steps")
    
    tab1, tab2, tab3 = st.tabs(["📈 Modeling Phase", "🌍 Deployment", "🔬 Research Extensions"])
    
    with tab1:
        st.markdown("""
        ### Modeling Improvements
        
        #### 1️⃣ Hyperparameter Optimization
        - Conduct grid search for Random Forest and Extra Trees
        - Optimize specifically for spatial CV performance
        - Consider ensemble methods combining multiple top models
        
        #### 2️⃣ Feature Engineering
        - Create interaction terms (e.g., Temperature × Depth)
        - Engineer temporal features (seasonal contrasts, trends)
        - Add derived variables (e.g., nutrient ratios)
        
        #### 3️⃣ Class Imbalance Handling
        - SMOTE or ADASYN for minority classes (Halophila, Ruppia)
        - Cost-sensitive learning with class weights
        - Focal loss for multi-class classification
        
        #### 4️⃣ Model Interpretability
        - SHAP values for instance-level explanations
        - Partial dependence plots for feature effects
        - ICE (Individual Conditional Expectation) curves
        
        #### 5️⃣ Uncertainty Quantification
        - Implement prediction intervals (quantile regression forests)
        - Calibration analysis (reliability diagrams)
        - Conformal prediction for coverage guarantees
        
        #### 6️⃣ Neural Networks & Deep Learning
        - **Multi-Layer Perceptrons (MLPs):** For tabular feature learning
        - **Attention Mechanisms:** To automatically identify important features
        - **Neural Additive Models (NAMs):** Interpretable neural networks
        - **TabNet:** Self-supervised learning for tabular data
        - **AutoInt/Deep FM:** Automatic feature interaction learning
        - **Spatial-Aware Neural Networks:** Incorporate geographic coordinates
        - **Ensemble Deep Learning:** Combine neural networks with tree-based models
        """)
    
    with tab2:
        st.markdown("""
        ### Deployment Considerations
        
        #### 1️⃣ Model Packaging
        - Serialize final model with `joblib` or `pickle`
        - Create prediction pipeline with preprocessing steps
        - Version control for model tracking (MLflow, DVC)
        
        #### 2️⃣ API Development
        - RESTful API with FastAPI or Flask
        - Batch prediction endpoints for large datasets
        - Real-time prediction service for monitoring
        
        #### 3️⃣ Geographic Information System (GIS) Integration
        - Export predictions as GeoTIFF or shapefiles
        - Integrate with QGIS or ArcGIS workflows
        - Web mapping interface (Folium, Leaflet)
        
        #### 4️⃣ Operational Monitoring
        - Track prediction confidence over time
        - Detect data drift (environmental changes)
        - Alert system for low-confidence predictions
        
        #### 5️⃣ User Interface
        - Web dashboard for managers and researchers
        - Mobile app for field biologists
        - Automated reporting system
        """)
    
    with tab3:
        st.markdown("""
        ### Research Extensions
        
        #### 1️⃣ Temporal Dynamics
        - Multi-year analysis (2010-2023) to capture trends
        - Seasonal models for phenology
        - Time series forecasting for future distributions
        
        #### 2️⃣ Climate Change Scenarios
        - Project seagrass distributions under RCP scenarios
        - Assess vulnerability of different families
        - Identify climate refugia
        
        #### 3️⃣ High-Resolution Remote Sensing
        - Integrate satellite imagery (Sentinel-2, Landsat)
        - **Convolutional Neural Networks (CNNs)** for multispectral image analysis
        - **Vision Transformers (ViT)** for large-scale satellite data
        - **U-Net architectures** for seagrass bed segmentation
        - Drone surveys with **object detection models** (YOLO, Faster R-CNN)
        - Multi-modal fusion: Combine tabular + image data
        
        #### 4️⃣ Mechanistic Modeling Integration
        - Combine ML predictions with eco-physiological models
        - Incorporate species niche theory
        - Validate against experimental data
        
        #### 5️⃣ Biodiversity Analysis
        - Predict ecosystem services (carbon sequestration, nursery habitat)
        - Model co-occurrence patterns with fauna
        - Identify biodiversity hotspots
        
        #### 6️⃣ Threat Assessment
        - Incorporate anthropogenic stressors (pollution, fishing, anchoring)
        - Predict invasion risk (Halophila expansion)
        - Conservation prioritization
        """)
    
    # Data limitations and caveats
    st.markdown("## ⚠️ Data Limitations & Caveats")
    
    st.markdown("""
    <div class="warning-box">
        <h4 style="margin-top: 0;">Important Considerations</h4>
        <ol>
            <li><strong>Temporal Snapshot:</strong> Data from 2015 only - may not capture long-term trends</li>
            <li><strong>Pseudo-Absences:</strong> Absence points may not be true absences (detection issues)</li>
            <li><strong>Spatial Bias:</strong> Sampling concentrated in accessible coastal areas</li>
            <li><strong>Substrate Uncertainty:</strong> Many observations have "Unknown" substrate</li>
            <li><strong>Model Resolution:</strong> Environmental predictors at ~1km resolution may miss microhabitat effects</li>
            <li><strong>Class Imbalance:</strong> Posidonia heavily overrepresented; rare families understudied</li>
            <li><strong>Generalization:</strong> Models trained on Mediterranean may not transfer to other regions</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("## 🌊 Conservation Implications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4 style="margin-top: 0;">💚 Protected Areas</h4>
            <ul>
                <li>Use models to identify high-probability seagrass zones</li>
                <li>Prioritize areas with multiple family co-occurrence</li>
                <li>Focus on rare species habitats (Halophila, Ruppia)</li>
                <li>Monitor temporal changes in suitable habitat</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
            <h4 style="margin-top: 0;">🚨 Threat Mitigation</h4>
            <ul>
                <li>Identify vulnerable areas (low salinity, high nutrient zones)</li>
                <li>Target water quality improvement efforts</li>
                <li>Regulate coastal development in predicted habitats</li>
                <li>Early warning system for invasive species spread</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Final thoughts
    st.markdown("## 💭 Final Thoughts")
    
    st.markdown("""
    <div class="info-box">
        <p style="font-size: 1.1em;"><strong>This analysis demonstrates the power of machine learning 
        for ecological prediction, while revealing critical insights about seagrass distribution and 
        essential methodological considerations.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🔬 Key Scientific Discoveries")
    st.markdown("""
    - **Binary Classification:** Chlorophyll-α (primary productivity) dominates presence/absence prediction with 88.0% spatial accuracy
    - **Multi-Class Classification:** Water clarity (Secchi depth) is the strongest family discriminator, appearing in 7 of top 10 features
    - **Methodological Insight:** Spatial cross-validation reveals realistic performance with 10.8% (binary) and 18.0% (multi-class) accuracy drops
    - **Model Robustness:** Random Forest excels in stratified CV, while K Neighbors shows best spatial generalization for family classification
    """)
    
    st.markdown("#### 🌊 Mediterranean Seagrass: A Critical Ecosystem")
    st.markdown("These meadows are among the most valuable marine ecosystems, providing essential services:")
    st.markdown("""
    - 🌊 **Carbon Sequestration:** "Blue carbon" storage (up to 83,000 metric tons CO₂/km²/year)
    - 🐟 **Biodiversity Hotspot:** Nursery habitat for commercial fish species and endangered fauna
    - 🏖️ **Coastal Protection:** Wave attenuation (up to 40% reduction) and sediment stabilization
    - 💧 **Water Quality:** Nutrient uptake, pathogen removal, and oxygen production
    """)
    
    st.markdown("#### ⚠️ Conservation Imperatives")
    st.markdown("**Mediterranean seagrass meadows have declined by 13-50% since 1960s due to:**")
    st.markdown("""
    - Coastal development and anchoring damage
    - Water quality degradation (eutrophication, turbidity)
    - Climate change (warming, sea-level rise)
    - Invasive species competition
    """)
    
    st.markdown("**Our models identify two critical environmental factors:**")
    st.markdown("""
    1. **Chlorophyll-α levels** indicate suitable productivity zones for seagrass presence
    2. **Water clarity (Secchi depth)** determines which families can establish and persist
    """)
    
    st.markdown("")  # Add spacing
    
    st.markdown("""
    <div class="info-box">
        <p><em><strong>This intelligence panel provides actionable, spatially-aware predictions for Mediterranean 
        seagrass conservation.</strong> The models achieve strong performance while accounting for geographic 
        generalization—a critical advance over traditional methods. By identifying key environmental drivers 
        (water clarity and productivity), we enable targeted management interventions: improving water quality, 
        establishing marine protected areas, and monitoring climate impacts.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <p><em>The next frontier is integrating these predictions 
        with remote sensing, neural networks, and real-time monitoring to create a comprehensive early-warning 
        system for seagrass decline across the Mediterranean basin.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # References
    st.markdown("---")
    st.markdown("## 📚 References & Resources")
    
    st.markdown("""
    ### Primary Reference
    **Effrosynidis, D., Arampatzis, A., & Sylaios, G. (2018).**  
    *Seagrass detection in the Mediterranean: A supervised learning approach.*  
    Ecological Informatics, 48, 158-175.  
    DOI: [10.1016/j.ecoinf.2018.09.004](https://doi.org/10.1016/j.ecoinf.2018.09.004)
    
    ### Additional Resources
    - **CMEMS:** Copernicus Marine Environment Monitoring Service - [marine.copernicus.eu](https://marine.copernicus.eu/)
    - **EUNIS:** European Nature Information System - Habitat Classification
    - **IUCN Red List:** Seagrass species conservation status
    - **Seagrass Watch:** Global seagrass monitoring network
    - **MedSeagrass:** Mediterranean seagrass conservation initiative
    
    ### Machine Learning References
    - Breiman, L. (2001). Random forests. *Machine Learning*, 45, 5-32.
    - Roberts et al. (2017). Cross-validation strategies for data with temporal, spatial, 
      hierarchical, or phylogenetic structure. *Ecography*, 40(8), 913-929.
    """)
    
    # Acknowledgments
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;">
        <h3 style="color: #2E8B57;">🙏 Acknowledgments</h3>
        <p>This intelligence panel is built upon the pioneering work of Effrosynidis et al. (2018) 
        and the invaluable data provided by the Copernicus Marine Service and contributing research institutions.</p>
        <p style="margin-top: 1rem;"><strong>For the Mediterranean Sea and its precious seagrass meadows 🌊🌿</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
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

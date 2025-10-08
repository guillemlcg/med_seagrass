"""
Multi-Class Classification Page - Mediterranean Seagrass Intelligence Panel
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
from pathlib import Path

def show(df):
    """Display multi-class classification analysis page"""
    
    st.markdown('<h1 class="section-header">🔢 Multi-Class Classification: Family Detection</h1>', 
                unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="info-box">
        <h3 style="margin-top: 0;">Objective</h3>
        <p>When seagrass is present, classify the observation into one of <strong>5 seagrass families</strong>:</p>
        <ul>
            <li><strong>Posidonia</strong> - Endemic Mediterranean species</li>
            <li><strong>Cymodocea</strong> - Fast-growing, adaptable</li>
            <li><strong>Zostera</strong> - Eelgrass, prefers sheltered areas</li>
            <li><strong>Halophila</strong> - Invasive from Red Sea</li>
            <li><strong>Ruppia</strong> - Lagoon specialist</li>
        </ul>
        <p><strong>Challenge:</strong> Significant class imbalance with Cymodocea dominating the dataset</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Class distribution
    st.markdown("## 📊 Class Distribution")
    
    presence_df = df[df['Presence'] == True].copy()
    family_counts = presence_df['BIO_FAMILY'].value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_dist = go.Figure()
        
        fig_dist.add_trace(go.Bar(
            x=family_counts.index,
            y=family_counts.values,
            marker=dict(
                color=['#2E8B57', '#3CB371', '#66CDAA', '#8FBC8F', '#90EE90'],
            ),
            text=family_counts.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Percentage: %{customdata:.1f}%<extra></extra>',
            customdata=(family_counts.values / family_counts.sum() * 100)
        ))
        
        fig_dist.update_layout(
            title="Seagrass Family Distribution (Presence Only)",
            xaxis_title="Family",
            yaxis_title="Number of Observations",
            height=400
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        st.markdown("### Class Statistics")
        
        class_stats = pd.DataFrame({
            'Family': family_counts.index,
            'Count': family_counts.values,
            'Percentage': (family_counts.values / family_counts.sum() * 100).round(2)
        })
        
        st.dataframe(
            class_stats.style.background_gradient(cmap='Greens', subset=['Count', 'Percentage']),
            use_container_width=True,
            height=250
        )
        
        st.markdown("""
        <div class="warning-box" style="margin-top: 1rem;">
            <p style="margin: 0;"><strong>⚠️ Class Imbalance:</strong></p>
            <p style="margin: 5px 0 0 0;">Cymodocea represents the majority class, 
            which may bias model predictions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Model comparison results (from EDA) - 7 models tested
    # Note: Multiclass uses Macro F1 as primary metric due to class imbalance
    # Updated with corrected CV strategy results
    multiclass_stratified = {
        'Model': ['K Neighbors', 'SVM-Linear', 'Random Forest', 'Logistic Regression', 
                  'Ridge Classifier', 'Decision Tree', 'LDA'],
        'Accuracy': [0.8164, 0.7199, 0.8606, 0.8084, 0.8186, 0.8594, 0.8277],
        'Precision': [0.7921, 0.6893, 0.8470, 0.7760, 0.7952, 0.8419, 0.8099],
        'Recall': [0.8164, 0.7199, 0.8606, 0.8084, 0.8186, 0.8594, 0.8277],
        'Macro_F1': [0.7659, 0.6572, 0.8222, 0.7454, 0.7590, 0.8169, 0.7781]
    }
    
    multiclass_spatial = {
        'Model': ['K Neighbors', 'SVM-Linear', 'Random Forest', 'Logistic Regression', 
                  'Ridge Classifier', 'Decision Tree', 'LDA'],
        'Accuracy': [0.6809, 0.6413, 0.6303, 0.5580, 0.5453, 0.5088, 0.3629],
        'Precision': [0.6396, 0.6083, 0.5951, 0.5196, 0.5064, 0.4696, 0.3168],
        'Recall': [0.6809, 0.6413, 0.6303, 0.5580, 0.5453, 0.5088, 0.3629],
        'Macro_F1': [0.6209, 0.5844, 0.5758, 0.4955, 0.4821, 0.4390, 0.2788]
    }
    
    df_mc_strat = pd.DataFrame(multiclass_stratified)
    df_mc_spatial = pd.DataFrame(multiclass_spatial)
    
    # Model selection and comparison
    st.markdown("## ⚙️ Interactive Model Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cv_type = st.selectbox(
            "Select Cross-Validation Strategy:",
            ["Stratified K-Fold (10-fold)", "Spatial Cross-Validation (GroupKFold by Zone)"],
            help="Spatial CV accounts for geographic clustering",
            key="mc_cv"
        )
    
    with col2:
        metric = st.selectbox(
            "Select Performance Metric:",
            ["Macro_F1", "Accuracy", "Precision", "Recall"],
            help="Macro F1 gives equal weight to all classes (recommended for imbalanced datasets)",
            key="mc_metric"
        )
    
    # Select appropriate dataframe
    df_mc_results = df_mc_strat if "Stratified" in cv_type else df_mc_spatial
    
    # Performance comparison
    st.markdown(f"### 📊 Model Performance Comparison - {metric}")
    
    fig_mc_compare = go.Figure()
    
    fig_mc_compare.add_trace(go.Bar(
        x=df_mc_results['Model'],
        y=df_mc_results[metric],
        marker=dict(
            color=df_mc_results[metric],
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title=metric)
        ),
        text=df_mc_results[metric].round(2),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' + metric + ': %{y:.2f}<extra></extra>'
    ))
    
    fig_mc_compare.update_layout(
        title=f"{metric} Comparison - {cv_type}",
        xaxis_title="Model",
        yaxis_title=metric,
        height=500,
        xaxis_tickangle=-45,
        yaxis_range=[0, 1]
    )
    
    st.plotly_chart(fig_mc_compare, use_container_width=True)
    
    # Detailed comparison
    st.markdown("### 🔍 Detailed Multi-Metric Comparison")
    
    selected_mc_models = st.multiselect(
        "Select models to compare:",
        options=df_mc_results['Model'].tolist(),
        default=['K Neighbors', 'SVM-Linear', 'Random Forest'],
        key="mc_models"
    )
    
    if selected_mc_models:
        # Create comparison chart
        metrics_list = ['Accuracy', 'Precision', 'Recall', 'Macro_F1']
        
        fig_mc_radar = go.Figure()
        
        for model in selected_mc_models:
            model_data = df_mc_results[df_mc_results['Model'] == model].iloc[0]
            values = [model_data[m] for m in metrics_list]
            values.append(values[0])
            
            fig_mc_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics_list + [metrics_list[0]],
                fill='toself',
                name=model
            ))
        
        fig_mc_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title=f"Multi-Metric Comparison - {cv_type}",
            height=500
        )
        
        st.plotly_chart(fig_mc_radar, use_container_width=True)
        
        # Detailed table
        st.markdown("#### 📋 Detailed Metrics Table")
        filtered_mc = df_mc_results[df_mc_results['Model'].isin(selected_mc_models)].copy()
        
        # Apply styling
        styled_mc = filtered_mc.style.format(
            {
                'Accuracy': '{:.2f}',
                'Precision': '{:.2f}',
                'Recall': '{:.2f}',
                'Macro_F1': '{:.2f}'
            }
        )
        styled_mc = styled_mc.background_gradient(cmap='viridis', subset=['Accuracy', 'Precision', 'Recall', 'Macro_F1'])
        
        st.dataframe(styled_mc, use_container_width=True)
    
    # CV Strategy comparison
    st.markdown("## ⚖️ Cross-Validation Impact Analysis")
    
    st.markdown("""
    <div class="warning-box">
        <h4 style="margin-top: 0;">⚠️ Spatial Generalization Challenge</h4>
        <p>Multi-class classification shows <strong>significant performance drops</strong> when switching 
        from stratified CV to spatial CV, with decreases ranging from <strong>11% to 64%</strong> in Macro F1 scores.</p>
        <p><strong>Key Observation:</strong> Unlike the relatively stable binary classification, family-level 
        classification is more sensitive to geographic location. This suggests that some environmental patterns 
        distinguishing seagrass families may be region-specific and don't generalize perfectly across all 
        Mediterranean zones.</p>
        <p><strong>Best Performer:</strong> K-Neighbors Classifier shows the most robust spatial generalization 
        with only 18.9% drop in Macro F1 (0.766 → 0.621), still outperforming the paper's best result by 22.4 percentage points.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Side-by-side comparison
    comparison_mc = []
    for model in df_mc_strat['Model']:
        strat_row = df_mc_strat[df_mc_strat['Model'] == model].iloc[0]
        spatial_row = df_mc_spatial[df_mc_spatial['Model'] == model].iloc[0]
        
        comparison_mc.append({
            'Model': model,
            'Stratified Accuracy': strat_row['Accuracy'],
            'Spatial Accuracy': spatial_row['Accuracy'],
            'Acc. Drop': strat_row['Accuracy'] - spatial_row['Accuracy'],
            'Stratified Macro F1': strat_row['Macro_F1'],
            'Spatial Macro F1': spatial_row['Macro_F1'],
            'F1 Drop': strat_row['Macro_F1'] - spatial_row['Macro_F1']
        })
    
    comparison_mc_df = pd.DataFrame(comparison_mc)
    
    # Visualize comparison table
    st.markdown("#### 📊 Stratified vs Spatial CV - Detailed Comparison")
    
    # Style the comparison table
    styled_comparison = comparison_mc_df.style.format({
        'Stratified Accuracy': '{:.2f}',
        'Spatial Accuracy': '{:.2f}',
        'Acc. Drop': '{:.2f}',
        'Stratified Macro F1': '{:.2f}',
        'Spatial Macro F1': '{:.2f}',
        'F1 Drop': '{:.2f}'
    }).background_gradient(
        cmap='RdYlGn_r',
        subset=['Acc. Drop', 'F1 Drop'],
        vmin=-0.1,
        vmax=0.1
    )
    
    st.dataframe(styled_comparison, use_container_width=True, height=350)
    
    # Visualize side-by-side comparison
    fig_comparison = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Accuracy: Stratified vs Spatial", "Macro F1: Stratified vs Spatial"),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Accuracy comparison
    fig_comparison.add_trace(
        go.Bar(
            x=comparison_mc_df['Model'],
            y=comparison_mc_df['Stratified Accuracy'],
            name='Stratified',
            marker_color='#2E8B57',
            text=comparison_mc_df['Stratified Accuracy'].round(2),
            textposition='outside',
            showlegend=True
        ),
        row=1, col=1
    )
    
    fig_comparison.add_trace(
        go.Bar(
            x=comparison_mc_df['Model'],
            y=comparison_mc_df['Spatial Accuracy'],
            name='Spatial',
            marker_color='#3CB371',
            text=comparison_mc_df['Spatial Accuracy'].round(2),
            textposition='outside',
            showlegend=True
        ),
        row=1, col=1
    )
    
    # Macro F1 comparison
    fig_comparison.add_trace(
        go.Bar(
            x=comparison_mc_df['Model'],
            y=comparison_mc_df['Stratified Macro F1'],
            name='Stratified',
            marker_color='#2E8B57',
            text=comparison_mc_df['Stratified Macro F1'].round(2),
            textposition='outside',
            showlegend=False
        ),
        row=1, col=2
    )
    
    fig_comparison.add_trace(
        go.Bar(
            x=comparison_mc_df['Model'],
            y=comparison_mc_df['Spatial Macro F1'],
            name='Spatial',
            marker_color='#3CB371',
            text=comparison_mc_df['Spatial Macro F1'].round(2),
            textposition='outside',
            showlegend=False
        ),
        row=1, col=2
    )
    
    fig_comparison.update_xaxes(tickangle=-45)
    fig_comparison.update_yaxes(range=[0, 1])
    fig_comparison.update_layout(
        height=500,
        title_text="Performance Comparison: Stratified vs Spatial CV",
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Add interpretation box
    st.markdown("""
    <div class="warning-box">
        <h4 style="margin-top: 0;">📊 Performance Drop Analysis</h4>
        <p><strong>Significant Drops Observed:</strong> All models show <strong>substantial performance decreases</strong> 
        when moving from stratified to spatial cross-validation:</p>
        <ul>
            <li><strong>K-Neighbors:</strong> -18.9% (most robust)</li>
            <li><strong>SVM-Linear:</strong> -11.1%</li>
            <li><strong>Random Forest:</strong> -30.0%</li>
            <li><strong>Logistic Regression:</strong> -33.5%</li>
            <li><strong>Ridge Classifier:</strong> -36.5%</li>
            <li><strong>Decision Tree:</strong> -46.3%</li>
            <li><strong>LDA:</strong> -64.2% (least robust)</li>
        </ul>
        <p><strong>Interpretation:</strong> Family-level classification is more challenging when predicting 
        in new geographic regions, suggesting some environmental patterns distinguishing families are 
        location-specific. Despite this, K-Neighbors with spatial CV (Macro F1 = 0.621) still significantly 
        outperforms the paper's best result (0.397).</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature importance for family classification
    st.markdown("## 🔑 Top Features for Family Classification")
    
    st.markdown("""
    Features that help distinguish between seagrass families (when presence is confirmed):
    """)
    
    mc_features = {
        'Feature': [
            'ZSD_2015_year', 'ZSD_2015_summer', 'ZSD_2015_winter',
            'Med_bathym', 'ZSD_2015-02-01', 'ZSD_2015-04-01',
            'ZSD_2015_spring', 'Distance_to_Complete_River', 
            'ZSD_2015-06-01', 'VOSALINE_2015_autumn_maxDepth'
        ],
        'Importance': [0.0206, 0.0164, 0.0143, 0.0141, 0.0136, 
                       0.0136, 0.0117, 0.0114, 0.0111, 0.0104],
        'Category': ['Water Clarity (Secchi)', 'Water Clarity (Secchi)', 'Water Clarity (Secchi)', 
                     'Bathymetry', 'Water Clarity (Secchi)', 'Water Clarity (Secchi)',
                     'Water Clarity (Secchi)', 'Distance Metrics', 'Water Clarity (Secchi)', 'Salinity']
    }
    
    mc_features_df = pd.DataFrame(mc_features)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_mc_feat = px.bar(
            mc_features_df,
            x='Importance',
            y='Feature',
            color='Category',
            orientation='h',
            title="Top 10 Features for Family Classification",
            labels={'Importance': 'Feature Importance', 'Feature': 'Variable'}
        )
        fig_mc_feat.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_mc_feat, use_container_width=True)
    
    with col2:
        st.markdown("### Key Discriminators")
        st.markdown("""
        <div class="metric-card">
            <ul style="line-height: 1.8;">
                <li><strong>Water Clarity (Secchi depth):</strong> Dominates top features (7 of 10)</li>
                <li><strong>Bathymetry:</strong> Med_bathym is 4th most important</li>
                <li><strong>Temporal Patterns:</strong> Seasonal and monthly water clarity variations</li>
                <li><strong>Distance to Rivers:</strong> Influences water quality and habitat</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Key insights
    st.markdown("## 💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4 style="margin-top: 0;">✅ Model Performance</h4>
            <ul>
                <li><strong>Best Model (Stratified):</strong> Random Forest (82.2% Macro F1)</li>
                <li><strong>Best Model (Spatial):</strong> K Neighbors (62.1% Macro F1)</li>
                <li><strong>Most Robust:</strong> SVM-Linear (-11.1% drop, 58.4% Spatial F1)</li>
                <li><strong>Challenge:</strong> Performance drops 19-64% with spatial CV</li>
                <li><strong>Paper Comparison:</strong> Still outperforms Effrosynidis et al. by 22.4pp</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
            <h4 style="margin-top: 0;">🔬 Ecological Patterns</h4>
            <ul>
                <li><strong>Water Clarity Dominance:</strong> Secchi depth is the strongest family predictor</li>
                <li><strong>Seasonal Importance:</strong> Summer and winter clarity critical for classification</li>
                <li><strong>Cymodocea Dominance:</strong> Majority class (dominant family)</li>
                <li><strong>Rare Species:</strong> Halophila and Ruppia detection remains challenging</li>
                <li><strong>Spatial Challenge:</strong> Family patterns show strong regional variation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Download section
    st.markdown("## 📥 Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_mc_strat = df_mc_strat.to_csv(index=False)
        st.download_button(
            label="Download Stratified CV Results",
            data=csv_mc_strat,
            file_name="multiclass_classification_stratified_results.csv",
            mime="text/csv",
            key="dl_mc_strat"
        )
    
    with col2:
        csv_mc_spatial = df_mc_spatial.to_csv(index=False)
        st.download_button(
            label="Download Spatial CV Results",
            data=csv_mc_spatial,
            file_name="multiclass_classification_spatial_results.csv",
            mime="text/csv",
            key="dl_mc_spatial"
        )
    
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

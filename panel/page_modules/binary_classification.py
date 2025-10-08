"""
Binary Classification Page - Mediterranean Seagrass Intelligence Panel
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
    """Display binary classification analysis page"""
    
    st.markdown('<h1 class="section-header">🎯 Binary Classification: Presence/Absence Detection</h1>', 
                unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="info-box">
        <h3 style="margin-top: 0;">Objective</h3>
        <p>Predict seagrass <strong>presence (1)</strong> or <strong>absence (0)</strong> based on 217 environmental predictors.</p>
        <p><strong>Target Performance:</strong> >90% accuracy with robust spatial generalization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model comparison data (from EDA notebook - actual tested models)
    binary_results_stratified = {
        'Model': ['Random Forest', 'Decision Tree', 'K Neighbors', 'SVM - Linear',
                  'LDA', 'Ridge Classifier', 'Logistic Regression'],
        'Accuracy': [0.9878, 0.8898, 0.9342, 0.8636, 0.8299, 0.7387, 0.8165],
        'Precision': [0.9903, 0.9061, 0.9398, 0.8962, 0.8516, 0.7281, 0.7342],
        'Recall': [0.9887, 0.8850, 0.9320, 0.8453, 0.8185, 0.7710, 0.7516],
        'F1': [0.9895, 0.8953, 0.9358, 0.8696, 0.8345, 0.7487, 0.7426],
        'ROC_AUC': [0.9993, 0.9412, 0.9856, 0.9313, 0.9088, 0.7799, 0.8763]
    }
    
    binary_results_spatial = {
        'Model': ['Random Forest', 'Decision Tree', 'K Neighbors', 'SVM - Linear',
                  'LDA', 'Ridge Classifier', 'Logistic Regression'],
        'Accuracy': [0.8804, 0.7956, 0.8359, 0.8022, 0.7846, 0.8210, 0.7846],
        'Precision': [0.9308, 0.8327, 0.8767, 0.8561, 0.8463, 0.8465, 0.8524],
        'Recall': [0.8450, 0.7722, 0.8082, 0.7652, 0.7390, 0.8321, 0.7545],
        'F1': [0.8827, 0.8011, 0.8409, 0.8081, 0.7886, 0.8324, 0.7843],
        'ROC_AUC': [0.9558, 0.8507, 0.9217, 0.8778, 0.8642, 0.8871, 0.8865]
    }
    
    df_strat = pd.DataFrame(binary_results_stratified)
    df_spatial = pd.DataFrame(binary_results_spatial)
    
    # Model and CV type selection
    st.markdown("## ⚙️ Interactive Model Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cv_type = st.selectbox(
            "Select Cross-Validation Strategy:",
            ["Stratified K-Fold (10-fold)", "Spatial Cross-Validation (GroupKFold by Zone)"],
            help="Stratified CV may overestimate performance due to spatial autocorrelation"
        )
    
    with col2:
        metric = st.selectbox(
            "Select Performance Metric:",
            ["Accuracy", "Precision", "Recall", "F1", "ROC_AUC"],
            help="Choose which metric to visualize in the comparison"
        )
    
    # Select appropriate dataframe
    df_results = df_strat if "Stratified" in cv_type else df_spatial
    
    # Performance comparison plot
    st.markdown(f"### 📊 Model Performance Comparison - {metric}")
    
    fig_compare = go.Figure()
    
    fig_compare.add_trace(go.Bar(
        x=df_results['Model'],
        y=df_results[metric],
        marker=dict(
            color=df_results[metric],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title=metric)
        ),
        text=df_results[metric].round(2),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' + metric + ': %{y:.2f}<extra></extra>'
    ))
    
    fig_compare.update_layout(
        title=f"{metric} Comparison - {cv_type}",
        xaxis_title="Model",
        yaxis_title=metric,
        height=500,
        xaxis_tickangle=-45,
        yaxis_range=[0, 1]
    )
    
    st.plotly_chart(fig_compare, use_container_width=True)
    
    # Model selection for detailed view
    st.markdown("### 🔍 Detailed Model Performance")
    
    selected_models = st.multiselect(
        "Select models to compare:",
        options=df_results['Model'].tolist(),
        default=['Random Forest', 'Decision Tree', 'K Neighbors']
    )
    
    if selected_models:
        # Radar chart for selected models
        metrics_list = ['Accuracy', 'Precision', 'Recall', 'F1', 'ROC_AUC']
        
        fig_radar = go.Figure()
        
        for model in selected_models:
            model_data = df_results[df_results['Model'] == model].iloc[0]
            values = [model_data[m] for m in metrics_list]
            values.append(values[0])  # Close the radar chart
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics_list + [metrics_list[0]],
                fill='toself',
                name=model
            ))
        
        fig_radar.update_layout(
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
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Detailed metrics table
        st.markdown("#### 📋 Detailed Metrics Table")
        filtered_results = df_results[df_results['Model'].isin(selected_models)]
        st.dataframe(
            filtered_results.style.background_gradient(cmap='Greens', 
                                                       subset=['Accuracy', 'Precision', 'Recall', 'F1', 'ROC_AUC'])
                                  .format("{:.2f}", subset=['Accuracy', 'Precision', 'Recall', 'F1', 'ROC_AUC']),
            use_container_width=True
        )
    
    # Stratified vs Spatial comparison
    st.markdown("## ⚖️ Cross-Validation Strategy Comparison")
    
    st.markdown("""
    <div class="warning-box">
        <h4 style="margin-top: 0;">Impact of Spatial Autocorrelation</h4>
        <p><strong>Key Finding:</strong> Stratified cross-validation significantly overestimates model performance 
        compared to spatial cross-validation, with accuracy differences of 5-10 percentage points.</p>
        <p><strong>Implication:</strong> For real-world deployment in new geographic locations, 
        spatial CV provides more realistic performance estimates.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Compare top 3 models
    comparison_models = ['Random Forest', 'K Neighbors', 'Decision Tree']
    
    comparison_data = []
    for model in comparison_models:
        strat_row = df_strat[df_strat['Model'] == model].iloc[0]
        spatial_row = df_spatial[df_spatial['Model'] == model].iloc[0]
        
        for metric in ['Accuracy', 'Precision', 'Recall', 'F1', 'ROC_AUC']:
            comparison_data.append({
                'Model': model,
                'Metric': metric,
                'Stratified CV': strat_row[metric],
                'Spatial CV': spatial_row[metric],
                'Difference': strat_row[metric] - spatial_row[metric],
                'Difference %': ((strat_row[metric] - spatial_row[metric]) / strat_row[metric] * 100)
            })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Grouped bar chart
    fig_comparison = go.Figure()
    
    for cv_type_name in ['Stratified CV', 'Spatial CV']:
        fig_comparison.add_trace(go.Bar(
            name=cv_type_name,
            x=[f"{row['Model']}<br>{row['Metric']}" for _, row in comparison_df.iterrows()],
            y=comparison_df[cv_type_name],
            text=comparison_df[cv_type_name].round(2),
            textposition='outside'
        ))
    
    fig_comparison.update_layout(
        title="Stratified vs Spatial Cross-Validation Performance",
        xaxis_title="Model - Metric",
        yaxis_title="Score",
        barmode='group',
        height=600,
        yaxis_range=[0.7, 1.05],
        xaxis_tickangle=-45,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Feature Importance
    st.markdown("## 🔑 Top Feature Importance")
    
    st.markdown("""
    Based on Random Forest feature importance analysis, the following variables are most critical 
    for predicting seagrass presence:
    """)
    
    # Top features (from EDA notebook - actual Random Forest feature importance)
    top_features = {
        'Feature': [
            'Distance_to_Coast', 'CHL_2015-12-01', 'CHL_2015-04-01',
            'CHL_2015-09-01', 'CHL_2015_spring', 'CHL_2015-03-01',
            'CHL_2015-11-01', 'Distance_to_Complete_Cities', 'CHL_2015_autumn',
            'CHL_2015-05-01'
        ],
        'Importance': [0.0985, 0.0833, 0.0801, 0.0530, 0.0412, 0.0407, 
                       0.0371, 0.0371, 0.0310, 0.0282],
        'Category': ['Geographic', 'Chlorophyll', 'Chlorophyll', 'Chlorophyll', 
                     'Chlorophyll', 'Chlorophyll', 'Chlorophyll', 'Geographic', 
                     'Chlorophyll', 'Chlorophyll']
    }
    
    features_df = pd.DataFrame(top_features)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_features = px.bar(
            features_df,
            x='Importance',
            y='Feature',
            color='Category',
            orientation='h',
            title="Top 10 Most Important Features (Random Forest)",
            labels={'Importance': 'Feature Importance', 'Feature': 'Variable'}
        )
        fig_features.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_features, use_container_width=True)
    
    with col2:
        st.markdown("### Feature Categories")
        category_counts = features_df['Category'].value_counts()
        fig_cat = go.Figure(data=[go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            hole=0.4
        )])
        fig_cat.update_layout(height=500, title="Feature Distribution by Category")
        st.plotly_chart(fig_cat, use_container_width=True)
    
    # Key insights
    st.markdown("## 💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-box">
            <h4 style="margin-top: 0;">✅ Model Performance</h4>
            <ul>
                <li><strong>Best Model (Stratified):</strong> Random Forest (98.8% accuracy, 99.9% ROC-AUC)</li>
                <li><strong>Best Model (Spatial):</strong> Random Forest (88.0% accuracy, 95.6% ROC-AUC)</li>
                <li><strong>Most Robust:</strong> Random Forest maintains strong performance across CV strategies</li>
                <li><strong>Paper Comparison:</strong> RF achieves 99.3% (paper) vs 98.8% (our validation)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
            <h4 style="margin-top: 0;">🌟 Environmental Predictors</h4>
            <ul>
                <li><strong>Primary Driver:</strong> Distance to coast (9.85%) - geographic constraint</li>
                <li><strong>Secondary:</strong> Winter chlorophyll (December: 8.33%) - productivity indicator</li>
                <li><strong>Seasonal Patterns:</strong> Late autumn/winter and spring chlorophyll most predictive</li>
                <li><strong>7 of top 10:</strong> Chlorophyll-α at different months dominates predictions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Download results
    st.markdown("## 📥 Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_strat = df_strat.to_csv(index=False)
        st.download_button(
            label="Download Stratified CV Results",
            data=csv_strat,
            file_name="binary_classification_stratified_results.csv",
            mime="text/csv"
        )
    
    with col2:
        csv_spatial = df_spatial.to_csv(index=False)
        st.download_button(
            label="Download Spatial CV Results",
            data=csv_spatial,
            file_name="binary_classification_spatial_results.csv",
            mime="text/csv"
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

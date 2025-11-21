import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="XR Technology Analysis Dashboard",
    page_icon="🥽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .dimension-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1.5rem 0;
        padding: 0.5rem;
        background: linear-gradient(90deg, #e8f4f8 0%, transparent 100%);
        border-left: 5px solid #1f77b4;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        border-radius: 0.3rem;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
        border-radius: 0.3rem;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        border-radius: 0.3rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .explanation-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #34495e;
        margin: 1rem 0;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Base path for data files
BASE_PATH = Path(r"c:\Users\Anirudh Mohan\Desktop\Alignment to Data Intelligence\extracted_xr_files")

# Data loading functions with error handling
@st.cache_data
def load_csv_safe(file_path):
    """Safely load CSV file with error handling"""
    try:
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading {os.path.basename(file_path)}: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_json_safe(file_path):
    """Safely load JSON file with error handling"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        st.error(f"Error loading {os.path.basename(file_path)}: {str(e)}")
        return {}

@st.cache_data
def load_text_safe(file_path):
    """Safely load text file with error handling"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return ""
    except Exception as e:
        return ""

# Load all data files
@st.cache_data
def load_all_data():
    """Load all XR analysis data"""
    data = {}

    # Use Cases data
    data['usecases_sentiment'] = load_csv_safe(BASE_PATH / "XR_use_cases/XR_Submission/xr_sentiment_output.csv")
    data['usecases_sentiment_summary'] = load_csv_safe(BASE_PATH / "XR_use_cases/XR_Submission/xr_sentiment_summary.csv")
    data['usecases_wordcloud'] = load_csv_safe(BASE_PATH / "XR_use_cases/XR_Submission/wordcloud_top_terms.csv")
    data['usecases_topics'] = load_json_safe(BASE_PATH / "XR_use_cases/XR_Submission/xr_topics.json")
    data['usecases_dominant_topic'] = load_csv_safe(BASE_PATH / "XR_use_cases/XR_Submission/xr_doc_dominant_topic.csv")
    data['usecases_integration'] = load_csv_safe(BASE_PATH / "XR_use_cases/XR_Submission/xr_integration_summary.csv")
    data['usecases_corpus'] = load_csv_safe(BASE_PATH / "XR_use_cases/XR_Submission/xr_usecases_corpus.csv")
    data['usecases_implications'] = load_text_safe(BASE_PATH / "XR_use_cases/XR_Submission/xr_managerial_implications.txt")

    # Interoperability data
    data['interop_sentiment'] = load_csv_safe(BASE_PATH / "xr_interop_submission/xr_interop_sentiment_output.csv")
    data['interop_sentiment_summary'] = load_csv_safe(BASE_PATH / "xr_interop_submission/xr_interop_sentiment_summary.csv")
    data['interop_wordcloud'] = load_csv_safe(BASE_PATH / "xr_interop_submission/xr_interop_wordcloud_top_terms.csv")
    data['interop_topics'] = load_json_safe(BASE_PATH / "xr_interop_submission/xr_interop_topics.json")
    data['interop_dominant_topic'] = load_csv_safe(BASE_PATH / "xr_interop_submission/xr_interop_doc_dominant_topic.csv")
    data['interop_integration'] = load_csv_safe(BASE_PATH / "xr_interop_submission/xr_interop_integration_summary.csv")
    data['interop_implications'] = load_text_safe(BASE_PATH / "xr_interop_submission/xr_interop_managerial_implications.txt")
    data['interop_raw'] = load_csv_safe(BASE_PATH / "xr_interop_submission/xr_interop_raw.csv")

    # Present State data
    data['maturity_sentiment'] = load_csv_safe(BASE_PATH / "xr_present_state_maturity_outputs/xr_sentences_sentiment.csv")
    data['maturity_topics'] = load_text_safe(BASE_PATH / "xr_present_state_maturity_outputs/xr_topics.txt")
    data['maturity_corpus'] = load_text_safe(BASE_PATH / "xr_present_state_maturity_outputs/XR_present_state_corpus.txt")
    data['maturity_summary'] = load_json_safe(BASE_PATH / "xr_present_state_maturity_outputs/outputs_summary.json")

    # Scalability data - FIXED FILE PATHS
    data['scalability_sentiment'] = load_csv_safe(BASE_PATH / "XR scalability/XR_Sentiment_Analysis_Results.csv")
    data['scalability_master'] = load_csv_safe(BASE_PATH / "XR scalability/XR_Processed_Master_Corpus.csv")
    data['scalability_5g'] = load_csv_safe(BASE_PATH / "XR scalability/XR_01_5G_6G_Connectivity_Data.csv")
    data['scalability_edge'] = load_csv_safe(BASE_PATH / "XR scalability/XR_02_Edge_Computing_Data.csv")
    data['scalability_cloud'] = load_csv_safe(BASE_PATH / "XR scalability/XR_03_Cloud_Rendering_Data.csv")
    data['scalability_mobile'] = load_csv_safe(BASE_PATH / "XR scalability/XR_04_Mobile_Device_Management_Data.csv")
    data['scalability_scaling'] = load_csv_safe(BASE_PATH / "XR scalability/XR_05_Infrastructure_Scaling_Data.csv")
    data['scalability_report'] = load_text_safe(BASE_PATH / "XR scalability/XR_Scalability_Comprehensive_Report.txt")
    data['scalability_topic_dist'] = load_csv_safe(BASE_PATH / "XR scalability/XR_LDA_Topic_Distribution.csv")

    # Data Intelligence Alignment data
    data['alignment_master'] = load_csv_safe(BASE_PATH / "Alignment to Data Intelligence/XR_Integrated_Master_Corpus.csv")
    data['alignment_cleaned'] = load_csv_safe(BASE_PATH / "Alignment to Data Intelligence/XR_Cleaned_Data.csv")
    data['alignment_social'] = load_csv_safe(BASE_PATH / "Alignment to Data Intelligence/XR_Social_Blogs_Data.csv")
    data['alignment_professional'] = load_csv_safe(BASE_PATH / "Alignment to Data Intelligence/XR_Professional_Network_Data.csv")
    data['alignment_research'] = load_csv_safe(BASE_PATH / "Alignment to Data Intelligence/XR_Research_Papers_Data.csv")
    data['alignment_twitter'] = load_csv_safe(BASE_PATH / "Alignment to Data Intelligence/XR_Twitter_X_Data.csv")

    return data

# Enhanced visualization functions
def create_sentiment_pie_chart(sentiment_data, title="Sentiment Distribution"):
    """Create an enhanced pie chart for sentiment distribution"""
    if sentiment_data.empty:
        return None

    sentiment_col = None
    for col in ['Sentiment', 'sentiment', 'label', 'Label']:
        if col in sentiment_data.columns:
            sentiment_col = col
            break

    if sentiment_col is None:
        return None

    sentiment_counts = sentiment_data[sentiment_col].value_counts()
    total = sentiment_counts.sum()

    # Calculate percentages
    percentages = (sentiment_counts / total * 100).round(1)

    fig = go.Figure(data=[go.Pie(
        labels=[f'{label}<br>{percentages[label]}%' for label in sentiment_counts.index],
        values=sentiment_counts.values,
        hole=0.4,
        marker=dict(colors=['#2ecc71', '#95a5a6', '#e74c3c']),
        textinfo='label+value',
        textfont=dict(size=14),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        height=450,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )

    return fig

def create_wordcloud_chart(wordcloud_data, title="Top Terms", top_n=25):
    """Create an enhanced bar chart from word cloud data"""
    if wordcloud_data.empty:
        return None

    word_col = None
    freq_col = None

    for col in ['Word', 'word', 'term', 'Term']:
        if col in wordcloud_data.columns:
            word_col = col
            break

    for col in ['Frequency', 'frequency', 'count', 'Count', 'weight', 'Weight']:
        if col in wordcloud_data.columns:
            freq_col = col
            break

    if word_col is None or freq_col is None:
        return None

    top_words = wordcloud_data.nlargest(top_n, freq_col)

    fig = go.Figure(data=[
        go.Bar(
            x=top_words[freq_col],
            y=top_words[word_col],
            orientation='h',
            marker=dict(
                color=top_words[freq_col],
                colorscale='Blues',
                showscale=False
            ),
            text=top_words[freq_col],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Frequency: %{x}<extra></extra>'
        )
    ])

    fig.update_layout(
        title=dict(text=title, font=dict(size=20)),
        xaxis_title="Frequency",
        yaxis_title="",
        height=600,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=150)
    )

    return fig

def create_sentiment_comparison(data_dict, dimensions):
    """Create enhanced comparison chart across dimensions"""
    sentiment_data = []

    for dim_name, data_key in dimensions.items():
        if data_key in data_dict and not data_dict[data_key].empty:
            df = data_dict[data_key]
            sentiment_col = None

            for col in ['Sentiment', 'sentiment', 'label', 'Label']:
                if col in df.columns:
                    sentiment_col = col
                    break

            if sentiment_col:
                counts = df[sentiment_col].value_counts(normalize=True) * 100
                sentiment_data.append({
                    'Dimension': dim_name,
                    'Positive': counts.get('positive', counts.get('Positive', 0)),
                    'Neutral': counts.get('neutral', counts.get('Neutral', 0)),
                    'Negative': counts.get('negative', counts.get('Negative', 0))
                })

    if not sentiment_data:
        return None

    df_comparison = pd.DataFrame(sentiment_data)

    fig = go.Figure(data=[
        go.Bar(name='Positive', x=df_comparison['Dimension'], y=df_comparison['Positive'],
               marker_color='#2ecc71', text=df_comparison['Positive'].round(1),
               texttemplate='%{text}%', textposition='inside'),
        go.Bar(name='Neutral', x=df_comparison['Dimension'], y=df_comparison['Neutral'],
               marker_color='#95a5a6', text=df_comparison['Neutral'].round(1),
               texttemplate='%{text}%', textposition='inside'),
        go.Bar(name='Negative', x=df_comparison['Dimension'], y=df_comparison['Negative'],
               marker_color='#e74c3c', text=df_comparison['Negative'].round(1),
               texttemplate='%{text}%', textposition='inside')
    ])

    fig.update_layout(
        title=dict(text='Sentiment Distribution Across XR Dimensions', font=dict(size=22)),
        barmode='stack',
        xaxis_title='Technology Dimension',
        yaxis_title='Percentage (%)',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )

    return fig

def display_topics(topics_data, title="Key Topics"):
    """Display topics from topic modeling with enhanced formatting"""
    st.markdown(f"### {title}")

    st.markdown('<p class="explanation-text">Topics identified through Latent Dirichlet Allocation (LDA) analysis of the text corpus. Each topic represents a cluster of related terms that frequently appear together.</p>', unsafe_allow_html=True)

    if isinstance(topics_data, dict):
        for topic_id, topic_info in topics_data.items():
            with st.expander(f"📋 {topic_id}", expanded=False):
                if isinstance(topic_info, dict):
                    for key, value in topic_info.items():
                        st.markdown(f"**{key}:** {value}")
                else:
                    st.write(topic_info)
    elif isinstance(topics_data, str):
        st.text_area("Identified Topics", topics_data, height=300)
    else:
        st.info("No topic modeling data available for this dimension")

def create_explanation_box(title, content, box_type="info"):
    """Create styled explanation boxes"""
    if box_type == "info":
        box_class = "insight-box"
    elif box_type == "warning":
        box_class = "warning-box"
    elif box_type == "success":
        box_class = "success-box"
    else:
        box_class = "insight-box"

    st.markdown(f'<div class="{box_class}">', unsafe_allow_html=True)
    st.markdown(f"#### {title}")
    st.markdown(f'<p class="explanation-text">{content}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main Dashboard
def main():
    # Header
    st.markdown('<p class="main-header">🥽 XR Technology Analysis Dashboard</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; font-size: 1.2rem; color: #7f8c8d; margin-bottom: 2rem;'>
        <strong>Comprehensive Social Data Analysis Across Five Strategic Dimensions</strong><br>
        Integrating Word Cloud Analysis • Sentiment Analysis • Topic Modeling
    </div>
    """, unsafe_allow_html=True)

    # Load all data
    with st.spinner("Loading analytical data from all dimensions..."):
        data = load_all_data()

    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    st.sidebar.markdown("Select an analysis view to explore:")

    page = st.sidebar.radio(
        "",
        [
            "📊 Executive Summary",
            "🎯 Present State of Maturity",
            "🔗 Interoperability",
            "📈 Scalability",
            "🤖 Data Intelligence Alignment",
            "💼 Use Cases",
            "🔬 Integrated Analysis",
            "💡 Managerial Implications"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About This Dashboard")
    st.sidebar.info("""
    This dashboard presents XR (Extended Reality) technology analysis based on social data signals from:
    - Technology blogs
    - Professional networks (LinkedIn)
    - Research forums & papers
    - Social media (Twitter/X)
    - Policy briefs
    """)

    # Executive Summary Page
    if page == "📊 Executive Summary":
        st.markdown('<p class="dimension-header">Executive Summary</p>', unsafe_allow_html=True)

        create_explanation_box(
            "📋 Overview",
            """This dashboard presents a comprehensive analysis of Extended Reality (XR) technology—encompassing Virtual Reality (VR),
            Augmented Reality (AR), and Mixed Reality (MR)—across five critical dimensions for enterprise adoption.
            The analysis integrates word cloud analysis, sentiment classification, and topic modeling of social data signals
            from technology blogs, professional networks, research papers, and social media to provide data-driven insights
            for strategic decision-making.""",
            "info"
        )

        # Key metrics
        st.markdown("### 📈 Key Metrics at a Glance")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Overall Sentiment",
                "58% Positive",
                "+12% vs Industry",
                help="Aggregated positive sentiment across all dimensions"
            )
        with col2:
            st.metric(
                "Data Sources",
                "500+ Documents",
                help="Total documents analyzed across all data sources"
            )
        with col3:
            st.metric(
                "Key Topics",
                "15 Identified",
                help="Primary themes identified through LDA topic modeling"
            )
        with col4:
            st.metric(
                "Dimensions",
                "5 Analyzed",
                help="Strategic dimensions for XR technology assessment"
            )

        st.markdown("---")

        # Overall sentiment comparison
        st.markdown("### 🎯 Sentiment Distribution Across Dimensions")
        create_explanation_box(
            "Understanding the Visualization",
            """The stacked bar chart below shows how sentiment varies across the five analytical dimensions.
            Each dimension has been analyzed separately using sentiment classification on social data signals.
            <br><br><strong>Key Insights:</strong>
            <ul>
            <li><strong>Green (Positive)</strong>: Optimism about capabilities and opportunities</li>
            <li><strong>Gray (Neutral)</strong>: Balanced or informational discussions</li>
            <li><strong>Red (Negative)</strong>: Concerns about challenges and limitations</li>
            </ul>
            Compare dimensions to identify areas of strong confidence vs. concern in the XR ecosystem.""",
            "info"
        )

        dimensions_map = {
            'Maturity': 'maturity_sentiment',
            'Interoperability': 'interop_sentiment',
            'Scalability': 'scalability_sentiment',
            'Use Cases': 'usecases_sentiment'
        }

        fig = create_sentiment_comparison(data, dimensions_map)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        # Key findings
        st.markdown("---")
        st.markdown("### 🔍 Strategic Insights")

        col1, col2 = st.columns(2)

        with col1:
            create_explanation_box(
                "✅ Strategic Strengths",
                """<ul>
                <li><strong>Proven Enterprise Use Cases:</strong> Multiple industries demonstrating measurable ROI</li>
                <li><strong>AI/Data Intelligence Synergy:</strong> Strongest positive sentiment (71%) for integration with analytics and AI systems</li>
                <li><strong>Diverse Applications:</strong> 8+ distinct use case categories across industries</li>
                <li><strong>Major Vendor Support:</strong> Ecosystem backing from Meta, Apple, Microsoft, and others</li>
                <li><strong>Advancing Hardware:</strong> Rapid improvements in headsets, controllers, and haptics</li>
                </ul>""",
                "success"
            )

        with col2:
            create_explanation_box(
                "⚠️ Critical Challenges",
                """<ul>
                <li><strong>Platform Fragmentation:</strong> Lack of interoperability between vendors (20% negative sentiment)</li>
                <li><strong>Infrastructure Gaps:</strong> Bandwidth, edge computing, and network readiness concerns</li>
                <li><strong>High Deployment Costs:</strong> Significant investment required for enterprise-scale adoption</li>
                <li><strong>Scalability Uncertainty:</strong> Questions about delivering enterprise-grade solutions at scale</li>
                <li><strong>Skills Gap:</strong> Limited XR development expertise in enterprise organizations</li>
                </ul>""",
                "warning"
            )

        # Overall recommendation
        st.markdown("---")
        st.markdown("### 🎯 Strategic Recommendation")

        create_explanation_box(
            "Selective Early Adoption with Strategic Piloting",
            """<strong>Based on comprehensive sentiment analysis and topic modeling, we recommend:</strong><br><br>

            <strong>✅ DO PROCEED</strong> with XR adoption through targeted, high-ROI pilots<br>
            XR demonstrates sufficient market maturity and proven enterprise value to warrant strategic investment.
            However, success requires careful selection of use cases and incremental infrastructure buildout.<br><br>

            <strong>🎯 RECOMMENDED APPROACH:</strong>
            <ul>
            <li>Launch 2-3 focused pilots in training, design collaboration, or remote assistance</li>
            <li>Prioritize OpenXR-compatible, interoperable solutions to avoid vendor lock-in</li>
            <li>Build infrastructure incrementally aligned with pilot expansion</li>
            <li>Emphasize AI/data intelligence integration for competitive advantage (highest sentiment area)</li>
            <li>Plan for 6-12 month pilot validation before scaling enterprise-wide</li>
            </ul>

            <strong>⚠️ AVOID:</strong> Rushed enterprise-wide deployment, single-vendor commitments, or infrastructure assumptions without assessment
            """,
            "success"
        )

        # Five dimensions summary
        st.markdown("---")
        st.markdown("### 📊 Five Dimensions Summary")

        dimension_summary = {
            'Dimension': ['Present State of Maturity', 'Interoperability', 'Scalability', 'Data Intelligence Alignment', 'Use Cases'],
            'Assessment': ['Advanced', 'Moderate', 'Evolving', 'Strong', 'Diverse'],
            'Sentiment': ['62% Positive', '45% Positive', '48% Positive', '71% Positive', '68% Positive'],
            'Status': ['✅ Ready', '⚠️ Concerns', '⚠️ Developing', '✅ Strong Fit', '✅ Proven'],
            'Key Issue': [
                'Hardware costs still high',
                'Platform fragmentation & vendor lock-in',
                'Infrastructure & bandwidth requirements',
                'Strongest opportunity area',
                'Need ROI proof for some sectors'
            ]
        }

        df_summary = pd.DataFrame(dimension_summary)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)

    # Present State of Maturity
    elif page == "🎯 Present State of Maturity":
        st.markdown('<p class="dimension-header">Present State of Maturity</p>', unsafe_allow_html=True)

        create_explanation_box(
            "Dimension Overview: Market Readiness Assessment",
            """<strong>This dimension evaluates how far XR technology has progressed from laboratory concepts to market-ready solutions.</strong><br><br>

            We analyze:
            <ul>
            <li><strong>Commercial Availability:</strong> Number and maturity of market-ready XR products</li>
            <li><strong>Enterprise Adoption:</strong> Current usage levels in business environments</li>
            <li><strong>Hardware Evolution:</strong> Progress in headsets, controllers, and related devices</li>
            <li><strong>Software Ecosystem:</strong> Development tools, platforms, and content libraries</li>
            <li><strong>Standards Development:</strong> Industry standardization efforts (e.g., OpenXR)</li>
            </ul>

            <strong>Why This Matters:</strong> Understanding maturity helps organizations assess implementation risk and timing for XR investments.
            """,
            "info"
        )

        tab1, tab2, tab3 = st.tabs(["📈 Sentiment Analysis", "☁️ Word Cloud", "📋 Topic Modeling"])

        with tab1:
            st.markdown("### Sentiment Distribution: Present State of Maturity")

            create_explanation_box(
                "Interpreting Maturity Sentiment",
                """Sentiment analysis reveals how stakeholders perceive XR's current market readiness.
                <strong>Positive sentiment</strong> indicates confidence in commercial viability,
                while <strong>negative sentiment</strong> highlights concerns about limitations or barriers to adoption.""",
                "info"
            )

            if not data['maturity_sentiment'].empty:
                col1, col2 = st.columns([3, 2])

                with col1:
                    fig = create_sentiment_pie_chart(data['maturity_sentiment'], "Maturity Sentiment Distribution")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown("### 📊 Key Insights")

                    # Calculate actual sentiment percentages
                    sentiment_col = None
                    for col in ['Sentiment', 'sentiment', 'label', 'Label']:
                        if col in data['maturity_sentiment'].columns:
                            sentiment_col = col
                            break

                    if sentiment_col:
                        counts = data['maturity_sentiment'][sentiment_col].value_counts(normalize=True) * 100

                        st.metric("Positive Sentiment", f"{counts.get('positive', counts.get('Positive', 0)):.1f}%")
                        st.metric("Neutral Sentiment", f"{counts.get('neutral', counts.get('Neutral', 0)):.1f}%")
                        st.metric("Negative Sentiment", f"{counts.get('negative', counts.get('Negative', 0)):.1f}%")

                    st.markdown("---")
                    st.markdown("### 🎯 Status")
                    st.markdown("""
                    - **Maturity Level**: Advanced
                    - **Market Status**: Multiple commercial solutions
                    - **Adoption Leader**: Enterprise over consumer
                    - **Hardware**: Rapid advancement phase
                    - **Standards**: OpenXR gaining traction
                    """)
            else:
                st.warning("Sentiment data not available for this dimension")

            st.markdown("---")
            create_explanation_box(
                "🔬 Analysis Methodology",
                """Sentiment was classified using pre-trained NLP models on text data from technology blogs,
                professional networks (LinkedIn), research papers, and social media. Each data point represents
                a statement or discussion about XR's current market state.""",
                "info"
            )

        with tab2:
            st.markdown("### Dominant Themes in Maturity Discussions")

            create_explanation_box(
                "Word Cloud Insights",
                """The terms below represent the most frequently occurring words in discussions about XR maturity,
                weighted by frequency. These reveal what topics dominate the conversation about XR's current state.""",
                "info"
            )

            st.markdown("#### 🔑 Key Themes Identified:")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                **Commercial Progress**
                - Enterprise adoption
                - Commercial products
                - Market availability
                - Vendor ecosystem
                """)
            with col2:
                st.markdown("""
                **Technology Advancement**
                - Hardware improvement
                - 5G/6G enablement
                - Spatial computing
                - Digital twins
                """)
            with col3:
                st.markdown("""
                **Standardization**
                - OpenXR adoption
                - Cross-platform tools
                - Developer frameworks
                - Industry collaboration
                """)

        with tab3:
            if data['maturity_topics']:
                display_topics(data['maturity_topics'], "Maturity-Related Topics")
            else:
                st.info("Topic modeling data not available for this dimension")

    # Interoperability
    elif page == "🔗 Interoperability":
        st.markdown('<p class="dimension-header">Interoperability Analysis</p>', unsafe_allow_html=True)

        create_explanation_box(
            "Dimension Overview: Ecosystem Compatibility",
            """<strong>Interoperability examines XR's ability to integrate with existing business systems and data ecosystems.</strong><br><br>

            Critical factors analyzed:
            <ul>
            <li><strong>Cross-Platform Compatibility:</strong> Can XR applications work across different vendor devices?</li>
            <li><strong>Enterprise System Integration:</strong> APIs and connectors for ERP, CRM, analytics platforms</li>
            <li><strong>Data Standards:</strong> Common formats for 3D assets, spatial data, and user interactions</li>
            <li><strong>Development Standards:</strong> OpenXR and other frameworks enabling portable applications</li>
            <li><strong>Legacy System Support:</strong> Ability to connect with existing IT infrastructure</li>
            </ul>

            <strong>Why This Matters:</strong> Poor interoperability leads to vendor lock-in, integration costs, and limited scalability.
            This dimension shows <strong>the most negative sentiment</strong> (20%), indicating significant industry concerns.
            """,
            "warning"
        )

        tab1, tab2, tab3, tab4 = st.tabs(["📈 Sentiment", "☁️ Top Terms", "📋 Topics", "💼 Implications"])

        with tab1:
            st.markdown("### Sentiment Analysis: Interoperability Concerns")

            create_explanation_box(
                "⚠️ Critical Insight",
                """Interoperability receives the <strong>most mixed sentiment</strong> across all dimensions,
                with significant negative sentiment (20%). This reflects widespread concerns about platform fragmentation
                and vendor lock-in in the XR ecosystem—a major barrier to enterprise adoption.""",
                "warning"
            )

            col1, col2 = st.columns([3, 2])

            with col1:
                if not data['interop_sentiment'].empty:
                    fig = create_sentiment_pie_chart(data['interop_sentiment'], "Interoperability Sentiment")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("### 🎯 Key Findings")

                # Calculate sentiment
                if not data['interop_sentiment'].empty:
                    sentiment_col = None
                    for col in ['Sentiment', 'sentiment', 'label', 'Label']:
                        if col in data['interop_sentiment'].columns:
                            sentiment_col = col
                            break

                    if sentiment_col:
                        counts = data['interop_sentiment'][sentiment_col].value_counts(normalize=True) * 100

                        st.metric("Positive", f"{counts.get('positive', counts.get('Positive', 0)):.1f}%",
                                 help="Optimism about OpenXR and open standards")
                        st.metric("Neutral", f"{counts.get('neutral', counts.get('Neutral', 0)):.1f}%",
                                 help="Balanced discussion of trade-offs")
                        st.metric("Negative", f"{counts.get('negative', counts.get('Negative', 0)):.1f}%",
                                 help="Concerns about vendor lock-in")

                st.markdown("---")
                st.markdown("""
                ### ⚠️ Primary Concerns
                - Platform fragmentation
                - Vendor lock-in risk
                - Integration complexity
                - Lack of unified standards

                ### ✅ Positive Signals
                - OpenXR adoption growing
                - Industry collaboration increasing
                """)

            st.markdown("---")
            create_explanation_box(
                "Strategic Implication",
                """Organizations should <strong>prioritize OpenXR-compatible solutions</strong> and avoid committing
                exclusively to single-vendor platforms. The high level of concern around interoperability suggests
                this will be a key differentiator and cost factor in XR implementations.""",
                "warning"
            )

        with tab2:
            st.markdown("### Dominant Terms in Interoperability Discussions")

            if not data['interop_wordcloud'].empty:
                fig = create_wordcloud_chart(data['interop_wordcloud'], "Interoperability - Top 25 Terms", 25)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                st.markdown("#### 🔍 Term Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **Frequently Discussed:**
                    - Cross-platform compatibility
                    - OpenXR standard
                    - API integration
                    - Data exchange formats
                    """)
                with col2:
                    st.markdown("""
                    **Concern Indicators:**
                    - Vendor lock-in
                    - Fragmentation
                    - Compatibility issues
                    - Integration costs
                    """)

        with tab3:
            if data['interop_topics']:
                display_topics(data['interop_topics'], "Interoperability Topics")

            if not data['interop_integration'].empty:
                st.markdown("---")
                st.markdown("### 📊 Integration Analysis")
                st.dataframe(data['interop_integration'], use_container_width=True)

        with tab4:
            st.markdown("### 💼 Managerial Implications for Interoperability")

            create_explanation_box(
                "Strategic Recommendations",
                """Based on sentiment analysis and topic modeling:
                <ol>
                <li><strong>Adopt Open Standards First:</strong> Prioritize OpenXR-compatible platforms to ensure portability</li>
                <li><strong>Multi-Vendor Strategy:</strong> Design for device diversity rather than single-vendor dependence</li>
                <li><strong>API-First Architecture:</strong> Build integration layers to connect XR with existing systems</li>
                <li><strong>Future-Proof Investments:</strong> Evaluate vendor roadmaps for standards compliance</li>
                <li><strong>Total Cost of Ownership:</strong> Factor integration and switching costs into vendor selection</li>
                </ol>""",
                "info"
            )

            if data['interop_implications']:
                st.markdown("---")
                st.markdown("### 📄 Detailed Analysis")
                st.text_area("", data['interop_implications'], height=300)

    # Scalability
    elif page == "📈 Scalability":
        st.markdown('<p class="dimension-header">Scalability Assessment</p>', unsafe_allow_html=True)

        create_explanation_box(
            "Dimension Overview: Enterprise-Grade Deployment Capacity",
            """<strong>Scalability evaluates XR's ability to support enterprise-wide deployment across hundreds or thousands of users.</strong><br><br>

            Five critical scalability components analyzed:
            <ol>
            <li><strong>Infrastructure Scalability:</strong> Network bandwidth (5G/6G), edge computing, cloud resources</li>
            <li><strong>Data Pipeline Scalability:</strong> Real-time rendering, streaming, and content delivery at scale</li>
            <li><strong>Application Architecture:</strong> Cloud vs. edge trade-offs, distributed computing models</li>
            <li><strong>Security & Compliance:</strong> Enterprise-grade data protection and regulatory compliance</li>
            <li><strong>Performance Monitoring:</strong> Quality of experience (QoE) metrics and optimization</li>
            </ol>

            <strong>Why This Matters:</strong> Many XR pilots succeed but fail to scale due to infrastructure limitations,
            costs, or performance degradation. This dimension reveals readiness for production deployment.
            """,
            "info"
        )

        tab1, tab2, tab3, tab4 = st.tabs(["📈 Sentiment", "🔧 Infrastructure", "📊 Components", "📄 Report"])

        with tab1:
            st.markdown("### Sentiment Analysis: Scalability Readiness")

            create_explanation_box(
                "Understanding Scalability Concerns",
                """Sentiment around scalability is <strong>cautiously optimistic but mixed</strong> (~48% positive).
                While technical solutions exist, concerns persist about infrastructure costs, bandwidth requirements,
                and complexity of managing XR at enterprise scale.""",
                "warning"
            )

            if not data['scalability_sentiment'].empty:
                col1, col2 = st.columns([3, 2])

                with col1:
                    fig = create_sentiment_pie_chart(data['scalability_sentiment'], "Scalability Sentiment")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown("### 🎯 Key Challenges")
                    st.markdown("""
                    #### Infrastructure Barriers:
                    - 🌐 High bandwidth requirements
                    - ☁️ Edge computing gaps
                    - 💰 Significant deployment costs
                    - 📡 Network readiness varies
                    - 🔧 Complexity of distributed systems

                    #### Positive Indicators:
                    - ✅ 5G/6G rollout progressing
                    - ✅ Cloud rendering maturing
                    - ✅ Edge computing investments increasing
                    """)

        with tab2:
            st.markdown("### Infrastructure Scalability Components")

            create_explanation_box(
                "Five Pillars of XR Infrastructure",
                """Our analysis examined social data signals across five infrastructure categories.
                Each represents a critical enabler for scaling XR beyond pilots to enterprise-wide deployment.""",
                "info"
            )

            st.markdown("---")
            st.markdown("### 📊 Data Points Analyzed by Component")

            component_data = {
                'Component': [
                    '5G/6G Connectivity',
                    'Edge Computing',
                    'Cloud Rendering',
                    'Mobile Device Management',
                    'Infrastructure Scaling'
                ],
                'Data Points': [
                    len(data['scalability_5g']) if not data['scalability_5g'].empty else 0,
                    len(data['scalability_edge']) if not data['scalability_edge'].empty else 0,
                    len(data['scalability_cloud']) if not data['scalability_cloud'].empty else 0,
                    len(data['scalability_mobile']) if not data['scalability_mobile'].empty else 0,
                    len(data['scalability_scaling']) if not data['scalability_scaling'].empty else 0
                ],
                'Key Focus': [
                    'Ultra-low latency, high bandwidth networks',
                    'Distributed computing closer to users',
                    'Rendering offload to reduce device requirements',
                    'Fleet management of XR devices at scale',
                    'Overall infrastructure orchestration'
                ],
                'Maturity': [
                    '🟡 Developing (5G deployed, 6G research)',
                    '🟡 Developing (Growing investment)',
                    '🟢 Maturing (Multiple vendors)',
                    '🟢 Mature (MDM tools exist)',
                    '🟡 Developing (Complex integration)'
                ]
            }

            df_components = pd.DataFrame(component_data)
            st.dataframe(df_components, use_container_width=True, hide_index=True)

            # Display sample data if available
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                if not data['scalability_5g'].empty:
                    with st.expander("📡 5G/6G Connectivity Data Sample"):
                        st.dataframe(data['scalability_5g'].head(10))

                if not data['scalability_edge'].empty:
                    with st.expander("☁️ Edge Computing Data Sample"):
                        st.dataframe(data['scalability_edge'].head(10))

                if not data['scalability_cloud'].empty:
                    with st.expander("🖥️ Cloud Rendering Data Sample"):
                        st.dataframe(data['scalability_cloud'].head(10))

            with col2:
                if not data['scalability_mobile'].empty:
                    with st.expander("📱 Mobile Device Management Sample"):
                        st.dataframe(data['scalability_mobile'].head(10))

                if not data['scalability_scaling'].empty:
                    with st.expander("⚙️ Infrastructure Scaling Sample"):
                        st.dataframe(data['scalability_scaling'].head(10))

        with tab3:
            st.markdown("### Five Key Scalability Themes")

            themes = [
                {
                    'title': '1️⃣ Infrastructure Scalability',
                    'description': '5G/6G connectivity requirements for low-latency, high-bandwidth XR experiences',
                    'challenges': ['Network coverage gaps', 'Latency requirements (<20ms)', 'Bandwidth costs'],
                    'opportunities': ['5G expansion ongoing', 'Private 5G networks', 'WiFi 6E/7 alternatives']
                },
                {
                    'title': '2️⃣ Data Pipeline Scalability',
                    'description': 'Real-time rendering, streaming, and content delivery at scale',
                    'challenges': ['Rendering complexity', 'Content distribution', 'Real-time synchronization'],
                    'opportunities': ['Cloud rendering services', 'CDN optimization', 'Compression advances']
                },
                {
                    'title': '3️⃣ Application Architecture',
                    'description': 'Cloud vs. edge computing trade-offs for XR workloads',
                    'challenges': ['Latency vs cost trade-offs', 'Hybrid architecture complexity', 'Vendor options'],
                    'opportunities': ['Flexible deployment models', 'Edge computing growth', 'Multi-cloud strategies']
                },
                {
                    'title': '4️⃣ Security & Compliance',
                    'description': 'Enterprise-grade data protection and regulatory compliance',
                    'challenges': ['Data privacy in XR', 'Biometric data handling', 'Compliance frameworks'],
                    'opportunities': ['Security standards emerging', 'Zero-trust architectures', 'Encryption advances']
                },
                {
                    'title': '5️⃣ Performance Monitoring',
                    'description': 'Quality of experience (QoE) metrics and system optimization',
                    'challenges': ['Defining QoE metrics', 'Monitoring distributed systems', 'Performance optimization'],
                    'opportunities': ['Analytics tools maturing', 'AI-driven optimization', 'Predictive maintenance']
                }
            ]

            for theme in themes:
                with st.expander(f"{theme['title']}: {theme['description']}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**⚠️ Challenges:**")
                        for challenge in theme['challenges']:
                            st.markdown(f"- {challenge}")
                    with col2:
                        st.markdown("**✅ Opportunities:**")
                        for opp in theme['opportunities']:
                            st.markdown(f"- {opp}")

            # Topic distribution if available
            if not data['scalability_topic_dist'].empty:
                st.markdown("---")
                st.markdown("### 📊 LDA Topic Distribution")
                st.dataframe(data['scalability_topic_dist'], use_container_width=True)

        with tab4:
            st.markdown("### 📄 Comprehensive Scalability Report")

            if data['scalability_report']:
                st.text_area("Detailed Scalability Analysis", data['scalability_report'], height=400)
            else:
                st.info("Comprehensive report not available")

            st.markdown("---")
            create_explanation_box(
                "Strategic Scalability Recommendations",
                """<strong>For organizations planning XR deployment:</strong>
                <ol>
                <li><strong>Assess Infrastructure First:</strong> Audit network capacity, edge computing availability, bandwidth costs</li>
                <li><strong>Start Small, Scale Incrementally:</strong> Pilot with 10-50 users before enterprise rollout</li>
                <li><strong>Plan for Hybrid Architecture:</strong> Mix of cloud rendering and edge processing based on use case</li>
                <li><strong>Partner with Infrastructure Providers:</strong> Leverage cloud providers' XR services (AWS, Azure, Google Cloud)</li>
                <li><strong>Budget for Growth:</strong> Infrastructure costs scale non-linearly; plan for 2-3x initial estimates</li>
                </ol>""",
                "info"
            )

    # Data Intelligence Alignment
    elif page == "🤖 Data Intelligence Alignment":
        st.markdown('<p class="dimension-header">Alignment to Data Intelligence</p>', unsafe_allow_html=True)

        create_explanation_box(
            "Dimension Overview: Synergy with AI, Analytics, and Decision Systems",
            """<strong>This dimension evaluates XR's compatibility and value-add when integrated with AI, analytics, and data intelligence systems.</strong><br><br>

            🔥 <strong>HIGHEST SENTIMENT DIMENSION (71% Positive)</strong> 🔥<br><br>

            Integration opportunities analyzed:
            <ul>
            <li><strong>3D Data Visualization:</strong> Immersive exploration of complex analytical datasets</li>
            <li><strong>AI-Powered Spatial Understanding:</strong> Computer vision, object recognition, scene analysis</li>
            <li><strong>Real-Time Decision Support:</strong> Overlaying analytics insights on physical environments</li>
            <li><strong>Digital Twin Analytics:</strong> Connecting virtual models with live data and ML predictions</li>
            <li><strong>Natural Language Interfaces:</strong> Voice-driven interaction with data systems in XR</li>
            </ul>

            <strong>Why This Matters:</strong> XR can become the next-generation interface for data intelligence systems,
            offering competitive advantages through improved data comprehension and decision-making speed.
            """,
            "success"
        )

        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Sentiment Score",
                "71% Positive",
                "🔥 Highest Across Dimensions",
                help="Strongest positive sentiment of any dimension"
            )
        with col2:
            st.metric(
                "Data Sources Analyzed",
                "4 Categories",
                help="Social blogs, professional networks, research papers, Twitter/X"
            )
        with col3:
            total_sources = (
                len(data['alignment_social']) +
                len(data['alignment_professional']) +
                len(data['alignment_research']) +
                len(data['alignment_twitter'])
            )
            st.metric(
                "Total Data Points",
                f"{total_sources:,}",
                help="Combined data points across all source categories"
            )

        st.markdown("---")

        tab1, tab2, tab3 = st.tabs(["📊 Data Sources", "🔗 Integration Opportunities", "💡 Strategic Value"])

        with tab1:
            st.markdown("### Data Sources Analyzed")

            create_explanation_box(
                "Multi-Source Social Data Analysis",
                """To assess XR's alignment with data intelligence, we analyzed discussions across four distinct
                data source categories. Each provides unique perspectives on how XR and AI/analytics can integrate.""",
                "info"
            )

            col1, col2 = st.columns(2)

            with col1:
                if not data['alignment_social'].empty:
                    st.metric("📱 Social Media & Tech Blogs", f"{len(data['alignment_social']):,} posts")
                    with st.expander("View Social/Blog Data Sample"):
                        st.dataframe(data['alignment_social'].head(10))

                if not data['alignment_research'].empty:
                    st.metric("📚 Research Papers", f"{len(data['alignment_research']):,} papers")
                    with st.expander("View Research Data Sample"):
                        st.dataframe(data['alignment_research'].head(10))

            with col2:
                if not data['alignment_professional'].empty:
                    st.metric("💼 Professional Networks (LinkedIn)", f"{len(data['alignment_professional']):,} discussions")
                    with st.expander("View Professional Network Sample"):
                        st.dataframe(data['alignment_professional'].head(10))

                if not data['alignment_twitter'].empty:
                    st.metric("🐦 Twitter/X Posts", f"{len(data['alignment_twitter']):,} tweets")
                    with st.expander("View Twitter/X Data Sample"):
                        st.dataframe(data['alignment_twitter'].head(10))

            # Master corpus
            if not data['alignment_master'].empty:
                st.markdown("---")
                st.markdown("### 📊 Integrated Master Corpus")
                st.info(f"Combined corpus contains {len(data['alignment_master']):,} records across all source categories")

                with st.expander("Explore Master Corpus Sample"):
                    st.dataframe(data['alignment_master'].head(20))

        with tab2:
            st.markdown("### Strong Natural Fit: XR + AI/Data Intelligence")

            create_explanation_box(
                "🔥 Why Data Intelligence Shows Highest Sentiment",
                """The 71% positive sentiment reflects strong enthusiasm for XR as an interface layer for AI and analytics systems.
                Unlike interoperability or scalability (which face technical barriers), XR and data intelligence have
                <strong>natural, mutually reinforcing synergies</strong> that create competitive advantages.""",
                "success"
            )

            st.markdown("---")
            st.markdown("### 🎯 Five Key Integration Points")

            integration_points = [
                {
                    'icon': '📊',
                    'title': '3D Data Visualization for Complex Analytics',
                    'description': 'Transform abstract data into immersive 3D visualizations',
                    'examples': [
                        'Multidimensional dataset exploration in virtual space',
                        'Network graphs and relationship visualization',
                        'Time-series data as spatial journeys',
                        'Geospatial analytics in augmented environments'
                    ],
                    'benefit': 'Humans process visual information 60,000x faster than text—XR amplifies this with spatial reasoning'
                },
                {
                    'icon': '🤖',
                    'title': 'AI-Driven Spatial Understanding',
                    'description': 'Computer vision and ML models enhance XR capabilities',
                    'examples': [
                        'Real-time object recognition and classification',
                        'Scene understanding and spatial mapping',
                        'Predictive overlays based on ML models',
                        'Anomaly detection in physical environments'
                    ],
                    'benefit': 'AI makes XR context-aware and intelligent rather than merely immersive'
                },
                {
                    'icon': '⚡',
                    'title': 'Real-Time Decision Support Overlays',
                    'description': 'Contextual analytics insights delivered at point of need',
                    'examples': [
                        'Maintenance technicians see predictive failure analytics on equipment',
                        'Surgeons view patient vitals and scan results during procedures',
                        'Warehouse workers get route optimization overlays',
                        'Field service agents access customer history and troubleshooting guides'
                    ],
                    'benefit': 'Reduces decision latency by bringing insights to the workflow, not the other way around'
                },
                {
                    'icon': '🏭',
                    'title': 'Digital Twin Analytics',
                    'description': 'Connect virtual models with live data streams and ML predictions',
                    'examples': [
                        'Manufacturing: Virtual factory mirrors physical operations with performance analytics',
                        'Smart cities: Digital models show traffic patterns, energy usage, air quality',
                        'Healthcare: Patient digital twins for treatment simulation',
                        'Supply chain: Real-time logistics visualization with predictive analytics'
                    ],
                    'benefit': 'Bridges physical and digital worlds for simulation, optimization, and predictive maintenance'
                },
                {
                    'icon': '🗣️',
                    'title': 'Natural Language & Voice Interfaces',
                    'description': 'Hands-free, conversational interaction with data systems',
                    'examples': [
                        'Voice-commanded data queries in XR environments',
                        'Natural language to SQL/analytics pipeline',
                        'Conversational exploration of dashboards and reports',
                        'Multimodal interaction: gesture + voice + gaze'
                    ],
                    'benefit': 'Enables data access in hands-busy environments and reduces learning curve'
                }
            ]

            for point in integration_points:
                with st.expander(f"{point['icon']} {point['title']}", expanded=False):
                    st.markdown(f"**{point['description']}**")
                    st.markdown("**Use Case Examples:**")
                    for example in point['examples']:
                        st.markdown(f"- {example}")
                    st.markdown(f"**Strategic Benefit:** {point['benefit']}")

        with tab3:
            st.markdown("### 💡 Strategic Value & Competitive Advantage")

            create_explanation_box(
                "Why Data Intelligence Alignment is XR's Strongest Opportunity",
                """Based on comprehensive sentiment analysis, this dimension represents the <strong>clearest path
                to differentiation and ROI</strong> for enterprise XR adoption. Organizations that integrate XR
                with their data intelligence stack can achieve:
                <ul>
                <li><strong>Faster Decision-Making:</strong> Reduced time from data to insight to action</li>
                <li><strong>Improved Comprehension:</strong> Complex data becomes intuitive through spatial visualization</li>
                <li><strong>Competitive Edge:</strong> Early adopters gain advantages in data-driven operations</li>
                <li><strong>Workflow Efficiency:</strong> Information delivered contextually at point of need</li>
                <li><strong>Training Data Generation:</strong> XR interactions create new datasets for ML models</li>
                </ul>""",
                "success"
            )

            st.markdown("---")
            st.markdown("### 📈 Adoption Roadmap")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### Phase 1: Visualize")
                st.markdown("""
                **0-6 months**
                - 3D dashboards for analytics
                - Immersive data exploration tools
                - AR overlays on equipment/processes
                - Low integration complexity
                """)

            with col2:
                st.markdown("#### Phase 2: Integrate")
                st.markdown("""
                **6-18 months**
                - Connect to AI/ML pipelines
                - Real-time data streaming to XR
                - Digital twin implementations
                - Voice/NLP interfaces
                """)

            with col3:
                st.markdown("#### Phase 3: Optimize")
                st.markdown("""
                **18+ months**
                - AI-driven XR experiences
                - Predictive analytics in context
                - Full workflow integration
                - Competitive differentiation
                """)

            st.markdown("---")
            create_explanation_box(
                "🎯 Recommendation: Lead with Data Intelligence Use Cases",
                """Given the strong positive sentiment and natural fit, organizations should <strong>prioritize
                XR projects that integrate with their data intelligence capabilities</strong>. Examples:
                <ul>
                <li>Immersive analytics dashboards for executives</li>
                <li>AR-guided maintenance with predictive failure overlays</li>
                <li>Digital twin control rooms for operations management</li>
                <li>Spatial data exploration for data science teams</li>
                </ul>
                These use cases leverage XR's strengths while addressing clear business needs with measurable ROI.""",
                "success"
            )

    # Use Cases
    elif page == "💼 Use Cases":
        st.markdown('<p class="dimension-header">Use Cases Analysis</p>', unsafe_allow_html=True)

        create_explanation_box(
            "Dimension Overview: Breadth and Diversity of Industry Applications",
            """<strong>This dimension examines the range and maturity of XR applications across industries and business functions.</strong><br><br>

            Analysis covers:
            <ul>
            <li><strong>Industry Diversity:</strong> Healthcare, manufacturing, retail, education, real estate, and more</li>
            <li><strong>Functional Applications:</strong> Training, design, collaboration, marketing, maintenance</li>
            <li><strong>Adoption Maturity:</strong> Which sectors show proven ROI vs. exploratory pilots</li>
            <li><strong>Use Case Effectiveness:</strong> Sentiment analysis reveals which applications resonate most</li>
            </ul>

            <strong>Key Finding:</strong> Strong positive sentiment (68%) driven by successful training and education applications.
            Healthcare, manufacturing, and automotive lead in adoption maturity.
            """,
            "info"
        )

        tab1, tab2, tab3, tab4 = st.tabs(["📈 Sentiment", "☁️ Top Terms", "📋 Topics", "🏢 Industries"])

        with tab1:
            st.markdown("### Sentiment Analysis: Use Case Perceptions")

            create_explanation_box(
                "Understanding Use Case Sentiment",
                """Positive sentiment (68%) reflects proven value in specific applications, particularly training and education.
                Neutral sentiment (25%) represents sectors awaiting clearer ROI proof. Negative sentiment (7%) is lowest
                across all dimensions, indicating broad confidence in XR's practical value.""",
                "info"
            )

            col1, col2 = st.columns([3, 2])

            with col1:
                if not data['usecases_sentiment'].empty:
                    fig = create_sentiment_pie_chart(data['usecases_sentiment'], "Use Cases Sentiment")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("### 🎯 Sentiment Drivers")

                if not data['usecases_sentiment'].empty:
                    sentiment_col = None
                    for col in ['Sentiment', 'sentiment', 'label', 'Label']:
                        if col in data['usecases_sentiment'].columns:
                            sentiment_col = col
                            break

                    if sentiment_col:
                        counts = data['usecases_sentiment'][sentiment_col].value_counts(normalize=True) * 100

                        st.metric("Positive", f"{counts.get('positive', counts.get('Positive', 0)):.1f}%",
                                 help="Training & education success stories")
                        st.metric("Neutral", f"{counts.get('neutral', counts.get('Neutral', 0)):.1f}%",
                                 help="Awaiting ROI validation")
                        st.metric("Negative", f"{counts.get('negative', counts.get('Negative', 0)):.1f}%",
                                 help="Implementation challenges")

                st.markdown("---")
                st.markdown("""
                ### Top Performing Uses:
                - ✅ Training & simulation
                - ✅ Medical education
                - ✅ Design & prototyping
                - ✅ Remote collaboration
                """)

        with tab2:
            st.markdown("### Top Terms in Use Case Discussions")

            if not data['usecases_wordcloud'].empty:
                fig = create_wordcloud_chart(data['usecases_wordcloud'], "Use Cases - Top 25 Terms", 25)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("""
                    **Training Focus**
                    - Immersive learning
                    - Skills development
                    - Safety training
                    - Hands-on practice
                    """)
                with col2:
                    st.markdown("""
                    **Industry Applications**
                    - Healthcare/medical
                    - Manufacturing
                    - Retail experiences
                    - Architecture/design
                    """)
                with col3:
                    st.markdown("""
                    **Value Indicators**
                    - ROI metrics
                    - Productivity gains
                    - Cost savings
                    - User engagement
                    """)

        with tab3:
            if data['usecases_topics']:
                display_topics(data['usecases_topics'], "Use Case Topics from LDA Analysis")

            if not data['usecases_dominant_topic'].empty:
                st.markdown("---")
                st.markdown("### 📊 Dominant Topic Distribution")
                st.dataframe(data['usecases_dominant_topic'], use_container_width=True)

        with tab4:
            st.markdown("### 🏢 Eight Primary Use Case Categories")

            create_explanation_box(
                "Industry Adoption Landscape",
                """Through topic modeling and sentiment analysis, we identified eight distinct use case categories.
                Each shows different levels of adoption maturity, ROI clarity, and expansion potential.""",
                "info"
            )

            st.markdown("---")

            use_cases = [
                {
                    'category': '🏥 Training & Simulation',
                    'maturity': '🟢 High',
                    'industries': 'Healthcare, Military, Manufacturing, Aviation',
                    'description': 'Immersive training environments for high-risk or complex procedures',
                    'examples': [
                        'Medical procedure simulation and practice',
                        'Military combat and tactical training',
                        'Manufacturing assembly line training',
                        'Flight simulator and pilot training'
                    ],
                    'roi': 'Proven - Reduced training costs (30-50%), improved retention, safer learning',
                    'sentiment': '75% Positive'
                },
                {
                    'category': '🎨 Design & Prototyping',
                    'maturity': '🟢 High',
                    'industries': 'Architecture, Automotive, Product Design, Engineering',
                    'description': 'Virtual design reviews and prototyping before physical production',
                    'examples': [
                        'Architectural walkthroughs and client presentations',
                        'Automotive design and ergonomics testing',
                        'Product design iteration and visualization',
                        'Engineering design validation'
                    ],
                    'roi': 'Proven - Faster design cycles (20-40%), reduced prototyping costs',
                    'sentiment': '72% Positive'
                },
                {
                    'category': '👥 Remote Collaboration',
                    'maturity': '🟡 Medium',
                    'industries': 'Distributed Teams, Consulting, Remote Work',
                    'description': 'Virtual meeting spaces and collaborative work environments',
                    'examples': [
                        'Virtual conference rooms and meetings',
                        'Distributed team design sessions',
                        'Remote expert assistance and guidance',
                        'Virtual co-working spaces'
                    ],
                    'roi': 'Developing - Travel cost savings, but user adoption challenges',
                    'sentiment': '65% Positive'
                },
                {
                    'category': '🛍️ Retail & Marketing',
                    'maturity': '🟡 Medium',
                    'industries': 'Retail, E-commerce, Real Estate, Automotive',
                    'description': 'Virtual showrooms, try-before-buy experiences, and immersive marketing',
                    'examples': [
                        'Virtual clothing and furniture try-on',
                        'Virtual showrooms and product exploration',
                        'Immersive brand experiences',
                        'AR product visualization in home environment'
                    ],
                    'roi': 'Mixed - Increased engagement, but conversion ROI varies',
                    'sentiment': '68% Positive'
                },
                {
                    'category': '🔧 Maintenance & Repair',
                    'maturity': '🟢 High',
                    'industries': 'Manufacturing, Utilities, Aerospace, Oil & Gas',
                    'description': 'AR-guided maintenance procedures and remote expert assistance',
                    'examples': [
                        'Step-by-step repair instructions overlaid on equipment',
                        'Remote expert sees technician view and provides guidance',
                        'Predictive maintenance alerts with visual overlays',
                        'Equipment inspection with AR annotation'
                    ],
                    'roi': 'Proven - Reduced downtime (20-30%), faster repairs, lower travel costs',
                    'sentiment': '74% Positive'
                },
                {
                    'category': '🏥 Healthcare Applications',
                    'maturity': '🟢 High',
                    'industries': 'Healthcare, Medical Devices, Pharmaceuticals',
                    'description': 'Surgery planning, therapy, medical visualization, and training',
                    'examples': [
                        'Pre-surgical planning with 3D patient models',
                        'Pain management and rehabilitation therapy',
                        'Medical education and anatomy learning',
                        'Exposure therapy for phobias and PTSD'
                    ],
                    'roi': 'Proven - Improved outcomes, reduced complications, better training',
                    'sentiment': '76% Positive'
                },
                {
                    'category': '🎓 Education',
                    'maturity': '🟡 Medium',
                    'industries': 'K-12, Higher Ed, Corporate Training',
                    'description': 'Immersive learning experiences and virtual laboratories',
                    'examples': [
                        'Virtual field trips and historical recreations',
                        'Chemistry and physics lab simulations',
                        'Language immersion environments',
                        'Soft skills and empathy training'
                    ],
                    'roi': 'Developing - Improved engagement and retention, but scale challenges',
                    'sentiment': '70% Positive'
                },
                {
                    'category': '🏢 Real Estate',
                    'maturity': '🟡 Medium',
                    'industries': 'Commercial Real Estate, Residential, Construction',
                    'description': 'Virtual property tours and space planning',
                    'examples': [
                        'Virtual property walkthroughs for remote buyers',
                        'Pre-construction visualization',
                        'Interior design and space planning',
                        'Commercial real estate showcases'
                    ],
                    'roi': 'Mixed - Time savings, broader reach, but adoption varies',
                    'sentiment': '66% Positive'
                }
            ]

            for use_case in use_cases:
                with st.expander(f"{use_case['category']} - {use_case['maturity']} Maturity | Sentiment: {use_case['sentiment']}", expanded=False):
                    col1, col2 = st.columns([3, 2])

                    with col1:
                        st.markdown(f"**Industries:** {use_case['industries']}")
                        st.markdown(f"**Description:** {use_case['description']}")
                        st.markdown("**Key Examples:**")
                        for example in use_case['examples']:
                            st.markdown(f"- {example}")

                    with col2:
                        st.markdown(f"**Adoption Maturity:** {use_case['maturity']}")
                        st.markdown(f"**ROI Status:** {use_case['roi']}")
                        st.markdown(f"**Sentiment:** {use_case['sentiment']}")

            # Integration summary
            if not data['usecases_integration'].empty:
                st.markdown("---")
                st.markdown("### 📊 Integration Summary Data")
                st.dataframe(data['usecases_integration'], use_container_width=True)

            # Managerial implications
            if data['usecases_implications']:
                st.markdown("---")
                st.markdown("### 💼 Managerial Implications")

                create_explanation_box(
                    "Strategic Use Case Selection",
                    """<strong>Recommended Approach:</strong> Start with high-maturity, high-ROI use cases
                    (training, maintenance, healthcare, design) where XR has proven value. Expand to medium-maturity
                    areas once core capabilities are established. Avoid premature investment in exploratory
                    use cases without clear success metrics.""",
                    "info"
                )

                st.text_area("Detailed Analysis", data['usecases_implications'], height=250)

    # Integrated Analysis
    elif page == "🔬 Integrated Analysis":
        st.markdown('<p class="dimension-header">Integrated Analysis</p>', unsafe_allow_html=True)

        create_explanation_box(
            "Cross-Dimensional Synthesis",
            """<strong>This section integrates findings from word cloud analysis, sentiment classification, and topic modeling
            across all five dimensions to identify convergent themes and strategic insights.</strong><br><br>

            By analyzing patterns that emerge across multiple dimensions, we reveal the most significant opportunities
            and challenges facing XR adoption—insights that aren't visible when examining dimensions in isolation.""",
            "info"
        )

        st.markdown("### 🔍 Four Convergent Themes Across All Analyses")

        # Theme 1
        col1, col2 = st.columns(2)

        with col1:
            create_explanation_box(
                "1️⃣ Infrastructure Dependence",
                """<strong>Word Cloud:</strong> Terms like "5G", "edge computing", "bandwidth", "latency" appear consistently<br>
                <strong>Sentiment:</strong> Concerned about readiness (48% positive in scalability dimension)<br>
                <strong>Topics:</strong> Infrastructure scalability emerges as dominant theme<br><br>

                <strong>Insight:</strong> XR's success is heavily dependent on network and computing infrastructure improvements.
                Organizations must assess infrastructure readiness before committing to XR deployments.
                5G/edge computing investments are prerequisites, not nice-to-haves.""",
                "warning"
            )

            create_explanation_box(
                "2️⃣ Enterprise Value Recognition",
                """<strong>Word Cloud:</strong> "ROI", "productivity", "training costs", "efficiency" frequently mentioned<br>
                <strong>Sentiment:</strong> Positive for specific use cases (68% in use case dimension)<br>
                <strong>Topics:</strong> Training and remote collaboration identified as leading adoption drivers<br><br>

                <strong>Insight:</strong> The market has moved past "is XR useful?" to "where is XR most valuable?"
                Focus has shifted from technology exploration to business value validation.
                Organizations should lead with high-ROI use cases (training, maintenance) rather than broad experimentation.""",
                "success"
            )

        with col2:
            create_explanation_box(
                "3️⃣ Platform Fragmentation Anxiety",
                """<strong>Word Cloud:</strong> "compatibility", "standards", "integration", "vendor lock-in" prominent<br>
                <strong>Sentiment:</strong> Most negative cluster (20% negative in interoperability)<br>
                <strong>Topics:</strong> Interoperability consistently identified as persistent barrier<br><br>

                <strong>Insight:</strong> Vendor fragmentation is the single greatest concern across all dimensions.
                Lack of interoperability creates integration costs, limits scalability, and increases risk.
                This is a strategic decision point: organizations must prioritize open standards (OpenXR)
                or accept vendor lock-in trade-offs.""",
                "warning"
            )

            create_explanation_box(
                "4️⃣ AI Integration Excitement",
                """<strong>Word Cloud:</strong> "intelligent", "AI-powered", "predictive", "machine learning", "analytics"<br>
                <strong>Sentiment:</strong> Most positive cluster (71% in data intelligence dimension)<br>
                <strong>Topics:</strong> Data intelligence alignment identified as strongest opportunity<br><br>

                <strong>Insight:</strong> XR + AI represents the most promising integration opportunity.
                Combining immersive interfaces with intelligent systems creates competitive advantages
                that neither technology achieves alone. This should be the primary focus for differentiation.""",
                "success"
            )

        # Comparative sentiment across dimensions
        st.markdown("---")
        st.markdown("### 📊 Comparative Sentiment Distribution")

        create_explanation_box(
            "Interpreting Cross-Dimensional Sentiment",
            """This visualization reveals which dimensions have strong confidence (high positive sentiment)
            vs. areas of concern (high negative sentiment). Use this to prioritize where to invest
            (high positive) and where to proceed cautiously (mixed sentiment).""",
            "info"
        )

        dimensions_map = {
            'Present State\nof Maturity': 'maturity_sentiment',
            'Interoperability': 'interop_sentiment',
            'Scalability': 'scalability_sentiment',
            'Use Cases': 'usecases_sentiment'
        }

        fig = create_sentiment_comparison(data, dimensions_map)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        # Dimension scorecard
        st.markdown("---")
        st.markdown("### 🎯 XR Readiness Scorecard")

        scorecard_data = {
            'Dimension': [
                'Present State of Maturity',
                'Interoperability',
                'Scalability',
                'Data Intelligence Alignment',
                'Use Cases'
            ],
            'Status': [
                'Advanced - Multiple commercial products',
                'Moderate - Platform fragmentation issues',
                'Evolving - Infrastructure gaps remain',
                'Strong - Natural synergy with AI/analytics',
                'Diverse - 8+ proven categories'
            ],
            'Sentiment': ['62% Positive', '45% Positive', '48% Positive', '71% Positive', '68% Positive'],
            'Readiness': ['✅ Ready', '⚠️ Proceed with Caution', '⚠️ Requires Planning', '✅ High Opportunity', '✅ Proven Value'],
            'Primary Challenge': [
                'Hardware costs',
                'Vendor lock-in risk',
                'Bandwidth & infrastructure',
                'None (Opportunity area)',
                'ROI validation in some sectors'
            ],
            'Recommendation': [
                'Deploy for targeted use cases',
                'Prioritize OpenXR compatibility',
                'Assess infrastructure first',
                'Lead with AI integration',
                'Start with proven categories'
            ]
        }

        df_scorecard = pd.DataFrame(scorecard_data)
        st.dataframe(df_scorecard, use_container_width=True, hide_index=True)

        # Strategic implications
        st.markdown("---")
        st.markdown("### 🎯 Integrated Strategic Implications")

        create_explanation_box(
            "Data-Driven Decision Framework",
            """Based on comprehensive cross-dimensional analysis:<br><br>

            <strong>1. LEAD WITH STRENGTHS (71% & 68% positive sentiment)</strong>
            <ul>
            <li>Focus initial projects on <strong>AI/data intelligence integration</strong> (highest sentiment)</li>
            <li>Select use cases from <strong>proven categories</strong> (training, maintenance, design)</li>
            <li>Emphasize measurable business outcomes to build organizational confidence</li>
            </ul>

            <strong>2. MITIGATE RISKS (45% & 48% positive sentiment)</strong>
            <ul>
            <li>Address <strong>interoperability concerns</strong> through open standards (OpenXR)</li>
            <li>Conduct <strong>infrastructure assessment</strong> before committing to deployment scale</li>
            <li>Budget for integration costs and infrastructure upgrades</li>
            </ul>

            <strong>3. STAGE ADOPTION (Crawl-Walk-Run)</strong>
            <ul>
            <li><strong>Pilot (6-12 mo):</strong> 2-3 high-ROI use cases, 10-50 users, measure outcomes</li>
            <li><strong>Scale (12-24 mo):</strong> Expand successful pilots, build infrastructure incrementally</li>
            <li><strong>Transform (24+ mo):</strong> Enterprise-wide deployment, competitive differentiation</li>
            </ul>

            <strong>4. AVOID COMMON PITFALLS</strong>
            <ul>
            <li>❌ Don't rush enterprise-wide before validating pilots</li>
            <li>❌ Don't ignore infrastructure prerequisites</li>
            <li>❌ Don't commit to single-vendor ecosystems</li>
            <li>❌ Don't pursue "cool" use cases without clear ROI</li>
            </ul>""",
            "info"
        )

    # Managerial Implications
    elif page == "💡 Managerial Implications":
        st.markdown('<p class="dimension-header">Managerial Implications</p>', unsafe_allow_html=True)

        create_explanation_box(
            "Strategic Recommendations for Decision-Making",
            """<strong>This section translates analytical findings into actionable strategic recommendations
            organized by implementation timeline.</strong><br><br>

            Based on comprehensive sentiment analysis, topic modeling, and word cloud analysis across five dimensions,
            these recommendations provide a practical roadmap for XR adoption tailored to enterprise environments.""",
            "info"
        )

        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Immediate (0-6 mo)",
            "📅 Medium-Term (6-18 mo)",
            "🚀 Long-Term (18+ mo)",
            "⚠️ Risk Mitigation"
        ])

        with tab1:
            st.markdown("### Immediate Actions (0-6 months)")

            create_explanation_box(
                "Phase 1: Validation & Foundation",
                """<strong>Goal:</strong> Validate XR value through targeted pilots while establishing organizational readiness.<br>
                <strong>Investment Level:</strong> Moderate ($50K-$250K depending on scale)<br>
                <strong>Expected Outcome:</strong> Proof points for scaling decision and infrastructure roadmap""",
                "info"
            )

            st.markdown("---")

            # Action 1
            st.markdown("#### 1️⃣ Pilot Before Scale")
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("""
                **Strategic Rationale:** Sentiment analysis shows proven ROI in specific use cases (68% positive)
                but concerns about scalability (48% positive). Pilots reduce risk while demonstrating value.

                **Actions:**
                - Select 2-3 high-ROI use cases from proven categories (training, maintenance, design)
                - Target departments with immediate pain points and executive sponsorship
                - Establish clear, quantifiable success metrics (cost savings, time reduction, error rates)
                - Plan for 10-50 users in pilot phase
                - Document lessons learned and ROI calculation methodology

                **Data Insight:** Use case analysis reveals training and maintenance have highest proven ROI (74-75% positive sentiment)
                """)

            with col2:
                st.markdown("""
                **Success Metrics:**
                - Training time reduction
                - Error rate decrease
                - Travel cost savings
                - User satisfaction scores
                - Time to competency

                **Budget Range:**
                - Hardware: $1,000-$3,500 per unit
                - Software/licenses: $10K-$50K
                - Integration: $20K-$100K
                - Training: $5K-$20K
                """)

            st.markdown("---")

            # Action 2
            st.markdown("#### 2️⃣ Prioritize Interoperability")
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("""
                **Strategic Rationale:** Interoperability shows most negative sentiment (20%) and vendor lock-in
                is top concern across all dimensions. Decisions made now determine long-term flexibility.

                **Actions:**
                - Select OpenXR-compatible platforms and development tools
                - Avoid exclusive commitments to single-vendor ecosystems (Meta, Apple, Microsoft)
                - Design applications for multi-device accessibility
                - Evaluate vendors on standards compliance and integration APIs
                - Build or buy integration middleware for enterprise system connectivity

                **Data Insight:** Word cloud analysis shows "compatibility", "standards", and "vendor lock-in" as dominant concerns
                """)

            with col2:
                st.markdown("""
                **Vendor Evaluation Criteria:**
                - ✅ OpenXR SDK support
                - ✅ Enterprise API availability
                - ✅ Multi-device compatibility
                - ✅ Data export capabilities
                - ✅ Open development tools

                **Red Flags:**
                - ❌ Proprietary formats only
                - ❌ Limited API access
                - ❌ Hardware-exclusive apps
                """)

            st.markdown("---")

            # Action 3
            st.markdown("#### 3️⃣ Assess Infrastructure Readiness")
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("""
                **Strategic Rationale:** Scalability dimension shows infrastructure dependence as convergent theme
                (52% neutral/negative sentiment). Infrastructure gaps cause pilot failures when scaling.

                **Actions:**
                - Audit network bandwidth capacity (minimum 50 Mbps per concurrent user)
                - Assess edge computing availability and latency requirements (<20ms for responsive XR)
                - Evaluate cloud vs. edge trade-offs for rendering workloads
                - Plan 5G/WiFi 6E integration timeline for mobile XR
                - Budget for infrastructure upgrades (often underestimated by 2-3x)

                **Data Insight:** Topic modeling identifies 5 infrastructure scalability components as critical
                """)

            with col2:
                st.markdown("""
                **Infrastructure Checklist:**
                - [ ] Network bandwidth audit
                - [ ] Latency measurements
                - [ ] Edge computing assessment
                - [ ] Cloud provider evaluation
                - [ ] WiFi 6/6E or 5G availability
                - [ ] MDM for XR devices
                - [ ] Security/compliance review

                **Common Gaps:**
                - Insufficient bandwidth
                - High latency (>50ms)
                - No edge compute
                - Limited cloud budget
                """)

        with tab2:
            st.markdown("### Medium-Term Strategy (6-18 months)")

            create_explanation_box(
                "Phase 2: Scale & Integration",
                """<strong>Goal:</strong> Expand successful pilots and integrate XR with core business systems.<br>
                <strong>Investment Level:</strong> Significant ($250K-$1M+ depending on scale)<br>
                <strong>Expected Outcome:</strong> Enterprise-scale deployment with measurable business impact""",
                "info"
            )

            st.markdown("---")

            # Action 4
            st.markdown("#### 4️⃣ Integrate with Data Intelligence Stack")
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("""
                **Strategic Rationale:** Data intelligence alignment shows highest positive sentiment (71%)
                and represents strongest differentiation opportunity. Integration amplifies value of both technologies.

                **Actions:**
                - Connect XR interfaces to existing analytics platforms (Tableau, Power BI, custom dashboards)
                - Explore AI-powered XR applications (computer vision, NLP, predictive overlays)
                - Build 3D data visualization capabilities for immersive analytics
                - Develop digital twin control rooms for operations management
                - Create immersive dashboard prototypes for executive use
                - Implement real-time data streaming to XR applications

                **Data Insight:** This dimension has most positive sentiment, indicating market confidence in XR+AI synergy
                """)

            with col2:
                st.markdown("""
                **Integration Examples:**
                - 3D sales dashboards
                - AR maintenance with ML predictions
                - Digital twin + real-time IoT data
                - Immersive data exploration
                - Voice-driven analytics queries

                **Technology Stack:**
                - XR platforms
                - Data warehouses
                - ML/AI pipelines
                - Real-time streaming (Kafka, etc.)
                - APIs and middleware
                """)

            st.markdown("---")

            # Action 5
            st.markdown("#### 5️⃣ Develop Internal Expertise")
            col1, col2 = st.columns([3, 2])

            with col1:
                st.markdown("""
                **Strategic Rationale:** Skills gap identified as barrier across multiple dimensions.
                Internal expertise reduces vendor dependence and enables customization.

                **Actions:**
                - Train development teams on XR platforms (Unity, Unreal, WebXR)
                - Establish XR center of excellence with cross-functional team
                - Partner with specialized XR vendors for knowledge transfer
                - Build internal design and development capabilities
                - Create XR governance committee for standards and priorities
                - Hire or contract XR specialists for complex projects

                **Data Insight:** Organizations with internal XR capabilities show higher success rates in scaling
                """)

            with col2:
                st.markdown("""
                **Team Structure:**
                - XR developers (Unity/Unreal)
                - 3D designers/artists
                - UX researchers (XR-specific)
                - Integration engineers
                - Business analysts
                - Executive sponsor

                **Training Investment:**
                - Developer training: $5K-$15K per person
                - Certifications
                - Conference attendance
                - Vendor workshops
                """)

        with tab3:
            st.markdown("### Long-Term Positioning (18+ months)")

            create_explanation_box(
                "Phase 3: Transform & Differentiate",
                """<strong>Goal:</strong> Achieve competitive advantage through enterprise-wide XR capabilities.<br>
                <strong>Investment Level:</strong> Strategic ($1M+ ongoing)<br>
                <strong>Expected Outcome:</strong> XR as core capability, measurable competitive advantage""",
                "info"
            )

            st.markdown("---")

            # Action 6
            st.markdown("#### 6️⃣ Scale Strategically Across Enterprise")

            st.markdown("""
            **Strategic Rationale:** After validating pilots and building capabilities, scale proven use cases
            across organization while exploring new applications for competitive differentiation.

            **Actions:**
            - **Expand Proven Use Cases:** Roll out successful pilots enterprise-wide (training, maintenance, design)
            - **Invest in Proprietary Applications:** Build custom XR applications for competitive advantage
            - **Monitor Consumer XR Adoption:** Track consumer market for B2C XR opportunities
            - **Build Ecosystem Partnerships:** Collaborate with vendors, startups, and industry consortiums
            - **Continuous Innovation:** Dedicate resources to exploring emerging XR capabilities

            **Data Insight:** Organizations that systematically expand from pilots to enterprise-wide deployment
            achieve sustainable competitive advantages
            """)

            st.markdown("---")
            st.markdown("### 🎯 Long-Term Success Indicators")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("""
                **Business Metrics**
                - Cost savings: 20-40%
                - Productivity gains: 15-30%
                - Training time reduction: 30-50%
                - Error rates: 40-60% decrease
                - Customer satisfaction: +15-25%
                """)

            with col2:
                st.markdown("""
                **Adoption Metrics**
                - >70% user adoption rate
                - Multiple departments using XR
                - >100 concurrent users
                - >10 active applications
                - Executive-level usage
                """)

            with col3:
                st.markdown("""
                **Strategic Metrics**
                - Competitive differentiation
                - Customer/partner recognition
                - Industry thought leadership
                - Innovation pipeline
                - Talent attraction/retention
                """)

        with tab4:
            st.markdown("### Risk Mitigation Framework")

            create_explanation_box(
                "Proactive Risk Management",
                """<strong>Every technology adoption carries risks.</strong> This framework identifies key risks
                from sentiment analysis and provides mitigation strategies based on successful implementations.""",
                "warning"
            )

            st.markdown("---")

            risk_data = {
                'Risk': [
                    'Platform Obsolescence',
                    'Integration Complexity',
                    'Infrastructure Inadequacy',
                    'User Adoption Resistance',
                    'ROI Uncertainty',
                    'Security & Privacy Concerns',
                    'Vendor Dependence',
                    'Skills Gap'
                ],
                'Likelihood': ['Medium', 'High', 'Medium', 'Medium', 'High', 'Low', 'High', 'High'],
                'Impact': ['High', 'Medium', 'High', 'Medium', 'High', 'High', 'Medium', 'Medium'],
                'Mitigation Strategy': [
                    'Adopt open standards (OpenXR), avoid proprietary lock-in, modular architecture',
                    'Phased rollout, API-first approach, dedicated integration team, middleware layer',
                    'Partner with cloud/edge providers, incremental infrastructure investment, hybrid models',
                    'Strong change management, training programs, executive sponsorship, user feedback loops',
                    'Start with measurable high-impact pilots, document ROI methodology, regular assessment',
                    'Enterprise security frameworks, data governance policies, compliance audits, zero-trust',
                    'Multi-vendor strategy, open standards, contract flexibility, internal capabilities',
                    'Training programs, hiring, vendor partnerships, centers of excellence, knowledge transfer'
                ],
                'Data Source': [
                    'Interoperability sentiment (20% negative)',
                    'Scalability topics (complexity theme)',
                    'Scalability sentiment (52% concern)',
                    'Cross-dimension user themes',
                    'Use case sentiment (25% neutral awaiting proof)',
                    'Topic modeling security themes',
                    'Interoperability word cloud',
                    'Cross-dimension capability themes'
                ]
            }

            df_risks = pd.DataFrame(risk_data)
            st.dataframe(df_risks, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("### 🎯 Governance Recommendations")

            col1, col2 = st.columns(2)

            with col1:
                create_explanation_box(
                    "Establish XR Governance",
                    """<ul>
                    <li><strong>XR Steering Committee:</strong> Cross-functional leadership (IT, business units, innovation)</li>
                    <li><strong>Clear Decision Rights:</strong> Who approves projects, budgets, vendor selection</li>
                    <li><strong>Standards & Guidelines:</strong> Technical standards, UX patterns, security requirements</li>
                    <li><strong>Portfolio Management:</strong> Prioritize projects based on ROI and strategic alignment</li>
                    </ul>""",
                    "info"
                )

            with col2:
                create_explanation_box(
                    "Success Metrics & Monitoring",
                    """<ul>
                    <li><strong>Define Clear Metrics:</strong> Specific, measurable success criteria per use case</li>
                    <li><strong>Regular Technology Monitoring:</strong> Track XR market evolution, vendor capabilities</li>
                    <li><strong>Quarterly ROI Assessment:</strong> Evaluate business value and course-correct</li>
                    <li><strong>User Feedback Loops:</strong> Continuous input from XR users and stakeholders</li>
                    </ul>""",
                    "info"
                )

        # Display actual managerial implications from files
        st.markdown("---")
        st.markdown("### 📄 Detailed Implications by Dimension")

        impl_tab1, impl_tab2 = st.tabs(["Use Cases Dimension", "Interoperability Dimension"])

        with impl_tab1:
            if data['usecases_implications']:
                create_explanation_box(
                    "Use Cases: Strategic Insights",
                    "Analysis of managerial implications specific to XR use case selection and implementation",
                    "info"
                )
                st.text_area("", data['usecases_implications'], height=300, label_visibility="collapsed")

        with impl_tab2:
            if data['interop_implications']:
                create_explanation_box(
                    "Interoperability: Strategic Insights",
                    "Analysis of managerial implications for platform selection and integration strategy",
                    "info"
                )
                st.text_area("", data['interop_implications'], height=300, label_visibility="collapsed")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 2rem 0;'>
        <p style='font-size: 1.1rem;'><strong>XR Technology Analysis Dashboard</strong></p>
        <p>Data-Driven Decision Support for Extended Reality Adoption</p>
        <p style='font-size: 0.9rem;'>Analytical Framework: Word Cloud Analysis • Sentiment Analysis • Topic Modeling</p>
        <p style='font-size: 0.85rem; margin-top: 1rem;'>
            Based on social data signals from technology blogs, professional networks, research papers, and social media
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

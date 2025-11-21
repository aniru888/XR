"""
XR Technology Readiness Dashboard
Main Entry Point - Executive Context Landing Page
"""
import streamlit as st
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "config"))
sys.path.insert(0, str(Path(__file__).parent.parent / "analysis" / "common"))

from dimensions import (
    ALL_DIMENSIONS,
    get_overall_readiness,
    get_data_summary,
    ANALYTICAL_FRAMEWORK,
    COLORS
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="XR Technology Readiness Dashboard",
    page_icon="🥽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Professional Design
st.markdown(f"""
<style>
    /* ============================================================
       DESIGN SYSTEM - Modern Professional Theme
       ============================================================ */

    /* Smooth Scroll & Base Animations */
    html {{
        scroll-behavior: smooth;
    }}

    * {{
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    /* Color Palette */
    :root {{
        --primary-blue: {COLORS['primary_blue']};
        --accent-teal: {COLORS['accent_teal']};
        --success-green: {COLORS['success_green']};
        --warning-amber: {COLORS['warning_amber']};
        --alert-red: {COLORS['alert_red']};
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
        --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.15);
    }}

    /* ============================================================
       TYPOGRAPHY - Professional Hierarchy
       ============================================================ */

    .main h1 {{
        color: {COLORS['primary_blue']};
        font-weight: 700;
        font-size: 2.5rem;
        letter-spacing: -0.02em;
        border-bottom: 3px solid {COLORS['accent_teal']};
        padding-bottom: 12px;
        margin-bottom: 1.5rem;
        animation: fadeInDown 0.6s ease-out;
    }}

    .main h2 {{
        color: {COLORS['primary_blue']};
        font-weight: 600;
        font-size: 1.875rem;
        letter-spacing: -0.01em;
        margin-top: 2.5rem;
        margin-bottom: 1.25rem;
        animation: fadeInLeft 0.5s ease-out;
    }}

    .main h3 {{
        color: #2c3e50;
        font-weight: 600;
        font-size: 1.5rem;
        margin-top: 1.5rem;
        animation: fadeIn 0.5s ease-out;
    }}

    /* ============================================================
       CARDS & CONTAINERS - Modern Depth
       ============================================================ */

    /* Framework Table Container */
    .framework-table {{
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(0, 102, 204, 0.1);
        box-shadow: var(--shadow-sm);
        margin: 24px 0;
        animation: fadeInUp 0.6s ease-out;
    }}

    .framework-table:hover {{
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }}

    /* Metric Cards - Enhanced Design */
    div[data-testid="metric-container"] {{
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e8eaf0;
        box-shadow: var(--shadow-sm);
        animation: fadeInUp 0.5s ease-out;
    }}

    div[data-testid="metric-container"]:hover {{
        box-shadow: var(--shadow-md);
        transform: translateY(-3px);
        border-color: {COLORS['accent_teal']};
    }}

    /* Data Tables - Modern Look */
    div[data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        animation: fadeIn 0.6s ease-out;
    }}

    div[data-testid="stDataFrame"]:hover {{
        box-shadow: var(--shadow-md);
    }}

    /* ============================================================
       SIDEBAR - Professional Navigation
       ============================================================ */

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['primary_blue']} 0%, #0a3d5c 100%);
        box-shadow: 2px 0 16px rgba(0, 0, 0, 0.1);
    }}

    section[data-testid="stSidebar"] .stMarkdown {{
        color: white;
        animation: fadeIn 0.5s ease-out;
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: white !important;
    }}

    /* Sidebar Hover Effects */
    section[data-testid="stSidebar"] .stMarkdown:hover {{
        opacity: 0.9;
    }}

    /* ============================================================
       CONTENT BOXES - Refined Design
       ============================================================ */

    /* Quote Boxes */
    .quote-box {{
        background: linear-gradient(135deg, rgba(227, 242, 253, 0.6) 0%, rgba(187, 222, 251, 0.8) 100%);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 12px;
        border-left: 4px solid {COLORS['primary_blue']};
        border-right: 1px solid rgba(0, 102, 204, 0.1);
        border-top: 1px solid rgba(0, 102, 204, 0.1);
        border-bottom: 1px solid rgba(0, 102, 204, 0.1);
        margin: 20px 0;
        font-style: italic;
        color: #1a1a1a;
        box-shadow: var(--shadow-sm);
        animation: fadeInUp 0.5s ease-out;
    }}

    .quote-box:hover {{
        box-shadow: var(--shadow-md);
        transform: translateX(4px);
        border-left-width: 6px;
    }}

    .quote-box strong {{
        color: {COLORS['primary_blue']};
        font-size: 1.1em;
        font-weight: 700;
        letter-spacing: 0.01em;
    }}

    /* Data Quality Badge */
    .quality-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {COLORS['success_green']} 0%, #1e7e34 100%);
        color: white;
        padding: 8px 20px;
        border-radius: 24px;
        font-weight: 600;
        font-size: 0.9em;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
        animation: fadeIn 0.6s ease-out;
    }}

    .quality-badge:hover {{
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
    }}

    /* ============================================================
       BUTTONS & INTERACTIVE ELEMENTS
       ============================================================ */

    button[kind="primary"] {{
        background: linear-gradient(135deg, {COLORS['primary_blue']} 0%, #004d99 100%);
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        box-shadow: var(--shadow-sm);
    }}

    button[kind="primary"]:hover {{
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }}

    /* Expander Styling */
    div[data-testid="stExpander"] {{
        background: #ffffff;
        border: 1px solid #e8eaf0;
        border-radius: 12px;
        box-shadow: var(--shadow-sm);
        margin: 16px 0;
    }}

    div[data-testid="stExpander"]:hover {{
        box-shadow: var(--shadow-md);
        border-color: {COLORS['accent_teal']};
    }}

    /* ============================================================
       ANIMATIONS - Subtle & Professional
       ============================================================ */

    @keyframes fadeIn {{
        from {{
            opacity: 0;
        }}
        to {{
            opacity: 1;
        }}
    }}

    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes fadeInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}

    /* ============================================================
       RESPONSIVE POLISH
       ============================================================ */

    /* Smooth Focus States */
    *:focus {{
        outline: 2px solid {COLORS['accent_teal']};
        outline-offset: 2px;
    }}

    /* Link Styling */
    a {{
        color: {COLORS['primary_blue']};
        text-decoration: none;
        font-weight: 500;
        border-bottom: 1px solid transparent;
    }}

    a:hover {{
        border-bottom-color: {COLORS['primary_blue']};
        opacity: 0.8;
    }}

    /* Column Gap Refinement */
    div[data-testid="column"] {{
        padding: 8px;
    }}

    /* Tabs Modern Look */
    button[data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }}

    button[data-baseweb="tab"]:hover {{
        background: rgba(0, 102, 204, 0.05);
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("# 🥽 XR Dashboard")
    st.markdown("---")

    st.markdown("### 📊 Five-Dimension Framework")
    st.markdown("""
    Navigate to individual dimension analyses:
    """)

    for dim in ALL_DIMENSIONS:
        st.markdown(f"{dim.icon} **{dim.name}**")
        st.caption(f"{dim.readiness_color} {dim.readiness_score}%")

    st.markdown("---")

    # Overall readiness
    readiness = get_overall_readiness()
    st.metric(
        "Overall Readiness",
        f"{readiness['average_score']:.0f}%",
        help="Average readiness across all 5 dimensions"
    )
    st.caption(f"{readiness['status']}")

    st.markdown("---")
    st.caption("Data updated: 2024-2025")
    st.caption("Sources: 591 verified URLs")

# ============================================================================
# MAIN CONTENT - EXECUTIVE CONTEXT
# ============================================================================

# Hero Section
st.markdown("# 🎯 Extended Reality (XR) Technology Readiness")
st.markdown("### Executive Strategic Assessment Framework")

st.markdown("""
<div style='background: linear-gradient(135deg, #0066CC 0%, #00C9A7 100%);
            color: white; padding: 20px; border-radius: 10px; margin: 20px 0;'>
    <h3 style='color: white; margin: 0;'>🧭 Strategic Question</h3>
    <p style='font-size: 1.2em; margin: 10px 0 0 0;'>
        In an AI-native enterprise increasingly dependent on data intelligence,
        which emerging technologies deserve strategic investment for sustainable competitive advantage?
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FIVE-DIMENSION FRAMEWORK
# ============================================================================

st.markdown("## 📐 The Five-Dimension Analytical Framework")

st.markdown("""
This dashboard evaluates Extended Reality (XR) technology—encompassing Virtual Reality (VR),
Augmented Reality (AR), and Mixed Reality (MR)—through a comprehensive five-dimension lens
to determine its readiness for enterprise deployment.
""")

# Framework Table
framework_df_data = []
for dim in ALL_DIMENSIONS:
    framework_df_data.append({
        "Dimension": f"{dim.icon} {dim.name}",
        "Purpose": dim.purpose,
        "Readiness": f"{dim.readiness_color} {dim.readiness_score}%"
    })

import pandas as pd
framework_df = pd.DataFrame(framework_df_data)

st.markdown('<div class="framework-table">', unsafe_allow_html=True)
st.dataframe(
    framework_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Dimension": st.column_config.TextColumn("Dimension", width="medium"),
        "Purpose": st.column_config.TextColumn("Purpose", width="large"),
        "Readiness": st.column_config.TextColumn("Readiness", width="small")
    }
)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# LEADERSHIP PERSPECTIVE
# ============================================================================

st.markdown("## 💡 Leadership Perspective")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="quote-box">
        <strong>📚 Azeem Azhar's Vision</strong><br/>
        <em>"The exponential age demands that businesses adopt technologies that
        fundamentally reshape operations, not just incrementally improve them."</em>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="quote-box">
        <strong>🤖 Ananya Srivastava's Framework</strong><br/>
        <em>"AI-native enterprises must evaluate technologies through multiple lenses:
        maturity, compatibility, scalability, and strategic alignment."</em>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# METHODOLOGY
# ============================================================================

st.markdown("## 🔬 Analytical Methodology")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📊 Word Cloud Analysis**
    - Pre-trained NLP models
    - Identifies dominant themes
    - Visualizes key concepts
    - Highlights industry focus
    """)

with col2:
    st.markdown("""
    **😊 Sentiment Analysis**
    - TextBlob polarity scoring
    - Positive/Neutral/Negative classification
    - Industry optimism assessment
    - Risk signal detection
    """)

with col3:
    st.markdown("""
    **🎯 Topic Modeling (LDA)**
    - Latent Dirichlet Allocation
    - Unsupervised theme extraction
    - Cross-dimensional patterns
    - Strategic insight generation
    """)

# ============================================================================
# DATA QUALITY & SOURCES
# ============================================================================

st.markdown("## 📚 Data Quality & Verification")

summary = get_data_summary()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Dimensions Analyzed",
        summary['total_dimensions'],
        help="Five comprehensive dimensions"
    )

with col2:
    st.metric(
        "Total Entries",
        f"{summary['total_entries']:,}",
        help="Data points across all dimensions"
    )

with col3:
    st.metric(
        "Verified URLs",
        summary['total_verified_urls'],
        delta="Real articles, not homepages",
        help="All sources return 200 OK status"
    )

with col4:
    st.metric(
        "Data Period",
        "2020-2025",
        help="Recent and relevant industry data"
    )

st.markdown('<span class="quality-badge">✓ All URLs Verified | ✓ Real Articles | ✓ No Synthetic Data</span>', unsafe_allow_html=True)

# ============================================================================
# DIMENSION BREAKDOWN
# ============================================================================

st.markdown("## 📊 Dimension-Specific Data")

dimension_data = []
for dim in ALL_DIMENSIONS:
    dimension_data.append({
        "Dimension": f"{dim.icon} {dim.name}",
        "Entries": f"{dim.entry_count:,}",
        "Sources": len(dim.get_source_paths()),
        "Readiness": dim.readiness_score,  # Numeric value for progress bar
        "Status": dim.readiness_color,
        "Key Finding": dim.key_finding
    })

dimension_df = pd.DataFrame(dimension_data)

st.dataframe(
    dimension_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Dimension": st.column_config.TextColumn("Dimension", width="medium"),
        "Entries": st.column_config.TextColumn("Entries", width="small"),
        "Sources": st.column_config.TextColumn("Source Files", width="small"),
        "Readiness": st.column_config.ProgressColumn(
            "Readiness",
            format="%d%%",  # Display as percentage
            min_value=0,
            max_value=100
        ),
        "Status": st.column_config.TextColumn("Status", width="small"),
        "Key Finding": st.column_config.TextColumn("Key Finding", width="large")
    }
)

# ============================================================================
# ANALYTICAL FRAMEWORK METADATA
# ============================================================================

st.markdown("## 🔍 Framework Details")

with st.expander("📋 View Complete Framework Metadata"):
    st.markdown(f"**Title:** {ANALYTICAL_FRAMEWORK['title']}")
    st.markdown(f"**Description:** {ANALYTICAL_FRAMEWORK['description']}")

    st.markdown("**Methodology Components:**")
    for method in ANALYTICAL_FRAMEWORK['methodology']:
        st.markdown(f"- **{method['name']}:** {method['description']}")

    st.markdown("**Data Quality:**")
    dq = ANALYTICAL_FRAMEWORK['data_quality']
    st.markdown(f"- Verified URLs: {dq['total_verified_urls']}")
    st.markdown(f"- Verification Status: {dq['verification_status']}")
    st.markdown(f"- Publication Period: {dq['publication_period']}")

# ============================================================================
# NAVIGATION GUIDE
# ============================================================================

st.markdown("## 🧭 How to Navigate This Dashboard")

st.markdown("""
1. **📍 Start Here (Executive Context)** - Understand the framework and methodology
2. **📊 Explore Each Dimension** - Use the sidebar to navigate to individual analyses
3. **🔍 Review Analytics** - Each dimension shows Word Cloud, Sentiment, and Topics
4. **📚 Verify Sources** - All dimensions include verified source URLs
5. **🎯 Strategic Synthesis** - Review cross-dimensional insights and recommendations

---

### 🚀 Ready to Begin?

Use the sidebar to navigate to any of the five dimensions. Each page provides:
- **Framework Purpose** - The strategic question being answered
- **Visual Analytics** - Word clouds, sentiment charts, topic models
- **Verified Sources** - Real articles with working URLs
- **Managerial Implications** - Actionable insights for decision-makers
""")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D; padding: 20px;'>
    <p><strong>XR Technology Readiness Dashboard</strong></p>
    <p>Analytical Framework for Strategic Technology Assessment</p>
    <p>Data Sources: 591 Verified URLs | Analysis Period: 2020-2025</p>
</div>
""", unsafe_allow_html=True)

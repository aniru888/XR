"""
Scalability Dimension
Capacity to deliver enterprise-grade solutions
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "config"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "analysis" / "common"))

from dimensions import get_dimension_by_id, COLORS
from data_loader import load_dimension
from text_analytics import WordCloudGenerator, SentimentAnalyzer, TopicModeler

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Scalability | XR Dashboard",
    page_icon="⚡",
    layout="wide"
)

# Load dimension configuration
dimension = get_dimension_by_id('scalability')
if not dimension:
    st.error("Failed to load dimension configuration")
    st.stop()

# Load data
try:
    data = load_dimension('scalability')
    corpus = data['corpus']
    text = data['text']
    sources = data['sources']
except Exception as e:
    st.error(f"Failed to load dimension data: {e}")
    st.stop()

# ============================================================================
# DIMENSION HEADER
# ============================================================================

st.markdown(f"# {dimension.icon} {dimension.name}")

st.markdown(f"""
<div style='background: linear-gradient(135deg, {COLORS['primary_blue']} 0%, {COLORS['accent_teal']} 100%);
            color: white; padding: 20px; border-radius: 10px; margin: 20px 0;'>
    <h3 style='color: white; margin: 0;'>📐 Framework Purpose</h3>
    <p style='font-size: 1.2em; margin: 10px 0 0 0;'>{dimension.purpose}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='background: #f8f9fa; padding: 15px; border-left: 5px solid {COLORS['accent_teal']};
            border-radius: 5px; margin: 20px 0;'>
    <strong>🔍 Analysis Question:</strong><br/>
    {dimension.question}
</div>
""", unsafe_allow_html=True)

# ============================================================================
# KEY METRICS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Readiness Score", f"{dimension.readiness_score}%")
    st.caption(dimension.readiness_color)

with col2:
    st.metric("Data Entries", f"{dimension.entry_count:,}")

with col3:
    st.metric("Verified URLs", len(sources))

with col4:
    st.metric("Infrastructure Stack", "5 Layers")

# ============================================================================
# KEY FINDING
# ============================================================================

st.markdown(f"""
<div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['primary_blue']};
            margin: 20px 0;'>
    <h4 style='margin: 0; color: {COLORS["primary_blue"]};'>💡 Key Finding</h4>
    <p style='font-size: 1.1em; margin: 10px 0 0 0; color: #1a1a1a;'>{dimension.key_finding}</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# INFRASTRUCTURE BREAKDOWN
# ============================================================================

st.markdown("## 🏗️ Infrastructure Stack Analysis")

st.markdown("""
Scalability of XR requires a comprehensive infrastructure stack spanning from network layer to device management:
""")

stack_data = [
    {
        "Layer": "🌐 5G/6G Network",
        "Purpose": "Low-latency wireless connectivity",
        "Key Vendors": "Nokia, Verizon, Ericsson, Qualcomm",
        "Entries": "~120"
    },
    {
        "Layer": "🖥️ Edge Computing",
        "Purpose": "Distributed processing near users",
        "Key Vendors": "Cloudflare, Akamai, VMware",
        "Entries": "~120"
    },
    {
        "Layer": "☁️ Cloud Rendering",
        "Purpose": "Remote rendering and streaming",
        "Key Vendors": "AWS, Azure, Google, NVIDIA",
        "Entries": "~120"
    },
    {
        "Layer": "📱 Device Management",
        "Purpose": "Fleet management and provisioning",
        "Key Vendors": "Microsoft Intune, Jamf, MongoDB",
        "Entries": "~120"
    },
    {
        "Layer": "🔧 Infrastructure Tools",
        "Purpose": "Orchestration and deployment",
        "Key Vendors": "Kubernetes, Docker, Okta",
        "Entries": "~120"
    }
]

stack_df = pd.DataFrame(stack_data)
st.dataframe(stack_df, use_container_width=True, hide_index=True)

# ============================================================================
# TEXT ANALYTICS
# ============================================================================

st.markdown("---")
st.markdown("## 📊 Text Analytics")

# Load pre-computed analytics from data files
analytics_path = dimension.get_data_paths()[0].parent  # XR scalability directory
sentiment_file = analytics_path / "XR_Sentiment_Analysis_Results.csv"
topics_file = analytics_path / "XR_LDA_Topic_Distribution.csv"

if text and len(text.strip()) > 100:

    # Word Cloud
    st.markdown("### 📊 Word Cloud Analysis")
    try:
        wc_gen = WordCloudGenerator(width=1200, height=600)
        wordcloud = wc_gen.generate(text, max_words=100, colormap='inferno')

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Infrastructure Themes in XR Scalability', fontsize=16, fontweight='bold', pad=20)
        st.pyplot(fig)

        col1, col2 = st.columns([2, 1])
        with col1:
            top_words = wc_gen.get_top_words(text, n=20)
            top_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
            st.dataframe(top_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Infrastructure Focus:**")
            if top_words:
                st.markdown(f"- Core technology: **{top_words[0][0]}**")
                st.markdown("- Reveals bottlenecks")
                st.markdown("- Shows vendor priorities")
    except Exception as e:
        st.warning(f"Word cloud generation failed: {e}")

    # Sentiment Analysis
    st.markdown("---")
    st.markdown("### 😊 Sentiment Analysis")
    try:
        if sentiment_file.exists():
            # Load pre-computed sentiment results
            sentiment_df = pd.read_csv(sentiment_file)

            # Calculate summary statistics from global_sentiment_score
            avg_sentiment = sentiment_df['global_sentiment_score'].mean()
            sentiment_counts = sentiment_df['global_sentiment_class'].value_counts()
            total = len(sentiment_df)

            pos_pct = (sentiment_counts.get('Positive', 0) / total) * 100
            neu_pct = (sentiment_counts.get('Neutral', 0) / total) * 100
            neg_pct = (sentiment_counts.get('Negative', 0) / total) * 100

            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg Sentiment", f"{avg_sentiment:.3f}")
            with col2:
                st.metric("Positive", f"{pos_pct:.1f}%",
                         delta=f"{sentiment_counts.get('Positive', 0)} records",
                         delta_color="off")
            with col3:
                st.metric("Neutral", f"{neu_pct:.1f}%",
                         delta=f"{sentiment_counts.get('Neutral', 0)} records",
                         delta_color="off")
            with col4:
                st.metric("Negative", f"{neg_pct:.1f}%",
                         delta=f"{sentiment_counts.get('Negative', 0)} records",
                         delta_color="off")

            # Show detailed sentiment breakdown
            with st.expander("📊 View Detailed Sentiment by Infrastructure Layer"):
                display_df = sentiment_df[['aspect', 'category', 'global_sentiment_score', 'global_sentiment_class']].copy()
                display_df.columns = ['Aspect', 'Category', 'Sentiment Score', 'Classification']
                st.dataframe(
                    display_df.head(50),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Sentiment Score": st.column_config.NumberColumn(
                            "Sentiment Score",
                            format="%.3f",
                            help="Compound sentiment score (-1 to +1)"
                        )
                    }
                )
        else:
            st.info("Pre-computed sentiment analysis not available.")
    except Exception as e:
        st.warning(f"Sentiment analysis display failed: {e}")

    # Topic Modeling
    st.markdown("---")
    st.markdown("### 🎯 Topic Modeling (LDA)")
    try:
        if topics_file.exists():
            # Load pre-computed topic distribution
            lda_df = pd.read_csv(topics_file)

            st.markdown("**Infrastructure Layer Topics:**")
            st.markdown("")

            # Display topic distribution summary
            topic_cols = [col for col in lda_df.columns if col.startswith('Topic_')]
            if topic_cols:
                # Calculate average distribution across all documents
                topic_avgs = {}
                for col in topic_cols:
                    topic_avgs[col] = lda_df[col].mean()

                # Create topic boxes with distribution
                topic_names = {
                    'Topic_1': '5G/6G Connectivity & Network',
                    'Topic_2': 'Edge Computing & Processing',
                    'Topic_3': 'Cloud Rendering & Streaming'
                }

                for i, (topic_col, avg_prob) in enumerate(sorted(topic_avgs.items(), key=lambda x: x[1], reverse=True)[:3], 1):
                    topic_name = topic_names.get(topic_col, f"Infrastructure Theme {i}")
                    prob_pct = avg_prob * 100

                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                                padding: 15px; border-radius: 8px; border-left: 4px solid {COLORS['accent_teal']};
                                margin: 10px 0;'>
                        <h4 style='margin: 0 0 8px 0; color: {COLORS["primary_blue"]};'>
                            🔸 {topic_name}
                        </h4>
                        <p style='margin: 0; color: #1a1a1a; font-size: 0.95em;'>
                            <strong>Document Coverage:</strong> {prob_pct:.1f}% average
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                # Show distribution table
                with st.expander("📊 View Topic Distribution Details"):
                    st.dataframe(
                        lda_df[topic_cols].head(20),
                        use_container_width=True,
                        column_config={col: st.column_config.NumberColumn(col, format="%.3f") for col in topic_cols}
                    )
        else:
            st.info("Pre-computed topic modeling not available.")
    except Exception as e:
        st.warning(f"Topic modeling display failed: {e}")

else:
    st.info("Limited text data available for analytics")

# ============================================================================
# DATA SOURCES
# ============================================================================

st.markdown("---")
st.markdown("## 📚 Verified Data Sources")

st.markdown(f"**{len(sources)} verified URLs** from infrastructure vendors:")

source_categories = {
    "Network Operators": ["nokia", "verizon", "ericsson", "qualcomm"],
    "Cloud Platforms": ["aws", "azure", "microsoft", "google"],
    "Edge Providers": ["cloudflare", "akamai", "vmware"],
    "Infrastructure Tools": ["kubernetes", "nvidia", "mongodb", "okta", "jamf"]
}

for category, keywords in source_categories.items():
    category_sources = [s for s in sources if any(kw in s.lower() for kw in keywords)]
    if category_sources:
        with st.expander(f"📁 {category} ({len(category_sources)} sources)"):
            for i, url in enumerate(category_sources, 1):
                st.markdown(f"{i}. [{url}]({url})")

# ============================================================================
# MANAGERIAL IMPLICATIONS
# ============================================================================

st.markdown("---")
st.markdown("## 💼 Managerial Implications")

st.markdown("""
**Scalability Requirements:**

- 📡 **Network:** 5G/6G connectivity for low-latency streaming (< 20ms)
- 🖥️ **Edge:** Distributed compute to reduce cloud dependency
- ☁️ **Cloud:** Elastic rendering capacity for peak demand
- 📱 **Device Management:** Enterprise-grade MDM for fleet control
- 🔧 **Orchestration:** Container-based deployment (Kubernetes)

**Critical Success Factors:**

1. **Hybrid Architecture:** Combine edge + cloud for cost-performance balance
2. **Vendor Partnerships:** Engage with Nokia/Verizon for 5G, AWS/Azure for cloud
3. **Pilot Sizing:** Start with 50-100 devices to validate infrastructure
4. **Bandwidth Planning:** Budget for 10-50 Mbps per active XR device
5. **Monitoring Stack:** Real-time observability for latency and quality metrics

**Cost Considerations:**

- Network: $50-200/device/month (5G connectivity)
- Cloud Rendering: $0.10-1.00/hour per stream
- Edge Infrastructure: $10K-100K capex per edge location
- Device Management: $5-15/device/month
""")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D; padding: 20px;'>
    <p><strong>Scalability Analysis</strong></p>
    <p>Part of the Five-Dimension XR Technology Readiness Framework</p>
</div>
""", unsafe_allow_html=True)

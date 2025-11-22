"""
Alignment to Data Intelligence Dimension
Synergy with AI, analytics, and decision systems
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
    page_title="AI Alignment | XR Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Load dimension configuration
dimension = get_dimension_by_id('ai_alignment')
if not dimension:
    st.error("Failed to load dimension configuration")
    st.stop()

# Load data
try:
    data = load_dimension('ai_alignment')
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
    st.metric("AI Integration", "High Potential")

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
# AI-XR SYNERGY MATRIX
# ============================================================================

st.markdown("## 🔗 AI-XR Synergy Matrix")

st.markdown("""
XR and AI create powerful synergies across multiple enterprise functions:
""")

synergy_data = [
    {
        "AI Capability": "🧠 Computer Vision",
        "XR Integration": "Spatial mapping, object recognition",
        "Enterprise Use": "Quality inspection, asset tracking",
        "Maturity": "🟢 Production-ready"
    },
    {
        "AI Capability": "🗣️ Natural Language",
        "XR Integration": "Voice commands, conversational UI",
        "Enterprise Use": "Hands-free operation, training",
        "Maturity": "🟢 Production-ready"
    },
    {
        "AI Capability": "🤖 Machine Learning",
        "XR Integration": "Predictive analytics, personalization",
        "Enterprise Use": "Maintenance predictions, adaptive training",
        "Maturity": "🟡 Pilot-stage"
    },
    {
        "AI Capability": "🎨 Generative AI",
        "XR Integration": "Content generation, simulation",
        "Enterprise Use": "Rapid prototyping, scenario planning",
        "Maturity": "🟡 Emerging"
    },
    {
        "AI Capability": "📊 Data Analytics",
        "XR Integration": "Real-time visualization, dashboards",
        "Enterprise Use": "Executive analytics, spatial BI",
        "Maturity": "🟡 Pilot-stage"
    }
]

synergy_df = pd.DataFrame(synergy_data)
st.dataframe(synergy_df, use_container_width=True, hide_index=True)

# ============================================================================
# TEXT ANALYTICS (Pre-computed from CSV files)
# ============================================================================

st.markdown("---")
st.markdown("## 📊 Text Analytics")

# Load pre-computed analytics from CSV files
analytics_path = dimension.get_data_paths()[0].parent if dimension.get_data_paths() else None
sentiment_file = analytics_path / "xr_ai_alignment_sentiment.csv" if analytics_path else None
topics_file = analytics_path / "xr_ai_alignment_topics.csv" if analytics_path else None
wordcloud_img = analytics_path / "xr_ai_alignment_wordcloud.png" if analytics_path else None
sentiment_img = analytics_path / "xr_ai_alignment_sentiment_distribution.png" if analytics_path else None
top_words_file = analytics_path / "xr_ai_alignment_top_words.csv" if analytics_path else None

# Word Cloud
st.markdown("### 📊 Word Cloud Analysis")
if wordcloud_img and wordcloud_img.exists():
    from PIL import Image
    st.image(str(wordcloud_img), use_container_width=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        if top_words_file and top_words_file.exists():
            top_words_df = pd.read_csv(top_words_file)
            top_words_df.columns = ['Word', 'Frequency']
            st.dataframe(top_words_df.head(20), use_container_width=True, hide_index=True)

    with col2:
        st.markdown("**AI Integration Points:**")
        if top_words_file and top_words_file.exists():
            top_word = top_words_df.iloc[0]['Word']
            st.markdown(f"- Primary focus: **{top_word}**")
            st.markdown("- Shows AI-XR convergence")
            st.markdown("- Highlights data flows")
else:
    st.info("Word cloud visualization not available")

# Sentiment Analysis
st.markdown("---")
st.markdown("### 😊 Sentiment Analysis")
if sentiment_file and sentiment_file.exists():
    sentiment_df = pd.read_csv(sentiment_file)

    # Calculate summary statistics
    avg_compound = sentiment_df['compound'].mean()
    sentiment_counts = sentiment_df['label'].value_counts()
    total = len(sentiment_df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Sentiment", f"{avg_compound:.3f}")
    with col2:
        positive_pct = (sentiment_counts.get('positive', 0) / total) * 100
        st.metric("Positive", f"{positive_pct:.1f}%", delta="55.4%")
    with col3:
        neutral_pct = (sentiment_counts.get('neutral', 0) / total) * 100
        st.metric("Neutral", f"{neutral_pct:.1f}%")
    with col4:
        negative_pct = (sentiment_counts.get('negative', 0) / total) * 100
        st.metric("Negative", f"{negative_pct:.1f}%")

    # Display sentiment distribution chart
    if sentiment_img and sentiment_img.exists():
        from PIL import Image
        st.image(str(sentiment_img), use_container_width=True)

    st.markdown("**Interpretation:**")
    if positive_pct > 50:
        st.success("🎯 Strong optimism about AI-XR convergence")
    else:
        st.info("⚖️ Balanced perspective on integration challenges")

    # Show detailed breakdown by source type
    with st.expander("📊 View Sentiment Details by Source Type"):
        source_type_sentiment = sentiment_df.groupby('source_type')['compound'].agg(['mean', 'count']).round(3)
        source_type_sentiment.columns = ['Average Sentiment', 'Number of Sources']
        st.dataframe(source_type_sentiment, use_container_width=True)
else:
    st.info("Sentiment analysis data not available")

# Topic Modeling
st.markdown("---")
st.markdown("### 🎯 Topic Modeling (LDA)")
if topics_file and topics_file.exists():
    topics_df = pd.read_csv(topics_file)

    st.markdown("**AI-XR Integration Themes:**")

    for idx, row in topics_df.iterrows():
        topic_name = row['topic']
        keywords = row['keywords']

        # Display topic with styled box
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                    padding: 15px; border-radius: 8px; margin: 10px 0;
                    border-left: 4px solid #3b82f6;'>
            <h4 style='margin: 0; color: #1e40af;'>{topic_name}</h4>
            <p style='margin: 5px 0 0 0; color: #1f2937;'><strong>Keywords:</strong> {keywords}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("**Key Themes Identified:**")
    st.markdown("- 🌐 **World Models**: AI systems that understand physics and causality")
    st.markdown("- 👓 **Hardware Evolution**: Vision Pro, Quest 3, and next-gen devices")
    st.markdown("- 🏭 **Digital Twins**: Industrial applications using spatial data")
else:
    st.info("Topic modeling data not available")

# ============================================================================
# DATA SOURCES
# ============================================================================

st.markdown("---")
st.markdown("## 📚 Verified Data Sources")

if sources and len(sources) > 0:
    st.markdown(f"**{len(sources)} verified URLs** analyzing AI-XR integration:")

    with st.expander("📖 View All Source URLs"):
        for i, url in enumerate(sources, 1):
            st.markdown(f"{i}. [{url}]({url})")

# ============================================================================
# MANAGERIAL IMPLICATIONS
# ============================================================================

st.markdown("---")
st.markdown("## 💼 Managerial Implications")

st.markdown("""
**AI-Native XR Strategy:**

- 🧠 **Computer Vision First:** Start with proven CV applications (quality inspection, spatial mapping)
- 🗣️ **Voice Integration:** Enable hands-free XR operation through NLP
- 📊 **Data Pipeline:** Build robust data flow from XR sensors to analytics platform
- 🤖 **ML Models:** Train custom models on XR-generated spatial data
- 🎨 **Generative AI:** Experiment with AI-generated XR content for training scenarios

**Integration Architecture:**

1. **Data Collection:** XR devices capture spatial, behavioral, environmental data
2. **Real-time Processing:** Edge AI for immediate feedback (safety alerts, guidance)
3. **Batch Analytics:** Cloud-based ML for pattern recognition and predictions
4. **Feedback Loop:** AI insights inform XR content and experiences

**Quick Wins:**

- ✅ Voice commands in hands-free environments (manufacturing, field service)
- ✅ Computer vision for quality inspection and defect detection
- ✅ Spatial analytics for warehouse optimization and layout planning

**Strategic Investments:**

- 🎯 Build proprietary training datasets from XR usage
- 🎯 Develop custom ML models for your specific workflows
- 🎯 Create AI-powered digital twins using XR-captured spatial data
""")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D; padding: 20px;'>
    <p><strong>AI Alignment Analysis</strong></p>
    <p>Part of the Five-Dimension XR Technology Readiness Framework</p>
</div>
""", unsafe_allow_html=True)

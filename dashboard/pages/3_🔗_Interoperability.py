"""
Interoperability Dimension
Compatibility with existing business and data ecosystems
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
    page_title="Interoperability | XR Dashboard",
    page_icon="🔗",
    layout="wide"
)

# Load dimension configuration
dimension = get_dimension_by_id('interoperability')
if not dimension:
    st.error("Failed to load dimension configuration")
    st.stop()

# Load data
try:
    data = load_dimension('interoperability')
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
    st.metric("Text Corpus", f"{len(text):,} chars")

# ============================================================================
# KEY FINDING
# ============================================================================

st.markdown(f"""
<div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['primary_blue']};
            margin: 20px 0;'>
    <h4 style='margin: 0;'>💡 Key Finding</h4>
    <p style='font-size: 1.1em; margin: 10px 0 0 0;'>{dimension.key_finding}</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# TEXT ANALYTICS
# ============================================================================

st.markdown("## 📊 Text Analytics")

if text and len(text.strip()) > 100:

    # Word Cloud
    st.markdown("### 📊 Word Cloud Analysis")
    try:
        wc_gen = WordCloudGenerator(width=1200, height=600)
        wordcloud = wc_gen.generate(text, max_words=100, colormap='plasma')

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Key Concepts in XR Interoperability', fontsize=16, fontweight='bold', pad=20)
        st.pyplot(fig)

        col1, col2 = st.columns([2, 1])
        with col1:
            top_words = wc_gen.get_top_words(text, n=20)
            top_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
            st.dataframe(top_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Integration Focus:**")
            if top_words:
                st.markdown(f"- Top theme: **{top_words[0][0]}**")
                st.markdown("- Shows compatibility priorities")
                st.markdown("- Highlights ecosystem gaps")
    except Exception as e:
        st.warning(f"Word cloud generation failed: {e}")

    # Sentiment Analysis
    st.markdown("---")
    st.markdown("### 😊 Sentiment Analysis")
    try:
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        if len(sentences) >= 5:
            analyzer = SentimentAnalyzer()
            sentiments = analyzer.analyze_corpus(sentences)
            summary = analyzer.get_summary_stats(sentiments)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg Polarity", f"{summary['avg_polarity']:.3f}")
            with col2:
                st.metric("Positive", f"{summary['positive_pct']:.1f}%")
            with col3:
                st.metric("Neutral", f"{summary['neutral_pct']:.1f}%")
            with col4:
                st.metric("Negative", f"{summary['negative_pct']:.1f}%")

            fig = analyzer.plot_distribution(sentiments, title="Sentiment - Interoperability Challenges")
            st.pyplot(fig)
    except Exception as e:
        st.warning(f"Sentiment analysis failed: {e}")

    # Topic Modeling
    st.markdown("---")
    st.markdown("### 🎯 Topic Modeling (LDA)")
    try:
        if len(sentences) >= 5:
            n_topics = min(3, len(sentences) // 3)
            modeler = TopicModeler(n_topics=n_topics)
            modeler.fit(sentences)
            labels = modeler.get_topic_labels(n_words=5)

            st.markdown("**Integration Themes:**")
            for topic_id, label in labels.items():
                st.markdown(f"- {label}")
    except Exception as e:
        st.warning(f"Topic modeling failed: {e}")

else:
    st.info("Limited text data available for analytics")

# ============================================================================
# DATA SOURCES
# ============================================================================

st.markdown("---")
st.markdown("## 📚 Verified Data Sources")

if sources and len(sources) > 0:
    st.markdown(f"**{len(sources)} verified URLs** analyzing XR interoperability standards:")

    with st.expander("📖 View All Source URLs"):
        for i, url in enumerate(sources, 1):
            st.markdown(f"{i}. [{url}]({url})")

# ============================================================================
# MANAGERIAL IMPLICATIONS
# ============================================================================

st.markdown("---")
st.markdown("## 💼 Managerial Implications")

st.markdown("""
**Interoperability Challenges:**

- 🔗 **Standards Fragmentation:** Multiple competing standards (OpenXR, WebXR, proprietary SDKs)
- 🔧 **Legacy System Integration:** Complex interfaces with existing enterprise systems
- 📊 **Data Pipeline Compatibility:** Need for seamless data flow with analytics platforms
- 🔒 **Security Protocols:** Authentication and authorization across XR and enterprise systems

**Strategic Recommendations:**

1. **Prioritize Open Standards:** Adopt OpenXR-compatible solutions where possible
2. **API-First Architecture:** Ensure XR solutions expose well-documented APIs
3. **Pilot Integration Tests:** Validate compatibility with your specific tech stack
4. **Vendor Roadmap Review:** Assess vendor commitment to standards evolution
""")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D; padding: 20px;'>
    <p><strong>Interoperability Analysis</strong></p>
    <p>Part of the Five-Dimension XR Technology Readiness Framework</p>
</div>
""", unsafe_allow_html=True)

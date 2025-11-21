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
    <h4 style='margin: 0;'>💡 Key Finding</h4>
    <p style='font-size: 1.1em; margin: 10px 0 0 0;'>{dimension.key_finding}</p>
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
# TEXT ANALYTICS
# ============================================================================

st.markdown("---")
st.markdown("## 📊 Text Analytics")

if text and len(text.strip()) > 100:

    # Word Cloud
    st.markdown("### 📊 Word Cloud Analysis")
    try:
        wc_gen = WordCloudGenerator(width=1200, height=600)
        wordcloud = wc_gen.generate(text, max_words=100, colormap='cool')

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('AI-XR Integration Themes', fontsize=16, fontweight='bold', pad=20)
        st.pyplot(fig)

        col1, col2 = st.columns([2, 1])
        with col1:
            top_words = wc_gen.get_top_words(text, n=20)
            top_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
            st.dataframe(top_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**AI Integration Points:**")
            if top_words:
                st.markdown(f"- Primary focus: **{top_words[0][0]}**")
                st.markdown("- Shows AI-XR convergence")
                st.markdown("- Highlights data flows")
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

            fig = analyzer.plot_distribution(sentiments, title="Sentiment - AI-XR Synergy")
            st.pyplot(fig)

            st.markdown("**Interpretation:**")
            if summary['positive_pct'] > 50:
                st.success("🎯 Strong optimism about AI-XR convergence")
            else:
                st.info("⚖️ Balanced perspective on integration challenges")
    except Exception as e:
        st.warning(f"Sentiment analysis failed: {e}")

    # Topic Modeling
    st.markdown("---")
    st.markdown("### 🎯 Topic Modeling (LDA)")
    try:
        if len(sentences) >= 5:
            n_topics = min(4, len(sentences) // 5)
            modeler = TopicModeler(n_topics=n_topics)
            modeler.fit(sentences)
            labels = modeler.get_topic_labels(n_words=5)

            st.markdown("**AI-XR Integration Themes:**")
            for topic_id, label in labels.items():
                st.markdown(f"- {label}")

            if n_topics > 1:
                fig = modeler.plot_topics(n_words=8, title="AI Alignment Topics")
                st.pyplot(fig)
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

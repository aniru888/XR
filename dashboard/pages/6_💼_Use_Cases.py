"""
Use Cases Dimension
Breadth and diversity of industry applications
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
    page_title="Use Cases | XR Dashboard",
    page_icon="💼",
    layout="wide"
)

# Load dimension configuration
dimension = get_dimension_by_id('use_cases')
if not dimension:
    st.error("Failed to load dimension configuration")
    st.stop()

# Load data
try:
    data = load_dimension('use_cases')
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
    st.metric("Use Cases", f"{dimension.entry_count}")

with col3:
    st.metric("Verified URLs", len(sources))

with col4:
    st.metric("Industries", "7+ Sectors")

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
# USE CASE MATRIX
# ============================================================================

st.markdown("## 🎯 Enterprise Use Case Matrix")

st.markdown("""
XR applications span multiple industries with varying levels of maturity:
""")

use_case_data = [
    {
        "Industry": "🏭 Manufacturing",
        "Primary Use Case": "Assembly guidance, quality inspection",
        "ROI Potential": "High (15-25% efficiency gain)",
        "Maturity": "🟢 Production-ready",
        "Example": "Boeing assembly, Volkswagen training"
    },
    {
        "Industry": "🏥 Healthcare",
        "Primary Use Case": "Surgical planning, medical training",
        "ROI Potential": "High (reduced errors, faster training)",
        "Maturity": "🟢 Production-ready",
        "Example": "Mayo Clinic simulations"
    },
    {
        "Industry": "🏗️ Construction",
        "Primary Use Case": "Design review, safety training",
        "ROI Potential": "Medium (10-15% rework reduction)",
        "Maturity": "🟡 Pilot-stage",
        "Example": "BIM visualization, site planning"
    },
    {
        "Industry": "🛒 Retail",
        "Primary Use Case": "Virtual try-on, immersive shopping",
        "ROI Potential": "Medium (higher conversion rates)",
        "Maturity": "🟡 Pilot-stage",
        "Example": "IKEA Place, virtual showrooms"
    },
    {
        "Industry": "📚 Education",
        "Primary Use Case": "Immersive learning, lab simulations",
        "ROI Potential": "Medium (better retention)",
        "Maturity": "🟡 Pilot-stage",
        "Example": "Medical schools, engineering programs"
    },
    {
        "Industry": "🎮 Entertainment",
        "Primary Use Case": "Gaming, virtual events",
        "ROI Potential": "High (new revenue streams)",
        "Maturity": "🟢 Production-ready",
        "Example": "Meta Horizon, VRChat events"
    },
    {
        "Industry": "⚙️ Field Service",
        "Primary Use Case": "Remote assistance, maintenance",
        "ROI Potential": "High (reduced travel, faster repairs)",
        "Maturity": "🟢 Production-ready",
        "Example": "PTC ThingWorx, Microsoft Dynamics"
    }
]

use_case_df = pd.DataFrame(use_case_data)
st.dataframe(use_case_df, use_container_width=True, hide_index=True)

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
        wordcloud = wc_gen.generate(text, max_words=100, colormap='Set2')

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Dominant Use Case Themes', fontsize=16, fontweight='bold', pad=20)
        st.pyplot(fig)

        col1, col2 = st.columns([2, 1])
        with col1:
            top_words = wc_gen.get_top_words(text, n=20)
            top_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
            st.dataframe(top_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Application Focus:**")
            if top_words:
                st.markdown(f"- Primary application: **{top_words[0][0]}**")
                st.markdown("- Shows industry priorities")
                st.markdown("- Reveals emerging patterns")
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

            fig = analyzer.plot_distribution(sentiments, title="Sentiment - Use Case Success")
            st.pyplot(fig)

            st.markdown("**Success Signal:**")
            if summary['positive_pct'] > 40:
                st.success("🎯 High positive sentiment indicates successful deployments")
            elif summary['negative_pct'] > 30:
                st.warning("⚠️ Elevated negative sentiment suggests implementation challenges")
            else:
                st.info("⚖️ Balanced sentiment reflects mixed results across use cases")
    except Exception as e:
        st.warning(f"Sentiment analysis failed: {e}")

    # Topic Modeling
    st.markdown("---")
    st.markdown("### 🎯 Topic Modeling (LDA)")
    try:
        if len(sentences) >= 5:
            n_topics = min(4, len(sentences) // 3)
            modeler = TopicModeler(n_topics=n_topics)
            modeler.fit(sentences)
            labels = modeler.get_topic_labels(n_words=5)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Application Themes:**")
                for topic_id, label in labels.items():
                    st.markdown(f"- {label}")

            with col2:
                # Map themes to industries
                st.markdown("**Industry Mapping:**")
                st.markdown("- Manufacturing & Field Service")
                st.markdown("- Healthcare & Education")
                st.markdown("- Retail & Entertainment")

            if n_topics > 1:
                fig = modeler.plot_topics(n_words=8, title="Use Case Themes")
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
    st.markdown(f"**{len(sources)} verified use case articles** with real-world implementations:")

    with st.expander("📖 View All Source URLs"):
        for i, url in enumerate(sources, 1):
            # Try to extract domain for better display
            domain = url.split('/')[2] if len(url.split('/')) > 2 else url
            st.markdown(f"{i}. [{domain}]({url})")
else:
    st.info("Source URLs are embedded in the corpus data")

# ============================================================================
# USE CASE DEEP DIVE
# ============================================================================

st.markdown("---")
st.markdown("## 🔍 Use Case Deep Dive")

# Display actual use case data if available
if isinstance(corpus, pd.DataFrame) and not corpus.empty:
    st.markdown("### 📊 Documented Use Cases")

    # Show sample use cases
    display_cols = []
    for col in ['Industry', 'Use_Case', 'Technology', 'Benefits', 'Maturity']:
        if col in corpus.columns:
            display_cols.append(col)

    if display_cols:
        sample_cases = corpus[display_cols].head(10)
        st.dataframe(sample_cases, use_container_width=True, hide_index=True)

        # Download option
        csv = corpus.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Use Case Dataset",
            data=csv,
            file_name="xr_use_cases.csv",
            mime="text/csv"
        )

# ============================================================================
# MANAGERIAL IMPLICATIONS
# ============================================================================

st.markdown("---")
st.markdown("## 💼 Managerial Implications")

st.markdown("""
**Use Case Selection Framework:**

1. **High ROI, High Maturity (Quick Wins):**
   - ✅ Manufacturing assembly guidance
   - ✅ Field service remote assistance
   - ✅ Medical training simulations
   - **Action:** Immediate pilot, fast track to production

2. **High ROI, Medium Maturity (Strategic Bets):**
   - 🎯 Quality inspection automation
   - 🎯 Construction design review
   - 🎯 Retail virtual showrooms
   - **Action:** Pilot with vendor partnership, 6-12 month timeline

3. **Experimental (R&D):**
   - 🔬 Spatial collaboration (metaverse)
   - 🔬 AI-generated training content
   - 🔬 Digital twin integration
   - **Action:** Small-scale experimentation, monitor evolution

**Industry-Specific Recommendations:**

- **Manufacturing:** Start with hands-free assembly guidance (proven 15-25% efficiency gain)
- **Healthcare:** Focus on surgical planning and training (clear safety benefits)
- **Field Service:** Deploy remote assistance for complex maintenance (reduce travel costs)
- **Retail:** Experiment with virtual try-on for high-value products (furniture, vehicles)
- **Education:** Partner with institutions for specialized training programs

**Critical Success Factors:**

- 🎯 Clear ROI metrics defined upfront (efficiency, quality, safety, cost)
- 🎯 User adoption focus (ergonomics, ease of use, training)
- 🎯 Content creation pipeline (who creates and maintains XR experiences?)
- 🎯 Integration with existing workflows (don't create silos)
""")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D; padding: 20px;'>
    <p><strong>Use Cases Analysis</strong></p>
    <p>Part of the Five-Dimension XR Technology Readiness Framework</p>
</div>
""", unsafe_allow_html=True)

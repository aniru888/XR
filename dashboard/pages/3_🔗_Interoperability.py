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
    <h4 style='margin: 0; color: {COLORS["primary_blue"]};'>💡 Key Finding</h4>
    <p style='font-size: 1.1em; margin: 10px 0 0 0; color: #1a1a1a;'>{dimension.key_finding}</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# TEXT ANALYTICS
# ============================================================================

st.markdown("## 📊 Text Analytics")

# Load pre-computed analytics from data files
analytics_path = dimension.get_data_paths()[0].parent  # xr_interop_submission directory
sentiment_file = analytics_path / "xr_interop_sentiment.csv"
topics_file = analytics_path / "xr_interop_topics.csv"
top_words_file = analytics_path / "xr_interop_top_words.csv"
wordcloud_img = analytics_path / "xr_interop_wordcloud.png"
sentiment_img = analytics_path / "xr_interop_sentiment_distribution.png"

# Word Cloud
st.markdown("### ☁️ Word Cloud Analysis")
try:
    if wordcloud_img.exists():
        # Display pre-computed word cloud image
        from PIL import Image
        img = Image.open(wordcloud_img)
        st.image(img, use_container_width=True, caption="Key Concepts in XR Interoperability")
    else:
        # Fallback to generating word cloud
        wc_gen = WordCloudGenerator(width=1200, height=600)
        wordcloud = wc_gen.generate(text, max_words=100, colormap='plasma')

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Key Concepts in XR Interoperability', fontsize=16, fontweight='bold', pad=20)
        st.pyplot(fig)

    # Display top words table
    col1, col2 = st.columns([2, 1])
    with col1:
        if top_words_file.exists():
            top_words_df = pd.read_csv(top_words_file)
            st.dataframe(
                top_words_df.head(20),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "word": "Word",
                    "frequency": st.column_config.NumberColumn("Frequency", format="%d")
                }
            )
        else:
            wc_gen = WordCloudGenerator()
            top_words = wc_gen.get_top_words(text, n=20)
            top_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
            st.dataframe(top_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("**Integration Focus:**")
        if top_words_file.exists():
            top_words_df = pd.read_csv(top_words_file)
            if len(top_words_df) > 0:
                st.markdown(f"- Top theme: **{top_words_df.iloc[0]['word']}**")
        st.markdown("- Shows compatibility priorities")
        st.markdown("- Highlights ecosystem gaps")
except Exception as e:
    st.warning(f"Word cloud visualization failed: {e}")

# Sentiment Analysis
st.markdown("---")
st.markdown("### 😊 Sentiment Analysis")
try:
    if sentiment_file.exists():
        # Load pre-computed sentiment results
        sentiment_df = pd.read_csv(sentiment_file)

        # Calculate summary statistics
        avg_compound = sentiment_df['compound'].mean()
        sentiment_counts = sentiment_df['label'].value_counts()
        total = len(sentiment_df)

        pos_pct = (sentiment_counts.get('positive', 0) / total) * 100
        neu_pct = (sentiment_counts.get('neutral', 0) / total) * 100
        neg_pct = (sentiment_counts.get('negative', 0) / total) * 100

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Sentiment", f"{avg_compound:.3f}")
        with col2:
            st.metric("Positive", f"{pos_pct:.1f}%",
                     delta=f"{sentiment_counts.get('positive', 0)} sources",
                     delta_color="off")
        with col3:
            st.metric("Neutral", f"{neu_pct:.1f}%",
                     delta=f"{sentiment_counts.get('neutral', 0)} sources",
                     delta_color="off")
        with col4:
            st.metric("Negative", f"{neg_pct:.1f}%",
                     delta=f"{sentiment_counts.get('negative', 0)} sources",
                     delta_color="off")

        # Display sentiment distribution chart
        if sentiment_img.exists():
            from PIL import Image
            img = Image.open(sentiment_img)
            st.image(img, use_container_width=True, caption="Sentiment Distribution Across Sources")

        # Show detailed sentiment breakdown
        with st.expander("📊 View Detailed Sentiment Breakdown"):
            display_df = sentiment_df[['platform', 'compound', 'label']].copy()
            display_df.columns = ['Platform', 'Sentiment Score', 'Category']
            st.dataframe(
                display_df,
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
        st.info("Pre-computed sentiment analysis not available. Run generate_interop_analysis.py to create it.")
except Exception as e:
    st.warning(f"Sentiment analysis display failed: {e}")

# Topic Modeling
st.markdown("---")
st.markdown("### 🎯 Topic Modeling (LDA)")
try:
    if topics_file.exists():
        # Load pre-computed topics
        topics_df = pd.read_csv(topics_file)

        st.markdown("**Key Integration Themes Identified:**")
        st.markdown("")

        for idx, row in topics_df.iterrows():
            topic_num = idx + 1
            keywords = row['keywords']

            # Create colored topic boxes
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                        padding: 15px; border-radius: 8px; border-left: 4px solid {COLORS['accent_teal']};
                        margin: 10px 0;'>
                <h4 style='margin: 0 0 8px 0; color: {COLORS["primary_blue"]};'>
                    🔸 Topic {topic_num}
                </h4>
                <p style='margin: 0; color: #1a1a1a; font-size: 0.95em;'>
                    <strong>Keywords:</strong> {keywords}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Pre-computed topic modeling not available. Run generate_interop_analysis.py to create it.")
except Exception as e:
    st.warning(f"Topic modeling display failed: {e}")

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

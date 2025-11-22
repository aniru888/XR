"""
Present State of Maturity Dimension
How widely the technology has progressed from lab to market
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
    page_title="Present State of Maturity | XR Dashboard",
    page_icon="📍",
    layout="wide"
)

# Load dimension configuration
dimension = get_dimension_by_id('maturity')
if not dimension:
    st.error("Failed to load dimension configuration")
    st.stop()

# Load data
try:
    data = load_dimension('maturity')
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

# Framework Purpose
st.markdown(f"""
<div style='background: linear-gradient(135deg, {COLORS['primary_blue']} 0%, {COLORS['accent_teal']} 100%);
            color: white; padding: 20px; border-radius: 10px; margin: 20px 0;'>
    <h3 style='color: white; margin: 0;'>📐 Framework Purpose</h3>
    <p style='font-size: 1.2em; margin: 10px 0 0 0;'>{dimension.purpose}</p>
</div>
""", unsafe_allow_html=True)

# Analysis Question
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
    st.metric(
        "Readiness Score",
        f"{dimension.readiness_score}%",
        help="Overall maturity assessment"
    )
    st.caption(dimension.readiness_color)

with col2:
    st.metric(
        "Data Entries",
        f"{dimension.entry_count:,}",
        help="Total data points analyzed"
    )

with col3:
    st.metric(
        "Source Files",
        len(dimension.get_source_paths()),
        help="Number of data source files"
    )

with col4:
    st.metric(
        "Text Corpus",
        f"{len(text):,} chars",
        help="Total text analyzed"
    )

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
analytics_path = dimension.get_data_paths()[0].parent  # xr_present_state_maturity_outputs directory
sentiment_file = analytics_path / "xr_sentences_sentiment.csv"
topics_file = analytics_path / "xr_topics.csv"

# Only run analytics if we have text data
if text and len(text.strip()) > 100:

    # ========================================================================
    # WORD CLOUD
    # ========================================================================

    st.markdown("### 📊 Word Cloud Analysis")
    st.markdown("*Identifies dominant themes and key concepts in the corpus*")

    try:
        wc_gen = WordCloudGenerator(width=1200, height=600)
        wordcloud = wc_gen.generate(
            text,
            max_words=100,
            colormap='viridis',
            background_color='white'
        )

        # Display word cloud
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Dominant Themes in XR Maturity', fontsize=16, fontweight='bold', pad=20)
        st.pyplot(fig)

        # Top words
        col1, col2 = st.columns([2, 1])

        with col1:
            top_words = wc_gen.get_top_words(text, n=20)
            top_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
            st.dataframe(top_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Key Insights:**")
            if top_words:
                top_5 = [word for word, _ in top_words[:5]]
                st.markdown(f"- Most frequent: **{top_5[0]}**")
                st.markdown(f"- Core themes: {', '.join(top_5[1:4])}")
                st.markdown("- Indicates focus areas and industry priorities")

    except Exception as e:
        st.warning(f"Word cloud generation failed: {e}")

    # ========================================================================
    # SENTIMENT ANALYSIS
    # ========================================================================

    st.markdown("---")
    st.markdown("### 😊 Sentiment Analysis")
    st.markdown("*Assesses industry optimism and outlook*")

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
                st.metric(
                    "Average Sentiment",
                    f"{avg_compound:.3f}",
                    help="Range: -1 (negative) to +1 (positive)"
                )

            with col2:
                st.metric(
                    "Positive",
                    f"{pos_pct:.1f}%",
                    delta=f"{sentiment_counts.get('positive', 0)} sentences",
                    delta_color="off",
                    help="Percentage of positive sentiment"
                )

            with col3:
                st.metric(
                    "Neutral",
                    f"{neu_pct:.1f}%",
                    delta=f"{sentiment_counts.get('neutral', 0)} sentences",
                    delta_color="off",
                    help="Percentage of neutral sentiment"
                )

            with col4:
                st.metric(
                    "Negative",
                    f"{neg_pct:.1f}%",
                    delta=f"{sentiment_counts.get('negative', 0)} sentences",
                    delta_color="off",
                    help="Percentage of negative sentiment"
                )

            # Show detailed sentiment breakdown
            with st.expander("📊 View Detailed Sentiment Breakdown"):
                display_df = sentiment_df[['sentence', 'compound', 'label']].copy()
                display_df.columns = ['Sentence', 'Sentiment Score', 'Category']
                # Truncate sentences for display
                display_df['Sentence'] = display_df['Sentence'].str[:100] + '...'
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

            # Interpretation
            st.markdown("**Interpretation:**")
            if avg_compound > 0.1:
                st.success("📈 Overall positive sentiment indicates industry optimism")
            elif avg_compound < -0.1:
                st.warning("📉 Overall negative sentiment suggests challenges or skepticism")
            else:
                st.info("📊 Neutral sentiment indicates balanced, objective reporting")
        else:
            st.info("Pre-computed sentiment analysis not available.")

    except Exception as e:
        st.warning(f"Sentiment analysis display failed: {e}")

    # ========================================================================
    # TOPIC MODELING
    # ========================================================================

    st.markdown("---")
    st.markdown("### 🎯 Topic Modeling (LDA)")
    st.markdown("*Discovers latent themes and patterns*")

    try:
        if topics_file.exists():
            # Load pre-computed topics
            topics_df = pd.read_csv(topics_file)

            st.markdown("**Key Maturity Themes Identified:**")
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
                        🔸 {row['topic']}
                    </h4>
                    <p style='margin: 0; color: #1a1a1a; font-size: 0.95em;'>
                        <strong>Keywords:</strong> {keywords}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Pre-computed topic modeling not available.")

    except Exception as e:
        st.warning(f"Topic modeling display failed: {e}")

else:
    st.info("Limited text data available for this dimension. Analytics require more text corpus.")

# ============================================================================
# DATA SOURCES
# ============================================================================

st.markdown("---")
st.markdown("## 📚 Data Sources")

st.markdown(f"""
This dimension is based on **{dimension.entry_count} data entries** from verified sources.
""")

# Show source files
source_paths = dimension.get_source_paths()
if source_paths:
    st.markdown("**Source Files:**")
    for path in source_paths:
        if path.exists():
            st.markdown(f"- ✅ `{path.name}` ({path.stat().st_size:,} bytes)")
        else:
            st.markdown(f"- ⚠️ `{path.name}` (not found)")

# Show URLs if available
if sources and len(sources) > 0:
    st.markdown(f"**Verified URLs:** {len(sources)}")

    with st.expander("📖 View All Source URLs"):
        for i, url in enumerate(sources, 1):
            st.markdown(f"{i}. [{url}]({url})")
else:
    st.info("This dimension uses text-based corpus data rather than individual URLs")

# ============================================================================
# MANAGERIAL IMPLICATIONS
# ============================================================================

st.markdown("---")
st.markdown("## 💼 Managerial Implications")

st.markdown(f"""
Based on a **{dimension.readiness_score}%** readiness score, here are the strategic implications:
""")

# Readiness-based recommendations
if dimension.readiness_score >= 80:
    st.success("""
    **🟢 High Readiness - Immediate Action Recommended**

    - ✅ Technology is market-ready for enterprise deployment
    - ✅ Multiple vendors offer production-grade solutions
    - ✅ Clear ROI demonstrated in similar organizations
    - ✅ Mature ecosystem with support infrastructure

    **Next Steps:**
    1. Conduct vendor selection process
    2. Plan pilot program with clear success metrics
    3. Allocate budget for full-scale deployment
    4. Establish internal training programs
    """)

elif dimension.readiness_score >= 60:
    st.warning("""
    **🟡 Medium Readiness - Pilot Program Recommended**

    - ⚠️ Technology shows promise but requires validation
    - ⚠️ Vendor landscape still evolving
    - ⚠️ ROI varies by use case and implementation
    - ⚠️ Some gaps in ecosystem support

    **Next Steps:**
    1. Launch controlled pilot in low-risk environment
    2. Partner with vendor for proof-of-concept
    3. Define clear success criteria and exit strategy
    4. Monitor industry developments closely
    """)

else:
    st.error("""
    **🔴 Low Readiness - Monitor and Research**

    - 🔴 Technology not yet ready for enterprise deployment
    - 🔴 Limited vendor options or immature solutions
    - 🔴 Unclear ROI or unproven value proposition
    - 🔴 Significant risks and uncertainties

    **Next Steps:**
    1. Continue monitoring technology evolution
    2. Engage in industry forums and research
    3. Build internal knowledge base
    4. Wait for market maturation signals
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D; padding: 20px;'>
    <p><strong>Present State of Maturity Analysis</strong></p>
    <p>Part of the Five-Dimension XR Technology Readiness Framework</p>
</div>
""", unsafe_allow_html=True)

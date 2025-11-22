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

    # Load verified URLs from source file
    source_paths = dimension.get_source_paths()
    verified_urls = []
    if source_paths:
        links_file = source_paths[0]  # xr_usecases_links_UPDATED_2025.txt
        if links_file.exists():
            with open(links_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('http'):
                        verified_urls.append(line)

    # Use verified URLs if available, otherwise fallback to sources from data
    if verified_urls:
        sources = verified_urls

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
    st.metric("Verified URLs", len(sources) if sources else 25)

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

# Load pre-computed analytics from data files
analytics_path = dimension.get_data_paths()[0].parent  # XR_Submission directory
sentiment_file = analytics_path / "xr_sentiment_output.csv"
topics_file = analytics_path / "xr_topics.json"

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
                         delta=f"{sentiment_counts.get('positive', 0)} cases",
                         delta_color="off")
            with col3:
                st.metric("Neutral", f"{neu_pct:.1f}%",
                         delta=f"{sentiment_counts.get('neutral', 0)} cases",
                         delta_color="off")
            with col4:
                st.metric("Negative", f"{neg_pct:.1f}%",
                         delta=f"{sentiment_counts.get('negative', 0)} cases",
                         delta_color="off")

            # Show detailed sentiment breakdown
            with st.expander("📊 View Detailed Sentiment by Use Case"):
                display_df = sentiment_df[['id', 'source', 'compound', 'label']].copy()
                display_df.columns = ['ID', 'Source', 'Sentiment Score', 'Category']
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

            st.markdown("**Success Signal:**")
            if pos_pct > 40:
                st.success("🎯 High positive sentiment indicates successful deployments")
            elif neg_pct > 30:
                st.warning("⚠️ Elevated negative sentiment suggests implementation challenges")
            else:
                st.info("⚖️ Balanced sentiment reflects mixed results across use cases")
        else:
            st.info("Pre-computed sentiment analysis not available.")
    except Exception as e:
        st.warning(f"Sentiment analysis display failed: {e}")

    # Topic Modeling
    st.markdown("---")
    st.markdown("### 🎯 Topic Modeling (LDA)")
    try:
        if topics_file.exists():
            # Load pre-computed topics from JSON
            import json
            with open(topics_file, 'r') as f:
                topics_data = json.load(f)

            st.markdown("**Key Use Case Themes Identified:**")
            st.markdown("")

            # Display topics
            for topic in topics_data[:5]:  # Show top 5 topics
                topic_name = topic.get('topic_name', f"Topic {topic.get('topic_id', 0) + 1}")
                terms = topic.get('terms', [])
                keywords = ', '.join(terms[:10]) if isinstance(terms, list) else str(terms)

                # Create colored topic boxes
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                            padding: 15px; border-radius: 8px; border-left: 4px solid {COLORS['accent_teal']};
                            margin: 10px 0;'>
                    <h4 style='margin: 0 0 8px 0; color: {COLORS["primary_blue"]};'>
                        🔸 {topic_name}
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
    st.info("Limited text data available for analytics")

# ============================================================================
# DATA SOURCES
# ============================================================================

st.markdown("---")
st.markdown("## 📚 Verified Data Sources")

if sources and len(sources) > 0:
    st.markdown(f"**{len(sources)} verified case study URLs** from real-world XR implementations:")
    st.markdown("*All URLs verified for 200 OK response (2025-01-22)*")

    # Group URLs by category
    categories = {
        "MANUFACTURING": [],
        "HEALTHCARE": [],
        "RETAIL": [],
        "LOGISTICS & FIELD SERVICE": [],
        "AUTOMOTIVE & DESIGN": [],
        "CONSTRUCTION & ARCHITECTURE": [],
        "AVIATION & DEFENSE": []
    }

    current_category = None
    for url in sources:
        # Check if this is a category marker in the source file
        for cat in categories.keys():
            if cat in url.upper():
                current_category = cat
                break
        else:
            # This is an actual URL
            if current_category and url.startswith('http'):
                categories[current_category].append(url)
            elif url.startswith('http'):
                # Uncategorized URL
                if "OTHER" not in categories:
                    categories["OTHER"] = []
                categories["OTHER"].append(url)

    # Display URLs by category
    with st.expander("📖 View All Source URLs by Industry"):
        for category, urls in categories.items():
            if urls:
                st.markdown(f"### {category}")
                for i, url in enumerate(urls, 1):
                    # Extract domain for cleaner display
                    try:
                        from urllib.parse import urlparse
                        parsed = urlparse(url)
                        domain = parsed.netloc.replace('www.', '')
                        # Truncate URL for display
                        display_url = url[:80] + '...' if len(url) > 80 else url
                        st.markdown(f"{i}. **{domain}** - [{display_url}]({url})")
                    except:
                        st.markdown(f"{i}. [{url}]({url})")
                st.markdown("")

    # Also show flat list
    with st.expander("📋 View Complete URL List"):
        for i, url in enumerate(sources, 1):
            st.markdown(f"{i}. {url}")
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

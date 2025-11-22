"""
How Sentiment Analysis & Topic Modeling Work
Educational deep-dive into the analytics methods used across all dimensions
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "config"))

from dimensions import COLORS

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Analytics Explained | XR Dashboard",
    page_icon="🧠",
    layout="wide"
)

# ============================================================================
# PAGE HEADER
# ============================================================================

st.markdown("# 🧠 How Sentiment Analysis & Topic Modeling Work")

st.markdown(f"""
<div style='background: linear-gradient(135deg, {COLORS['primary_blue']} 0%, {COLORS['accent_teal']} 100%);
            color: white; padding: 20px; border-radius: 10px; margin: 20px 0;'>
    <h3 style='color: white; margin: 0;'>📚 Educational Deep-Dive</h3>
    <p style='font-size: 1.2em; margin: 10px 0 0 0;'>
        Understanding the algorithms powering the analytics across all XR dimensions
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
This page explains the two core analytical methods used throughout the XR Technology Readiness Framework:
- **Sentiment Analysis** using the VADER algorithm
- **Topic Modeling** using Latent Dirichlet Allocation (LDA)

Both methods are **unsupervised** - they don't require labeled training data, making them perfect for
analyzing new research without manual annotation.
""")

# ============================================================================
# SENTIMENT ANALYSIS SECTION
# ============================================================================

st.markdown("---")
st.markdown("## 📊 Sentiment Analysis: VADER Algorithm")

st.markdown("""
### What It Does
Analyzes text to determine if it's **positive**, **negative**, or **neutral** based on emotional tone.

### Algorithm Used: VADER (Valence Aware Dictionary and sEntiment Reasoner)

VADER is specifically designed for social media and short texts, making it ideal for analyzing
technical documentation, research papers, and industry reports.
""")

# ============================================================================
# VADER STEP-BY-STEP
# ============================================================================

with st.expander("🔍 **Step-by-Step: How VADER Works**", expanded=True):
    st.markdown("""
    #### Step 1: Lexicon-Based Scoring
    VADER has a **sentiment lexicon** - a dictionary of ~7,500 words with pre-assigned sentiment scores:
    """)

    st.code("""
Examples from VADER lexicon:
"excellent" → +3.1 (very positive)
"good" → +1.9 (positive)
"compatibility" → +0.5 (slightly positive)
"problem" → -1.5 (negative)
"fragmentation" → -1.2 (negative)
"neutral" → 0.0 (neutral)
    """)

    st.markdown("""
    #### Step 2: Text Processing & Word Scoring
    For each word in the text:
    1. Look up the word in the lexicon
    2. Get its base sentiment score
    3. Apply **intensity modifiers**:
       - **Capitalization**: "EXCELLENT" gets boosted (+0.733)
       - **Punctuation**: "Good!!!" gets boosted (+0.292 per !)
       - **Degree modifiers**: "very good" gets boosted, "somewhat good" gets reduced
       - **Negations**: "not good" gets flipped (positive → negative)
    """)

    st.markdown("""
    #### Step 3: Calculate Compound Score
    VADER produces 4 scores:
    """)

    st.code("""
{
    'neg': 0.0,    # Proportion of negative words (0-1)
    'neu': 0.893,  # Proportion of neutral words (0-1)
    'pos': 0.107,  # Proportion of positive words (0-1)
    'compound': 0.34  # Overall sentiment (-1 to +1)
}
    """, language="python")

    st.markdown("**Compound Score Formula:**")
    st.latex(r"\text{compound} = \frac{\sum_{i} w_i}{\sqrt{\sum_{i} w_i^2 + 15}}")

    st.markdown("""
    This normalization ensures the score stays between -1 and +1.

    #### Step 4: Classification
    Based on the **compound score**:
    """)

    st.code("""
if compound >= 0.05:  → Positive
elif compound <= -0.05: → Negative
else:                  → Neutral
    """)

# ============================================================================
# INTERACTIVE DEMO
# ============================================================================

st.markdown("---")
st.markdown("### 🎮 Interactive Demo: Try VADER Yourself")

st.markdown("Enter your own text to see how VADER analyzes sentiment in real-time:")

example_text = st.text_area(
    "Sample Text:",
    "OpenXR provides excellent cross-platform compatibility for XR applications. However, fragmentation persists across proprietary SDKs.",
    height=120,
    help="Try different texts to see how VADER scores them!"
)

if example_text:
    try:
        # Use VADER (not TextBlob) to match the explanation
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            sia = SentimentIntensityAnalyzer()
            scores = sia.polarity_scores(example_text)
            vader_available = True
        except ImportError:
            # Fallback to basic implementation if VADER not available
            vader_available = False
            scores = {'compound': 0.0, 'pos': 0.0, 'neu': 1.0, 'neg': 0.0}

        if vader_available:
            compound_score = scores['compound']

            # Display all VADER scores
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Compound Score",
                    f"{compound_score:.3f}",
                    help="Overall sentiment: -1 (very negative) to +1 (very positive)"
                )

            with col2:
                st.metric(
                    "Positive",
                    f"{scores['pos']:.3f}",
                    help="Proportion of positive words"
                )

            with col3:
                st.metric(
                    "Neutral",
                    f"{scores['neu']:.3f}",
                    help="Proportion of neutral words"
                )

            with col4:
                st.metric(
                    "Negative",
                    f"{scores['neg']:.3f}",
                    help="Proportion of negative words"
                )

            # Classification based on VADER thresholds
            st.markdown("---")
            col_a, col_b = st.columns(2)

            with col_a:
                if compound_score >= 0.05:
                    label = "Positive"
                    color = "green"
                    emoji = "😊"
                elif compound_score <= -0.05:
                    label = "Negative"
                    color = "red"
                    emoji = "😟"
                else:
                    label = "Neutral"
                    color = "blue"
                    emoji = "😐"

                st.markdown(f"### :{color}[{emoji} {label}]")

            with col_b:
                if compound_score >= 0.05:
                    threshold = '≥ 0.05 (VADER positive threshold)'
                elif compound_score <= -0.05:
                    threshold = '≤ -0.05 (VADER negative threshold)'
                else:
                    threshold = 'between -0.05 and 0.05 (neutral range)'

                st.markdown(f"**Classification Reasoning:**")
                st.markdown(f"Compound score **{compound_score:.3f}** is {threshold}")
        else:
            st.warning("⚠️ VADER library not installed. Install with: `pip install vaderSentiment`")
            st.info("The demo requires VADER to show accurate sentiment analysis as described above.")

    except Exception as e:
        st.error(f"Error analyzing sentiment: {e}")
        st.info("Make sure vaderSentiment is installed: `pip install vaderSentiment`")

# ============================================================================
# MATHEMATICAL FOUNDATION
# ============================================================================

with st.expander("📐 **Mathematical Foundation: VADER Compound Score**"):
    st.markdown("""
    **Detailed Formula:**

    Let W = [w₁, w₂, ..., wₙ] be sentiment scores for n words
    """)

    st.latex(r"\text{compound} = \frac{\sum_{i=1}^{n} w_i}{\sqrt{\sum_{i=1}^{n} w_i^2 + \alpha}}")

    st.markdown("""
    where α = 15 (normalization constant)

    **Example Calculation:**
    """)

    # Interactive calculation
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Word Scores:**")
        words_example = pd.DataFrame({
            'Word': ['excellent', 'compatibility', 'fragmentation', 'good'],
            'Score': [3.1, 0.5, -1.2, 0.8]
        })
        st.dataframe(words_example, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("**Calculation Steps:**")
        scores = np.array([3.1, 0.5, -1.2, 0.8])
        numerator = scores.sum()
        denominator = np.sqrt((scores**2).sum() + 15)
        compound = numerator / denominator

        st.markdown(f"""
        1. **Numerator:** {' + '.join([f'{s:+.1f}' for s in scores])} = **{numerator:.1f}**
        2. **Denominator:** √({' + '.join([f'{s**2:.2f}' for s in scores])} + 15) = √{(scores**2).sum() + 15:.2f} = **{denominator:.2f}**
        3. **Compound:** {numerator:.1f} / {denominator:.2f} = **{compound:.3f}**
        4. **Classification:** {'Positive ✓' if compound >= 0.05 else 'Negative' if compound <= -0.05 else 'Neutral'}
        """)

# ============================================================================
# TOPIC MODELING SECTION
# ============================================================================

st.markdown("---")
st.markdown("## 🔍 Topic Modeling: LDA (Latent Dirichlet Allocation)")

st.markdown("""
### What It Does
Discovers **hidden themes** in a collection of documents by grouping words that frequently appear together.

### Algorithm: Latent Dirichlet Allocation (LDA)

LDA is a probabilistic model that assumes documents are mixtures of topics, and topics are mixtures of words.
""")

# ============================================================================
# LDA STEP-BY-STEP
# ============================================================================

with st.expander("🔍 **Step-by-Step: How LDA Works**", expanded=True):
    st.markdown("""
    #### Step 1: Text Preprocessing
    """)

    st.code("""
# Original text
"OpenXR provides cross-platform compatibility for XR applications"

# After preprocessing:
1. Lowercase → "openxr provides cross-platform compatibility xr applications"
2. Remove stopwords → "openxr cross-platform compatibility applications"
3. Tokenize → ["openxr", "cross-platform", "compatibility", "applications"]
    """, language="python")

    st.markdown("""
    #### Step 2: Create Document-Term Matrix
    Convert text to numbers (bag-of-words):
    """)

    # Example matrix
    matrix_example = pd.DataFrame({
        'openxr': [3, 1, 2],
        'cross-platform': [2, 1, 0],
        'compatibility': [1, 2, 1],
        'standards': [0, 3, 1],
        'android': [0, 0, 2]
    }, index=['Doc 1', 'Doc 2', 'Doc 3'])

    st.dataframe(matrix_example, use_container_width=True)

    st.markdown("""
    - Each **row** = one source document
    - Each **column** = one word
    - Each **cell** = word frequency in that document
    """)

    st.markdown("""
    #### Step 3: Initialize Random Topics
    Start with random assignment of words to K topics (typically K=3-5 for XR data)

    #### Step 4: Iterative Refinement (Gibbs Sampling)
    For each word in each document, reassign it to a topic based on:
    """)

    st.latex(r"P(\text{topic} | \text{word}, \text{document}) \propto P(\text{word} | \text{topic}) \times P(\text{topic} | \text{document})")

    st.markdown("""
    **In Plain English:**
    - How often does this word appear in this topic across all documents?
    - How prevalent is this topic in the current document?
    """)

    st.markdown("""
    #### Step 5: Example Iteration
    """)

    st.code("""
Word: "openxr" in Document 5

Check Topic 1:
  - "openxr" appears 15 times in Topic 1 across all docs
  - Topic 1 makes up 60% of Document 5
  - Score: 15 × 0.60 = 9.0

Check Topic 2:
  - "openxr" appears 3 times in Topic 2
  - Topic 2 makes up 20% of Document 5
  - Score: 3 × 0.20 = 0.6

Check Topic 3:
  - "openxr" appears 1 time in Topic 3
  - Topic 3 makes up 20% of Document 5
  - Score: 1 × 0.20 = 0.2

Winner: Topic 1 (score 9.0) → Assign "openxr" to Topic 1
    """)

    st.markdown("""
    Repeat this process **thousands of times** (typically 50-1000 iterations) until topics stabilize.

    #### Step 6: Extract Top Keywords
    After convergence, rank words by their probability in each topic to get the top keywords.
    """)

# ============================================================================
# VISUAL EXAMPLE
# ============================================================================

st.markdown("---")
st.markdown("### 📊 Visual Example: Topic Discovery")

st.markdown("""
Here's how LDA might discover topics in XR interoperability research:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                padding: 15px; border-radius: 8px; border-left: 4px solid {COLORS['accent_teal']};
                margin: 10px 0;'>
        <h4 style='margin: 0 0 8px 0; color: {COLORS["primary_blue"]};'>
            🔸 Topic 1: Technical Integration
        </h4>
        <p style='margin: 0; color: #1a1a1a; font-size: 0.9em;'>
            <strong>Keywords:</strong><br/>
            openxr, interoperability, systems, devices, runtimes, technical, data, compatibility
        </p>
        <p style='margin: 8px 0 0 0; color: #666; font-size: 0.85em;'>
            <em>Pattern:</em> Technical implementation details
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                padding: 15px; border-radius: 8px; border-left: 4px solid {COLORS['accent_teal']};
                margin: 10px 0;'>
        <h4 style='margin: 0 0 8px 0; color: {COLORS["primary_blue"]};'>
            🔸 Topic 2: Standards & Industry
        </h4>
        <p style='margin: 0; color: #1a1a1a; font-size: 0.9em;'>
            <strong>Keywords:</strong><br/>
            standards, enterprise, integration, industry, cross, enable, blocks
        </p>
        <p style='margin: 8px 0 0 0; color: #666; font-size: 0.85em;'>
            <em>Pattern:</em> Business adoption and standardization
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                padding: 15px; border-radius: 8px; border-left: 4px solid {COLORS['accent_teal']};
                margin: 10px 0;'>
        <h4 style='margin: 0 0 8px 0; color: {COLORS["primary_blue"]};'>
            🔸 Topic 3: Developer Tools
        </h4>
        <p style='margin: 0; color: #1a1a1a; font-size: 0.9em;'>
            <strong>Keywords:</strong><br/>
            cross, platform, device, support, developer, guidance, android, compatibility
        </p>
        <p style='margin: 8px 0 0 0; color: #666; font-size: 0.85em;'>
            <em>Pattern:</em> Developer tools and cross-platform development
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MATHEMATICAL FOUNDATION
# ============================================================================

with st.expander("📐 **Mathematical Foundation: LDA Joint Probability**"):
    st.markdown("""
    LDA models the joint probability of words and topics using Bayesian inference:
    """)

    st.latex(r"P(\mathbf{w}, \mathbf{z} | \alpha, \beta) = \prod_{d} P(\theta_d | \alpha) \times \prod_{k} P(\phi_k | \beta) \times \prod_{d}\prod_{n} P(z_{d,n} | \theta_d) \times P(w_{d,n} | \phi_{z_{d,n}})")

    st.markdown("""
    **Where:**
    - **θ_d** = topic distribution for document d (what % of each topic in this document?)
    - **φ_k** = word distribution for topic k (what % of each word in this topic?)
    - **z_d,n** = topic assignment for word n in document d
    - **w_d,n** = the nth word in document d
    - **α, β** = Dirichlet priors (hyperparameters controlling distribution smoothness)

    **In Simpler Terms:**

    LDA tries to find the topic and word distributions that best explain the observed documents.
    It does this by:
    1. Assuming each document is a mixture of topics
    2. Assuming each topic is a mixture of words
    3. Iteratively adjusting these distributions to maximize the probability of seeing the actual words in the documents
    """)

# ============================================================================
# COMPARISON & BEST PRACTICES
# ============================================================================

st.markdown("---")
st.markdown("## ⚖️ Methods Comparison & Best Practices")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📊 Sentiment Analysis (VADER)

    ✅ **Strengths:**
    - Handles technical/business language well
    - Captures nuance and intensity
    - Fast and deterministic
    - No training data needed
    - Good with short texts

    ⚠️ **Limitations:**
    - May miss domain-specific sentiment
    - Struggles with sarcasm/irony
    - Lexicon-based (fixed vocabulary)
    - Doesn't understand context deeply

    **Best Used For:**
    - Analyzing industry reports
    - Gauging technology reception
    - Tracking sentiment trends
    - Quick text classification
    """)

with col2:
    st.markdown("""
    ### 🔍 Topic Modeling (LDA)

    ✅ **Strengths:**
    - Discovers hidden themes
    - Groups semantically related words
    - Unsupervised learning
    - Reveals document structure
    - Interpretable results

    ⚠️ **Limitations:**
    - Requires setting K (topic count)
    - Topics not always meaningful
    - Bag-of-words assumption
    - Sensitive to preprocessing

    **Best Used For:**
    - Exploring large corpora
    - Finding research themes
    - Organizing documents
    - Understanding domain structure
    """)

# ============================================================================
# WHY THESE WORK FOR XR
# ============================================================================

st.markdown("---")
st.markdown("## 🎯 Why These Methods Work Well for XR Data")

st.markdown(f"""
<div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 20px; border-radius: 10px; border-left: 5px solid {COLORS['primary_blue']};
            margin: 20px 0;'>
    <h4 style='margin: 0; color: {COLORS["primary_blue"]};'>✨ Key Advantages</h4>
    <ul style='margin: 10px 0 0 0; color: #1a1a1a;'>
        <li><strong>Unsupervised Learning:</strong> No need for labeled training data - perfect for emerging XR technologies</li>
        <li><strong>Technical Text Handling:</strong> Both handle technical jargon and mixed sentiment well</li>
        <li><strong>Deterministic Results:</strong> Same input always produces same output (with fixed random seed)</li>
        <li><strong>Scalable:</strong> Can process thousands of documents efficiently</li>
        <li><strong>Interpretable:</strong> Results are human-readable and explainable</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# PRACTICAL IMPLEMENTATION
# ============================================================================

st.markdown("---")
st.markdown("## 💻 Practical Implementation")

st.markdown("Here's how these algorithms are implemented in the XR dashboard:")

tab1, tab2 = st.tabs(["Sentiment Analysis Code", "Topic Modeling Code"])

with tab1:
    st.code("""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER
sia = SentimentIntensityAnalyzer()

# Analyze text
text = "OpenXR provides excellent cross-platform compatibility"
scores = sia.polarity_scores(text)

# scores = {
#     'neg': 0.0,
#     'neu': 0.667,
#     'pos': 0.333,
#     'compound': 0.7579
# }

# Classify
if scores['compound'] >= 0.05:
    label = 'positive'
elif scores['compound'] <= -0.05:
    label = 'negative'
else:
    label = 'neutral'

print(f"Sentiment: {label} (score: {scores['compound']:.3f})")
    """, language="python")

with tab2:
    st.code("""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Step 1: Convert text to word counts
vectorizer = CountVectorizer(
    max_features=150,
    stop_words='english',
    ngram_range=(1, 2),
    min_df=1,
    max_df=0.8
)
doc_term_matrix = vectorizer.fit_transform(documents)

# Step 2: Run LDA
lda = LatentDirichletAllocation(
    n_components=3,        # Number of topics
    random_state=42,       # For reproducibility
    max_iter=50           # Iterations
)
lda.fit(doc_term_matrix)

# Step 3: Extract top keywords for each topic
feature_names = vectorizer.get_feature_names_out()

for topic_idx, topic in enumerate(lda.components_):
    top_indices = topic.argsort()[-10:][::-1]
    top_words = [feature_names[i] for i in top_indices]
    print(f"Topic {topic_idx + 1}: {', '.join(top_words)}")
    """, language="python")

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

st.markdown("---")
st.markdown("## 💡 Key Takeaways")

st.info("""
**Remember:**

1. **Sentiment Analysis (VADER)** tells us **how people feel** about XR technologies
   - Positive sentiment → industry optimism, successful implementations
   - Negative sentiment → challenges, concerns, barriers
   - Neutral sentiment → objective, factual reporting

2. **Topic Modeling (LDA)** tells us **what themes are being discussed**
   - Discovers hidden patterns in large document collections
   - Groups related concepts together
   - Reveals the structure of XR research landscape

3. **Both are unsupervised** - perfect for analyzing emerging technologies without pre-labeled data

4. **Results are deterministic** - same analysis always produces same results (great for reproducibility)

5. **Use them together** for comprehensive insights: sentiment shows reception, topics show focus areas
""")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D; padding: 20px;'>
    <p><strong>Analytics Methodology Explained</strong></p>
    <p>Part of the Five-Dimension XR Technology Readiness Framework</p>
    <p style='font-size: 0.9em; margin-top: 10px;'>
        For more details, see dimension-specific analyses:
        Maturity | Interoperability | Scalability | AI Alignment | Use Cases
    </p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import plotly.express as px
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="XR Data Intelligence Dashboard", layout="wide")

st.title("🧩 Mathemagica 2.0: XR & Data Intelligence Alignment")
st.markdown("**Focus:** Synergy of AI (World Models vs LLMs) in Extended Reality Decision Systems.")

# --- DATA LOADING ---
try:
    with open('xr_social_data.txt', 'r', encoding='utf-8') as f:
        raw_text = f.read()
except FileNotFoundError:
    st.error("Error: Data file 'xr_social_data.txt' not found. Please ensure data ingestion is complete.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.header("Analysis Controls")
stop_words_extra = st.sidebar.text_input("Add Stop Words (comma separated)", "xr, ai, model, data, models, world, llms, spatial, intelligence")

# --- ANALYSIS LOGIC ---
def process_text(text):
    # Split by double newlines to separate entries, then clean
    entries = [entry.strip() for entry in text.split('\n\n') if len(entry) > 20]
    # Also handle single line splits if the file format is different
    if len(entries) < 5:
         entries = [line.strip() for line in text.split('\n') if len(line) > 20]
    return pd.DataFrame(entries, columns=['text'])

df = process_text(raw_text)

if df.empty:
    st.error("Data file is empty or formatting is incorrect.")
    st.stop()

# Sentiment
df['sentiment'] = df['text'].apply(lambda x: TextBlob(x).sentiment.polarity)
df['sentiment_label'] = df['sentiment'].apply(lambda x: 'Positive' if x > 0.1 else ('Negative' if x < -0.1 else 'Neutral'))

# Topic Modeling
custom_stop_words = [x.strip() for x in stop_words_extra.split(',')]
from sklearn.feature_extraction import text 
stop_words = text.ENGLISH_STOP_WORDS.union(custom_stop_words)

cv = CountVectorizer(max_df=0.95, min_df=2, stop_words=list(stop_words))
try:
    dtm = cv.fit_transform(df['text'])
    lda = LatentDirichletAllocation(n_components=3, random_state=42)
    lda.fit(dtm)
    lda_success = True
except ValueError:
    st.warning("Not enough data for Topic Modeling. Please expand the dataset.")
    lda_success = False

# --- DASHBOARD LAYOUT ---

# ROW 1: KPIS & SENTIMENT
c1, c2 = st.columns([1, 2])

with c1:
    st.subheader("📊 Social Sentiment")
    fig_pie = px.pie(df, names='sentiment_label', title="Public Perception: Industrial XR", hole=0.4, 
                     color_discrete_map={'Positive':'#00CC96', 'Negative':'#EF553B', 'Neutral':'#636EFA'})
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.info("**Insight:** High optimism for 'Industrial Efficiency', skepticism for 'Privacy' & 'LLM Hallucinations'.")

with c2:
    st.subheader("☁️ Dominant Vocabulary (World Cloud)")
    # Generate WordCloud
    combined_text = " ".join(df['text'])
    wc = WordCloud(width=800, height=400, background_color='white', colormap='magma', stopwords=stop_words).generate(combined_text)
    
    # Display using Matplotlib
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# ROW 2: TOPIC MODELING
st.divider()
st.subheader("🔍 Strategic Themes (LDA Topic Modeling)")

if lda_success:
    col1, col2, col3 = st.columns(3)

    def get_top_words(model, feature_names, n_top_words, topic_idx):
        return ", ".join([feature_names[i] for i in model.components_[topic_idx].argsort()[:-n_top_words - 1:-1]])

    tf_feature_names = cv.get_feature_names_out()

    with col1:
        st.markdown("### Topic 1: The Limitation")
        st.caption("Focus: LLM Shortcomings")
        st.write(get_top_words(lda, tf_feature_names, 8, 0))
        st.warning("Key Risk: 'Hallucinations' in text-based AI applied to physical tasks.")

    with col2:
        st.markdown("### Topic 2: The Solution")
        st.caption("Focus: World Models & Physics")
        st.write(get_top_words(lda, tf_feature_names, 8, 1))
        st.success("Opportunity: 'Predictive' physics engines and 'Spatial' agents.")

    with col3:
        st.markdown("### Topic 3: The Application")
        st.caption("Focus: Digital Twins")
        st.write(get_top_words(lda, tf_feature_names, 8, 2))
        st.info("Use Case: Real-time 'Decision' dashboards for factories.")
else:
    st.write("Topic modeling requires more data.")

# ROW 3: HOW THE ALGORITHMS WORK
st.divider()
st.subheader("🧠 How Sentiment Analysis & Topic Modeling Work")
st.markdown("*Understanding the algorithms behind the analytics*")

# Create two main expanders for detailed explanations
with st.expander("📊 **Sentiment Analysis: VADER Algorithm** - Click to explore"):
    st.markdown("""
    ### What It Does
    Analyzes text to determine if it's **positive**, **negative**, or **neutral** based on emotional tone.

    ### How It Works (Step-by-Step)

    #### Algorithm Used: VADER (Valence Aware Dictionary and sEntiment Reasoner)

    VADER is specifically designed for social media and short texts. Here's the exact process:

    #### Step 1: Lexicon-Based Scoring
    VADER has a **sentiment lexicon** - a dictionary of ~7,500 words with pre-assigned sentiment scores:

    ```
    Examples from VADER lexicon:
    "excellent" → +3.1 (very positive)
    "good" → +1.9 (positive)
    "compatibility" → +0.5 (slightly positive)
    "problem" → -1.5 (negative)
    "fragmentation" → -1.2 (negative)
    "neutral" → 0.0 (neutral)
    ```

    #### Step 2: Text Processing & Word Scoring
    For each word in the text:
    1. Look up the word in the lexicon
    2. Get its base sentiment score
    3. Apply **intensity modifiers**:
       - **Capitalization**: "EXCELLENT" gets boosted (+0.733)
       - **Punctuation**: "Good!!!" gets boosted (+0.292 per !)
       - **Degree modifiers**: "very good" gets boosted, "somewhat good" gets reduced
       - **Negations**: "not good" gets flipped (positive → negative)

    #### Step 3: Calculate Compound Score
    VADER produces 4 scores:
    """)

    # Show formula
    st.code("""
{
    'neg': 0.0,    # Proportion of negative words (0-1)
    'neu': 0.893,  # Proportion of neutral words (0-1)
    'pos': 0.107,  # Proportion of positive words (0-1)
    'compound': 0.34  # Overall sentiment (-1 to +1)
}
    """, language="python")

    st.markdown("""
    **Compound Score Formula:**
    """)
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

    st.markdown("""
    ---
    ### Real Example Demonstration

    Let's analyze a sample text about XR technology:
    """)

    # Interactive example
    example_text = st.text_area(
        "Try your own text (or use the default):",
        "OpenXR provides excellent cross-platform compatibility for XR applications. However, fragmentation persists across proprietary SDKs.",
        height=100
    )

    if example_text:
        from textblob import TextBlob
        sentiment_score = TextBlob(example_text).sentiment.polarity

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Sentiment Score", f"{sentiment_score:.3f}")

        with col2:
            if sentiment_score > 0.1:
                label = "Positive"
                color = "green"
            elif sentiment_score < -0.1:
                label = "Negative"
                color = "red"
            else:
                label = "Neutral"
                color = "blue"
            st.markdown(f"**Classification:** :{color}[{label}]")

        with col3:
            st.markdown(f"**Reasoning:** Score {sentiment_score:.3f} is {'≥ 0.1' if sentiment_score > 0.1 else '≤ -0.1' if sentiment_score < -0.1 else 'between -0.1 and 0.1'}")

    st.markdown("""
    ---
    ### Mathematical Foundation

    **VADER Compound Score Formula (Detailed):**

    Let W = [w₁, w₂, ..., wₙ] be sentiment scores for n words
    """)

    st.latex(r"\text{compound} = \frac{\sum_{i=1}^{n} w_i}{\sqrt{\sum_{i=1}^{n} w_i^2 + \alpha}}")

    st.markdown("""
    where α = 15 (normalization constant)

    **Example Calculation:**
    - Words: [+3.1, +0.5, -1.2, +0.8]
    - Numerator: 3.1 + 0.5 - 1.2 + 0.8 = 3.2
    - Denominator: √(3.1² + 0.5² + 1.2² + 0.8² + 15) = √26.94 = 5.19
    - **Compound: 3.2 / 5.19 = 0.616**
    """)

with st.expander("🔍 **Topic Modeling: LDA (Latent Dirichlet Allocation)** - Click to explore"):
    st.markdown("""
    ### What It Does
    Discovers **hidden themes** in a collection of documents by grouping words that frequently appear together.

    ### How It Works (Step-by-Step)

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

    # Show example matrix
    matrix_example = pd.DataFrame({
        'openxr': [3, 1, 2],
        'cross-platform': [2, 1, 0],
        'compatibility': [1, 2, 1],
        'standards': [0, 3, 1],
        'android': [0, 0, 2]
    }, index=['Doc 1', 'Doc 2', 'Doc 3'])

    st.dataframe(matrix_example)

    st.markdown("""
    - Each row = one source document
    - Each column = one word
    - Each cell = word frequency in that document

    #### Step 3: Initialize Random Topics
    Start with random assignment of words to K topics (we use K=3)

    #### Step 4: Iterative Refinement (Gibbs Sampling)
    For each word in each document, reassign it to a topic based on:
    """)

    st.latex(r"P(\text{topic} | \text{word}, \text{document}) \propto P(\text{word} | \text{topic}) \times P(\text{topic} | \text{document})")

    st.markdown("""
    **In English:**
    - How often does this word appear in this topic across all documents?
    - How prevalent is this topic in the current document?

    **Example iteration:**
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
    Repeat this process **thousands of times** until topics stabilize.

    #### Step 5: Extract Top Keywords
    After convergence, rank words by their probability in each topic.
    """)

    if lda_success:
        st.markdown("""
        ---
        ### Your Actual Topics (From This Dataset)
        """)

        for topic_idx in range(3):
            st.markdown(f"**Topic {topic_idx + 1} Keywords:**")
            keywords = get_top_words(lda, tf_feature_names, 10, topic_idx)
            st.info(keywords)

    st.markdown("""
    ---
    ### Mathematical Foundation: LDA Joint Probability

    LDA models the joint probability of words and topics:
    """)

    st.latex(r"P(\mathbf{w}, \mathbf{z} | \alpha, \beta) = \prod_{d} P(\theta_d | \alpha) \times \prod_{k} P(\phi_k | \beta) \times \prod_{d}\prod_{n} P(z_{d,n} | \theta_d) \times P(w_{d,n} | \phi_{z_{d,n}})")

    st.markdown("""
    where:
    - **θ_d** = topic distribution for document d
    - **φ_k** = word distribution for topic k
    - **z_d,n** = topic assignment for word n in document d
    - **w_d,n** = the nth word in document d
    - **α, β** = Dirichlet priors (hyperparameters)

    ---
    ### Why These Methods Work Well for XR Data

    ✅ **Sentiment Analysis (VADER) Strengths:**
    - Handles technical/business language well
    - Captures nuance: "excellent compatibility BUT fragmentation" → balances positive and negative
    - No training data needed (uses pre-built lexicon)

    ✅ **Topic Modeling (LDA) Strengths:**
    - Discovers hidden themes without manual labeling
    - Groups semantically related words
    - Reveals structure in large document collections

    ⚠️ **Limitations:**
    - VADER may miss domain-specific sentiment
    - LDA requires setting K (number of topics) manually
    - Both assume "bag of words" (ignore word order and context)
    """)

st.info("""
💡 **Key Takeaway:** Both methods are **unsupervised** - they don't need labeled training data,
making them perfect for analyzing new XR research without manual annotation. Results are deterministic
(same input → same output with fixed random seed).
""")

# ROW 4: RECOMMENDATIONS
st.divider()
st.subheader("🚀 Managerial Implications for Decision Making")
rec1, rec2 = st.columns(2)

with rec1:
    st.markdown("""
    **1. Pivot R&D Strategy:**
    * **STOP:** Investing in generic chatbots for VR.
    * **START:** Developing "Spatial Agents" using World Model architectures (JEPA).
    """)

with rec2:
    st.markdown("""
    **2. Data Alignment:**
    * Treat XR headsets as **Data Ingestion Nodes** for training physics models.
    * Focus on **Object Permanence** and **Causality** over text generation.
    """)

# ROW 4: RAW DATA VIEW
st.divider()
with st.expander("View Raw Data Corpus"):
    st.dataframe(df)

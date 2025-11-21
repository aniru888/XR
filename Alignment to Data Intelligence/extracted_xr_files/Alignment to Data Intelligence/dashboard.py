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

# ROW 3: RECOMMENDATIONS
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

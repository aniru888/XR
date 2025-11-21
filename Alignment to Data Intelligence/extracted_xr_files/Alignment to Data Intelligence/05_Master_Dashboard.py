import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

# Import logic from other modules (assuming they are in the same directory)
# Note: In a real package, we would structure this differently. 
# For this kit, we will re-implement the core logic or import if possible.
# To ensure robustness, I will include the core logic here to make this file standalone 
# but referencing the methodology of the other scripts.

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# --- CONFIG ---
st.set_page_config(page_title="Mathemagica 2.0 Analytics Suite", layout="wide")

st.title("🧩 Mathemagica 2.0: Master Analytics Dashboard")
st.markdown("### From Generative AI to Spatial Intelligence")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        # Try loading the cleaned data first
        df = pd.read_csv("XR_Cleaned_Data.csv")
    except FileNotFoundError:
        try:
            # Fallback to master corpus and clean it on the fly
            df = pd.read_csv("XR_Integrated_Master_Corpus.csv")
            # Simple cleaning for display if full cleaning script hasn't run
            if 'Cleaned_Text' not in df.columns:
                 df['Cleaned_Text'] = df['Text'].astype(str).str.lower()
        except FileNotFoundError:
            st.error("Data files not found. Please run the Data Generation step.")
            return pd.DataFrame()
    return df

df = load_data()

if df.empty:
    st.stop()

# --- SIDEBAR ---
st.sidebar.header("Controls")
analysis_mode = st.sidebar.radio("Select Analysis Module", ["Overview", "Word Clouds", "Aspect Sentiment", "LDA Topic Modeling"])

# --- MODULES ---

if analysis_mode == "Overview":
    st.header("Dataset Overview")
    st.metric("Total Documents", len(df))
    st.metric("Date Range", f"{df['Date'].min()} to {df['Date'].max()}")
    
    st.subheader("Source Distribution")
    if 'Source_Type' in df.columns:
        fig = px.pie(df, names='Source_Type', title="Documents by Source")
        st.plotly_chart(fig)
    
    st.dataframe(df.head(10))

elif analysis_mode == "Word Clouds":
    st.header("Optimized Word Clouds")
    
    dimension = st.selectbox("Select Dimension", ["Global", "Privacy", "Industrial Efficiency", "Innovation"])
    
    text_to_plot = ""
    if dimension == "Global":
        text_to_plot = " ".join(df['Cleaned_Text'].fillna('').astype(str))
    elif dimension == "Privacy":
        subset = df[df['Text'].str.contains("Privacy|Security|Surveillance", case=False, na=False)]
        text_to_plot = " ".join(subset['Cleaned_Text'].fillna('').astype(str))
    elif dimension == "Industrial Efficiency":
        subset = df[df['Text'].str.contains("Efficiency|Industrial|Manufacturing|ROI", case=False, na=False)]
        text_to_plot = " ".join(subset['Cleaned_Text'].fillna('').astype(str))
    elif dimension == "Innovation":
        subset = df[df['Text'].str.contains("Innovation|Future|Technology", case=False, na=False)]
        text_to_plot = " ".join(subset['Cleaned_Text'].fillna('').astype(str))
        
    if text_to_plot:
        wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text_to_plot)
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.warning("No data found for this dimension.")

elif analysis_mode == "Aspect Sentiment":
    st.header("Aspect-Based Sentiment Analysis")
    
    aspects = {
        "Privacy": ["privacy", "security", "surveillance", "data", "ethics"],
        "Efficiency": ["efficiency", "roi", "manufacturing", "industrial", "productivity"],
        "Innovation": ["innovation", "future", "technology", "advancement"]
    }
    
    results = []
    for name, keywords in aspects.items():
        pattern = '|'.join(keywords)
        subset = df[df['Text'].str.contains(pattern, case=False, na=False)]
        if not subset.empty:
            score = subset['Text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity).mean()
            results.append({"Aspect": name, "Sentiment Score": score})
            
    res_df = pd.DataFrame(results)
    
    c1, c2 = st.columns(2)
    with c1:
        st.dataframe(res_df)
    with c2:
        fig = px.bar(res_df, x='Aspect', y='Sentiment Score', color='Sentiment Score', range_y=[-1, 1], color_continuous_scale='RdBu')
        st.plotly_chart(fig)

elif analysis_mode == "LDA Topic Modeling":
    st.header("Latent Dirichlet Allocation (LDA)")
    
    n_topics = st.slider("Number of Topics", 2, 10, 3)
    
    if st.button("Run LDA Model"):
        with st.spinner("Training LDA Model..."):
            cv = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
            dtm = cv.fit_transform(df['Cleaned_Text'].fillna(''))
            
            lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
            lda.fit(dtm)
            
            feature_names = cv.get_feature_names_out()
            
            cols = st.columns(n_topics)
            for idx, topic in enumerate(lda.components_):
                top_words = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
                with cols[idx]:
                    st.subheader(f"Topic {idx+1}")
                    st.write(", ".join(top_words))

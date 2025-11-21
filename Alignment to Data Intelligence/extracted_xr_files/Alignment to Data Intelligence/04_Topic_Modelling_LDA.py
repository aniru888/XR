# 04_Topic_Modelling_LDA.py
# IEMT Social Data Analytics Methodology: Latent Dirichlet Allocation (LDA)
# This script implements LDA to discover hidden thematic structures in the corpus.
# It treats documents as mixtures of topics and topics as mixtures of words.

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def run_lda(text_series, n_topics=3, n_top_words=10):
    """
    Performs LDA Topic Modeling on a pandas Series of text.
    Prints the top words for each topic.
    
    Methodology:
    1. Vectorization: Converts text to a Document-Term Matrix (DTM) using CountVectorizer.
    2. LDA Model: Fits the LDA model to the DTM.
    3. Topic Extraction: Identifies the top words associated with each latent topic.
    """
    print("Vectorizing text...")
    # Use CountVectorizer to convert text to a matrix of token counts
    # max_df=0.95: Ignore terms that appear in >95% of documents (too common)
    # min_df=2: Ignore terms that appear in <2 documents (too rare)
    cv = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    dtm = cv.fit_transform(text_series.fillna(''))
    
    print(f"Fitting LDA model with {n_topics} topics...")
    # LDA: Documents are mixtures of topics, Topics are mixtures of words
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)
    
    # Display top words
    feature_names = cv.get_feature_names_out()
    topics = {}
    
    print("\n" + "="*40)
    print("LDA TOPIC MODEL RESULTS")
    print("="*40)
    
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topic_name = f"Topic {topic_idx+1}"
        topics[topic_name] = top_words
        print(f"\n{topic_name}:")
        print(", ".join(top_words))
        
    return lda, dtm, cv, topics

if __name__ == "__main__":
    try:
        df = pd.read_csv("XR_Cleaned_Data.csv")
        run_lda(df['Cleaned_Text'], n_topics=4)
        
    except FileNotFoundError:
        print("Please run 01_Data_Ingestion_Cleaning.py first.")

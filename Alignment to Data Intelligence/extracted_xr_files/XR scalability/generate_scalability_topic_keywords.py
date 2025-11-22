#!/usr/bin/env python3
"""
Generate Topic Keywords CSV for Scalability Dimension
Extracts LDA topic keywords and saves them in standard format for dashboard display
Following the same pattern as Maturity, Interoperability, and AI Alignment dimensions
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import sys

print("="*80)
print("XR SCALABILITY: TOPIC KEYWORDS EXTRACTION")
print("="*80)

# Load processed corpus
try:
    df = pd.read_csv('/home/user/XR/Alignment to Data Intelligence/extracted_xr_files/XR scalability/XR_Processed_Master_Corpus.csv')
    print(f"\n[1/4] Loaded corpus: {len(df)} records")
except FileNotFoundError:
    print("\n[ERROR] XR_Processed_Master_Corpus.csv not found")
    sys.exit(1)

# Prepare texts
texts = df['cleaned_text'].dropna().astype(str).tolist()
print(f"[2/4] Prepared {len(texts)} documents for topic modeling")

# Create document-term matrix
print("[3/4] Running LDA topic modeling...")
vectorizer = CountVectorizer(
    max_df=0.85,
    min_df=2,
    stop_words='english',
    max_features=1000,
    ngram_range=(1, 2)  # Include bigrams like "edge computing"
)

doc_term_matrix = vectorizer.fit_transform(texts)
print(f"  ✓ Document-term matrix: {doc_term_matrix.shape}")

# Fit LDA with 3 topics
lda_model = LatentDirichletAllocation(
    n_components=3,
    max_iter=25,
    learning_method='online',
    random_state=42,
    n_jobs=-1
)

lda_model.fit(doc_term_matrix)
print(f"  ✓ LDA model fitted with 3 topics")

# Extract topic keywords
feature_names = vectorizer.get_feature_names_out()
n_top_words = 10

topics_data = []

print("\n" + "="*80)
print("EXTRACTED TOPICS:")
print("="*80)

for topic_idx, topic in enumerate(lda_model.components_):
    top_indices = topic.argsort()[-n_top_words:][::-1]
    top_words = [feature_names[i] for i in top_indices]
    keywords_str = ', '.join(top_words)

    topics_data.append({
        'topic': f'Topic {topic_idx + 1}',
        'keywords': keywords_str
    })

    print(f"\nTopic {topic_idx + 1}:")
    print(f"  Keywords: {keywords_str}")

# Save to CSV
output_file = '/home/user/XR/Alignment to Data Intelligence/extracted_xr_files/XR scalability/XR_Scalability_Topics.csv'
topics_df = pd.DataFrame(topics_data)
topics_df.to_csv(output_file, index=False)

print("\n" + "="*80)
print(f"[4/4] ✓ Saved topic keywords to: XR_Scalability_Topics.csv")
print("="*80)
print("\nThis file can now be loaded by the Scalability dashboard page")
print("to display actual topic keywords instead of hardcoded labels.")
print("="*80)

#!/usr/bin/env python3
"""Regenerate all analysis outputs for Present State of Maturity dimension."""

import re
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import nltk

print("="*80)
print("XR PRESENT STATE OF MATURITY: COMPLETE ANALYSIS")
print("="*80)

# Load corpus
print("\n[1/4] Loading corpus...")
with open('XR_present_state_corpus.txt', 'r', encoding='utf-8') as f:
    corpus = f.read()

# Clean text
corpus_clean = re.sub(r'[^\w\s]', ' ', corpus.lower())
corpus_clean = re.sub(r'\s+', ' ', corpus_clean).strip()
print(f"  ✓ Loaded {len(corpus.split())} words")

# 1. Word Cloud Generation
print("\n[2/4] Generating word cloud...")
wc = WordCloud(
    width=1600,
    height=800,
    collocations=False,
    background_color='white',
    max_words=100
).generate(corpus_clean)

plt.figure(figsize=(16, 8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('XR Present State of Maturity - Key Themes', fontsize=20, pad=20)
plt.savefig('xr_wordcloud.png', bbox_inches='tight', dpi=300)
plt.close()
print("  ✓ Saved: xr_wordcloud.png")

# 2. Sentiment Analysis
print("\n[3/4] Running sentiment analysis...")
sia = SentimentIntensityAnalyzer()

# Split into sentences for granular analysis
sentences = [s.strip() for s in corpus.split('.') if len(s.strip()) > 20]
sentiments = []

for sentence in sentences:
    scores = sia.polarity_scores(sentence)
    sentiments.append({
        'sentence': sentence[:100],  # First 100 chars
        'compound': scores['compound'],
        'pos': scores['pos'],
        'neu': scores['neu'],
        'neg': scores['neg'],
        'label': 'positive' if scores['compound'] >= 0.05 else 'negative' if scores['compound'] <= -0.05 else 'neutral'
    })

df_sentiment = pd.DataFrame(sentiments)
df_sentiment.to_csv('xr_sentences_sentiment.csv', index=False)
print(f"  ✓ Analyzed {len(sentiments)} sentences")

# Sentiment distribution
sentiment_counts = df_sentiment['label'].value_counts()
avg_sentiment = df_sentiment['compound'].mean()

print(f"\n  Sentiment Distribution:")
print(f"    Positive: {sentiment_counts.get('positive', 0)} ({sentiment_counts.get('positive', 0)/len(sentiments)*100:.1f}%)")
print(f"    Neutral:  {sentiment_counts.get('neutral', 0)} ({sentiment_counts.get('neutral', 0)/len(sentiments)*100:.1f}%)")
print(f"    Negative: {sentiment_counts.get('negative', 0)} ({sentiment_counts.get('negative', 0)/len(sentiments)*100:.1f}%)")
print(f"    Average sentiment: {avg_sentiment:.3f}")

# Visualize sentiment distribution
plt.figure(figsize=(10, 6))
sentiment_counts.plot(kind='bar', color=['#2ecc71', '#95a5a6', '#e74c3c'])
plt.title('XR Present State of Maturity - Sentiment Distribution', fontsize=14)
plt.xlabel('Sentiment Category')
plt.ylabel('Number of Sentences')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('xr_sentiment_distribution.png', dpi=300)
plt.close()
print("  ✓ Saved: xr_sentiment_distribution.png")

# 3. Topic Modeling (LDA)
print("\n[4/4] Running topic modeling...")
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['xr', 'extended', 'reality', 'ar', 'vr', 'mr', 'technology', 'technologies'])

# Use sentences as documents for topic modeling
documents = [s.strip() for s in corpus.split('.') if len(s.strip()) > 30]

vectorizer = CountVectorizer(
    max_features=200,
    stop_words=stop_words,
    ngram_range=(1, 2),
    min_df=1,  # Changed from 2 to 1 for small corpus
    max_df=0.8
)

doc_term_matrix = vectorizer.fit_transform(documents)
lda = LDA(n_components=3, random_state=42, max_iter=50)
lda.fit(doc_term_matrix)

feature_names = vectorizer.get_feature_names_out()
print("\n  Top Topics Identified:")

topics_output = []
for topic_idx, topic in enumerate(lda.components_):
    top_indices = topic.argsort()[-10:][::-1]
    top_words = [feature_names[i] for i in top_indices]
    print(f"\n  Topic {topic_idx + 1}: {', '.join(top_words[:5])}")
    topics_output.append({
        'topic': f'Topic {topic_idx + 1}',
        'keywords': ', '.join(top_words)
    })

df_topics = pd.DataFrame(topics_output)
df_topics.to_csv('xr_topics.csv', index=False)
print("\n  ✓ Saved: xr_topics.csv")

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE")
print("="*80)
print("\nGenerated outputs:")
print("  - xr_wordcloud.png")
print("  - xr_sentences_sentiment.csv")
print("  - xr_sentiment_distribution.png")
print("  - xr_topics.csv")
print("="*80)

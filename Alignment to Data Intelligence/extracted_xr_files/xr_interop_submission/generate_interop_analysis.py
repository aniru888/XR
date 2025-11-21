#!/usr/bin/env python3
"""Generate complete analysis for XR Interoperability dimension."""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import nltk
import re

print("="*80)
print("XR INTEROPERABILITY: COMPLETE ANALYSIS")
print("="*80)

# Load data
print("\n[1/4] Loading data...")
df = pd.read_csv('xr_interop_raw.csv')
print(f"  ✓ Loaded {len(df)} sources")

# Combine all text for corpus
corpus = ' '.join(df['text'].fillna('').astype(str))
corpus_clean = re.sub(r'[^\w\s]', ' ', corpus.lower())
corpus_clean = re.sub(r'\s+', ' ', corpus_clean).strip()
print(f"  ✓ Combined corpus: {len(corpus.split())} words")

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
plt.title('XR Interoperability - Key Themes', fontsize=20, pad=20)
plt.savefig('xr_interop_wordcloud.png', bbox_inches='tight', dpi=300)
plt.close()
print("  ✓ Saved: xr_interop_wordcloud.png")

# Get top words
word_freq = {}
for word in corpus_clean.split():
    if len(word) > 3:  # Skip short words
        word_freq[word] = word_freq.get(word, 0) + 1

top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:30]
df_words = pd.DataFrame(top_words, columns=['word', 'frequency'])
df_words.to_csv('xr_interop_top_words.csv', index=False)
print(f"  ✓ Top 30 words saved to xr_interop_top_words.csv")

# 2. Sentiment Analysis
print("\n[3/4] Running sentiment analysis...")
sia = SentimentIntensityAnalyzer()

sentiments = []
for idx, row in df.iterrows():
    text = str(row['text'])
    scores = sia.polarity_scores(text)
    sentiments.append({
        'source': row['source_url'],
        'platform': row['platform'],
        'compound': scores['compound'],
        'pos': scores['pos'],
        'neu': scores['neu'],
        'neg': scores['neg'],
        'label': 'positive' if scores['compound'] >= 0.05 else 'negative' if scores['compound'] <= -0.05 else 'neutral'
    })

df_sentiment = pd.DataFrame(sentiments)
df_sentiment.to_csv('xr_interop_sentiment.csv', index=False)
print(f"  ✓ Analyzed {len(sentiments)} sources")

# Sentiment distribution
sentiment_counts = df_sentiment['label'].value_counts()
avg_sentiment = df_sentiment['compound'].mean()

print(f"\n  Sentiment Distribution:")
for label in ['positive', 'neutral', 'negative']:
    count = sentiment_counts.get(label, 0)
    pct = count / len(sentiments) * 100
    print(f"    {label.capitalize()}: {count} ({pct:.1f}%)")
print(f"    Average sentiment: {avg_sentiment:.3f}")

# Visualize sentiment distribution
plt.figure(figsize=(10, 6))
sentiment_counts.plot(kind='bar', color=['#2ecc71', '#95a5a6', '#e74c3c'])
plt.title('XR Interoperability - Sentiment Distribution', fontsize=14)
plt.xlabel('Sentiment Category')
plt.ylabel('Number of Sources')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('xr_interop_sentiment_distribution.png', dpi=300)
plt.close()
print("  ✓ Saved: xr_interop_sentiment_distribution.png")

# 3. Topic Modeling (LDA)
print("\n[4/4] Running topic modeling...")
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['xr', 'extended', 'reality', 'ar', 'vr', 'mr'])

# Use each source as a document
documents = df['text'].fillna('').tolist()

vectorizer = CountVectorizer(
    max_features=150,
    stop_words=stop_words,
    ngram_range=(1, 2),
    min_df=1,
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
df_topics.to_csv('xr_interop_topics.csv', index=False)
print("\n  ✓ Saved: xr_interop_topics.csv")

# Summary statistics
print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE")
print("="*80)
print("\nKey Statistics:")
print(f"  Sources analyzed: {len(df)}")
print(f"  Total words: {len(corpus.split())}")
print(f"  Average sentiment: {avg_sentiment:.3f}")
print(f"  Primary focus: OpenXR standards & cross-platform compatibility")
print("\nGenerated outputs:")
print("  - xr_interop_wordcloud.png")
print("  - xr_interop_top_words.csv")
print("  - xr_interop_sentiment.csv")
print("  - xr_interop_sentiment_distribution.png")
print("  - xr_interop_topics.csv")
print("="*80)

#!/usr/bin/env python3
"""
Regenerate ALL Maturity analytics with EXPANDED dataset (159 sentences from 17 sources).
Following Interoperability standard for consistency.
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import nltk
import re

print("="*80)
print("XR MATURITY: COMPLETE ANALYTICS REGENERATION (EXPANDED DATASET)")
print("="*80)

# Load EXPANDED data
print("\n[1/5] Loading EXPANDED data...")
with open('XR_present_state_VERBATIM_raw_EXPANDED.txt', 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Split into sentences
# Remove SOURCE: lines for cleaner processing
text_clean = re.sub(r'SOURCE:.*\n', '', raw_text)
text_clean = re.sub(r'\n+', '\n', text_clean)  # Remove extra newlines

# Split by sentence endings
sentences = re.split(r'[.!?]\s+', text_clean)
sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]

print(f"  ✓ Loaded {len(sentences)} sentences")
print(f"  ✓ Total words: {sum(len(s.split()) for s in sentences):,}")

# Combine all text for corpus
corpus = ' '.join(sentences)
corpus_clean = re.sub(r'[^\w\s]', ' ', corpus.lower())
corpus_clean = re.sub(r'\s+', ' ', corpus_clean).strip()

# 1. Word Cloud Generation
print("\n[2/5] Generating word cloud...")
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
plt.title('XR Maturity - Key Themes (Expanded Dataset)', fontsize=20, pad=20)
plt.savefig('xr_wordcloud.png', bbox_inches='tight', dpi=300)
plt.close()
print("  ✓ Saved: xr_wordcloud.png")

# Get top words
word_freq = {}
for word in corpus_clean.split():
    if len(word) > 3:  # Skip short words
        word_freq[word] = word_freq.get(word, 0) + 1

top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:30]
df_words = pd.DataFrame(top_words, columns=['word', 'frequency'])
df_words.to_csv('xr_top_words.csv', index=False)
print(f"  ✓ Top 30 words saved to xr_top_words.csv")

# 2. Sentiment Analysis
print("\n[3/5] Running sentiment analysis...")
sia = SentimentIntensityAnalyzer()

sentiments = []
for idx, sentence in enumerate(sentences):
    scores = sia.polarity_scores(sentence)
    sentiments.append({
        'sentence': sentence,
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
for label in ['positive', 'neutral', 'negative']:
    count = sentiment_counts.get(label, 0)
    pct = count / len(sentiments) * 100
    print(f"    {label.capitalize()}: {count} ({pct:.1f}%)")
print(f"    Average sentiment: {avg_sentiment:.3f}")

# Visualize sentiment distribution
plt.figure(figsize=(10, 6))
sentiment_counts.plot(kind='bar', color=['#2ecc71', '#95a5a6', '#e74c3c'])
plt.title('XR Maturity - Sentiment Distribution (Expanded Dataset)', fontsize=14)
plt.xlabel('Sentiment Category')
plt.ylabel('Number of Sentences')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('xr_sentiment_distribution.png', dpi=300)
plt.close()
print("  ✓ Saved: xr_sentiment_distribution.png")

# 3. Topic Modeling (LDA)
print("\n[4/5] Running topic modeling...")
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['xr', 'extended', 'reality', 'ar', 'vr', 'mr', 'year', 'market', 'technology', 'technologies'])

# Use sentences as documents
documents = sentences

vectorizer = CountVectorizer(
    max_features=150,
    stop_words=stop_words,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.8
)

doc_term_matrix = vectorizer.fit_transform(documents)
lda = LDA(n_components=5, random_state=42, max_iter=50)
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

# 4. Create summary corpus file
print("\n[5/5] Creating corpus file...")
with open('XR_present_state_corpus.txt', 'w', encoding='utf-8') as f:
    f.write(corpus)
print(f"  ✓ Saved: XR_present_state_corpus.txt ({len(corpus):,} characters)")

# Summary statistics
print("\n" + "="*80)
print("✅ ANALYTICS REGENERATION COMPLETE")
print("="*80)
print("\nDataset Expansion:")
print(f"  Previous: 39 sentences from 7 sources")
print(f"  NEW: {len(sentences)} sentences from 17 sources")
print(f"  Growth: +{len(sentences)-39} sentences (+{((len(sentences)-39)/39)*100:.0f}%)")

print("\nKey Statistics:")
print(f"  Total sentences: {len(sentences)}")
print(f"  Total words: {sum(len(s.split()) for s in sentences):,}")
print(f"  Average sentiment: {avg_sentiment:.3f}")
print(f"  Topics identified: {len(topics_output)}")

print("\nSentiment Breakdown:")
print(f"  Positive: {sentiment_counts.get('positive', 0)} ({sentiment_counts.get('positive', 0)/len(sentences)*100:.1f}%)")
print(f"  Neutral: {sentiment_counts.get('neutral', 0)} ({sentiment_counts.get('neutral', 0)/len(sentences)*100:.1f}%)")
print(f"  Negative: {sentiment_counts.get('negative', 0)} ({sentiment_counts.get('negative', 0)/len(sentences)*100:.1f}%)")

print("\nGenerated outputs:")
print("  - xr_wordcloud.png (1600x800, high-res)")
print("  - xr_top_words.csv (30 keywords)")
print("  - xr_sentences_sentiment.csv (all sentences)")
print("  - xr_sentiment_distribution.png (visualization)")
print("  - xr_topics.csv (5 topics)")
print("  - XR_present_state_corpus.txt (full text)")

print("\n" + "="*80)
print("✅ All analytics generated following Interoperability standard")
print("="*80)

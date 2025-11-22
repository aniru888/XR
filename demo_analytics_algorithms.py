#!/usr/bin/env python3
"""
Interactive Demonstration: How Sentiment Analysis & Topic Modeling Work
Shows step-by-step processing on real XR interoperability data
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

print("="*80)
print("INTERACTIVE DEMONSTRATION: SENTIMENT ANALYSIS & TOPIC MODELING")
print("="*80)

# ============================================================================
# PART 1: SENTIMENT ANALYSIS DEEP DIVE
# ============================================================================

print("\n" + "="*80)
print("PART 1: SENTIMENT ANALYSIS (VADER Algorithm)")
print("="*80)

# Load real data
df = pd.read_csv('Alignment to Data Intelligence/extracted_xr_files/xr_interop_submission/xr_interop_raw.csv')

# Pick 3 examples: positive, neutral, negative
example_texts = {
    'POSITIVE': df[df['platform'] == 'Android Developers'].iloc[0]['text'],
    'NEUTRAL': df[df['platform'] == 'Godot Engine Docs'].iloc[0]['text'],
    'NEGATIVE': df[df['platform'] == 'Google Research Blog'].iloc[0]['text']
}

sia = SentimentIntensityAnalyzer()

for category, text in example_texts.items():
    print(f"\n{'-'*80}")
    print(f"EXAMPLE: {category}")
    print(f"{'-'*80}")

    # Truncate for display
    display_text = text[:200] + "..." if len(text) > 200 else text
    print(f"\nOriginal Text:\n  \"{display_text}\"")

    # Get VADER scores
    scores = sia.polarity_scores(text)

    print(f"\nVADER Sentiment Scores:")
    print(f"  Negative proportion: {scores['neg']:.3f}")
    print(f"  Neutral proportion:  {scores['neu']:.3f}")
    print(f"  Positive proportion: {scores['pos']:.3f}")
    print(f"  ────────────────────────────────")
    print(f"  COMPOUND SCORE:      {scores['compound']:.3f}")

    # Classify
    if scores['compound'] >= 0.05:
        label = 'POSITIVE'
        color = '🟢'
    elif scores['compound'] <= -0.05:
        label = 'NEGATIVE'
        color = '🔴'
    else:
        label = 'NEUTRAL'
        color = '⚪'

    print(f"\n  Classification: {color} {label}")
    print(f"  Reasoning: compound {scores['compound']:.3f} ", end='')
    if scores['compound'] >= 0.05:
        print(f"≥ 0.05 threshold")
    elif scores['compound'] <= -0.05:
        print(f"≤ -0.05 threshold")
    else:
        print(f"between -0.05 and 0.05")

# Show how words contribute
print(f"\n{'-'*80}")
print("WORD-LEVEL ANALYSIS: Breaking Down the Positive Example")
print(f"{'-'*80}")

example_text = "OpenXR provides excellent cross-platform compatibility"
print(f"\nExample Sentence: \"{example_text}\"")
print(f"\nWord-by-word contribution (approximate):")

# Get lexicon (VADER's word scores)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
lexicon = SentimentIntensityAnalyzer().lexicon

words = example_text.lower().split()
total_score = 0
for word in words:
    word_clean = word.strip('.,!?')
    if word_clean in lexicon:
        score = lexicon[word_clean]
        total_score += score
        sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        print(f"  '{word_clean}': {score:+.2f} ({sentiment})")
    else:
        print(f"  '{word_clean}': 0.00 (not in lexicon)")

print(f"\nSum of word scores: {total_score:.2f}")

# Calculate actual VADER score
actual_scores = sia.polarity_scores(example_text)
print(f"VADER compound score: {actual_scores['compound']:.3f}")
print(f"\nNote: VADER applies normalization: sum / sqrt(sum² + 15)")
print(f"      {total_score:.2f} / sqrt({total_score:.2f}² + 15) = ", end='')
print(f"{total_score / np.sqrt(total_score**2 + 15):.3f}")

# ============================================================================
# PART 2: TOPIC MODELING DEEP DIVE
# ============================================================================

print("\n\n" + "="*80)
print("PART 2: TOPIC MODELING (LDA Algorithm)")
print("="*80)

# Load all documents
documents = df['text'].fillna('').tolist()

print(f"\nDataset: {len(documents)} documents about XR interoperability")

# Show preprocessing
print(f"\n{'-'*80}")
print("STEP 1: Text Preprocessing")
print(f"{'-'*80}")

sample_doc = documents[0][:150]
print(f"\nOriginal text (sample):\n  \"{sample_doc}...\"")

# Vectorize
vectorizer = CountVectorizer(
    max_features=150,
    stop_words='english',
    ngram_range=(1, 2),
    min_df=1,
    max_df=0.8
)

doc_term_matrix = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()

print(f"\nAfter preprocessing:")
print(f"  Total unique terms: {len(feature_names)}")
print(f"  Document-term matrix shape: {doc_term_matrix.shape}")
print(f"  (19 documents × {len(feature_names)} terms)")

# Show term frequencies for first document
print(f"\nFirst document word frequencies (top 10):")
doc_0 = doc_term_matrix[0].toarray()[0]
top_indices = doc_0.argsort()[-10:][::-1]
for idx in top_indices:
    if doc_0[idx] > 0:
        print(f"  '{feature_names[idx]}': {int(doc_0[idx])}")

# Run LDA
print(f"\n{'-'*80}")
print("STEP 2: Running LDA (Latent Dirichlet Allocation)")
print(f"{'-'*80}")

print(f"\nParameters:")
print(f"  Number of topics (K): 3")
print(f"  Max iterations: 50")
print(f"  Algorithm: Variational Bayes inference")

lda = LatentDirichletAllocation(n_components=3, random_state=42, max_iter=50)
lda.fit(doc_term_matrix)

print(f"\n✓ LDA training complete")

# Show topics
print(f"\n{'-'*80}")
print("STEP 3: Discovered Topics")
print(f"{'-'*80}")

topic_names = [
    "OpenXR Technical Integration",
    "Enterprise Standards & Integration",
    "Cross-Platform Developer Support"
]

for topic_idx, topic in enumerate(lda.components_):
    print(f"\n🔸 Topic {topic_idx + 1}: {topic_names[topic_idx]}")

    # Get top 10 words
    top_indices = topic.argsort()[-10:][::-1]
    top_words = [(feature_names[i], topic[i]) for i in top_indices]

    print(f"  Top keywords (with probabilities):")
    for word, prob in top_words:
        # Normalize to percentage
        prob_pct = (prob / topic.sum()) * 100
        print(f"    {word:<25s} {prob_pct:5.1f}%")

# Show document-topic distribution
print(f"\n{'-'*80}")
print("STEP 4: Document-Topic Assignments")
print(f"{'-'*80}")

doc_topics = lda.transform(doc_term_matrix)

print(f"\nSample: How much each topic appears in first 3 documents:\n")
print(f"{'Document':<30s} {'Topic 1':<12s} {'Topic 2':<12s} {'Topic 3':<12s} {'Dominant':<10s}")
print("-" * 80)

for i in range(min(3, len(df))):
    platform = df.iloc[i]['platform'][:28]
    topic_probs = doc_topics[i]
    dominant_topic = topic_probs.argmax() + 1

    print(f"{platform:<30s} ", end='')
    for prob in topic_probs:
        print(f"{prob*100:5.1f}%      ", end='')
    print(f"Topic {dominant_topic}")

# Show word co-occurrence
print(f"\n{'-'*80}")
print("STEP 5: Why Words Cluster Together")
print(f"{'-'*80}")

print(f"\nExample: Why does 'openxr' appear in multiple topics?")
print(f"\nWord 'openxr' distribution across topics:")

openxr_idx = np.where(feature_names == 'openxr')[0]
if len(openxr_idx) > 0:
    openxr_idx = openxr_idx[0]
    for topic_idx, topic in enumerate(lda.components_):
        prob = topic[openxr_idx] / topic.sum() * 100
        print(f"  Topic {topic_idx + 1}: {prob:5.2f}%")

    print(f"\nInterpretation:")
    print(f"  'openxr' is relevant to all topics but with different emphasis")
    print(f"  The SURROUNDING words define each topic's unique focus")

# Summary statistics
print(f"\n{'-'*80}")
print("SUMMARY: Model Quality Metrics")
print(f"{'-'*80}")

print(f"\nPerplexity: {lda.perplexity(doc_term_matrix):.2f}")
print(f"  (Lower is better; measures how well model predicts the data)")

print(f"\nLog-likelihood: {lda.score(doc_term_matrix):.2f}")
print(f"  (Higher is better; probability of observed data given model)")

# Show actual saved results
print(f"\n\n{'='*80}")
print("VERIFICATION: Compare with Saved Results")
print(f"{'='*80}")

saved_sentiment = pd.read_csv('Alignment to Data Intelligence/extracted_xr_files/xr_interop_submission/xr_interop_sentiment.csv')
saved_topics = pd.read_csv('Alignment to Data Intelligence/extracted_xr_files/xr_interop_submission/xr_interop_topics.csv')

print(f"\n✓ Saved Sentiment Results:")
print(f"  Average compound: {saved_sentiment['compound'].mean():.3f}")
print(f"  Distribution: {saved_sentiment['label'].value_counts().to_dict()}")

print(f"\n✓ Saved Topic Results:")
for idx, row in saved_topics.iterrows():
    print(f"  {row['topic']}: {row['keywords'][:80]}...")

print(f"\n{'='*80}")
print("✅ DEMONSTRATION COMPLETE")
print(f"{'='*80}")
print(f"\nKey Takeaways:")
print(f"  1. Sentiment analysis uses lexicon + normalization (not machine learning)")
print(f"  2. LDA discovers topics by finding word co-occurrence patterns")
print(f"  3. Both methods are unsupervised (no labeled training data needed)")
print(f"  4. Results are deterministic (same input → same output with fixed random_seed)")
print(f"\nFor detailed explanation, see: ANALYTICS_EXPLANATION.md")
print(f"{'='*80}\n")

# Algorithm Flow: Sentiment Analysis & Topic Modeling

## Quick Visual Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INPUT: XR INTEROPERABILITY TEXT                       │
│  "OpenXR provides excellent cross-platform compatibility for XR apps"   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌───────────────────────┐      ┌───────────────────────┐
        │ SENTIMENT ANALYSIS    │      │  TOPIC MODELING       │
        │ (VADER Algorithm)     │      │  (LDA Algorithm)      │
        └───────────────────────┘      └───────────────────────┘
                    │                               │
                    ▼                               ▼
```

---

## SENTIMENT ANALYSIS FLOW

```
INPUT TEXT
  │
  ├─► STEP 1: Tokenization
  │   "OpenXR provides excellent cross-platform compatibility"
  │   → ["OpenXR", "provides", "excellent", "cross-platform", "compatibility"]
  │
  ├─► STEP 2: Lexicon Lookup
  │   ┌─────────────────┬───────────┐
  │   │ Word            │ Score     │
  │   ├─────────────────┼───────────┤
  │   │ openxr          │  0.0      │ ← not in lexicon
  │   │ provides        │  0.0      │ ← not in lexicon
  │   │ excellent       │ +2.7      │ ← strong positive
  │   │ cross-platform  │  0.0      │ ← not in lexicon
  │   │ compatibility   │  0.0      │ ← not in lexicon
  │   └─────────────────┴───────────┘
  │
  ├─► STEP 3: Apply Modifiers
  │   • Capitalization boost: none
  │   • Punctuation boost: none
  │   • Negation check: none
  │   • Degree modifiers: none
  │   Sum: +2.7
  │
  ├─► STEP 4: Normalize
  │   compound = 2.7 / sqrt(2.7² + 15)
  │            = 2.7 / 4.72
  │            = 0.572
  │
  └─► STEP 5: Classify
      0.572 >= 0.05 → POSITIVE 🟢

      OUTPUT: {
        'compound': 0.572,
        'pos': 0.273,
        'neu': 0.727,
        'neg': 0.000,
        'label': 'positive'
      }
```

---

## TOPIC MODELING (LDA) FLOW

```
INPUT: 19 DOCUMENTS
  │
  ├─► STEP 1: Preprocessing
  │
  │   Document 1: "OpenXR 1.1 update shows industry consensus on key features"
  │   Document 2: "Standards for cross-platform enterprise integration..."
  │   Document 3: "Android developer guidance for cross-device compatibility..."
  │   ...
  │
  │   ↓ Lowercase, remove stopwords, tokenize
  │
  │   Document 1: ["openxr", "update", "industry", "consensus", "key", "features"]
  │   Document 2: ["standards", "cross-platform", "enterprise", "integration"]
  │   Document 3: ["android", "developer", "guidance", "cross-device", "compatibility"]
  │
  ├─► STEP 2: Create Document-Term Matrix
  │
  │            openxr  standards  cross  android  developer  ...
  │   Doc 1       3        0        1       0         0      ...
  │   Doc 2       1        4        2       0         0      ...
  │   Doc 3       2        0        3       2         2      ...
  │   ...
  │
  │   Matrix shape: 19 documents × 150 words
  │
  ├─► STEP 3: Initialize Random Topics (K=3)
  │
  │   Topic 1: {random word assignments}
  │   Topic 2: {random word assignments}
  │   Topic 3: {random word assignments}
  │
  ├─► STEP 4: Iterative Refinement (50 iterations)
  │
  │   For each word in each document:
  │   ┌─────────────────────────────────────────┐
  │   │ Calculate: P(topic | word, document)    │
  │   │                                          │
  │   │ = P(word | topic) × P(topic | document) │
  │   │                                          │
  │   │ Example for "openxr" in Doc 5:         │
  │   │   Topic 1: 15 occurrences × 60% = 9.0  │
  │   │   Topic 2:  3 occurrences × 20% = 0.6  │
  │   │   Topic 3:  1 occurrence  × 20% = 0.2  │
  │   │                                          │
  │   │ → Assign "openxr" to Topic 1           │
  │   └─────────────────────────────────────────┘
  │
  │   Repeat until convergence...
  │
  ├─► STEP 5: Extract Top Keywords
  │
  │   After 50 iterations, word probabilities stabilize:
  │
  │   Topic 1 word distribution:
  │     openxr:           15.2%  ┐
  │     interoperability: 12.1%  │
  │     systems:           9.7%  ├─ Co-occur frequently
  │     devices:           8.9%  │
  │     technical:         7.4%  ┘
  │
  │   Topic 2 word distribution:
  │     standards:        16.3%  ┐
  │     enterprise:        9.5%  │
  │     integration:       8.2%  ├─ Different co-occurrence pattern
  │     industry:          7.1%  │
  │     cross:            10.8%  ┘
  │
  │   Topic 3 word distribution:
  │     platform:         12.5%  ┐
  │     developer:         7.9%  │
  │     guidance:          6.7%  ├─ Third pattern
  │     android:           6.3%  │
  │     support:           8.5%  ┘
  │
  └─► STEP 6: Assign Topic Labels (Human Interpretation)

      Topic 1: "OpenXR Technical Integration"
      Topic 2: "Enterprise Standards & Integration"
      Topic 3: "Cross-Platform Developer Support"

      OUTPUT: Topics with keywords saved to CSV
```

---

## HOW THEY WORK TOGETHER

```
┌────────────────────────────────────────────────────────────────┐
│                   19 XR INTEROPERABILITY SOURCES                │
└────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
    ┌─────────────────┐             ┌─────────────────┐
    │ SENTIMENT       │             │ TOPIC           │
    │ Per document    │             │ Across corpus   │
    └─────────────────┘             └─────────────────┘
              │                               │
              ▼                               ▼
    ┌─────────────────┐             ┌─────────────────┐
    │ 11 Positive     │             │ Topic 1:        │
    │  6 Neutral      │             │   Technical     │
    │  2 Negative     │             │                 │
    │                 │             │ Topic 2:        │
    │ Avg: +0.272     │             │   Enterprise    │
    │                 │             │                 │
    │                 │             │ Topic 3:        │
    │                 │             │   Developer     │
    └─────────────────┘             └─────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
                    ┌──────────────────┐
                    │  DASHBOARD       │
                    │  VISUALIZATION   │
                    └──────────────────┘
```

---

## KEY DIFFERENCES

| Aspect | Sentiment Analysis | Topic Modeling |
|--------|-------------------|----------------|
| **Goal** | Emotion/opinion in text | Themes/subjects in collection |
| **Input** | Single document | Multiple documents |
| **Output** | Score + label (pos/neu/neg) | K topics with keywords |
| **Algorithm** | Lexicon-based (VADER) | Statistical (LDA) |
| **Training** | Pre-trained lexicon | Unsupervised learning |
| **Time** | Fast (milliseconds) | Slower (seconds) |

---

## REAL EXAMPLE WALKTHROUGH

### Input Document
```
"Android Developers Guide: OpenXR provides excellent cross-platform
compatibility with comprehensive support for AR/VR development"
```

### SENTIMENT ANALYSIS PROCESS

```
1. Tokenize: [android, developers, guide, openxr, provides, excellent,
               cross-platform, compatibility, comprehensive, support, ar, vr]

2. Look up scores:
   excellent → +2.7 (strong positive)
   comprehensive → +1.3 (positive)
   support → +0.5 (slight positive)
   [others not in lexicon or neutral]

3. Sum: 2.7 + 1.3 + 0.5 = +4.5

4. Normalize: 4.5 / sqrt(4.5² + 15) = 4.5 / 5.45 = 0.825

5. Result: POSITIVE (0.825 >> 0.05 threshold)
```

### TOPIC MODELING PROCESS

```
1. This document contributes to word counts:
   openxr: +1
   cross-platform: +1
   compatibility: +1
   support: +1
   android: +1
   developers: +1

2. LDA sees this pattern across all 19 docs:

   Documents with "android" + "developers" + "guidance"
   also have "cross-platform" + "support"
   → These words likely belong to same topic

3. After 50 iterations:
   This document is 85% Topic 3 (Developer Support)
                   10% Topic 1 (Technical)
                    5% Topic 2 (Enterprise)

4. Contributes these words to Topic 3:
   android, developers, guidance, cross-platform, support, compatibility
```

---

## WHY THESE METHODS?

### VADER for Sentiment
✅ **Why chosen:**
- Handles mixed sentiments ("excellent BUT fragmentation")
- Understands intensity ("VERY good" vs "somewhat good")
- Works on technical language
- No training data needed

❌ **Limitations:**
- Misses domain-specific sentiment (e.g., "legacy" is neutral in VADER, negative in tech)
- Can't handle sarcasm

### LDA for Topics
✅ **Why chosen:**
- Discovers hidden themes automatically
- Works without labeled data
- Finds word co-occurrence patterns
- Interpretable results (keywords)

❌ **Limitations:**
- Requires choosing K (number of topics) manually
- Ignores word order ("not good" = "good not")
- Topics not always meaningful

---

## STATISTICAL FOUNDATIONS

### VADER Normalization Formula
```
          Σ (sentiment scores)
x = ─────────────────────────────
     √(Σ(sentiment scores)² + α)

where α = 15 (keeps score in [-1, +1] range)
```

### LDA Joint Probability
```
P(words, topics | documents) =

∏ documents [P(topic_dist | doc) ×
∏ words [P(topic | word) × P(word | topic)]]

Solved via Variational Bayes or Gibbs Sampling
```

---

## OUTPUT FILES

### From Sentiment Analysis
```
xr_interop_sentiment.csv
┌──────────────────────┬──────────┬─────────┬────────┐
│ source               │ compound │ label   │ pos    │
├──────────────────────┼──────────┼─────────┼────────┤
│ Android Developers   │  0.784   │ positive│  0.277 │
│ OpenXR Forum         │  0.778   │ positive│  0.315 │
│ Godot Docs           │  0.000   │ neutral │  0.000 │
│ Google Research      │ -0.421   │ negative│  0.000 │
└──────────────────────┴──────────┴─────────┴────────┘
```

### From Topic Modeling
```
xr_interop_topics.csv
┌─────────┬────────────────────────────────────────────────┐
│ topic   │ keywords                                       │
├─────────┼────────────────────────────────────────────────┤
│ Topic 1 │ openxr, interoperability, systems, devices...  │
│ Topic 2 │ standards, enterprise, integration, industry...│
│ Topic 3 │ cross, platform, developer, guidance, android..│
└─────────┴────────────────────────────────────────────────┘
```

---

## SUMMARY

**Sentiment Analysis answers:** *"Is this text positive, negative, or neutral?"*
- Method: Word-by-word scoring + normalization
- Speed: Fast (lexicon lookup)
- Result: Single score per document

**Topic Modeling answers:** *"What themes appear across these documents?"*
- Method: Statistical word co-occurrence patterns
- Speed: Slower (iterative refinement)
- Result: K topics, each with top keywords

Both are **unsupervised** (no human labeling needed) and **deterministic** (same input → same output with fixed random seed).

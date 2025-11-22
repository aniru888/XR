#!/usr/bin/env python3
"""
Check if each dimension actually LOADS pre-computed analytics or computes on-the-fly
"""

import re

files = {
    "📍 Maturity": "dashboard/pages/2_📍_Maturity.py",
    "🔗 Interoperability": "dashboard/pages/3_🔗_Interoperability.py",
    "⚡ Scalability": "dashboard/pages/4_⚡_Scalability.py",
    "🤖 AI Alignment": "dashboard/pages/5_🤖_AI_Alignment.py",
    "💼 Use Cases": "dashboard/pages/6_💼_Use_Cases.py"
}

print("="*80)
print("ANALYTICS IMPLEMENTATION CHECK - ALL 5 DIMENSIONS")
print("="*80)

for name, filepath in files.items():
    print(f"\n{'='*80}")
    print(f"{name}")
    print('='*80)

    with open(filepath, 'r') as f:
        content = f.read()

    # Check for pre-computed file loading
    loads_csv = bool(re.search(r'pd\.read_csv.*sentiment', content) or
                     re.search(r'pd\.read_csv.*topic', content))

    loads_precomputed = bool(re.search(r'sentiment_file|topics_file', content))

    # Check for on-the-fly computation
    computes_sentiment = bool(re.search(r'SentimentAnalyzer\(\)', content))
    computes_topics = bool(re.search(r'TopicModeler\(\)', content))

    # Check for LDA execution
    executes_lda = bool(re.search(r'\.fit\(', content) and 'lda' in content.lower())

    print(f"\n📂 Pre-computed Data:")
    print(f"  Loads CSV files: {'✓ YES' if loads_csv or loads_precomputed else '✗ NO'}")

    print(f"\n⚙️ On-the-fly Computation:")
    print(f"  Computes sentiment: {'✓ YES' if computes_sentiment else '✗ NO'}")
    print(f"  Computes topics: {'✓ YES' if computes_topics else '✗ NO'}")
    print(f"  Executes LDA: {'✓ YES' if executes_lda else '✗ NO'}")

    # Find sentiment implementation
    sentiment_section = re.search(r'### 😊 Sentiment Analysis.*?(?=###|\Z)', content, re.DOTALL)
    if sentiment_section:
        section_text = sentiment_section.group(0)[:500]
        if 'pd.read_csv' in section_text or 'sentiment_file' in section_text:
            print(f"\n  ✅ Sentiment: Loads pre-computed CSV")
        elif 'SentimentAnalyzer()' in section_text:
            print(f"\n  ⚠️  Sentiment: Computes on-the-fly")
        else:
            print(f"\n  ❓ Sentiment: Implementation unclear")

    # Find topic implementation
    topic_section = re.search(r'### 🎯 Topic Modeling.*?(?=###|\Z)', content, re.DOTALL)
    if topic_section:
        section_text = topic_section.group(0)[:500]
        if 'pd.read_csv' in section_text or 'topics_file' in section_text:
            print(f"  ✅ Topics: Loads pre-computed CSV/JSON")
        elif 'TopicModeler()' in section_text:
            print(f"  ⚠️  Topics: Computes on-the-fly")
        else:
            print(f"  ❓ Topics: Implementation unclear")

    # Extract data file paths if mentioned
    data_files = re.findall(r'["\']([^"\']*(?:sentiment|topic|lda)[^"\']*\.(?:csv|json|png))["\']', content, re.IGNORECASE)
    if data_files:
        print(f"\n  📁 Data files referenced:")
        for df in set(data_files):
            print(f"     - {df}")

print(f"\n{'='*80}")
print("SUMMARY")
print('='*80)
print("""
Legend:
  ✅ Loads pre-computed CSV/JSON - Best practice (fast, consistent)
  ⚠️  Computes on-the-fly - Works but slower, may differ from saved results
  ❓ Implementation unclear - Needs review
""")

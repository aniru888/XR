"""
XR_Script_03_Sentiment_Analysis.py
XR Scalability Analytics: Confidence in scaling solutions
Purpose: Quantify optimism/skepticism about XR scalability
Author: Mathemagica 2.0 Data Science Team
Date: November 2024
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class XR_SentimentAnalyzer:
    """Analyzes sentiment regarding XR scalability challenges"""

    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

        # Define XR scalability challenge themes
        self.challenge_keywords = {
            'latency': ['latency', 'lag', 'delay', 'response time', 'jitter'],
            'bandwidth': ['bandwidth', 'throughput', 'network capacity', 'mbps', 'gbps'],
            'cost': ['cost', 'expensive', 'budget', 'investment', 'price'],
            'complexity': ['complex', 'difficult', 'challenge', 'bottleneck', 'limitation'],
            'device_mgmt': ['provisioning', 'management', 'fleet', 'deployment', 'onboarding'],
            'infrastructure': ['infrastructure', 'architecture', 'platform', 'compute', 'rendering']
        }

    def analyze_sentiment_vader(self, text):
        """VADER sentiment analysis"""
        scores = self.vader.polarity_scores(text)
        return scores['compound']  # -1 to +1

    def classify_sentiment(self, score):
        """Classify sentiment into categories"""
        if score >= 0.10:
            return 'Positive'
        elif score <= -0.10:
            return 'Negative'
        else:
            return 'Neutral'

    def extract_theme_sentiment(self, text):
        """Extract sentiment for each challenge theme"""
        theme_sentiments = {}

        for theme, keywords in self.challenge_keywords.items():
            # Check if any keyword present
            has_keyword = any(kw in text.lower() for kw in keywords)

            if has_keyword:
                sentiment = self.analyze_sentiment_vader(text)
                theme_sentiments[theme] = sentiment
            else:
                theme_sentiments[theme] = None

        return theme_sentiments

    def process_corpus(self, df):
        """Process entire corpus for sentiment"""

        results = []

        for idx, row in df.iterrows():
            text = row.get('cleaned_text', '')
            if pd.isna(text) or len(text) < 10:
                continue

            # Overall sentiment
            global_sentiment = self.analyze_sentiment_vader(text)

            # Theme-specific sentiment
            theme_sentiments = self.extract_theme_sentiment(text)

            result = {
                'record_id': idx,
                'aspect': row.get('aspect', 'Unknown'),
                'category': row.get('category', 'Unknown'),
                'global_sentiment_score': global_sentiment,
                'global_sentiment_class': self.classify_sentiment(global_sentiment)
            }

            # Add theme sentiments
            for theme, sentiment in theme_sentiments.items():
                result[f'theme_{theme}_sentiment'] = sentiment
                if sentiment is not None:
                    result[f'theme_{theme}_class'] = self.classify_sentiment(sentiment)

            results.append(result)

        return pd.DataFrame(results)

    def generate_summary(self, sentiment_df):
        """Generate sentiment summary"""

        print("\n" + "=" * 80)
        print("XR SCALABILITY SENTIMENT ANALYSIS SUMMARY")
        print("=" * 80)

        # Overall distribution
        print("\n--- GLOBAL SENTIMENT DISTRIBUTION ---")
        sentiment_counts = sentiment_df['global_sentiment_class'].value_counts()
        for sentiment, count in sentiment_counts.items():
            pct = (count / len(sentiment_df)) * 100
            print(f"  {sentiment}: {count} ({pct:.1f}%)")

        avg_sentiment = sentiment_df['global_sentiment_score'].mean()
        print(f"\n  Average sentiment score: {avg_sentiment:.3f}")

        if avg_sentiment > 0.1:
            print("  💡 INSIGHT: Industry is OPTIMISTIC about scaling solutions")
        elif avg_sentiment < -0.1:
            print("  ⚠️  INSIGHT: Industry is SKEPTICAL (concerns about feasibility)")
        else:
            print("  ℹ️  INSIGHT: BALANCED views on scalability challenges")

        # By aspect
        print("\n--- SENTIMENT BY XR ASPECT ---")
        for aspect in sentiment_df['aspect'].unique():
            aspect_df = sentiment_df[sentiment_df['aspect'] == aspect]
            avg_score = aspect_df['global_sentiment_score'].mean()
            print(f"  {aspect}: {avg_score:.3f}")

        # Theme-specific analysis
        print("\n--- CHALLENGE THEME SENTIMENT ---")
        theme_cols = [col for col in sentiment_df.columns if col.startswith('theme_') and col.endswith('_sentiment')]

        for col in theme_cols:
            theme_name = col.replace('theme_', '').replace('_sentiment', '').replace('_', ' ').title()
            theme_scores = sentiment_df[col].dropna()
            if len(theme_scores) > 0:
                avg_score = theme_scores.mean()
                print(f"  {theme_name}: {avg_score:.3f} ({len(theme_scores)} mentions)")

def main():
    """Main execution"""

    print("=" * 80)
    print("XR SCALABILITY: SENTIMENT ANALYSIS")
    print("=" * 80)

    # Load processed corpus
    try:
        df = pd.read_csv('XR_Processed_Master_Corpus.csv')
        print(f"[OK] Loaded corpus: {len(df)} records")
    except FileNotFoundError:
        print("[ERR] Error: XR_Processed_Master_Corpus.csv not found")
        print("Please run XR_Script_01_Data_Ingestion_Cleaning.py first.")
        return

    # Initialize analyzer
    analyzer = XR_SentimentAnalyzer()

    # Process corpus
    print("\nAnalyzing sentiment...")
    sentiment_results = analyzer.process_corpus(df)

    # Save results
    sentiment_results.to_csv('XR_Sentiment_Analysis_Results.csv', index=False)
    print(f"\n[OK] Sentiment analysis complete. Saved to XR_Sentiment_Analysis_Results.csv")
    
    # Generate summary
    summary = analyzer.generate_summary(sentiment_results)
    summary.to_csv('XR_Sentiment_Summary.csv')
    print(f"[OK] Summary saved to XR_Sentiment_Summary.csv")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

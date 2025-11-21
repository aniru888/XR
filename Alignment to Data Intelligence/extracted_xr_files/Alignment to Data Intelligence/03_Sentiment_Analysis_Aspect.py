# 03_Sentiment_Analysis_Aspect.py
# IEMT Social Data Analytics Methodology: Aspect-Based Sentiment Analysis (ABSA)
# This script calculates Sentiment (Polarity) and Controversy (Variance) for specific dimensions.

import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np

def run_absa(df):
    aspects_data = {
        "Privacy": ["privacy", "security", "surveillance", "data", "ethics"],
        "Efficiency": ["efficiency", "roi", "manufacturing", "industrial", "productivity"],
        "Innovation": ["innovation", "future", "technology", "advancement", "breakthrough"],
        "Safety": ["safety", "risk", "danger", "hazard", "accident"]
    }

    aspect_metrics = []

    print("Calculating Aspect-Based Sentiment...")
    for name, keywords in aspects_data.items():
        pattern = '|'.join(keywords)
        subset = df[df['Text'].str.contains(pattern, case=False, na=False)]
        
        if not subset.empty:
            # Calculate individual scores
            scores = subset['Text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
            
            # Metrics
            avg_sentiment = scores.mean()
            controversy = scores.std() # Standard Deviation as proxy for Controversy
            
            aspect_metrics.append({
                "Aspect": name, 
                "Sentiment": avg_sentiment,
                "Controversy": controversy,
                "Count": len(subset)
            })
            print(f"  {name}: Sentiment={avg_sentiment:.2f}, Controversy={controversy:.2f}")

    sent_df = pd.DataFrame(aspect_metrics)
    
    # Visualization
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    colors = ['#E15759' if s < 0 else '#59A14F' for s in sent_df['Sentiment']]
    bars = ax1.bar(sent_df['Aspect'], sent_df['Sentiment'], color=colors, alpha=0.8, label='Net Sentiment')
    ax1.set_ylabel('Net Sentiment Polarity', fontsize=12, fontweight='bold')
    ax1.set_ylim(-0.6, 0.6)
    ax1.axhline(0, color='black', linewidth=1)
    
    # Error bars for Controversy
    ax1.errorbar(sent_df['Aspect'], sent_df['Sentiment'], yerr=sent_df['Controversy'], 
                 fmt='o', color='black', capsize=5, label='Controversy (Std Dev)')
    
    ax1.set_title('Aspect-Based Sentiment & Controversy Analysis', fontsize=16, fontweight='bold')
    ax1.legend()
    plt.savefig("output_05_sentiment_aspects.png", dpi=300, bbox_inches='tight')
    print("[OK] Saved visualization to output_05_sentiment_aspects.png")

if __name__ == "__main__":
    try:
        df = pd.read_csv("XR_Cleaned_Data.csv")
        run_absa(df)
    except FileNotFoundError:
        print("Error: XR_Cleaned_Data.csv not found.")

"""
XR_Script_02_Word_Cloud_Analysis.py
XR Scalability Analytics: Dominant infrastructure theme visualization
Purpose: Generate word clouds for each XR scalability aspect
Author: Mathemagica 2.0 Data Science Team
Date: November 2024
"""

import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import os

class XR_WordCloudGenerator:
    """Generates XR-specific word clouds"""

    def __init__(self, width=1400, height=700, max_words=120):
        self.width = width
        self.height = height
        self.max_words = max_words

        # Custom stopwords for XR context
        self.xr_stopwords = {
            'xr', 'ar', 'vr', 'mr', 'extended', 'reality',
            'enterprise', 'solution', 'scale', 'scaling'
        }

    def generate_cloud(self, text_data, title, filename, colormap='viridis'):
        """Generate and save word cloud"""

        wordcloud = WordCloud(
            width=self.width,
            height=self.height,
            background_color='white',
            max_words=self.max_words,
            relative_scaling=0.5,
            min_font_size=10,
            colormap=colormap,
            stopwords=self.xr_stopwords,
            collocations=False  # Prevents duplicate words
        ).generate(text_data)

        # Create figure
        fig, ax = plt.subplots(figsize=(16, 9))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
        ax.axis('off')

        # Save
        plt.tight_layout(pad=0)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"[OK] Word cloud: {filename}")

    def get_top_words(self, text_data, top_n=25):
        """Extract top N words"""
        words = text_data.split()
        word_freq = Counter(words)
        return word_freq.most_common(top_n)

    def generate_aspect_clouds(self, df, output_dir='xr_wordclouds'):
        """Generate word clouds for each aspect"""

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        aspects = df['aspect'].unique()

        # Color maps for each aspect
        colormaps = {
            '5G/6G Connectivity': 'Blues',
            'Edge Computing': 'Greens',
            'Cloud Rendering': 'Purples',
            'MDM': 'Oranges',
            'Infrastructure Scaling': 'Reds'
        }

        for aspect in aspects:
            aspect_df = df[df['aspect'] == aspect]
            aspect_text = ' '.join(aspect_df['token_string'].dropna().astype(str))

            if len(aspect_text) > 100:
                title = f'XR Scalability: {aspect} (n={len(aspect_df)})'
                filename = os.path.join(output_dir, f'{aspect.replace("/", "_").replace(" ", "_").lower()}.png')
                colormap = colormaps.get(aspect, 'viridis')

                self.generate_cloud(aspect_text, title, filename, colormap)

                # Print top words
                top_words = self.get_top_words(aspect_text, top_n=15)
                print(f"\n  Top words ({aspect}):")
                for word, freq in top_words[:10]:
                    print(f"    {word}: {freq}")

    def generate_aggregate_cloud(self, df, output_dir='xr_wordclouds'):
        """Generate aggregate word cloud"""

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        all_text = ' '.join(df['token_string'].dropna().astype(str))

        title = f'XR Scalability: Aggregate Landscape (n={len(df)})'
        filename = os.path.join(output_dir, 'xr_aggregate_scalability.png')

        self.generate_cloud(all_text, title, filename, 'plasma')

        # Print top words
        top_words = self.get_top_words(all_text, top_n=30)
        print(f"\nTop 30 words (aggregate):")
        for word, freq in top_words:
            print(f"  {word}: {freq}")

def main():
    """Main execution"""

    print("=" * 80)
    print("XR SCALABILITY: WORD CLOUD ANALYSIS")
    print("=" * 80)

    # Load processed corpus
    try:
        df = pd.read_csv('XR_Processed_Master_Corpus.csv')
        print(f"Loaded corpus: {len(df)} records, {df['aspect'].nunique()} aspects")
    except FileNotFoundError:
        print("[ERR] Error: XR_Processed_Master_Corpus.csv not found")
        print("Please run XR_Script_01_Data_Ingestion_Cleaning.py first.")
        return

    # Initialize generator
    generator = XR_WordCloudGenerator()

    # Generate aggregate word cloud
    print("\n--- AGGREGATE WORD CLOUD ---")
    generator.generate_aggregate_cloud(df)

    # Generate aspect-specific word clouds
    print("\n--- ASPECT-SPECIFIC WORD CLOUDS ---")
    generator.generate_aspect_clouds(df)

    print("\n" + "=" * 80)
    print("OUTPUT: Word clouds saved to ./xr_wordclouds/ directory")
    print("=" * 80)

if __name__ == "__main__":
    main()

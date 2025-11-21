# 02_Word_Cloud_Generation.py
# IEMT Social Data Analytics Methodology: Visualization
# This script generates optimized, unique-token Word Clouds for different dimensions.

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def generate_wc(text_list, title, filename, colormap='magma'):
    if not text_list:
        print(f"  [!] No data for {title}")
        return
    
    combined = " ".join(text_list)
    
    # Configuration for uniqueness and aesthetics
    # collocations=False is CRITICAL to prevent repeated bigrams
    wc = WordCloud(width=1600, height=800, 
                   background_color='white', 
                   colormap=colormap, 
                   max_words=150,
                   collocations=False, 
                   regexp=r"\w[\w']+"
                   ).generate(combined)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20, color='#333333')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {filename}")

if __name__ == "__main__":
    print("Loading data...")
    try:
        df = pd.read_csv("XR_Cleaned_Data.csv")
        
        # 1. Global Cloud
        print("Generating Global Cloud...")
        generate_wc(df['Cleaned_Text'].fillna('').tolist(), 
                    "Global XR Discourse: Dominant Themes", 
                    "output_02_wordcloud_global.png",
                    colormap='magma')
        
        # 2. Privacy Cloud
        print("Generating Privacy Cloud...")
        privacy_df = df[df['Text'].str.contains("Privacy|Security|Surveillance", case=False, na=False)]
        generate_wc(privacy_df['Cleaned_Text'].fillna('').tolist(), 
                    "Privacy & Security: Key Concerns", 
                    "output_03_wordcloud_privacy.png",
                    colormap='inferno')
        
        # 3. Efficiency Cloud
        print("Generating Efficiency Cloud...")
        efficiency_df = df[df['Text'].str.contains("Efficiency|Industrial|Manufacturing|ROI", case=False, na=False)]
        generate_wc(efficiency_df['Cleaned_Text'].fillna('').tolist(), 
                    "Industrial Efficiency: Value Drivers", 
                    "output_04_wordcloud_efficiency.png",
                    colormap='viridis')
                    
    except FileNotFoundError:
        print("Error: XR_Cleaned_Data.csv not found. Run 01_Data_Ingestion_Cleaning.py first.")

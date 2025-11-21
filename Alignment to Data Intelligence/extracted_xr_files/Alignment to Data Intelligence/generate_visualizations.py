# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

print("="*60)
print("MATHEMAGICA 2.0: Professional Analytics Suite")
print("="*60)

# --- LOAD DATA ---
print("\n[1/6] Loading cleaned data...")
try:
    df = pd.read_csv("XR_Cleaned_Data.csv")
    print(f"[OK] Loaded {len(df)} documents")
except FileNotFoundError:
    print("[X] Cleaned data not found. Please run 01_Data_Ingestion_Cleaning.py first")
    exit(1)

# --- VISUALIZATION 1: SOURCE DISTRIBUTION ---
print("\n[2/6] Generating Source Distribution pie chart...")
if 'Source_Type' in df.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    source_counts = df['Source_Type'].value_counts()
    # Professional color palette (Tableau 10 style)
    colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2']
    
    wedges, texts, autotexts = ax.pie(source_counts, labels=source_counts.index, autopct='%1.1f%%', 
                                      colors=colors, startangle=90, pctdistance=0.85)
    
    # Draw circle for Donut Chart (Modern look)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    ax.set_title("Document Distribution by Source Type", fontsize=16, fontweight='bold')
    plt.setp(autotexts, size=10, weight="bold", color="white")
    plt.setp(texts, size=12)
    
    plt.savefig("output_01_source_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: output_01_source_distribution.png")

# --- VISUALIZATION 2: WORD CLOUDS ---
print("\n[3/6] Generating Optimized Word Clouds...")

def generate_wc(text_list, title, filename, colormap='magma'):
    if not text_list:
        print(f"  [!] No data for {title}")
        return
    
    # Deduplicate words within the text list to ensure "prominent" means "frequent across documents"
    # not just "repeated in one document"
    combined = " ".join(text_list)
    
    # Configuration for uniqueness and aesthetics
    wc = WordCloud(width=1600, height=800, 
                   background_color='white', 
                   colormap=colormap, 
                   max_words=150,
                   collocations=False, # CRITICAL: Prevents repeated bigrams (e.g. "Spatial Computing" + "Spatial")
                   stopwords=None, # Stopwords already handled in cleaning
                   regexp=r"\w[\w']+"
                   ).generate(combined)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20, color='#333333')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Saved: {filename}")

# Global - Magma for high contrast
generate_wc(df['Cleaned_Text'].fillna('').tolist(), 
            "Global XR Discourse: Dominant Themes", 
            "output_02_wordcloud_global.png",
            colormap='magma')

# Privacy - Reds/Inferno for "Warning/Heat"
privacy_df = df[df['Text'].str.contains("Privacy|Security|Surveillance", case=False, na=False)]
generate_wc(privacy_df['Cleaned_Text'].fillna('').tolist(), 
            "Privacy & Security: Key Concerns", 
            "output_03_wordcloud_privacy.png",
            colormap='inferno')

# Efficiency - Viridis/Greens for "Growth/Money"
efficiency_df = df[df['Text'].str.contains("Efficiency|Industrial|Manufacturing|ROI", case=False, na=False)]
generate_wc(efficiency_df['Cleaned_Text'].fillna('').tolist(), 
            "Industrial Efficiency: Value Drivers", 
            "output_04_wordcloud_efficiency.png",
            colormap='viridis')

# --- VISUALIZATION 3: ASPECT-BASED SENTIMENT ---
print("\n[4/6] Generating Advanced Sentiment Analysis...")

aspects_data = {
    "Privacy": ["privacy", "security", "surveillance", "data", "ethics"],
    "Efficiency": ["efficiency", "roi", "manufacturing", "industrial", "productivity"],
    "Innovation": ["innovation", "future", "technology", "advancement", "breakthrough"],
    "Safety": ["safety", "risk", "danger", "hazard", "accident"]
}

aspect_metrics = []

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

sent_df = pd.DataFrame(aspect_metrics)

# Dual-Axis Plot: Sentiment (Bar) vs Controversy (Line/Error Bar)
fig, ax1 = plt.subplots(figsize=(12, 7))

# Bar Chart for Sentiment
colors = ['#E15759' if s < 0 else '#59A14F' for s in sent_df['Sentiment']]
bars = ax1.bar(sent_df['Aspect'], sent_df['Sentiment'], color=colors, alpha=0.8, label='Net Sentiment')
ax1.set_ylabel('Net Sentiment Polarity (-1 to +1)', fontsize=12, fontweight='bold')
ax1.set_ylim(-0.6, 0.6)
ax1.axhline(0, color='black', linewidth=1)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + (0.02 if height > 0 else -0.05),
             f'{height:.2f}', ha='center', va='bottom', fontweight='bold')

# Controversy (Variance) as Error Bars or separate marker
# We'll use error bars to show the "spread" of opinion
ax1.errorbar(sent_df['Aspect'], sent_df['Sentiment'], yerr=sent_df['Controversy'], 
             fmt='o', color='black', capsize=5, label='Controversy (Std Dev)')

ax1.set_title('Aspect-Based Sentiment & Controversy Analysis', fontsize=16, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("output_05_sentiment_aspects.png", dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Saved: output_05_sentiment_aspects.png")

# --- VISUALIZATION 4: LDA TOPIC MODELING ---
print("\n[5/6] Generating LDA Topic Model...")

cv = CountVectorizer(max_df=0.95, min_df=2, stop_words='english', max_features=1000)
dtm = cv.fit_transform(df['Cleaned_Text'].fillna(''))

n_topics = 4
lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, max_iter=20)
lda.fit(dtm)

feature_names = cv.get_feature_names_out()

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
axes = axes.flatten()

# Dynamic Labeling based on top words (simple heuristic)
topic_labels = []
for idx, topic in enumerate(lda.components_):
    top_indices = topic.argsort()[:-4:-1]
    top_w = [feature_names[i] for i in top_indices]
    topic_labels.append(f"Topic {idx+1}\n({', '.join(top_w)})")

colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2']

for idx, ax in enumerate(axes):
    if idx < n_topics:
        top_indices = lda.components_[idx].argsort()[:-11:-1]
        top_words = [feature_names[i] for i in top_indices]
        top_weights = [lda.components_[idx][i] for i in top_indices]
        
        ax.barh(range(10), top_weights, color=colors[idx])
        ax.set_yticks(range(10))
        ax.set_yticklabels(top_words, fontsize=11)
        ax.invert_yaxis()
        ax.set_xlabel('Weight', fontsize=10)
        ax.set_title(topic_labels[idx], fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

plt.suptitle('Latent Dirichlet Allocation (LDA): Discovered Thematic Clusters', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig("output_06_lda_topics.png", dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Saved: output_06_lda_topics.png")

# --- VISUALIZATION 5: KEY METRICS SUMMARY ---
print("\n[6/6] Generating Executive Summary...")

fig = plt.figure(figsize=(16, 9))
gs = fig.add_gridspec(3, 4, hspace=0.4, wspace=0.3)

# Metric boxes
ax1 = fig.add_subplot(gs[0, 0])
ax1.text(0.5, 0.6, f"{len(df)}", ha='center', va='center', fontsize=48, fontweight='bold', color='#4E79A7')
ax1.text(0.5, 0.2, "Total Documents", ha='center', va='center', fontsize=14, color='#555')
ax1.axis('off')

ax2 = fig.add_subplot(gs[0, 1])
ax2.text(0.5, 0.6, f"{n_topics}", ha='center', va='center', fontsize=48, fontweight='bold', color='#F28E2B')
ax2.text(0.5, 0.2, "Thematic Clusters", ha='center', va='center', fontsize=14, color='#555')
ax2.axis('off')

ax3 = fig.add_subplot(gs[0, 2])
sentiment_avg = sent_df['Sentiment'].mean()
color_sent = '#59A14F' if sentiment_avg > 0 else '#E15759'
ax3.text(0.5, 0.6, f"{sentiment_avg:+.2f}", ha='center', va='center', fontsize=48, fontweight='bold', color=color_sent)
ax3.text(0.5, 0.2, "Avg Global Sentiment", ha='center', va='center', fontsize=14, color='#555')
ax3.axis('off')

ax4 = fig.add_subplot(gs[0, 3])
max_controversy = sent_df.loc[sent_df['Controversy'].idxmax()]
ax4.text(0.5, 0.6, f"{max_controversy['Aspect']}", ha='center', va='center', fontsize=24, fontweight='bold', color='#E15759')
ax4.text(0.5, 0.2, "Most Controversial", ha='center', va='center', fontsize=14, color='#555')
ax4.axis('off')

# Sentiment vs Controversy Scatter
ax5 = fig.add_subplot(gs[1:, :])
# Plot scatter
scatter = ax5.scatter(sent_df['Sentiment'], sent_df['Controversy'], 
                     s=sent_df['Count']*5, # Size by volume
                     c=sent_df['Sentiment'], cmap='RdYlGn', alpha=0.7, edgecolors='black')

ax5.set_xlabel('Net Sentiment (Negative <-> Positive)', fontsize=12, fontweight='bold')
ax5.set_ylabel('Controversy (Standard Deviation)', fontsize=12, fontweight='bold')
ax5.set_title('Strategic Matrix: Sentiment vs. Controversy', fontsize=16, fontweight='bold')
ax5.grid(True, linestyle='--', alpha=0.5)
ax5.axvline(0, color='black', linestyle='-', alpha=0.3)

# Annotate points
for i, txt in enumerate(sent_df['Aspect']):
    ax5.annotate(txt, (sent_df['Sentiment'][i], sent_df['Controversy'][i]), 
                 xytext=(5, 5), textcoords='offset points', fontsize=12, fontweight='bold')

plt.suptitle('Mathemagica 2.0: Executive Strategic Dashboard', fontsize=20, fontweight='bold', y=0.98)
plt.savefig("output_07_executive_summary.png", dpi=300, bbox_inches='tight')
plt.close()
print("[OK] Saved: output_07_executive_summary.png")

print("\n" + "="*60)
print("[OK] All visualizations generated successfully!")
print("="*60)

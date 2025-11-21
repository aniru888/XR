"""
XR_Script_04_Topic_Modeling_LDA.py
XR Scalability Analytics: Extract distinct scaling challenge themes
Purpose: Latent Dirichlet Allocation for XR scalability topics
Author: Mathemagica 2.0 Data Science Team
Date: November 2024
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class XR_TopicModeler:
    """LDA-based topic modeling for XR scalability"""

    def __init__(self, n_topics=3, max_iter=20, random_state=42):
        self.n_topics = n_topics
        self.max_iter = max_iter
        self.random_state = random_state
        self.lda_model = None
        self.vectorizer = None

    def fit_lda(self, texts):
        """Fit LDA model"""

        print(f"\nFitting LDA model with {self.n_topics} topics...")

        # Create document-term matrix
        self.vectorizer = CountVectorizer(
            max_df=0.85,
            min_df=2,
            stop_words='english',
            max_features=1000
        )

        doc_term_matrix = self.vectorizer.fit_transform(texts)
        print(f"[OK] Document-term matrix: {doc_term_matrix.shape}")

        # Fit LDA
        self.lda_model = LatentDirichletAllocation(
            n_components=self.n_topics,
            max_iter=self.max_iter,
            learning_method='online',
            random_state=self.random_state,
            n_jobs=-1
        )

        self.lda_model.fit(doc_term_matrix)
        print(f"[OK] LDA model fitted")

        return doc_term_matrix

    def display_topics(self, n_words=12):
        """Display top words per topic with XR-specific labels"""

        if self.lda_model is None:
            print("[ERR] Model not fitted")
            return

        feature_names = self.vectorizer.get_feature_names_out()

        print(f"\n{'=' * 80}")
        print(f"XR SCALABILITY: TOP {n_words} WORDS PER TOPIC")
        print(f"{'=' * 80}")

        # XR-specific topic labeling heuristics
        topic_labels = {
            'network': '[NETWORK INFRASTRUCTURE: 5G/Edge/Latency]',
            'cloud': '[CLOUD RENDERING: GPU/Streaming/Remote]',
            'device': '[DEVICE MANAGEMENT: MDM/Fleet/Provisioning]',
            'infrastructure': '[INFRASTRUCTURE: Scale/Multi-user/Deployment]',
            'compute': '[EDGE COMPUTING: Processing/CDN/Distributed]'
        }

        for topic_idx, topic in enumerate(self.lda_model.components_):
            top_indices = topic.argsort()[-n_words:][::-1]
            top_words = [feature_names[i] for i in top_indices]
            top_weights = [topic[i] for i in top_indices]

            # Auto-label based on keywords
            label = '[GENERAL SCALING THEME]'
            for key, lbl in topic_labels.items():
                if key in top_words or any(key in w for w in top_words[:5]):
                    label = lbl
                    break

            print(f"\nTOPIC {topic_idx + 1}: {label}")
            for i, (word, weight) in enumerate(zip(top_words, top_weights), 1):
                print(f"    {i:2d}. {word:20s} (weight: {weight:.4f})")

    def get_document_topics(self, doc_term_matrix):
        """Get topic distribution for documents"""

        if self.lda_model is None:
            return None

        doc_topic_dist = self.lda_model.transform(doc_term_matrix)

        print(f"\nDocument-topic matrix: {doc_topic_dist.shape}")
        print(f"Average topic distribution:")

        for topic_idx in range(self.n_topics):
            avg_dist = doc_topic_dist[:, topic_idx].mean()
            print(f"  Topic {topic_idx + 1}: {avg_dist:.4f}")

        return doc_topic_dist

def main():
    """Main execution"""

    print("=" * 80)
    print("XR SCALABILITY: TOPIC MODELING (LDA)")
    print("=" * 80)

    # Load processed corpus
    try:
        df = pd.read_csv('XR_Processed_Master_Corpus.csv')
        print(f"[OK] Loaded corpus: {len(df)} records")
    except FileNotFoundError:
        print("[ERR] Error: XR_Processed_Master_Corpus.csv not found")
        print("Please run XR_Script_01_Data_Ingestion_Cleaning.py first.")
        return

    # Prepare texts
    texts = df['cleaned_text'].dropna().astype(str).tolist()
    print(f"[OK] Prepared {len(texts)} documents for modeling")

    # Initialize and fit LDA
    modeler = XR_TopicModeler(n_topics=3, max_iter=25)
    doc_term_matrix = modeler.fit_lda(texts)

    # Display topics
    modeler.display_topics(n_words=12)

    # Get document-topic distribution
    doc_topic_dist = modeler.get_document_topics(doc_term_matrix)

    # Save results
    if doc_topic_dist is not None:
        topic_df = pd.DataFrame(
            doc_topic_dist,
            columns=[f'Topic_{i+1}' for i in range(modeler.n_topics)]
        )
        topic_df.to_csv('XR_LDA_Topic_Distribution.csv', index=False)
        print(f"\n[OK] Saved: XR_LDA_Topic_Distribution.csv")

    print("\n" + "=" * 80)
    print("INTERPRETATION:")
    print("  Topics represent latent XR scalability challenges")
    print("  Each topic = mixture of infrastructure keywords")
    print("  Overlapping topics reflect integrated scaling approach")
    print("=" * 80)

if __name__ == "__main__":
    main()

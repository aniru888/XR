"""
Reusable Text Analytics Utilities
Word Cloud Generation, Sentiment Analysis, Topic Modeling (LDA)
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re
from pathlib import Path


class TextPreprocessor:
    """Text preprocessing utilities"""

    def __init__(self):
        """Initialize preprocessor with stopwords"""
        self.stopwords = set(STOPWORDS)

        # Add XR-specific stopwords
        self.stopwords.update([
            'will', 'use', 'using', 'used', 'one', 'two', 'three',
            'also', 'may', 'can', 'could', 'would', 'should',
            'http', 'https', 'www', 'com', 'org', 'net', 'html'
        ])

        # Add metadata/source type stopwords
        self.stopwords.update([
            'blog', 'post', 'article', 'paper', 'study', 'research',
            'report', 'whitepaper', 'document', 'publication',
            'abstract', 'journal', 'news', 'newsroom', 'press',
            'linkedin', 'twitter', 'facebook', 'social', 'media',
            'professional', 'network', 'forum', 'reddit',
            'google', 'scholar', 'microsoft', 'meta', 'facebook',
            'developer', 'developers', 'insights', 'deloitte',
            'pwc', 'gartner', 'forrester', 'idc', 'industry',
            'case', 'source', 'sources', 'link', 'links', 'url'
        ])

        # Add generic filler words
        self.stopwords.update([
            'said', 'says', 'saying', 'according', 'stated',
            'announced', 'announced', 'released', 'launched',
            'introduced', 'presented', 'published', 'reported'
        ])

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text or pd.isna(text):
            return ""

        text = str(text).lower()
        # Remove URLs more comprehensively
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'www\.[a-zA-Z0-9\-\.]+\.[a-z]{2,}', '', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

    def remove_stopwords(self, text: str) -> str:
        """Remove stopwords from text"""
        words = text.split()
        # Filter out stopwords and very short words (< 3 chars)
        filtered = [w for w in words if w not in self.stopwords and len(w) > 2]
        return ' '.join(filtered)

    def preprocess(self, text: str, remove_stops: bool = True) -> str:
        """Full preprocessing pipeline"""
        text = self.clean_text(text)
        if remove_stops:
            text = self.remove_stopwords(text)
        return text


class WordCloudGenerator:
    """Generate word clouds from text corpus"""

    def __init__(self, width: int = 800, height: int = 400):
        """
        Initialize word cloud generator

        Args:
            width: Image width in pixels
            height: Image height in pixels
        """
        self.width = width
        self.height = height
        self.preprocessor = TextPreprocessor()

    def generate(
        self,
        text: str,
        max_words: int = 100,
        background_color: str = 'white',
        colormap: str = 'viridis',
        preprocess: bool = True
    ) -> WordCloud:
        """
        Generate word cloud from text

        Args:
            text: Input text corpus
            max_words: Maximum number of words to display
            background_color: Background color
            colormap: Matplotlib colormap name
            preprocess: Whether to preprocess text

        Returns:
            WordCloud object
        """
        if preprocess:
            text = self.preprocessor.preprocess(text)

        if not text.strip():
            # Return empty word cloud with placeholder
            text = "no data available"

        wordcloud = WordCloud(
            width=self.width,
            height=self.height,
            max_words=max_words,
            background_color=background_color,
            colormap=colormap,
            stopwords=self.preprocessor.stopwords,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text)

        return wordcloud

    def save(self, wordcloud: WordCloud, output_path: Path):
        """Save word cloud to file"""
        wordcloud.to_file(str(output_path))

    def plot(self, wordcloud: WordCloud, title: str = "Word Cloud"):
        """Plot word cloud using matplotlib"""
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        return fig

    def get_top_words(self, text: str, n: int = 20) -> List[Tuple[str, int]]:
        """
        Get top N most frequent words

        Returns:
            List of (word, frequency) tuples
        """
        text = self.preprocessor.preprocess(text)
        words = text.split()
        from collections import Counter
        word_counts = Counter(words)
        return word_counts.most_common(n)


class SentimentAnalyzer:
    """Sentiment analysis using TextBlob"""

    def __init__(self):
        """Initialize sentiment analyzer"""
        self.preprocessor = TextPreprocessor()

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text

        Returns:
            Dictionary with polarity, subjectivity, and classification
        """
        if not text or pd.isna(text):
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'classification': 'neutral'
            }

        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Classify sentiment
        if polarity > 0.1:
            classification = 'positive'
        elif polarity < -0.1:
            classification = 'negative'
        else:
            classification = 'neutral'

        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'classification': classification
        }

    def analyze_corpus(self, texts: List[str]) -> pd.DataFrame:
        """
        Analyze sentiment for a list of texts

        Returns:
            DataFrame with sentiment scores for each text
        """
        results = []
        for i, text in enumerate(texts):
            sentiment = self.analyze_text(text)
            sentiment['text_id'] = i
            sentiment['text_preview'] = str(text)[:100] if text else ""
            results.append(sentiment)

        return pd.DataFrame(results)

    def get_summary_stats(self, sentiments: pd.DataFrame) -> Dict:
        """
        Get summary statistics for sentiment analysis

        Returns:
            Dictionary with averages, distributions, percentages
        """
        if sentiments.empty:
            return {
                'avg_polarity': 0.0,
                'avg_subjectivity': 0.0,
                'positive_pct': 0.0,
                'negative_pct': 0.0,
                'neutral_pct': 0.0
            }

        total = len(sentiments)
        value_counts = sentiments['classification'].value_counts()

        return {
            'avg_polarity': sentiments['polarity'].mean(),
            'avg_subjectivity': sentiments['subjectivity'].mean(),
            'positive_pct': (value_counts.get('positive', 0) / total) * 100,
            'negative_pct': (value_counts.get('negative', 0) / total) * 100,
            'neutral_pct': (value_counts.get('neutral', 0) / total) * 100,
            'total_analyzed': total
        }

    def plot_distribution(self, sentiments: pd.DataFrame, title: str = "Sentiment Distribution"):
        """Plot sentiment distribution"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Classification bar chart
        class_counts = sentiments['classification'].value_counts()
        colors = {'positive': '#00C9A7', 'neutral': '#6C757D', 'negative': '#DC3545'}
        class_colors = [colors.get(c, '#6C757D') for c in class_counts.index]

        ax1.bar(class_counts.index, class_counts.values, color=class_colors)
        ax1.set_title('Sentiment Classification', fontweight='bold')
        ax1.set_ylabel('Count')

        # Polarity histogram
        ax2.hist(sentiments['polarity'], bins=20, color='#0066CC', alpha=0.7, edgecolor='black')
        ax2.axvline(x=0, color='red', linestyle='--', linewidth=1)
        ax2.set_title('Polarity Distribution', fontweight='bold')
        ax2.set_xlabel('Polarity Score')
        ax2.set_ylabel('Frequency')

        fig.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig


class TopicModeler:
    """Topic modeling using Latent Dirichlet Allocation (LDA)"""

    def __init__(self, n_topics: int = 5, random_state: int = 42):
        """
        Initialize topic modeler

        Args:
            n_topics: Number of topics to extract
            random_state: Random seed for reproducibility
        """
        self.n_topics = n_topics
        self.random_state = random_state
        self.preprocessor = TextPreprocessor()
        self.vectorizer = None
        self.lda_model = None
        self.feature_names = None

    def fit(self, texts: List[str], max_features: int = 1000) -> 'TopicModeler':
        """
        Fit LDA model on text corpus

        Args:
            texts: List of text documents
            max_features: Maximum number of features (vocabulary size)

        Returns:
            Self for method chaining
        """
        # Preprocess texts
        processed_texts = [self.preprocessor.preprocess(text) for text in texts]

        # Vectorize
        self.vectorizer = CountVectorizer(
            max_features=max_features,
            max_df=0.85,
            min_df=2,
            stop_words='english'
        )

        doc_term_matrix = self.vectorizer.fit_transform(processed_texts)
        self.feature_names = self.vectorizer.get_feature_names_out()

        # Fit LDA
        self.lda_model = LatentDirichletAllocation(
            n_components=self.n_topics,
            random_state=self.random_state,
            max_iter=20,
            learning_method='online',
            n_jobs=-1
        )

        self.lda_model.fit(doc_term_matrix)

        return self

    def get_top_words_per_topic(self, n_words: int = 10) -> Dict[int, List[Tuple[str, float]]]:
        """
        Get top words for each topic

        Args:
            n_words: Number of top words to return per topic

        Returns:
            Dictionary mapping topic_id to list of (word, weight) tuples
        """
        if self.lda_model is None:
            raise ValueError("Model not fitted yet. Call fit() first.")

        topics = {}
        for topic_idx, topic in enumerate(self.lda_model.components_):
            top_indices = topic.argsort()[-n_words:][::-1]
            top_words = [(self.feature_names[i], topic[i]) for i in top_indices]
            topics[topic_idx] = top_words

        return topics

    def get_topic_labels(self, n_words: int = 3) -> Dict[int, str]:
        """
        Generate human-readable labels for topics

        Args:
            n_words: Number of words to include in label

        Returns:
            Dictionary mapping topic_id to label string
        """
        topics = self.get_top_words_per_topic(n_words)
        labels = {}

        for topic_id, words in topics.items():
            top_words = [word for word, weight in words[:n_words]]
            label = f"Theme {topic_id + 1}: {', '.join(top_words).title()}"
            labels[topic_id] = label

        return labels

    def transform(self, texts: List[str]) -> np.ndarray:
        """
        Transform texts to topic distributions

        Returns:
            Array of shape (n_documents, n_topics) with topic proportions
        """
        if self.lda_model is None or self.vectorizer is None:
            raise ValueError("Model not fitted yet. Call fit() first.")

        processed_texts = [self.preprocessor.preprocess(text) for text in texts]
        doc_term_matrix = self.vectorizer.transform(processed_texts)
        return self.lda_model.transform(doc_term_matrix)

    def get_dominant_topic(self, texts: List[str]) -> pd.DataFrame:
        """
        Get dominant topic for each document

        Returns:
            DataFrame with document_id, dominant_topic, topic_label, confidence
        """
        topic_distributions = self.transform(texts)
        labels = self.get_topic_labels()

        results = []
        for doc_id, dist in enumerate(topic_distributions):
            dominant_topic = dist.argmax()
            confidence = dist[dominant_topic]

            results.append({
                'document_id': doc_id,
                'dominant_topic': dominant_topic,
                'topic_label': labels[dominant_topic],
                'confidence': confidence,
                'text_preview': texts[doc_id][:100] if doc_id < len(texts) else ""
            })

        return pd.DataFrame(results)

    def plot_topics(self, n_words: int = 10, title: str = "Topic Model (LDA)"):
        """Plot top words for each topic"""
        topics = self.get_top_words_per_topic(n_words)

        fig, axes = plt.subplots(1, self.n_topics, figsize=(4 * self.n_topics, 4))
        if self.n_topics == 1:
            axes = [axes]

        for topic_id, ax in enumerate(axes):
            words, weights = zip(*topics[topic_id])
            ax.barh(range(n_words), weights, color='#0066CC', alpha=0.7)
            ax.set_yticks(range(n_words))
            ax.set_yticklabels(words)
            ax.set_xlabel('Weight')
            ax.set_title(f'Topic {topic_id + 1}', fontweight='bold')
            ax.invert_yaxis()

        fig.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        return fig


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def quick_wordcloud(text: str, title: str = "Word Cloud") -> WordCloud:
    """Quick word cloud generation"""
    generator = WordCloudGenerator()
    return generator.generate(text)

def quick_sentiment(texts: List[str]) -> Dict:
    """Quick sentiment analysis with summary"""
    analyzer = SentimentAnalyzer()
    sentiments = analyzer.analyze_corpus(texts)
    return analyzer.get_summary_stats(sentiments)

def quick_topics(texts: List[str], n_topics: int = 5) -> Dict:
    """Quick topic modeling"""
    modeler = TopicModeler(n_topics=n_topics)
    modeler.fit(texts)
    return modeler.get_topic_labels()


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TEXT ANALYTICS UTILITIES - TEST")
    print("=" * 70)

    # Sample XR text
    sample_texts = [
        "Extended reality headsets enable immersive training simulations for manufacturing workers",
        "Virtual reality concerts provide engaging entertainment experiences with haptic feedback",
        "Augmented reality overlays assist technicians in complex maintenance procedures",
        "Mixed reality collaboration tools enhance remote teamwork and design reviews",
        "XR training reduces onboarding time and improves safety compliance metrics"
    ]

    combined_text = ' '.join(sample_texts)

    # Test Word Cloud
    print("\n📊 Testing Word Cloud Generation...")
    wc_gen = WordCloudGenerator()
    wordcloud = wc_gen.generate(combined_text)
    top_words = wc_gen.get_top_words(combined_text, n=5)
    print(f"✅ Top 5 words: {top_words}")

    # Test Sentiment Analysis
    print("\n😊 Testing Sentiment Analysis...")
    sentiment_analyzer = SentimentAnalyzer()
    sentiments = sentiment_analyzer.analyze_corpus(sample_texts)
    summary = sentiment_analyzer.get_summary_stats(sentiments)
    print(f"✅ Average polarity: {summary['avg_polarity']:.3f}")
    print(f"✅ Positive: {summary['positive_pct']:.1f}%, Neutral: {summary['neutral_pct']:.1f}%, Negative: {summary['negative_pct']:.1f}%")

    # Test Topic Modeling
    print("\n🎯 Testing Topic Modeling...")
    topic_modeler = TopicModeler(n_topics=2)
    topic_modeler.fit(sample_texts * 3)  # Repeat for more data
    labels = topic_modeler.get_topic_labels()
    print(f"✅ Topics identified:")
    for topic_id, label in labels.items():
        print(f"   - {label}")

    print("\n" + "=" * 70)
    print("✅ ALL TEXT ANALYTICS UTILITIES READY")
    print("=" * 70)

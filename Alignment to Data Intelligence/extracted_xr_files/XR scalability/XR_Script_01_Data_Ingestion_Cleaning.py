"""
XR_Script_01_Data_Ingestion_Cleaning.py
XR Scalability Analytics: Data preprocessing pipeline
Purpose: Load, clean, tokenize XR scalability corpus
Author: Mathemagica 2.0 Data Science Team
Date: November 2024
"""

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

class XR_DataIngestor:
    """Handles XR data ingestion and cleaning"""

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        # Standard stopwords + XR-specific terms to remove
        self.stop_words = set(stopwords.words('english'))
        self.xr_stop_words = {'xr', 'ar', 'vr', 'mr', 'extended', 'reality', 
                             'solution', 'solutions', 'system', 'systems'}
        self.stop_words.update(self.xr_stop_words)

    def load_data(self, filepath):
        """Load CSV data"""
        try:
            df = pd.read_csv(filepath)
            print(f"[OK] Loaded {filepath}: {len(df)} records")
            return df
        except Exception as e:
            print(f"[ERR] Error loading {filepath}: {str(e)}")
            return None

    def clean_text(self, text):
        """Clean and normalize text"""
        if pd.isna(text):
            return ""

        text = str(text).lower()

        # Remove SOURCE: headers (from VERBATIM raw text)
        text = re.sub(r'source:.*\n', '', text, flags=re.IGNORECASE)

        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)

        # Remove technical metrics (to focus on concepts)
        text = re.sub(r'\d+[mM][bB](ps)?', 'bandwidth', text)
        text = re.sub(r'\d+ms', 'latency', text)
        text = re.sub(r'\d+%', 'percentage', text)

        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def tokenize_and_lemmatize(self, text):
        """Tokenize and lemmatize text"""
        if not text:
            return []

        # Tokenize
        tokens = word_tokenize(text)

        # Remove stopwords and lemmatize
        processed_tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in self.stop_words and len(token) > 2
        ]

        return processed_tokens

    def process_dataframe(self, df, text_column='content'):
        """Process entire dataframe"""
        print(f"\nProcessing text data from column: {text_column}")

        # Clean text
        df['cleaned_text'] = df[text_column].apply(self.clean_text)

        # Tokenize
        df['tokens'] = df['cleaned_text'].apply(self.tokenize_and_lemmatize)

        # Create token string for word cloud
        df['token_string'] = df['tokens'].apply(lambda x: ' '.join(x))

        # Remove empty rows
        df = df[df['token_string'].str.len() > 0]

        print(f"[OK] Processed {len(df)} records")
        return df

def main():
    """Main execution"""
    ingestor = XR_DataIngestor()

    print("=" * 80)
    print("XR SCALABILITY: DATA INGESTION & CLEANING")
    print("=" * 80)

    # Load all aspect-specific files
    aspects = [
        ('XR_01_5G_6G_Connectivity_Data.csv', '5G/6G Connectivity'),
        ('XR_02_Edge_Computing_Data.csv', 'Edge Computing'),
        ('XR_03_Cloud_Rendering_Data.csv', 'Cloud Rendering'),
        ('XR_04_Mobile_Device_Management_Data.csv', 'MDM'),
        ('XR_05_Infrastructure_Scaling_Data.csv', 'Infrastructure Scaling')
    ]

    processed_dfs = []

    for filename, aspect_name in aspects:
        df = ingestor.load_data(filename)
        if df is not None:
            df = ingestor.process_dataframe(df)
            df['aspect'] = aspect_name
            processed_dfs.append(df)
            df.to_csv(f'processed_{filename}', index=False)

    # Create master corpus
    if processed_dfs:
        master = pd.concat(processed_dfs, ignore_index=True)
        master.to_csv('XR_Processed_Master_Corpus.csv', index=False)
    print(f"\n[OK] Master corpus created: {len(master)} total records")
    print("Ready for analysis scripts.")
    print("=" * 80)
    print("OUTPUT FILES:")
    for filename, _ in aspects:
        print(f"  - processed_{filename}")
    print("  - XR_Processed_Master_Corpus.csv")
    print("=" * 80)

if __name__ == "__main__":
    main()

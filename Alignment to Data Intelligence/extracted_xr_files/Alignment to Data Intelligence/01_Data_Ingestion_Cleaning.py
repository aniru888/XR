# 01_Data_Ingestion_Cleaning.py
# IEMT Social Data Analytics Methodology: Data Preprocessing
# This script handles the ingestion of the massive simulated corpus and performs
# rigorous cleaning including tokenization, POS-tagged lemmatization, and stop-word removal.

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import re

# Ensure NLTK resources are available
resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng', 'punkt_tab']
for resource in resources:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        try:
            nltk.data.find(f'corpora/{resource}')
        except LookupError:
            try:
                nltk.data.find(f'taggers/{resource}')
            except LookupError:
                nltk.download(resource)

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def load_and_clean_data(filepath):
    """
    Loads data from CSV, cleans text, removes stopwords, and lemmatizes with POS tagging.
    Returns a DataFrame with an 'Cleaned_Text' column.
    
    Methodology:
    1. Lowercase conversion for uniformity.
    2. Regex cleaning to remove non-alphabetic characters.
    3. Tokenization using NLTK's punkt tokenizer.
    4. Stop-word removal (Standard English + Domain Specific).
    5. POS-Tagged Lemmatization: "Running" (Verb) -> "Run", "Better" (Adj) -> "Good".
    """
    print(f"Loading data from {filepath}...")
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return pd.DataFrame()
    
    # Normalize column names to 'Text'
    if 'Text' not in df.columns:
        if 'Content' in df.columns:
            df['Text'] = df['Content']
        elif 'Abstract' in df.columns:
            df['Text'] = df['Abstract']
        elif 'Tweet' in df.columns:
            df['Text'] = df['Tweet']
        else:
            print("Warning: No suitable text column found. Creating empty 'Text' column.")
            df['Text'] = ""

    # Define Stop Words
    stop_words = set(stopwords.words('english'))
    # Domain specific stop words to remove generic terms and "stopwords" of the field
    # We remove 'xr', 'ai' etc because they are the *subject* of the study, not the *descriptors*
    stop_words.update([
        'xr', 'ai', 'model', 'models', 'world', 'llms', 'spatial', 'intelligence', 
        'using', 'new', 'based', 'approach', 'study', 'paper', 'research', 'analysis',
        'data', 'system', 'time', 'real', 'application', 'use', 'via', 'towards'
    ])
    
    lemmatizer = WordNetLemmatizer()

    def clean_text(text):
        if not isinstance(text, str):
            return ""
        # 1. Lowercase
        text = text.lower()
        # 2. Remove punctuation and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # 3. Tokenize
        tokens = word_tokenize(text)
        # 4. Remove stopwords and Lemmatize with POS
        cleaned_tokens = []
        for word in tokens:
            if word not in stop_words and len(word) > 2:
                # Apply POS-tagged lemmatization for higher accuracy
                lemma = lemmatizer.lemmatize(word, get_wordnet_pos(word))
                if lemma not in stop_words: # Check again after lemmatization
                    cleaned_tokens.append(lemma)
        
        return " ".join(cleaned_tokens)

    print("Cleaning text (this may take a moment due to POS tagging)...")
    df['Cleaned_Text'] = df['Text'].apply(clean_text)
    print("Data cleaning complete.")
    return df

if __name__ == "__main__":
    # Test run
    df = load_and_clean_data("XR_Integrated_Master_Corpus.csv")
    if not df.empty:
        print(df.head())
        df.to_csv("XR_Cleaned_Data.csv", index=False)
        print("Saved cleaned data to XR_Cleaned_Data.csv")

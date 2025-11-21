"""
1_wordcloud.py
- Reads xr_usecases_corpus.csv
- Creates xr_wordcloud.png and wordcloud_top_terms.csv
"""
import pandas as pd, re
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def clean_text_simple(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+',' ', text)
    text = re.sub(r'[^a-z0-9\s]',' ', text)
    tokens = nltk.word_tokenize(text)
    stop = set(stopwords.words('english'))
    lem = WordNetLemmatizer()
    tokens = [lem.lemmatize(t) for t in tokens if t not in stop and len(t)>2]
    return " ".join(tokens)

df = pd.read_csv("xr_usecases_corpus.csv", dtype=str)
if 'clean_text' not in df.columns or df['clean_text'].isnull().all():
    df['clean_text'] = df['raw_text'].fillna('').apply(clean_text_simple)

all_text = " ".join(df['clean_text'].tolist())
tokens = all_text.split()
counts = Counter(tokens)
top_terms = counts.most_common(200)
pd.DataFrame(top_terms, columns=['term','count']).to_csv("wordcloud_top_terms.csv", index=False)

wc = WordCloud(width=1200, height=600, background_color='white', collocations=False)
wc.generate_from_frequencies(dict(top_terms))
wc.to_file("xr_wordcloud.png")

print("Saved: xr_wordcloud.png and wordcloud_top_terms.csv")

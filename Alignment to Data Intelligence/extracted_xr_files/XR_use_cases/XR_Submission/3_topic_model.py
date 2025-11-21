"""
3_topic_model.py
- Reads xr_usecases_corpus.csv
- Produces xr_topics.json and xr_doc_dominant_topic.csv
"""
import pandas as pd, re, json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def preprocess(text):
    if not isinstance(text,str):
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
df['text_for_topics'] = df['clean_text'].fillna('')
df.loc[df['text_for_topics'].str.strip()=='', 'text_for_topics'] = df['raw_text'].fillna('')
df['text_for_topics'] = df['text_for_topics'].apply(preprocess)

vectorizer = CountVectorizer(max_df=0.95, min_df=1, ngram_range=(1,2))
dtm = vectorizer.fit_transform(df['text_for_topics'])
terms = vectorizer.get_feature_names_out()
n_topics = 5
lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
lda.fit(dtm)

topics=[]
for i, comp in enumerate(lda.components_):
    top_idx = comp.argsort()[-10:][::-1]
    top_terms = [terms[j] for j in top_idx]
    topics.append({'topic_id':int(i),'terms':top_terms,'weights':comp[top_idx].tolist()})

with open("xr_topics.json","w",encoding="utf-8") as f:
    json.dump(topics,f,indent=2)
doc_topic = lda.transform(dtm)
df_out = df[['id','source','date']].copy()
df_out['dominant_topic'] = doc_topic.argmax(axis=1)
df_out.to_csv("xr_doc_dominant_topic.csv", index=False)
print("Saved: xr_topics.json and xr_doc_dominant_topic.csv")

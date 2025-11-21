"""
2_sentiment.py
- Reads xr_usecases_corpus.csv
- Produces xr_sentiment_output.csv (per doc) and xr_sentiment_summary.csv
"""
import pandas as pd
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
nltk.download('punkt', quiet=True)

df = pd.read_csv("xr_usecases_corpus.csv", dtype=str)
df['text_for_sent'] = df['clean_text'].fillna('')
df.loc[df['text_for_sent'].str.strip()=='', 'text_for_sent'] = df['raw_text'].fillna('')

analyzer = SentimentIntensityAnalyzer()
rows=[]
for _,r in df.iterrows():
    txt = str(r['text_for_sent'])
    vs = analyzer.polarity_scores(txt)
    compound = vs['compound']
    if compound>=0.05:
        label='positive'
    elif compound<=-0.05:
        label='negative'
    else:
        label='neutral'
    rows.append({
        'id': r.get('id',''),
        'source': r.get('source',''),
        'date': r.get('date',''),
        'compound': compound,
        'neg': vs['neg'],
        'neu': vs['neu'],
        'pos': vs['pos'],
        'label': label
    })
out = pd.DataFrame(rows)
out.to_csv("xr_sentiment_output.csv", index=False)
summary = out['label'].value_counts().rename_axis('label').reset_index(name='count')
summary.to_csv("xr_sentiment_summary.csv", index=False)
print("Saved: xr_sentiment_output.csv and xr_sentiment_summary.csv")

"""
4_integration_report.py
- Reads: wordcloud_top_terms.csv, xr_sentiment_summary.csv, xr_topics.json
- Produces xr_integration_summary.csv and xr_managerial_implications.txt
"""
import pandas as pd, json

# load files (must exist)
wc = pd.read_csv("wordcloud_top_terms.csv") if pd.io.common.file_exists("wordcloud_top_terms.csv") else None
sent = pd.read_csv("xr_sentiment_summary.csv") if pd.io.common.file_exists("xr_sentiment_summary.csv") else None

with open("xr_topics.json","r", encoding="utf-8") as f:
    topics = json.load(f)

# create a compact integration summary
rows = []
top_terms = ", ".join(wc['term'].head(10).tolist()) if wc is not None else ""
for t in topics:
    rows.append({
        'topic_id': t['topic_id'],
        'top_terms': "; ".join(t['terms'])
    })
df_topics = pd.DataFrame(rows)
df_topics.to_csv("xr_integration_summary.csv", index=False)

# Managerial implications - automatic draft
positive = 0
neutral = 0
negative = 0
if sent is not None:
    for _,r in sent.iterrows():
        if r['label']=='positive' or r.get('label')=='positive':
            positive += int(r.get('count',0))
        elif r['label']=='neutral' or r.get('label')=='neutral':
            neutral += int(r.get('count',0))
        elif r['label']=='negative' or r.get('label')=='negative':
            negative += int(r.get('count',0))

implications = []
implications.append("Top use-case terms (word cloud): " + top_terms)
implications.append("Topics identified (brief):")
for t in topics:
    implications.append(f" - Topic {t['topic_id']}: {', '.join(t['terms'][:5])} ...")
implications.append("Sentiment snapshot: positive={}, neutral={}, negative={}".format(positive,neutral,negative))
implications.append("\nManagerial implications (draft):")
implications.append("1) Focus early investments on domains with clear ROI (e.g., industrial maintenance, medical training).")
implications.append("2) Prioritize integration and interoperability pilots to reduce integration risk flagged in corpus.")
implications.append("3) Consider hardware cost and user comfort mitigation strategies (pilot subsidies, UX testing).")

with open("xr_managerial_implications.txt","w", encoding="utf-8") as f:
    f.write("\n".join(implications))

print("Saved: xr_integration_summary.csv and xr_managerial_implications.txt")

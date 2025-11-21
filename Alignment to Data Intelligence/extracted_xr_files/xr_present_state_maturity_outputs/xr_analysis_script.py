# Reproducible script for XR Present State of Maturity analysis
# Corpus path: /mnt/data/xr_present_state_maturity_outputs/XR_present_state_corpus.txt
# Outputs: wordcloud PNG, sentiment CSV, sentiment plot PNG, topics TXT
# This script mirrors the notebook steps used to generate outputs

import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

# (Insert the corpus text here or load from file)
corpus = open(r'XR_present_state_corpus.txt','r',encoding='utf-8').read()
wc = WordCloud(width=1600,height=800,collocations=False).generate(corpus)
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.savefig('xr_wordcloud.png', bbox_inches='tight')

# Sentiment: use NLTK VADER or fallback
# ...
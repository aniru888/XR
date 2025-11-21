"""
0_data_prep.py
- Validates xr_usecases_corpus.csv is present and has required columns.
- Writes a cleaned copy xr_usecases_corpus.csv if needed.
"""
import pandas as pd
import os
import sys

in_path = "xr_usecases_corpus.csv"
if not os.path.exists(in_path):
    print(f"ERROR: {in_path} not found. Please upload it to Colab files pane.")
    sys.exit(1)

df = pd.read_csv(in_path, dtype=str)
required = {'id','source','date','url','industry','raw_text','clean_text'}
missing = required - set(df.columns)
if missing:
    print("WARN: Missing columns:", missing)
    # Try to create missing columns
    for c in missing:
        df[c] = ""
# Ensure id exists
if df['id'].isnull().any() or df['id'].eq('').any():
    df['id'] = ["XR_{:04d}".format(i+1) for i in range(len(df))]

df.to_csv("xr_usecases_corpus.csv", index=False)
print("Validated and saved: xr_usecases_corpus.csv")

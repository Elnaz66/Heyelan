import pandas as pd
import json
import os
import re
import numpy as np
from scrappers.utils import turkey_cities

# Cleaning data
df = pd.read_csv('main_3.csv')

df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')

df['olu_sayisi'] = df['olu_sayisi'].str.lower().map(
    {'çok sayıda': None, 'belirtilmemiş': None}
)
df['olu_sayisi'] = df['olu_sayisi'].astype('Int64')
df['olu_sayisi'] = pd.to_numeric(
    df['olu_sayisi'], errors='coerce', downcast='integer'
)
df['olu_sayisi'] = df['olu_sayisi'].fillna(0)


df['yarali_sayisi'] = pd.to_numeric(
    df['yarali_sayisi'], errors='coerce', downcast='integer'
)
df['yarali_sayisi'] = df['yarali_sayisi'].fillna(0)

df['il'] = df['il'].str.lower()
df = df[df['il'].isin(turkey_cities)]


def compare_rows(a, b):  # Remove duplicates with a 3 day range
    if a['il'] == b['il'] and a['olu_sayisi'] == b['olu_sayisi'] and a['yarali_sayisi'] == b['yarali_sayisi'] and a['ilce'] and b['ilce']:
        diff = (a['date'] - b['date']) / np.timedelta64(1, 'D')
        for a_ilce in a['ilce']:
            if a_ilce in b['ilce']:
                if a['mahalle'] and b['mahalle']:
                    for a_mahalle in a['mahalle']:
                        if a_mahalle in b['mahalle']:
                            if diff <= 3:
                                return True
                if a['koy'] and b['koy']:
                    for a_koy in a['koy']:
                        if a_koy in b['koy']:
                            if diff <= 3:
                                return True
    return False


duplicates = [True] * len(df.index)
for i in range(1, len(df)):
    for j in range(i):
        if compare_rows(df.iloc[i], df.iloc[j]):
            duplicates[j] = False
df = df[duplicates]


df.to_csv("final_data.csv", index=False)

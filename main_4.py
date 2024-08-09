import pandas as pd
import json
import os
import re
import numpy as np
from scrappers.utils import turkey_cities
from unicode_tr import unicode_tr

# Cleaning data
df = pd.read_csv('main_3.csv')

df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')

df['yaralı_sayısı'] = df['yaralı_sayısı'].astype('Int64')
df['yaralı_sayısı'] = df['yaralı_sayısı'].fillna(0)

df['ölu_sayısı'] = df['ölu_sayısı'].astype('Int64')
df['ölu_sayısı'] = df['ölu_sayısı'].fillna(0)

df['il'] = df['il'].fillna('')
df['il'] = df['il'].apply(lambda text: unicode_tr(text).lower())
df = df[df['il'].isin(turkey_cities)]

df['ilçe'] = df['ilçe'].fillna('')
df['ilçe'] = df['ilçe'].apply(lambda text: unicode_tr(text).lower())

df['mahalle'] = df['mahalle'].fillna('')
df['mahalle'] = df['mahalle'].apply(lambda text: unicode_tr(text).lower())

df['köy'] = df['köy'].fillna('')
df['köy'] = df['köy'].apply(lambda text: unicode_tr(text).lower())


def compare_rows(a, b):  # Remove duplicates with a 3 day range
    if a['il'] == b['il'] and a['ölu_sayısı'] == b['ölu_sayısı'] and a['yaralı_sayısı'] == b['yaralı_sayısı'] and a['ilçe'] and b['ilçe']:
        diff = (a['date'] - b['date']) / np.timedelta64(1, 'D')
        b_ilçeler = b['ilçe'].split(',')
        for a_ilçe in a['ilçe'].split(','):
            if a_ilçe in b_ilçeler:
                if a['mahalle'] and b['mahalle']:
                    b_mahalleler = b['mahalle'].split(',')
                    for a_mahalle in a['mahalle'].split(','):
                        if a_mahalle in b_mahalleler:
                            if diff <= 3:
                                return True
                if a['köy'] and b['köy']:
                    b_köy = b['köy'].split(',')
                    for a_köy in a['köy'].split(','):
                        if a_köy in b_köy:
                            if diff <= 3:
                                return True
    return False


duplicates = [True] * len(df.index)
for i in range(1, len(df)):
    for j in range(i):
        if compare_rows(df.iloc[i], df.iloc[j]):
            duplicates[j] = False
df = df[duplicates]


df.to_csv("main_4.csv", index=False)

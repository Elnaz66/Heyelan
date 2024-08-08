import pandas as pd
import json
import os
import re
import numpy as np

# all_data = []
# for folder in ["gpt-version0", "gpt-version1", "gpt-version2", "gpt-version3"]:
#     for filename in os.listdir(folder):
#         if filename.endswith(".json"):
#             filepath = os.path.join(folder, filename)
#             with open(filepath, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#                 all_data.append(data)

# Converting dictionary keys to latin alphabet
all_data = []
with open('combined.json', "r", encoding="utf-8") as f:
    data = json.load(f)
    for row in data:
        data_clean = {
            "source_link": row['source_link'],
            "keyword": row['keyword'],
            "headline": row['headline'],
            "website_keywords": row['website_keywords'],
            "description": row['description'],
            "body": row['body'],
            "date": row['date'],
        }
        for key, value in row.items():
            key_clean = key.replace('ö', 'o').lower().replace('ü', 'u').replace(
                'ı', 'i').replace('ç', 'c').replace('ğ', 'c')
            if key_clean in ['ilce', 'il', 'koy', 'olu_sayisi', 'yarali_sayisi', 'mahalle']:
                data_clean[key_clean] = value
        all_data.append(data_clean)

df = pd.DataFrame(all_data)

df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
df['olu_sayisi'] = df['olu_sayisi'].str.lower().map(
    {'çok sayıda': None, 'belirtilmemiş': None})
df['olu_sayisi'] = df['olu_sayisi'].astype('Int64')
df['olu_sayisi'] = pd.to_numeric(df['olu_sayisi'], errors='coerce', downcast='integer')
df['olu_sayisi'] = df['olu_sayisi'].fillna(0)

df['yarali_sayisi'] = pd.to_numeric(df['yarali_sayisi'], errors='coerce', downcast='integer')
df['yarali_sayisi'] = df['yarali_sayisi'].fillna(0)

# linklerin sonundaki sayı kısmını sil
df['source_link'] = df['source_link'].apply(lambda x: re.sub(r'-\d+$', '', x))
df['source_link'] = df['source_link'].str.lower()
df = df.drop_duplicates(subset=['source_link'])

turkey_cities = [
    'adana', 'adıyaman', 'afyonkarahisar', 'ağrı', 'aksaray', 'amasya', 'ankara',
    'antalya', 'ardahan', 'artvin', 'aydın', 'balıkesir', 'bartın', 'batman',
    'bayburt', 'bilecik', 'bingöl', 'bitlis', 'bolu', 'burdur', 'bursa', 'çanakkale',
    'çankırı', 'çorum', 'denizli', 'diyarbakır', 'düzce', 'edirne', 'elazığ', 'erzincan',
    'erzurum', 'eskişehir', 'gaziantep', 'giresun', 'gümüşhane', 'hakkari', 'hatay',
    'ığdır', 'ısparta', 'istanbul', 'izmir', 'kahramanmaraş', 'karabük', 'karaman',
    'kars', 'kastamonu', 'kayseri', 'kırıkkale', 'kırklareli', 'kırşehir', 'kilis',
    'kocaeli', 'konya', 'kütahya', 'malatya', 'manisa', 'mardin', 'mersin', 'muğla',
    'muş', 'nevşehir', 'niğde', 'ordu', 'osmaniye', 'rize', 'sakarya', 'samsun',
    'şanlıurfa', 'siirt', 'sinop', 'sivas', 'şırnak', 'tekirdağ', 'tokat', 'trabzon',
    'tunceli', 'uşak', 'van', 'yalova', 'yozgat', 'zonguldak'
]

df['il'] = df['il'].str.lower()
df_turkey = df[df['il'].isin(turkey_cities)]


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


df.to_csv("combined.csv", encoding="utf-8", index=False)

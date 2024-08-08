import pandas as pd
import json
import os
import re

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
            "date": row['date']
        }
        for key, value in row.items():
            key_clean = key.replace('ö', 'o').lower().replace('ü', 'u').replace(
                'ı', 'i').replace('ç', 'c').replace('ğ', 'c')
            if key_clean in ['ilce', 'il', 'koy', 'olu_sayisi', 'yarali_sayisi']:
                data_clean[key_clean] = value
        all_data.append(data_clean)

df = pd.DataFrame(all_data)

df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
df['olu_sayisi'] = df['olu_sayisi'].str.lower().map({'çok sayıda': None, 'Belirtilmemiş': None})
df['olu_sayisi'] = df['olu_sayisi'].astype('Int64')

df['yarali_sayisi'] = df['yarali_sayisi'].str.lower().map({'çok sayıda': None, 'Belirtilmemiş': None})
df['yarali_sayisi'] = df['yarali_sayisi'].astype('Int64')

# linklerin sonundaki sayı kısmını sil
df['source_link'] = df['source_link'].apply(lambda x: re.sub(r'-\d+$', '', x))
df['source_link'] = df['source_link'].str.lower()
df = df.drop_duplicates(subset=['source_link'])

# print(df.dtypes)
# print(len(df.index))
# df = df.drop_duplicates(subset=['il', 'olu_sayisi', 'yarali_sayisi'])
# print(len(df.index))


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

df.to_csv("combined.csv", encoding="utf-8", index=False)

import scrappers.gpt as gpt
from scrappers.utils import read_json_files, save_json
import os
import pandas as pd
from unicode_tr import unicode_tr

# Extract data from pages text using GPT
os.makedirs("gpt/", exist_ok=True)
scrapped_df = pd.read_csv('main_2.csv')
for page in scrapped_df.to_dict(orient="records"):
    if gpt.is_real_incident(page):
        news = gpt.read_news(page)
        if news:
            save_json("gpt/", news)

# Clean and save data in one CSV
all_data = []
for row in read_json_files("gpt/"):
    data_clean = {
        "source_link": row['source_link'],
        "keyword": row['keyword'],
        "headline": row['headline'],
        "description": row['description'],
        "body": row['body'],
        "date": row['date'],
    }
    # Cleaning key names by converting everything to English, then back to Turkish
    for key, value in row.items():
        key_clean = unicode_tr(key).lower()
        key_clean = key_clean.replace('ö', 'o').replace(
            'ü', 'u').replace('ı', 'i').replace('ç', 'c').replace('ğ', 'c')
        if key_clean in ['ilce', 'il', 'koy', 'olu_sayisi', 'yarali_sayisi', 'mahalle']:
            data_clean[key_clean] = value
    all_data.append(data_clean)

df = pd.DataFrame(all_data)
df = df.rename(columns={
    'ilce': 'ilçe',
    'koy': 'köy',
    'olu_sayisi': 'ölu_sayısı',
    'yarali_sayisi': 'yaralı_sayısı'
})
df.to_csv('main_3.csv', index=False)

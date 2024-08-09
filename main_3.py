import scrappers.gpt as gpt
from scrappers.utils import read_json_files, save_json

# Extract data from pages text using GPT
os.makedirs("gpt/", exist_ok = True)
scrapped_df = pd.read_csv('main_2.csv')
for i, page in scrapped_df.iterrows():
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
        "website_keywords": row['website_keywords'],
        "description": row['description'],
        "body": row['body'],
        "date": row['date'],
    }
    # Converting key names to english alphabet
    for key, value in row.items():
        key_clean = key.lower().replace('ö', 'o').replace(
            'ü', 'u').replace('ı', 'i').replace('ç', 'c').replace('ğ', 'c')
        if key_clean in ['ilce', 'il', 'koy', 'olu_sayisi', 'yarali_sayisi', 'mahalle']:
            data_clean[key_clean] = value
    all_data.append(data_clean)

df = pd.DataFrame(all_data)
df.to_csv('main_3.csv', index=False)

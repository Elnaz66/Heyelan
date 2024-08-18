import scrappers.gpt as gpt
from scrappers.utils import read_json_files, save_json
import os
import pandas as pd

# Extract data from pages text using GPT
os.makedirs("gpt/", exist_ok=True)
scrapped_df = pd.read_csv('main_2.csv')
scrapped_df = scrapped_df.fillna('')
for page in scrapped_df.to_dict(orient="records"):
    if gpt.is_real_incident(page):
        news = gpt.read_news(page)
        if news:
            save_json("gpt/", news)

# Save data in one CSV
all_data = []
for row in read_json_files("gpt/"):
    all_data.append(row)
df = pd.DataFrame(all_data)
df.to_csv('main_3.csv', index=False)

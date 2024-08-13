from apify_client import ApifyClient
import pandas as pd
from scrappers.utils import read_json_files, save_json, keywords
import os
import scrappers.google as google

# Extract links from Google
os.makedirs("google_links/", exist_ok=True)
for keyword in keywords:
    for website in ["aa.com.tr", "iha.com.tr", "cumhuriyet.com.tr", "milliyet.com.tr"]:
        for google_link in google.links(website, keyword):
            save_json("google_links/", google_link)

# Clean and save data in one CSV
df = pd.DataFrame(read_json_files("google_links/"))
df = df.drop_duplicates()
df = df.groupby('source_link')['keyword'].apply(','.join).reset_index()
df.to_csv('main_1.csv', index=False)

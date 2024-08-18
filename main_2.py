import scrappers.aa_com_tr as aa_com_tr
import scrappers.common as common
from scrappers.utils import read_json_files, save_json
from urllib.parse import urlparse
import pandas as pd
import os

# Extract text from pages' HTML
os.makedirs("scrapped/", exist_ok = True)
os.makedirs("server_error/", exist_ok = True)
os.makedirs("failed/", exist_ok = True)
google_links_df = pd.read_csv('main_1.csv')
for google_link in google_links_df.to_dict(orient="records"):
    page = None
    if "aa.com.tr" in urlparse(google_link['source_link']).netloc:
        page = aa_com_tr.scrap(google_link)
    else:
        page = common.scrap(google_link)

    if page and page != 500:
        save_json("scrapped/", page)
    elif page == 500:
        save_json("server_error/", google_link)
    else:
        save_json("failed/", google_link)

# Save data in one CSV
df = pd.DataFrame(read_json_files("scrapped/"))
df.to_csv('main_2.csv', index=False)

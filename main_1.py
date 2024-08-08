from apify_client import ApifyClient
import aa_com_tr
import common
import google
import pandas as pd
import gpt
import os
import json
from urllib.parse import urlparse


def json_files(directory):  # List JSON files in directory
    return [f for f in os.listdir(directory) if f.endswith('.json')]


def save_json(directory, data):
    # Get the highest numbered JSON file (to start where we stopped)
    highest_number = max(
        [int(f.split('.')[0]) for f in json_files(directory)],
        default=0
    )

    new_filename = f"{highest_number + 1}.json"
    with open(os.path.join(directory, new_filename), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_json_files(directory):
    file_list = []
    for filename in json_files(directory):
        with open(os.path.join(directory, filename), "r", encoding='utf-8') as file:
            file_list.append(json.load(file))
    return file_list


keywords = [
    "çamur akıntısı", "çamur akması", "çamur hareketi", "heyelan", "kaya çökmesi", "kaya devrilmesi",
    "kaya düşmesi", "kaya hareketi", "kaya kayması", "kaya yuvarlanması", "moloz akıntısı", "moloz akması",
    "moloz hareketi", "toprak çökmesi", "toprak hareketi", "toprak kayması", "toprak sürüklenmesi", "yamaç kayması",
    "yer çökmesi", "yer hareketleri", "yer kayması", "zemin çökmesi", "zemin hareketi", "zemin kayması"
]

# Google
for keyword in keywords:
    for website in ["aa.com.tr", "iha.com.tr", "cumhuriyet.com.tr", "milliyet.com.tr"]:
        for google_link in google.links(website, keyword):
            save_json("google_links/", google_link)


# Extract Body from pages' HTML
for google_link in read_json_files("google_links/"):
    page = None
    parsed_url = urlparse(google_link['source_link'])
    if "aa.com.tr" in parsed_url.netloc:
        page = aa_com_tr.scrap(google_link)
    else:
        page = common.scrap(google_link)

    if page and page != 500:
        save_json("scrapped/", page)
    elif page == 500:
        save_json("server_error/", google_link)
    else:
        save_json("failed/", google_link)


# Extract data from Bodies using GPT
for page in read_json_files("scrapped/"):
    if gpt.is_real_incident(page):
        news = gpt.read_news(page)
        if news:
            save_json("gpt/", news)

import requests
from bs4 import BeautifulSoup
import re
import json
import html2text
from datetime import datetime


def scrap(google_link):  # headline, keywords, description, body, date
    url = google_link['source_link']
    keyword = google_link['keyword']
    
    page = {"source_link": url, "keyword": keyword}
    print("Fetching", url, end=' ')
    response = None
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
            },
            timeout=30
        )
    except:
        print("500")
        return 500
    try:
        soup = BeautifulSoup(response.content, 'html.parser')

        page['headline'] = soup.find("title").get_text()

        keywords = soup.find("meta", {"name": "keywords"})['content']
        page['website_keywords'] = re.split(r", ?", keywords)

        page['description'] = soup.find(
            "meta", {"name": "description"}
        )['content']

        details = soup.find("div", class_="detay-icerik")
        details.find("div", class_="detay-paylas").decompose()
        for img in details.find_all("img"):
            img.decompose()
        h = html2text.HTML2Text()
        h.ignore_links = True
        page['body'] = h.handle(details.prettify())

        match = re.search(
            r"\d+\.\d+\.\d+",
            soup.find("span", class_="tarih").get_text()
        )
        if match:
            page['date'] = match.group()

        print("success")
        return page
    except:
        print("failed")
        return {}


if __name__ == "__main__":
    page = scrap(
        "https://www.aa.com.tr/tr/teyithatti/bilim-teknoloji/afrikada-yeni-bir-kita-ve-okyanus-olusuyor-iddiasi-/1815598", "kazı")
    print(page['body'])

import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import html2text


def scrap(google_link):  # headline, website_keywords, description, body, date, source_link, keyword
    url = google_link['source_link']
    keyword = google_link['keyword']

    page = {"source_link": url, "keyword": keyword}
    print("Fetching", url, end=' ')
    response = None
    try:
        response = requests.get(url, timeout=30)
    except:
        print("500")
        return 500
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        schema = parse_schema(soup)
        page["headline"] = schema["headline"]
        page["website_keywords"] = schema["keywords"]
        page["description"] = schema["description"]

        body = schema["articleBody"]
        h = html2text.HTML2Text()
        h.ignore_links = True
        page['body'] = h.handle(body)

        page["date"] = convert_date(schema["datePublished"])
        print("success")
        return page
    except:
        print("failed")
        return {}


def convert_date(date_str):
    # 2024-05-08T15:07:44+03:00 -> 08.05.2024
    date_str = re.match(r'\d{4}-\d{2}-\d{2}', date_str).group()
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")


def parse_schema(soup):
    schema = soup.find(
        "script",
        type="application/ld+json",
        attrs={"class": None},
        string=re.compile(r'"@type": ?"NewsArticle"'),
    )
    schema_string = schema.get_text().replace("\r\n", "").replace(
        "\n", "").replace("\t", "").replace("&amp;", "&")
    return json.loads(schema_string)


if __name__ == "__main__":
    # page = scrap(
    #     "https://www.iha.com.tr/elazig-haberleri/luks-arac-yoldan-cikti-1i-agir-2-yarali-80628747", "keyword")
    page = scrap(
        "https://www.milliyet.com.tr/yazarlar/zeynep-kakinc/kars-kazi-mi-degil-mi-7076818", "keyword")
    print(page['body'])

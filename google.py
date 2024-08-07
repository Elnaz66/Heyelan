from apify_client import ApifyClient

client = ApifyClient("apify_api_vBSKW5o9NlOvEAcQeS8czI9pbNjPK81NIVqZ")


def links(website, keyword):
    run_input = {
        "includeUnfilteredResults": True,
        "maxPagesPerQuery": 5,  # change to 5
        "mobileResults": False,
        "queries": f"site:{website} {keyword}",
        "resultsPerPage": 100,  # change to 100
        "saveHtml": False,
        "saveHtmlToKeyValueStore": False,
        "languageCode": "",
        "countryCode": "tr",
    }
    run = client.actor("apify/google-search-scraper").call(run_input=run_input)
    result_list = client.dataset(
        run["defaultDatasetId"]
    ).list_items(view="organic_results")

    results = []
    for item in result_list.items:
       results.append({"source_link": item['url'], "keyword": keyword})
       print(item['url']) 
    return results


if __name__ == "__main__":
    for link in links("iha.com.tr", "yer kayması"):
        print(link)

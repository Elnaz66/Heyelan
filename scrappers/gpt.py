from openai import OpenAI
import json
client = OpenAI(
    api_key="sk-proj-RcPWI0GSnveTG2aZI6R0T3BlbkFJQr2QadQAuqQnuhOlp64v")

def is_real_incident(page) -> bool:
    print("Is", page['source_link'], "a real incident:", end=' ')
    prompt = """Is the following Turkish paragraph talking about a landslide (heyelan) incident that happenned, or just a warning or an explanation about the topic? If it was a real incident, did it happen in Turkey? Give me the result in the following JSON format: {{"landslide_incident_and_in_turkey": bool}}
Headline: {headline}
Description: {description}
Body:
md
{body}
""".format(headline=str(page['headline'])[:1500], description=str(page['description'])[:1500], body=str(page['body'])[:1500])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a data analyst designed to output JSON."},
            {"role": "user", "content": prompt},
        ]
    )
    try:
        result = json.loads(response.choices[0].message.content)
        print(result['landslide_incident_and_in_turkey'])
        return result['landslide_incident_and_in_turkey']
    except:
        print("Gpt iyi bir sonuç vermedi")
        return False


def read_news(page):  # headline, website_keywords, description, body, date, source_link, keyword, il, ilçe, mahalle, köy, ölü_sayısı, yaralı_sayısı
    print("Reading", page['source_link'], ":", end=' ')
    prompt = """From the following turkish paragraph about a landslide, give me the following information in JSON format:
```json
{{
"il": str,
"ilçe": str,
"mahalle str,
"köy": str,
"ölü_sayısı": int,
"yaralı_sayısı": int,
}}
```
If the incident happened in a `mahalle`, then make `köy` null. On the other hand, if the incident happened in a `köy`, make`mahalle` null.
If you didn't find `ölü_sayısı`, make it null.
If you didn't find `yaralı_sayısı`, make it null.
Do not include animal deaths or injuries in `ölü_sayısı` or `yaralı_sayısı`.
Headline: {headline}
Description: {description}
Body:
```md
{body}
```
""".format(headline=str(page['headline'])[:1500], description=str(page['description'])[:1500], body=str(page['body'])[:1500])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a data analyst designed to output JSON."},
            {"role": "user", "content": prompt},
        ]
    )
    try:
        result = json.loads(response.choices[0].message.content)
        page.update(result)
        print("finished")
        return page
    except:
        print("Gpt iyi bir sonuç vermedi")
        return {}


if __name__ == "__main__":
    # import common
    # page = common.scrap(
    #     "https://www.iha.com.tr/bursa-haberleri/heyelan-sonrasi-ucurumun-kenarindaki-otomobiller-boyle-kurtarildi-75614580", "heyelan")

    import common
    page = common.scrap(
        {
            "source_link": "https://www.milliyet.com.tr/egitim/deyimler-ve-anlamlari-turkcede-en-cok-kullanilan-kisa-uzun-ve-kaliplasmis-deyim-ornekleri-ve-anlamlari-6562456",
            "keyword": "çamur akıntısı"
        }
    )

    # import aa_com_tr
    # page = aa_com_tr.scrap(
    #     "https://www.aa.com.tr/tr/gundem/istanbulun-karadenize-acilan-sahillerindeki-tehlike-rip-akintisi/2658797", "heyelan")

    if page:
        if (is_real_incident(page)):
            gpt_page = read_news(page)
            print(gpt_page)


# Pricing equation: \left(\frac{0.5}{10^{6}}\cdot2000+\frac{1.50}{10^{6}}\cdot30\right)\cdot1000

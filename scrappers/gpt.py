from openai import OpenAI
import json
from unicode_tr import unicode_tr

client = OpenAI(
    api_key="sk-proj-RcPWI0GSnveTG2aZI6R0T3BlbkFJQr2QadQAuqQnuhOlp64v")


def is_real_incident(page) -> bool:
    print("Is", page['source_link'], "a real incident:", end=' ')
    prompt = """Aşağıdaki paragraflarda anlatılan olayın mutlaka ve sadece yaşanmış bir heyelan olayı olması gerekmektedir. Bu olay, herhangi bir uyarı, araştırma, inceleme, bilimsel çalışma, geçmişte meydana gelen bir heyelan veya konuya ilişkin bir açıklama olmamalıdır. Eğer olay gerçek bir heyelan olayı ise, bu olayın Türkiye'de yaşanıp yaşanmadığını belirleyin. Sonucu bana şu JSON formatında verin: {{"turkiyenin_heyelan_haberleri": bool}}
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
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        result = json.loads(response.choices[0].message.content)
        print(result['turkiyenin_heyelan_haberleri'])
        return result['turkiyenin_heyelan_haberleri']
    except:
        print("Gpt iyi bir sonuç vermedi")
        return False


def read_news(page):  # headline, website_keywords, description, body, date, source_link, keyword, il, ilçe, mahalle, köy, ölü_sayısı, yaralı_sayısı
    print("Reading", page['source_link'], ":", end=' ')
    prompt = """Olay bir `mahalle`de meydana geldiyse, `köy`'ü boş bırak. Öte yandan, olay bir `köy`de meydana geldiyse, `mahalle`'i boş bırak.
`ölü_sayısı`'yı bulamadıysanız, boş bırak.
`yaralı_sayısı`'yı bulamadıysanız, boş bırak.
`kayıp_sayısı`'yı bulamadıysanız, boş bırak.
`ölü_sayısı`, kayıp_sayısı veya `yaralı_sayısı`'ya hayvan ölümlerini, kayıpları veya yaralanmalarını dahil etmeyin. mahsur kalanlar, yaralı veya kayıp değillerdir. Aşağıdaki paragraflarda anlatılan olayın mutlaka ve sadece yaşanmış bir heyelan olayı olması gerekmektedir. Bu olay, herhangi bir uyarı, araştırma, inceleme, bilimsel çalışma, geçmişte meydana gelen bir heyelan veya konuya ilişkin bir açıklama olmamalıdır. Eğer olay gerçek bir heyelan olayı ise, bu olayın Türkiye'de yaşanıp yaşanmadığını belirleyin.
bana JSON formatında ver,
```json
{{
"il": str,
"ilçe": str,
"mahalle: str,
"köy": str,
"ölü_sayısı": int,
"yaralı_sayısı": int,
"kayıp_sayısı": int
}}
```
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
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        result = json.loads(response.choices[0].message.content)
        # Cleaning key names by converting everything to English, then back to Turkish
        english = {}
        for key, value in result.items():
            key = unicode_tr(key).lower()
            key = key.replace('ö', 'o')
            key = key.replace('ü', 'u')
            key = key.replace('ı', 'i')
            key = key.replace('ç', 'c')
            key = key.replace('ğ', 'c')
            if key in ['il', 'ilce',  'koy', 'mahalle', 'olu_sayisi', 'yarali_sayisi', 'kayip_sayisi']:
                english[key] = value

        turkish = {
            "il": english['il'],
            "ilçe": english['ilce'],
            "köy": english['koy'],
            "mahalle": english['mahalle'],
            "ölü_sayısı": english['olu_sayisi'],
            "yaralı_sayısı": english['yarali_sayisi'],
            "kayıp_sayısı": english['kayip_sayisi'],
        }
        page.update(turkish)
        return page
    except:
        print("Gpt iyi bir sonuç vermedi")
        return {}


if __name__ == "__main__":
    page = is_real_incident(
        {
            "source_link": "https://www.aa.com.tr/tr/turkiye/turkiyede-son-90-yilda-1343-kisi-heyelan-nedeniyle-hayatini-kaybetti/2120967",
            "keyword": "çamur akıntısı",
            "headline": "Türkiye'de son 90 yılda 1343 kişi heyelan nedeniyle hayatını kaybetti",
            "description": "Türkiye'de doğal afet kaynaklı kayıplar arasında depremden sonra en fazla ölüme neden olan heyelan, İTÜ Avrasya Yer Bilimleri Enstitüsü bünyesindeki araştırmaya konu oldu. - Anadolu Ajansı",
            "body": """######  İstanbul

İstanbul Teknik Üniversitesi (İTÜ) Avrasya Yer Bilimleri Enstitüsü
bünyesindeki bir araştırmada, **Türkiye'de son 90 yılda 389 ölümlü heyelanda
1343 kişinin hayatını kaybetti** ği belirlendi.

Öğretim Üyesi Doç. Dr. Tolga Görüm ve doktora öğrencisi Seçkin Fidan
tarafından Türkiye'deki ölümcül heyelan olaylarının tespit edilmesi için
2017'de çalışma başlatıldı.

Görüm ve Fidan, 1929'dan 2019'a kadar ülkedeki ölümlü heyelanları di­jital ve
yazılı medya kaynaklarından inceledi.

Yaklaşık 3 yıl süren çalışma sonucunda İTÜ bünyesinde Türkiye'de meydana gelen
ölümlü heyelan olaylarını içeren bir veri tabanı oluşturuldu.

Türkiye Ölümcül Heyelan Veri Tabanı'na (FATALDOT) göre, Türkiye'de her yıl
ortalama 4 ölümlü heyelan gerçekleşirken ortalama 15 kişi hayatını kaybetti.
Heyelanların Türkiye’de doğal afet kaynaklı kayıplar arasında depremden sonra
en fazla ölüme neden olan afet türü olarak ikinci sırada yer aldığı
belirlendi. Son 20 yılda ölümcül heyelan ortalaması 12,2’ye, ölüm ortalaması
ise 23,6’ya yükseldi.

Araştırmaya göre, Türkiye'de 81 ilin 67’sinde ölümlü heyelan olayı yaşandı.
Ölümlü heyelanlarda 38 olay, 336 ölüm ile Trabzon, 30 olay, 191 ölüm ile Rize,
58 olay, 85 ölüm ile İstanbul'un hem olay hem de ölüm frekansının en yüksek
olduğu iller olduğu tespit edildi.

Türkiye'de en yüksek ölümlü heyelan vakası ise 1929'da Trabzon ile Rize
sınırında yaşandı. Toplam 19 köyü etkileyen afette 148 kişinin hayatını
kaybettiği kayıtlara yansıdı. 1995 yılında Isparta'nın Senirkent ilçesindeki
moloz akması olayında da 74 kişi hayatını kaybetti.

Araştırmayla ilgili AA muhabirine açıklamalarda bulunan Doç. Dr. Görüm,
Türkiye'de her yıl onlarca kişinin ölümüne neden olan çok sayıda heyelan
meydana geldiğini söyledi.

Türkiye'de heyelanların ele alınması ve ölümlerin kaydedilmesinin ihmal
edildiğini belirten Görüm, "Bu kapsamda 'Türkiye Ölümcül Heyelan Veri Tabanı'
çalışmasına 2017 yılında yüksek lisans öğrencim olan Seçkin Fidan ile
başladık. Çalışmadaki amacımız geçmişten günümüze heyelana bağlı ölümleri
incelemekti." dedi.

Görüm, heyelanların depremden sonra meydana gelen ölümlü doğal afetlerde
ikinci sırada olduğuna dikkati çekti.

1929 ile 2019 yılları arasındaki 90 yıllık dönemi Cumhurbaşkanlığı arşivleri,
gazeteler ve AFAD raporlarından araştırdıklarını ifade eden Görüm, şöyle devam
etti:

"Verilerde de heyelanların hangi bölgede, hangi nedenlere bağlı olarak
dağıldıklarını ortaya koyduk. Türkiye’deki ölümlü heyelanlar Doğu Karadeniz
Bölümü ve İstanbul çevresi olmak üzere iki bölgede yoğunlaşmaktadır. Genel
olarak, Doğu Karadeniz Bölümü’nde doğal faktörlerle tetiklenen ölümlü
heyelanlar yoğunluk gösterirken, İstanbul ve çevresinde ise antropojenik
faktörlerle tetiklenen ölümlü heyelan olayları yoğunluk göstermektedir. Ayrıca
ölümlerdeki artış nüfus artışına bağlı da paralellikte gösteriyor. Günümüze
yaklaştıkça artan nüfus aynı zamanda ölüm oranlarını da artırıyor. Araştırmada
Türkiye'de son 90 yılda 389 ölümlü heyelanda 1343 kişinin hayatını kaybettiği
tespit ettik. Bu heyelanlardan 883 kişinin ölümüyle sonuçlanan 147 olay doğal
faktörlerle (yağış, kar erimesi gibi hidrometeorolojik koşullar), 301 kişinin
ölümüyle sonuçlanan 197 ölümlü heyelan olayı ise antropojenik faktörlerle
(inşaat ve altyapı çalışmaları) tetiklenmiştir. 159 kişinin ölümüyle
sonuçlanan 45 olayın ise tetikleyici faktörü tespit edilememiştir."

Doğal faktörlerle tetiklenen ölümlü heyelan olaylarının yüzde 65'inin
Karadeniz Bölgesi'nde yaşandığını kaydeden Görüm, "Antropojenik faktörlerle
tetiklenen vakalarda 1-2 kişi hayatını kaybederken hidrometeorolojik
koşulların daha büyük alanları etkilemesi nedeniyle vaka başına 3-4 kişinin
hayatını kaybettiğini tespit ettik." dedi.

###  "Son 20 yılda heyelan olayları 2 kat arttı"

Son 20 yılda heyelanların iki kat arttığını anlatan Görüm, ortalama ölümlerin
de heyelan sayısıyla orantılı arttığını bildirdi.

Görüm, Türkiye'de heyelan riskinin en fazla olduğu bölgenin Doğu Karadeniz, en
az riskin olduğu yerin ise İç Anadolu Bölgesi olduğunu dile getirdi.

Heyelanların artmasının en önemli nedeninin nüfus ve değişen iklim koşulları
olduğunu vurgulayan Görüm, şu bilgileri verdi:

"Karadeniz Bölgesi'ndeki ölümlü heyelanların çoğu yaz döneminde gerçekleşmiş.
Bu da bize yaz döneminde Karadeniz'e düşen yağışının çok daha ekstrem bir
yağış karakteristiğine sahip olduğunu gösteriyor. Çok ani şekilde yüksek
miktarda yağış düştüğü için bu da topraktaki boşluk suyu basıncını artırıyor
ve birçok ölümlü vakaya neden oluyor. Mesela Batı Karadeniz'de, Türkiye'de
heyelan olma olasılığının en yüksek olduğu yerlerden birisi olmasına rağmen
ölüm sayısı düşük. Doğu Karadeniz'de heyelan ve ölüm olaylarının yüksek
olmasının nedeni dağınık yerleşme tipi, özellikle çay plantasyonu ve bu
alanlara ulaşmak için yapılmış çok yoğun yol ağlarıdır. Bu durum ölümleri daha
da arttırmış."

Görüm, FATALDOT'un yakın zamanda "Web Tabanlı Coğrafi Bilgi Sistemleri"
ortamında paylaşıma açılacağını, herkesin bu verilerden faydalanabileceğini
sözlerine ekledi.

Anadolu Ajansı web sitesinde, AA Haber Akış Sistemi (HAS) üzerinden abonelere
sunulan haberler, özetlenerek yayımlanmaktadır. **Abonelik için lütfen
iletişime geçiniz.**

 """
        }
    )
    
    if page:
        if (is_real_incident(page)):
            gpt_page = read_news(page)
            print(gpt_page)


# Pricing equation: \left(\frac{0.5}{10^{6}}\cdot2000+\frac{1.50}{10^{6}}\cdot30\right)\cdot1000

import pandas as pd

turkey_cities = [
    'adana', 'adıyaman', 'afyonkarahisar', 'ağrı', 'aksaray', 'amasya', 'ankara', 
    'antalya', 'ardahan', 'artvin', 'aydın', 'balıkesir', 'bartın', 'batman', 
    'bayburt', 'bilecik', 'bingöl', 'bitlis', 'bolu', 'burdur', 'bursa', 'çanakkale', 
    'çankırı', 'çorum', 'denizli', 'diyarbakır', 'düzce', 'edirne', 'elazığ', 'erzincan', 
    'erzurum', 'eskişehir', 'gaziantep', 'giresun', 'gümüşhane', 'hakkari', 'hatay', 
    'ığdır', 'ısparta', 'istanbul', 'izmir', 'kahramanmaraş', 'karabük', 'karaman', 
    'kars', 'kastamonu', 'kayseri', 'kırıkkale', 'kırklareli', 'kırşehir', 'kilis', 
    'kocaeli', 'konya', 'kütahya', 'malatya', 'manisa', 'mardin', 'mersin', 'muğla', 
    'muş', 'nevşehir', 'niğde', 'ordu', 'osmaniye', 'rize', 'sakarya', 'samsun', 
    'şanlıurfa', 'siirt', 'sinop', 'sivas', 'şırnak', 'tekirdağ', 'tokat', 'trabzon', 
    'tunceli', 'uşak', 'van', 'yalova', 'yozgat', 'zonguldak'
]

df = pd.read_csv("Heyelan_Verileri2.csv", encoding="utf-8")
df['il'] = df['il'].str.lower()
df_turkey = df[df['il'].isin(turkey_cities)]
df_turkey.to_csv("Turkiye_Heyelan_Verileri_son.csv", encoding="utf-8-sig", index=False)

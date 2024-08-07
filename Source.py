import pandas as pd
import re

# CSV dosyasını yükle
df = pd.read_csv("combined.csv", encoding="utf-8")

# Fonksiyon: Linkin sonundaki sayı kısmını siler
def remove_trailing_number(url):
    return re.sub(r'-\d+$', '', url)

# 'source_link' sütunundaki linklerin sonundaki sayı kısmını sil
df['source_link'] = df['source_link'].apply(remove_trailing_number)

# Değişiklikleri yeni bir CSV dosyasına kaydet
df.to_csv("combined_cleaned.csv", encoding="utf-8-sig", index=False)

print("Linklerin sonundaki sayı kısmı silindi ve değişiklikler combined_cleaned.csv adlı dosyaya kaydedildi.")

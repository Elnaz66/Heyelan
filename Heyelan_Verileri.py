import pandas as pd

df = pd.read_csv("combined_cleaned.csv", encoding="utf-8")

# source_link sütunundaki tüm değerleri küçük harfe çevirme
df['source_link'] = df['source_link'].str.lower()

# Aynı source_link değerine sahip satırları birleştirirken, keyword değerlerini bir araya getirme
df_grouped = df.groupby('source_link', as_index=False).agg({
    'keyword': lambda x: ', '.join(set(', '.join(x).split(', '))), 
    **{col: 'first' for col in df.columns if col != 'source_link' and col != 'keyword'}  
})
df_final = df_grouped.drop_duplicates(subset=['il', 'date','ilçe'])

df_final.to_csv("Heyelan_Verileri2.csv", encoding="utf-8-sig", index=False)
print("Tekrarlayan veriler kaldırıldı ve Heyelan_Verileri.csv adlı yeni dosyaya kaydedildi.")

#import pandas as pd

#df = pd.read_csv("combined_cleaned.csv", encoding="utf-8")
#df['source_link'] = df['source_link'].str.lower()

#df = df.drop_duplicates(subset=["source_link"])

#df.to_csv("Heyelan_Verileri.csv", encoding="utf-8-sig", index=False)
#print("Tekrarlayan veriler kaldırıldı ve Heyelan_Verileri.csv adlı yeni dosyaya kaydedildi.")
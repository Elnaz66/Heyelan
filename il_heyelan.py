import pandas as pd

df = pd.read_excel("Turkiye_Heyelan_Verileri_sonhali1.xlsx")
df['il'] = df['il'].str.lower()
#İl bazında grup oluşturup her gruptaki satır sayısını hesaplama
il_counts = df.groupby('il').size().reset_index(name='count')

# İl bazında veri sayımını içeren veri çerçevesini Excel dosyasına kaydetme
with pd.ExcelWriter("Il_Bazinda_Veriler.xlsx", engine="openpyxl") as writer:
    il_counts.to_excel(writer, index=False)

# *******************************************************************

#veri = pd.read_excel('Turkiye_Heyelan_Verileri_sonhali1.xlsx')

#il_olum = veri[['il', 'ölü_sayısı']]

# Her il için ölü sayılarını topla
#toplam_olum = il_olum.groupby('il').sum()
#toplam_olum.to_excel('il_Bazinda_Olusayisi.xlsx')

#print(toplam_olum)

import pandas as pd

df = pd.read_excel("Turkiye_Heyelan_Verileri_sonhali1.xlsx")
df['il'] = df['il'].str.lower()
il_counts = df.groupby('il').value_counts()

with pd.ExcelWriter("Il_Bazinda_Veriler.xlsx", engine="openpyxl") as writer:
    il_counts.to_excel(writer, index=False)

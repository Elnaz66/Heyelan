import pandas as pd

df = pd.read_excel("combined.csv")
df['il'] = df['il'].str.lower()
il_counts = df.groupby('il').value_counts()

with pd.ExcelWriter("il_bazinda_veriler.xlsx", engine="openpyxl") as writer:
    il_counts.to_excel(writer, index=False)

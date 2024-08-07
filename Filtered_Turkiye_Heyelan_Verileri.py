import pandas as pd
import re

df = pd.read_csv("Turkiye_Heyelan_Verileri_son.csv", encoding='utf-8')

keywords = [
    "çamur akıntısı", "çamur akması", "çamur hareketi", "çökme", "heyelan",
    "kaya çökmesi", "kaya devrilmesi", "kaya düşmesi", "kaya hareketi", "kaya kayması",
    "kaya yuvarlanması", "moloz akıntısı", "moloz akması", "moloz hareketi",
    "toprak çökmesi", "toprak hareketi", "toprak kayması", "toprak sürüklenmesi",
    "yamaç kayması", "yer çökmesi", "yer hareketleri", "yer kayması", "zemin çökmesi",
    "zemin hareketi", "zemin kayması"
]

regex = re.compile(r'\b(?:' + '|'.join(keywords) + r')\b', flags=re.IGNORECASE)

filtered_df = df[df['body'].str.contains(regex, na=False)]

filtered_df.to_csv("Turkiye_Heyelan_Verileri_sonhali.csv", index=False, encoding='utf-8-sig')






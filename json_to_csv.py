import json
import os

folders = ["gpt-version0", "gpt-version1", "gpt-version2", "gpt-version3"]

all_data = []

for folder in folders:
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_data.append(data)

with open("combined.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

import pandas as pd

df = pd.read_json("combined.json")

df.to_csv("combined.csv", encoding="utf-8-sig", index=False)

print("Veriler başarıyla birleştirildi ve combined.csv adlı CSV dosyasına dönüştürüldü.")


#import pandas as pd

#with open('combined.json', encoding='utf-8') as inputfile:
   # df = pd.read_json(inputfile)

#df.to_csv('csvfile.csv', encoding='utf-8', index=False)
import pandas as pd
import json

text_file = open("../table.html", "r")
data = text_file.read()

df_list = pd.read_html(data)
df = df_list[0]
df = df.replace({'~': ','}, regex=True)

items = {}

for index, row in df.iterrows():
    items[row['Name']] = {'range': row['Rng'], 'effect': row['Effects']}

with open('../items/staff.json') as f:
    data = json.load(f)

data.update(items)

with open("../items/staff.json", "w") as outfile:
    json.dump(data, outfile)


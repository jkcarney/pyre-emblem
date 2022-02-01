import pandas as pd
import json

text_file = open("table.html", "r")
data = text_file.read()

df_list = pd.read_html(data)
df = df_list[0]
df = df.replace({'~': ','}, regex=True)

items = {}

_valid_move_types = ['Foot', 'Armours', 'Knights1', 'Knights2', 'Nomads', 'NomadTroopers', 'Fighters', 'Bandits',
                     'Pirates', 'Mages', 'Fliers']

for index, row in df.iterrows():
    items[row['Terrain']] = {'avoid': row['Avoid'], 'def': row['Def'], 'Foot': row['Foot'], 'Armours': row['Armours'],
                             'Knights1': row['Knights 1'], "Knights2": row['Knights 2'], "Nomads": row['Nomads'],
                             "NomadTroopers": row['Nomad Troopers'], 'Fighters': row['Fighters'],
                             'Bandits': row['Bandits'], 'Pirates': row['Pirates'], 'Mages': row['Mages'],
                             'Fliers': row['Fliers']}

with open('../jsons/terrain.json') as f:
    data = json.load(f)

data.update(items)


with open("../jsons/terrain.json", "w") as outfile:
    json.dump(data, outfile)
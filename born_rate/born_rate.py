import requests
import json
import pandas as pd

# load data
response = requests.get('https://www.cia.gov/the-world-factbook/page-data/field/birth-rate/page-data.json')
data = json.loads(response.text)
nodes = data['result']['data']['fields']['nodes']

# shape data
df = pd.DataFrame(nodes)
df['birth_rate'] = df['formatted'].str.extract(r'([\d\.]+)').astype(float)
df_sorted = df.sort_values(by='birth_rate', ascending=True)
df_sorted.to_csv('born_rate.xlsx', sep='\t', index=False)
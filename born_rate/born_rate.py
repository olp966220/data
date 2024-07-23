import requests
import json
import pandas as pd
import re

def extract_str_from_brackets(text):
    match = re.search(r'\((.*?)\)', text)
    if match:
        return match.group(1)
    else:
        return None


# load data
response = requests.get('https://www.cia.gov/the-world-factbook/page-data/field/birth-rate/page-data.json')
data = json.loads(response.text)
nodes = data['result']['data']['fields']['nodes']

# shape data (births/1k population)
df = pd.DataFrame(nodes)
df['region'] = df['place'].apply(lambda x: x['region'])
df['birth_rate(births/1k population)'] = df['formatted'].str.extract(r'([\d\.]+)').astype(float)
df['time'] = df['formatted'].apply(extract_str_from_brackets)
df_sorted = df.sort_values(by='birth_rate(births/1k population)', ascending=True)
result = df_sorted[['time', 'region', 'placeName', 'birth_rate(births/1k population)']]
result.to_csv('born_rate.xlsx', sep='\t', index=False)
result.to_html('born_rate.html', index=False)


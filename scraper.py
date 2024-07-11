import requests
from bs4 import BeautifulSoup
import json

# URL of the Zenless Zone Zero Fandom wiki page
url = 'https://zenless-zone-zero.fandom.com/wiki/Agent/List'

# Parse the HTML content using BeautifulSoup
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# Get Agent data from URL.
data = []
table = soup.find('table', attrs={'class':'article-table sortable'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values
data.pop(0)

# Get list of Agent Names
#agents_list = []
#for Agent in data:
#    agents_list.append(Agent[0])

# Save the list of agents to a JSON file
with open('zenless_zone_zero_agents.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('Character list saved to zenless_zone_zero_agents.json')
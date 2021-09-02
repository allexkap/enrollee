import requests
from bs4 import BeautifulSoup

url = 'https://abit.itmo.ru/order/225/'
response = requests.get(url)
raw = response.text.encode(response.encoding).decode()
soup = BeautifulSoup(raw, 'html.parser')

result = []
titles = list(map(lambda l: l.text, soup.find_all('h3')))
for a, b in enumerate(soup.find_all('table')):
    scores = []
    for c in b.find_all('tr')[2:]:
        scores.append(int(c.find_all('td')[6].text))
    result.append((min(scores), len(scores), titles[a][9:]))
result.sort(key=lambda l: l[0] + 1 / l[1], reverse=True)
print('\n'.join(map(lambda l: '\t'.join(map(str, l)), result)))
#print(*result, sep='\n')

import os
import requests
from bs4 import BeautifulSoup

ch = {'без вступительных испытаний' : 'БВИ',
      'на бюджетное место в пределах особой квоты' : 'ОК',
      'на бюджетное место в пределах целевой квоты' : 'ЦК',
      'по общему конкурсу' : 'К',
      'на контрактной основе' : 'КО'}

for url in (f'https://abit.itmo.ru/bachelor/rating_rank/all/{x}/' for x in range(308, 337)):
    response = requests.get(url)
    raw = response.text.encode(response.encoding).decode()
    soup = BeautifulSoup(raw, 'html.parser')
    tp = ''
    out = []
    for row in soup.find_all('tr')[2:]:
        column = row.find_all('td')
        out.append([])
        if not column[0].text.isdigit():
            tp = column[0].text
            column.pop(0)
        for k in (0, 1, 2, 4, 5, 6, 9):
            if k == 2:
                out[-1].extend((column[k].text, tp))
            else:
                out[-1].append(int(column[k].text) if column[k].text else 0)
        out[-1].append(out[-1][-1] + out[-1][-2] + out[-1][-3] + out[-1][-4])
        out[-1].append(column[10].text == 'Да')
    dr = 'save/' + soup.title.text[37:-14] + '/'
    title = ' '.join(soup.p.text[23:].split()[::-1]) + '.csv'
    if not os.path.exists(dr):
        os.mkdir(dr)
    file = open(dr + title, 'w')
    wr = '\n'.join(map(lambda x: '\t'.join(map(lambda y: ch[y] if y in ch else y, map(str, x))), out))
    file.write(wr)
    file.close()
    print(title)

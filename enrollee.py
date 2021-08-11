import requests
from bs4 import BeautifulSoup

class Handler:
    def __init__(self, allmy: list):
        self.table = {'itmo' : self.itmo, 'spbgu' : self.spbgu, 'leti' : self.leti}
        self.soup = BeautifulSoup()
        self.allmy = allmy

        self.out = []
        self.title = ''
        self.time = ''
        self.ttl = 0
        self.bvi = 0
        self.sgl = 0
        self.ege = 0
        self.ost = 0
        self.k = []

        self.my = ()
        self.nm = 0

    def show(self, head: bool) -> str:
        rt = ''
        if head:
            rt += f'ttl\tbvi\tsgl\tost\tege\t|\t1\t2\t3\t4\t|\t{self.time}\n'
        rt += f'{self.ttl}\t{self.bvi}\t{self.sgl}\t{self.ost}\t{self.ege}\t|\t' \
              f'{self.k[0]}\t{self.k[1]}\t{self.k[2]}\t{self.k[3]}\t|\t{self.title}'
        return rt

    @staticmethod
    def comparator(a: list, b: list, f=True) -> bool:
        if not a and not b:
            return False
        if f:
            return sum(a) > sum(b) or sum(a) == sum(b) and Handler.comparator(a, b, False)
        else:
            return a[0] > b[0] or a[0] == b[0] and Handler.comparator(a[1:], b[1:], False)

    def analytics(self):
        k = [0, 0, 0, 0]
        ege, sgl = 0, 0
        for line in self.out:
            if Handler.comparator(line[2:6], self.my):
                if line[6]:
                    sgl += 1
                else:
                    ege += 1
                    k[line[1] - 1 if line[1] <= 4 else 3] += 1
        self.bvi = self.out[0][0] - 1
        self.sgl = sgl
        self.ege = ege
        self.k = k
        self.ost = self.ttl - self.bvi - self.sgl

    def get(self, fn: str, e: int, url: str) -> str:
        response = requests.get(url)
        raw = response.text.encode(response.encoding).decode()
        self.soup = BeautifulSoup(raw, 'html.parser')
        self.nm = e
        self.table[fn]()
        self.analytics()
        return self.show(not e)

    def itmo(self):
        out = []
        ok = False
        for row in self.soup.find_all('tr')[2:]:
            column = row.find_all('td')
            if not ok:
                if column[0].text == 'по общему конкурсу':
                    ok = True
                    column.pop(0)
                else:
                    continue
            if not column[0].text.isdigit():
                break
            out.append([])
            for k in (0, 1, 4, 5, 6, 9):
                out[-1].append(int(column[k].text) if column[k].text else 0)
            out[-1].append(column[10].text == 'Да')
        self.out = out

        self.my = self.allmy[0]
        self.title = self.soup.title.text[37:-14]
        self.time = self.soup.p.text[23:]
        temp = self.soup.body.h1.text
        self.ttl = int(temp[temp.rindex('К:') + 2: temp.index('),')])

    def spbgu(self):
        out = []
        for row in self.soup.find_all('tr')[1:]:
            column = row.find_all('td')
            if column[2].text != 'По результатам ВИ':
                continue
            out.append([])
            for k in (0, 3, 6, 7, 8, 9):
                temp = column[k].text.replace(',', ' ').replace('.', ' ').split()
                out[-1].append(int(temp[0]) if temp else 0)
            out[-1].append(column[10].text == 'Да')
        self.out = out

        self.my = self.allmy[1]
        temp = self.soup.body.text
        a = temp.index('Направление')
        b = temp.index(' \n', a)
        self.title = temp[a + 13: b]
        a = temp.index('обновления')
        b = temp.index('\n', a)
        self.time = temp[a + 12: b]
        a = temp.index('конкурсу')
        b = temp.index(' \n', a)
        total = int(temp[a + 10: b])
        for _ in range(2):
            a = temp.index('квота', b)
            b = temp.index(' \n', a)
            total -= int(temp[a + 7: b])
        self.ttl = total

    def leti(self):
        out = []
        for row in self.soup.find_all('tr')[2:]:
            column = row.find_all('td')
            if column[3].text != 'ОК':
                continue
            out.append([])
            for k in (0, 2, 5, 6, 7, 8):
                out[-1].append(int(column[k].text) if column[k].text != '-' else 0)
            out[-1].append(column[10].text == 'Да')
        self.out = out

        self.my = self.allmy[1]
        self.title = self.soup.title.text
        self.time = self.soup.p.text[37:55]
        self.ttl = (39, 49, 43)[self.nm]

def save(rt):
    global log
    log += rt + '\n'
    print(rt)

allmy = ((93, 94, 84, 8),
         (94, 93, 84, 0),
         (94, 99, 84, 0))
handler = Handler(allmy)

itmo = (f'https://abit.itmo.ru/bachelor/rating_rank/all/{x}/' for x in (313, 314))
spbgu = (f'https://cabinet.spbu.ru/Lists/1k_EntryLists/list_{x}.html' for x in ('ee25050d-89ab-41ba-8cfa-016f3afe1b33',
                                                                                '94eb54ce-57aa-45e7-9be3-3acd8bf9ca38'))
leti = (f'https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/podavshie-zayavlenie/{x}' for x in ())
name = ['itmo', 'spbgu', 'itmo']
isl = (itmo, spbgu)

log = ''
for gen in enumerate(isl):
    save(name[gen[0]])
    for url in enumerate(gen[1]):
        save(handler.get(name[gen[0]], *url))
    if gen[0] < len(isl) - 1:
        save('')
log += '-' * 52 + '\n'
open('out', 'a').write(log)

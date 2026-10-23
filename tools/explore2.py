import re, json, html as H
from bs4 import BeautifulSoup
s = open('_original_site/html/lab-members.html', encoding='utf-8').read()
soup = BeautifulSoup(s, 'lxml')
root = soup.find(id='PAGES_CONTAINER')
# find the first member heading and show its ancestors / siblings structure
h3 = [h for h in root.find_all('h3') if 'Michelle' in h.get_text()][0]
chain = []
el = h3
for _ in range(8):
    el = el.parent
    chain.append((el.name, el.get('id'), (el.get('class') or [])[:2], len(el.find_all('img')), len(el.find_all('wow-image'))))
for c in chain: print(c)
# the strip containing both image and text
strip = h3.find_parent(lambda t: t.name and t.find('wow-image') and t.find('h3'))
print('strip', strip.name, strip.get('id'))
print(str(strip)[:1500])

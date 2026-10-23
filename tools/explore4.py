import re
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('_original_site/html/lab-members.html', encoding='utf-8').read(), 'lxml')
root = soup.find(id='PAGES_CONTAINER')
members = [h.get_text(' ',strip=True) for h in root.find_all('h3')]
imgs=[]; seen=set()
for im in root.find_all('img'):
    m = re.search(r'media/([^/]+~mv2\.\w+)', im.get('src',''))
    if m and m.group(1) not in seen and (im.get('width')):
        seen.add(m.group(1)); imgs.append((m.group(1), im.get('alt')))
print(len(members), 'members;', len(imgs), 'member images')
for i in range(max(len(members),len(imgs))):
    print(i, members[i] if i<len(members) else '-', '<->', imgs[i][1] if i<len(imgs) else '-')

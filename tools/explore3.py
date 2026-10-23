import re, json, html as H
from bs4 import BeautifulSoup
s = open('_original_site/html/lab-members.html', encoding='utf-8').read()
soup = BeautifulSoup(s, 'lxml')
root = soup.find(id='PAGES_CONTAINER')
for el in root.descendants:
    n = getattr(el,'name',None)
    if n=='h3': print('H3', el.get_text(' ',strip=True))
    elif n=='img':
        src = el.get('src','')
        m = re.search(r'media/([^/]+~mv2\.\w+)', src)
        print('  IMG', m.group(1) if m else src[:60], '| alt=', el.get('alt'), '| w/h', el.get('width'), el.get('height'))
    elif n=='div' and el.get('data-testid')=='gallery-item-ghost' : print('  GALLERY-ITEM', el.get('aria-label'))
    elif n=='div' and el.get('aria-label') and 'gHvfPd' in (el.get('class') or []): print('  GALLERY-ITEM', el.get('aria-label'))

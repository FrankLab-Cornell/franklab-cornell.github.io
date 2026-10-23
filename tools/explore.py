import sys, json, html as H
from bs4 import BeautifulSoup
s = open('_original_site/html/lab-members.html', encoding='utf-8').read()
soup = BeautifulSoup(s, 'lxml')
root = soup.find(id='PAGES_CONTAINER') or soup.body
print('root', root.name, root.get('id'))
n=0
for el in root.descendants:
    if getattr(el,'name',None) in ('h1','h2','h3','h4','p','wow-image'):
        if el.name=='wow-image':
            info=json.loads(H.unescape(el.get('data-image-info','{}')) or '{}') if el.get('data-image-info') else {}
            im=info.get('imageData',{})
            print('IMG', im.get('uri'), im.get('name'), el.get('id'))
        else:
            t=el.get_text(' ',strip=True)
            if t: print(el.name.upper(), t[:90])
        n+=1
        if n>60: break

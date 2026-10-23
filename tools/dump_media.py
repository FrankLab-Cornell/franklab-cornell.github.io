import sys, re, json, html as H
sys.path.insert(0,'tools')
from wixmd import *
for page in sys.argv[1:]:
    soup, root = load(f'_original_site/html/{page}.html')
    print('=====', page)
    for el in root.descendants:
        n = getattr(el,'name',None)
        if n in ('h1','h2','h3'):
            print(n.upper(), el.get_text(' ',strip=True)[:60])
        if n=='img':
            m=re.search(r'media/([^/]+~mv2\.\w+)', el.get('src',''))
            print('  IMG', m.group(1) if m else el.get('src','')[:80], '| alt:', el.get('alt'), '|', el.get('width'), el.get('height'))
        if n=='wow-image':
            info=el.get('data-image-info')
            if info:
                d=json.loads(H.unescape(info)).get('imageData',{})
                print('  WOW', d.get('uri'), '|', d.get('alt'), d.get('width'), d.get('height'))
        st = el.get('style') if hasattr(el,'get') else None
        if st and 'wixstatic' in st: print('  STYLE-BG', re.findall(r'media/([^/)"]+)', st)[:2])
        if hasattr(el,'attrs'):
            for k,v in el.attrs.items():
                if isinstance(v,str) and 'wixstatic.com/media' in v and n not in ('img',) and k not in ('style','data-image-info'):
                    print('  ATTR', n, k, re.findall(r'media/([^/"]+)', v)[:1])

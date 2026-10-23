import sys
sys.path.insert(0, 'tools')
from wixmd import *
for page in sys.argv[1:]:
    soup, root = load(f'_original_site/html/{page}.html')
    print('=====', page)
    for tag, t in rich_blocks(root):
        print(f'[{tag}]', t.replace('\n', ' / ')[:400])

"""Helpers to convert Wix (Thunderbolt) rendered HTML into clean Markdown.
Source of truth is original_site/html/*.html (the text/*.md files are lossy)."""
import re, html as H
from bs4 import BeautifulSoup, NavigableString

ZW = dict.fromkeys(map(ord, '\u200b\u200c\u200d\ufeff'), None)

def clean(t):
    t = t.translate(ZW).replace('\xa0', ' ').replace('\r', '')
    return re.sub(r'[ \t]+', ' ', t)

def inline(el):
    """Convert inline content of el to markdown (links, bold, italics)."""
    out = []
    for c in el.children:
        if isinstance(c, NavigableString):
            out.append(clean(str(c)))
        elif c.name == 'br':
            out.append('\n')
        elif c.name == 'a':
            href = c.get('href', '')
            txt = inline(c).strip()
            if href and txt and not href.startswith('#'):
                out.append(f'[{txt}]({href})')
            else:
                out.append(txt)
        elif c.name in ('strong', 'b'):
            t = inline(c)
            out.append(f'**{t.strip()}**' + (' ' if t.endswith(' ') else '') if t.strip() else t)
        elif c.name in ('em', 'i'):
            t = inline(c)
            out.append(f'*{t.strip()}*' + (' ' if t.endswith(' ') else '') if t.strip() else t)
        else:
            out.append(inline(c))
    s = ''.join(out)
    return s

def tidy(s):
    s = re.sub(r'\*\*\s*\*\*', '', s)
    s = re.sub(r'[ ]*\n[ ]*', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    s = re.sub(r'[ ]{2,}', ' ', s)
    return s.strip()

def rich_blocks(root):
    """Yield (tag, markdown_text) for each text block in document order."""
    for rt in root.find_all(attrs={'data-testid': 'richTextElement'}):
        for blk in rt.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol'], recursive=False):
            if blk.name in ('ul', 'ol'):
                for li in blk.find_all('li'):
                    t = tidy(inline(li))
                    if t: yield ('li', t)
            else:
                t = tidy(inline(blk))
                if t: yield (blk.name, t)

def load(path):
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'lxml')
    return soup, soup.find(id='PAGES_CONTAINER')

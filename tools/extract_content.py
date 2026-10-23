"""Step 2: build clean Markdown content + image manifest from the saved Wix HTML.
Run:  .venv/bin/python tools/extract_content.py   (then python3 tools/process_images.py)"""
import sys, re, json
sys.path.insert(0, 'tools')
from wixmd import *

CORRECTIONS = []   # (where, before, after) -> reported at the end

def fix_url(u):
    n = re.sub(r'https://([a-z0-9-]+)\.proxy\.library\.cornell\.edu',
               lambda m: 'https://' + m.group(1).replace('-', '.'), u)
    if n != u: CORRECTIONS.append(('link', u, n))
    return n

def fix_links(md):
    md = re.sub(r'\]\((https?://[^)\s]+)\)', lambda m: '](' + fix_url(m.group(1)) + ')', md)
    return md

def autolink(md):
    """Turn bare http(s) URLs (not already inside a markdown link) into links."""
    def rep(m):
        url = m.group(0).rstrip('.,;')
        tail = m.group(0)[len(url):]
        return f'<{url}>' + tail
    return re.sub(r'(?<![\(<\[])https?://[^\s)<>\]]+', rep, md)

def slug(s):
    s = s.lower().replace("'", '').replace('í', 'i').replace('é', 'e')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def write(path, text):
    open(path, 'w', encoding='utf-8').write(text.rstrip() + '\n')

manifest = []   # images to process
def add_img(file, group, slg, alt):
    if not any(m['slug'] == slg and m['group'] == group for m in manifest):
        manifest.append({'file': file, 'group': group, 'slug': slg, 'alt': alt})
    return f'images/{group}/{slg}.jpg'

# ---------------------------------------------------------------- HOME
soup, root = load('_original_site/html/home.html')
blocks = list(rich_blocks(root))
DATE = re.compile(r'^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Spring|Summer|Fall|Winter)\s+\d{4}\s*[-:\u2013]', re.I)
news = []   # each: {'text':..., 'sub':[...]} or {'note':...}
for tag, t in blocks:
    if tag in ('h1', 'h2'): continue
    t = autolink(fix_links(t))
    if DATE.match(t):
        news.append({'text': t, 'sub': []})
    elif news and news[-1].get('text') and (t.startswith('[') or t.startswith('<')) and not news[-1].get('note'):
        news[-1]['sub'].append(t)
    else:
        news.append({'note': t})
lines = ['---', 'title: "Frank Lab"', '---', '', '# Welcome to the Frank Lab', '', '## Recent News', '']
for n in news:
    if 'note' in n:
        lines += ['', f'*{n["note"]}*', '']
    else:
        lines.append(f'- {n["text"]}')
        for s in n['sub']:
            lines.append(f'    - {s}')
write('content/index.md', '\n'.join(lines))
# NB: the original ends with a "Read More" button linking to the NESDB 2022 meeting page; it is already
# linked from the Feb 2022 news item, so it is not carried over.

# ---------------------------------------------------------------- ABOUT
soup, root = load('_original_site/html/mission-statement.html')
img = add_img('de23fd_4ef95ad3315a4884bfec08ae7cf36e3c~mv2.jpeg', 'about', 'about-lab', 'Lab members jumping in the snow in front of a frozen waterfall')
lines = ['---', 'title: "About Us"', '---', '', '# About Us', '', f'![{manifest[-1]["alt"]}]({img})', '']
for tag, t in rich_blocks(root):
    if tag == 'h1': continue
    t = fix_links(t)
    if tag == 'h2': lines += [f'## {t}', '']
    else:
        # bold the leading label ("Scientific scholarship:") for readability
        t = re.sub(r'^([A-Z][A-Za-z ]{3,45}):', r'**\1:**', t)
        lines += [t, '']
write('content/about.md', '\n'.join(lines))

# ---------------------------------------------------------------- RESEARCH
soup, root = load('_original_site/html/plant-grafting.html')
r = lambda f, slg, alt: add_img(f, 'research', slg, alt)
hero    = r('0cb15d_07796e84b3284f8db0231f700f7ac5c3~mv2.jpg', 'hero-plant-grafting', 'Grafted pepper seedling with roots')
fig_inc = r('0cb15d_775c18082cb24931ba2f534c7f54086f~mv2.png', 'graft-incompatibility', 'Anatomy of compatible and incompatible tomato and pepper grafts')
bg_ldc  = r('0cb15d_53f07b56068245adbf0f6877ee3243b5~mv2.jpg', 'bg-long-distance-communication', 'Grafted tomato plants')
vigor   = r('0cb15d_0f3ead46a35a425ca45a472a8a5ba27f~mv2.jpg', 'graft-induced-vigor', 'Lab member inspecting a grafted tomato plant in the greenhouse')
mobile  = r('0cb15d_5723f919aa9c4f63b08a66702252510b~mv2.png', 'graft-mobileomes', 'Confocal images of a tomato/eggplant graft junction')
bg_sust = r('0cb15d_7204f9c08627400e8ace9d9b9a74bf53~mv2.jpg', 'bg-sustainable-agriculture', 'Field of crops')
soy     = r('0cb15d_1351704901f24dc4abdfcfd3b5fc7517~mv2.jpg', 'hybrid-soybean', 'Bee visiting a soybean flower')
imgs = {'Plant Grafting': hero, 'Biology of Graft Incompatibility': fig_inc, 'Long-distance Communication': bg_ldc,
        'Graft-induced Vigor': vigor, 'Characterizing Graft "Mobileomes"': mobile,
        'Sustainable Agriculture': bg_sust, 'Making a Hybrid Soybean': soy}
alts = {v: next(m['alt'] for m in manifest if m['group']=='research' and f'images/research/{m["slug"]}.jpg' == v) for v in imgs.values()}
lines = ['---', 'title: "Research"', '---', '', '# Research: Plant Grafting', '', f'![{alts[hero]}]({hero})', '']
for tag, t in rich_blocks(root):
    if tag == 'h1': continue
    t = fix_links(t)
    if tag == 'h2':
        lines += [f'## {t}', '']
        if t in imgs: lines += [f'![{alts[imgs[t]]}]({imgs[t]})', '']
    else:
        lines += [t, '']
write('content/research.md', '\n'.join(lines))

# ---------------------------------------------------------------- CONTACT
soup, root = load('_original_site/html/contact.html')
lines = ['---', 'title: "Contact"', '---', '', '# Contact Us', '']
for tag, t in rich_blocks(root):
    if tag == 'h1': continue
    t = fix_links(t)
    if t.startswith('Mailing Address:'):
        parts = [p.strip() for p in t.split('\n') if p.strip()]
        lines += ['## Mailing Address', '']
        addr, rest = [], []
        for p in parts[1:]:
            (rest if re.match(r'(Telephone|Email|Margaret|Frank Lab)', p) else addr).append(p)
        lines += ['  \n'.join(addr), '']
        for p in rest: lines += [p, '']
    elif tag == 'h2':
        lines += [f'## {t}', '']
    else:
        lines += [t, '']
write('content/contact.md', '\n'.join(lines))

# ---------------------------------------------------------------- PEOPLE
soup, root = load('_original_site/html/lab-members.html')
# gallery slideshow at the top of the page
gal = [('d0f4d05d0b5e4ccb858d92a3b9187867~mv2.jpg', 'c920f0_', 'field-season-2026', 'Field season 2026'),
       ('d0527c106926477b9cf24b11d9594df6~mv2.png', 'c920f0_', 'lab-photo-2', 'Lab group photo'),
       ('b605710e7cc74181bde3fefbd1fa69b1~mv2.jpeg', 'c920f0_', 'lab-photo-3', 'Lab group photo')]
gallery = [add_img(p + f, 'groups', s, a) for f, p, s, a in gal]

# DOM walk: heading / image events (member photos are the <img> tags that carry a width attribute)
events = []
for el in root.descendants:
    n = getattr(el, 'name', None)
    if n == 'h3':
        events.append(('h3', el.get_text(' ', strip=True)))
    elif n == 'img' and el.get('width'):
        m = re.search(r'media/([^/]+~mv2\.\w+)', el.get('src', ''))
        if m: events.append(('img', m.group(1), el.get('alt') or ''))
names = [e[1] for e in events if e[0] == 'h3']
imgs_all = []
for e in events:
    if e[0] == 'img' and e[1] not in [x[0] for x in imgs_all]: imgs_all.append((e[1], e[2]))

photo = {}
# members 0..34: images are in the same order as the names (alt text/file names cross-checked)
for i in range(0, 35): photo[names[i]] = imgs_all[i]
# Manual correction from Margaret's lab (2026-10-22): the two photos at positions 3-4 were swapped by the order rule.
photo['Elise Boisevert'], photo['Jessica Morgan'] = photo['Jessica Morgan'], photo['Elise Boisevert']
# members 35..end: each image sits directly BEFORE its heading; take the last image before each heading
last = None
img_before = {}
cur = []
for e in events:
    if e[0] == 'img': cur.append((e[1], e[2]))
    else:
        img_before[e[1]] = cur[-1] if cur else None; cur = []
for nme in names[35:]: photo[nme] = img_before[nme]
# the extra screenshot that precedes Thomas Lonergan's photo is not used by any heading
used = {v[0] for v in photo.values() if v}
UNUSED = [x for x in imgs_all if x[0] not in used]

blocks = list(rich_blocks(root))
members, cur = [], None
for tag, t in blocks:
    if tag == 'h3':
        cur = {'name': t, 'blocks': []}; members.append(cur)
    elif cur is not None:
        cur['blocks'].append(t)
assert [m['name'] for m in members] == names, 'name/heading mismatch'

NAME_FIX = {'Elise Boisevert': 'Elise Boisvert', 'Samantha Pellitier': 'Samantha Pelletier'}
ROLE_FIX = {'Principle Investigator': 'Principal Investigator', 'Post-Doctoral Resarcher': 'Post-Doctoral Researcher'}
CURRENT_END = names.index('Annabel and Graham')   # everything up to here is listed first on the Wix page
people = []
for m in members:
    blks = [fix_links(b) for b in m['blocks'] if re.search(r'[A-Za-z0-9]', b) and b.strip() not in ('.',)]
    # drop stray link-only fragments like a lone "[Nelson](...)" line? keep, but report
    role = blks[0] if blks else ''
    bio = blks[1:]
    name = m['name']
    if name in NAME_FIX:
        CORRECTIONS.append(('name', name, NAME_FIX[name])); name = NAME_FIX[name]
    if role in ROLE_FIX:
        CORRECTIONS.append(('role', role, ROLE_FIX[role])); role = ROLE_FIX[role]
    p = photo.get(m['name'])
    ph = None
    if p:
        ph = add_img(p[0], 'people', slug(name), f'Photo of {name}')
    idx = names.index(m['name'])
    people.append({'name': name, 'role': role, 'group': 'current' if (idx <= CURRENT_END or name == 'Weiwei Chen') else 'alumni',
                   'photo': ph, 'photo_original_name': p[1] if p else None,
                   'bio': [autolink(b) for b in bio]})

def y(s): return json.dumps(s, ensure_ascii=False)
out = ['# Lab members, in the same order as the original Wix page.',
       '# group: "current" vs "alumni" is a best guess from the original ordering -> Margaret to confirm.']
for p in people:
    out.append(f'- name: {y(p["name"])}')
    out.append(f'  role: {y(p["role"])}')
    out.append(f'  group: {p["group"]}')
    out.append(f'  photo: {y(p["photo"])}' if p['photo'] else '  photo: null')
    out.append('  bio:' if p['bio'] else '  bio: []')
    for b in p['bio']: out.append(f'    - {y(b)}')
write('content/people.yml', '\n'.join(out))

lines = ['---', 'title: "Lab Members"', '---', '', '# Lab Members', '']
for g, alt in zip(gallery, [x[3] for x in gal]): lines.append(f'![{alt}]({g})')
lines.append('')
def person_md(p):
    L = [f'### {p["name"]}', '', f'*{p["role"]}*', '']
    if p['photo']: L += [f'![{p["name"]}]({p["photo"]})', '']
    for b in p['bio']: L += [b, '']
    return L
lines += ['## Current Lab Members', '']
for p in people:
    if p['group'] == 'current': lines += person_md(p)
lines += ['## Alumni', '']
for p in people:
    if p['group'] == 'alumni': lines += person_md(p)
write('content/people.md', '\n'.join(lines))

# ---------------------------------------------------------------- manifest + report
json.dump(manifest, open('content/image_manifest.json', 'w'), indent=2, ensure_ascii=False)
print('members:', len(people), '| with photo:', sum(1 for p in people if p['photo']),
      '| photos used:', len(used), '| unused member images:', UNUSED)
print('manifest images:', len(manifest))
for c in CORRECTIONS: print('FIX', c)

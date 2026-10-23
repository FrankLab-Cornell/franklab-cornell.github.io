"""Make contact sheets of the people photos (for checking name<->photo pairing). Output goes to content/_review/."""
import json, os
from PIL import Image, ImageDraw
m = [x for x in json.load(open('content/image_manifest.json')) if x['group'] == 'people']
os.makedirs('content/_review', exist_ok=True)
def sheet(items, out, cols=6, tw=200, th=260):
    rows = (len(items) + cols - 1) // cols
    S = Image.new('RGB', (cols * tw, rows * (th + 20)), 'white'); d = ImageDraw.Draw(S)
    for i, x in enumerate(items):
        im = Image.open(f"images/people/{x['slug']}.jpg"); im.thumbnail((tw - 6, th))
        S.paste(im, ((i % cols) * tw + 3, (i // cols) * (th + 20)))
        d.text(((i % cols) * tw + 3, (i // cols) * (th + 20) + th + 3), x['slug'][:32], fill='black')
    S.save(out)
sheet(m[:18], 'content/_review/people_1.jpg'); sheet(m[18:36], 'content/_review/people_2.jpg'); sheet(m[36:], 'content/_review/people_3.jpg')

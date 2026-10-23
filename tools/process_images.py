"""Resize/compress the original Wix images for the new site.
Run with the conda python (has Pillow):  python3 tools/process_images.py
Reads original_site/images/*, writes images/<group>/<slug>.jpg (EXIF-rotated, max width per group)."""
import json, os, re, sys
from PIL import Image, ImageOps
sys.path.insert(0, 'tools')

SRC = '_original_site/raw_images'
OUT = 'images'
# group -> (max_width, jpeg_quality)
LIMITS = {'people': (700, 84), 'groups': (1800, 82), 'research': (1800, 82), 'about': (1800, 82)}

def save(src_file, group, slug):
    w_max, q = LIMITS[group]
    im = Image.open(os.path.join(SRC, src_file))
    im = ImageOps.exif_transpose(im)
    if im.mode in ('RGBA', 'LA', 'P'):
        bg = Image.new('RGB', im.size, (255, 255, 255))
        im = im.convert('RGBA'); bg.paste(im, mask=im.split()[-1]); im = bg
    else:
        im = im.convert('RGB')
    if im.width > w_max:
        im = im.resize((w_max, round(im.height * w_max / im.width)), Image.LANCZOS)
    os.makedirs(os.path.join(OUT, group), exist_ok=True)
    out = os.path.join(OUT, group, slug + '.jpg')
    im.save(out, 'JPEG', quality=q, optimize=True, progressive=True)
    return out, im.size

if __name__ == '__main__':
    manifest = json.load(open('content/image_manifest.json'))
    total_in = total_out = 0
    for item in manifest:
        out, size = save(item['file'], item['group'], item['slug'])
        total_in += os.path.getsize(os.path.join(SRC, item['file'])); total_out += os.path.getsize(out)
        item['out'] = out; item['size'] = list(size)
    json.dump(manifest, open('content/image_manifest.json', 'w'), indent=2)
    print(f'{len(manifest)} images: {total_in/1e6:.1f} MB -> {total_out/1e6:.1f} MB')

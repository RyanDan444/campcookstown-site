#!/usr/bin/env python3
"""Grade and export every site photo as AVIF + WebP + JPEG at several widths.

Grading is gentle and honest: a touch of levels, local contrast, vibrance (saturation that
lifts dull colours more than already-rich ones), and sharpening after each resize.
Writes <out>/<slug>-w<width>.<ext> and <out>/manifest.json (slug -> {w, h, widths, focus}).
"""
import os, sys, json
import numpy as np, cv2
from PIL import Image, ImageFilter

SRC_DIRS = {
    '/home/claude/cc/photos/src': None,
}
UP = '/mnt/user-data/uploads'
EXTRA = {  # path -> slug
    f'{UP}/Camp Cookstown/homepage/willow-4k.png': 'film-willow',
    f'{UP}/Camp Cookstown/homepage/nap-4k.png': 'film-nap',
    f'{UP}/Camp Cookstown/homepage/belly-4k.png': 'film-belly',
    f'{UP}/Camp Cookstown/homepage/golden-4k.png': 'film-golden',
    f'{UP}/Camp Cookstown/homepage/hose-4k.png': 'film-hose',
    f'{UP}/Camp Cookstown/homepage/spa-4k.png': 'film-spa',
    f'{UP}/Camp Cookstown/homepage/camp-pano.jpg': 'camp-pano',
    f'{UP}/Downloads/carousel/real4k/2barn-blk-2k.jpg': 'barn-lane-pano',
    f'{UP}/Downloads/carousel/real4k/862356-4k.jpg': 'barn-inside-a',
    f'{UP}/Downloads/carousel/real4k/9a24a1e-4k.jpg': 'barn-inside-b',
    f'{UP}/Downloads/carousel/real4k/eee38bc-4k.jpg': 'barn-inside-beds',
    f'{UP}/Downloads/carousel/real4k/baffd50-blk-4k.jpg': 'field-pack-barn',
    f'{UP}/Downloads/carousel/real4k/cf57924-blk-4k.jpg': 'field-pack-lane',
    f'{UP}/Downloads/carousel/real4k/2e532b4-4k.jpg': 'field-run',
    f'{UP}/Downloads/carousel/real4k/7ffb652-4k.jpg': 'pool-two-dogs',
    f'{UP}/Downloads/carousel/real4k/ae3ac6b-4k.jpg': 'pool-shake',
    f'{UP}/Downloads/carousel/real4k/89aa4d2-4k.jpg': 'barn-asleep-shavings',
    f'{UP}/Downloads/carousel/real4k/5876685-blk-4k.jpg': 'aussie-bucket',
    f'{UP}/Downloads/carousel/real4k/fae819a-4k.jpg': 'golden-yawn',
    f'{UP}/Downloads/carousel/real4k/77d233e-4k.jpg': 'white-dog-roll',
}
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/cc/photos/out'
WIDTHS = [480, 900, 1600, 2400]
# per image tweaks: vibrance, contrast (clahe clip), warmth
TWEAK = {
    'dachshund-nap': dict(vib=0.22), 'frenchies-grass': dict(vib=0.18), 'goldens-asleep': dict(vib=0.14),
    'barn-inside-a': dict(vib=0.10, warm=3), 'barn-inside-b': dict(vib=0.10, warm=3), 'barn-inside-beds': dict(vib=0.10, warm=3),
    'barn-asleep-shavings': dict(vib=0.10, warm=2),
    'film-nap': dict(vib=0.12), 'film-belly': dict(vib=0.10),
}


def grade(img_bgr, vib=0.16, clahe=1.15, warm=0):
    img = img_bgr.astype(np.float32) / 255.0
    # levels on luminance, 0.15% clip, gentle
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lo, hi = np.percentile(lum, 0.15), np.percentile(lum, 99.85)
    if hi - lo > 0.2:
        img = np.clip((img - lo) / (hi - lo), 0, 1) * 0.985 + 0.0075  # keep a hair of headroom
    # local contrast on L (LAB), subtle
    lab = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    cl = cv2.createCLAHE(clipLimit=clahe, tileGridSize=(8, 8))
    l2 = cl.apply(l)
    l = cv2.addWeighted(l, 0.55, l2, 0.45, 0)
    lab = cv2.merge((l, a, b))
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR).astype(np.float32) / 255.0
    # vibrance: HSV saturation lift weighted toward low saturation pixels
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = np.clip(s + vib * s * (1.0 - s) * 2.2, 0, 1)
    hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    if warm:
        img[..., 2] = np.clip(img[..., 2] + warm / 255.0, 0, 1)  # red up a hair
        img[..., 0] = np.clip(img[..., 0] - warm / 255.0, 0, 1)  # blue down a hair
    return np.clip(img * 255, 0, 255).astype(np.uint8)


def export(pil, slug, widths, manifest, src_w, src_h):
    manifest[slug] = {'w': src_w, 'h': src_h, 'widths': []}
    for w in widths:
        if w > src_w * 1.5:
            continue
        if w >= src_w:
            im = pil if w == src_w else pil.resize((w, round(src_h * w / src_w)), Image.LANCZOS)
        else:
            im = pil.resize((w, round(src_h * w / src_w)), Image.LANCZOS)
        # sharpen after resize, gentle
        im = im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=48 if w < src_w else 70, threshold=2))
        im.save(os.path.join(OUT, f'{slug}-w{w}.avif'), quality=62, speed=4)
        im.save(os.path.join(OUT, f'{slug}-w{w}.webp'), quality=80, method=6)
        im.save(os.path.join(OUT, f'{slug}-w{w}.jpg'), quality=82, optimize=True, progressive=True)
        manifest[slug]['widths'].append(w)
    manifest[slug]['h_over_w'] = round(src_h / src_w, 4)


def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    jobs = []
    for d in SRC_DIRS:
        for f in sorted(os.listdir(d)):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                jobs.append((os.path.join(d, f), os.path.splitext(f)[0]))
    jobs += list(EXTRA.items())
    only = set(sys.argv[2:]) if len(sys.argv) > 2 else None
    for path, slug in jobs:
        if only and slug not in only:
            continue
        if not os.path.exists(path):
            print('MISSING', path); continue
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            print('unreadable', path); continue
        h, w = img.shape[:2]
        if w > 2600:  # keep masters sane: nothing on the site is served above 2400
            s = 2600 / w
            img = cv2.resize(img, (2600, round(h * s)), interpolation=cv2.INTER_AREA)
            h, w = img.shape[:2]
        t = TWEAK.get(slug, {})
        g = grade(img, **t)
        pil = Image.fromarray(cv2.cvtColor(g, cv2.COLOR_BGR2RGB))
        export(pil, slug, WIDTHS, manifest, w, h)
        print(f'{slug:24s} {w}x{h} -> {manifest[slug]["widths"]}')
        sys.stdout.flush()
    mpath = os.path.join(OUT, 'manifest.json')
    old = json.load(open(mpath)) if os.path.exists(mpath) else {}
    old.update(manifest)
    json.dump(old, open(mpath, 'w'), indent=1)
    print('manifest', len(old))


if __name__ == '__main__':
    main()

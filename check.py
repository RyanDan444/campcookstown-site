#!/usr/bin/env python3
"""Verify the built site in out/: every internal link and asset resolves, no em or en dashes, word counts.
python3 check.py   (expects 'links ok' and 'dashes: 0')"""
import os, re, html, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
pages = sorted(f for f in os.listdir(OUT) if f.endswith('.html'))
ok = True
for f in pages:
    s = open(os.path.join(OUT, f), encoding='utf-8').read()
    for h in set(re.findall(r'href="(/[^"#?]*)', s)):
        p = h.strip('/') or 'index'
        if p == 'site.webmanifest': continue
        target = os.path.join(OUT, p + ('' if '.' in p.split('/')[-1] else '.html'))
        if not os.path.exists(target): print('BROKEN LINK', f, h); ok = False
    for h in set(re.findall(r'(?:src|href|data-mobile|data-desktop|poster)="(/Assets/[^"]+)"', s)):
        if not os.path.exists(os.path.join(OUT, h.strip('/'))): print('MISSING ASSET', f, h); ok = False
    for chunk in re.findall(r'srcset="([^"]+)"', s):
        for part in chunk.split(','):
            u = part.strip().split(' ')[0]
            if u.startswith('/Assets') and not os.path.exists(os.path.join(OUT, u.strip('/'))): print('MISSING SRCSET', f, u); ok = False
    m = re.search(r'<main id="main" tabindex="-1">(.*?)</main>', s, re.S)
    words = len(html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1))).split()) if m else 0
    title = re.search(r'<title>(.*?)</title>', s).group(1)
    print(f'{f:22} {words:5d} words  | {title}')
dashes = sum(open(os.path.join(OUT, f), encoding='utf-8').read().count('—') + open(os.path.join(OUT, f), encoding='utf-8').read().count('–') for f in pages)
for f in ('sitemap.xml', 'robots.txt', 'site.webmanifest', 'vercel.json'):
    if not os.path.exists(os.path.join(OUT, f)): print('MISSING', f); ok = False
print('links ok' if ok else 'LINK PROBLEMS')
print('dashes:', dashes)
sys.exit(0 if ok and dashes == 0 else 1)

#!/usr/bin/env python3
"""Prove a deployed copy matches this package byte for byte.
python3 verify_live.py https://campcookstown-site.vercel.app
Fetches every page and asset listed in MANIFEST.sha256 under out/ from that host and compares digests."""
import sys, os, hashlib, urllib.request

if len(sys.argv) < 2: print(__doc__); sys.exit(2)
base = sys.argv[1].rstrip('/')
here = os.path.dirname(os.path.abspath(__file__))
rows = [l.split('  ', 1) for l in open(os.path.join(here, 'MANIFEST.sha256')).read().splitlines() if '  out/' in l]
ok = bad = 0
for digest, path in rows:
    rel = path[len('out/'):]
    if rel.endswith('.html'):
        url = base + ('/' if rel == 'index.html' else '/' + rel[:-5])   # clean URLs
    else:
        url = base + '/' + rel
    req = urllib.request.Request(url, headers={'Accept-Encoding': 'identity', 'User-Agent': 'camp-verify'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: data = r.read()
    except Exception as e:
        print('FETCH FAILED', url, e); bad += 1; continue
    h = hashlib.sha256(data).hexdigest()
    if h == digest: ok += 1
    else: print('DIFFERS', url); bad += 1
print(f'{ok} files identical, {bad} problems')
sys.exit(0 if bad == 0 else 1)

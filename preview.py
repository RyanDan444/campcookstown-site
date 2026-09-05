#!/usr/bin/env python3
"""One file previews of a built page with every asset inlined, for a private review link.
python3 preview.py index phone  -> preview/index-phone.html  (mobile video, mobile film, photos <= 900 px)
python3 preview.py index desk   -> preview/index-desk.html   (desktop video, desktop film, photos <= 1200 px)
The hero videos come from light encodes in preview/_tmp (720x1280 crf 33 for phones, 640x1138 crf 34 for desk),
so that a one file preview stays under the 16 MB artifact limit.
"""
import os, re, sys, base64, json

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out'); PV = os.path.join(HERE, 'preview'); os.makedirs(PV, exist_ok=True)
MIME = {'.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.mp4': 'video/mp4', '.woff': 'font/woff', '.avif': 'image/avif'}


def uri(path):
    ext = os.path.splitext(path)[1]
    return f'data:{MIME[ext]};base64,' + base64.b64encode(open(os.path.join(OUT, path.lstrip('/')), 'rb').read()).decode()


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else 'index'
    mode = sys.argv[2] if len(sys.argv) > 2 else 'phone'
    cap = 900 if mode == 'phone' else 1200
    html = open(os.path.join(OUT, slug + '.html')).read()
    # pictures -> one webp img at the capped width
    def pic(m):
        block = m.group(0)
        img = re.search(r'<img [^>]*>', block).group(0)
        srcset = re.search(r'<img [^>]*srcset="([^"]+)"', block).group(1)
        cands = [c.strip().split(' ') for c in srcset.split(',')]
        sizes = re.search(r' sizes="([^"]*)"', img)
        local_cap = 900 if (sizes and ('20vw' in sizes.group(1) or '25vw' in sizes.group(1))) else cap
        best = None
        for u, w in cands:
            w = int(w[:-1])
            if w <= local_cap or best is None:
                best = u
        img = re.sub(r' srcset="[^"]*"', '', img); img = re.sub(r' sizes="[^"]*"', '', img)
        img = re.sub(r'src="[^"]*"', 'src="' + uri(best) + '"', img, count=1)
        return img
    html = re.sub(r'<picture>.*?</picture>', pic, html, flags=re.S)
    # hero video: keep one source
    lite = os.path.join(PV, '_tmp', 'hero-mobile.mp4' if mode == 'phone' else 'hero-desktop.mp4')
    v = uri(os.path.relpath(lite, OUT))
    # one copy of the video serves both the phone and the desktop attribute
    html = re.sub(r' data-desktop="[^"]+"', '', html); html = re.sub(r'data-mobile="[^"]+"', f'data-mobile="{v}"', html)
    html = html.replace("var src=v.getAttribute(mobile?'data-mobile':'data-desktop');", "var src=v.getAttribute('data-mobile')||v.getAttribute('data-desktop');")
    # the font preloads would duplicate the inlined fonts
    html = re.sub(r'<link rel="preload" href="[^"]*" as="font"[^>]*>', '', html)
    for path in set(re.findall(r'"(/Assets/video/hero-poster[^"]+)"', html)):
        html = html.replace(f'"{path}"', f'"{uri(path)}"')
    for path in set(re.findall(r'srcset="(/Assets/video/hero-poster[^"]+)"', html)):
        html = html.replace(f'srcset="{path}"', f'srcset="{uri(path)}"')
    # the film: phones get the day loop inlined; wide screens get every other frame inlined
    m = re.search(r'data-base="([^"]+)"', html); base = m.group(1) if m else '/Assets/film'
    fdir = os.path.join(OUT, base.lstrip('/'), 'd')
    allf = sorted(os.listdir(fdir)) if os.path.isdir(fdir) else []
    frames = []
    if mode != 'phone':
        keep = allf[::3] + ([allf[-1]] if allf and (len(allf) - 1) % 3 else [])
        frames = [uri(f'{base}/d/{f}') for f in keep]
        html = html.replace('data-frames="%d"' % len(allf), 'data-frames="%d"' % len(frames))
        html = html.replace('<script>', '<script>window.FILM_FRAMES=' + json.dumps(frames) + ';</script><script>', 1)
        html = html.replace("function url(i){return base+'/d/'+String(i+1).padStart(3,'0')+'.webp'}", "function url(i){return (w.FILM_FRAMES&&w.FILM_FRAMES[i])||(base+'/d/'+String(i+1).padStart(3,'0')+'.webp')}")
    for path in set(re.findall(r'"(/Assets/(?:video|film[^"/]*)/[^"]+)"', html)):
        if os.path.exists(os.path.join(OUT, path.lstrip('/'))) and 'hero-' not in path and not (mode != 'phone' and 'day-' in path) and not (mode == 'phone' and 'pane-' in path):
            html = html.replace(f'"{path}"', f'"{uri(path)}"')
    # fonts, brand images, remaining asset urls
    for path in set(re.findall(r'(/Assets/(?:fonts|brand)/[\w.-]+)', html)):
        if os.path.exists(os.path.join(OUT, path.lstrip('/'))):
            html = html.replace(f'url({path})', f'url({uri(path)})').replace(f'"{path}"', f'"{uri(path)}"')
    html = re.sub(r'srcset="[^"]*\.png[^"]*"', '', html)
    # internal links stay as is (they will not resolve in a preview); booking links are real
    banner = '<div style="position:fixed;left:0;right:0;bottom:0;z-index:99;background:#C8973F;color:#0F1A14;font:600 12px/1.3 Inter,system-ui,sans-serif;text-align:center;padding:6px 10px;letter-spacing:.06em;text-transform:uppercase">Private preview · home page only · links to other pages do not work here</div>'
    html = html.replace('</body>', banner + '</body>')
    outp = os.path.join(PV, f'{slug}-{mode}.html')
    open(outp, 'w').write(html)
    print(outp, round(os.path.getsize(outp) / 1e6, 1), 'MB', len(frames), 'frames inlined')
    # the same page as an artifact body: the head's title, styles and scripts, then the body, no document tags
    head = re.search(r'<head>(.*?)</head>', html, re.S).group(1)
    body = re.search(r'<body[^>]*>(.*)</body>', html, re.S).group(1)
    keep = ''.join(re.findall(r'<title>.*?</title>|<style>.*?</style>|<script[^>]*>.*?</script>', head, re.S))
    bodycls = re.search(r'<body([^>]*)>', html).group(1)
    art = keep + (f'<div{bodycls}>' + body + '</div>' if 'class=' in bodycls else body)
    artp = os.path.join(PV, f'artifact-{mode}.html')
    open(artp, 'w').write(art)
    print(artp, round(os.path.getsize(artp) / 1e6, 1), 'MB')


if __name__ == '__main__':
    main()

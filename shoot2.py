#!/usr/bin/env python3
"""Walk a page screen by screen, the way a person scrolls, and stitch the screens into one strip.
python3 shoot2.py <slug> [desk|phone] [step]   ->  shots/<slug>-<mode>-walk.jpg
Sticky heroes and the scroll film render exactly as a visitor sees them, unlike a full page capture."""
import sys, os, threading, time, http.server, socketserver, functools
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out'); SHOTS = os.path.join(HERE, 'shots'); os.makedirs(SHOTS, exist_ok=True)
PORT = 8766

class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        p = self.path.split('?')[0]
        if p != '/' and '.' not in p.split('/')[-1] and os.path.exists(os.path.join(OUT, p.strip('/') + '.html')):
            self.path = p.rstrip('/') + '.html'
        return super().do_GET()

def serve():
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('127.0.0.1', PORT), functools.partial(H, directory=OUT))
    threading.Thread(target=httpd.serve_forever, daemon=True).start(); return httpd

def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else 'index'
    mode = sys.argv[2] if len(sys.argv) > 2 else 'phone'
    step = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    httpd = serve(); time.sleep(0.3)
    vw, vh, dpr, mob = (390, 844, 2, True) if mode == 'phone' else (1440, 900, 1, False)
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=dpr, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); pg.goto(f'http://127.0.0.1:{PORT}/' + ('' if slug == 'index' else slug), wait_until='networkidle')
        pg.wait_for_timeout(600)
        frames = []
        y = 0
        total = pg.evaluate('document.documentElement.scrollHeight')
        while y < total:
            pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(900)
            frames.append(pg.screenshot())
            y += int(vh * step)
            total = pg.evaluate('document.documentElement.scrollHeight')
            if len(frames) > 60: break
        b.close()
    ims = [Image.open(__import__('io').BytesIO(f)) for f in frames]
    W = ims[0].width; Hh = sum(i.height for i in ims) + 6 * (len(ims) - 1)
    strip = Image.new('RGB', (W, Hh), (255, 0, 0)); yy = 0
    for im in ims:
        strip.paste(im, (0, yy)); yy += im.height + 6
    scale = 1.0 if mode == 'phone' else 0.6
    strip = strip.resize((int(W * scale), int(Hh * scale)), Image.LANCZOS)
    out = os.path.join(SHOTS, f'{slug}-{mode}-walk.jpg'); strip.save(out, quality=82)
    print(out, len(ims), 'screens', strip.size)
    httpd.shutdown()

if __name__ == '__main__':
    main()

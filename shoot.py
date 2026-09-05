#!/usr/bin/env python3
"""Screenshot every page at desktop and phone widths. python3 shoot.py [slug ...] [--full]"""
import sys, os, threading, http.server, socketserver, functools, time
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE if os.path.isdir(os.path.join(HERE, 'out')) else os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'out'); SHOTS = os.path.join(ROOT, 'shots'); os.makedirs(SHOTS, exist_ok=True)
PORT = 8765

class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        # clean urls: /day-camp -> /day-camp.html
        p = self.path.split('?')[0]
        if p != '/' and '.' not in p.split('/')[-1] and os.path.exists(os.path.join(OUT, p.strip('/') + '.html')):
            self.path = p.rstrip('/') + '.html'
        return super().do_GET()

def serve():
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('127.0.0.1', PORT), functools.partial(H, directory=OUT))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    full = '--full' in sys.argv
    slugs = args or ['index', 'day-camp', 'overnight-camp', 'rates', 'our-story', 'camp-life', 'faq', 'reviews', 'contact', 'spa', '404']
    httpd = serve(); time.sleep(0.3)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for slug in slugs:
            url = f'http://127.0.0.1:{PORT}/' + ('' if slug == 'index' else slug)
            for name, vw, vh, dpr, mobile in (('desk', 1440, 900, 1, False), ('phone', 390, 844, 2, True)):
                ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile)
                pg = ctx.new_page(); pg.goto(url, wait_until='networkidle')
                pg.evaluate("document.querySelectorAll('.r').forEach(e=>e.classList.add('in'))")
                if full:
                    h = pg.evaluate('document.body.scrollHeight')
                    for y in range(0, h, vh // 2):
                        pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(120)
                    pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
                    pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(500)
                    pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(300)
                else:
                    pg.wait_for_timeout(400)
                if full: pg.evaluate("document.getElementById('top').style.display='none';var m=document.getElementById('mcta');if(m)m.style.display='none'")
                pg.screenshot(path=os.path.join(SHOTS, f'{slug}-{name}.png'), full_page=full)
                if full:
                    pg.evaluate("document.getElementById('top').style.display='';var m=document.getElementById('mcta');if(m)m.style.display=''")
                    # also the top of the page, exactly as it opens
                    pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(200)
                    pg.screenshot(path=os.path.join(SHOTS, f'{slug}-{name}-top.png'), full_page=False)
                ctx.close()
            print('shot', slug)
        b.close()
    httpd.shutdown()

if __name__ == '__main__':
    main()

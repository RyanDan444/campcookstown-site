#!/usr/bin/env python3
"""Desktop hero screenshots at several sizes, plus a scrolled state.
python3 shot_hero.py [slug]  -> shots/h-<w>x<h>.png, shots/h-1440-scroll.png"""
import sys, os, time
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shoot2 import serve, PORT, SHOTS

def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else 'index'
    httpd = serve(); time.sleep(0.3)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for (vw, vh) in [(1440, 900), (1920, 1080), (1366, 768), (1280, 720), (2560, 1440), (1100, 760)]:
            ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=1)
            pg = ctx.new_page(); pg.goto(f'http://127.0.0.1:{PORT}/' + ('' if slug == 'index' else slug), wait_until='networkidle')
            pg.wait_for_timeout(2600)
            pg.mouse.move(vw * 0.7, vh * 0.4); pg.wait_for_timeout(700)
            pg.screenshot(path=os.path.join(SHOTS, f'h-{vw}x{vh}.png'))
            if vw == 1440:
                for y in (300, 620, 900):
                    pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(700)
                    pg.screenshot(path=os.path.join(SHOTS, f'h-1440-scroll{y}.png'))
            ctx.close()
        b.close()
    httpd.shutdown(); print('done')

if __name__ == '__main__':
    main()

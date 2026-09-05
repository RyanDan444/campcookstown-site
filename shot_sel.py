#!/usr/bin/env python3
"""Screenshot one element of a built page.
python3 shot_sel.py <slug> <css selector> [phone|desk] [name]  ->  shots/<name>.png"""
import sys, os, time
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shoot2 import serve, PORT, SHOTS


def main():
    slug, sel = sys.argv[1], sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'phone'
    name = sys.argv[4] if len(sys.argv) > 4 else f'{slug}-{mode}-sel'
    httpd = serve(); time.sleep(0.3)
    vw, vh, dpr, mob = (390, 844, 2, True) if mode == 'phone' else (1440, 900, 1, False)
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=dpr, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); pg.goto(f'http://127.0.0.1:{PORT}/' + ('' if slug == 'index' else slug), wait_until='networkidle')
        el = pg.locator(sel).first
        el.scroll_into_view_if_needed(); pg.wait_for_timeout(1400)
        # let every reveal inside finish
        pg.evaluate("sel => {document.querySelectorAll(sel + ' .r, ' + sel + '.r').forEach(e => e.classList.add('in'))}", sel)
        pg.wait_for_timeout(500)
        out = os.path.join(SHOTS, name + '.png'); el.screenshot(path=out)
        b.close()
    print(out)
    httpd.shutdown()


if __name__ == '__main__':
    main()

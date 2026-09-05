#!/usr/bin/env python3
"""Camp Cookstown site generator. python3 build.py  ->  writes out/.

Every word lives in content.py. This file only renders. Real photos, real reviews, real prices
(live from pricing.json with inline fallbacks). No dashes anywhere a customer reads; the build refuses
to write a page that contains one.
"""
import os, sys, json, shutil, html, datetime, hashlib
from content import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
SRC = os.path.join(HERE, 'src')
PHOTO_SRC = os.path.join(SRC, 'photos')      # graded exports + manifest.json
VIDEO_SRC = os.path.join(SRC, 'video')       # hero-desktop.mp4, hero-mobile.mp4, posters, film/
STAMP = datetime.date.today().isoformat()
PAGES = {}
ASSETS = {}   # logical path -> hashed path, filled by assets()
MANIFEST = json.load(open(os.path.join(PHOTO_SRC, 'manifest.json')))


def A(path):
    """Hashed URL for a logical /Assets/... path (folders pass through)."""
    return ASSETS.get(path, path)


def _hashed_copy(src, logical):
    h = hashlib.sha1(open(src, 'rb').read()).hexdigest()[:8]
    stem, ext = os.path.splitext(logical)
    hashed = f'{stem}.{h}{ext}'
    dst = os.path.join(OUT, hashed.lstrip('/'))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(src, dst)
    ASSETS[logical] = hashed
    return hashed
FILM_FRAMES = len([f for f in os.listdir(os.path.join(VIDEO_SRC, 'film', 'd')) if f.endswith('.webp')]) if os.path.isdir(os.path.join(VIDEO_SRC, 'film', 'd')) else 0
NAV = [('/day-camp', 'Day Camp'), ('/overnight-camp', 'Overnight Camp'), ('/rates', 'Rates'), ('/camp-life', 'Camp Life'), ('/our-story', 'Our Story')]
ICON = {
 'phone': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.9 2z"/></svg>',
 'menu': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
 'arrow': '<svg class="arr" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'sun': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
 'group': '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><circle cx="17" cy="10" r="2.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M14 20a4.5 4.5 0 0 1 7.5-3.4"/></svg>',
 'heart': '<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-9.5-9.3C1.2 8.6 3.3 5 6.8 5c2 0 3.3 1 4.2 2.3C11.9 6 13.2 5 15.2 5c3.5 0 5.6 3.6 4.3 6.7C19.5 16.4 12 21 12 21z"/></svg>',
 'barn': '<svg viewBox="0 0 24 24"><path d="M3 21V10l9-6 9 6v11M3 21h18M9 21v-6h6v6"/></svg>',
 'bowl': '<svg viewBox="0 0 24 24"><path d="M3 12h18a9 9 0 0 1-18 0zM8 8c0-2 1.5-3 3-3s3 1 3 3M14 8c0-1.5 1-2 2-2"/></svg>',
 'moon': '<svg viewBox="0 0 24 24"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg>',
 'paw': '<svg viewBox="0 0 24 24"><circle cx="7" cy="8" r="2"/><circle cx="12" cy="5.5" r="2"/><circle cx="17" cy="8" r="2"/><path d="M12 10c-3 0-6 3-6 6 0 2 1.5 3 3 3 1 0 2-.5 3-.5s2 .5 3 .5c1.5 0 3-1 3-3 0-3-3-6-6-6z"/></svg>',
 'shield': '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8.5-8 9.5C7.5 20.5 4 17 4 12V6l8-3z"/><path d="M9 12l2 2 4-4"/></svg>',
 'clock': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
}
SOCIAL_ICON = {
 'Instagram': '<svg viewBox="0 0 24 24"><path d="M7.5 2h9A5.5 5.5 0 0 1 22 7.5v9a5.5 5.5 0 0 1-5.5 5.5h-9A5.5 5.5 0 0 1 2 16.5v-9A5.5 5.5 0 0 1 7.5 2zm0 2A3.5 3.5 0 0 0 4 7.5v9A3.5 3.5 0 0 0 7.5 20h9a3.5 3.5 0 0 0 3.5-3.5v-9A3.5 3.5 0 0 0 16.5 4h-9zM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm5.3-3.3a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4z"/></svg>',
 'TikTok': '<svg viewBox="0 0 24 24"><path d="M16.5 3c.4 2.4 1.9 4 4.5 4.2v3.3c-1.7 0-3.2-.5-4.5-1.4v6.4a6 6 0 1 1-6-6c.3 0 .7 0 1 .1v3.4a2.7 2.7 0 1 0 1.7 2.5V3h3.3z"/></svg>',
 'Facebook': '<svg viewBox="0 0 24 24"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.3H7.4V14h2.8v8h3.3z"/></svg>',
 'YouTube': '<svg viewBox="0 0 24 24"><path d="M22.5 7.2a2.8 2.8 0 0 0-2-2C18.8 4.8 12 4.8 12 4.8s-6.8 0-8.5.4a2.8 2.8 0 0 0-2 2C1 8.9 1 12 1 12s0 3.1.5 4.8a2.8 2.8 0 0 0 2 2c1.7.4 8.5.4 8.5.4s6.8 0 8.5-.4a2.8 2.8 0 0 0 2-2c.5-1.7.5-4.8.5-4.8s0-3.1-.5-4.8zM9.8 15.1V8.9l5.7 3.1-5.7 3.1z"/></svg>',
}


def esc(s):
    return html.escape(s, quote=True)


def book(pos, lp='home'):
    return f'{START}?src=site&cmp={lp}-{pos}'


def pic(slug, sizes='100vw', cls='', eager=False, alt=None, focus=None, w_cap=None):
    m = MANIFEST[slug]
    widths = [w for w in m['widths'] if w <= m['w'] and (not w_cap or w <= w_cap)] or [min(m['widths'])]
    if alt is None:
        alt = PHOTOS.get(slug, '')
    src = A(f'/Assets/photos/{slug}-w{widths[-1]}.webp')
    def ss(ext):
        return ', '.join(f'{A(f"/Assets/photos/{slug}-w{w}.{ext}")} {w}w' for w in widths)
    h = round(widths[-1] * m['h_over_w'])
    style = f' style="object-position:{focus}"' if focus else ''
    load = 'eager" fetchpriority="high' if eager else 'lazy'
    return (f'<picture><source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<img src="{src}" srcset="{ss("webp")}" sizes="{sizes}" width="{widths[-1]}" height="{h}" alt="{esc(alt)}" loading="{load}" decoding="async" class="{cls}"{style}></picture>')


def btn(text, href, kind='primary', arrow=True, cls=''):
    return f'<a class="btn btn-{kind}{(" " + cls) if cls else ""}" href="{href}">{text}{ICON["arrow"] if arrow else ""}</a>'


# ---------------------------------------------------------------- chrome
def header(active, lp, lean=False):
    CUR = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{CUR if h == active else ""}>{t}</a>' for h, t in NAV)
    logo = f'<img src="{A("/Assets/brand/logo-240.png")}" srcset="{A("/Assets/brand/logo-240.png")} 1x, {A("/Assets/brand/logo-480.png")} 2x" width="120" height="79" alt="Camp Cookstown">'
    if lean:
        return f"""<a class="skip" href="#main">Skip to content</a>
<header id="top"><div class="bar"><a class="logo" href="/" aria-label="Camp Cookstown home">{logo}</a>
  <div class="right"><a class="call" href="{TEL}" aria-label="Call {PHONE}">{ICON['phone']}</a>{btn(CTA_SHORT, book('nav', lp), 'primary', False, 'book')}</div></div></header>"""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header id="top"><div class="bar">
  <a class="logo" href="/" aria-label="Camp Cookstown home">{logo}</a>
  <nav aria-label="Main">{links}</nav>
  <div class="right"><a class="signin" href="{SIGNIN}">Family sign in</a><a class="call" href="{TEL}" aria-label="Call {PHONE}">{ICON['phone']}</a>{btn(CTA, book('nav', lp), 'primary', False, 'book')}<button class="menu" type="button" data-menu aria-label="Menu" aria-controls="drawer" aria-expanded="false">{ICON['menu']}</button></div>
</div></header>
<div id="drawer" aria-hidden="true"><div class="head">{logo}<button class="x" type="button" data-menu aria-label="Close menu">&times;</button></div>
  <div class="links">{links}</div>
  <div class="foot">{btn(CTA, book('menu', lp))}<div class="quiet"><a href="{TEL}">Call</a><span>·</span><a href="{SMS}">Text</a><span>·</span><a href="{SIGNIN}">Family sign in</a></div></div></div>"""


def mcta(lp):
    return f'<div id="mcta">{btn(CTA, book("mcta", lp))}<a class="call" href="{TEL}" aria-label="Call {PHONE}">{ICON["phone"]}</a></div>'


def footer(lean=False):
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{SOCIAL_ICON[n]}</a>' for n, u in SOCIAL)
    if lean:
        return f"""<footer class="lean"><div class="wrap"><div class="lean-row"><img src="{A('/Assets/brand/logo-240.png')}" alt="Camp Cookstown"><span>{ADDRESS}</span><a href="{TEL}"><b>{PHONE}</b></a><span>Open every day. Drop off 7:30 to 8:30 am or 11 to noon, pick up 11 to noon or 5 to 6 pm.</span></div>
  <div class="bottom"><span>&copy; {datetime.date.today().year} Camp Cookstown Inc.</span><span><a href="/">campcookstown.com</a> · <a href="/privacy-policy">Privacy</a></span></div></div></footer>"""
    towns = ' '.join(f'<a href="/{s}">{t}</a>' for s, t in TOWN_LINKS)
    return f"""<footer><div class="wrap"><div class="cols">
  <div class="blurb"><img src="{A('/Assets/brand/logo-240.png')}" alt="Camp Cookstown" width="120" height="79"><p>Cage free dog day camp and overnight camp on 45 acres in Essa, Ontario. Minutes from Cookstown and Highway 400, serving Barrie, Innisfil, Alliston, Bradford, Newmarket and Tottenham since 2008.</p><div class="social">{soc}</div></div>
  <div><h4>Camp</h4><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul></div>
  <div><h4>Good to know</h4><ul><li><a href="/faq">Questions</a></li><li><a href="/reviews">Reviews</a></li><li><a href="/spa">The Spa Treatment</a></li><li><a href="/contact">Contact and directions</a></li><li><a href="{SIGNIN}">Family sign in</a></li></ul></div>
  <div class="findus"><h4>Find us</h4><ul><li><b>{ADDRESS.replace(', Essa', '<br>Essa')}</b></li><li><a href="{TEL}"><b>{PHONE}</b></a> · <a href="{SMS}">text us</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Open every day of the year</li><li>Drop off 7:30 to 8:30 am or 11 to noon<br>Pick up 11 to noon or 5 to 6 pm</li></ul></div>
</div><div class="towns"><b style="color:#fff">Families drive from</b> {towns}</div><div class="bottom"><span>&copy; {datetime.date.today().year} Camp Cookstown Inc.</span><span><a href="/privacy-policy">Privacy</a></span></div></div></footer>"""


TOWN_LINKS = [('dog-boarding-barrie', 'Barrie'), ('dog-boarding-innisfil', 'Innisfil'), ('dog-boarding-alliston', 'Alliston'), ('dog-boarding-bradford', 'Bradford'), ('dog-boarding-newmarket', 'Newmarket'),
              ('dog-boarding-aurora', 'Aurora'), ('dog-boarding-king-city', 'King City'), ('dog-boarding-east-gwillimbury', 'East Gwillimbury'), ('dog-boarding-vaughan', 'Vaughan'), ('dog-boarding-caledon', 'Caledon'), ('dog-boarding-borden', 'Borden and Angus')]


# ---------------------------------------------------------------- blocks
def hero(eyebrow, h1, lede, lp, video=False, photo=None, focus='center', short=False, price=None, sub=CTA_SUB, pos='hero', start=0, lede_m=None):
    if video:
        media = (f'<img class="bgblur" src="{A("/Assets/video/hero-poster.webp")}" alt="" aria-hidden="true" decoding="async">'
                 f'<canvas class="hbg" width="96" height="170" aria-hidden="true"></canvas>'
                 f'<video class="hv" muted loop playsinline preload="metadata" aria-hidden="true" data-start="{start}" data-desktop="{A("/Assets/video/hero-desktop.mp4")}" data-mobile="{A("/Assets/video/hero-mobile.mp4")}"></video>'
                 f'<picture class="poster"><source media="(max-width: 900px), (max-height: 500px)" type="image/webp" srcset="{A("/Assets/video/hero-poster-mobile.webp")}"><source media="(max-width: 900px), (max-height: 500px)" srcset="{A("/Assets/video/hero-poster-mobile.jpg")}"><source type="image/webp" srcset="{A("/Assets/video/hero-poster.webp")}"><img src="{A("/Assets/video/hero-poster.jpg")}" alt="" fetchpriority="high" decoding="async"></picture>')
    else:
        media = pic(photo, '100vw', '', True, focus=focus, w_cap=1600)
    pr = f'<p class="price">{price[0]}<small>{price[1]}</small></p>' if price else ''
    subl = f'<p class="sub">{sub} <b class="callline">Or call <a href="{TEL}">{PHONE}</a>.</b></p>' if sub else ''
    ledes = f'<p class="lede d">{lede}</p><p class="lede m">{lede_m}</p>' if lede_m else f'<p class="lede">{lede}</p>'
    inner = f"""<div class="inner"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1>{ledes}{pr}
      <div class="act">{btn(CTA, book(pos, lp))}</div>{subl}</div>"""
    cue = '<div class="cue"><span>Scroll</span><i></i></div>' if not short else ''
    pause = '<button type="button" class="pausebtn" hidden aria-pressed="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg><span>Pause</span></button>' if video else ''
    if short:
        return f'<section class="hero short"><div class="media">{media}</div><div class="shade"></div>{inner}</section>'
    return f'<div class="hero-wrap"><section class="hero{" tall" if video else ""}"><div class="media">{media}</div><div class="shade"></div>{inner}{cue}{pause}</section></div>'


def proof():
    sp = '<span class="stars sp" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
    return f"""<div class="proof"><div class="wrap row">
  <div class="cell"><b><span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>{RATING} on Google</b><span>{REVIEW_COUNT} reviews</span></div>
  <div class="cell"><b>{sp}45 acres</b><span>Fenced farmland</span></div>
  <div class="cell"><b>{sp}Cage free</b><span>A heated barn and a real pack</span></div>
  <div class="cell"><b>{sp}Since 2008</b><span>Owner run, open every day</span></div>
</div></div>"""


def doors(lp='home'):
    return f"""<section><div class="wrap" data-stagger><div class="split"><div><p class="eyebrow r">Two ways to camp</p><h2 class="r">Come for the day, or stay the night.</h2></div>
  <p class="lede r">All play, all supervised, and outside whenever the weather says yes.</p></div>
  <div class="doors">
    <a class="door r" href="/day-camp">{pic('senior-golden-grass', '(max-width: 760px) 100vw, 50vw', '', False, focus='center 40%')}<div class="txt"><h3>Day Camp</h3><p>Drop off in the morning. Pick up a tired, happy dog.</p><span class="from"><span><span class="pv" data-item-price="day.week">${RATES['day.week']}</span> a day</span><span class="arr">{ICON['arrow']}</span></span></div></a>
    <a class="door r" href="/overnight-camp">{pic('dachshund-nap', '(max-width: 760px) 100vw, 50vw', '', False, focus='center 45%')}<div class="txt"><h3>Overnight Camp</h3><p>Days in the field, nights in the heated barn with the pack.</p><span class="from"><span>From <span class="pv" data-item-price="overnight.week">${RATES['overnight.week']}</span> a night</span><span class="arr">{ICON['arrow']}</span></span></div></a>
  </div>
  <div class="perk r"><b>The Spa Treatment</b><span>A wash, dry, ears and nails before pick up. A little extra for campers only.</span><a href="/spa">About the spa</a></div></div></section>"""


def film(title='What your dog actually does all day.', eyebrow='A day at camp'):
    caps = ''.join(f'<div class="c" data-a="{a}" data-b="{b}"><small>{s}</small><b>{t}</b></div>' for a, b, s, t in FILM_CAPTIONS)
    return f"""<section class="film" data-frames="{FILM_FRAMES}" data-base="{A('/Assets/film')}" aria-label="Real footage from a day at camp"><div class="stage">
  <img class="still" src="{A('/Assets/film/d/001.webp')}" alt="" aria-hidden="true" loading="lazy" decoding="async">
  <video class="loop" muted loop playsinline preload="none" aria-hidden="true" data-src="{A('/Assets/video/day-mobile.mp4')}" poster="{A('/Assets/video/day-poster-mobile.jpg')}"></video>
  <canvas aria-hidden="true"></canvas><div class="shade"></div>
  <div class="head"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div><p class="clock" aria-live="off"></p>
  <div class="cap">{caps}</div><div class="bar"><i></i></div></div></section>"""


def day_strip(title='Here is the day, start to finish.'):
    figs = ''.join(f'<figure data-slot="{s}" class="r"><span class="now"><i></i>Right now</span>{pic(p, "(max-width: 760px) 50vw, 20vw", "", False)}<figcaption><small>{t}</small><b>{h}</b><span>{dsc}</span></figcaption></figure>' for s, t, h, dsc, p in DAY)
    return f'<section class="day tight"><div class="wrap" data-stagger><p class="eyebrow r">The schedule</p><h2 class="r">{title}</h2><div class="grid">{figs}</div></div></section>'


def reviews(idx=(0, 1, 2, 3), title='What the humans say.', four=True, lp='home'):
    cards = ''.join(f'<article class="review r"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><q>{esc(REVIEWS[i][1])}</q><div class="who"><b>{esc(REVIEWS[i][0])}</b><span>Google review</span></div></article>' for i in idx)
    return f"""<section class="dark"><div class="wrap" data-stagger><p class="eyebrow r">{RATING} on Google · {REVIEW_COUNT} reviews</p><h2 class="r">{title}</h2>
  <div class="reviews-grid{' four' if four else ''}">{cards}</div>
  <div class="more r"><a class="link" href="/reviews">More reviews</a><a class="link" href="{MAPS}" target="_blank" rel="noopener">All {REVIEW_COUNT} on Google</a></div></div></section>"""


def rate_tiles(lp='home'):
    tiles = [
        ('Day Camp', f'<span class="pv" data-item-price="day.week">${RATES["day.week"]}</span>', 'a day', 'One full day outside with the pack. Drop off in the morning, pick up a tired, happy dog.',
         [f'Ten day pack <span class="pv" data-item-price="day.pack">${RATES["day.pack"]}</span>, that is <span class="pv" data-item-price="day.perday">$40</span> a day', 'Use the pack whenever you like', 'First day free for new campers']),
        ('Overnight Camp', f'<small>from</small><span class="pv" data-item-price="overnight.week">${RATES["overnight.week"]}</span>', 'a night', f'Days in the field, nights in the heated barn with the pack. Weekends are <span class="pv" data-item-price="overnight.weekend">${RATES["overnight.weekend"]}</span> a night.',
         [f'Eight nights or more, <span class="pv" data-item-price="overnight.t3">${RATES["overnight.t3"]}</span> a night', f'Fifteen nights or more, <span class="pv" data-item-price="overnight.t4">${RATES["overnight.t4"]}</span> a night', f'Twenty eight nights or more, <span class="pv" data-item-price="overnight.t5">${RATES["overnight.t5"]}</span> a night']),
    ]
    cards = ''.join(f'<article class="card r"><div class="name"><h3>{n}</h3><div class="amt">{p}<em style="font-family:var(--sans)">{per}</em></div></div><p class="spec">{sp}</p><ul>{"".join(f"<li>{x}</li>" for x in lis)}</ul><div class="act">{btn(CTA, book("rates", lp))}</div></article>' for n, p, per, sp, lis in tiles)
    return f"""<section class="mist"><div class="wrap" data-stagger><div class="split"><div><p class="eyebrow r">Prices, on the page</p><h2 class="r">Real prices, right here.</h2></div>
  <p class="lede r">Ten percent off each extra dog from the same home. Cancel any time, free. All prices plus HST.</p></div>
  <div class="cards two">{cards}</div>
  <p class="fine r">Holidays and long weekends are <span class="pv" data-item-price="overnight.holiday">${RATES["overnight.holiday"]}</span> a night. Those dates fill up early, so half is paid at booking and that deposit is the one thing we cannot refund. <a href="/rates" style="font-weight:600;text-decoration:underline;text-underline-offset:3px">Every rate, in one place</a>.</p></div></section>"""


def steps(lp='home', h='Three free steps, then your dog decides.'):
    items = [
        ('Book a free meet and greet', 'Two minutes online. Pick a day that suits you. No card needed.'),
        ('Come say hi', 'About twenty minutes. Walk the property, meet the team, and your dog meets a few new friends.'),
        ('First day or night on us', 'A free trial visit, so your dog can decide. Then book whenever you like.'),
    ]
    st = ''.join(f'<div class="step r"><span class="n">{i + 1}</span><h3>{t}</h3><p>{p}</p><span class="free">Free</span></div>' for i, (t, p) in enumerate(items))
    return f"""<section><div class="wrap" data-stagger><div class="split"><div><p class="eyebrow r">How it works</p><h2 class="r">{h}</h2></div><p class="lede r">Nothing to pay and nothing to sign up for until you have seen the place and your dog has had a day here.</p></div>
  <div class="steps">{st}</div><div class="btns r" style="margin-top:var(--s5)">{btn(CTA, book('steps', lp))}</div></div></section>"""


def team_block(eyebrow='Who is taking care of your dog?', h='Taylor and Hannah, every single day.', lede='They are the ones at the barn door at drop off, on the field all day, and on the phone when you want to check in.'):
    return f"""<section class="tight"><div class="wrap" data-stagger><div class="split"><div><p class="eyebrow r">{eyebrow}</p><h2 class="r">{h}</h2></div><p class="lede r">{lede}</p></div>
  <div class="team">
    <figure class="r">{pic('counselor-aussie', '(max-width: 860px) 50vw, 33vw', '', False, focus='center 30%')}<figcaption><b>Taylor</b><span>Camp manager</span></figcaption></figure>
    <figure class="r">{pic('hannah', '(max-width: 860px) 50vw, 33vw', '', False, focus='center 35%')}<figcaption><b>Hannah</b><span>Camp manager</span></figcaption></figure>
    <div class="r"><p class="eyebrow">The faces your dog will know</p><h3>They know every dog by name.</h3><p>They match the groups, they serve the dinners one at a time, and they are the ones who text you a photo when you are missing your pup. Your dog will love them in about a minute.</p></div>
  </div></div></section>"""


def story_short():
    return team_block() + band('barn-lane-pano', 'Built by two brothers, for their own dogs first.', 'Ryan and Dan wanted a place they would trust with their own dogs, so they built one. Camp Cookstown opened in 2008 on 45 acres of Essa farmland, and the same two brothers still run it.', focus='28% 62%', button=btn('Meet Ryan and Dan', '/our-story', 'white'))


def gracie(lp='home', full=False):
    bubble = f"""<div class="bubble r"><div class="who"><i></i>Gracie · a sample text</div>
    <div class="m you">Hi! Do you have room for my golden, Brody, this Saturday night?</div>
    <div class="m her">We do. Saturday is a weekend night, so it is $80 plus HST, and Brody would need a quick meet and greet first. It is free and takes about twenty minutes. Want me to book one this week?</div>
    <div class="m you">Yes please, Thursday afternoon?</div>
    <div class="m her">Done. Thursday at 1:15 pm. I have texted you the details, and Taylor and Hannah know Brody is coming.</div></div>"""
    return f"""<section class="gracie{' full' if full else ' tight'}"><div class="wrap box" data-stagger><div><p class="eyebrow r">{GRACIE_EYEBROW}</p><h2 class="r">{GRACIE_H2}</h2>
  <p class="r">{GRACIE_P1}</p><p class="r">{GRACIE_P2}</p>
  <div class="ways r"><a href="{TEL}">Call {PHONE}</a><a href="{SMS}">Text {TEXT_NUMBER}</a></div>
  <p class="fineline r">Anything she quotes is confirmed when you book.</p></div>
  {bubble}</div></section>"""


def cta(lp='home', h='Start with a free meet and greet.', p='Walk the property, meet the team, and your dog’s first day or night is on us.'):
    return f"""<section class="cta"><div class="wrap" data-stagger><h2 class="r">{h}</h2><p class="lede r">{p}</p>
  <div class="btns r">{btn(CTA, book('cta', lp), 'white')}<a class="btn btn-ghost" href="{TEL}">Call {PHONE}</a></div>
  <p class="r" style="margin-top:var(--s3);font-size:var(--t-small);opacity:.9">After that, book whenever you like online. Cancel any time, free.</p></div></section>"""


def band(photo, h, lede=None, focus='center 50%', button=''):
    return f"""<section class="band"><div class="par">{pic(photo, '100vw', '', False, focus=focus)}</div><div class="wrap"><h2 class="r">{h}</h2>{f'<p class="lede r">{lede}</p>' if lede else ''}{f'<div class="btns r" style="margin-top:var(--s4)">{button}</div>' if button else ''}</div></section>"""


def three(items, eyebrow, h, lede=None):
    cells = ''.join(f'<div class="r"><span class="ic">{ICON[ic]}</span><h3>{t}</h3><p>{p}</p></div>' for ic, t, p in items)
    return f"""<section><div class="wrap" data-stagger><div class="split"><div><p class="eyebrow r">{eyebrow}</p><h2 class="r">{h}</h2></div>{f'<p class="lede r">{lede}</p>' if lede else ''}</div><div class="three">{cells}</div></div></section>"""


def faq(items, eyebrow='Straight answers', h='What people ask before the first visit.'):
    qs = ''.join(f'<details class="r"><summary>{esc(q)}<i>+</i></summary><div class="a">{esc(a)}</div></details>' for q, a in items)
    return f"""<section class="tight"><div class="wrap" data-stagger><p class="eyebrow r">{eyebrow}</p><h2 class="r">{h}</h2><div class="faq">{qs}</div>
  <p class="fine r">Something else? Call {PHONE} or text {TEXT_NUMBER}, any hour. Gracie, our AI front desk, answers in seconds, and Taylor and Hannah take it from there.</p></div></section>"""


DAY_THREE = [('sun', 'All day outside', 'Sun, shade, tall grass and puppy pools on 45 fenced acres. The barn is heated and cooled for the days that need it.'),
             ('group', 'Matched groups', 'Up to 40 campers, grouped by size and energy, so the quiet ones and the wild ones each get their kind of day.'),
             ('shield', 'Certified counselors', 'Every counselor holds Pet First Aid and Pet CPR, and they are beside the dogs from drop off to pick up.')]
NIGHT_THREE = [('barn', 'The barn', 'Heated in winter, air conditioned in summer, beds everywhere. It is theirs at night, and we are always close.'),
               ('bowl', 'Food from home', 'Bring what they eat at home. We serve it exactly your way, one dog at a time, and give medication at no charge.'),
               ('moon', 'Someone on the property, every night', 'A counselor is on the property every night of the year, and a 24 hour emergency vet clinic is close by.')]
PUPPY_THREE = [('paw', 'From three months', 'Puppies join from three months old. Up to nine months they come as they are; after that, spayed or neutered.'),
               ('group', 'Small matched groups', 'A few gentle friends their own size and energy, with a counselor beside them the whole time.'),
               ('moon', 'Never alone at night', 'Sleepovers are in the warm barn with the pack, and a counselor is on the property every night.')]


# ---------------------------------------------------------------- the document
def jsonld(slug, title, desc, faq_items=None, rated=False):
    if slug == 'index':
        biz = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "/#business", "name": "Camp Cookstown", "url": SITE + '/',
               "image": SITE + A('/Assets/brand/og-home.jpg'), "telephone": "+1-705-434-4777", "email": EMAIL, "priceRange": "$$", "foundingDate": "2008",
               "address": {"@type": "PostalAddress", "streetAddress": "5268 Simcoe County Road 56", "addressLocality": "Essa", "addressRegion": "ON", "postalCode": "L0L 1L0", "addressCountry": "CA"},
               "hasMap": MAPS,
               "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": o, "closes": c} for o, c in (("07:30", "08:30"), ("11:00", "12:00"), ("17:00", "18:00"))],
               "sameAs": [u for _, u in SOCIAL],
               "areaServed": ["Cookstown", "Barrie", "Innisfil", "Alliston", "Bradford", "Newmarket", "Tottenham", "Essa"]}
    else:
        biz = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "/#business", "name": "Camp Cookstown", "url": SITE + '/'}
    if rated:
        biz["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": RATING, "reviewCount": REVIEW_COUNT}
    out = [biz]
    if faq_items:
        out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]})
    return ''.join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in out)


def page(slug, title, desc, body, active=None, noindex=False, lp=None, faq_items=None, og=None, lean=False, rated=False):
    lp = lp or (slug if slug != 'index' else 'home')
    canon = SITE + ('/' if slug == 'index' else '/' + slug)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ''
    gtm = f"<script>(function(w,d,s,l,i){{var h=location.hostname;if(h!=='campcookstown.com'&&h!=='www.campcookstown.com'&&location.search.indexOf('__gtm=preview')<0)return;w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f)}})(window,document,'script','dataLayer','{GTM}');</script>" if GTM else ''
    og = A(og or '/Assets/brand/og-home.jpg')
    css = CSS.replace('/Assets/fonts/fraunces-var.woff', A('/Assets/fonts/fraunces-var.woff')).replace('/Assets/fonts/inter-var.woff', A('/Assets/fonts/inter-var.woff'))
    doc = f"""<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}">{robots}
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}{og}"><meta property="og:site_name" content="Camp Cookstown"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0F1A14"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><link rel="icon" href="{A('/Assets/brand/favicon-32.png')}" sizes="32x32"><link rel="apple-touch-icon" href="{A('/Assets/brand/apple-touch-icon.png')}"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="{A('/Assets/fonts/fraunces-var.woff')}" as="font" type="font/woff" crossorigin><link rel="preload" href="{A('/Assets/fonts/inter-var.woff')}" as="font" type="font/woff" crossorigin><link rel="preconnect" href="https://book.campcookstown.com" crossorigin>
<style>{css}</style>{jsonld(slug, title, desc, faq_items, rated)}{gtm}</head>
<body{' class="lean"' if lean else ''}>{header(active, lp, lean)}<main id="main" tabindex="-1">{body}</main>{footer(lean)}{mcta(lp)}<script>{JS}</script></body></html>"""
    for bad in ('—', '–'):
        if bad in doc:
            i = doc.index(bad)
            raise SystemExit(f'{slug}: a dash slipped in near: {doc[max(0, i - 60):i + 60]!r}')
    open(os.path.join(OUT, slug + '.html'), 'w').write(doc)
    PAGES[slug] = (title, noindex)
    return doc


# ---------------------------------------------------------------- pages
def home():
    b = hero('Cage free dog camp · Since 2008', 'Your dog’s dream vacation.',
             'Day camp and overnight camp on 45 acres of farmland at Cookstown, minutes from Highway 400. Every dog runs with the pack all day and sleeps in a warm barn at night.', 'home', video=True,
             lede_m='Day camp and overnight camp on 45 acres at Cookstown, minutes from Highway 400.')
    b += proof() + doors() + reviews() + film() + day_strip() + rate_tiles() + steps() + story_short() + gracie() + cta()
    page('index', 'Camp Cookstown | Dog Boarding and Day Camp near Barrie', 'Cage free dog day camp and overnight boarding on 45 acres at Cookstown, minutes off Highway 400. Heated barn, open every day since 2008. Free meet and greet first.', b, '/', rated=True)


def day():
    b = hero('Dog day camp · Cookstown', 'Drop off a dog.<br>Pick up a happy one.', 'A whole day outside on 45 fenced acres with a pack of friends and counselors who adore them.', 'day-camp', video=True, start=2.6,
             price=(f'<span class="pv" data-item-price="day.week">${RATES["day.week"]}</span> a day', f'or the ten day pack at <span class="pv" data-item-price="day.pack">${RATES["day.pack"]}</span>'))
    b += proof()
    b += three(DAY_THREE, 'Day camp, not daycare', 'A real camp, with the sky for a ceiling.', 'Camp is a farm. Dogs run, dig, splash and nap outside all day, and come into the barn when the weather sends them.')
    b += reviews((1, 7, 3), 'First days, in their words.', four=False, lp='day-camp')
    b += band('goldens-pink-pool', 'Forty five acres. One very good day.', focus='center 30%')
    b += film() + day_strip()
    dc = [('Day Camp', f'<span class="pv" data-item-price="day.week">${RATES["day.week"]}</span>', 'a day', 'Any day of the year. Drop off in the morning, pick up in the afternoon or evening.', ['Drop off 7:30 to 8:30 am or 11 to noon', 'Pick up 11 to noon or 5 to 6 pm', 'Ten percent off each extra dog']),
          ('Ten Day Pack', f'<span class="pv" data-item-price="day.pack">${RATES["day.pack"]}</span>', 'for ten days', 'Ten days for the price of eight. Use them whenever you like.', ['That is <span class="pv" data-item-price="day.perday">$40</span> a day', 'Book each day online in seconds', 'Ten percent off each extra dog'])]
    cards = ''.join(f'<article class="card r"><div class="name"><h3>{n}</h3><div class="amt">{p}<em style="font-family:var(--sans)">{per}</em></div></div><p class="spec">{sp}</p><ul>{"".join(f"<li>{x}</li>" for x in lis)}</ul><div class="act">{btn(CTA, book("card", "day-camp"))}</div></article>' for n, p, per, sp, lis in dc)
    b += f"""<section class="mist"><div class="wrap" data-stagger><p class="eyebrow r">Day camp rates</p><h2 class="r">Two prices. Simple.</h2>
      <div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">{cards}</div><p class="fine r">Prices are plus HST. Dogs need to be over three months old, healthy, free of fleas and ticks, current on their rabies shot, and spayed or neutered if over nine months.</p></div></section>"""
    b += steps('day-camp') + faq(DAY_FAQ, 'Day camp questions', 'What people ask before the first day.') + gracie('day-camp')
    b += cta('day-camp', 'The first day is free.', 'Book the free meet and greet online. Walk the property, meet the team, and let your dog decide.')
    page('day-camp', 'Dog Daycare near Barrie and Innisfil | Camp Cookstown Day Camp', 'Cage free dog day camp on 45 acres at Cookstown, minutes from Barrie and Innisfil. $50 a day, ten day pack $400, first day free. Open every day of the year.', b, '/day-camp', faq_items=DAY_FAQ, rated=True)


def night():
    rows = [('Weeknights', 'Monday to Thursday', 'overnight.week'), ('Weekends', 'Friday to Sunday', 'overnight.weekend'), ('Eight nights or more', 'Any nights', 'overnight.t3'), ('Fifteen nights or more', 'Any nights', 'overnight.t4'), ('Twenty eight nights or more', 'Any nights', 'overnight.t5'), ('Holidays and long weekends', 'March Break, and December 20 to January 1. Half paid at booking, and that deposit stays with the camp if plans change.', 'overnight.holiday')]
    tbl = ''.join(f'<tr><td><b>{a}</b><span>{d}</span></td><td class="amt"><span class="pv" data-item-price="{k}">${RATES[k]}</span> <small>a night</small></td></tr>' for a, d, k in rows)
    b = hero('Dog boarding · Cookstown', 'Days in the field. Nights in the barn.', 'Full days outside on 45 acres, dinner served one at a time, and a warm barn to fall asleep in with the pack. A counselor is on the property every night.', 'overnight-camp', video=True,
             price=(f'From <span class="pv" data-item-price="overnight.week">${RATES["overnight.week"]}</span> a night', f'weekends <span class="pv" data-item-price="overnight.weekend">${RATES["overnight.weekend"]}</span>, holidays <span class="pv" data-item-price="overnight.holiday">${RATES["overnight.holiday"]}</span>'))
    b += proof()
    b += three(NIGHT_THREE, 'Boarding, the camp way', 'Sleepovers with friends.', 'Camp is a sleepover with the pack. Full days outside, dinner served one at a time, and a warm barn to fall asleep in.')
    b += reviews((4, 0, 8), 'First sleepovers, in their words.', four=False, lp='overnight-camp')
    b += band('barn-asleep-shavings', 'A sleepover with friends, in a barn that is warm all winter.', focus='center 55%')
    b += f"""<section class="mist" id="rates"><div class="wrap" data-stagger><div class="split"><div><p class="eyebrow r">Overnight rates</p><h2 class="r">The longer the stay, the lower the night.</h2></div><p class="lede r">Every price is per night, plus HST. Ten percent off each extra dog from the same home. Cancel any time, free.</p></div>
      <table class="price r"><thead><tr><th>Stay</th><th>Per night</th></tr></thead><tbody>{tbl}</tbody></table>
      <p class="fine r">A night runs from drop off to pick up the next morning. Drop off 7:30 to 8:30 am or 11 to noon. Pick up 11 to noon or 5 to 6 pm. A pick up between 5 and 6 pm on the last day adds a day of camp at <span class="pv" data-item-price="overnight.pm-pickup">${RATES['overnight.pm-pickup']}</span>.</p>
      <div class="btns r" style="margin-top:var(--s4)">{btn(CTA, book('rates', 'overnight-camp'))}</div>
      <div class="perk r" style="margin-top:var(--s5)"><b>The Spa Treatment</b><span>A wash, dry, ears and nails before pick up, so they go home fresh. Priced by size and coat.</span><a href="/spa">About the spa</a></div></div></section>"""
    b += film('A day and a night at camp.', 'Sleepover footage') + day_strip('A day and a night, start to finish.')
    b += steps('overnight-camp') + faq(NIGHT_FAQ, 'Overnight questions', 'What people ask before the first sleepover.') + gracie('overnight-camp')
    b += cta('overnight-camp', 'Start with a free night at camp.', 'Book the free meet and greet online. Walk the property, meet the team, and your dog’s first night is on us.')
    page('overnight-camp', 'Dog Boarding near Barrie | Overnight Camp at Camp Cookstown', 'Cage free dog boarding on 45 acres at Cookstown, minutes from Barrie and Innisfil. Heated barn, a counselor on site every night, from $65 a night. First night free.', b, '/overnight-camp', faq_items=NIGHT_FAQ, rated=True)


def rates():
    def tbl(rows, unit=''):
        return '<table class="price r"><thead><tr><th>What</th><th>Price</th></tr></thead><tbody>' + ''.join(f'<tr><td><b>{a}</b><span>{d}</span></td><td class="amt">{p}{unit}</td></tr>' for a, d, p in rows) + '</tbody></table>'
    P = lambda k: f'<span class="pv" data-item-price="{k}">${RATES[k]}</span>'
    dayrows = [('Day Camp', 'One full day, any day of the year', P('day.week')), ('Ten Day Pack', '$40 a day, use them whenever you like', P('day.pack'))]
    nightrows = [('Weeknights', 'Monday to Thursday', P('overnight.week')), ('Weekends', 'Friday to Sunday', P('overnight.weekend')), ('Eight nights or more', 'Any nights', P('overnight.t3')), ('Fifteen nights or more', 'Any nights', P('overnight.t4')), ('Twenty eight nights or more', 'Any nights', P('overnight.t5')), ('Holidays and long weekends', 'March Break, and December 20 to January 1. Half paid at booking, and that deposit stays with the camp if plans change.', P('overnight.holiday'))]
    extras = [('The Spa Treatment', 'Wash, dry, massage, ears and nails, for campers only', 'By size and coat'), ('Vet visit', 'If your dog needs the clinic, we take them', '$40 plus the bill'), ('Food, if you forget it', 'We have some on hand', '$50 plus the bag'), ('Late pick up', 'Between 5 and 6 pm on the last day of a stay', P('overnight.pm-pickup') + ', a day of camp')]
    b = hero('Rates · Day and overnight', 'Real prices, on the page.', 'Everything below is plus HST. Ten percent off each extra dog from the same home. Cancel any time at no charge, holiday deposits aside.', 'rates', photo='pack-looking-up', focus='center 18%', short=True, sub=None)
    b += f"""<section><div class="wrap" data-stagger><p class="eyebrow r">Day camp</p><h2 class="r">Two prices. Simple.</h2>{tbl(dayrows)}
      <p class="r" style="margin-top:var(--s4)"><a href="/day-camp" style="font-weight:600;text-decoration:underline;text-underline-offset:4px">What a day at camp looks like</a></p></div></section>"""
    b += f"""<section class="mist"><div class="wrap" data-stagger><p class="eyebrow r">Overnight camp</p><h2 class="r">The longer the stay, the lower the night.</h2>{tbl(nightrows, ' <small>a night</small>')}
      <p class="fine r">A night runs from drop off to pick up the next morning. Drop off 7:30 to 8:30 am or 11 to noon. Pick up 11 to noon or 5 to 6 pm. A pick up between 5 and 6 pm on the last day adds a day of camp.</p>
      <p class="r" style="margin-top:var(--s4)"><a href="/overnight-camp" style="font-weight:600;text-decoration:underline;text-underline-offset:4px">What a sleepover looks like</a></p></div></section>"""
    b += f"""<section><div class="wrap" data-stagger><p class="eyebrow r">Extras</p><h2 class="r">The little things, priced.</h2>{tbl(extras)}
      <p class="fine r">Medication is given at no charge. Bring it in the original container.</p></div></section>"""
    b += steps('rates') + cta('rates')
    page('rates', 'Rates | Camp Cookstown Dog Boarding and Day Camp Prices', 'Camp Cookstown rates: day camp $50, ten day pack $400, overnight from $65 a night, holidays $100. Ten percent off each extra dog. Cancel any time, free.', b, '/rates')


def story():
    b = hero('Ryan and Dan · Since 2008', 'Two brothers, a barn, and a lot of dogs.', 'We toured the world playing music. Then we came home and built the place we wished existed for our own dogs.', 'our-story', photo='barn-sunset', focus='center 60%', short=True)
    b += f"""<section><div class="wrap split" data-stagger><div><p class="eyebrow r">How it started</p><h2 class="r">Nineteen, a tour bus, and two dogs at home.</h2></div>
      <div class="prose r"><p>At nineteen we left Ontario to play music, and the road took us further than we ever expected, all the way to Las Vegas, singing country classics on a stage with Shania Twain.</p>
      <p>The hard part was never the shows. It was leaving our dogs. We wanted a place we trusted, so when we came home we built one: a real camp, on 45 acres of farmland in Essa, where a dog can spend the day outside with friends and sleep in a warm barn with the pack.</p>
      <p>Camp Cookstown opened in 2008. The same two brothers still run it, with a team of counselors who are here for one reason. They love dogs the way we do.</p></div></div></section>"""
    b += band('barn-lane-pano', 'Built in 2008 on 45 acres of Essa farmland.', focus='28% 62%')
    b += team_block('The team', 'The faces your dog will know.', 'Taylor and Hannah run the camp every day, with a crew of counselors who are here for one reason. They love dogs the way we do.')
    b += three([('sun', 'Cage free, always', 'A dog on vacation is outside with friends, and sleeps in the barn with the pack. It has been the promise since day one.'),
                ('heart', 'Treated like our own', 'The same food, the same medication, the same fuss. If we would not do it for our dogs, we do not do it for yours.'),
                ('moon', 'Tired is happy', 'A dog that has run all day, splashed in a pool and napped in the sun goes home content. That is the whole idea.')], 'What we believe', 'Three rules we have never broken.')
    b += reviews((2, 5, 6), 'Some families have been coming for nine years.', four=False, lp='our-story')
    b += cta('our-story', 'Come walk the property.', 'The meet and greet is free, and so is your dog’s first day or night.')
    page('our-story', 'Our Story | Ryan and Dan of Camp Cookstown', 'Two brothers who toured the world playing music came home and built a cage free camp for dogs on 45 acres in Essa, Ontario. Camp Cookstown, since 2008.', b, '/our-story')


def life():
    allp = [('barn-lane-pano', 'wide'), ('pack-looking-up', 'tall'), ('counselor-field-sky', ''), ('goldens-pink-pool', ''), ('field-pack-barn', 'wide'), ('spaniel-pool-hat', ''), ('senior-golden-grass', 'tall'), ('three-goldens-hearts', ''), ('party-hats', ''), ('barn-inside-beds', 'wide'), ('lab-and-pal', ''), ('goldens-two-faces', 'wide'), ('golden-water', ''), ('dachshund-nap', ''), ('pool-shake', ''), ('whippet-hoodie', ''), ('cavalier-blanket', ''), ('chihuahua-blanket', ''), ('counselor-aussie', 'wide'), ('frenchies-grass', 'tall'), ('field-run', ''), ('goldens-asleep', ''), ('barn-asleep-shavings', 'wide'), ('golden-yawn', ''), ('aussie-bucket', '')]
    tiles = ''.join(f'<figure class="{c} r">{pic(p, "(max-width: 760px) 50vw, 25vw")}</figure>' for p, c in allp)
    links = ' · '.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL[:3])
    b = hero('Camp life', 'Real campers. Real days.', 'Every photo on this site is a real dog on a real day at camp. Here are some of our favourites.', 'camp-life', photo='counselor-field-sky', focus='center 30%', short=True, sub=None)
    b += film('Have a look around.', 'Real footage') + day_strip()
    b += f"""<section class="mist"><div class="wrap" data-stagger><p class="eyebrow r">Photos</p><h2 class="r">A few of the pack.</h2>
      <div class="mosaic">{tiles}</div><p class="follow r">New photos most days. Follow along on {links}.</p>
      <a class="yt r" href="https://www.youtube.com/watch?v={YOUTUBE_ID}" data-id="{YOUTUBE_ID}" target="_blank" rel="noopener">{pic('goldens-two-faces', '(max-width: 720px) 100vw, 80vw', '', False, 'Play the Camp Cookstown video')}<span class="play"><i>&#9654;</i>Play the camp video</span></a></div></section>"""
    b += cta('camp-life', 'Your dog belongs in these photos.', 'Book the free meet and greet online and come see the place for yourself.')
    page('camp-life', 'Camp Life | Photos and Video from Camp Cookstown', 'Real photos and video of real campers at Camp Cookstown, the cage free dog camp on 45 acres in Essa, Ontario.', b, '/camp-life')


def faq_page():
    b = hero('Questions', 'Straight answers.', 'Everything people ask before the first visit. If yours is not here, call or text and you will have an answer in seconds.', 'faq', photo='goldens-two-faces', focus='center 40%', short=True, sub=None)
    b += faq(GENERAL_FAQ, 'Before the first visit', 'The questions we hear most.') + gracie('faq', full=True)
    b += cta('faq', 'Still wondering? Come see it.', 'The meet and greet is free, takes twenty minutes, and answers everything.')
    page('faq', 'FAQ | Camp Cookstown Dog Camp Questions', 'What your dog needs before camp, drop off and pick up times, food, medication, nights in the barn, and cancellations. Camp Cookstown, Essa, Ontario.', b, faq_items=GENERAL_FAQ)


def reviews_page():
    cards = ''.join(f'<article class="review r"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><q>{esc(t)}</q><div class="who"><b>{esc(n)}</b><span>Google review</span></div></article>' for n, t in REVIEWS)
    b = hero(f'{RATING} on Google · {REVIEW_COUNT} reviews', 'What the humans say.', f'Real reviews from real families, copied from Google. Read all {REVIEW_COUNT} there.', 'reviews', photo='three-goldens-hearts', focus='center 40%', short=True, sub=None)
    b += f"""<section class="dark"><div class="wrap" data-stagger><div class="reviews-grid" style="margin-top:0">{cards}</div>
      <div class="btns r" style="margin-top:var(--s5)"><a class="btn btn-ghost" href="{MAPS}" target="_blank" rel="noopener">All {REVIEW_COUNT} reviews on Google</a></div></div></section>"""
    b += cta('reviews', 'Your dog’s first day is on us.', 'Book the free meet and greet online, walk the property, and decide for yourself.')
    page('reviews', f'Reviews | Camp Cookstown, {RATING} on Google', f'Real Google reviews of Camp Cookstown, the cage free dog camp on 45 acres near Barrie, Ontario. Rated {RATING} from {REVIEW_COUNT} reviews.', b, rated=True)


def contact():
    b = hero('Contact and directions', 'Come see the place.', 'Minutes from Highway 400 at Cookstown. Call or text any hour and Gracie answers.', 'contact', photo='barn-sunset', focus='center 62%', short=True, sub=None)
    b += f"""<section><div class="wrap" data-stagger><p class="eyebrow r">Find us</p><h2 class="r">5268 Simcoe County Road 56, Essa.</h2>
      <div class="contact"><div class="r"><small>Call, text or email</small><b><a href="{TEL}">{PHONE}</a></b><p><a href="{SMS}">Text {TEXT_NUMBER}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div class="r"><small>Drop off and pick up</small><b>Every day of the year</b><p>Drop off 7:30 to 8:30 am or 11 to noon.<br>Pick up 11 to noon or 5 to 6 pm.</p></div>
      <div class="r"><small>Directions</small><b><a href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps</a></b><p>Highway 400 to Cookstown, then west on County Road 56. Watch for our flag at the bottom of the hill, then drive on down to the barn.</p></div></div></div></section>"""
    b += gracie('contact', full=True)
    b += band('goldens-two-faces', 'Come walk the property. The meet and greet is free.', focus='center 40%')
    b += cta('contact', 'Book the free meet and greet.', 'Twenty minutes, a walk around the farm, and your dog meets a few new friends.')
    page('contact', 'Contact | Camp Cookstown, Essa, Ontario', f'Camp Cookstown, {ADDRESS}. Call or text {PHONE} any hour. Open every day, drop off from 7:30 am.', b)


def spa():
    b = hero('Spa · For campers only', 'Go home fresh.', 'A wash, a dry, a gentle massage, clean ears and trimmed nails, all done before pick up.', 'spa', photo='pool-shake', focus='center 45%', short=True, sub=None)
    b += f"""<section><div class="wrap" data-stagger><div class="split"><div><p class="eyebrow r">What is included</p><h2 class="r">Four things, done gently.</h2></div>
      <p class="lede r">Add it to any day or sleepover. Prices depend on size and coat, so ask when you book or call for a number.</p></div>
      <ol class="num"><li class="r"><div><b>Wash and dry</b><span>A full body wash with natural shampoo, then a proper dry.</span></div></li>
      <li class="r"><div><b>Gentle massage</b><span>Pure relaxation after a big day outside.</span></div></li>
      <li class="r"><div><b>Ear cleaning</b><span>Clean and clear, checked while we are there.</span></div></li>
      <li class="r"><div><b>Nail trim</b><span>Happier paws, and a happier floor at home.</span></div></li></ol></div></section>"""
    b += band('golden-water', 'A little extra, for campers only.', focus='center 35%')
    b += cta('spa', 'Add the spa when you book.', 'Or call and we will quote it for your dog’s size and coat.')
    page('spa', 'The Spa Treatment | Camp Cookstown', 'A wash, dry, massage, ear cleaning and nail trim for dogs staying at Camp Cookstown, done before pick up. For campers only, priced by size and coat.', b)


def privacy():
    b = f"""<section class="nf"><div class="wrap"><p class="eyebrow">Privacy</p><h1>Your information stays with us.</h1><p class="sub">Plain English, because that is how we do everything.</p></div></section>
    <section><div class="wrap prose">
      <h3>What we collect</h3><p>When you book, we collect what we need to look after your dog: your name, phone number and email, your dog’s details, vaccination records and any notes you give us. Bookings run through our own system at book.campcookstown.com.</p>
      <h3>How we use it</h3><p>To run camp: confirming bookings, reaching you if something comes up, and sending photos and updates about your dog. We never sell or rent your information.</p>
      <h3>Calls and texts</h3><p>Our front desk, Gracie, is an AI. Calls and texts to the camp may be answered by her and are kept so our team can follow up properly. Ask for a person any time and one of us will call you back.</p>
      <h3>Cookies and analytics</h3><p>This site uses standard analytics and advertising cookies so we can see which pages are useful and whether our ads are working. If you arrived from an ad, the click identifier is kept so we can attribute your booking. You can block cookies in your browser and the site still works.</p>
      <h3>Photos</h3><p>We take photos of campers during the day and share them with you and on our social accounts. Tell us at the meet and greet if you would rather your dog stayed off social media.</p>
      <h3>Questions</h3><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call {PHONE}.</p></div></section>"""
    page('privacy-policy', 'Privacy Policy | Camp Cookstown', 'How Camp Cookstown collects and uses your information.', b, noindex=True)


def notfound():
    b = f"""<section class="nf"><div class="wrap"><p class="eyebrow">Page not found</p><h1>This one wandered off.</h1><p class="sub">The page you want is not here, but the dogs are. Try one of these.</p>
      <div class="btns">{btn('Home', '/', 'white', False)}{btn('Day Camp', '/day-camp', 'ghost', False)}{btn('Overnight Camp', '/overnight-camp', 'ghost', False)}{btn('Rates', '/rates', 'ghost', False)}</div></div></section>"""
    page('404', 'Page not found | Camp Cookstown', 'That page is not here.', b, noindex=True)


INDEXED_LANDING = {'dog-boarding', 'dog-daycare', 'dog-boarding-barrie', 'dog-daycare-barrie', 'dog-camp', 'puppy-camp', 'dog-kennel-barrie', 'dog-kennel'}


def landing(slug):
    title, desc, h1a, h1b, lede, drive, kind = TOWNS[slug]
    h1 = f'{h1a} <span style="display:block">{h1b}</span>' if len(h1a) + len(h1b) > 28 else f'{h1a} {h1b}'
    eyebrow = {'boarding': 'Dog boarding · Cookstown', 'daycare': 'Dog day camp · Cookstown', 'kennel': 'Cage free boarding · Cookstown', 'camp': 'Cookstown dog camp · Since 2008', 'puppy': 'Puppy camp · Cookstown', 'offer-night': 'First night free', 'offer-day': 'First day free'}[kind]
    if kind in ('boarding', 'kennel', 'offer-night'):
        price = (f'From <span class="pv" data-item-price="overnight.week">${RATES["overnight.week"]}</span> a night', f'weekends <span class="pv" data-item-price="overnight.weekend">${RATES["overnight.weekend"]}</span>, holidays <span class="pv" data-item-price="overnight.holiday">${RATES["overnight.holiday"]}</span>')
    elif kind in ('daycare', 'offer-day'):
        price = (f'<span class="pv" data-item-price="day.week">${RATES["day.week"]}</span> a day', f'or the ten day pack at <span class="pv" data-item-price="day.pack">${RATES["day.pack"]}</span>')
    else:
        price = None
    night = kind in ('boarding', 'kennel', 'offer-night')
    b = hero(eyebrow, h1, lede, slug, video=True, price=price, start=2.6 if kind in ('daycare', 'offer-day', 'puppy', 'camp') else 0)
    b += proof()
    b += f'<section class="tight"><div class="wrap" data-stagger><p class="eyebrow r">Getting here</p><p class="lede r">{drive}</p></div></section>'
    b += reviews((4, 0, 2) if night else (1, 7, 3), 'What the humans say.', four=False, lp=slug)
    if kind == 'kennel':
        b += three([('barn', 'A heated barn to sleep in', 'Nights are in a heated, air conditioned barn with beds everywhere, together with the pack.'),
                    ('sun', 'Forty five acres to run on', 'Days are outside on 45 fenced acres with sun, shade, tall grass and puppy pools.'),
                    ('moon', 'Someone on the property, every night', 'A counselor is on the property every night of the year, and a 24 hour emergency vet clinic is close by.')], 'What a night here looks like', 'A barn, a field, and a pack of friends.')
    elif kind in ('boarding', 'offer-night'):
        b += three(NIGHT_THREE, 'Boarding, the camp way', 'Sleepovers with friends.', 'Camp is a sleepover with the pack. Full days outside, dinner served one at a time, and a warm barn to fall asleep in.')
    elif kind in ('daycare', 'offer-day'):
        b += three(DAY_THREE, 'Day camp, not daycare', 'A real camp, with the sky for a ceiling.')
    elif kind == 'puppy':
        b += three(PUPPY_THREE, 'Puppies, gently', 'A first day that feels easy.')
    else:
        b += three([('sun', 'All day outside', 'Sun, shade, tall grass and puppy pools on 45 fenced acres.'), ('barn', 'A heated barn', 'Warm in winter, cool in summer, beds everywhere. Sleepovers with the pack.'), ('shield', 'Certified counselors', 'Pet First Aid and Pet CPR, beside the dogs from drop off to lights out.')], 'A real camp', 'Fields, a barn, and a pack of friends.')
    bands = {'boarding': ('barn-asleep-shavings', 'A sleepover with friends, in a barn that is warm all winter.', 'center 55%'),
             'kennel': ('barn-inside-beds', 'The barn, with the beds where the pack sleeps.', 'center 50%'),
             'offer-night': ('goldens-asleep', 'The first night is on us.', 'center 50%'),
             'daycare': ('field-pack-barn', 'Forty five acres. One very good day.', 'center 50%'),
             'offer-day': ('goldens-pink-pool', 'The first day is on us.', 'center 30%'),
             'puppy': ('goldens-pink-pool', 'Small groups, gentle starts.', 'center 30%'),
             'camp': ('field-pack-lane', 'A real camp, with a real pack.', 'center 50%')}
    ph, cap, foc = bands[kind]
    b += band(ph, cap, focus=foc)
    b += rate_tiles(slug) + steps(slug)
    b += faq((NIGHT_FAQ if night else DAY_FAQ if kind in ('daycare', 'offer-day') else GENERAL_FAQ)[:3])
    if kind == 'offer-night':
        b += cta(slug, 'Your dog’s first night is on us.', 'Book the free meet and greet online. After it, the first night at camp is free.')
    elif kind == 'offer-day':
        b += cta(slug, 'Your dog’s first day is on us.', 'Book the free meet and greet online. After it, the first day at camp is free.')
    else:
        b += cta(slug)
    page(slug, title, desc, b, lp=slug, lean=True, noindex=slug not in INDEXED_LANDING)


# ---------------------------------------------------------------- assets and machine files
def assets():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'Assets'))
    for sub in ('fonts', 'brand'):
        for f in sorted(os.listdir(os.path.join(SRC, sub))):
            if f == 'logo-trimmed.png' or f.startswith('.'):
                continue
            _hashed_copy(os.path.join(SRC, sub, f), f'/Assets/{sub}/{f}')
    for f in sorted(os.listdir(PHOTO_SRC)):
        if f.endswith(('.avif', '.webp')):
            _hashed_copy(os.path.join(PHOTO_SRC, f), f'/Assets/photos/{f}')
    for f in sorted(os.listdir(VIDEO_SRC)):
        p = os.path.join(VIDEO_SRC, f)
        if os.path.isfile(p) and not f.startswith('.'):
            _hashed_copy(p, f'/Assets/video/{f}')
    fd = os.path.join(VIDEO_SRC, 'film', 'd')
    if os.path.isdir(fd):
        # the frames keep their numbering; the folder itself is hashed so a re-cut gets a new URL
        h = hashlib.sha1(b''.join(open(os.path.join(fd, f), 'rb').read() for f in sorted(os.listdir(fd)))).hexdigest()[:8]
        dst = os.path.join(OUT, 'Assets', f'film.{h}', 'd')
        shutil.copytree(fd, dst)
        ASSETS['/Assets/film'] = f'/Assets/film.{h}'
        ASSETS['/Assets/film/d/001.webp'] = f'/Assets/film.{h}/d/001.webp'


def machine_files():
    pages = ['/'] + [f'/{s}' for s, (t, noindex) in PAGES.items() if s not in ('index', '404', 'privacy-policy') and not noindex]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{p}</loc><lastmod>{STAMP}</lastmod></url>' for p in pages) + '</urlset>\n'
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    redirects = [('/about', '/our-story'), ('/about/meet-owners', '/our-story'), ('/about/why-choose-us', '/faq'), ('/top-10-reasons', '/faq'), ('/guest-services', '/'),
                 ('/guest-services/day-camp', '/day-camp'), ('/guest-services/overnight-camp', '/overnight-camp'), ('/guest-services/the-spa-treatment', '/spa'), ('/guest-services/transportation', '/contact'),
                 ('/photos', '/camp-life'), ('/videos', '/camp-life'), ('/faqs', '/faq'), ('/our-rates', '/rates'), ('/contact-us', '/contact'), ('/index.php', '/'),
                 ('/dog-boarding-toronto', '/overnight-camp')]
    csp = ("default-src 'self'; base-uri 'self'; form-action 'self'; object-src 'none'; frame-ancestors 'self' https://tagassistant.google.com; "
           "img-src 'self' data: https://i.ytimg.com https://www.google.com https://www.google.ca https://googleads.g.doubleclick.net https://stats.g.doubleclick.net https://www.googletagmanager.com; "
           "media-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; "
           "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.googleadservices.com https://googleads.g.doubleclick.net; "
           "connect-src 'self' https://book.campcookstown.com https://www.google-analytics.com https://*.google-analytics.com https://*.analytics.google.com https://www.googletagmanager.com https://*.doubleclick.net https://www.google.com; "
           "frame-src https://www.youtube-nocookie.com https://www.youtube.com https://td.doubleclick.net https://tagassistant.google.com")
    vercel = {
        "cleanUrls": True, "trailingSlash": False,
        "redirects": [{"source": a, "destination": b, "permanent": True} for a, b in redirects],
        "headers": [
            {"source": "/Assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
                {"key": "Strict-Transport-Security", "value": "max-age=31536000"},
                {"key": "Content-Security-Policy", "value": csp}]},
            {"source": "/(.*)", "has": [{"type": "host", "value": ".*\\.vercel\\.app"}], "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]},
        ],
    }
    json.dump(vercel, open(os.path.join(OUT, 'vercel.json'), 'w'), indent=1)
    json.dump({"name": "Camp Cookstown", "short_name": "Camp Cookstown", "start_url": "/", "display": "browser", "background_color": "#F7F4EC", "theme_color": "#0F1A14",
               "icons": [{"src": A('/Assets/brand/icon-192.png'), "sizes": "192x192", "type": "image/png"}, {"src": A('/Assets/brand/icon-512.png'), "sizes": "512x512", "type": "image/png"}]},
              open(os.path.join(OUT, 'site.webmanifest'), 'w'))


def main():
    global CSS, JS
    CSS = open(os.path.join(SRC, 'site.css')).read()
    JS = open(os.path.join(SRC, 'site.js')).read()
    assets()
    home(); day(); night(); rates(); story(); life(); faq_page(); reviews_page(); contact(); spa(); privacy(); notfound()
    for slug in TOWNS:
        landing(slug)
    machine_files()
    print(f'wrote {len(PAGES)} pages, film frames {FILM_FRAMES}')


if __name__ == '__main__':
    main()

# Camp Cookstown website

The whole site is generated from two files: `content.py` (every word, every fact, every price fallback) and `build.py` (how it renders). `python3 build.py` writes 33 pages and every asset into `out/`, which is what Vercel serves.

## Everyday

    python3 build.py && python3 check.py

Expect `wrote 33 pages` and `links ok`, `dashes: 0`. The build refuses to write a page that contains a dash. Commit and push, Vercel deploys `out/` on every push to main.

## Where things live

- `content.py`: copy, reviews, questions, rates fallbacks, the town pages table, the Gracie lines.
- `build.py`: the page blocks (hero, proof strip, doors, film, day strip, reviews, rate tiles, steps, Gracie, CTA, footer) and every page.
- `src/site.css`, `src/site.js`: the look and the motion. Inlined into every page at build time. No libraries.
- `src/photos/`: the graded photo exports (AVIF and WebP at 480, 900, 1600, 2400) plus `manifest.json`. Made by `tools/make_photos.py` from `raw/`.
- `src/video/`: the hero film, the two back window loops, posters and the film frames. Made by `tools/make_video.py` from the 4K master (the 23 Aug 2026 upscale of Camp Cookstown (Real Hero)_4, 2160x3840): `python3 tools/make_video.py <master.mp4> <outdir> hero|panes|film|day|all`, then copy the results into `src/video/`.
- `src/fonts/`, `src/brand/`: Fraunces and Inter, the logo, icons, the share image.
- `out/`: the built site. `out/vercel.json` carries clean URLs, the old address redirects, cache and security headers, and noindex on every host except campcookstown.com.

## The hero

Phones: the whole 36 second film, full screen, uncut. It opens on the pack in the field, dissolves from the last shot into the rainbow partway through, and loops back onto the frame it started on. Wide screens: the same film in the front window of a 3D stage, with two smaller windows of other scenes behind it at different depths. The windows arrive from the back when the page opens, lean with the mouse, and sink away as the page slides up over the hero (the hero is fixed on wide screens and everything after it sits in `.after`). The blurred backdrop is the front video itself, painted to a small canvas. All of it is CSS and about sixty lines of JS in the hero block of `src/site.js`; the stage measurements live in the `@media (min-width:901px)` block of `src/site.css` and are in vh so the cluster keeps its shape on any screen.

## Prices

Every price on the site is a `<span data-item-price="key">` with the current number baked in as a fallback. On load the page fetches `https://book.campcookstown.com/pricing.json` and replaces them, so the RateCard in the booking system is the only place a price changes. Keys: day.week, day.pack, overnight.week, overnight.weekend, overnight.t3, overnight.t4, overnight.t5, overnight.holiday, overnight.pm-pickup. When a rate changes, also update the fallback in `content.py` so the first paint is right too.

## The booking button

Every button goes to `https://book.campcookstown.com/get-started?src=site&cmp=<page>-<spot>`, straight into the three step signup for the free meet and greet. Click ids (gclid, wbraid, gbraid, fbclid, msclkid, utm_*) found on the URL, in cookies or in session storage ride along on every booking link. Returning families use the quiet Family sign in link in the header, which opens the sign in form directly.

## Adding or changing a town page

Add a row to `TOWNS` in `content.py` (title, meta, two H1 halves, lede, drive line, kind) and build. The kind picks the blocks: boarding, daycare, kennel, camp, puppy, offer-night, offer-day. Then point the keyword or ad at `/the-slug`.

## Replacing a photo

Drop the new file in `raw/`, run `python3 tools/make_photos.py src/photos <slug>`, add the alt text to `PHOTOS` in `content.py`, and use the slug in `build.py`. Give a replaced photo a new slug: assets are cached for a year by file name.

## Checking a page

- `python3 shoot.py <slug>`: page top at desktop and phone.
- `python3 shoot2.py <slug> phone`: walks the page screen by screen the way a person scrolls, and stitches it.
- `python3 preview.py index phone` or `index desk`: a one file preview with everything inlined, for a private link, plus `preview/artifact-*.html` for an artifact. Uses light hero encodes from `preview/_tmp/` (see the note at the top of `preview.py`) so the file stays under 16 MB.
- `python3 shot_hero.py`: the desktop hero at six screen sizes plus three scroll positions, and `python3 shot_sel.py index "section.day" phone`: one section, one screen.
- `python3 verify_live.py https://<deployment>.vercel.app`: proves the live host matches `out/` file for file.

## Git from a Claude session on the Mac

The Claude device shell cannot delete files, so every git command leaves an empty `.lock` file behind in `.git/` (the rename works, the unlink does not) and the next command refuses to run. Move the locks out of the way first, then run the command, then move them again:

    for f in $(find .git -maxdepth 3 -name "*.lock"); do mv "$f" ../_to_delete/git-locks/$(basename $f).$(date +%s%N); done

Pushing is always done by Ryan from Terminal: `cd ~/Claude/Projects/Camp\ Cookstown/website-2026/campcookstown-site && git push`.

## Rules that do not move

No dashes anywhere a customer reads. Real photos, real reviews, real numbers only. One primary action per page: the free meet and greet. Say what camp is, never what it is not. Toronto stays off the site. Logins, DNS and money are Ryan's fingers.

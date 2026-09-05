# Start here: the state of the Camp Cookstown site and how to work on it

Written at the end of the 5 September 2026 session. A new Claude session should read this, then `README.md`, and it has everything it needs.

## Where the site is

- Source of truth: the git repo on Ryan's Mac at `~/Claude/Projects/Camp Cookstown/website-2026/campcookstown-site` (connected folder "Camp Cookstown"). Pushed to GitHub `RyanDan444/campcookstown-site` (public), branch `main`.
- Live: Vercel project `campcookstown-site` (id prj_RJWL5gTdwco2fwJwz4M9w3hmmN4P, team ryan-kowarsky, team_JRmastUAdA0ZJecT6hGiU7H7). Every push to `main` deploys `out/` as is, no build step. Production alias `campcookstown-site.vercel.app`. Last deployed commit at the time of writing: 67f1c55 "Hero film opens on the pack in the field", READY.
- Private previews (one file, everything inlined) live as artifacts: desktop `https://claude.ai/code/artifact/3286b054-c19e-4294-808e-4f6ae02f077b`, phone `https://claude.ai/code/artifact/332a8578-1530-4a20-b85a-eb7e514eeb67`. To update them, rebuild with `preview.py` and publish `preview/artifact-desk.html` and `preview/artifact-phone.html` passing those URLs, so the links Ryan has keep working.
- The real domain campcookstown.com is still on the old Concrete CMS site at Whetham. Launch morning switches DNS at Cloudflare, which is Ryan's job.

## The one thing not in the repo

The 4K master film: `Camp Cookstown (Real Hero)_4`, the 23 Aug 2026 Higgsfield upscale, 2160x3840, 30 fps, 36.1 s, HEVC. On the Mac it is `Downloads/hf_20260823_191857_3a389979...mp4` and the same file is `Camp Cookstown/homepage/hero-mobile.mp4`. Do not use the horizontal "Camp Cookstown 4k Hero Video.mp4" from 14 August, that is the old hero. Every video asset in `src/video/` is cut from the master by `tools/make_video.py`; the outputs are committed, so the master is only needed to recut.

## How a Claude session works on this (the method that worked)

1. Get the files into the cloud workspace: `git clone https://github.com/RyanDan444/campcookstown-site.git`, or stage the changed files from the Mac with the device bridge if the Mac is ahead of GitHub. Check the Mac first: `git --no-optional-locks log --oneline | head -3` in the repo, compared with GitHub.
2. Work in the cloud: edit `content.py`, `build.py`, `src/site.css`, `src/site.js`; run `python3 build.py && python3 check.py`; look at it with `shoot2.py` (screen by screen walk), `shot_sel.py` (one section), `shot_hero.py` (desktop hero at six sizes). Playwright and Chromium are already in the container; ffmpeg, Pillow and OpenCV too. Headless Chromium cannot decode H.264, so in screenshots every video shows its poster frame, which is expected.
3. Put it back on the Mac: copy changed files under `/mnt/user-data/outputs/sync/<same relative path>` and call `device_commit_files` with those staged paths (50 files, 20 MB per file, 100 MB per call). Compare md5 lists first so only changed files move. Hashed assets in `out/Assets/` change name when their content changes, so new files must be added and the old ones moved out (the device shell cannot delete: `mv` them to `website-2026/_to_delete/`).
4. Commit on the Mac from the device shell with the lock workaround in `README.md` (every git command leaves an empty `.lock` behind; move the locks away before and after). Use `-c user.name="Ryan Kowarsky" -c user.email="kowarskyr@gmail.com"`.
5. Ryan pushes. Always hand him the command as a code block: `cd ~/Claude/Projects/Camp\ Cookstown/website-2026/campcookstown-site && git push`. Vercel deploys in about ten seconds; `get_deployment campcookstown-site.vercel.app` on the Vercel MCP confirms the commit and READY.

Network from the cloud container: GitHub, PyPI and the Vercel and Google APIs work; cdnjs, vercel.com pages, book.campcookstown.com and Higgsfield uploads and downloads do not. The Mac's device shell has no network at all. WebFetch works for reading live pages.

## What the site is now

Everything in `README.md`, plus the rulings that shaped it. All copy and facts are in `content.py`; nothing is hard coded in `build.py` except structure.

- Home hero: the whole 36 second film, uncut, opening on the pack in the field, looping seamlessly. Phones: full screen. Wide screens: a fixed 3D stage with three windows of real footage at three depths, mouse lean, glare, a blurred backdrop painted from the front video, the page slides up over it. Details in the README section "The hero".
- Under the hero: proof strip (4.8 on Google, 45 acres, cage free, since 2008), two doors (day and overnight), the film (scroll scrubbed on wide screens, a loop on phones), "Here is the day" (a swipe row on phones that opens on the current part of the day), reviews, prices (live from pricing.json), three free steps, Taylor and Hannah, the brothers panorama shown whole, Gracie at a glance, the closing call to action.
- 33 pages: home, day camp, overnight camp, rates, camp life, our story, faq, reviews, contact, spa, privacy, 404, and 22 ad landing pages with the old slugs so the keyword final URLs keep working. Indexed pages are in the sitemap; the pure town variants and offer pages carry noindex.

## Rulings from Ryan that must hold

No dashes anywhere a customer reads. Real photos, real reviews, real numbers only, never generated footage. Say what camp is, never what it is not. Toronto and GTA stay off the site. No "#1" claims, the real 4.8 is the claim. The one action is the free meet and greet, straight into `book.campcookstown.com/get-started`. Headline "Your dog's dream vacation." stays. Eyebrow "Cage free dog camp · Since 2008" stays. No image cropped so a dog loses a face; no image zoomed unless on purpose. The nav stays transparent over the hero. Holiday deposits are not refunded, said nicely. Rabies is the only vaccination requirement, not pushed. Gracie gets one honest line (she is an AI) and must read as someone who can answer absolutely anything, day or night. Logins, DNS and money are Ryan's fingers.

## Open at the end of this session

- Launch morning (Ryan present): add campcookstown.com to the Vercel project, switch DNS at Cloudflare, confirm no X-Robots-Tag noindex on the real domain (vercel.json only sets it on `*.vercel.app`), check the redirects, submit the sitemap, repoint the Google Ads sitelinks. Keyword final URLs need no change.
- The GitHub repo is public. Ryan was told how to make it private (Settings, Danger Zone, Change visibility). His call.
- Vercel deployment protection is on by default, so Dan cannot view the vercel.app site without a Vercel login; either turn protection off for this project or share the artifact previews.
- Still wanted: a real photo of Ryan and Dan for Our Story; a GTM container id (`GTM` in `content.py` is empty, so no tag manager loads yet).
- The old CMS pages at Whetham stay untouched until the DNS switch; the redirects in `out/vercel.json` cover the old URLs.

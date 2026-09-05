#!/usr/bin/env python3
"""Cut the hero loops, posters and the film assets from the 4K master.

Source: the 23 Aug 2026 4K upscale of Camp Cookstown (Real Hero)_4, 2160x3840, 30 fps, 36.1 s.
Memory safe: each scene is cut on its own first (fast seek), then the small intermediates are crossfaded.

Outputs (into OUT):
  hero-mobile.mp4    810x1440  the whole film, uncut, as a seamless loop (phones, full screen)
  hero-desktop.mp4   900x1600  the same, sharper, for the front window of the 3D stage on wide screens
  hero-poster.jpg / hero-poster-mobile.jpg   first frame of each
  pane-b.mp4 / pane-c.mp4  540x960  short loops of other scenes for the two back windows
  day-mobile.mp4     648x1152  the day loop for phones (field, hose, belly rub, nap), autoplay, 8.4 s
  film/d/NNN.webp   1200x676   desktop film frames, 8 fps, scrubbed by scroll

Seamless loops: the tail of the last scene is crossfaded into the head of the first, and the output is
trimmed so that its first and last frames are the same frame (see full() and pane()). The older scene cut
of the hero is still available as 'hero-cut'.
"""
import os, subprocess, sys, shutil

SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/cc/hero/hero4k.mp4'
OUT = sys.argv[2] if len(sys.argv) > 2 else '/home/claude/cc/hero/out'
TMP = os.path.join(OUT, '_tmp')
os.makedirs(TMP, exist_ok=True)
XF = 0.5

# (start, end, desktop crop y in 4K coords, name)
SCENES = {
    'rainbow': (0.10, 2.70, 2544),
    'field': (12.30, 15.80, 1150),
    'willow': (2.80, 5.40, 1950),
    'hose': (17.00, 19.00, 1150),
    'belly': (31.50, 35.90, 1150),
    'bellyrub': (20.00, 22.00, 1350),
    'nap': (9.00, 11.50, 1500),
    'golden': (28.70, 30.30, 1200),
}
HERO_ORDER = ['field', 'willow', 'hose', 'belly', 'rainbow']
FILM_ORDER = ['field', 'hose', 'bellyrub', 'nap']
DELOGO = 'delogo=x=690:y=550:w=780:h=110:show=0'


def run(cmd):
    print(' '.join(cmd)[:300]); sys.stdout.flush()
    subprocess.run(cmd, check=True)


def cut(name, s, e, mode, w, h, tag):
    out = os.path.join(TMP, f'{tag}-{name}-{s:.2f}-{e:.2f}.mp4')
    if os.path.exists(out):
        return out
    vf = []
    if name == 'rainbow':
        vf.append(DELOGO)
    if mode == 'crop':
        vf.append(f'crop=2160:1215:0:{SCENES[name][2]}')
    vf.append(f'scale={w}:{h}:flags=lanczos')
    vf += ['setsar=1', 'format=yuv420p']
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s:.3f}', '-to', f'{e:.3f}', '-i', SRC, '-vf', ','.join(vf),
         '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '12', '-r', '30', '-threads', '2', out])
    return out


def xfade(files, durs):
    inputs = []
    for f in files:
        inputs += ['-i', f]
    parts, prev, total = [], '[0:v]', durs[0]
    for i in range(1, len(files)):
        off = total - XF
        out = f'[x{i}]' if i < len(files) - 1 else '[vout]'
        parts.append(f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{out}')
        total = off + durs[i]
        prev = out
    return inputs, ';'.join(parts), total


def hero(mode, w, h, base, crf, maxrate, poster):
    r_s, r_e, _ = SCENES['rainbow']
    f_s, f_e, _ = SCENES['field']
    seq = [('rainbow', r_e - XF, r_e)] + [(n, SCENES[n][0], SCENES[n][1]) for n in HERO_ORDER] + [('field', f_s, f_s + XF)]
    files, durs = [], []
    for name, s, e in seq:
        files.append(cut(name, s, e, mode, w, h, base))
        durs.append(e - s)
    inputs, fc, total = xfade(files, durs)
    start = XF  # the first fade is complete here: a clean field frame
    mp4 = os.path.join(OUT, base + '.mp4')
    run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', fc, '-map', '[vout]', '-ss', f'{start:.3f}',
         '-an', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-crf', str(crf), '-maxrate', maxrate, '-bufsize', '3M',
         '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-r', '30', '-threads', '2', mp4])
    run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-frames:v', '1', '-q:v', '3', os.path.join(OUT, poster)])
    print('hero', base, 'bytes', os.path.getsize(mp4), 'duration about', round(total - start, 2)); sys.stdout.flush()


def probe_duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    return float(out)


def full(w, h, base, crf, maxrate, poster, start=SCENES['field'][0]):
    """The whole 36 second film, uncut, as a seamless loop that opens on the pack in the field.

    The master is scaled once (title text on the opening shot removed). The film is then rotated to begin at
    `start`: the part from `start` to the end plays first, its last half second dissolves into the opening
    rainbow shot, and the film runs on to `start` again, so the last frame is the first frame. Nothing is cut."""
    inter = os.path.join(TMP, f'full-{w}x{h}.mp4')
    if not os.path.exists(inter):
        run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-vf', f"{DELOGO}:enable='between(t,0,2.75)',scale={w}:{h}:flags=lanczos,setsar=1,format=yuv420p",
             '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '12', '-r', '30', '-threads', '2', inter])
    dur = probe_duration(inter)
    a = os.path.join(TMP, f'full-a-{w}x{h}-{start:.2f}.mp4')
    b = os.path.join(TMP, f'full-b-{w}x{h}-{start:.2f}.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{start:.3f}', '-i', inter, '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '12', '-r', '30', '-threads', '2', a])
    run(['ffmpeg', '-v', 'error', '-y', '-i', inter, '-t', f'{start + XF:.3f}', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '12', '-r', '30', '-threads', '2', b])
    la = probe_duration(a)
    mp4 = os.path.join(OUT, base + '.mp4')
    fc = f'[0:v][1:v]xfade=transition=fade:duration={XF}:offset={la - XF:.3f}[vout]'
    total = la - XF + start  # ends on the frame it started on
    run(['ffmpeg', '-v', 'error', '-y', '-i', a, '-i', b, '-filter_complex', fc, '-map', '[vout]', '-t', f'{total:.3f}',
         '-an', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-crf', str(crf), '-maxrate', maxrate, '-bufsize', '4M',
         '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-r', '30', '-threads', '2', mp4])
    run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-frames:v', '1', '-q:v', '3', os.path.join(OUT, poster)])
    print('full', base, 'bytes', os.path.getsize(mp4), 'duration about', round(total, 2)); sys.stdout.flush()


def pane(order, base, w, h, crf, maxrate, poster=None):
    """A small seamless loop of a few scenes: last scene tail, the scenes, first scene head, crossfaded, so the
    first and last frames are the same frame. Used for the two back windows of the desktop hero and the phone
    film loop."""
    l_s, l_e, _ = SCENES[order[-1]]
    f_s, f_e, _ = SCENES[order[0]]
    seq = [(order[-1], l_e - XF, l_e)] + [(n, SCENES[n][0], SCENES[n][1]) for n in order] + [(order[0], f_s, f_s + XF)]
    files, durs = [], []
    for name, s, e in seq:
        files.append(cut(name, s, e, 'full', w, h, base))
        durs.append(e - s)
    inputs, fc, total = xfade(files, durs)
    mp4 = os.path.join(OUT, base + '.mp4')
    run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', fc, '-map', '[vout]', '-ss', f'{XF:.3f}',
         '-an', '-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-crf', str(crf), '-maxrate', maxrate, '-bufsize', '2M',
         '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-r', '30', '-threads', '2', mp4])
    run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-frames:v', '1', '-q:v', '4', os.path.join(OUT, poster or (base + '-poster.jpg'))])
    print('pane', base, 'bytes', os.path.getsize(mp4), 'duration about', round(total - XF, 2)); sys.stdout.flush()


def film_frames(w, h, q, final_scale):
    files, durs = [], []
    for n in FILM_ORDER:
        s, e, _ = SCENES[n]
        files.append(cut(n, s, e, 'crop', w, h, 'film-d'))
        durs.append(e - s)
    inputs, fc, total = xfade(files, durs)
    d = os.path.join(OUT, 'film', 'd')
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', fc + f';[vout]fps=8,scale={final_scale}:flags=lanczos[f]', '-map', '[f]',
         '-c:v', 'libwebp', '-lossless', '0', '-quality', str(q), '-compression_level', '6', '-threads', '2', os.path.join(d, '%03d.webp')])
    fs = sorted(os.listdir(d))
    print('film d', len(fs), 'frames', sum(os.path.getsize(os.path.join(d, f)) for f in fs) // 1024, 'KB', 'duration', round(total, 2)); sys.stdout.flush()


def day_loop(w, h, crf, maxrate):
    pane(FILM_ORDER, 'day-mobile', w, h, crf, maxrate, poster='day-poster-mobile.jpg')


if __name__ == '__main__':
    what = sys.argv[3] if len(sys.argv) > 3 else 'all'
    if what in ('all', 'hero'):
        full(810, 1440, 'hero-mobile', 31, '1200k', 'hero-poster-mobile.jpg')
        full(900, 1600, 'hero-desktop', 29, '1900k', 'hero-poster.jpg')
    if what == 'hero-cut':
        hero('full', 810, 1440, 'hero-mobile', 30, '1400k', 'hero-poster-mobile.jpg')
        hero('full', 1080, 1920, 'hero-desktop', 28, '3500k', 'hero-poster.jpg')
    if what in ('all', 'film'):
        film_frames(1440, 810, 54, '1200:676')
    if what in ('all', 'film', 'day'):
        day_loop(648, 1152, 30, '1200k')
    if what in ('all', 'panes'):
        pane(['hose', 'bellyrub', 'golden'], 'pane-b', 540, 960, 30, '900k')
        pane(['nap', 'belly', 'willow'], 'pane-c', 540, 960, 30, '900k')
    print('ALL DONE')

#!/usr/bin/env python3
"""Turns an animated GIF into a transparent sprite sheet for an animated header.

    python scripts/frames.py input.gif data/portrait-sheet.png [--bg white|black|none] [--tolerance 18]

Writes the sheet (frames side by side, same size) and a JSON next to it with the frame size and
durations; point "portrait_frames" in profile.json at that JSON. The background is removed by
flood-filling from the image border, so a solid background that touches the edges goes away while
the same color inside the outline (eyes, highlights) stays. Needs Pillow.
"""
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageSequence

BG = {"white": (255, 255, 255), "black": (0, 0, 0)}


def clear_background(frame, color, tolerance):
    """Make the border-connected region close to `color` transparent."""
    rgba = frame.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size

    def near(p):
        return all(abs(a - b) <= tolerance for a, b in zip(p[:3], color))

    stack = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    seen = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add((x, y))
        if near(px[x, y]):
            px[x, y] = (0, 0, 0, 0)
            stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return rgba


def detect_block(frame):
    """Size of the square blocks of upscaled pixel art: the gcd of the color run lengths.

    Sampled rows and columns; the first and last run of each line are skipped because the image
    border may cut them. Returns 1 for anything that is not cleanly upscaled.
    """
    w, h = frame.size
    px = frame.load()
    g = 0
    lines = [[px[x, y] for x in range(w)] for y in range(0, h, max(1, h // 24))]
    lines += [[px[x, y] for y in range(h)] for x in range(0, w, max(1, w // 24))]
    for line in lines:
        runs, n = [], 1
        for a, b in zip(line, line[1:]):
            if a == b:
                n += 1
            else:
                runs.append(n)
                n = 1
        for r in runs[1:]:  # runs[0] touches the border
            g = math.gcd(g, r)
            if g == 1:
                return 1
    return g or 1


def fade_sides(frame, share):
    """Fade the alpha towards the left and right edges (where a figure is cut by the image border)."""
    alpha = frame.getchannel("A")
    w, h = frame.size
    edge = max(1, round(w * share))
    px = alpha.load()
    for x in range(edge):
        k = ((x + 1) / edge) ** 1.5
        for xx in (x, w - 1 - x):
            for y in range(h):
                px[xx, y] = round(px[xx, y] * k)
    frame.putalpha(alpha)
    return frame


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src")
    ap.add_argument("dst", help="output PNG; the JSON gets the same name with .json")
    ap.add_argument("--bg", default="white", choices=["white", "black", "none"])
    ap.add_argument("--tolerance", type=int, default=18)
    ap.add_argument("--height", type=int, default=0,
                    help="target frame height, about 2x the displayed size (pixel art: nearest whole factor)")
    ap.add_argument("--colors", type=int, default=128, help="palette size of the PNG (0 keeps full color; pixel art needs few)")
    ap.add_argument("--native", default="1",
                    help="pixel-art block size: shrink by this factor first (exact, no smoothing; also much faster). "
                         "'auto' detects it")
    ap.add_argument("--scale", type=int, default=1, help="enlarge by this whole factor at the end, without smoothing")
    ap.add_argument("--fade-sides", type=float, default=0,
                    help="share of the width faded on each side, for figures cut by the image edges")
    args = ap.parse_args()

    gif = Image.open(args.src)
    native = detect_block(gif.convert("RGB")) if args.native == "auto" else int(args.native)
    if args.native == "auto":
        print(f"pixel-art block size: {native}" + (" (not upscaled pixel art)" if native == 1 else ""))
    frames, durations = [], []
    for f in ImageSequence.Iterator(gif):
        durations.append(f.info.get("duration") or 100)
        f = f.convert("RGBA")
        if native > 1:  # upscaled pixel art: one sample per block recovers the original pixels
            f = f.resize((f.width // native, f.height // native), Image.NEAREST)
        frames.append(clear_background(f, BG[args.bg], args.tolerance) if args.bg != "none" else f)

    # Crop every frame to the union of their visible areas, so the sprite keeps its position
    box = None
    for f in frames:
        b = f.getchannel("A").getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    frames = [f.crop(box) for f in frames]
    if args.height and native > 1:  # pixel art: closest whole factor, no smoothing
        k = max(1, round(args.height / frames[0].height))
        frames = [f.resize((f.width * k, f.height * k), Image.NEAREST) for f in frames]
    elif args.height and args.height < frames[0].height:  # smaller sheet: the SVG inlines it as base64
        size = (round(frames[0].width * args.height / frames[0].height), args.height)
        frames = [f.resize(size, Image.LANCZOS) for f in frames]
    if args.scale > 1:
        frames = [f.resize((f.width * args.scale, f.height * args.scale), Image.NEAREST) for f in frames]
    if args.fade_sides > 0:  # after scaling, so the fade is smooth instead of one step per art pixel
        frames = [fade_sides(f, args.fade_sides) for f in frames]
    fw, fh = frames[0].size

    sheet = Image.new("RGBA", (fw * len(frames), fh), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * fw, 0))
    if args.colors:  # resizing creates thousands of in-between colors; a palette brings the size back down
        sheet = sheet.quantize(args.colors, method=Image.Quantize.FASTOCTREE)
    sheet.save(args.dst, optimize=True)

    meta = {"frame_w": fw, "frame_h": fh, "durations": durations}
    Path(args.dst).with_suffix(".json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    print(f"{args.dst}: {len(frames)} frames of {fw}x{fh}, {sum(durations)} ms per loop, {Path(args.dst).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

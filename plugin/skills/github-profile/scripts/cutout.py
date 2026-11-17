#!/usr/bin/env python3
"""Removes a dark background from an illustration and saves a transparent WebP for the header.

    python scripts/cutout.py input.png data/portrait.webp [--threshold 16] [--fade-left 0.18]

Built for dot-matrix / pixel-art images on a black background, where a plain threshold would
punch holes between the dots: the image is blurred so the dots merge, small gaps are closed,
enclosed holes are filled and loose specks (stars) are removed. Needs Pillow and numpy.
"""
import argparse

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--threshold", type=int, default=16, help="brightness that counts as figure after blurring")
    ap.add_argument("--fade-left", type=float, default=0.18, help="share of the width faded on the left (0 to disable)")
    ap.add_argument("--height", type=int, default=560, help="output height in px (about 2x the displayed size)")
    args = ap.parse_args()

    im = Image.open(args.src).convert("RGB")
    arr = np.asarray(im).astype(np.int16)

    # Brightest channel, blurred so the LED dots merge with the black gaps between them
    lum = Image.fromarray(arr.max(axis=2).astype(np.uint8))
    mask = lum.filter(ImageFilter.GaussianBlur(7)).point(lambda v: 255 if v > args.threshold else 0)
    # Closing joins dark parts of the figure (clothes, chair) with the rest
    mask = mask.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))
    # Fill enclosed holes: whatever cannot be reached from the top corners is figure
    inv = mask.point(lambda v: 0 if v else 255)
    ImageDraw.floodfill(inv, (0, 0), 128)
    ImageDraw.floodfill(inv, (inv.width - 1, 0), 128)
    mask = inv.point(lambda v: 0 if v == 128 else 255)
    # Opening removes loose specks of the background
    mask = mask.filter(ImageFilter.MinFilter(21)).filter(ImageFilter.MaxFilter(21))

    rgba = im.copy()
    rgba.putalpha(mask.filter(ImageFilter.GaussianBlur(2)))
    rgba = rgba.crop(mask.getbbox())
    if args.fade_left > 0:  # scenes often run straight into the left edge
        a = np.asarray(rgba.getchannel("A")).astype(np.float32)
        ramp = np.clip(np.linspace(0, 1 / args.fade_left, a.shape[1]), 0, 1) ** 1.5
        rgba.putalpha(Image.fromarray((a * ramp[None, :]).astype(np.uint8)))

    out = rgba.resize((round(rgba.width * args.height / rgba.height), args.height), Image.LANCZOS)
    out.save(args.dst, "WEBP", quality=86, method=6)
    print(f"{args.dst}: {out.size[0]}x{out.size[1]}")


if __name__ == "__main__":
    main()

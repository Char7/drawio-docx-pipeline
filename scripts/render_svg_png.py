#!/usr/bin/env python3
"""Rasterize an already valid white/light SVG to PNG (does NOT parse draw.io directly)."""
import argparse
import sys
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("svg", type=Path, help="Already exported/verified SVG from a capable renderer")
    p.add_argument("png", type=Path)
    p.add_argument("--scale", type=float, default=2.0)
    a = p.parse_args()
    if a.scale <= 0:
        p.error("--scale must be greater than zero")
    if a.svg.resolve() == a.png.resolve():
        p.error("input SVG and output PNG must differ")
    try:
        import cairosvg
    except ImportError:
        print("CairoSVG unavailable. Use a real graphics renderer such as FigCraft or Inkscape.", file=sys.stderr)
        return 3
    try:
        cairosvg.svg2png(url=str(a.svg), write_to=str(a.png),
                         background_color="#FFFFFF", scale=a.scale)
        print(f"Created {a.png}; VERIFY ACTUAL PNG pixels, fonts and A4 layout before use")
        return 0
    except Exception as exc:
        print(f"SVG export failed: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())

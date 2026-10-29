#!/usr/bin/env python3
"""Check actual exported PNG opacity/white margins; still perform a human visual QA."""
import argparse
import json
import sys
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("image", type=Path)
    p.add_argument("--min-width", type=int, default=1200)
    p.add_argument("--no-corner-check", action="store_true", help="For intentional edge-to-edge artwork")
    a = p.parse_args()
    try:
        from PIL import Image
    except ImportError:
        print("Pillow not installed: pip install Pillow", file=sys.stderr)
        return 3
    try:
        with Image.open(a.image) as im:
            im.load()
            original_format = im.format
            rgb = im.convert("RGBA")
            w, h = rgb.size
            alpha = rgb.getchannel("A").getextrema()
            offset = min(4, (w - 1) // 2, (h - 1) // 2)
            positions = [(offset, offset), (w-1-offset, offset),
                         (offset, h-1-offset), (w-1-offset, h-1-offset)]
            corners = [rgb.getpixel(pos) for pos in positions]
            white = all(min(pixel[:3]) >= 245 and pixel[3] == 255 for pixel in corners)
            errors = []
            if original_format != "PNG":
                errors.append("not a PNG")
            if w < a.min_width:
                errors.append(f"width {w} below requested {a.min_width}")
            if alpha != (255, 255):
                errors.append("transparent pixels detected")
            if not a.no_corner_check and not white:
                errors.append("corners are not opaque white (inspect manually if edge-to-edge)")
            report = {"file": str(a.image), "format": original_format, "width": w,
                      "height": h, "alpha_min_max": alpha, "corner_rgba": corners,
                      "opaque_white_corners": white, "errors": errors,
                      "note": "Pixel checks do not validate fonts, labels, arrow semantics or A4 print quality"}
            print(json.dumps(report, indent=2))
            return 2 if errors else 0
    except (OSError, ValueError) as exc:
        print(f"Failed: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Export draw.io XML to PNG via the draw.io Desktop CLI (not Computer Use)."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--drawio", help="Path to draw.io Desktop executable; otherwise search PATH")
    parser.add_argument("--scale", type=float, default=2.0)
    parser.add_argument("--border", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=150)
    args = parser.parse_args(argv)
    try:
        if not args.source.is_file() or args.source.suffix.lower() != ".drawio":
            raise ValueError("source must exist and have a .drawio extension")
        if args.output.exists():
            raise ValueError("refusing to overwrite an existing PNG")
        if args.output.suffix.lower() != ".png":
            raise ValueError("output must end in .png")
        if not 0.5 <= args.scale <= 6 or not 0 <= args.border <= 100:
            raise ValueError("invalid scale or border")
        exe = args.drawio or shutil.which("drawio") or shutil.which("draw.io")
        if not exe:
            raise ValueError("draw.io Desktop CLI not found: provide --drawio. Never silently start Computer Use.")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        cmd = [str(exe), "--export", "--format", "png", "--output", str(args.output),
               "--border", str(args.border), "--scale", str(args.scale), str(args.source)]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=args.timeout)
        if result.returncode != 0 or not args.output.is_file() or args.output.stat().st_size == 0:
            raise ValueError(f"draw.io Desktop CLI failed (exit {result.returncode}): {result.stderr[-800:]}")
        print(json.dumps({"status": "EXPORTED__PIXEL_AND_WORD_QA_PENDING",
                          "output": str(args.output), "size_bytes": args.output.stat().st_size,
                          "renderer": "draw.io Desktop CLI, no GUI automation"}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

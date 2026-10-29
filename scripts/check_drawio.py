#!/usr/bin/env python3
"""Inspect editable diagrams.net/draw.io XML (including compressed <diagram> payloads)."""
import argparse
import base64
import json
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

IMAGE_RX = re.compile(r"(?:^|;)image=([^;]*)")

def graph_models(root):
    if root.tag == "mxGraphModel":
        return [root]
    if root.tag != "mxfile":
        raise ValueError("Expected <mxfile> or <mxGraphModel>")
    models = []
    for diagram in root.findall("diagram"):
        model = diagram.find("mxGraphModel")
        if model is not None:
            models.append(model)
            continue
        payload = (diagram.text or "").strip()
        if not payload:
            continue
        data = base64.b64decode(payload)
        text = zlib.decompress(data, -15).decode("utf-8")
        models.append(ET.fromstring(urllib.parse.unquote(text)))
    return models

def inspect(path):
    root = ET.parse(path).getroot()
    models = graph_models(root)
    reports = []
    for graph in models:
        cells = list(graph.iter("mxCell"))
        nodes = [c for c in cells if c.get("vertex") == "1"]
        edges = [c for c in cells if c.get("edge") == "1"]
        backgrounds = graph.get("background", "")
        external = []
        embedded_count = 0
        for node in nodes:
            m = IMAGE_RX.search(node.get("style", ""))
            if not m:
                continue
            val = urllib.parse.unquote(m.group(1))
            if val.startswith("data:image/"):
                embedded_count += 1
            else:
                external.append(val[:200])
        reports.append({
            "background": backgrounds, "white_background": backgrounds.upper() in ("#FFFFFF", "WHITE"),
            "vertices": len(nodes), "edges": len(edges), "embedded_image_vertices": embedded_count,
            "external_image_references": external,
            "contains_thai": any(any("\u0e00" <= c <= "\u0e7f" for c in (n.get("value") or "")) for n in nodes),
        })
    return {"file": str(path), "diagram_count": len(reports), "diagrams": reports}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--require-white", action="store_true")
    args = parser.parse_args()
    try:
        report = inspect(args.source)
        errors = []
        if not report["diagrams"]:
            errors.append("no readable graph model")
        for i, d in enumerate(report["diagrams"], 1):
            if not d["vertices"]:
                errors.append(f"diagram {i} has no editable vertices")
            if args.require_white and not d["white_background"]:
                errors.append(f"diagram {i} lacks explicit white #FFFFFF background")
        report["errors"] = errors
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2 if errors else 0
    except (OSError, ValueError, ET.ParseError, zlib.error) as exc:
        print(json.dumps({"file": str(args.source), "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())

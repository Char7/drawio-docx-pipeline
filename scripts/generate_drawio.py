#!/usr/bin/env python3
"""Generate editable diagrams.net .drawio XML from a JSON figure specification.

Standard-library only. No browser, GUI automation, or Computer Use.
After generation, export through draw.io Desktop CLI and visually inspect
the PNG; successful XML generation alone is not a visual QA PASS.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
CELL_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,79}$")
IMAGE_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
MAX_IMAGE_BYTES = 16 * 1024 * 1024


class SpecError(ValueError):
    """Invalid figure specification or graph topology."""


def positive(value, name, allow_zero=False):
    if type(value) not in (int, float) or value < 0 or (value == 0 and not allow_zero) or value > 100000:
        raise SpecError(f"{name} must be a positive number within range")
    return value


def color(value, name):
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise SpecError(f"{name} must be #RRGGBB")
    return value


def valid_id(value):
    if not isinstance(value, str) or not CELL_ID.fullmatch(value) or value in ("0", "1"):
        raise SpecError(f"Invalid cell ID: {value!r}")
    return value


def label(text):
    if not isinstance(text, str) or len(text) > 3000:
        raise SpecError("label must be text up to 3000 characters")
    return html.escape(text).replace("\n", "<br/>")


def add_geometry(cell, obj):
    attrs = {key: str(positive(obj[key], key, key in ("x", "y")))
             for key in ("x", "y", "width", "height")}
    ET.SubElement(cell, "mxGeometry", {**attrs, "as": "geometry"})


def embedded_image(path):
    suffix = path.suffix.lower()
    if suffix not in IMAGE_MIME or not path.is_file() or path.stat().st_size > MAX_IMAGE_BYTES:
        raise SpecError(f"Missing, oversized, or unsupported image: {path}")
    data = path.read_bytes()
    if not data or suffix == ".png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SpecError(f"Invalid PNG: {path}")
    if suffix in (".jpg", ".jpeg") and not data.startswith(b"\xff\xd8\xff"):
        raise SpecError(f"Invalid JPEG: {path}")
    return IMAGE_MIME[suffix], base64.b64encode(data).decode("ascii"), hashlib.sha256(data).hexdigest()


def make_drawio(spec, spec_path):
    if not isinstance(spec, dict):
        raise SpecError("JSON root must be an object")
    page = spec.get("page", {})
    if not isinstance(page, dict):
        raise SpecError("page must be an object")
    width = positive(page.get("width", 900), "page.width")
    height = positive(page.get("height", 600), "page.height")
    if min(width, height) < 100:
        raise SpecError("page must be at least 100 x 100")
    background = color(page.get("background", "#FFFFFF"), "background")
    title = spec.get("title", "Diagram")
    if not isinstance(title, str) or not 1 <= len(title) <= 100:
        raise SpecError("title must be 1-100 characters")
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    if not isinstance(nodes, list) or not nodes or len(nodes) > 500 or not isinstance(edges, list) or len(edges) > 1000:
        raise SpecError("invalid nodes/edges list size")

    xml = ET.Element("mxfile", {"host": "app.diagrams.net", "agent": "drawio-docx-pipeline/programmatic", "type": "device"})
    diagram = ET.SubElement(xml, "diagram", {"id": "generated-diagram", "name": title})
    model = ET.SubElement(diagram, "mxGraphModel", {
        "grid": "1", "gridSize": "10", "guides": "1", "connect": "1",
        "arrows": "1", "page": "1", "pageScale": "1",
        "pageWidth": str(width), "pageHeight": str(height), "background": background
    })
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    seen, assets = set(), []

    for n in nodes:
        if not isinstance(n, dict):
            raise SpecError("Each node must be an object")
        uid = valid_id(n.get("id"))
        if uid in seen:
            raise SpecError(f"Duplicate node ID: {uid}")
        seen.add(uid)
        kind = n.get("kind", "box")
        if kind not in ("box", "text", "image"):
            raise SpecError(f"Unsupported node kind: {kind}")
        for key in ("x", "y", "width", "height"):
            if key not in n:
                raise SpecError(f"{uid} missing {key}")
        if n["x"] + n["width"] > width or n["y"] + n["height"] > height:
            raise SpecError(f"{uid} exceeds page bounds")
        if kind == "image":
            name = n.get("path")
            if not isinstance(name, str) or not name:
                raise SpecError(f"Image node {uid} requires path")
            asset = Path(name)
            if not asset.is_absolute():
                asset = spec_path.parent / asset
            mime, encoded, digest = embedded_image(asset)
            style = f"shape=image;html=1;imageAspect=1;aspect=fixed;strokeColor=none;image=data:{mime},{encoded};"
            value = ""
            assets.append({"node_id": uid, "name": asset.name, "sha256": digest})
        else:
            value = label(n.get("label", ""))
            font = n.get("font_family", spec.get("font_family", "Arial"))
            if not isinstance(font, str) or len(font) > 70 or any(x in font for x in (";", "=", "\n")):
                raise SpecError("Invalid font family")
            size = n.get("font_size", 22)
            if type(size) is not int or not 7 <= size <= 80:
                raise SpecError("font_size must be an integer from 7 to 80")
            align = n.get("align", "center")
            if align not in ("left", "center", "right"):
                raise SpecError("align must be left/center/right")
            ink = color(n.get("font_color", "#183451"), "font_color")
            if kind == "text":
                style = "text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;"
            else:
                fill = color(n.get("fill", "#EFF6FF"), "fill")
                stroke = color(n.get("stroke", "#477DB3"), "stroke")
                style = f"rounded=1;arcSize=16;html=1;whiteSpace=wrap;fillColor={fill};strokeColor={stroke};strokeWidth=2;"
            style += (f"fontFamily={font};fontSize={size};fontColor={ink};fontStyle={1 if n.get('bold', False) else 0};"
                      f"align={align};verticalAlign=middle;")
        cell = ET.SubElement(root, "mxCell", {"id": uid, "value": value, "style": style, "vertex": "1", "parent": "1"})
        add_geometry(cell, n)

    node_ids = set(seen)
    for edge in edges:
        if not isinstance(edge, dict):
            raise SpecError("Each edge must be an object")
        uid = valid_id(edge.get("id"))
        src, dst = edge.get("source"), edge.get("target")
        if uid in seen or src not in node_ids or dst not in node_ids:
            raise SpecError(f"Edge {uid} duplicates an ID or refers to a missing vertex")
        if src == dst and not edge.get("allow_loop", False):
            raise SpecError(f"Edge {uid} is a loop without allow_loop")
        seen.add(uid)
        arrow = edge.get("arrow", "block")
        if arrow not in ("block", "none", "open"):
            raise SpecError("Invalid arrow type")
        ink = color(edge.get("stroke", "#64748B"), "edge.stroke")
        thickness = positive(edge.get("width", 3), "edge.width")
        style = (f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor={ink};"
                 f"strokeWidth={thickness};endArrow={arrow};endFill=1;")
        for field in ("exit", "entry"):
            point = edge.get(field)
            if point is not None:
                if not isinstance(point, list) or len(point) != 2 or any(type(x) not in (int, float) or not 0 <= x <= 1 for x in point):
                    raise SpecError(f"Edge {uid} {field} anchor must be [x,y] in [0,1]")
                style += f"{field}X={point[0]};{field}Y={point[1]};{field}Dx=0;{field}Dy=0;"
        cell = ET.SubElement(root, "mxCell", {
            "id": uid, "style": style, "edge": "1", "parent": "1", "source": src, "target": dst
        })
        ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})

    result = b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(xml, encoding="utf-8") + b"\n"
    evidence = {"nodes": len(nodes), "edges": len(edges), "embedded_assets": assets,
                "explicit_white_background": background.upper() == "#FFFFFF"}
    return result, evidence


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.output.suffix.lower() != ".drawio":
            raise SpecError("Output must end in .drawio")
        if args.output.exists() or args.manifest and args.manifest.exists():
            raise SpecError("Refusing to overwrite existing .drawio or manifest")
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        data, evidence = make_drawio(spec, args.spec.resolve())
        ET.fromstring(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as target:
            target.write(data)
        evidence.update({"drawio": str(args.output), "source_spec": str(args.spec),
                         "drawio_sha256": hashlib.sha256(data).hexdigest(),
                         "status": "SOURCE_GENERATED__NATIVE_EXPORT_AND_VISUAL_QA_PENDING"})
        if args.manifest:
            args.manifest.parent.mkdir(parents=True, exist_ok=True)
            with args.manifest.open("x", encoding="utf-8") as target:
                json.dump(evidence, target, ensure_ascii=False, indent=2)
                target.write("\n")
        print(json.dumps(evidence, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, ET.ParseError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

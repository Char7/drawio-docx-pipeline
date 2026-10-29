#!/usr/bin/env python3
"""Read-only basic DOCX OOXML structure audit; Word visual/font QA is still required."""
import argparse
import json
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("document", type=Path)
    a = p.parse_args()
    try:
        with zipfile.ZipFile(a.document) as z:
            if "word/document.xml" not in z.namelist():
                raise ValueError("Missing word/document.xml")
            doc = ET.fromstring(z.read("word/document.xml"))
            paragraphs = list(doc.iter(W + "p"))
            texts = ["".join(t.text or "" for t in para.iter(W + "t")) for para in paragraphs]
            table_count = len(list(doc.iter(W + "tbl")))
            fonts = set()
            for node in doc.iter(W + "rFonts"):
                for key in ("ascii", "hAnsi", "eastAsia", "cs"):
                    val = node.get(W + key)
                    if val:
                        fonts.add(val)
            secs = list(doc.iter(W + "pgSz"))
            pages = [node.attrib for node in secs]
            media = [n for n in z.namelist() if n.startswith("word/media/") and not n.endswith("/")]
            result = {"file": str(a.document), "paragraphs": len(paragraphs),
                      "sample_text": [t[:120] for t in texts if t.strip()][:8],
                      "tables": table_count, "media": len(media),
                      "fonts_directly_referenced": sorted(fonts),
                      "page_size_elements": pages,
                      "warning": "This does NOT verify installed font/substitution, rendering or print preview."}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(json.dumps({"file": str(a.document), "error": str(exc)}), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())

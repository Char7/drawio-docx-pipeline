# Programmatic draw.io authoring — DEFAULT (no Computer Use)

## Mandatory priority for agents

**For new diagrams, use code-first authoring before any graphical-interface workflow.**
The standard path is **FIG-SPEC → JSON → Python → editable uncompressed mxGraph XML (.drawio) → draw.io Desktop CLI PNG export → visual/Word QA**.

Do **not** launch diagrams.net in a browser and drag shapes with mouse actions, click Save repeatedly, or use generic Computer Use merely to construct diagrams. A browser login is not needed for programmatic generation. The web editor is for optional human edits and approved exceptional cases.

This rule applies to **diagram authoring**, not manual inspection. Use the Desktop **command-line exporter**, not GUI clicking. If unavailable, report BLOCKED_NATIVE_EXPORT and choose another explicitly supported non-GUI renderer only when suitable; **never silently switch to Computer Use**. GUI editing requires the user's explicit request or approval when programmatic features are insufficient.

## Architecture

1. Read the host project's FIG-SPEC, approved design rules, Figure ID and stored sources. Reuse suitable approved assets. Apply FIG-0A scope before new AI image generations.
2. Create JSON with page dimensions, editable boxes/text, exact source/target edges, exit/entry anchors and optional standalone **text-free** image assets.
3. Generate .drawio using scripts/generate_drawio.py. Standard-library ElementTree produces mxfile / diagram / mxGraphModel / mxCell / mxGeometry. A PNG/JPEG asset is embedded as Base64 (image cell), while text and arrows remain editable graph cells. Duplicate IDs, missing endpoints, out-of-page geometry and overwrites are rejected.
4. Export each version using scripts/export_drawio_cli.py (draw.io Desktop command line), not screen control. Keep .drawio and PNG versions, hashes and cloud File ID (when storing via Google Drive).
5. Inspect **actual exported PNG pixels** for opaque white background, Thai tones/vowels, readable wrapping, connector endpoints, intended arrow semantics and no overlap. Use scripts/check_png.py if Pillow exists. XML parsing and export exit 0 alone do not prove visual correctness.
6. Insert approved PNG into an editable Word document using OfficeCLI or an equivalent approved document pipeline. Keep paragraphs and tables native. Inspect all pages with real Word engine and A4 portrait when the host requires it.
7. Store Figure ID → .drawio source → PNG → Word file → QA evidence mapping. Save superseded versions in backups; never overwrite approved DOCX. A human-edited .drawio needs re-export and replacement in a new Word version.

## Runnable example

From the repository root (Python 3.10+; standard library for authoring):

~~~bash
python scripts/generate_drawio.py examples/programmatic-three-steps.json output/FIG01_v01.drawio --manifest output/FIG01_v01.source.json
python scripts/check_drawio.py output/FIG01_v01.drawio --require-white
python scripts/export_drawio_cli.py output/FIG01_v01.drawio output/FIG01_v01.png --drawio "/path/to/draw.io" --scale 2 --border 8
python scripts/check_png.py output/FIG01_v01.png --min-width 1600
python -m unittest discover -s scripts -p "test_*.py"
~~~

On Windows PowerShell, change only the executable path (example):

~~~powershell
python scripts/generate_drawio.py examples/programmatic-three-steps.json .\output\FIG01_v01.drawio --manifest .\output\FIG01_v01.json
python scripts/export_drawio_cli.py .\output\FIG01_v01.drawio .\output\FIG01_v01.png --drawio "C:\Program Files\draw.io\draw.io.exe" --scale 2
~~~

Use new filenames v02, v03, etc. for subsequent edits. The scripts refuse to overwrite outputs. If CLI rendering cannot be completed, mark export/visual QA PENDING, not PASS.

## JSON structure

~~~json
{
  "title": "ตัวอย่างความสัมพันธ์",
  "page": {"width": 900, "height": 480, "background": "#FFFFFF"},
  "font_family": "TH SarabunPSK",
  "nodes": [
    {"id": "a", "kind": "box", "label": "เริ่มต้น", "x": 60, "y": 150, "width": 240, "height": 100, "fill": "#EAF3FF", "stroke": "#3979C6"},
    {"id": "b", "kind": "box", "label": "สิ้นสุด", "x": 590, "y": 150, "width": 240, "height": 100},
    {"id": "picture", "kind": "image", "path": "assets/subject.png", "x": 370, "y": 290, "width": 120, "height": 120}
  ],
  "edges": [
    {"id": "a_to_b", "source": "a", "target": "b", "exit": [1, 0.5], "entry": [0, 0.5], "arrow": "block"}
  ]
}
~~~

The kind is box, text or image. The image path is relative to the spec file unless absolute; its bytes are embedded and its local location is not stored in the generated .drawio. Exit/entry anchors use the 0..1 normalized coordinate range: left-top [0,0], right-center [1,0.5]. For biological figures, visually inspect whether each anchor reaches the correct organ/label.

## Scope and safe fallback

- This is a simple editable, uncompressed, single-page generator for boxes, text, PNG/JPEG image vertices and orthogonal connectors. It does not implement every arbitrary draw.io feature.
- **Source XML passes structural checks** but not automatically font rendering, scientific semantics or connector visual alignment. Fix bad anchors after inspecting the exported pixels.
- The Desktop CLI is native software invoked non-interactively; **it is not Computer Use**. It might still fail on a GUI-less or restricted machine. Record the actual failure and do not claim export success.
- Do not commit private source images, student data, copyrighted user documents, credentials or fonts into this public skill repository.
- Keep SOURCE_XML_PASS, NATIVE_EXPORT_PASS, VISUAL_QA_PASS and DOCX_WORD_QA_PASS distinct; user approval remains separate.

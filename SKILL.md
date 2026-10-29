---
name: drawio-docx-pipeline
description: Create editable draw.io diagrams with opaque white backgrounds, export print-ready PNGs, insert them into editable DOCX documents, and validate the results. Use for mind maps, science diagrams, flowcharts, teaching notes, and other figure-rich Word documents.
---

# Draw.io → PNG → DOCX pipeline

## Goal
Produce **two kinds of editable deliverables**: an original `.drawio` file for editing diagram elements, and a `.docx` file with editable body text/tables. The inserted diagram is a **raster PNG** and its individual labels/arrows are **not** editable inside Word. Keep the diagram source paired with the DOCX.

## Preconditions
1. Read the host project's rules, destination directory guide, prior QA results, and input sources. Preserve originals and make backups before editing.
2. Confirm that a real draw.io / diagrams.net editor, Word editor or OfficeCLI/WordCraft equivalent, and SVG/PNG export route are actually available. Tool discovery is **not proof** of functionality.
3. For factual/scientific content, verify the requested indicator, terminology, numerical relationships, arrow directions, and visual semantics from authorized sources; never silently invent textbook claims.
4. Never commit private source material, credentials, personal files, or licensed fonts into a public skill repository.

## Workflow
1. **Figure specification.** Record a stable Figure ID, purpose, audience, source references, labels, intended relations, print size, and science/visual QA criteria. Use [the FIG-SPEC template](references/fig-spec-template.md).
2. **Prepare optional imagery.** If a scene/object illustration is needed, generate a **text-free source image** first. Import/embed it into draw.io; add labels/arrows/symbols only after import. Prefer drawn, precise symbols for wiring, graphs, scales, rays, and other exact relationships.
3. **Author in draw.io.** Use an explicitly **opaque white canvas** (`#FFFFFF`) and editable shapes, connectors, and labels. Save `<Figure_ID>.drawio`. Reopen the file to confirm actual editability. See [workflow details](references/workflow.md).
4. **Export print-ready PNG.** Prefer native diagrams.net **PNG export with transparent background OFF and appearance LIGHT**; aim for 2×–3× or at least ~300 dpi at the intended physical size. **Visually inspect the exported pixels**, not just the XML background attribute. If the native export is dark/incorrect or unavailable, use a **trusted white-background SVG export** followed by a renderer such as FigCraft, Inkscape, or the optional `scripts/render_svg_png.py`; do not assume a simple draw.io XML-to-SVG script supports arbitrary diagrams or embedded imagery.
5. **Validate the PNG.** Run `scripts/check_png.py` when Pillow is available. Ensure the image is opaque/white at its margins, lettering is readable, no elements are clipped, and all labels/arrow directions are accurate. A dark-background export **FAILS**, even when the `.drawio` source declares `#FFFFFF`.
6. **Author the DOCX.** OfficeCLI is a suitable primary tool, with WordCraft/Word as alternatives for final layout. Keep titles, descriptions, learning activities, and tables as **real editable DOCX elements**; insert the completed PNG once, with proportions preserved, on an A4 page (or requested size).
7. **Validate in Word.** Reopen the DOCX, check Thai text wrapping, installed fonts (e.g. TH SarabunPSK where required), no substitution, image quality, page breaks, and printable A4 layout. Use real Word validation when accessible. Structural OOXML checks alone do not prove Word's visual rendering.
8. **Revision test.** Change one label or connector in a **copy** of the `.drawio` source; re-export white PNG; replace the corresponding image in DOCX; save and reopen. Do not rerender the AI source image just to fix a label.
9. **Archive and index.** Keep `.drawio` source, PNG export, DOCX, and FIG-SPEC linked by Figure ID. Before modifying an existing artifact, preserve an appropriately named previous version. Update the host project's file map and index when a file is created, renamed, or moved.

## Gates (never fabricate PASS)
- **FIG-0:** fact/figure specification confirmed.
- **FIG-1:** any AI-generated base image checked (if used).
- **FIG-2:** editable draw.io, labels/arrows, *actual* opaque white PNG, print sharpness.
- **DOCX QA:** body/table editable; PNG placed correctly; Word/font/page render checked.
- **Workflow revision:** update source → re-export → replace image in DOCX, then reopen.

If any gate fails, report **FAIL / PARTIAL PASS / NOT_VERIFIED** with the exact blocker. Preserve failed images as QA evidence outside accepted output directories.

## Reusable commands
```bash
python scripts/check_drawio.py examples/three_steps.drawio --require-white
python scripts/check_png.py path/to/figure.png --min-width 1600
python scripts/check_docx.py path/to/document.docx
# Only when a trusted SVG export already exists and CairoSVG is installed:
python scripts/render_svg_png.py path/to/figure.svg path/to/figure.png --scale 2
```

See [quality checks](references/qa-checklist.md) and the [README](README.md) for installation and limitations.

---
name: drawio-docx-pipeline
description: Create editable draw.io diagrams with opaque white backgrounds, export print-ready PNGs, insert them into editable DOCX documents, and validate the results. Use for mind maps, science diagrams, flowcharts, teaching notes, and other figure-rich Word documents.
---

# Draw.io → PNG → DOCX pipeline

## Goal
Produce **two kinds of editable deliverables**: an original `.drawio` file for editing diagram elements, and a `.docx` file with editable body text/tables. The inserted diagram is a **raster PNG** and its individual labels/arrows are **not** editable inside Word. Keep the diagram source paired with the DOCX.

## Mandatory execution mode — Programmatic First / No Computer Use

**Create or revise diagrams programmatically using Python and mxGraph XML by default. Never use browser Computer Use, mouse dragging, screenshot clicking, or GUI automation to create normal diagrams.** The agent must first attempt the JSON → editable .drawio path with scripts/generate_drawio.py; export with draw.io Desktop CLI using scripts/export_drawio_cli.py. If the CLI fails or a required feature cannot be represented, report BLOCKED/PARTIAL and seek explicit permission for a GUI fallback; do not silently invoke Computer Use.

Read [programmatic-authoring.md](references/programmatic-authoring.md) before writing a diagram. CLI export and Word render are still separate required QA gates; XML generation itself cannot prove visually correct arrows or Thai fonts.

## Preconditions
1. Read the host project's rules, destination directory guide, prior QA results, and input sources. Preserve originals and make backups before editing.
2. Confirm Python 3, draw.io Desktop CLI or an approved non-GUI export route, and OfficeCLI/Word or equivalents are actually available. Tool discovery is **not proof** that generation/export/rendering works.
3. For factual/scientific content, verify the requested indicator, terminology, numerical relationships, arrow directions, and visual semantics from authorized sources; never silently invent textbook claims.
4. Never commit private source material, credentials, personal files, or licensed fonts into a public skill repository.

## Mandatory resource-saving pre-generation gate
Before **any** new AI image, define *only* the visual asset(s) the diagram will actually need; never request a finished infographic/poster when draw.io only needs a plant, animal, organ, or small part. Draft a per-figure [asset plan](references/asset-plan-template.md) stating the exact subject/parts, placement box/aspect, resolution, excluded scene elements, background, scientific references, reuse check and expected useful coverage. Default to one tight, text-free subject per required image, at least 80% useful subject coverage and no more than 15% expected crop/discard. Validate a structured plan with `python scripts/check_asset_plan.py examples/scoped-image-plan.json --ready` before generation. Save **every** generation (including rejected outputs) as an unchanged original with SHA/provenance; edited derivatives belong separately. A saved image is not automatically QA-approved.

Prefer **programmatic Python + mxGraph XML** for authoring `.drawio`, followed by **draw.io Desktop CLI** for export; web GUI/Computer Use is exceptional and requires explicit authorization. XML inspection does not prove native app roundtrip.

## Workflow
1. **Figure specification.** Record a stable Figure ID, purpose, audience, source references, labels, intended relations, print size, and science/visual QA criteria. Use [the FIG-SPEC template](references/fig-spec-template.md).
2. **Plan only needed imagery (FIG-0A).** Inventory reusable approved source artwork, decide exact content and layout box, validate expected useful occupancy, and write the scoped asset plan *before* generating. Generating a full poster and cropping out an element is a workflow error unless justified and logged.
3. **Prepare optional imagery.** If a scene/object illustration is needed, generate a **text-free source image** first. Import/embed it into draw.io; add labels/arrows/symbols only after import. Prefer drawn, precise symbols for wiring, graphs, scales, rays, and other exact relationships.
4. **Author without Computer Use.** Write a JSON figure spec and run `python scripts/generate_drawio.py SPEC.json Figure_v01.drawio --manifest Figure_v01.json` to produce uncompressed editable mxGraph XML with a **white canvas**, editable vertices, edges and embedded image bytes. Create a new version for each revision. Verify graph topology and test reopening in a real editor separately. See [programmatic authoring](references/programmatic-authoring.md).
5. **Export print-ready PNG without GUI.** Prefer `python scripts/export_drawio_cli.py Figure_v01.drawio Figure_v01.png --drawio /path/to/draw.io --scale 2` using installed draw.io Desktop CLI; use opaque white background and LIGHT rendering. Aim for 2×–3× or at least ~300 dpi at the intended physical size. **Visually inspect the exported pixels**, not just the XML background attribute. If the native export is dark/incorrect or unavailable, use a **trusted white-background SVG export** followed by a renderer such as FigCraft, Inkscape, or the optional `scripts/render_svg_png.py`; do not assume a simple draw.io XML-to-SVG script supports arbitrary diagrams or embedded imagery.
6. **Validate the PNG.** Run `scripts/check_png.py` when Pillow is available. Ensure the image is opaque/white at its margins, lettering is readable, no elements are clipped, and all labels/arrow directions are accurate. A dark-background export **FAILS**, even when the `.drawio` source declares `#FFFFFF`.
7. **Author the DOCX.** OfficeCLI is a suitable primary tool, with WordCraft/Word as alternatives for final layout. Keep titles, descriptions, learning activities, and tables as **real editable DOCX elements**; insert the completed PNG once, with proportions preserved, on an A4 page (or requested size).
8. **Validate in Word.** Reopen the DOCX, check Thai text wrapping, installed fonts (e.g. TH SarabunPSK where required), no substitution, image quality, page breaks, and printable A4 layout. Use real Word validation when accessible. Structural OOXML checks alone do not prove Word's visual rendering.
9. **Revision test.** Change one label or connector in a **copy** of the `.drawio` source; re-export white PNG; replace the corresponding image in DOCX; save and reopen. Do not rerender the AI source image just to fix a label.
10. **Archive and index.** Keep `.drawio` source, PNG export, DOCX, and FIG-SPEC linked by Figure ID. Before modifying an existing artifact, preserve an appropriately named previous version. Update the host project's file map and index when a file is created, renamed, or moved.

## Gates (never fabricate PASS)
- **FIG-0:** fact/figure specification confirmed.
- **FIG-0A:** scoped asset plan checked before any generation; reuse review, only required subject, crop/discard budget.
- **FIG-1:** any AI-generated base image checked (if used).
- **FIG-2:** editable draw.io, labels/arrows, *actual* opaque white PNG, print sharpness.
- **DOCX QA:** body/table editable; PNG placed correctly; Word/font/page render checked.
- **Workflow revision:** update source → re-export → replace image in DOCX, then reopen.

If any gate fails, report **FAIL / PARTIAL PASS / NOT_VERIFIED** with the exact blocker. Preserve failed images as QA evidence outside accepted output directories.

## Reusable commands
```bash
python scripts/check_asset_plan.py examples/scoped-image-plan.json --ready
python scripts/generate_drawio.py examples/programmatic-three-steps.json output/FIG01_v01.drawio --manifest output/FIG01_v01.json
python scripts/check_drawio.py output/FIG01_v01.drawio --require-white
python scripts/export_drawio_cli.py output/FIG01_v01.drawio output/FIG01_v01.png --drawio /path/to/draw.io --scale 2
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/check_drawio.py examples/three_steps.drawio --require-white
python scripts/check_png.py path/to/figure.png --min-width 1600
python scripts/check_docx.py path/to/document.docx
# Only when a trusted SVG export already exists and CairoSVG is installed:
python scripts/render_svg_png.py path/to/figure.svg path/to/figure.png --scale 2
```

See [quality checks](references/qa-checklist.md) and the [README](README.md) for installation and limitations.

## Editorial extensions (Thai A4 science notes)

For a project that requires textbook-inspired figure layout, ImageGen-first illustration, academically formatted Word tables, separate memory-box tables, and word-safe Thai paragraphs, use [Editorial QA extension V3.2](references/editorial-quality-gates-v3-2.md). This includes mandatory visual endpoint QA for draw.io connectors, cloud ID/SHA traceability, and **native Word rendering of every page**. Component approval does **not** confer chapter approval; never overwrite approved artifacts. The extension is opt-in through the host project's rules.

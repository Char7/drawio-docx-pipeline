# drawio-docx-pipeline

A reusable agent skill for making **editable diagram sources** in [draw.io / diagrams.net](https://www.diagrams.net/), exporting **opaque white PNGs**, and inserting them into **editable Word documents**.

**ภาษาไทย:** Skill สำหรับสร้าง Mind Map, แผนภาพวิทยาศาสตร์ และ Flowchart ด้วย draw.io โดยใช้พื้นหลังสีขาว เก็บไฟล์ `.drawio` ให้แก้กล่อง/ข้อความ/ลูกศรได้ ส่งออกเป็น PNG แล้วแทรกใน DOCX ที่ข้อความหลักและตารางยังแก้ไขได้

## Default: programmatic authoring (no Computer Use)

**Agents MUST generate editable .drawio with Python + mxGraph XML first, without browser clicks or GUI mouse automation.** Draw.io Desktop is used through its **CLI for PNG export**, not as a manually driven editor. Only a specifically requested/authorized GUI-only exception may use Computer Use; missing CLI support is **BLOCKED**, not permission for silent fallback.

~~~bash
python scripts/generate_drawio.py examples/programmatic-three-steps.json output/FIG01_v01.drawio --manifest output/FIG01_v01.json
python scripts/check_drawio.py output/FIG01_v01.drawio --require-white
python scripts/export_drawio_cli.py output/FIG01_v01.drawio output/FIG01_v01.png --drawio "/path/to/draw.io" --scale 2
python -m unittest discover -s scripts -p "test_*.py"
~~~

See [programmatic authoring and strict no-Computer-Use policy](references/programmatic-authoring.md), plus the JSON example, generator and CLI exporter. Native export and visual connector/Thai font QA remain mandatory before Word.

## What is editable?

| Artifact | Editable elements |
| --- | --- |
| `.drawio` | Diagram labels, arrows, shapes, positions, embedded images (in draw.io) |
| `.png` | **Not editable** as separate objects; regenerate it from the source |
| `.docx` | Body text, titles, tables, image position/size; **not individual PNG labels** |

## Reduce wasted image generation

**Plan before you generate:** If a diagram needs a fish, leaf, circuit part, or one anatomical object, generate **that isolated object**—not a decorated full-page poster that will be cropped. Use an [asset scope plan](references/asset-plan-template.md) for the required subject and visible parts, target draw.io box, aspect ratio, print resolution, transparent/white background, exclusions and reuse check. Aim for at least 80% usable subject and no more than 15% anticipated discard. Always archive all generated originals (including failures), preserve edited derivatives separately, and record SHA/provenance; only QA-passed assets can be embedded.

Use **Python + mxGraph XML first** to author the editable .drawio. Use draw.io **Desktop CLI** for native export and verify the actual rendered PNG. If export fails, record the error and use an expressly approved fallback; never silently use Computer Use. Keep every editable `.drawio` revision. Neither a web view nor XML validity proves successful native editing.

```bash
python scripts/check_asset_plan.py examples/scoped-image-plan.json --ready
```

## Workflow

```text
Verified content / FIG-SPEC / scoped asset plan
          |
Only needed isolated, text-free subject asset
          v
Python + editable mxGraph XML: white canvas + shapes + labels + arrows
          |
      Editable .drawio
          |
   Native PNG (light/opaque)
          |  if native export fails appearance QA:
          +--> SVG from a trusted renderer --> FigCraft / Inkscape / CairoSVG
          |
   White, high-resolution PNG
          |
  OfficeCLI / WordCraft / Microsoft Word
          |
 DOCX with editable body and tables
          |
   QA: white pixels, language, print size, source re-export, Word reopen
```

See [SKILL.md](SKILL.md), [workflow](references/workflow.md), and [QA checklist](references/qa-checklist.md).

## Quick start

1. Place this repository under a skill directory that your agent can read, or direct your agent to read `SKILL.md`. **A public GitHub repository does not automatically install itself in your assistant or lnwjud.**
2. Provide the lesson topic or figure brief, audience, and source material.
3. Ask for `<Figure_ID>.drawio` and `<Figure_ID>.png` (white, high resolution), and a DOCX with editable body text/tables.
4. Review the image in the actual A4 document; approve the figure and DOCX separately.

### Optional validators

```bash
python scripts/check_asset_plan.py examples/scoped-image-plan.json --ready
python scripts/check_drawio.py examples/three_steps.drawio --require-white
python -m pip install -r requirements-optional.txt
python scripts/check_png.py figure.png --min-width 1600
python scripts/check_docx.py document.docx
python scripts/render_svg_png.py figure.svg figure.png --scale 2
```

`check_drawio.py` and `check_docx.py` use Python's standard library. `check_png.py` requires Pillow; SVG rasterization additionally requires CairoSVG and its compatible native dependencies.

## Evidence and limitations

This workflow was informed by a real Windows / Thai A4 DOCX workflow using draw.io web, an SVG/PNG graphics tool, OfficeCLI, WordCraft, and Microsoft Word. **That does not mean every installation has these tools or that every diagram will export correctly without adjustment.**

In an observed workflow, diagrams.net web exported **a dark-background PNG** despite a white source setting; a white SVG to PNG export path worked for the *simple, controlled test figure*. This repository **does not claim automatic compatibility with arbitrary compressed draw.io files, image-heavy diagrams, or complex typography**. Inspect those in the actual application and verify the final pixels.

## Public repository hygiene

This repository contains **only the skill, original generic examples, and source scripts**—no private lesson PDFs, generated student documents, project folders, credential files, or font binaries. Do not publish user materials without permission. Licensed under the [MIT License](LICENSE), Copyright (c) 2026 Char7. You may use, modify, and distribute the skill (including commercially), provided the MIT copyright and permission notice is retained.

## Thai science-note editorial QA extension

When a host project requires ImageGen-first isolated plant illustrations, native editable draw.io connectors, academically styled Word tables, one memory-box table per idea, and Thai word-safe A4 paragraphs, follow [the V3.2 editorial QA extension](references/editorial-quality-gates-v3-2.md). This includes checking connector endpoints against exported pixels, preserving every accepted/rejected file version, and validating **all Word pages natively**, not only OOXML structure. User approval is scoped to the specific artifact or component reviewed.

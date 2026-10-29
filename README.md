# drawio-docx-pipeline

A reusable agent skill for making **editable diagram sources** in [draw.io / diagrams.net](https://www.diagrams.net/), exporting **opaque white PNGs**, and inserting them into **editable Word documents**.

**ภาษาไทย:** Skill สำหรับสร้าง Mind Map, แผนภาพวิทยาศาสตร์ และ Flowchart ด้วย draw.io โดยใช้พื้นหลังสีขาว เก็บไฟล์ `.drawio` ให้แก้กล่อง/ข้อความ/ลูกศรได้ ส่งออกเป็น PNG แล้วแทรกใน DOCX ที่ข้อความหลักและตารางยังแก้ไขได้

## What is editable?

| Artifact | Editable elements |
| --- | --- |
| `.drawio` | Diagram labels, arrows, shapes, positions, embedded images (in draw.io) |
| `.png` | **Not editable** as separate objects; regenerate it from the source |
| `.docx` | Body text, titles, tables, image position/size; **not individual PNG labels** |

## Workflow

```text
Verified content / FIG-SPEC
          |
Optional text-free generated illustration
          v
draw.io: white canvas + shapes + labels + arrows
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

This repository contains **only the skill, original generic examples, and source scripts**—no private lesson PDFs, generated student documents, project folders, credential files, or font binaries. Do not publish user materials without permission. No open-source license has been selected yet; public visibility alone does not confer reuse rights.

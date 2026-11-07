# Implementation workflow

## Default non-GUI authoring route

**Mandatory for normal figures:** JSON FIG-SPEC → `scripts/generate_drawio.py` (Python ElementTree/mxGraph) → versioned editable `.drawio` → `scripts/export_drawio_cli.py` (draw.io Desktop executable) → PNG pixel QA → editable Word body/tables + native Word QA. This does **not** require opening a browser or using Computer Use.

Agents must **not** choose diagrams.net web mouse control or manual Desktop UI as the initial authoring method. If the programmatic generator cannot express a necessary complex feature, record a concrete blocker and obtain explicit permission for the GUI exception. Do not silently fall back. See [programmatic authoring details](programmatic-authoring.md).

## 1. Scope and Figure ID

Keep one stable Figure ID across the source, export, and document reference. Example: `FIG01_EnergyFlow.drawio` → `FIG01_EnergyFlow.png` → `lesson.docx` + a FIG-SPEC.

Choose the figure structure based on what learners must understand—not on decoration. A science flowchart, classification tree, and electrical circuit require different layout semantics.

## 1A. Scope AI source artwork before generation (FIG-0A)

- Check whether an approved existing asset already shows the necessary structure; reuse instead of re-generating.
- Identify each **individual image subject** needed in the final draw.io, exact body part or whole organism/system, and what must not appear. For a part, request that part directly—not a large infographic to crop.
- Describe draw.io box, aspect ratio, target print pixel dimensions, transparent/white background, scientific references, prompt and exclusion rules. Target >=80% useful subject occupancy, <=15% planned discard/crop unless a justified exception is recorded before generation.
- Never generate labels, arrows, cards, full-lesson graphics or decorations that should be made as editable elements in draw.io.
- Store **all** original generated images including wrong-topic/rejected trials, immutable SHA/provenance, separate derived crops; archiving is not approval. See [asset plan](asset-plan-template.md) and `scripts/check_asset_plan.py`.

## 2. Draw.io editing

- Create a white, opaque diagram page; set the page/background color to `#FFFFFF`.
- Make the diagram labels and connectors editable as draw.io objects.
- Place any original generated source art into the diagram **before** adding text, callouts, or relations.
- Embed source art where supported; if assets are linked, confirm links survive reopen and transfer to other devices.
- For electrical circuits, optics, forces, measurement scales and other exact figures, use explicit symbols/coordinates rather than relying on an illustration model to infer correctness.
- Use the **Python mxGraph XML generator first**. Use installed draw.io **Desktop CLI for exporting**, not GUI clicks. Web/Computer Use authoring is by explicit approval only.
- Save **each** `.drawio` version, even discarded trials, with a unique suffix. Never overwrite the previous edit without a backup.
- Save the `.drawio` file, close it, reopen it, and edit a label to verify source portability. Record actual native UI roundtrip separately from XML parse.

## 3. PNG export (native Desktop CLI primary; no Computer Use)

1. Run `python scripts/generate_drawio.py examples/programmatic-three-steps.json output/FIG01_v01.drawio --manifest output/FIG01_v01.json`.
2. Run `python scripts/check_drawio.py output/FIG01_v01.drawio --require-white` to check source structure.
3. Run `python scripts/export_drawio_cli.py output/FIG01_v01.drawio output/FIG01_v01.png --drawio /path/to/draw.io --scale 2 --border 8`. The installed Desktop CLI runs without mouse clicks.
4. Verify exported PNG is opaque white, Thai font/tones readable, no clipping, correct arrow direction and physical print sharpness. Structural XML checks are **not** visual validation.
5. When the executable is missing, report `BLOCKED_NATIVE_EXPORT`; do not launch Computer Use automatically. Any non-GUI fallback must be supported and documented.

## 4. SVG → PNG fallback

If native export is unavailable or fails:
- Obtain an actual vector SVG with **light colors and correct fonts/geometry** using draw.io export or a renderer that supports the source. For simple diagrams only, a controlled source-to-SVG conversion may be validated manually.
- Preserve a white background `<rect fill="#FFFFFF">` (or explicitly set it in the SVG-to-PNG renderer).
- Use a supported graphics exporter (FigCraft, Inkscape, or CairoSVG).
- Run pixel/opacity checks and visually compare against the draw.io source.

**Limitations:** generic `.drawio` cannot simply be renamed to `.svg`. Lossless conversion of group transforms, rich HTML labels, embedded raster images, custom connectors, compressed models, and multi-page diagrams needs a real editor/rendering engine. Do not claim that a simple XML parser handles all these features.

## 5. DOCX layout

- Use real Word paragraphs and tables for the explanatory content.
- Insert the image with proportional sizing. Consider portrait A4 and print margins before choosing the image width.
- Keep image descriptions and accessible alt text where supported.
- For Thai documents, verify font availability and East Asia font assignment. **Do not distribute font binaries** as part of this skill.
- Reopen and render the final DOCX using Microsoft Word or an equivalent application; XML validity is not visual QA.

## 6. Revision and traceability

A change to a label should update the `.drawio` source, not the old PNG's pixels. Create or verify a backup, edit source, export a new white PNG, replace the DOCX image, reopen and repeat print QA.

A project may use an index such as:

```text
FIG01 | indicator/topic | sources/pages | ./diagrams/FIG01.drawio
      | ./diagrams/exports/FIG01.png | ./docs/lesson.docx | QA / reviewer
```

## 7. Failing safely

- If PNG remains black after choosing Light/opaque export, record **VISUAL FAIL** and use the SVG fallback only if its image can be checked.
- If the embedded image no longer loads after moving the `.drawio`, mark **NOT_VERIFIED** until portable embedding is confirmed.
- If the requested font is substituted in Word, mark **FONT QA FAIL** until corrected.
- If the user needs individual diagram labels editable directly within Word, **this is not that output**: it supplies an editable source `.drawio` paired with a raster PNG in Word.

## 8. Editorial QA for Thai educational DOCX

For the host project's specific textbook-style presentation and acceptance rules, apply [the V3.2 editorial QA extension](editorial-quality-gates-v3-2.md). In particular, don't treat separately stored source sentences as separate Word paragraphs; let Word flow the actual Thai prose until the margin. Check the *actual native Word render* for midword splits. Avoid indiscriminate U+200B/U+2060 insertion; if a word splits, adjust only that local word-boundary break and rerender. With textbook-inspired draw.io mind maps, verify that relational connectors actually touch their target vertices/cards, not just that edge XML is present. Academic tables and memory boxes must remain native Word tables and fit within A4 portrait text margins. Preserve version history and scoped approval statuses.

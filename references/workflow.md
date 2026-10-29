# Implementation workflow

## 1. Scope and Figure ID

Keep one stable Figure ID across the source, export, and document reference. Example: `FIG01_EnergyFlow.drawio` → `FIG01_EnergyFlow.png` → `lesson.docx` + a FIG-SPEC.

Choose the figure structure based on what learners must understand—not on decoration. A science flowchart, classification tree, and electrical circuit require different layout semantics.

## 2. Draw.io editing

- Create a white, opaque diagram page; set the page/background color to `#FFFFFF`.
- Make the diagram labels and connectors editable as draw.io objects.
- Place any original generated source art into the diagram **before** adding text, callouts, or relations.
- Embed source art where supported; if assets are linked, confirm links survive reopen and transfer to other devices.
- For electrical circuits, optics, forces, measurement scales and other exact figures, use explicit symbols/coordinates rather than relying on an illustration model to infer correctness.
- Save the `.drawio` file, close it, reopen it, and edit a label to verify source portability.

## 3. PNG export (primary)

1. In diagrams.net, choose **File → Export As → PNG**.
2. Use a **Light** appearance (where a theme option is shown).
3. Turn **transparent background OFF**.
4. Prefer scale 2× or 3×; verify legibility at the intended A4 print width.
5. Export, reopen the downloaded PNG, and visually check:
   - background **white**, not black or transparent;
   - Thai labels render correctly, including vowels and tone marks;
   - all arrows/lines point where intended and aren't cropped;
   - objects have adequate contrast, no clipping or line overlap.

A white background attribute in the draw.io XML is **not sufficient** to mark the export as PASS.

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

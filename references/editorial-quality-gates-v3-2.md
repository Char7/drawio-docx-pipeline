# Editorial QA extension: science short notes (Pipeline V3.2)

This reusable extension is based on review of a Thai primary-science A4 Word workflow. Apply it when a host project requests these constraints. **Host-specific source, copyright, storage, and approval policies take precedence**; do not publish source PDFs, user documents, or generated images in this public skill.

## 1. Source and acceptance boundaries
- Read the project's latest checkpoint, source mapping, and design approvals before editing. Use the designated *cut* PDF and reviewed Markdown together: Markdown for prose, matching PDF pages for image/table/mind-map composition. Do not silently substitute original/full-PDF page numbers.
- Never rerun whole-book OCR when reviewed source text exists. Resolve uncertain words with targeted source-page inspection only. Keep RAW, REVIEWED, and FILTERED_FOR_DOCX as distinct versioned stages; never overwrite RAW.
- Remove quizzes/exercises, answer keys, app prompts, and promotional material when the host project excludes them. Keep useful factual exposition unless explicitly excluded.
- Approval is scoped: **a reviewer accepting typography, one diagram, or one table is not approval of a whole chapter**. Maintain component-level statuses and carry unrelated pending gates forward.

## 2. Isolated generated assets BEFORE editable draw.io annotation
- For living organisms, plant parts, seed/sprout/flower/fruit life-cycle stages, or physical objects requiring illustration, use the project's approved image-generation method to make **standalone, text-free, appropriately sized** artwork. Generate only necessary subjects/stages, not finished lesson infographics to crop.
- Before generation record exactly which visual assets are needed, proposed placement and print size, orientation, reusable assets, and useful-area/crop budget. Store *all* originals (including rejected outputs), SHA-256, generation provenance, and accepted derivative mapping. A generated infographic with pre-rendered labels or arrows is **not** a compliant object asset.
- Compose final figures in draw.io: embed the individual source images, and add titles, labels, arrows, circles, shape backgrounds and lines as **native editable draw.io objects**. Do not fake an illustrated plant using primitive shapes when the host rule specifically requires generated natural artwork; do not crop a finished figure out of the reference PDF.
- Keep the source figure's **semantic grouping, hierarchy, learning order, and color roles** when redesigning an existing textbook mind map, but improve whitespace, contrast and symmetry. Do not create new scientific relationships just for visual balance.

## 3. Diagram topology and visual checks
- Every *meaningful* arrow/line must reach the correct labeled target. Inspect the actual **exported pixels** for dangling line ends, disconnected edges, arrows that terminate short of a card, text occluded by lines, clipped fonts or vowel/tone-mark collisions.
- Where a connector should attach to an editable card, bind its native draw.io edge to actual source/target cell IDs and use explicit exit/entry anchors (for example, bottom-center to top-center). Verify endpoint IDs refer to existing editable vertices, verify geometrical side, and export again after every topology fix.
- If a line is intentionally decorative rather than relational, record that exception; don't claim all edges are anchored merely because the XML contains edge cells. XML parsing is a *structural* check; the real draw.io export is the visual check.
- Use visually consistent edge color, thickness, spacing, arrow semantics and pastel/dark color contrast; **no text touching or crossing connectors**. Text, labels, arrows and shapes remain editable in the `.drawio` original, **not** inside the raster PNG embedded in Word.
- Save a new `.drawio` filename **before** rendering a new PNG. If the host uses cloud storage, verify the cloud File ID, path and size by readback; keep a local Figure ID → cloud File ID → source SHA-256 → PNG → DOCX mapping. Never infer a File ID from a filename alone.

## 4. Academic editable tables and separate memory boxes
- Use native Word tables, not screenshots. Academic-style tables: clear bold headers, subdued fills/borders, consistent cell padding, aligned text, balanced column widths, and accurate row/column grouping.
- Calculate table width against **actual printable A4 portrait page width** (page width minus left/right margins), not just the page width. Keep every table within margins, prevent orphaned header rows/awkward row splits when supported, and recheck after paragraph-flow changes.
- A `memory box` is **one independent Word table per concept**, with its own title/body and spacing between boxes. Never merge multiple distinct memory points into one continuous table merely for convenience.
- Keep table content editable, readable at 100% zoom/print, and consistent across the chapter.

## 5. Thai paragraph and word-safe reflow
- Continuous prose belongs to **one coherent Word paragraph** (or intentional prose paragraphs), not a separate paragraph for each source line or sentence. Let Word use the available text width before wrapping; do not manually add hard breaks to mimic a narrow OCR transcription.
- **No Thai word may be torn across lines.** Inspect Microsoft Word's *native* render at readable zoom, including roots/plant stems, Thai dependent vowels/tones, and compound technical terms.
- If native Word repeatedly divides a Thai word, apply the **smallest localized** break *before a complete word or phrase*, rerender, and check the entire paragraph again. Hard line breaks must be rare and documented; never solve this by making every line arbitrarily short.
- **Do not blanket-insert U+200B zero-width spaces or U+2060 word joiners** throughout an entire Thai paragraph. Testing has shown bulk insertion can produce new or clipped Word layout errors. Prefer normal Thai language metadata, intended Thai font (e.g. THSarabunPSK when required), normal character runs, and targeted Word QA.
- Keep original visible wording intact unless a separate content revision is authorized; prove paragraph/text and table content equivalence. Preserve A4 portrait, Arabic numerals if requested, and editable Word body/table text. Avoid visible spell-check underlines in final inspected output.

## 6. Versioned DOCX, Word Native QA, and traceability
- Never overwrite approved files or earlier revisions. Back up rules and any mutable status registers first. For a diagram repair: **edit .drawio copy → export a fresh PNG → embed the new PNG into a newly versioned DOCX → reopen it**. Confirm DOCX's embedded media hash matches the new export, not merely its filename.
- Run structural DOCX checks (ZIP/OOXML, page dimensions, fonts, table count, media hashes), then **render every page in real Microsoft Word**. Inspect table widths, pagination, image placement, font substitution, Thai word breaks, legibility, page boundaries, and the entire figure's connectors.
- Record separate PASS / FAIL / PENDING / NOT_VERIFIED for source, assets, editable draw.io, cloud mapping, PNG, academic tables, memory boxes, native Word layout, and user approval. Never equate successful rendering with user approval or scientific fact-checking.
- If an artifact's bytes differ from the hash in a previously accepted checkpoint, flag it as **changed/unverified** rather than claiming the new bytes were approved; retain both the accepted hash and current hash.
- When image generation returns an unusable composite rather than required isolated assets, stop the *final acceptance* gate and retain partial work. Do not substitute procedural drawings or call the chapter approved.

## Acceptance example
A user may approve a chapter's **Thai text reflow** while the image-generation gates for its plant/plant-life-cycle figures remain pending. Record `TYPOGRAPHY_APPROVED_BY_USER` for the verified version and `CHAPTER_QA_PENDING` for the document. A revised mind map may pass topology, export and Word QA separately.

Use this guide alongside [workflow](workflow.md) and [quality checklist](qa-checklist.md); it is not a substitute for each host project's authoritative Pipeline version.

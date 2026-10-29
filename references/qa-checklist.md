# Quality acceptance checklist

| Gate | What to inspect | Accept only when |
| --- | --- | --- |
| FIG-0 | Scientific/content reference, figure purpose, diagram logic | Terms, classifications, symbols, directions and quantities are source-supported |
| FIG-1 | Optional generated base picture | No unintended text/labels/arrows; objects are appropriate; no copied copyrighted source artwork |
| Source | The original `.drawio` | Reopens, editable text/shapes/edges, correct background, embedded assets still load |
| Export | Actual PNG pixels | White/opaque (not dark/transparent), sharp enough for paper, Thai labels and arrows correct |
| Word | DOCX body/tables | Selectable/editable Word elements; PNG inserted at proper size/aspect ratio |
| Font | Word on destination machine | Intended font installed, no visible substitution, East Asia Thai display correct |
| Layout | Actual A4 page render/print preview | Nothing clipped, readable at print size, sensible margins and spacing |
| Revisions | Modify source and re-export | Changed PNG replaces image in DOCX; old asset preserved if needed |
| Provenance | Figure ID and file map | Source, export, document, sources and QA report can be found from the host project's index |

**Do not mark the workflow PASS based only on XML, the existence of an exported file, or a successful DOCX save.** Render and inspect.

## Executable checks

- `python scripts/check_drawio.py figure.drawio --require-white`: XML integrity, model existence, vertex/edge counts, optional image-link warnings.
- `python scripts/check_png.py figure.png --min-width 1600`: PNG format, alpha channel, dimensions and white corner samples. May falsely flag drawings intentionally occupying the outermost corners; inspect manually.
- `python scripts/check_docx.py lesson.docx`: DOCX zip/XML readability and basic counts for paragraphs/tables/media/fonts. Not a substitute for Microsoft Word print preview.

## Stop conditions

Stop and report a concrete issue if:
- the figure misrepresents a source, especially wiring/polarity, classification, scales, or causal direction;
- image generation contains bogus text that has been hidden rather than fixed;
- a diagram's white background cannot be verified in exported pixels;
- required doc typography cannot be checked or shows substitution;
- there is no editable `.drawio` source to accompany the PNG;
- source/user material would be exposed to a public GitHub repository without permission.

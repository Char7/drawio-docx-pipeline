# Quality acceptance checklist

| Gate | What to inspect | Accept only when |
| --- | --- | --- |
| Programmatic authoring | Python + mxGraph XML source created without Computer Use | JSON spec and versioned .drawio exist; Desktop CLI export is separate; no silent browser/GUI fallback |
| FIG-0A | AI asset plan **before** generation | Only necessary image subjects/parts, reuse check, target draw.io placement, >=80% useful subject and <=15% expected discard; no prebuilt poster/labels/arrows |
| Source archive | Generated imagery and variants | Every generation, including rejects, saved as unmodified originals with hashes/provenance; derivatives linked separately; archives do not imply approval |
| FIG-0 | Scientific/content reference, figure purpose, diagram logic | Terms, classifications, symbols, directions and quantities are source-supported |
| FIG-1 | Optional generated base picture | No unintended text/labels/arrows; objects are appropriate; no copied copyrighted source artwork |
| Source | Every versioned `.drawio` | Reopens, editable text/shapes/edges, correct background, embedded assets still load |
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
- an agent tries browser/desktop Computer Use for ordinary diagram authoring without an explicit user request or fallback authorization;
- draw.io Desktop CLI is not installed, and no approved non-GUI export route exists; do not fabricate native export PASS;
- an image is about to be generated without an asset scope plan, or a large scene will be mostly cropped without scientific justification;
- required images were generated but not archived with traceable SHA/source;
- installed draw.io Desktop could not open/save/export and a fallback is mislabeled native;
- the figure misrepresents a source, especially wiring/polarity, classification, scales, or causal direction;
- image generation contains bogus text that has been hidden rather than fixed;
- a diagram's white background cannot be verified in exported pixels;
- required doc typography cannot be checked or shows substitution;
- there is no editable `.drawio` source to accompany the PNG;
- source/user material would be exposed to a public GitHub repository without permission.

## Editorial extension acceptance gates

| Gate | Required evidence | Mark FAIL / PENDING when |
| --- | --- | --- |
| PDF/Markdown source mapping | Correct cut-source page IDs and filtered Markdown stage | Old-page references or unreviewed RAW are substituted |
| ImageGen-first isolated assets | Exact required subject/stage, original image + provenance/SHA | Full infographic, procedural substitute or unauthorized PDF copy |
| Editable connector topology | Export preview *and* verified native source/target cells where relevant | Line ends short of its card, crosses text, or points at wrong node |
| Academic Word tables | Balanced real table widths within A4 text margins | Table overflows or text is clipped |
| Separate memory boxes | One native, independently spaced table per concept | Different memory concepts are one joined table |
| Thai paragraph reflow | Coherent paragraph with normal Word line wrap, *native Word* screenshot | Every source line is its own paragraph, or a Thai word is ripped |
| Word-wide visual review | Real Word screenshot/print preview for **every page** | Only HTML or OOXML checks exist |
| Approval scope/version | Component approvals and exact accepted hashes separately recorded | Partial approval is promoted to whole-chapter approval |

See [editorial-quality-gates-v3-2.md](editorial-quality-gates-v3-2.md) for the complete workflow and the warning against blanket zero-width/word-joiner insertion in Thai prose.

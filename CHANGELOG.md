# Changelog

## 0.3.0 — 2026-11-07

- Changed the default authoring path to **Programmatic First**: Python + editable mxGraph XML, not browser or desktop Computer Use.
- Added standard-library `scripts/generate_drawio.py`, Thai JSON example, optional embedded PNG/JPEG assets, native editable edges/anchors and non-overwrite protection.
- Added `scripts/export_drawio_cli.py` for non-interactive native PNG export, with explicit BLOCKED handling if Desktop CLI is absent.
- Added `scripts/test_generate_drawio.py`, GitHub Actions XML/structure checks, and `references/programmatic-authoring.md` for agent reuse in other projects.
- Preserved existing FIG-SPEC, scoped ImageGen assets, actual PNG visual QA, OfficeCLI/Word validation and versioned approval rules. GUI authoring now requires explicit permission.


## 0.2.0 — 2026-11-04

- Added FIG-0A scoped asset-plan gate to reduce large unused AI generations and unnecessary cropping. New `scripts/check_asset_plan.py` and one-subject example, plus template.
- Require archiving all original generated images (including rejected outputs) and all editable draw.io versions with traceable source/export/DOCX links.
- Prefer installed draw.io Desktop to web/SVG fallback; distinguish GUI editing/export evidence from XML structure tests.
- No project-private images, source documents, or fonts committed.

## 0.1.0 — 2026-10-29

- Initial reusable `drawio-docx-pipeline` skill and generic example.
- Defined actual white/opaque PNG acceptance, source/edit/re-export, Thai Word QA, and safely documented SVG fallback.
- Added draw.io/PNG/DOCX checkers and optional SVG rasterizer.
- No user documents, generated copyrighted assets, credentials, or fonts are bundled.

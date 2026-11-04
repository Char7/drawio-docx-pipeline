# Scoped AI source image plan — FIG-0A template

Complete this **before any image-generation call**. Use a copy per Figure ID. The goal is to generate only source artwork that is actually placed in the editable draw.io diagram; layout, labels and arrows belong in draw.io, not baked into the image.

## Identity and reuse

- Figure ID and intended learner outcome:
- Image subject required? YES / NO (if NO, use draw.io objects directly):
- Search existing generated/approved subject archive before creating a new asset:
- Reuse decision: path/sha or why an existing image is unsuitable:
- Number of truly necessary image subjects (minimum possible):
- Scientific references and uncertainty:
- Age/grade suitability:

## One row per requested image (not per poster/scene)

| Asset ID | Precisely what must be visible | What must NOT be generated | Placement box (px) | Aspect and requested px | Useful coverage | Expected discarded/cropped fraction | Background | Prompt ID/status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <asset> | <one organism/organ/component and only needed parts> | <extra organs, captions, arrows, layout, background> | <W×H> | <ratio, W×H> | >=80% | <=15% | transparent/flat white | <plan> |

Generate isolated subjects, not whole infographics and not extra decorations for extraction. Only allow a complete scene where relationships or habitat scientifically require the scene; justify that exception **before** generation. Do not ask for maximum resolution unless the final placement requires it.

## Before generation

- Plan validated by `python scripts/check_asset_plan.py <plan.json> --ready`.
- No duplicates, no speculative variations, no unneeded background.
- Source-only prompt and negative prompt prohibit all text, arrows, labels, infographic cards and watermarks.
- Each asset has a reference, target crop/use region, planned useful coverage and size, and no oversized image waste.
- Any previous image failures analyzed before another prompt is submitted.
- The plan is a production gate; it is **not user approval** of the finished illustration.

## After generation

- Save **all** raw image outputs immediately, including incorrect/off-topic outputs, with byte-for-byte SHA-256, IDs, prompt description and reason for rejection. Keep edits/crops as linked derivatives, not replacements.
- Scientific and visual QA checks exact subject anatomy/structure, age suitability and usable composition. Only passed assets go into draw.io.
- Embed image in an editable, versioned `.drawio` source; keep labels, connectors, text separate.
- Prefer installed draw.io Desktop for open/Save As/reopen/native PNG export. Native CLI/GUI failure must be recorded; SVG/Chromium fallback is not native export.
- Map source image SHA -> `.drawio` version -> PNG SHA -> DOCX and review status. Preserve every source version.

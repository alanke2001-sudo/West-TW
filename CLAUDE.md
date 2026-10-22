# West-TW

This repo is B300's growing database of public-source (OSINT) research reports, browsed offline through tag filters on `index.html`. All reader-facing text is Traditional Chinese.

Standing workflow: every new research report produced for B300 is also added here, following README.md「新增報告」:

- One folder per report: `reports/<YYYY-MM-topic>/` with a self-contained offline `index.html` (inline CSS/SVG, no external fonts or scripts), the `.docx`, and `figures/*.png`. Give every chapter heading an `id` and add the back link to `../../index.html`.
- Register it in `data/catalog.json` with report-level tags plus per-chapter `sections` (anchor, one-sentence summary, tags). Use only tags already in `tag_groups` (4 groups, 23 tags). B300 found 60 tags too many (2026-10-22), so keep the vocabulary small, about 25 at most: no tags for equipment models, cities or sources; those stay in the report text. Add a new broad topic tag only when nothing fits.
- Run `python3 tools/build_catalog.py`. It must print `ok` with no warnings. Never edit `data/catalog.js` by hand.
- Update the README「目前收錄」table, then open a PR against `main`.
- Each claim in a report keeps its judgment label (事實／官方評估／推估／本報告推算) and a numbered source link.

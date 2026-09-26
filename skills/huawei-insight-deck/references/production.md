# Reproducible production

Paths below start at this skill folder. Use a private build folder and a new output
filename. Python 3 standard library suffices for fetch, assembly and checks.
The optional sample builder needs Node.js and Codex's bundled `@oai/artifact-tool`;
it is not a public npm dependency to install blindly. If unavailable, use an available
PPTX editor for native content and the same assembler. Do not fall back to legacy styling.

```bash
python3 scripts/fetch_official_template.py .template-cache/official-light-2021.pptx
# If needed, set ARTIFACT_TOOL_MODULE to the runtime's dist/artifact_tool.mjs.
node scripts/build_content.mjs assets/example-deck.json .build/content.pptx
python3 scripts/assemble_official.py \
  --template .template-cache/official-light-2021.pptx \
  --content .build/content.pptx --spec assets/example-deck.json \
  --output .build/review.pptx
python3 scripts/check_official.py \
  --template .template-cache/official-light-2021.pptx --deck .build/review.pptx
```

## Spec and content contract

`slides` is an ordered array. `kind` selects the source slide:

- `cover`: `title` and three `metadata` lines; fit the original frame.
- `contents`: `items` (at most five), optional zero-based `active` index. Repeat
  this page at section boundaries; don't invent a separate chapter master.
- `body`: `title`, one-based `content_slide` referencing the content-only PPTX.
- `end`: preserve the original ending layout/text.
- All pages accept `notes` for sources/scope. Template provenance is appended.

`example-deck.json` adds `content` data for the five demonstrated layouts.
The assembler is independent of this convenience schema and accepts native content
produced by other tools.

Content must use **12196763 × 6858000 EMU**, with no extra title/footer. Native
text, shapes, pictures, tables and charts must fit the original body rectangle.
Groups and rotation are rejected because the bounds check cannot resolve those
transforms. Ungroup or explicitly enhance and test bounds support.
Pictures/charts retain their relationships, including workbook parts; check editability
when using these types. The shipped fixture covers text, shapes, arrows and native
tables, not chart/workbook fidelity.

The assembler remaps shape/relationship IDs, preserves binary dependencies, writes
source notes, omits sample data and rejects a changed source hash. Outputs never
overwrite inputs or existing files. Assembly does not prove text fit or evidence quality.

## Validation and preview

1. Run `check_official.py`. For the sample also run
   `python3 scripts/test_official.py --template <source> --content <content>`.
2. Render in LibreOffice/PowerPoint with reference fonts. A per-process font config
   may expose installed fonts without changing system settings.
3. Inspect every slide full-size; compare cover, contents, body/footer and ending
   with the source. Check CJK glyphs, wrapping, arrows, table rows and source notes.
4. Deliver PPTX and previews with render engine/font details, native element counts,
   shell preservation results and untested application limits.

```bash
soffice --headless --convert-to pdf --outdir .build .build/review.pptx
pdftoppm -scale-to 1600 -png .build/review.pdf .build/page
```

Do not use full-slide screenshots as editable output. Official background art
remains an image; new research text and diagrams remain native.

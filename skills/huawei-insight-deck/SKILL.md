---
name: huawei-insight-deck
description: >-
  Produce editable Chinese technical and executive PPTs using the pinned Huawei
  official 2021 light 16:9 template. Use for 华为风格PPT、技术汇报、研究一页纸、
  版式优化 and render QA when the argument is established. Preserves official
  cover, contents/chapter navigation, body and ending layouts, while adding
  native architecture diagrams, flows, comparisons and evidence. Pair with
  tech-research-deck when the research narrative still needs development.
---

# Huawei Official-Template Research Deck

Use this skill for visual production. Keep research claims and evidence decisions
in the user brief or `$tech-research-deck`; a template establishes neither technical
validity nor company endorsement.

## Source of truth

The default is the user-selected [Huawei official light 16:9 template, 2021](https://e.huawei.com/cn/documents/others/4f951fb72e1944288d3aa73bf40d8a8b).
Its exact file and hash are pinned in `assets/official-template.json`.

- Reuse its actual masters, layouts, theme, artwork, dimensions and placeholders.
  Preserve their bytes with the bundled assembler. Do not redraw a similar shell.
- Source pages: cover, contents, body, chart-color example and ending.
  **No separate chapter master exists.** Reuse contents as chapter navigation;
  an optional red current item is our navigation convention.
- Source slide 4 is a color reference, not a page to ship with sample numbers.
- Body title: 32pt Microsoft YaHei; primary body: 18pt; secondary: 12.99pt.
  Retain positions, white background, page number, confidentiality label and logo.
  No added title underline, fixed insight band or compulsory bottom strip.
- New content belongs inside the original body area. Shorten or split crowded
  content; never silently shrink the official font scale to solve overflow.
- Source-derived rules override community styles. SeanDongX is a conceptual
  layout reference only, not an official Huawei specification.
- Follow explicit user requests for different branding/template treatment, and
  disclose such deviations rather than claiming an exact template match.

Read [official-template-spec.md](references/official-template-spec.md) before authoring.
Select content arrangements from [template-archetypes.md](references/template-archetypes.md).
Qualify facts using [data-rigor-and-caveats.md](references/data-rigor-and-caveats.md).

## Build and inspect

1. Establish one supported claim per body slide; choose the structure by its argument.
2. Fetch/verify the original with `scripts/fetch_official_template.py`. A failed
   download or hash mismatch is a dependency failure: obtain the original file
   instead of inventing a replacement template.
3. Use the official PPTX directly in a capable editor, or follow the reproducible
   [production recipe](references/production.md): author native content on the exact
   canvas, then `scripts/assemble_official.py` fills original placeholders and
   places it in the official shell. `scripts/build_content.mjs` demonstrates five
   layouts using Artifact Tool; the assembler accepts other native PPTX producers.
4. Put claim-level source, date, scope and derivation in notes; keep important
   qualifiers visible. Distinguish facts, vendor claims, inference, estimates and
   proposed validation with words, not just colors.
5. Verify relationships, shell preservation, body bounds and native tables/charts
   where used. Render all pages with the reference fonts. Compare cover, navigation,
   body and ending against the source; inspect content for clipping, overlaps,
   broken arrows and unreadable notes. XML checks alone are not visual QA.
6. Deliver editable PPTX, previews and a short validation summary. State untested
   applications and any font substitution.

The [example spec](assets/example-deck.json) contains illustrative analysis and
proposed validation, with no fabricated benchmark or partner commitments.
The repository README links the rendered gallery and editable sample.

## Legacy boundary

`scripts/legacy/` and `references/legacy/` preserve the old custom red system for
explicit historical reproduction only. Do not load them for the official-template
workflow. They are not Huawei's official specification.

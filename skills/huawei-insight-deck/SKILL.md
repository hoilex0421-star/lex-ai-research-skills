---
name: huawei-insight-deck
description: >-
  Build Huawei-style restrained-red 16:9 research slides in two page families:
  (A) 市场/洞察论点页 — a quantified-claim title, 「洞察启示」band, left quant chart,
  right same-field comparison cards (市场空间/TAM, 客户画像, 选型分档, 竞品横评, 应用结构占比);
  and (B) 技术研究叙事页 — 学术界/产业界 时间线, 框架/流程图 (stage boxes + arrows),
  技术路径对比 (显式 vs 隐式), 对比/选型表, 案例页, each closing on a red 结论 band.
  Use this WHENEVER an analyst or 算力研究员 wants an executive-facing 洞察/论点/趋势/技术路径
  one-pager in a clean red corporate house style — even if they don't name "Huawei" or "模板".
  Trigger on 「按华为那个模板做一页」「市场空间页」「保守vs乐观」「分场景对比卡」「左图右卡」
  「时间线/发展脉络页」「技术路径/框架图」「显式vs隐式」「对比表/选型表」「洞察启示页」, or whenever
  a data-rigorous one-pager whose every number carries a named source is wanted. Pairs with
  (does not replace) the base pptx skill for build/render/QA mechanics.
---

# Huawei-style 洞察论点页 & 技术研究叙事页

A reusable template + helper library for the executive-facing research one-pager
in a restrained-red corporate house style (modeled on Huawei/Goldman research
slides). It captures both the **visual layout** and — just as important — the
**data-rigor discipline** that makes such a page survive a domain expert
challenging the evidence chain.

It covers **two page families**. Pick the one that matches the job:

- **(A) 市场/洞察论点页** — *"这个市场多大、谁在买、怎么打"*. Quantified-claim title →
  「洞察启示」band → left quant chart → right same-field comparison cards.
  Use for 市场空间/TAM, 客户画像, 选型分档（高中低档）, 竞品横评, 应用结构占比, 成本/趋势拐点.
- **(B) 技术研究叙事页** — *"这项技术怎么演进、有哪些路线、谁在做"*. A claim title →
  one of the narrative archetypes (时间线 / 框架流程 / 技术路径对比 / 对比表 / 案例页) →
  a red 结论 band. Use for 发展脉络/timeline, 技术框架与流程, 显式vs隐式路线, 选型/能力对比表,
  代表团队/论文案例页.

Both families share the same brand system, the same red 论点型标题, the same
"结论先行 + 数据可回溯" discipline, and the same render-QA loop. They differ only
in the middle layout. `references/template-archetypes.md` summarizes the reference
deck this skill was modeled on and maps each archetype to its helpers.

## Order of operations (do not skip)

1. **Research first.** Gather every figure, ratio, date, team name and source the
   page needs. Do NOT open this template until you have the substance. A beautiful
   page on an unsourced number is worse than no page — see
   `references/data-rigor-and-caveats.md`.
2. **Pick the family + archetype** (A or B; which middle layout) and lay out with
   `scripts/deck_helpers.py`. Copy the matching example and mutate it.
3. **Render → eyeball → fix.** Convert to PDF, rasterize, and look for label
   overlaps before shipping. This loop is mandatory, not optional.

## Family A — 市场/洞察论点页 (the 5 structural parts)

Every page is the same five parts, top to bottom. `example_market_page.py` is a
complete worked example.

1. **论点型标题 (`title_band`)** — a *claim* with a **quantified payload** in the
   title itself. Red key clause + black remainder.
   - Good: "各应用场景市场空间：2030 保守 25 万 vs 乐观 ~100 万，家庭弹性最大"
   - Bad: "市场空间分析" (topic, no claim, no number)
2. **「洞察启示」band (`insight_band`)** — a red tag + **2 conclusion-first bullets**,
   each carrying a named driver/signal (a firm, an event, a year). 结论在上、证据在下.
3. **Left: quantified chart (`stacked_bar`, or a line from `seg`)** — every segment
   labeled, totals on top, start/end years, CAGR. Diagonal lines use `seg` (STRAIGHT).
4. **Right: same-field comparison cards (`card`)** — N cards, **identical row labels**
   so the reader scans them as columns ("罗列即对比"). For 算力 audiences the
   能力/capability row should carry a compute or data dimension.
5. **Footnote + footer (`footer`)** — terse on-page caliber note; the **full source
   list with URLs lives in the speaker notes**.

## Family B — 技术研究叙事页 (claim title → archetype → 结论 band)

Same red `title_band` on top and a `conclusion_band` (the red 结论 line) on the
bottom. The middle is ONE of these archetypes — see `example_narrative_page.py`
(slide 1 = timeline, slide 2 = framework + table):

1. **时间线页 (`time_axis` + `event_card` + `tag_chip`/`legend`)** — a central
   `time_axis` (returns tick x-centers); `event_card`s above (学术界) and below
   (产业界), each with a date + 红字产品名 header and a one-line contribution. Category
   `tag_chip`s (场景生成/场景理解…) act as the legend. *Conclusion: 节奏/方向, not a list.*
2. **框架/流程页 (`section_header` + `stage_box` + `arrow`)** — labeled stage boxes
   (建模→运动→渲染) joined by block `arrow`s, optionally grouped by a colored `accent`
   strip. Left category labels via `tag_chip` (输入/输出/算力).
3. **技术路径对比页 (two `section_header` columns + flows + `spec_table`)** — two
   sub-claim headers (显式 vs 隐式), a small flow under each, and a `spec_table`
   comparing them across **identical fields** (可编辑性/物理真实/泛化/算力/代表工作).
4. **对比/选型表页 (`spec_table`)** — a clean grid with a red header row; first column
   is the field, the rest are the compared models/approaches. Cells can be rich runs
   (use RED for the one number/word that matters, e.g. 算力 `cube + SIMT`).
5. **案例页 (`section_header` + `image_ph` + `spec_table`)** — a featured team/product:
   a spec table of the method, `image_ph` slots for result screenshots, a small
   pipeline of `stage_box`+`arrow`. (Web images can't auto-embed — see rigor §7.)

## Visual system (all enforced by the helpers)

- **微软雅黑** everywhere; **C7000B red is the dominant accent** and the **ONLY**
  colour for 重点/结论/title key clause. Large white space, rounded cards, light
  gray borders. 16:9, **13.333 × 7.5 in**.
- **Series shades** (family A): `RED` / `RED2` / `RED3` — shades, not hues; the
  *story* is told by growth and the 判断 line, not by colour.
- **Category chips** (family B only): `BLUE` / `GREEN` / `NAVY` are MUTED category
  tags (场景生成/场景理解, 输入/输出, 显式/隐式) — never used for emphasis or conclusions.
  Keeping conclusions monochrome-red is what keeps the page on-brand.
- Full palette, coordinates and per-part geometry: `references/layout-and-visual-spec.md`.

## Build & QA workflow

```bash
python3 your_build.py                                   # imports deck_helpers
libreoffice --headless --convert-to pdf your.pptx --outdir .
pdftoppm -png -r 200 your.pdf out                       # then VIEW out-1.png
```

Render-QA hard checks (do every time — these are the bugs that actually happen):
- **Zero text overlap.** Data labels, axis labels, stage-box text, table cells and
  the footnote must not collide. If a label sits on a line, move it to open space.
- **Diagonal lines are straight, not stairs** (use `seg`, connector type 1).
- **Arrows sit in the GAP between stage boxes**, not overlapping them; table columns
  don't truncate; chips don't run past the 0.5" right margin (auto-width helps).
- Title and 结论 band stay one line; on-page caliber note ≤3 short lines (rest → notes).

## Data rigor — the part that makes or breaks the page

Applies to BOTH families. Read `references/data-rigor-and-caveats.md`. In brief:

- **Every number carries 指标 + 基准 + 对象.** *What* metric, *vs whom*, *on what benchmark*.
- **Distinguish 总量 (sourced) from 占比/拆分 (often 研判).** Label derived splits as 研判;
  cite both the total's source and the share's source.
- **Caliber must match across a comparison** (人形 / 含四足 / 是否含机械臂; 全球 vs 单一市场).
- **Outliers go in the caliber note, never as the axis or upper bound.**
- **No source, no number.** A search-engine AI summary is NOT a citable source.
- **Web images can't be auto-embedded** — the user must drop the asset into the
  connected project folder; otherwise use `image_ph` as a placeholder + give the link.

## Files

- `scripts/deck_helpers.py` — import this. Family A: `title_band/insight_band/card/
  stacked_bar/seg/footer`. Family B: `tag_chip/legend/section_header/stage_box/arrow/
  time_axis/event_card/image_ph/spec_table/conclusion_band/note`. Plus the palette.
- `scripts/example_market_page.py` — runnable 保守vs乐观 市场 page (family A).
- `scripts/example_narrative_page.py` — runnable timeline + framework/table page (family B).
- `references/template-archetypes.md` — the reference deck's page types + when to use each.
- `references/layout-and-visual-spec.md` — exact coordinates, geometry, palette.
- `references/data-rigor-and-caveats.md` — the rigor checklist with the real failure cases.

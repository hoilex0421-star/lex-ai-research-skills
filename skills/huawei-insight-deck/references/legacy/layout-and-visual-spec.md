> Historical custom design only. Not the official Huawei template; do not use in the default workflow.

# Layout & visual spec

Exact geometry for the Huawei-style market/insight 论点页. Units are inches on a
**13.333 × 7.5** (16:9) slide. The helpers in `scripts/legacy/deck_helpers.py` already
encode these; this file is the reference when you need to deviate or debug.

## Table of contents
- Palette
- Consulting color discipline
- Grid / safe margins
- Part-by-part coordinates
- Chart construction (stacked bar, trend line)
- Common pitfalls

## Palette

| Token | Hex | Use |
|---|---|---|
| RED | C7000B | the ONLY accent: 重点 / 主轴 / 工业 / card strips / title key clause |
| RED2 | D85C5C | second series (商业 / 第二序列) |
| RED3 | EAB3B5 | third series (家庭 / 第三序列) |
| DARK | 1A1A1A | body text |
| MID | 595959 | subtitles / chart subtitle |
| MUTE | 8C8C8C | footnotes / caliber notes |
| GRAYH | 6E6E6E | conservative/neutral totals & labels |
| GRID | D9D9D9 | baselines / gridlines |
| GF | F6F6F6 | insight band fill, alternating card fill |
| PINK | FBECED | conclusion (结论) band fill |
| LINEGRY | E2E2E2 | card / band borders |
| WHITE | FFFFFF | text on red |

Font: **微软雅黑** on latin + ea + cs runs (the helper `_setfont` does all three;
setting only `font.name` leaves CJK glyphs in a fallback face).

## Consulting color discipline

Public McKinsey and BCG materials use different brand colors but share the same
discipline: white space and grayscale carry most of the page; one brand hue
organizes hierarchy; another hue appears sparingly for comparison or status.
McKinsey describes its identity as deep blue on white with high contrast and a
reworked data-visualization system. BCG's 2025 public AI reports are predominantly
deep/bright green, with warm neutral comparison marks and rare semantic alerts.
Use these as visual references, not as brand templates to clone.

### Theme-color budget

- A slide may use at most **three non-neutral theme colors**.
- Default composition: **one dominant + one supporting**. A third color is
  allowed only for a stable semantic role such as risk/status or a genuine route
  distinction.
- White, black, grayscale text/borders, and light tints derived from an active
  theme color do not add a new theme color.
- Photographs and screenshots are excluded from the count, but their surrounding
  frames, captions, overlays, and chart marks are included.
- Pick one palette logic for the slide/deck. Do not mix McKinsey-blue and BCG-green
  systems decoratively.
- A shade may replace another shade in the same role; do not use both just to add
  visual variety.

### Recommended restrained-red recipe

This skill's default remains Huawei-compatible while adopting consulting-style
restraint:

| Role | Token | Hex | Rule |
|---|---|---|---|
| Dominant claim/emphasis | RED | C7000B | titles, conclusions, key number |
| Supporting structure | NAVY | 1F3864 | axes, one route/category family |
| Optional semantic exception | GREEN | 4F8A3D | status or second route only when meaning requires it |

`RED + NAVY` is the default. Add `GREEN` only when a two-route/status distinction
would otherwise be ambiguous. `BLUE` may substitute for `NAVY` on a blue-forward
page, but **BLUE and NAVY must not both appear on that page**.

For a user-requested non-red consulting variant, use the same role structure:

- McKinsey-inspired: deep navy + clear blue; optional warm signal color.
- BCG-inspired: deep green + bright green; optional warm neutral comparison color.

Do not present these as official brand palettes. The reusable rule is the role
discipline and the three-color ceiling.

### Color audit

Call `assert_theme_color_budget(slide)` after constructing each slide. The helper
ignores the template's neutral colors, pale derived fills, and pictures, then
raises an error listing the remaining theme colors if the count exceeds three.

## Grid / safe margins

- Left/right safe margin: **0.5**. Title hairline rule at y=0.96 spans 0.5→12.83.
- Two columns below the insight band:
  - **Left half** (chart): x ≈ 0.6 → 6.45.
  - **Right half** (cards): x ≈ 6.66 → 12.82 (width ≈ 6.16).
- Footer rule at y=7.06; footer text at y=7.12.

## Part-by-part coordinates

**1. Title band** — box (0.5, 0.30, 12.4, 0.60), 20pt bold, ls 1.04, vertically
centered. Red key clause then black remainder, same run sequence. Hairline rule
`hline(0.5, 0.96, 12.33, RED, 2.2)`.

**2. Insight band** — red tag `rect(0.5, 1.06, 1.18, 0.96, RED, rounded)`,
tag text 11.5pt white centered. Body `rect(1.78, 1.06, 11.05, 0.96, GF, border)`,
bullets at (1.98, 1.06, 10.7, 0.96), 9pt, ls 1.16, each led by a red "▪".

**3a. Left chart region** — subtitle at (0.6, 2.02). Legend chips at y≈2.40
(dot d=0.12 + label). Plot region typically `(xl=1.18, yt=2.55, xr=5.6, yb=6.02)`.
Group/year labels under baseline at y≈6.30. Caliber note starts y≈6.46–6.50.

**4. Right cards** — x=6.66, width=6.16. Card strip width default 1.66.
Stack 3 cards in y∈[2.10, 6.55]; give a card with long text (e.g. 实例) more
height (≈1.9) and the others ≈1.4, with ~0.06 gaps. Row labels red bold 7.2pt,
values dark 7.2pt, ls 1.16. **Identical labels across all cards.**

**5. Footer** — `footer(src, brand)`: hairline + source (7pt MUTE, left) + brand
tag (7.5pt RED, right). Optional 结论 band above it:
`rect(0.5, 6.62, 12.33, 0.36, PINK, rounded)` with "结论：…".

## Chart construction

**Stacked bar (`stacked_bar`)** — pass `region=(xl,yt,xr,yb)`, a list of bar dicts
`{x, vals:[bottom..top], total, label_bottom, top_is_red}`, the series colours
(bottom→top), and `ymax`. Position bar x's yourself; group paired bars
(e.g. 保守/乐观) tightly (~0.14 gap) and separate year-groups wider (~0.62).
Segment value labels print inside any segment taller than 0.24"; totals print
above each bar (red if `top_is_red`, else GRAYH).

**Trend line (build from `seg` + `dot`)** — map years to x evenly, values to y via
`y = yb - v*scale`. Draw each segment with `seg(x1,y1,x2,y2)` (STRAIGHT). Add
`dot` markers and value labels in OPEN space (above early points, beside the last).
Threshold lines: `hline(..., dash='dash')` with the label placed at the LEFT end,
just above the line, so it never collides with end-of-line markers on the right.

## Common pitfalls

- **Stair-step "line".** `add_connector(2, ...)` is the elbow connector; a diagonal
  becomes right-angle stairs. Use `seg` (type 1).
- **CJK in wrong font.** Always set typeface on a:latin/a:ea/a:cs (helper does it).
- **Overlapping end-of-line labels vs threshold labels.** Keep threshold labels on
  the left, value labels on the right; never both near the final year.
- **Caliber note overflow.** >3 lines pushes into the footer. Move detail to the
  speaker notes; keep on-page note ≤3 short lines.
- **Shadows.** Every shape sets `shadow.inherit = False`; default theme shadows
  look cheap on this clean layout.

## Family B — 技术研究叙事页 geometry

Same title band (y 0.30, rule at 0.96) and a `conclusion_band` near the bottom
(y≈6.55–6.60). The middle (y≈1.1 → 6.4) holds one archetype.

### Secondary category-chip palette (Family B only)
| Token | Hex | Use |
|---|---|---|
| NAVY | 1F3864 | default supporting category / time-axis band |
| GREEN | 4F8A3D | optional second route or semantic status |
| BLUE | 2E5C9E | substitute for NAVY on a blue-forward page; never use both |
| BLUEF | EAF1FA | very light blue panel fill |
| GREENF | EEF5E9 | very light green panel fill |

This table is an inventory, not permission to use every swatch together. Red stays
the only color for conclusions/emphasis; category colors are muted labels only.
The normal Family B page is `RED + NAVY`, optionally `+ GREEN`.

### Helper geometry
- **`tag_chip(x, y, label, fill, ...)`** — auto-sizes width via `_est_w` (CJK≈1.02·pt,
  latin≈0.56·pt, +0.11" padding each side). Pass `w=` to fix width; `fill=None` for an
  outline chip. Default h=0.26, rounded rad 0.18. Returns end-x for chaining.
- **`legend(x, y, items)`** — inline row of dot+label; returns end-x.
- **`section_header(x, y, w, label, bar=True)`** — red bold sub-claim; `bar=True` puts
  it on a PINK strip (h=0.34). Use two side-by-side for a 显式 vs 隐式 split (left x≈0.55
  w≈6.15; right x≈7.05 w≈6.18).
- **`stage_box(x, y, w, h, title, body=None, accent=None)`** — rounded box; `accent`
  draws a 0.07" colored top strip. Title centered; with `body`, title top + body below.
  Typical h 0.55–0.70 in a flow.
- **`arrow(x, y, w, h, direction='right')`** — block arrow; place in the GAP between
  boxes (w≈0.30–0.36, h≈0.16, y = box_y + ~0.12 to vertically center on a 0.62 box).
- **`time_axis(x, y, w, labels, color=NAVY)`** — navy band (h 0.30) with evenly spaced
  white tick labels; **returns the list of tick x-centers**. Put 学术界 cards above,
  产业界 cards below. A 4-tick axis at x=0.55 w=12.68 → centers near 2.14/5.31/8.48/11.65.
- **`event_card(x, y, w, h, head_runs, body, img=True)`** — rounded card; with `img=True`
  an `image_ph` occupies the top ~42% then the header + body. Typical w 2.75, h 1.30,
  4-across with ~0.25 gaps starting x=0.55.
- **`image_ph(x, y, w, h, caption)`** — F2F2F2 placeholder + faint "图/截图" + optional
  caption below. Use wherever a real screenshot will be dropped in later.
- **`spec_table(x, y, w, col_w, headers, rows, row_h=0.30)`** — red header row + zebra
  body. `col_w` = list of column widths (sum ≈ w). First column left-aligned (the field),
  rest centered. Cells may be a rich run-list `[(text,size,color,bold),...]` — use RED for
  the one differentiator. Returns y below the table. For a 5-row 显式vs隐式 table use
  col_w≈[2.2, 5.24, 5.24], row_h≈0.46.
- **`conclusion_band(runs, y=6.60, tag="结论")`** — full-width PINK strip + red 结论 chip +
  bold takeaway (lead clause RED). `tag=None` drops the chip. This is Family B's mandatory
  bottom line (the reference deck ends almost every page this way).
- **`note(x, y, w, txt)`** — small gray 注/caption line.

### Route evolution three-panel geometry
Use for "当前方案 → 方向一 → 方向二" pages.

- Keep the claim band at y≈1.18 and start the three panels no earlier than y≈2.2,
  so the page has a clear breathing gap between title and route map.
- Three large dashed panels usually work at:
  - 当前方案: x≈0.35, y≈2.28, w≈3.95, h≈4.10
  - 方向一: x≈5.05, y≈2.28, w≈3.75, h≈4.10
  - 方向二: x≈8.95, y≈2.28, w≈4.10, h≈4.10
- If the middle/right panels need equal strategic weight, keep their headers aligned
  and use only one red "演进" arrow from the current panel toward the future panels.
- Put short representative notes at each panel's bottom (e.g. "代表案例 A").
  Do not add a second comparison table on the same slide unless body text remains
  comfortably above ~7pt.

### Data-flywheel case-page geometry
Use for "糖水 demo 数据 vs 牛奶真实数据" pages.

- Top contrast panels: left x≈0.35, w≈4.6; right x≈5.45, w≈7.55; y≈1.65, h≈2.40.
  The right panel can carry 5 small noise boxes plus a horizontal flywheel strip.
- Middle claim strip: x≈0.35, y≈4.20, w≈12.65, h≈0.34. State the four dimensions
  inline instead of using a separate dimension-card row when space is tight.
- Bottom case cards: three equal cards at x≈0.45 / 4.85 / 9.25, y≈4.65, w≈3.75,
  h≈2.00-2.20. Each card hierarchy is:
  1) gray header with company name,
  2) three same-field rows (落地方式 / 采集数据 / 飞轮闭环),
  3) image band inside the card.
- Images must sit inside card boundaries and align to a shared top or bottom.
  If source images have different aspect ratios, preserve aspect ratio and center
  them; do not stretch just to make widths identical.

### Family B pitfalls
- **Arrow overlapping a box.** Always leave a real gap; an arrow drawn over a box edge
  looks like a bug. Compute box right-edge + small gap for the arrow x.
- **Chip running off-canvas.** Auto-width helps, but a far-right chip (学术界/产业界 tags)
  must satisfy `x + w ≤ 12.83`. Give a fixed `w` and check.
- **Table text truncation.** If a cell wraps to 2 lines, raise `row_h`; don't shrink the
  font below ~7.5pt. Keep the field column narrow and the compared columns wide.
- **Too many hues.** Resist coloring stage boxes by hue. Use the gray box + a single
  `accent` strip, and let red carry the conclusion. Run
  `assert_theme_color_budget(slide)`; more than three theme colors is a delivery
  blocker, not a stylistic preference.
- **One-page over-compression.** If a page needs both route mechanics and case evidence,
  split it. The Huawei style tolerates density, but not when mechanism, criteria, and
  screenshots fight for the same vertical band.
- **Floating screenshots.** Case-card images must be visually owned by the card. If a
  screenshot crosses or sits below the card border, enlarge/reposition the card before
  delivery.

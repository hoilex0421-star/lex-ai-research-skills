# Data rigor & caveats

This page type is built for analyst work that gets reviewed by someone who
challenges the evidence chain. A clean layout on a shaky number fails the review.
Each rule below is followed by the real failure it prevents, so you understand
*why* it matters rather than treating it as a rote MUST.

## 1. Every number carries 指标 + 基准 + 对象

A figure with no metric, baseline and object is unreadable. State *what* metric,
*relative to whom/what*, *on which test set / over what period*.

- Bad: "SOTA VLA 绝对 +18~46%" — +what? vs whom? where?
- Good: "换上更强底座，同款 VLA 真机任务成功率绝对 +18~46 个百分点 vs 官方基线（SimplerEnv 等）"
- Same for soft words: "提升 / 增强 / 逼近 / 接近" must each say *提升什么、多少、相对谁*.

## 2. Separate 总量 (sourced) from 占比 / 拆分 (usually 研判)

Firms publish totals and qualitative application paths; they rarely publish
per-segment unit counts per year. So a per-scenario number is almost always:

> per-scenario value = **sourced total** × **sourced share path** → **a 研判 split**

Label the split as 研判/估算 on the page, and in the notes cite *both* the total's
source *and* the share path's source. Don't present a derived split as if a firm
published it.

Real case: a 三场景 table's 工业/商业/家庭 cells were derived this way. The honest
footnote reads "各格＝总量 × 应用结构(高盛/摩根士丹利) 的研判拆分；机构未逐场景披露单位数".

## 3. Caliber must match across any comparison

The single most dangerous trap on a market page. If the conservative axis is
**humanoid-only** but the optimistic anchor secretly includes **quadrupeds** (or
industrial arms, or a single regional market), the comparison silently inflates
the optimistic side. Always state scope: 人形 only / 含四足 / 是否含机械臂 / 全球 vs 单一市场.

Real case: an optimistic "SAG 81万/2030" anchor turned out to be **humanoid +
quadruped, 69% quadruped** in 2025 — i.e. mostly mechanical dogs. Pure-humanoid
from the same source was ~25万 (≈ the conservative Goldman figure). The fix was to
flag "含四足、且四足为主" and lean the humanoid-only optimistic case on a
humanoid-defined source instead. Industrial robotic arms (IFR, ~500k+ installs/yr)
are a separate existing market and belong in NONE of these humanoid forecasts.

## 4. Outliers are not featured

A lone figure far above every other source is probably a different caliber
(cumulative vs annual, capacity vs shipment, demand vs sales, one market vs global).
Put it in the caliber note as a labeled possibility; never use it as the chart axis
or the upper bound.

Real case: "中信 ~500万/2030" sat above most firms' 2035 numbers. It stays in the
note as "激进离群口径，不作主轴"; the axis tops out at the credible ~100–300万 band.

## 5. No source, no number — and a search summary is not a source

Before attributing a figure to a firm, verify it against the **primary report**
(the firm's own PDF/article). Search-engine answer boxes and AI summaries
synthesize and can invent attributions.

Real case: a "deployment split 制造35% / 物流25% / 科研15%" was carried on a slide
attributed to Goldman. It traced back to a search-engine AI summary; no Goldman (or
any) report contains it. It was replaced with a citable Morgan Stanley figure
("long-run ~90% industrial+commercial / ~10% household") plus Goldman's "2030 almost
entirely industrial". Rule of thumb: if you can't point to the firm's own document,
either find one or drop the attribution and mark the number 研判/示意.

## 6. Three-bucket caliber labeling

Tag each external figure as one of: **官方/机构发布** (firm's published number),
**厂商自报** (a company's own claim about itself), or **研判/估算** (your derivation).
Keep them visually distinct and never let a 研判 number masquerade as 官方.

## 7. Web-image embedding is constrained (tooling reality)

Images on the web (paper figures, blog charts, GitHub raw) cannot be pulled into
the workspace automatically: base64 transfer is blocked, direct download is
disallowed, and a browser download lands in the user's local Downloads, not the
connected folder. So:

- To embed a figure, the **user must save it into the connected project folder**;
  then you can read, crop and place it. Or use local assets already in the project.
- Otherwise, give the **direct link** and open it in the user's browser to save.
- When suggesting figures, name *which paper / which figure / the direct link / why
  it evidences the claim*, and mark the source caliber.

## 8. Traceability — speaker notes carry the full sourcing

The on-page caliber note is terse. The slide's **speaker notes** must hold the full
chain: each figure → primary source → URL → caliber, plus the derivation of any
研判 split (e.g. "保守2030 工业15/商业10/家庭0=25"). A reviewer's "where's this
from?" should be answered in one click. Write it as you build, not after.

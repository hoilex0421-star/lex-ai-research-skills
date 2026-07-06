# Reference-deck archetypes (技术研究叙事页)

This skill's Family B was distilled from a 23-page Huawei research deck on
空间智能 / 世界模型 / 具身智能 (embodied & spatial intelligence). This file
summarizes that deck's repeatable design system so you can reproduce its pages.
Family A (市场/洞察论点页) is documented in `layout-and-visual-spec.md`.

## What every page in the reference deck shares

- **16:9, white background, dense but ordered.** One page = one argument.
- **论点型标题 on top.** A full *claim* sentence, key phrase in **red**, often on a
  light-red highlight bar spanning the slide width. Never a bare topic. Examples
  from the deck: "空间智能/世界模型2024年开始逐渐成为热点，学术界产业界在不断发布研究和产品";
  "多模态大模型在3D空间生成和理解任务上，泛化能力不足制约应用落地".
- **A red 结论/判断 line at the bottom.** A full-width light strip whose lead clause
  is red and bold — the "so what". This is the `conclusion_band` helper.
- **微软雅黑.** Red (≈C7000B) is the dominant accent and the only colour for
  conclusions/emphasis. Secondary **blue / green / navy** appear ONLY as small
  category tags (场景生成/场景理解, 输入/输出, 显式/隐式). Neutral grays for boxes/borders.
- **Screenshot-heavy.** Real paper/product screenshots in a grid, each captioned with
  date + team + 红字产品名. Since web images can't auto-embed, use `image_ph` slots and
  have the user drop real assets into the connected folder.
- **Source/注 line** in small gray at the bottom; full sourcing in speaker notes.

## The five recurring middle layouts

| # | Archetype | What it answers | Helpers |
|---|---|---|---|
| 1 | **时间线页** (学术界/产业界) | 发展脉络、节奏 | `time_axis` + `event_card` + `tag_chip`/`legend` |
| 2 | **框架/流程页** | 一个系统怎么运转 | `section_header` + `stage_box` + `arrow` + `tag_chip` |
| 3 | **技术路径对比页** | 两条路线各自怎样、谁强谁弱 | two `section_header` + flows + `spec_table` |
| 4 | **对比/选型表页** | 横向比模型/方案/分档 | `spec_table` (rich-run cells) |
| 5 | **案例页** | 一个代表团队/论文做了什么 | `section_header` + `image_ph` + `spec_table` + flow |

### 1. 时间线页
Central horizontal time axis (a navy band with white date ticks). 学术界 events as
cards ABOVE the axis, 产业界 events BELOW. Each card: a small screenshot, a header
line "日期 + 红字产品名", one line of contribution. Category chips (生成 vs 理解) sit
top-left as a legend. Conclusion states the *trend/direction*, never re-lists events.

### 2. 框架/流程页
Left-edge category labels (输入 → … → 输出, or 显式表征/隐式表征). Process stages as
rounded boxes joined by red block arrows (建模 → 运动 → 渲染). Stage groups can share a
thin colored top strip (`accent`). Keep each box to a title + ≤1 short line.

### 3. 技术路径对比页
Two columns, each a red sub-claim header + a tiny stage flow, then a single
`spec_table` underneath comparing both routes across **identical fields**
(可编辑性 / 物理真实 / 泛化-长程 / 算力诉求 / 代表工作). Put the differentiating number or
keyword in red inside the cell (e.g. 算力 "训练高（cube + SIMT）").

### 4. 对比/选型表页
A clean grid: red header row, first column = the dimension, remaining columns = the
compared models/approaches. Zebra body rows. This is the workhorse for 选型分档 and
竞品横评 when a chart isn't the right tool.

### 5. 案例页
A featured team/product (often a professor + lab). A method `spec_table` (输入/网络/
渲染/关键路径…), `image_ph` slots for result screenshots with captions, and a small
`stage_box`+`arrow` pipeline of the method. Credentials/affiliation in a side panel.

## Mapping a request to an archetype

- "发展脉络 / 这两年都发生了什么 / 谁先谁后" → **时间线页**.
- "这套系统/方法是怎么跑通的 / 画个框架图" → **框架/流程页**.
- "A 路线 vs B 路线 / 显式 vs 隐式 / 端云" → **技术路径对比页**.
- "横向比这几个模型/产品/方案 / 选型分档" → **对比/选型表页** (or Family A cards if each
  needs a rich multi-field profile).
- "讲清楚某团队/某论文做了什么" → **案例页**.
- "这个市场多大 / 谁在买 / 保守vs乐观 / TAM" → **Family A 市场/洞察论点页**.

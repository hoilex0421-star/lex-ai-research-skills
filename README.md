# Huazi PPT Skill

`huawei-insight-deck` 是一个给 Codex 使用的 PPT 研究页技能，用来快速生成 **华为/咨询公司风格的克制红 16:9 高管汇报页**。它适合把市场判断、技术路线、竞品对比、趋势脉络等材料，整理成一页可直接放进汇报 deck 的结构化 PPT。

本仓库同时提供两个可独立调用的技能：

- `$huawei-insight-deck`：生成华为风格的单页洞察、市场分析和技术叙事页面。
- `$tech-research-deck`：基于文章和互联网研究，生成完整的技术研究阅读型 PPT。

`tech-research-deck` 的页面正文默认不使用不必要的引号，顶部结论条统一标注为“洞察”。

这个 skill 的目标不是只把页面做得好看，而是把页面做成：

- **结论先行**：标题直接给判断和关键数字，不写空泛主题。
- **数据可回溯**：每个数字都要求有口径、对象、来源，来源放脚注或 speaker notes。
- **一页讲清楚**：左侧图表/流程承载核心证据，右侧卡片/表格承载同字段对比。
- **可编辑 PPT**：使用 PowerPoint 原生形状、文字、表格、图表，后续可以继续改。

## 使用后的效果

使用这个 skill 后，Codex 会优先生成两类完整页面。

### A. 市场 / 洞察论点页

适合回答：“这个市场多大、谁在买、怎么打、增长拐点在哪里？”

典型页面结构：

```text
论点型标题：2030 保守/乐观市场空间、CAGR、关键判断
洞察启示：2 条结论先行 bullet
左侧：市场空间图、结构占比图、增长曲线或堆叠柱
右侧：同字段比较卡片，例如 TAM / 客户画像 / 选型分档 / 竞品横评
底部：口径说明、来源、结论 band
```

可用于：

- 市场空间 / TAM 测算
- 保守 vs 乐观情景
- 客户画像和采购分层
- 产品高中低档选型
- 竞品横向对比
- 应用场景结构占比
- 成本下降或商业模式拐点

示例请求：

```text
$huawei-insight-deck
按华为那个模板做一页，主题是具身智能一体机市场空间：
左边画 2025-2030 市场规模增长，右边做保守/中性/乐观三种场景卡片，
每个数字都标来源。
```

### B. 技术研究叙事页

适合回答：“这项技术怎么演进、路线怎么分、不同方案如何选？”

典型页面结构：

```text
论点型标题：技术路线判断
中部主体：时间线 / 框架流程 / 显式vs隐式路线 / 选型表 / 案例页
底部：红色结论 band，总结技术节奏、路线取舍或算力含义
```

可用于：

- 学术界 / 产业界发展时间线
- 技术框架和输入-方法-输出流程
- 显式路线 vs 隐式路线对比
- 模型、系统、芯片、平台选型表
- 代表论文、团队、产品案例页

示例请求：

```text
$huawei-insight-deck
做一页技术路线页，比较机器人世界模型的显式建模路线和隐式生成路线：
中间放两条流程，下面做对比表，字段包括可编辑性、物理真实、泛化、算力、代表工作。
```

## 页面风格

- 画布：16:9，适合 PowerPoint 汇报。
- 主色：克制红 `#C7000B`，用于标题重点、结论、关键数字。
- 字体：微软雅黑，适合中文商业汇报。
- 版式：白底、浅灰边框、红色强调，不做花哨渐变。
- 图表：优先使用清晰的趋势线、堆叠柱、对比表、流程框。
- 信息密度：面向高管阅读，一页只讲一个核心判断。

## 适合谁用

这个 skill 更适合研究员、战略分析、产品规划、算力/AI 产业分析场景，尤其适合：

- 需要把零散材料压缩成一页洞察页
- 需要把技术路线讲成管理层能看懂的结构
- 需要每个数字和判断都能追溯来源
- 需要输出可编辑 PPT，而不是一张不可改的图片

## 安装

Clone this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/hoilex0421-star/Huazi-ppt-skill.git ~/.codex/skills/huawei-insight-deck
ln -s ~/.codex/skills/huawei-insight-deck/skills/tech-research-deck ~/.codex/skills/tech-research-deck
```

Then restart Codex or open a new thread. Use either skill as:

```text
$huawei-insight-deck
$tech-research-deck
```

## Contents

- `SKILL.md` - skill trigger rules and workflow
- `references/` - layout, archetype, and data-rigor references
- `scripts/` - helper library and runnable examples
- `agents/` - agent configuration
- `skills/tech-research-deck/` - complete technical research deck skill

## 使用建议

为了得到更好的页面，请在请求里尽量提供：

- 主题和目标读者，例如“给 SP 战略汇报用”
- 想做的页面类型，例如“市场空间页 / 技术路线页 / 竞品对比页”
- 已知数据、来源链接、口径说明
- 你希望保留的结论或判断

如果没有完整数据，Codex 会先帮你补研究和口径，再按模板出页。

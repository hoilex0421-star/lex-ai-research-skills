---
name: tech-research-deck
description: >-
  Create research-analyst reading decks that explain a technology's architecture,
  core modules, technical routes, representative players/papers/products, and
  development trends. Use when the user asks to梳理技术、讲清楚技术架构、技术路线、
  发展趋势、路线演进、技术全景、产业技术研究、技术研究页、算力启示,
  or to turn papers, product notes, screenshots, or fragmented technical opinions
  into a dense Chinese reading PPT. Pair with huawei-insight-deck for the final
  restrained-red slide style and render-QA; switch to investment-recommendation-deck
  when the task becomes company-specific investment judgement.
---

# Tech Research Deck

Use this skill when the job is to play the **research analyst**: make a complex
technology understandable, defensible, and slide-ready.

Use `$huawei-insight-deck` after the research structure is clear to build the
visual slides.

## Inputs This Skill Handles

- A technical topic or question, such as embodied AI models, world models, AI
  Infra, inference optimization, data flywheels, edge compute, or evaluation.
- Papers, websites, screenshots, PPT pages, Markdown notes, or rough opinions.
- A request to build a chapter in a reading deck, not necessarily a full deck.
- A requirement to explain implications for compute, platform, data, or hardware.

## Outputs This Skill Should Produce

- A slide-ready research outline with clear page claims.
- A technical architecture map or route split.
- A comparison of technical routes using identical dimensions.
- A trend judgement with evidence and caveats.
- Suggested Huawei-style page archetypes to execute with `$huawei-insight-deck`.

## Communication Job

By the end, the reader should understand:

- what the technology is and how the system is structured;
- which modules matter most;
- which technical routes exist and why they differ;
- where the field is moving;
- what the trend implies for compute, data, AI Infra, products, or ecosystem.

Do not turn a technology research deck into a company recommendation unless the
user explicitly asks for investment judgement. Use `$investment-recommendation-deck`
for that.

## Workflow

1. **Frame the technology boundary.**
   Define the domain, system boundary, upstream/downstream modules, and what is
   out of scope.

2. **Build the architecture map.**
   Identify the major layers and dependencies. For AI/robotics topics, usually
   separate model, data, infra/runtime, evaluation, hardware/deployment, and
   application scenarios.

3. **Split technical routes.**
   Describe each route as `input -> method -> output -> tradeoff`. Compare routes
   by identical dimensions such as scalability, data requirement, inference cost,
   generalization, engineering maturity, and representative players.

4. **Locate the trend.**
   Explain what is changing and why now: model architecture, data availability,
   benchmark/evaluation, deployment constraint, cost curve, regulation, or user
   demand.

5. **Translate to implications.**
   End each section with the "so what" for the intended audience, especially
   compute platform implications when the user is a算力研究员.

6. **Build reading slides.**
   Use `$huawei-insight-deck` for page layout. Read
   `references/technical-reading-deck-patterns.md` when choosing slide sequence
   and page archetypes.

## Slide Sequence Patterns

For most technical research decks:

1. 技术全景架构页
2. 核心模块拆解页
3. 技术路线演进页
4. 代表玩家/论文/产品案例页
5. 数据、Infra、评测或部署瓶颈页
6. 趋势判断和对算力/平台的启示页

For a short one-page explanation, use only:

- one claim title;
- one architecture or route diagram;
- one comparison/case evidence block;
- one judgement line.

## Evidence Rules

- Use primary or reliable sources for papers, products, benchmarks, and company
  claims when web research is needed.
- Separate confirmed facts from analyst judgement.
- Do not overstate performance claims without benchmark, date, and object.
- Use representative examples to clarify routes, not to imply market leadership
  unless evidence supports that claim.

## Slide Copy Rules

- Avoid quotation marks in slide body copy unless they are necessary for a
  verbatim quote, an official product/technical term, or a term whose wording
  itself is being discussed.
- Rewrite emphasis as a direct statement instead of wrapping phrases in Chinese
  or English quotation marks. For example, use
  `具身数据已成为独立赛道，但规模化供给尚未等于可持续盈利`.
- Label the top-of-page conclusion or takeaway strip `洞察`, not `核心判断`.

## References

- Read `references/technical-reading-deck-patterns.md` for detailed page patterns,
  wording heuristics, and common technical-route structures.

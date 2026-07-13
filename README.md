# Lex AI Research Skills

**Research is a system, not a document.**

[English](README.md) | [简体中文](README.zh-CN.md)

A library of reusable Codex skills for industrial research, technology analysis, evidence organization, and executive communication. It packages a personal research method into installable workflows that can be used independently or combined from question framing through editable presentation delivery.

## Available Skills

| Skill | Purpose | Best for | Main output |
| --- | --- | --- | --- |
| `tech-research-deck` | Structures a research problem, verifies evidence, decomposes architectures and technical routes, compares representative cases, and develops defensible trend judgments. | Technology landscapes, industrial value chains, route comparisons, system architecture, product or paper analysis, data and infrastructure implications, and forward-looking research. | A source-aware, slide-ready research narrative with architecture maps, route decompositions, same-field comparisons, case evidence, trend judgments, and page-level claims. |
| `huawei-insight-deck` | Turns established judgments into consistent, editable, executive-readable pages using a restrained visual system, reusable layout components, and render QA. | Dense reading slides, executive one-pagers, comparison tables, route diagrams, evidence cards, page polishing, and final presentation production. | An editable 16:9 PowerPoint deck with consistent page structure, native elements, source notes, and visually inspected renders. |

`tech-research-deck` owns the research question, evidence, architecture, routes, cases, and trends. `huawei-insight-deck` owns the conversion of an established argument into consistent, editable pages for executive reading. Each skill can be used on its own, or they can be chained when a task needs both research development and presentation production.

## Why This Repository Exists

Reusable research quality does not come from a single prompt. It comes from a repeatable method for framing the question, collecting and qualifying evidence, comparing alternatives on consistent dimensions, writing a clear claim for each page, and checking the rendered result before delivery.

This repository makes that method explicit. The skills preserve the decisions that are easy to lose between projects: where the research boundary sits, what counts as sufficient evidence, which comparison fields remain stable, how facts are separated from analyst judgment, and how a page is validated after construction. The result is a working library for producing research that is easier to inspect, update, and communicate.

## How It Works

```text
source material
  -> research framing
  -> evidence and source verification
  -> architecture and route decomposition
  -> page-level claims
  -> slide construction
  -> render and visual QA
  -> editable PPT output
```

- **Claim-first:** each page starts with the conclusion it must establish. Evidence, diagrams, and comparisons are selected to support that claim rather than accumulated without hierarchy.
- **Traceability:** important facts, numbers, benchmark results, and company statements retain their source, date, object, and measurement context. Confirmed facts remain distinct from analyst judgment.
- **Same-field comparison:** competing routes, products, cases, or scenarios are compared using the same dimensions so that differences are meaningful rather than rhetorical.
- **Editable delivery:** final pages use native PowerPoint text, shapes, tables, and charts wherever practical. The deck remains usable after delivery instead of becoming a set of flattened images.

## Quick Start

Use the research skill when the question is still being defined or the evidence and technical structure need to be developed:

```text
$tech-research-deck
```

Use the presentation skill when the argument already exists and needs to become a consistent, executive-readable deck or one-pager:

```text
$huawei-insight-deck
```

For an end-to-end assignment, start with `$tech-research-deck` to establish the research structure and page claims, then use `$huawei-insight-deck` to construct, render, inspect, and deliver the editable presentation.

## Installation

### Symlink installation

Symlinks keep the installed skills connected to the cloned repository, so repository updates are immediately available in Codex.

```bash
git clone https://github.com/hoilex0421-star/lex-ai-research-skills.git
cd lex-ai-research-skills
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/huawei-insight-deck" ~/.codex/skills/huawei-insight-deck
ln -s "$PWD/skills/tech-research-deck" ~/.codex/skills/tech-research-deck
```

### Direct copy

Use direct copies when the installed skills should remain independent of the cloned repository.

```bash
mkdir -p ~/.codex/skills
cp -R skills/huawei-insight-deck ~/.codex/skills/huawei-insight-deck
cp -R skills/tech-research-deck ~/.codex/skills/tech-research-deck
```

Restart Codex or open a new task after installation so the skills are discovered.

## Usage Examples

### Technology research

```text
$tech-research-deck
Build an executive research deck on embodied AI data infrastructure. Define the industry boundary, map the value chain from collection and teleoperation to processing, simulation, evaluation, and delivery, compare real-world and synthetic-data routes on consistent dimensions, identify representative companies and projects with traceable sources, and conclude with evidence-based implications for model training and AI infrastructure through 2028.
```

### Executive presentation production

```text
$huawei-insight-deck
Turn the approved embodied AI data infrastructure research outline into an editable 16:9 executive reading deck. Use one claim per page, a restrained red visual system, native PowerPoint elements, concise source notes, and consistent comparison layouts. Render the full deck, inspect every page for clipping, overlap, hierarchy, and source readability, then deliver the editable PPTX.
```

## Case Gallery

### Embodied Data Industry Research: From Data Factories to Physical AI Infrastructure

This is a real output example produced with the research and presentation workflow in this repository. It demonstrates how a broad industrial question can be turned into an evidence-led narrative, a structured industry model, an operating workflow, and a forward outlook. The source PPTX is not provided for download.

| Research framing | Industry architecture |
| --- | --- |
| ![Research framing: the scope and central thesis of the embodied data industry research](assets/cases/embodied-data-industry/cover.png) | ![Industry architecture: the embodied data value chain and infrastructure layers](assets/cases/embodied-data-industry/industry-chain.png) |
| **Research framing:** defines the research boundary, audience, and central question. | **Industry architecture:** maps the participants, layers, and value flow across the industry. |

| Operating workflow | Forward outlook |
| --- | --- |
| ![Operating workflow: how an embodied data factory collects, processes, validates, and delivers data](assets/cases/embodied-data-industry/data-factory-workflow.png) | ![Forward outlook: evidence-based development outlook for the embodied data industry from 2026 to 2028](assets/cases/embodied-data-industry/outlook-2026-2028.png) |
| **Operating workflow:** explains how a data factory turns collection into validated training assets. | **Forward outlook:** summarizes the expected transition toward physical AI infrastructure from 2026 to 2028. |

## Repository Structure

```text
lex-ai-research-skills/
├── README.md
├── README.zh-CN.md
├── assets/
│   └── cases/
│       └── embodied-data-industry/
│           ├── cover.png
│           ├── industry-chain.png
│           ├── data-factory-workflow.png
│           └── outlook-2026-2028.png
└── skills/
    ├── huawei-insight-deck/
    │   ├── SKILL.md
    │   ├── agents/
    │   ├── references/
    │   └── scripts/
    └── tech-research-deck/
        ├── SKILL.md
        ├── agents/
        └── references/
```

Each skill is self-contained. Its `SKILL.md` defines when to use it and how the workflow operates; supporting references hold detailed research or layout rules; scripts provide deterministic presentation helpers where production requires them.

## Quality Principles

- **Claim-first pages:** one page carries one defensible argument, stated before supporting detail.
- **Evidence traceability:** material facts and numbers preserve their source, date, scope, and measurement context; source notes remain connected to the claim they support.
- **Consistent comparison dimensions:** routes, products, companies, and cases are evaluated using identical fields wherever a direct comparison is intended.
- **Direct body copy:** body text avoids unnecessary quotation marks. Quotation marks are reserved for verbatim language, official terms, or wording that is itself under analysis.
- **Standard conclusion label:** the top conclusion strip is labeled `洞察`, not `核心判断`.
- **Editable PowerPoint:** text, shapes, tables, and charts remain editable so the output can be reviewed and revised after delivery.
- **Render QA:** every completed deck is rendered and visually inspected for overlap, clipping, alignment, hierarchy, image placement, and source-note readability.

## What Comes Next

The library will continue to add reusable skills for research, analysis, and communication as the underlying methods become stable enough to package and maintain.

# GitHub AI Research Skills Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform `Huazi-ppt-skill` into the renamed, bilingual `lex-ai-research-skills` repository with two independently installable skills and a dedicated real-output gallery.

**Architecture:** Keep the repository root as the presentation and navigation layer, and place every installable skill under `skills/<skill-name>/`. Treat English and Chinese READMEs as equal entry points with matching section structure, while keeping all PPT screenshots confined to one case-gallery section in each README.

**Tech Stack:** Git, GitHub CLI, Markdown, Codex skill folders, PNG slide exports

---

## File Structure

Files created or moved by this implementation:

```text
README.md
README.zh-CN.md
.gitignore
assets/cases/embodied-data-industry/
  cover.png
  industry-chain.png
  data-factory-workflow.png
  outlook-2026-2028.png
skills/huawei-insight-deck/
  SKILL.md
  agents/openai.yaml
  references/data-rigor-and-caveats.md
  references/layout-and-visual-spec.md
  references/template-archetypes.md
  scripts/deck_helpers.py
  scripts/example_market_page.py
  scripts/example_narrative_page.py
skills/tech-research-deck/
  SKILL.md
  agents/openai.yaml
  references/technical-reading-deck-patterns.md
```

Responsibilities:

- `README.md`: complete English project introduction, installation guide, usage examples, and gallery.
- `README.zh-CN.md`: complete Chinese project introduction with the same information architecture.
- `.gitignore`: excludes local brainstorming artifacts and macOS metadata.
- `assets/cases/embodied-data-industry/`: stores the four public gallery images only.
- `skills/huawei-insight-deck/`: contains the complete independently installable visual-slide skill.
- `skills/tech-research-deck/`: retains the complete independently installable technology-research skill.

### Task 1: Protect Local Artifacts And Migrate The Huawei Skill

**Files:**
- Create: `.gitignore`
- Move: `SKILL.md` to `skills/huawei-insight-deck/SKILL.md`
- Move: `agents/openai.yaml` to `skills/huawei-insight-deck/agents/openai.yaml`
- Move: `references/data-rigor-and-caveats.md` to `skills/huawei-insight-deck/references/data-rigor-and-caveats.md`
- Move: `references/layout-and-visual-spec.md` to `skills/huawei-insight-deck/references/layout-and-visual-spec.md`
- Move: `references/template-archetypes.md` to `skills/huawei-insight-deck/references/template-archetypes.md`
- Move: `scripts/deck_helpers.py` to `skills/huawei-insight-deck/scripts/deck_helpers.py`
- Move: `scripts/example_market_page.py` to `skills/huawei-insight-deck/scripts/example_market_page.py`
- Move: `scripts/example_narrative_page.py` to `skills/huawei-insight-deck/scripts/example_narrative_page.py`

- [ ] **Step 1: Add repository-local exclusions**

Create `.gitignore` with exactly:

```gitignore
.DS_Store
.superpowers/
```

- [ ] **Step 2: Create the destination directories**

Run:

```bash
mkdir -p skills/huawei-insight-deck/agents
mkdir -p skills/huawei-insight-deck/references
mkdir -p skills/huawei-insight-deck/scripts
```

Expected: all three destination directories exist.

- [ ] **Step 3: Move the tracked skill files with Git history**

Run:

```bash
git mv SKILL.md skills/huawei-insight-deck/SKILL.md
git mv agents/openai.yaml skills/huawei-insight-deck/agents/openai.yaml
git mv references/data-rigor-and-caveats.md skills/huawei-insight-deck/references/data-rigor-and-caveats.md
git mv references/layout-and-visual-spec.md skills/huawei-insight-deck/references/layout-and-visual-spec.md
git mv references/template-archetypes.md skills/huawei-insight-deck/references/template-archetypes.md
git mv scripts/deck_helpers.py skills/huawei-insight-deck/scripts/deck_helpers.py
git mv scripts/example_market_page.py skills/huawei-insight-deck/scripts/example_market_page.py
git mv scripts/example_narrative_page.py skills/huawei-insight-deck/scripts/example_narrative_page.py
```

Expected: the old root-level `SKILL.md`, `agents/`, `references/`, and `scripts/` no longer contain tracked files.

- [ ] **Step 4: Verify internal relative references still resolve**

Run:

```bash
test -f skills/huawei-insight-deck/references/template-archetypes.md
test -f skills/huawei-insight-deck/references/layout-and-visual-spec.md
test -f skills/huawei-insight-deck/references/data-rigor-and-caveats.md
test -f skills/huawei-insight-deck/scripts/deck_helpers.py
test -f skills/huawei-insight-deck/scripts/example_market_page.py
test -f skills/huawei-insight-deck/scripts/example_narrative_page.py
rg -n "references/|scripts/" skills/huawei-insight-deck/SKILL.md
```

Expected: every path mentioned by `SKILL.md` exists relative to `skills/huawei-insight-deck/`.

- [ ] **Step 5: Verify both skill identities**

Run:

```bash
rg -n "^name: huawei-insight-deck$" skills/huawei-insight-deck/SKILL.md
rg -n "^name: tech-research-deck$" skills/tech-research-deck/SKILL.md
```

Expected: one exact match for each skill name.

- [ ] **Step 6: Commit the structural migration**

Run:

```bash
git add .gitignore skills
git commit -m "Reorganize repository as a multi-skill library"
```

Expected: one commit containing the ignore rules and skill directory migration, with no `.superpowers/` content.

### Task 2: Add The Embodied Data Industry Case Gallery Assets

**Files:**
- Create: `assets/cases/embodied-data-industry/cover.png`
- Create: `assets/cases/embodied-data-industry/industry-chain.png`
- Create: `assets/cases/embodied-data-industry/data-factory-workflow.png`
- Create: `assets/cases/embodied-data-industry/outlook-2026-2028.png`

Source directory:

```text
/Users/lex/Documents/lexnote/01-项目-具身智能洞察2026/outputs/具身数据产业研究-从数据工厂到物理AI基础设施-v0.1/
```

- [ ] **Step 1: Create the gallery directory**

Run:

```bash
mkdir -p assets/cases/embodied-data-industry
```

Expected: the target directory exists.

- [ ] **Step 2: Copy and rename the selected rendered slides**

Run:

```bash
cp "/Users/lex/Documents/lexnote/01-项目-具身智能洞察2026/outputs/具身数据产业研究-从数据工厂到物理AI基础设施-v0.1/slide-1.png" assets/cases/embodied-data-industry/cover.png
cp "/Users/lex/Documents/lexnote/01-项目-具身智能洞察2026/outputs/具身数据产业研究-从数据工厂到物理AI基础设施-v0.1/slide-3.png" assets/cases/embodied-data-industry/industry-chain.png
cp "/Users/lex/Documents/lexnote/01-项目-具身智能洞察2026/outputs/具身数据产业研究-从数据工厂到物理AI基础设施-v0.1/slide-7.png" assets/cases/embodied-data-industry/data-factory-workflow.png
cp "/Users/lex/Documents/lexnote/01-项目-具身智能洞察2026/outputs/具身数据产业研究-从数据工厂到物理AI基础设施-v0.1/slide-10.png" assets/cases/embodied-data-industry/outlook-2026-2028.png
```

Expected: four PNG files are present under the gallery directory.

- [ ] **Step 3: Verify format and dimensions**

Run:

```bash
file assets/cases/embodied-data-industry/*.png
```

Expected: all four files report `PNG image data, 1600 x 900`.

- [ ] **Step 4: Commit the gallery assets**

Run:

```bash
git add assets/cases/embodied-data-industry
git commit -m "Add embodied data research gallery"
```

Expected: one commit containing exactly four PNG files.

### Task 3: Rewrite The Complete English README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the existing README with the English information architecture**

Write `README.md` with these sections and messages:

```markdown
# Lex AI Research Skills

**Research is a system, not a document.**

[English](README.md) | [简体中文](README.zh-CN.md)

A reusable library of Codex skills for industrial research, technology analysis,
evidence organization, and executive communication.

## Available Skills
```

Add a four-column skill matrix using:

- `huawei-insight-deck`: converts a settled argument into editable restrained-red executive slides.
- `tech-research-deck`: structures source material and web research into a complete technology reading deck.

Continue with these sections in this exact order:

```markdown
## Why This Repository Exists
## How It Works
## Quick Start
## Installation
## Usage Examples
## Case Gallery
## Repository Structure
## Quality Principles
## What Comes Next
```

Content requirements:

- `Why This Repository Exists` explains that repeatable research quality comes from reusable methods for framing, evidence, comparison, claims, and visual QA.
- `How It Works` shows `source material -> framing -> verification -> architecture/routes -> page claims -> slide construction -> visual QA -> editable PPT`.
- `Quick Start` shows the two invocation names and one-sentence selection guidance.
- `Installation` includes both symbolic-link and direct-copy methods using the renamed repository URL.
- `Usage Examples` gives one concrete English prompt per skill.
- `Case Gallery` contains the four images and no other section contains an image.
- `Repository Structure` reflects the new `skills/` and `assets/` layout.
- `Quality Principles` covers claim-first structure, evidence traceability, consistent comparison dimensions, direct slide copy without unnecessary quotation marks, the `洞察` label convention, editable output, and mandatory render QA.
- `What Comes Next` states that future research, analysis, and communication skills will be added under the same installable structure without promising dates or unbuilt skills.

- [ ] **Step 2: Add installation commands for symbolic links**

Use this exact flow:

```bash
git clone https://github.com/hoilex0421-star/lex-ai-research-skills.git
cd lex-ai-research-skills
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/huawei-insight-deck" ~/.codex/skills/huawei-insight-deck
ln -s "$PWD/skills/tech-research-deck" ~/.codex/skills/tech-research-deck
```

- [ ] **Step 3: Add installation commands for direct copies**

Use:

```bash
mkdir -p ~/.codex/skills
cp -R skills/huawei-insight-deck ~/.codex/skills/huawei-insight-deck
cp -R skills/tech-research-deck ~/.codex/skills/tech-research-deck
```

- [ ] **Step 4: Add the gallery only under `## Case Gallery`**

Use a GitHub-compatible two-column HTML table. Each image path must occur once:

```html
<table>
  <tr>
    <td width="50%"><img src="assets/cases/embodied-data-industry/cover.png" alt="Embodied data industry research cover"></td>
    <td width="50%"><img src="assets/cases/embodied-data-industry/industry-chain.png" alt="Embodied data industry chain and data layer"></td>
  </tr>
  <tr>
    <td><strong>Research framing</strong><br>Defines the report boundary and the shift from data production to Physical AI infrastructure.</td>
    <td><strong>Industry architecture</strong><br>Maps the industrial chain and the role of the embodied-data layer.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/cases/embodied-data-industry/data-factory-workflow.png" alt="Embodied data factory workflow"></td>
    <td width="50%"><img src="assets/cases/embodied-data-industry/outlook-2026-2028.png" alt="Embodied data industry outlook from 2026 to 2028"></td>
  </tr>
  <tr>
    <td><strong>Operating workflow</strong><br>Breaks the data factory into an inspectable end-to-end process.</td>
    <td><strong>Forward outlook</strong><br>Turns evidence into a staged 2026-2028 industry view.</td>
  </tr>
</table>
```

- [ ] **Step 5: Validate the English README**

Run:

```bash
rg -n "^## " README.md
rg -n "README.zh-CN.md|lex-ai-research-skills|\\$huawei-insight-deck|\\$tech-research-deck" README.md
rg -n "assets/cases/embodied-data-industry" README.md
rg -n "Zara|张咋啦|inspired by|借鉴" README.md && exit 1 || true
```

Expected:

- All ten required `##` sections appear in the specified order.
- The Chinese language link, renamed repository URL, and both skill invocations appear.
- Exactly four gallery image references appear, all after `## Case Gallery`.
- No named external inspiration reference appears.

- [ ] **Step 6: Commit the English README**

Run:

```bash
git add README.md
git commit -m "Rewrite English skill library README"
```

Expected: one commit modifying only `README.md`.

### Task 4: Add The Complete Chinese README

**Files:**
- Create: `README.zh-CN.md`

- [ ] **Step 1: Create the Chinese README as a complete peer of the English README**

Begin with:

```markdown
# Lex AI Research Skills

**研究不是一份文档，而是一套系统。**

[English](README.md) | [简体中文](README.zh-CN.md)

一个面向产业研究、技术分析、证据组织和高管沟通的可复用 Codex 技能库。

## 可用技能
```

Continue with these sections in this exact order:

```markdown
## 为什么建立这个仓库
## 工作方式
## 快速开始
## 安装
## 使用示例
## 案例展示
## 仓库结构
## 质量原则
## 后续方向
```

Content requirements:

- The skill matrix is as detailed as the English version and uses the same four fields.
- The explanation distinguishes research structuring from visual slide execution.
- Installation commands are identical to the verified English commands.
- Usage examples are natural Chinese prompts for both skills.
- Slide body copy is described without unnecessary quotation marks.
- The top conclusion strip is called `洞察`, not `核心判断`.
- The gallery is the only section containing images.
- The language is natural Chinese rather than a literal or abbreviated translation.

- [ ] **Step 2: Add the Chinese gallery only under `## 案例展示`**

Use the same four image paths and table structure as the English README, with these captions:

```html
<table>
  <tr>
    <td width="50%"><img src="assets/cases/embodied-data-industry/cover.png" alt="具身数据产业研究封面"></td>
    <td width="50%"><img src="assets/cases/embodied-data-industry/industry-chain.png" alt="具身数据产业链与数据层"></td>
  </tr>
  <tr>
    <td><strong>研究定调</strong><br>界定研究边界，呈现具身数据从数据生产走向物理 AI 基础设施的核心命题。</td>
    <td><strong>产业架构</strong><br>梳理产业链结构及具身数据层在其中的位置。</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/cases/embodied-data-industry/data-factory-workflow.png" alt="具身数据工厂工作流"></td>
    <td width="50%"><img src="assets/cases/embodied-data-industry/outlook-2026-2028.png" alt="具身数据产业2026至2028年展望"></td>
  </tr>
  <tr>
    <td><strong>运营流程</strong><br>把数据工厂拆解为可检查、可比较的端到端流程。</td>
    <td><strong>趋势展望</strong><br>基于证据形成 2026-2028 年分阶段产业判断。</td>
  </tr>
</table>
```

- [ ] **Step 3: Validate the Chinese README**

Run:

```bash
rg -n "^## " README.zh-CN.md
rg -n "README.md|lex-ai-research-skills|\\$huawei-insight-deck|\\$tech-research-deck" README.zh-CN.md
rg -n "assets/cases/embodied-data-industry" README.zh-CN.md
rg -n "Zara|张咋啦|inspired by|借鉴" README.zh-CN.md && exit 1 || true
```

Expected:

- All ten required Chinese `##` sections appear in the specified order.
- The English language link, renamed repository URL, and both skill invocations appear.
- Exactly four gallery image references appear, all after `## 案例展示`.
- No named external inspiration reference appears.

- [ ] **Step 4: Commit the Chinese README**

Run:

```bash
git add README.zh-CN.md
git commit -m "Add Chinese skill library README"
```

Expected: one commit creating only `README.zh-CN.md`.

### Task 5: Run Repository And Content Validation

**Files:**
- Verify: `README.md`
- Verify: `README.zh-CN.md`
- Verify: `skills/huawei-insight-deck/`
- Verify: `skills/tech-research-deck/`
- Verify: `assets/cases/embodied-data-industry/`

- [ ] **Step 1: Verify required files**

Run:

```bash
test -f README.md
test -f README.zh-CN.md
test -f skills/huawei-insight-deck/SKILL.md
test -f skills/tech-research-deck/SKILL.md
test "$(find assets/cases/embodied-data-industry -maxdepth 1 -name '*.png' | wc -l | tr -d ' ')" = "4"
```

Expected: all commands exit successfully.

- [ ] **Step 2: Verify bilingual structure and links**

Run:

```bash
rg -n "\\[English\\]\\(README.md\\).*\\[简体中文\\]\\(README.zh-CN.md\\)" README.md README.zh-CN.md
rg -n "https://github.com/hoilex0421-star/lex-ai-research-skills.git" README.md README.zh-CN.md
```

Expected: both README files contain the language switch and new clone URL.

- [ ] **Step 3: Verify gallery confinement**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

checks = [
    ("README.md", "## Case Gallery"),
    ("README.zh-CN.md", "## 案例展示"),
]
needle = "assets/cases/embodied-data-industry/"
for filename, heading in checks:
    text = Path(filename).read_text()
    assert heading in text, f"{filename}: missing gallery heading"
    before, gallery = text.split(heading, 1)
    assert needle not in before, f"{filename}: image appears before gallery"
    assert gallery.count(needle) == 4, f"{filename}: expected four gallery images"
PY
```

Expected: in each file the gallery heading appears before exactly four image references, and no image references appear before that heading.

- [ ] **Step 4: Verify copy rules**

Run:

```bash
! rg -n "Zara|张咋啦|inspired by|借鉴" README.md README.zh-CN.md
rg -n "洞察" README.md README.zh-CN.md skills/tech-research-deck/SKILL.md
rg -n 'not `核心判断`|不用 `核心判断`' README.md README.zh-CN.md
```

Expected: named inspiration references are absent; `洞察` appears in both READMEs and the skill definition; `核心判断` appears only where the documentation explains that it is not the page label.

- [ ] **Step 5: Verify repository hygiene**

Run:

```bash
git diff --check main...HEAD
git status --short
git ls-files .superpowers
```

Expected:

- `git diff --check main...HEAD` produces no output.
- Git status contains no unexpected files.
- `git ls-files .superpowers` produces no output.

- [ ] **Step 6: Review the rendered Markdown locally**

Inspect both README files in a Markdown-capable viewer or GitHub preview and confirm:

- headings are balanced and scan well;
- tables do not contain malformed tags;
- all four images load at 16:9 without cropping;
- no image appears outside the gallery;
- Chinese and English pages feel equally complete.

Expected: no broken link, broken table, missing image, or visibly abbreviated language version.

### Task 6: Publish The Renamed GitHub Repository

**Files:**
- Remote repository: `hoilex0421-star/lex-ai-research-skills`

- [ ] **Step 1: Confirm authentication and renamed repository state**

Run:

```bash
gh auth status
git remote -v
gh repo view hoilex0421-star/lex-ai-research-skills --json name,url,defaultBranchRef
```

Expected:

- GitHub CLI is authenticated as `hoilex0421-star`.
- The repository name and URL are `lex-ai-research-skills`.
- The default branch is `main`.

- [ ] **Step 2: Ensure the canonical remote uses the renamed URL**

Run:

```bash
git remote set-url origin https://github.com/hoilex0421-star/lex-ai-research-skills.git
git remote -v
```

Expected: both fetch and push URLs use `lex-ai-research-skills.git`.

- [ ] **Step 3: Fast-forward the completed feature branch in the main worktree**

Run:

```bash
MAIN_ROOT="$(git worktree list --porcelain | awk '/^worktree / {sub(/^worktree /, ""); print; exit}')"
test "$(git -C "$MAIN_ROOT" branch --show-current)" = "main"
test -z "$(git -C "$MAIN_ROOT" status --short)"
git -C "$MAIN_ROOT" merge --ff-only feat/skill-library-readme
```

Expected: the main worktree is clean and local `main` fast-forwards to the reviewed feature branch without a merge commit.

- [ ] **Step 4: Push the updated default branch**

Run:

```bash
git -C "$MAIN_ROOT" push -u origin main
```

Expected: the local `main` branch is synchronized with `origin/main`.

- [ ] **Step 5: Update the repository description**

Run:

```bash
gh repo edit hoilex0421-star/lex-ai-research-skills \
  --description "Reusable Codex skills for technology research, evidence-led analysis, and editable executive presentations. English / 中文."
```

Expected: the public repository description matches the bilingual AI research skill library positioning.

- [ ] **Step 6: Verify the renamed repository**

Run:

```bash
gh repo view hoilex0421-star/lex-ai-research-skills --json name,url,description,defaultBranchRef
git -C "$MAIN_ROOT" status --short
git -C "$MAIN_ROOT" log -15 --oneline --decorate
```

Expected:

- Repository name is `lex-ai-research-skills`.
- URL is `https://github.com/hoilex0421-star/lex-ai-research-skills`.
- Description matches the bilingual AI research skill library positioning.
- Default branch is `main`.
- Git status is clean.
- Recent commits include the design spec, structure migration, gallery, and both README commits.

- [ ] **Step 7: Verify a fresh clone**

Run:

```bash
rm -rf /tmp/lex-ai-research-skills-verify
git clone --depth 1 https://github.com/hoilex0421-star/lex-ai-research-skills.git /tmp/lex-ai-research-skills-verify
test -f /tmp/lex-ai-research-skills-verify/README.md
test -f /tmp/lex-ai-research-skills-verify/README.zh-CN.md
test -f /tmp/lex-ai-research-skills-verify/skills/huawei-insight-deck/SKILL.md
test -f /tmp/lex-ai-research-skills-verify/skills/tech-research-deck/SKILL.md
test "$(find /tmp/lex-ai-research-skills-verify/assets/cases/embodied-data-industry -maxdepth 1 -name '*.png' | wc -l | tr -d ' ')" = "4"
```

Expected: the fresh clone contains both READMEs, both skills, and all four gallery images.

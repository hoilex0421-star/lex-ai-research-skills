# Official source and measured specification

Authority: [Huawei PPT模板-浅色版16-9, 2021](https://e.huawei.com/cn/documents/others/4f951fb72e1944288d3aa73bf40d8a8b).
Exact URL, SHA256 and geometry are in [the manifest](../assets/official-template.json).
Values were measured from the original PPTX, not inferred from screenshots.

| Element | Source rule |
| --- | --- |
| Canvas | 12196763 × 6858000 EMU, approximately 13.3385 × 7.5 inches; do not round to 13.333 |
| Cover | Source slide 1, layout 1 `探索`; mountain/paraglider art, red L, bottom brand strip |
| Cover title | x=898996, y=907092, cx=6559809, cy=690255 EMU; 32pt Microsoft YaHei |
| Cover metadata | x≈1.0163, y≈2.1319, w≈7.1477, h≈0.7042 inches; 14pt |
| Contents/navigation | Source slide 2, layout 5 `1_Contents page`; EBEBEB background; original short red line and static 目录 title |
| Navigation list | x=1033620, y=1843088, cx=10045712, cy=3013725 EMU; 22pt numbered list |
| Body | Source slide 3, layout 6 `1_Chinese text page`; white, black title, official footer |
| Body title | x=729175, y=456134, cx=10740640, cy=993400 EMU; 32pt, line spacing 34.30pt |
| Body content | x=736908, y=1501989, cx=10733557, cy=4690459 EMU; primary 18pt, secondary 12.99pt |
| Footer | Inherited page-number field and Huawei Confidential text, 9.74pt Arial; original logo position |
| Color example | Source slide 4: inspect chart/table colors; omit from authored deck |
| Ending | Source slide 5, layout 7 `End page`; retain source Thank you, mission/legal text and logo for exact-template work |

The source has four cover layouts; the reference slide uses `探索`. Do not switch
artwork automatically. It has **no separate chapter layout**. Reusing the contents
list with a red current item is our disclosed navigation convention; retain original
list size and position.

## Colors and content

The actual theme includes C7000A, E9002F, F4A100, FFFF00, 232323 and 666666.
The contents line uses C7000B. Preserve both instead of globally normalizing reds.
New body examples use C7000A, grayscale and white; additional chart colors should
come from the source palette when needed. Do not import community gradients,
spheres, large red headlines or red/navy/green defaults into official mode.

The official blank body does not prescribe every technical diagram. Our architecture
rows, flow nodes, comparison tables and evidence panels are **content arrangements
inside the body region**, not official layouts. Use 18pt primary labels and 12.99pt
secondary explanation/table detail. Avoid repeating a claim in title, insight band
and bottom conclusion.

## Exact preservation and source artifacts

The assembler preserves all 34 source parts under `ppt/slideMasters/`,
`ppt/slideLayouts/`, `ppt/theme/` and `ppt/media/` byte-for-byte. It replaces slide
content, omits the sample chart/table slide, and writes new speaker notes.
The unused empty off-canvas textbox on source slide 3 is omitted in new body slides.
Off-canvas color swatches in the original master remain: distinguish inherited
palette references from accidentally overflowing new content.

Fonts are not bundled. Render with legitimately available Microsoft YaHei and Arial.
Do not describe substituted-font renders as visually exact. Original artwork and
marks belong to Huawei; this library and sample are not official Huawei publications
and imply no endorsement.

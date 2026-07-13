# -*- coding: utf-8 -*-
"""
Worked example: the SECOND page family this skill covers — Huawei-style
technical-narrative pages. Two slides:
  1) a 学术界/产业界 timeline page,
  2) a 显式 vs 隐式 framework + comparison-table page.
Run:  python3 example_narrative_page.py  ->  example_narrative_page.pptx
Render to eyeball overlaps:
  libreoffice --headless --convert-to pdf example_narrative_page.pptx
  pdftoppm -png -r 200 example_narrative_page.pdf out
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from deck_helpers import *


def slide_timeline(s):
    title_band(s, "空间智能 / 世界模型 2024 起加速：", "学术界与产业界并行发布，落地节奏明显前移")

    # category legend (muted blue/green chips — NOT for emphasis)
    ex = tag_chip(s, 0.5, 1.10, "场景生成", fill=BLUE)
    tag_chip(s, ex + 0.14, 1.10, "场景理解", fill=GREEN)
    note(s, 0.5, 1.44, 8.0, "注：示意时间线，仅列代表性事件；红字为重点产品/模型。")

    # academic row (上) — image+head cards
    AY = 1.90
    acad = [
        (0.55, [("2024.6 ", 7.5, DARK, True), ("WonderWorld", 7.5, RED, True)], "单图秒级生成可探索 3DGS 场景"),
        (3.55, [("2024.12 ", 7.5, DARK, True), ("Genesis", 7.5, RED, True)], "多物理求解 + 生成式数据引擎"),
        (6.55, [("2025.1 ", 7.5, DARK, True), ("Genie2", 7.5, RED, True)], "可交互 3D 世界模型（DeepMind）"),
        (9.55, [("2025.3 ", 7.5, DARK, True), ("Cosmos", 7.5, RED, True)], "世界基座 + 物理一致视频生成"),
    ]
    for x, head, body in acad:
        event_card(s, x, AY, 2.75, 1.30, head, body, img=True)
    tag_chip(s, 12.45, AY + 0.45, "学术界", fill=BLUE, w=0.78)

    # time axis (middle) — returns tick centers
    time_axis(s, 0.55, 3.62, 12.68, ["2024.6", "2024.9", "2024.12", "2025.3"], color=NAVY)

    # industry row (下)
    IY = 4.20
    ind = [
        (0.55, [("2024.10 ", 7.5, DARK, True), ("DiffGS", 7.5, RED, True)], "清华：AI 生成 3DGS 资产"),
        (3.55, [("2024.12 ", 7.5, DARK, True), ("CAT4D", 7.5, RED, True)], "Google：单视频转 4D 场景"),
        (6.55, [("2025.1 ", 7.5, DARK, True), ("World Labs", 7.5, RED, True)], "李飞飞：单图生成可漫游 3D"),
        (9.55, [("2025.3 ", 7.5, DARK, True), ("GameGen-X", 7.5, RED, True)], "港大：开放世界视频游戏生成"),
    ]
    for x, head, body in ind:
        event_card(s, x, IY, 2.75, 1.30, head, body, img=True)
    tag_chip(s, 12.45, IY + 0.45, "产业界", fill=GREEN, w=0.78)

    conclusion_band(s, [("生成与理解双线并进：", 9.5, RED, True),
                        ("2024H2 起 学术界出新模型、产业界跟进落地，世界模型正从离线渲染走向可交互、可仿真。", 9.5, DARK, False)],
                    y=5.80)
    footer(s, "来源：各团队论文 / 官方发布（详见备注，含链接）。", brand="技术研究叙事页")
    s.notes_slide.notes_text_frame.text = "时间线每个事件在备注里写：团队 / 论文或发布链接 / 一句话贡献 / 口径。"


def slide_framework(s):
    title_band(s, "空间智能生成两条技术路线：", "显式三维表征 vs 隐式世界模型，长期走向互补")

    # two-column sub-claim headers (red text on light bars)
    section_header(s, 0.55, 1.16, 6.15, "路线一 · 显式表征：先建三维、再渲染", bar=True, color=RED)
    section_header(s, 7.05, 1.16, 6.18, "路线二 · 隐式表征：端到端预测下一帧", bar=True, color=RED)

    # left flow: 输入 -> 三维重建 -> 渲染输出
    fy = 1.80
    tag_chip(s, 0.55, fy, "输入", fill=NAVY, w=0.70)
    stage_box(s, 1.40, fy - 0.04, 1.55, 0.62, "图像 / 点云", accent=BLUE)
    arrow(s, 3.02, fy + 0.12, 0.34, 0.16, color=RED)
    stage_box(s, 3.42, fy - 0.04, 1.55, 0.62, "3DGS / Mesh", "可编辑、物理真实", accent=BLUE)
    arrow(s, 5.04, fy + 0.12, 0.34, 0.16, color=RED)
    stage_box(s, 5.42, fy - 0.04, 1.25, 0.62, "渲染图像", accent=BLUE)

    # right flow: 输入 -> 自回归世界模型 -> 预测帧
    tag_chip(s, 7.05, fy, "输入", fill=NAVY, w=0.70)
    stage_box(s, 7.90, fy - 0.04, 1.55, 0.62, "历史帧 + 动作", accent=GREEN)
    arrow(s, 9.52, fy + 0.12, 0.34, 0.16, color=RED)
    stage_box(s, 9.92, fy - 0.04, 1.70, 0.62, "自回归世界模型", "Token → 帧", accent=GREEN)
    arrow(s, 11.67, fy + 0.12, 0.30, 0.16, color=RED)
    stage_box(s, 12.00, fy - 0.04, 1.23, 0.62, "预测下一帧", accent=GREEN)

    # comparison table (same fields across both routes)
    th = spec_table(
        s, 0.55, 2.95, 12.68,
        [2.2, 5.24, 5.24],
        ["对比维度", "显式表征（建模→渲染）", "隐式表征（世界模型）"],
        [
            ["可编辑性", "高：几何/材质可直接改", "低：编辑需经条件控制"],
            ["物理真实", "强：依赖专业管线", "成长中：靠数据与算力逼近"],
            ["泛化 / 长程", "弱：依赖重建质量", "强：可外推未见场景"],
            ["算力诉求", "推理中等、建模偏离线", [("训练高（", 8, DARK, False), ("cube + SIMT", 8, RED, True), ("）", 8, DARK, False)]],
            ["代表工作", "Free360 / InstantSplat / 3DGS", "Cosmos / Genie2 / GameGen-X"],
        ],
        row_h=0.46,
    )

    conclusion_band(s, [("两条路线将共存互补：", 9.5, RED, True),
                        ("近场可控用显式建模、远场泛化用隐式预测；二者在数据引擎与算力底座上逐步融合。", 9.5, DARK, False)],
                    y=6.55)
    footer(s, "来源：各路线代表论文与开源实现（详见备注）。表中算力为研判口径。", brand="技术研究叙事页")
    s.notes_slide.notes_text_frame.text = "对比表每格标口径：官方/机构 vs 厂商自报 vs 研判；算力维度注明 FP16/卡 等基准。"


if __name__ == '__main__':
    prs = newdeck()
    slide_timeline(blank(prs))
    slide_framework(blank(prs))
    out = os.path.join(os.path.dirname(__file__), 'example_narrative_page.pptx')
    prs.save(out); print('saved', out)

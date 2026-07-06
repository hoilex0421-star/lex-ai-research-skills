# -*- coding: utf-8 -*-
"""
Worked example: a Huawei-style market/insight 论点页 for "三场景市场空间".
Run:  python3 example_market_page.py   ->  example_market_page.pptx
Then render to check zero label overlap:
  libreoffice --headless --convert-to pdf example_market_page.pptx
  pdftoppm -png -r 200 example_market_page.pdf out
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from deck_helpers import *

def build(s):
    # Part 1 — 论点型标题 (red key clause + black remainder, quantified payload)
    title_band(s, "各应用场景市场空间：2030 保守 25 万 vs 乐观 ~100 万，", "工业孵化催熟、家庭弹性最大")

    # Part 2 — 洞察启示 (conclusion-first, each bullet sourced)
    insight_band(s, ["洞察", "启示"], [
        [("出货分场景：", 9, DARK, True),
         ("工业（制造+物流）近期主战场、订单最实；商业（零售/导览/安防）正起步多为试点；家庭 TAM 最大但最晚。", 9, DARK, False)],
        [("口径分歧：", 9, DARK, True),
         ("保守（高盛 base）2030~25 万 vs 乐观（SAG/BofA）~100 万；越乐观、越靠后，家庭弹性最大。", 9, DARK, False)],
    ])

    # Part 3 — left quantified chart (stacked bar: 保守/乐观 × 2030/2035, stacked by scenario)
    text(s, 0.6, 2.02, 5.6, 0.22, [[("全球年出货（万台）· 分场景堆叠，保守 vs 乐观 并列", 8.5, MID, True)]])
    lx = 0.62
    for nm, co in [("工业", RED), ("商业", RED2), ("家庭", RED3)]:
        dot(s, lx + 0.06, 2.40, 0.12, co); text(s, lx + 0.17, 2.30, 0.7, 0.2, [[(nm, 8, DARK, False)]]); lx += 0.78
    xp = 1.18
    xs = [xp + 0.10, xp + 0.10 + 0.96]; g2 = xs[1] + 0.82 + 0.62; xs += [g2, g2 + 0.96]
    bars = [
        {'x': xs[0], 'vals': [15, 10, 0],   'total': 25,  'label_bottom': '保守', 'top_is_red': False},
        {'x': xs[1], 'vals': [45, 35, 20],  'total': 100, 'label_bottom': '乐观', 'top_is_red': True},
        {'x': xs[2], 'vals': [50, 38, 50],  'total': 138, 'label_bottom': '保守', 'top_is_red': False},
        {'x': xs[3], 'vals': [90, 80, 130], 'total': 300, 'label_bottom': '乐观', 'top_is_red': True},
    ]
    stacked_bar(s, (xp, 2.55, 5.6, 6.02), bars, [RED, RED2, RED3], ymax=300)
    text(s, xs[0] - 0.1, 6.30, 0.82 * 2 + 0.34, 0.2, [[("2030", 8.5, DARK, True)]], align=PP_ALIGN.CENTER)
    text(s, xs[2] - 0.1, 6.30, 0.82 * 2 + 0.34, 0.2, [[("2035", 8.5, DARK, True)]], align=PP_ALIGN.CENTER)
    # Part 5 (left) — multi-source footnote, every figure named + caliber flagged
    text(s, 0.6, 6.50, 5.9, 0.55, [
        [("总量口径：", 6.3, RED, True), ("保守＝高盛 2024 base；乐观＝SAG 81万/2030(含四足)、BofA~100万/2030–35；2035 乐观研判外推~300万。", 6.3, MUTE, False)],
        [("各格＝总量×应用结构(高盛/摩根士丹利)的研判拆分；机构未逐场景披露单位数。详见备注（含链接）。", 6.3, MUTE, False)],
    ], ls=1.16)

    # Part 4 — right same-field cards (identical row labels = a comparison)
    RX, RW = 6.66, 6.16
    card(s, RX, 2.10, RW, 1.92, "工业 · 制造+物流",
         [[("近期主战场", 7.4, WHITE, True)], [("2030 ", 7, WHITE, False), ("15–45 万", 7.4, WHITE, True)], [("2035 ", 7, WHITE, False), ("50–90 万", 7.4, WHITE, True)]],
         RED, [("客户", "车厂 / 3C 代工 · 3PL 物流 / 电商仓"), ("买点", "顶替工位 · 降人力 · ROI 可算"), ("实例", "优必选 / 星动纪元 / 原力灵机 / 银河通用"), ("定位", "订单最实、初创最集中")])
    card(s, RX, 4.10, RW, 1.42, "商业 · 商用服务",
         [[("正起步", 7.4, WHITE, True)], [("2030 ", 7, WHITE, False), ("10–35 万", 7.4, WHITE, True)], [("2035 ", 7, WHITE, False), ("35–80 万", 7.4, WHITE, True)]],
         RED2, [("客户", "零售连锁 / 商超 · 酒店 · 展馆导览 · 安防"), ("买点", "补货/导购 · 送物 · 巡检"), ("进展", "多为试点 / demo"), ("定位", "场景散、单点验证为主")])
    card(s, RX, 5.60, RW, 1.42, "家庭 · 消费",
         [[("TAM 最大、最晚", 7.4, WHITE, True)], [("2030 ", 7, WHITE, False), ("0–20 万", 7.4, WHITE, True)], [("2035 ", 7, WHITE, False), ("50–130 万", 7.4, WHITE, True)]],
         RED3, [("客户", "C 端家庭"), ("买点", "收纳 / 餐厨 / 陪护"), ("卡点", "安全 · 成本 · 泛化未过关"), ("定位", "几无规模落地")])

    footer(s, "来源：高盛 2024/2026、摩根士丹利 2025、SAG、BofA。分场景数量为研判估算。")
    s.notes_slide.notes_text_frame.text = "在备注里写全每个数字的一手出处+链接（可回溯）。示例略。"

if __name__ == '__main__':
    prs = newdeck(); build(blank(prs))
    out = os.path.join(os.path.dirname(__file__), 'example_market_page.pptx')
    prs.save(out); print('saved', out)

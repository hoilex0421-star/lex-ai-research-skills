#!/usr/bin/env python3
"""Build an Outlook-ready email (HTML + draft .eml) from a minutes JSON spec.

Usage:
    python3 build_email.py minutes.json [--out DIR]

JSON spec (see assets/example-minutes.json):
{
  "subject": "【会议纪要】XX交流纪要（2026-10-27）",
  "file_stem": "XX交流纪要",
  "greeting": ["各位领导、同事好：", "以下为 ... 请查阅。"],
  "classification": "□绝密 □机密 □秘密 ■内部公开",
  "meta": [["会议时间", "..."], ["与会人员", "第一行\\n第二行"]],
  "blocks": [
    {"h2": "一、交流关键信息"},
    {"h3": "1. 公司定位：..."},
    {"conclusion": "结论：..."},
    {"p": "段落"},
    {"ol": ["要点", {"text": "带子项", "subs": ["a", "b"], "tail": "补充一句"}]},
    {"table": {"head": ["项目", "当前情况", "备注"], "rows": [["...", "...", "..."]]}}
  ]
}
Inline **bold** is supported in every text field.
"""
import argparse
import base64
import html
import json
import re
from email.header import Header
from pathlib import Path

FONT = "font-family:'Microsoft YaHei','微软雅黑',Arial,sans-serif;"
RED = "#A11D21"
BOX_BG = "#F2F2F2"      # light gray: leadership prefers no pink
BOX_BAR = "#A6A6A6"
TH_BG = "#F1EFEA"
BORDER = "#D9D5CC"
TXT = f"{FONT}font-size:14px;line-height:1.6;"


def fmt(s: str) -> str:
    s = html.escape(s).replace("\n", "<br>")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def p(s, extra=""):
    return f'<p style="{TXT}margin:0 0 6px 0;color:#1a1a1a;{extra}">{fmt(s)}</p>'


def h2(s):
    return (f'<p style="{FONT}font-size:17px;font-weight:bold;color:{RED};margin:20px 0 8px 0;'
            f'border-bottom:2px solid {RED};padding-bottom:4px;">{fmt(s)}</p>')


def h3(s):
    return f'<p style="{FONT}font-size:15px;font-weight:bold;color:#1a1a1a;margin:16px 0 6px 0;">{fmt(s)}</p>'


def conclusion(s):
    return ('<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin:4px 0 8px 0;width:100%;"><tr>'
            f'<td style="border-left:4px solid {BOX_BAR};background:{BOX_BG};padding:8px 12px;{TXT}color:{RED};font-weight:bold;">'
            f'{fmt(s)}</td></tr></table>')


def li(x):
    if isinstance(x, str):
        return f'<li style="{TXT}margin:4px 0;">{fmt(x)}</li>'
    subs = "".join(f'<li style="{TXT}margin:2px 0;">{fmt(s)}</li>' for s in x.get("subs", []))
    sub_html = f'<ul style="margin:2px 0;padding-left:20px;">{subs}</ul>' if subs else ""
    tail = f'<div style="{TXT}margin-top:2px;">{fmt(x["tail"])}</div>' if x.get("tail") else ""
    return f'<li style="{TXT}margin:4px 0;">{fmt(x["text"])}{sub_html}{tail}</li>'


def ol(items):
    return f'<ol style="margin:0 0 6px 0;padding-left:24px;">{"".join(li(i) for i in items)}</ol>'


def table(spec):
    cell = f"border:1px solid {BORDER};padding:6px 10px;{FONT}font-size:13px;line-height:1.5;vertical-align:top;"
    th = "".join(f'<td style="background:{TH_BG};{cell}font-weight:bold;">{fmt(c)}</td>' for c in spec["head"])
    trs = "".join("<tr>" + "".join(f'<td style="{cell}">{fmt(c)}</td>' for c in r) + "</tr>" for r in spec["rows"])
    return ('<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;margin:6px 0 10px 0;width:100%;">'
            f'<tr>{th}</tr>{trs}</table>')


RENDER = {"h2": h2, "h3": h3, "conclusion": conclusion, "p": p, "ol": ol, "table": table}


def build(spec: dict) -> str:
    out = []
    greeting = spec.get("greeting", [])
    for i, g in enumerate(greeting):
        out.append(p(g, "margin-bottom:14px;" if i == len(greeting) - 1 else ""))
    if spec.get("classification"):
        out.append(p(spec["classification"], "color:#55534E;"))
    for k, v in spec.get("meta", []):
        out.append(f'<p style="{TXT}margin:0 0 6px 0;color:#1a1a1a;"><b>{fmt(k)}：</b>{fmt(v)}</p>')
    for block in spec.get("blocks", []):
        (kind, value), = block.items()
        out.append(RENDER[kind](value))
    title = html.escape(spec.get("file_stem", "会议纪要"))
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title}</title></head>'
            f'<body style="margin:0;padding:16px;background:#ffffff;"><div style="max-width:860px;">{"".join(out)}</div></body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    doc = build(spec)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stem = spec.get("file_stem", "会议纪要")
    (out / f"{stem}_邮件正文.html").write_text(doc, encoding="utf-8")
    body = base64.encodebytes(doc.encode("utf-8")).decode().replace("\n", "\r\n")
    eml = ("X-Unsent: 1\r\n"
           f"Subject: {Header(spec.get('subject', stem), 'utf-8').encode()}\r\n"
           "To: \r\nMIME-Version: 1.0\r\n"
           "Content-Type: text/html; charset=utf-8\r\n"
           "Content-Transfer-Encoding: base64\r\n\r\n" + body)
    (out / f"{stem}.eml").write_text(eml, encoding="utf-8", newline="")
    print(f"wrote {out / (stem + '.eml')} and {out / (stem + '_邮件正文.html')}")


if __name__ == "__main__":
    main()

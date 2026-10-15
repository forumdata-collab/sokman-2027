#!/usr/bin/env python3
"""由 real2027/rewrite/<肖>.json 組裝站內 content/<肖>.md（格式跟足原檔）。

格式（原檔實錄）：
## 屬X的你
<空>
{整體}
<空>
{寒命人…熱命人…平命人…}
<空>
---
<空>
---
<空>
**{中文年}{干支}{肖}年出生**：{句}
<空>
…（每個出生年一段）
<空>
**農曆一月（壬寅月）**
本月為X的{屬}。
<空>
**財運：** …
（事業／感情／身體／是非同格式，每項後空行）
---
（下一個月）

用法：
  python3 assemble_content.py --dry-run 羊        # 只 print，唔寫檔
  python3 assemble_content.py --write             # 寫入 content/<肖>.md（先備份 .bak-<ts>）
"""
import argparse
import datetime
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path("/home/ubuntu/sokman-2027")
REWRITE = ROOT / "real2027" / "rewrite_v2"
REWRITE_FALLBACK = ROOT / "real2027" / "rewrite"
CONTENT = ROOT / "content"


def rewrite_path(z: str) -> pathlib.Path:
    p2 = REWRITE / f"{z}.json"
    return p2 if p2.exists() else REWRITE_FALLBACK / f"{z}.json"

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"
CN_NUM = "〇一二三四五六七八九"
MONTHS = ["一月", "二月", "三月", "四月", "五月", "六月",
          "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_GANZHI = ["壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未",
                "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑"]
ASPECTS = ["財運", "事業", "感情", "身體", "是非"]


def cn_year(y: int) -> str:
    """1931 -> 一九三一（4 位數字逐位轉中文，0 -> 〇）"""
    return "".join(CN_NUM[int(d)] for d in str(y))


def ganzhi(y: int) -> str:
    i = (y - 4) % 60
    return GAN[i % 10] + ZHI[i % 12]


def build_md(z: str) -> str:
    d = json.loads(rewrite_path(z).read_text(encoding="utf-8"))
    overall = d["整體"].strip()
    # 站內風格：段落以「肖X的你」開頭（原稿有啲寫「肖X今年…」）
    if overall.startswith(f"肖{z}") and not overall.startswith(f"肖{z}的你"):
        overall = f"肖{z}的你" + overall[len(f"肖{z}"):]
    elif not overall.startswith(f"肖{z}的你"):
        overall = f"肖{z}的你{overall}"
    lines: list[str] = []
    lines += [f"## 屬{z}的你", "", overall, ""]
    han = d["寒命"].strip()
    re_ = d["熱命"].strip()
    ping = d["平命"].strip()
    parts = []
    for pre, txt in (("寒命人", han), ("熱命人", re_), ("平命人", ping)):
        if not txt.startswith(pre):
            txt = pre + ("，" if txt[:1] not in "，。、" else "") + txt
        if not txt.endswith("。"):
            txt += "。"
        parts.append(txt)
    lines.append("".join(parts))
    lines += ["", "---", ""]

    for item in d["各年"]:
        y = int("".join(str(int(ch)) if ch.isdigit() else str(CN_NUM.index(ch)) for ch in item["出生年"])[:4])
        lines.append(f"**{cn_year(y)}{ganzhi(y)}{z}年出生**：{item['句'].strip()}")
        lines.append("")

    months = {m["月"]: m for m in d["月"]}
    for i, m in enumerate(MONTHS):
        mm = months.get(m)
        if mm is None:
            sys.exit(f"{z}: 缺 {m}")
        lines.append(f"**農曆{m}（{MONTH_GANZHI[i]}月）**")
        lines.append(f"本月為{z}的{mm.get('屬', '').strip()}。")
        lines.append("")
        first = True
        for a in ASPECTS:
            txt = (mm.get(a) or "").strip()
            if not txt:
                sys.exit(f"{z} {m}: 缺 {a}")
            if first and a == "財運":
                # 原檔喺財運句首提當月入中星；星由審計核實，故由組裝器統一注入
                txt = f"{MONTH_STARS[i]}星入中，{txt}"
                first = False
            lines += [f"**{a}：** {txt}", ""]
        lines += ["---", ""]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


# 真書 p52-53 流月飛星入中星（2027）：五黃→四綠→三碧→二黑→一白→九紫→八白→七赤→六白→五黃→四綠→三碧
MONTH_STARS = ["五黃廉貞", "四綠文曲", "三碧祿存", "二黑巨門", "一白貪狼", "九紫右弼",
               "八白左輔", "七赤破軍", "六白武曲", "五黃廉貞", "四綠文曲", "三碧祿存"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dry-run", metavar="肖")
    ap.add_argument("zodiacs", nargs="*")
    a = ap.parse_args()

    if a.dry_run:
        print(build_md(a.dry_run)[:2500])
        return

    zs = a.zodiacs or [p.stem for p in sorted(REWRITE_FALLBACK.glob("*.json"))]
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    for z in zs:
        if not rewrite_path(z).exists():
            print(f"skip {z}: 未有 rewrite JSON")
            continue
        md = build_md(z)
        out = CONTENT / f"{z}.md"
        if a.write:
            if out.exists():
                shutil.copy2(out, out.with_suffix(f".md.bak-{stamp}"))
            out.write_text(md, encoding="utf-8")
        print(f"{z}: {len(md)} chars, {md.count('**農曆')} 個月" + ("（已寫入）" if a.write else "（dry）"))


if __name__ == "__main__":
    main()

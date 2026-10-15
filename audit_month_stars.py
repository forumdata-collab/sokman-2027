#!/usr/bin/env python3
"""核對站內每月「X星入中」係否符合真書 2027 流月飛星（五黃→四綠→三碧→二黑→一白→九紫→八白→七赤→六白→五黃→四綠→三碧）。"""
import pathlib
import re

CONTENT = pathlib.Path("/home/ubuntu/sokman-2027/content")
MONTHS = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
REAL = ["五黃", "四綠", "三碧", "二黑", "一白", "九紫", "八白", "七赤", "六白", "五黃", "四綠", "三碧"]
STAR_RE = re.compile(r"([一二三四五六七八九][白黑碧綠黃赤紫])[^，。]{0,6}入中")

bad = 0
missing = 0
for f in sorted(CONTENT.glob("*.md")):
    txt = f.read_text(encoding="utf-8")
    # 切出每月段落
    pos = [txt.find("**農曆" + m + "（") for m in MONTHS]
    for i, m in enumerate(MONTHS):
        start = pos[i]
        end = pos[i + 1] if i + 1 < len(MONTHS) else len(txt)
        if start < 0:
            print(f"{f.stem} {m}: 段落找唔到")
            missing += 1
            continue
        seg = txt[start:end]
        found = STAR_RE.findall(seg)
        uniq = sorted(set(found))
        if not uniq:
            print(f"{f.stem} {m}: ⚪ 冇提入中星（真書應為 {REAL[i]}）")
            missing += 1
        elif uniq == [REAL[i]]:
            pass
        else:
            print(f"{f.stem} {m}: 🔴 站內講 {uniq}，真書應為 {REAL[i]}")
            bad += 1
print(f"\n合計：錯 {bad} 處（有提到但寫錯）、缺 {missing} 處（冇提或段落缺）")

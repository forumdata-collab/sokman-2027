#!/usr/bin/env python3
"""content/*.md 品質檢查：簡體字、禁語、星名對真書、每月五欄、入中星。

用法: python3 qa_content.py [--fix-report]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/home/ubuntu/sokman-2027")
CONTENT = ROOT / "content"
REAL = ROOT / "real2027"
ZODIACS = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
ASPECTS = ["財運", "事業", "感情", "身體", "是非"]
MONTHS = ["一月", "二月", "三月", "四月", "五月", "六月",
          "七月", "八月", "九月", "十月", "十一月", "十二月"]
MONTH_STARS = ["五黃", "四綠", "三碧", "二黑", "一白", "九紫", "八白", "七赤", "六白", "五黃", "四綠", "三碧"]

# 簡體偵測：Big5 編碼得到 = 繁體字庫有嘅字；編唔到嘅 CJK 字就當簡體混入。
# （opencc 字元級轉換會誤判「丑／凶／吃／干／台／峰／群」等兩體通用字，故唔用。）
def simplified_chars(text: str) -> list[str]:
    ok_variants = set("着峯裏裡鷄牀邨衞")  # 兩體通用／異體字，唔算簡體
    out = []
    for c in text:
        if "\u4e00" <= c <= "\u9fff" and c not in ok_variants:
            try:
                c.encode("big5")
            except UnicodeEncodeError:
                out.append(c)
    return sorted(set(out))
BANNED = ["蘇民峰", "原著", "師傅", "AI", "機器", "GPT", "推演", "筆者", "本書"]

issues = 0


def check(z):
    global issues
    p = CONTENT / f"{z}.md"
    t = p.read_text(encoding="utf-8")
    # 1) 簡體
    simp = simplified_chars(t)
    if simp:
        print(f"{z}: 🔴 簡體字 {simp[:20]}{' …' if len(simp) > 20 else ''}")
        issues += 1
    # 2) 禁語
    for w in BANNED:
        if w in t:
            print(f"{z}: 🔴 禁語「{w}」出現 {t.count(w)} 次")
            issues += 1
    # 3) 每月五欄
    for i, m in enumerate(MONTHS):
        seg_m = re.search(r"\*\*農曆" + m + r"（[^）]+）\*\*(.*?)(?=\*\*農曆|\Z)", t, re.S)
        if not seg_m:
            print(f"{z} {m}: 🔴 段落缺失")
            issues += 1
            continue
        seg = seg_m.group(1)
        for a in ASPECTS:
            if f"**{a}：**" not in seg and f"{a}：" not in seg:
                print(f"{z} {m}: 🔴 缺 {a}")
                issues += 1
        if f"本月為{z}的" not in seg:
            print(f"{z} {m}: 🟠 缺「本月為{z}的…月」句")
            issues += 1
        if MONTH_STARS[i] not in seg[:120]:
            print(f"{z} {m}: 🟠 首欄未見入中星 {MONTH_STARS[i]}")
            issues += 1
    # 4) 星名 vs 真書
    rp = REAL / f"{z}.json"
    if rp.exists():
        d = json.loads(rp.read_text(encoding="utf-8"))
        miss = []
        for key in ("吉星", "凶星"):
            node = d.get("整體運程", {}).get(key)
            texts = []
            if isinstance(node, dict):
                for v in node.values():
                    texts += v if isinstance(v, list) else [str(v)]
            names = re.findall(r"[「『]([^」』]{1,6})[」』]", " ".join(texts))
            for n in names:
                if n not in t and n not in ("太歲", "歲破"):
                    miss.append(n)
        if "吉星全無" in json.dumps(d.get("整體運程", {}).get("吉星", {}), ensure_ascii=False) and "吉星全無" not in t:
            miss.append("（吉星全無句）")
        if miss:
            print(f"{z}: 🟠 真書星名未見於站內: {sorted(set(miss))}")
            issues += 1
    # 5) 各年段
    n_years_site = len(re.findall(r"^\*\*[〇一二三四五六七八九]{4}[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]" + z + r"年出生\*\*", t, re.M))
    if rp.exists():
        v2 = ROOT / "real2027" / "rewrite_v2" / f"{z}.json"
        n_real = len(json.loads(v2.read_text(encoding="utf-8")).get("各年", [])) if v2.exists() else 0
        if n_years_site != n_real:
            print(f"{z}: 🟠 出生年份段 站內 {n_years_site} vs 真書 {n_real}")
            issues += 1


for z in ZODIACS:
    check(z)
print(f"\n總問題數: {issues}")

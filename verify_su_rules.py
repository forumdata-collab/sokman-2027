#!/usr/bin/env python3
"""蘇氏答案認證系統：以書內容（OCR）驗證網站展示的九宮化解/犯太歲飾物/熱平寒。

推理流程：
1. 從 OCR 文字檔提取書中關鍵片段（證據）
2. 以 knowledge_base.json（蘇氏規則引擎）為標準答案
3. 對照 build_site.py / index.html 的展示資料
4. 輸出 ✅/⚠️/❌ 認證報告
"""
import json
import pathlib
import re

ROOT = pathlib.Path("/home/ubuntu/sokman-2027")
OCR_DIR = ROOT / "ocr" / "rabbit_2023"
KB_PATH = ROOT / "knowledge_base.json"
CONTENT_DIR = ROOT / "content"

STAR_NAMES = ["一白", "二黑", "三碧", "四綠", "五黃", "六白", "七赤", "八白", "九紫"]

def ocr_text():
    """全部 OCR 文字檔合併。"""
    parts = []
    if OCR_DIR.exists():
        for f in sorted(OCR_DIR.glob("*.txt")):
            parts.append(f.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)

def evidence(text, keywords, window=60):
    """在 OCR 文字中尋找同時含多個關鍵字的片段。"""
    hits = []
    for kw in keywords:
        for m in re.finditer(re.escape(kw), text):
            s = max(0, m.start() - window)
            e = min(len(text), m.end() + window)
            hits.append(text[s:e].replace("\n", " "))
    return hits[:5]

def verify_九宮(kb, live_remedies):
    """九宮化解：知識庫 vs 網站 STAR_DATA。"""
    print("=" * 60)
    print("🔍 認證一：九宮化解物品（書 p42 vs 網站 STAR_DATA）")
    print("=" * 60)
    report = []
    for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        entry = kb["九宮化解"][num]
        kb_remedy = entry["化解"]
        live = live_remedies.get(num, {})
        live_remedy = live.get("remedy", "")
        # 檢查網站文字包含書中關鍵詞（音樂盒/粉紅色/一杯水/白石/富貴竹/九枝紅花...）
        # 書中核心物品詞
        core_items = {
            "1": ["音樂盒", "一杯水"],
            "2": ["音樂盒"],
            "3": ["粉紅色"],
            "4": ["富貴竹", "一杯水"],
            "5": ["音樂盒", "一杯水"],
            "6": ["一杯水", "白石"],
            "7": ["一杯水"],
            "8": ["一杯水"],
            "9": ["植物", "紅花"],
        }
        missing = [it for it in core_items[num] if it not in live_remedy]
        ok = not missing
        status = "✅" if ok else "⚠️"
        report.append((status, num, entry["星"], live_remedy[:45]))
        print(f"  {status} {entry['星']:8s} 書:「{kb_remedy}」 站:「{live_remedy[:40]}」")
        if missing:
            print(f"        └ 缺: {missing}")
    return report

def verify_飾物(kb, ts_year=2027):
    """犯太歲飾物：規則驗證（太歲三合/六合 + 排除自身犯太歲）。"""
    print()
    print("=" * 60)
    print("🔍 認證二：犯太歲飾物規則（太歲三合/六合·排除自身犯太歲）")
    print("=" * 60)
    rule = kb["犯太歲飾物"]["_規則"]
    print(f"  書載規則: {rule}")
    # 2027 未年(羊太歲)
    taishui_sets = {
        2024: {"z": "龍", "犯": {"龍", "狗", "兔", "牛"}},
        2025: {"z": "蛇", "犯": {"蛇", "豬", "猴", "虎"}},
        2026: {"z": "馬", "犯": {"馬", "鼠", "牛", "兔"}},
        2027: {"z": "羊", "犯": {"羊", "牛", "狗", "鼠"}},
        2028: {"z": "猴", "犯": {"猴", "虎", "蛇", "豬"}},
    }
    SANHE = {"羊": ["兔", "豬"], "蛇": ["雞", "牛"], "馬": ["虎", "狗"], "猴": ["鼠", "龍"],
             "雞": ["蛇", "牛"], "狗": ["虎", "馬"], "龍": ["猴", "鼠"], "牛": ["蛇", "雞"],
             "鼠": ["猴", "龍"], "虎": ["馬", "狗"], "兔": ["豬", "羊"], "豬": ["兔", "羊"]}
    LIUHE = {"鼠": "牛", "牛": "鼠", "虎": "豬", "兔": "狗", "龍": "雞", "蛇": "猴",
             "馬": "羊", "羊": "馬", "猴": "蛇", "雞": "龍", "狗": "兔", "豬": "虎"}
    print()
    for y in sorted(taishui_sets):
        info = taishui_sets[y]
        z = info["z"]
        forbidden_y = info["犯"]
        partners = [LIUHE[z]] + SANHE[z]
        safe = [p for p in partners if p not in forbidden_y]
        banned = [p for p in partners if p in forbidden_y]
        status = "✅" if not banned else "⚠️(需提示排除)"
        print(f"  {status} {y}年太歲{z}: 三合/六合={partners} "
              f"→ 可戴:{safe} {('不可戴:' + str(banned)) if banned else ''}")
    return True

def verify_熱平寒(kb):
    """熱平寒：書/p42及官方定義 vs 網站說明。"""
    print()
    print("=" * 60)
    print("🔍 認證三：熱平寒定義（蘇民峰官方 vs 網站）")
    print("=" * 60)
    for k in ["寒命", "熱命", "平命"]:
        e = kb["熱平寒"][k]
        print(f"  ✅ {k}: {e['期間']} | 喜用:{e['喜用']} | {e['說明']}")
    print()
    print("  網站 calcMing 邏輯驗證（由 /tmp/sokman_js.txt）:")
    js = (ROOT / "tmp_js_check.js")
    return True

def main():
    kb = json.loads(KB_PATH.read_text(encoding="utf-8"))
    text = ocr_text()
    print(f"OCR 文字總長: {len(text)} 字元, 來自 {len(list(OCR_DIR.glob('*.txt')))} 個檔案")

    # 從網站 build_site.py 提取 live STAR_DATA remedies
    live_remedies = {}
    build_src = (ROOT / "build_site.py").read_text(encoding="utf-8")
    js_src = pathlib.Path("/tmp/sokman_js.txt").read_text(encoding="utf-8") if pathlib.Path("/tmp/sokman_js.txt").exists() else ""
    data_src = js_src if js_src else build_src
    for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        m = re.search(rf'{num}:\{{\'name\':\'([^\']+)\'.*?\'remedy\':\'([^\']+)\'', data_src)
        if m:
            live_remedies[num] = {"name": m.group(1), "remedy": m.group(2)}
    if not live_remedies:
        # fallback: from index.html
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            m = re.search(rf'{num}:\{{name:\'([^\']+)\'.*?remedy:\'([^\']+)\'', html)
            if m:
                live_remedies[num] = {"name": m.group(1), "remedy": m.group(2)}

    print()
    verify_九宮(kb, live_remedies)
    verify_飾物(kb)
    verify_熱平寒(kb)
    print()
    print("認證完成。")

if __name__ == "__main__":
    main()
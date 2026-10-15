#!/usr/bin/env python3
"""比對真書 2027（real2027/*.json）同站內 content/*.md 嘅吉星／凶星清單。
用法: python3 audit_real2027.py [--json out.json]
輸出：每個生肖 真書吉星/凶星、站內吉星/凶星、多推（站內有真書冇）、漏推（真書有站內冇）。
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/home/ubuntu/sokman-2027")
REAL = ROOT / "real2027"
CONTENT = ROOT / "content"
ZODIACS = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]

# 星名抽取：引號「」或 **粗體**
STAR_RE = re.compile(r"[「『]([^」』]{1,6})[」』]")
BOLD_RE = re.compile(r"\*\*([^*]{1,8})\*\*")
KNOWN_NOT_STAR = {"太歲", "三刑", "值太歲", "沖太歲", "刑太歲", "害太歲", "破太歲"}


def real_stars(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    overall = d.get("整體運程", {})
    out = {"吉星": [], "凶星": [], "raw": {}}
    for key in ("吉星", "凶星"):
        node = overall.get(key)
        if node is None:
            continue
        texts = []
        if isinstance(node, dict):
            for v in node.values():
                texts += v if isinstance(v, list) else [str(v)]
        elif isinstance(node, list):
            texts = [str(x) for x in node]
        else:
            texts = [str(node)]
        out["raw"][key] = " ".join(texts)
        for t in texts:
            if key == "吉星" and ("吉星全無" in t or "吉星欠奉" in t or "並無吉星" in t):
                out[key] = ["（全無）"]
                break
            out[key] += STAR_RE.findall(t)
    # 去重保序
    for key in ("吉星", "凶星"):
        seen, dedup = set(), []
        for s in out[key]:
            if s not in seen:
                seen.add(s)
                dedup.append(s)
        out[key] = dedup
    return out


def site_stars(path):
    """站內：「吉星有…」「凶星有…」句子（該句到「。」為止）中的星名，粗體／引號／無標記都抽。"""
    txt = path.read_text(encoding="utf-8")
    m = re.search(r"## 屬.+?的你(.*?)(?=\n## |\n---)", txt, re.S)
    seg = m.group(1) if m else txt[:4000]
    out = {"吉星": [], "凶星": [], "raw": {}}
    for key in ("吉星", "凶星"):
        hit = re.search(key + r"[^。]{0,8}?有([^。]*)", seg)
        if not hit:
            continue
        body = hit.group(1)
        # 「吉星有…；凶星有…」同一句時切走另一邊
        other = "凶星" if key == "吉星" else "吉星"
        body = re.split(other, body)[0]
        sentence = (key + "有" + body).strip()
        out["raw"][key] = sentence
        names = [s.strip("「」『』") for s in BOLD_RE.findall(body) + STAR_RE.findall(body)]
        if not names:
            # 無粗體／引號：抽「XX星」「XXXX貴人」等 2-4 字詞
            names = re.findall(r"([\u4e00-\u9fff]{2,4})(?:貴人星|貴人|星)", body)
        seen, dedup = set(), []
        for s in names:
            if s and s not in KNOWN_NOT_STAR and s not in seen:
                seen.add(s)
                dedup.append(s)
        out[key] = dedup
    return out


def main():
    rows = []
    for z in ZODIACS:
        rp, sp = REAL / f"{z}.json", CONTENT / f"{z}.md"
        row = {"生肖": z, "真書": None, "站內": None}
        if rp.exists():
            row["真書"] = real_stars(rp)
        if sp.exists():
            row["站內"] = site_stars(sp)
        rows.append(row)

    for r in rows:
        z = r["生肖"]
        if not r["真書"]:
            print(f"== {z}: 真書未抄")
            continue
        rs, ss = r["真書"], r["站內"] or {"吉星": [], "凶星": []}
        for key in ("吉星", "凶星"):
            real_set, site_set = set(rs[key]), set(ss[key])
            extra = sorted(site_set - real_set)
            missing = sorted(real_set - site_set)
            print(f"== {z} · {key}")
            print(f"   真書: {rs[key] or ['?']}")
            print(f"   站內: {ss[key] or ['?']}")
            if extra:
                print(f"   🔴 站內多推（真書冇）: {extra}")
            if missing:
                print(f"   🟠 站內漏推（真書有）: {missing}")
            if not extra and not missing:
                print("   🟢 一致")
    if "--json" in sys.argv:
        out = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote", out)


if __name__ == "__main__":
    main()

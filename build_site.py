#!/usr/bin/env python3
"""將 content/*.md 組合成單頁靜態站（we1co 風格，dark theme）。
新增：九宮飛星互動圖（2024-2030）、犯太歲速查、免責聲明更新。
修正：九宮化解物品改用蘇民峰原作、犯太歲飾物三合六合排除法、寒熱平命邊界修正（立夏/立秋/立冬）、生肖運程預設收折。"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUT = ROOT / "index.html"

ZODIAC_ORDER = ["鼠","牛","虎","兔","龍","蛇","馬","羊","猴","雞","狗","豬"]
ZODIAC_EN = {
    "鼠":"Rat","牛":"Ox","虎":"Tiger","兔":"Rabbit","龍":"Dragon","蛇":"Snake",
    "馬":"Horse","羊":"Goat","猴":"Monkey","雞":"Rooster","狗":"Dog","豬":"Pig",
}
YEARS = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
YEAR_CN = {2024:"甲辰", 2025:"乙巳", 2026:"丙午", 2027:"丁未", 2028:"戊申", 2029:"己酉", 2030:"庚戌"}

def year_options(selected=2027):
    return "\n".join(
        f'<option value="{y}"{" selected" if y == selected else ""}>{y} {YEAR_CN[y]}年</option>'
        for y in YEARS
    )

TOOL_SECTIONS = [("飛星","✦ 九宮飛星"),("犯太歲","⚡ 犯太歲速查"),("mingcalc","🔥 寒熱平命"),("大門地氈","🧭 大門地氈")]

def quick_index():
    lines = ['<div class="quick-index">', '<span class="qi-label">快速索引</span>']
    for anchor, label in TOOL_SECTIONS:
        lines.append(f'<a href="#{anchor}">{label}</a>')
    lines.append('<span class="qi-label" style="margin-left:6px">生肖</span>')
    for z in ZODIAC_ORDER:
        lines.append(f'<a href="#{z}">{z}</a>')
    lines.append('</div>')
    return "\n".join(lines)


def md_to_html(md):
    lines = md.split("\n"); out = []; in_list = False
    for ln in lines:
        s = ln.strip()
        if not s:
            if in_list: out.append("</ul>"); in_list = False
            continue
        if s == "---":
            if in_list: out.append("</ul>"); in_list = False
            out.append('<hr class="divider">'); continue
        if s.startswith("### "):
            if in_list: out.append("</ul>"); in_list = False
            out.append(f'<h4>{s[4:]}</h4>'); continue
        if s.startswith("## "):
            if in_list: out.append("</ul>"); in_list = False
            out.append(f'<h3>{s[3:]}</h3>'); continue
        if s.startswith("- "):
            if not in_list: out.append("<ul>"); in_list = True
            item = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s[2:])
            out.append(f"<li>{item}</li>"); continue
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        out.append(f"<p>{s}</p>")
    if in_list: out.append("</ul>")
    return "\n".join(out)


def build():
    css = (pathlib.Path(__file__).resolve().parent / 'assets' / 'sokman.css').read_text(encoding='utf-8')
    js = (pathlib.Path(__file__).resolve().parent / 'assets' / 'sokman.js').read_text(encoding='utf-8')

    hero = """<!DOCTYPE html>
<html lang="zh-Hant" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="2027 丁未羊年十二生肖運程 — 以開源曆法庫計算干支/飛星，九宮化解物品及犯太歲規則對照蘇民峰原作。僅供娛樂參考。">
<title>2027 丁未羊年 · 十二生肖運程（AI 風格生成）</title>
<style>""" + css + """</style>
</head>
<body>
<div class="container">

<div class="hero">
<div class="hero-badge">2027 · 丁未 · 九紫入中</div>
<h1>🐏 2027 丁未羊年 十二生肖運程</h1>
<p>以開源曆法庫計算真實干支／飛星／太歲關係 · 九宮化解物品、飾物規則及熱平寒命對照蘇民峰原作</p>
<div class="disclaimer">
⚠️ <b>免責聲明</b>：本頁內容為 <b>AI 風格模仿生成</b>，並非蘇民峰親筆著作，僅供娛樂參考。曆法／干支／飛星／犯太歲關係由開源庫計算（客觀可驗），<b>九宮化解物品、犯太歲飾物建議及熱平寒命分類均經對照蘇民峰原作</b>（蘇民峰曆書九宮飛星化解篇、犯太歲飾物篇；此法為蘇氏通用推理，每年按飛星方位重新適用）。如有疑問，請諮詢專業風水師。
</div>
</div>

<div class="year-bar">
<div class="year-card"><div class="y">丁未</div><div class="g">天干地支</div><div class="s">火土之年</div></div>
<div class="year-card"><div class="y">九紫</div><div class="g">入中宮星</div><div class="s">桃花喜慶</div></div>
<div class="year-card"><div class="y">西南</div><div class="g">太歲方位</div><div class="s">歲破在東北</div></div>
<div class="year-card"><div class="y">2022-27</div><div class="g">木火流年</div><div class="s">利寒命人</div></div>
</div>

""" + quick_index() + """
"""

    fly_section = """
<div class="section" id="飛星">
<div class="section-title"><span class="zodiac-icon">✦</span><span>九宮飛星互動圖</span></div>
<p style="font-size:13.5px;color:var(--dim);margin-bottom:10px">選擇年份查看當年九宮飛星分佈及化解方法。吉星宜催旺，凶星宜化解。<br>化解物品依照蘇民峰體系（見蘇民峰《生肖運程》曆書九宮飛星篇）：凶星以音樂盒（金屬發聲泄土）化二黑五黃，粉紅色物件泄三碧木；吉星以一杯水催六白八白、四枝富貴竹催四綠文昌、四盆植物九枝紅花催九紫喜慶。此法每年按飛星方位重新適用。</p>
<div class="fly-wrap">
<div class="fly-controls">
<label>選擇年份：</label>
<select id="fly-year" onchange="renderFly()">
""" + year_options(2027) + """
</select>
<button onclick="startAR()" style="background:var(--accent);color:#fff;border:none;border-radius:8px;padding:7px 14px;font-size:13.5px;cursor:pointer;font-weight:600">📷 AR 方位模式</button>
</div>
<div class="fly-year-label" id="fly-label"></div>
<div class="fly-dir" id="fly-dir" style="font-size:11.5px;color:var(--orange);margin-bottom:8px;text-align:center"></div>
<div class="fly-grid" id="fly-grid"></div>
</div>
</div>

<div id="ar-overlay">
<video id="ar-video" playsinline muted></video>
<canvas id="ar-canvas"></canvas>
<div class="ar-note-top">移動手機，鏡頭指向方位即可看到該方位的飛星／流年／化解</div>
<div id="ar-info"></div>
<button id="ar-close" onclick="stopAR()">✕ 關閉</button>
<button id="ar-cam-toggle" onclick="arToggleCam()">📷 實景開</button>
<div id="ar-slider-wrap"><span>手動調較方位</span><input type="range" id="ar-slider" min="0" max="359" value="0"><span id="ar-slider-val">0°</span></div>
</div>
"""

    ts_section = """
<div class="section" id="犯太歲">
<div class="section-title"><span class="zodiac-icon">⚡</span><span>犯太歲速查</span></div>
<p style="font-size:13.5px;color:var(--dim);margin-bottom:6px">選擇年份及生肖，查看犯太歲類型及化解建議。<br>飾物建議依照蘇民峰體系（見蘇民峰曆書犯太歲篇）：佩戴當年太歲生肖的三合／六合飾物（合太歲）；若該三合／六合生肖自身亦犯太歲，則不可佩戴。</p>
<div class="ts-controls">
<label>年份：</label>
<select id="ts-year" onchange="renderTS()">
""" + year_options(2027) + """
</select>
<label>生肖：</label>
<select id="ts-zodiac" onchange="renderTS()">
<option value="鼠">鼠</option><option value="牛">牛</option><option value="虎">虎</option>
<option value="兔">兔</option><option value="龍">龍</option><option value="蛇">蛇</option>
<option value="馬">馬</option><option value="羊" selected>羊</option><option value="猴">猴</option>
<option value="雞">雞</option><option value="狗">狗</option><option value="豬">豬</option>
</select>
</div>
<div class="ts-result" id="ts-result"></div>
</div>
"""

    ming_section = """
<div class="section" id="mingcalc">
<div class="section-title"><span class="zodiac-icon">🔥</span><span>寒熱平命快查 <span class="zodiac-en">· 蘇民峰招牌論命法</span></span></div>
<p style="font-size:14px;color:var(--dim);margin-bottom:14px">以出生當日所處節氣為準，判斷寒熱平三命。<strong>蘇民峰官方定義</strong>（masterso.com）：寒命＝立秋後至驚蟄前出生（跨年，喜火）；熱命＝立夏後至立秋前出生（喜水）；平命＝驚蟄後至立夏前出生（喜水不忌火，清明前較平、清明後較熱之平命）。揀你嘅出生日期：</p>
<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:end;margin-bottom:8px">
<label style="font-size:13px;color:var(--dim)">出生年月日
<input id="ming-date" type="date" min="1930-01-01" max="2035-12-31" value="1990-06-01" style="display:block;margin-top:4px;background:rgba(255,255,255,0.06);border:1px solid var(--border);border-radius:8px;color:var(--text);padding:8px 10px;font-size:14px"></label>
<button onclick="calcMing()" style="background:var(--accent);color:#fff;border:none;border-radius:8px;padding:9px 18px;font-size:14px;cursor:pointer;font-weight:600">計算</button>
</div>
<div id="ming-result" class="ming-result"></div>
<p style="font-size:12px;color:var(--dim);margin-top:12px">※ 以出生當日所處節氣（立秋／驚蟄／立夏／清明）為準，數據由開源曆法庫計算。日期預設只為示範。</p>
</div>
"""

    # ── 大門地氈旺宅化病法 ──
    door_section = """
<div class="section" id="大門地氈">
<div class="section-title"><span class="zodiac-icon">🧭</span><span>大門地氈旺宅化病法 <span class="zodiac-en">· 蘇民峰獨門法</span></span></div>
<p style="font-size:13.5px;color:var(--dim);margin-bottom:10px">依蘇民峰「大門地氈顏色旺宅化病方法」（見蘇民峰《生肖運程》曆書，通用推理體系）：每年飛星隨方位流轉，大門開向不同方位會迎入吉凶星，以特定顏色地氈及化解物催旺吉星、洩化凶星（五行生剋推理）。本站按你選擇的年份即時重新推算。選你大門開向：</p>
<div class="ts-controls">
<label>年份：</label>
<select id="door-year" onchange="renderDoor()">
""" + year_options(2027) + """
</select>
<label>大門開向：</label>
<select id="door-dir" onchange="renderDoor()">
<option value="東南">東南</option><option value="南">正南</option><option value="西南">西南</option>
<option value="東" selected>正東</option><option value="中宮">中宮</option><option value="西">正西</option>
<option value="東北">東北</option><option value="北">正北</option><option value="西北">西北</option>
</select>
</div>
<div class="fly-year-label" id="door-label"><!-- label --></div>
<div class="fly-grid" id="door-grid" style="max-width:440px;margin:0 auto 12px"></div>
<div class="ts-result" id="door-result" style="display:none"></div>
</div>
"""

    toggle = '<div class="toggle-all"><button onclick="toggleAll(true)">全部展開</button><button onclick="toggleAll(false)">全部收縮</button></div>\n'

    badges = {
        "鼠":("badge tai","害太歲"),"牛":("badge tai","沖太歲"),"虎":("badge normal","暗合"),
        "兔":("badge he","三合"),"龍":("badge normal","平常"),"蛇":("badge normal","平常"),
        "馬":("badge he","六合"),"羊":("badge tai","值太歲"),"猴":("badge normal","平常"),
        "雞":("badge normal","平常"),"狗":("badge tai","刑太歲"),"豬":("badge he","三合"),
    }
    body = []
    for z in ZODIAC_ORDER:
        md_file = CONTENT / f"{z}.md"
        if not md_file.exists(): continue
        md = md_file.read_text(encoding="utf-8")
        html_body = md_to_html(md)
        cls, label = badges[z]
        body.append(f'<details class="zodiac-sec" id="{z}">\n<summary><span class="zodiac-icon">{z}</span><span style="flex:1">屬{z}的你 <span class="zodiac-en">· {ZODIAC_EN[z]}</span></span><span class="badge {cls}">{label}</span></summary>\n<div class="sec-body">\n{html_body}\n</div>\n</details>')

    footer = """
<div class="footer">
<p>曆法數據（天干地支 · 節氣月干支 · 九宮飛星 · 太歲沖合刑害）由開源曆法庫計算 · 九宮化解物品及犯太歲飾物規則對照蘇民峰原作 · 運程文字由 AI 按蘇民峰文風生成，僅供娛樂參考</p>
<p>每年運程不同，過往內容只供參考，不應直接抄用</p>
<p>© 2027 生肖運程生成器 · 非官方產品，與作者無關</p>
</div>
<button id="toTop" aria-label="返回頂部">↑</button>
</div>
<script>""" + js + """
renderFly();
renderTS();
calcMing();
renderDoor();
</script>
</body>
</html>"""

    OUT.write_text(hero + fly_section + ts_section + ming_section + door_section + toggle + "\n".join(body) + footer, encoding="utf-8")
    print(f"OK index.html: {OUT.stat().st_size/1024:.0f} KB, {len(body)} 生肖")


if __name__ == "__main__":
    build()

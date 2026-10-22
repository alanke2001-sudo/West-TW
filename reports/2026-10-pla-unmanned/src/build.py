# -*- coding: utf-8 -*-
"""產生離線網頁 index.html、entries.json、entries.csv。
用法（於報告資料夾）：python3 src/build.py
"""
import base64, csv, html, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from data import REFS, CHAPTERS, E, TIMELINE, RANGE_CHART

TITLE = "解放軍無人系統與直升機威脅資料庫"
DATE = "2026-10-22"
LABEL = {"fact": "事實", "off": "官方評估", "est": "推估", "calc": "本報告推算", "gap": "資料缺口"}
esc = html.escape


def sup(refs):
    return "<sup>" + ",".join(f'<a href="#r{r}">{r}</a>' for r in refs) + "</sup>" if refs else ""


SHORT = {"U07": "其他 BZK／彩虹-4B", "U10": "閱兵新型無人作戰機", "U12": "殲-6 改裝無人機", "U14": "中國電科蜂群",
         "U17": "FPV／多旋翼", "U18": "艦載無人直升機", "U20": "076 型四川艦", "G01": "武裝機器狗", "G02": "機器狼群",
         "G03": "部隊試驗與登陸演練", "G04": "宇樹科技關聯", "G06": "閱兵無人地面車", "M01": "JARI 虎鯨無人艇",
         "M02": "無人掃雷／作戰艇", "C01": "LY-1 雷射", "C02": "颶風-3000 微波", "C03": "颶風-2000 微波", "C04": "沉默獵手雷射",
         "C05": "LW-30／LW-60 雷射", "C06": "光箭、天盾雷射", "C07": "天穹與遠漠", "C08": "YLC-48／DWL002", "C09": "閱兵反無人機方隊",
         "C10": "625 型彈砲合一", "C11": "干擾槍與基地防護", "C12": "閱兵電戰裝備", "C13": "產業規模與實測", "H01": "前衛系列",
         "H02": "QW-12／飛弩-16", "H04": "625 型（反直升機）", "H05": "紅旗-11", "H06": "熱焰彈干擾直升機", "H07": "直升機危險逼近",
         "H08": "艦艇雷射照射", "H09": "解放軍自身評估", "H10": "無人機與定向能", "H11": "反直升機地雷（缺口）",
         "U15": "ASN-301 反輻射", "U13": "九天母機", "M03": "HSU100 潛航器", "M04": "AJX002 潛航器"}
COLHEAD = {"c1": "無人飛行載具", "c2": "機器狗與地面載具", "c3": "水面與水下載具", "c4": "反無人機與電戰", "c5": "直升機威脅"}


def short(e):
    return SHORT.get(e["id"]) or re.split(r"[（「]", e["name"])[0].strip()


# ── 圖一：分類總覽 ──
def fig_overview():
    cols = [(a, n, t) for a, n, t, _ in CHAPTERS]
    W, colw, gap, x0 = 990, 180, 15, 15
    y0 = 58
    parts, maxy = [], 0
    for i, (a, no, t) in enumerate(cols):
        x = x0 + i * (colw + gap)
        es = [e for e in E if e["ch"] == a]
        parts.append(f'<rect x="{x}" y="{y0-44}" width="{colw}" height="36" class="d-hd"/>'
                     f'<text x="{x+colw/2}" y="{y0-21}" text-anchor="middle" class="d-th">{COLHEAD[a]}（{len(es)}）</text>')
        subs = []
        for e in es:
            if e["sub"] not in subs:
                subs.append(e["sub"])
        y = y0
        for s in subs:
            items = [short(e) for e in es if e["sub"] == s]
            h = 30 + 19 * len(items)
            parts.append(f'<rect x="{x}" y="{y}" width="{colw}" height="{h}" class="d-box"/>'
                         f'<text x="{x+10}" y="{y+20}" class="d-ts">{esc(s)}</text>')
            for j, it in enumerate(items):
                parts.append(f'<text x="{x+12}" y="{y+40+19*j}" class="d-t">· {esc(it)}</text>')
            y += h + 8
        maxy = max(maxy, y)
    H = maxy + 6
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="解放軍無人系統分類總覽">' + "".join(parts) + "</svg>")


# ── 圖二：射程與最低攔截高度 ──
def fig_range():
    W, left, right, top, bh, gap = 760, 170, 40, 40, 26, 12
    maxr = 16
    sx = lambda v: left + (W - left - right) * v / maxr
    n = len(RANGE_CHART)
    H = top + n * (bh + gap) + 40
    p = []
    for k in range(0, maxr + 1, 2):
        x = sx(k)
        p.append(f'<line x1="{x}" y1="{top-8}" x2="{x}" y2="{H-34}" class="d-grid"/>'
                 f'<text x="{x}" y="{H-16}" text-anchor="middle" class="d-ax">{k}</text>')
    p.append(f'<text x="{W-right}" y="{top-16}" text-anchor="end" class="d-ax">最大射程（公里）</text>')
    cls = {"便攜": "b-man", "野戰": "b-shorad", "定向能": "b-de"}
    for i, (nm, r, alt, kind) in enumerate(RANGE_CHART):
        y = top + i * (bh + gap)
        p.append(f'<text x="{left-10}" y="{y+bh/2+5}" text-anchor="end" class="d-t">{esc(nm)}</text>'
                 f'<rect x="{left}" y="{y}" width="{sx(r)-left}" height="{bh}" class="{cls[kind]}"/>')
        note = f"{r} 公里" + (f"｜最低 {alt} 公尺" if alt else "")
        if kind == "定向能":
            note += "（設計目標為無人機）"
        p.append(f'<text x="{sx(r)+8}" y="{y+bh/2+5}" class="d-t">{esc(note)}</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="可威脅直升機之武器射程比較">' + "".join(p) + "</svg>"


# ── 圖三：時間線 ──
def fig_timeline():
    W, top, step, xl = 760, 20, 40, 110
    H = top + step * len(TIMELINE) + 4
    p = [f'<line x1="{xl}" y1="{top}" x2="{xl}" y2="{H-14}" class="d-axis"/>']
    for i, (d, ev, refs) in enumerate(TIMELINE):
        y = top + i * step + 14
        yr = d[:4]
        p.append(f'<text x="{xl-16}" y="{y+5}" text-anchor="end" class="d-ts">{d}</text>'
                 f'<circle cx="{xl}" cy="{y}" r="6" class="d-dot{" y"+yr}"/>'
                 f'<text x="{xl+16}" y="{y+5}" class="d-t">{esc(ev)}</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="解放軍無人系統對台相關活動時間線">' + "".join(p) + "</svg>"


PHOTOS_META = json.load(open(os.path.join(HERE, "photos.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "photos.json")) else []
HAS_PHOTO = {p["id"] for p in PHOTOS_META}


def credit(p):
    lic = f'<a href="{esc(p["license_url"])}">{esc(p["license"])}</a>' if p["license_url"] else esc(p["license"])
    return f'圖片：{esc(p["author"] or "未署名")}，{lic}，取自 <a href="{esc(p["page"])}">Wikimedia Commons</a>'


def photo_appendix():
    names = {e["id"]: e["name"] for e in E}
    out = []
    for a, _, t, _ in CHAPTERS:
        ps = [p for p in PHOTOS_META if dict((e["id"], e["ch"]) for e in E)[p["id"]] == a]
        if not ps:
            continue
        out.append(f'<h3>{esc(t)}</h3><div class="photos">')
        for p in ps:
            b64 = base64.b64encode(open(os.path.join(OUT, "figures", "photos", p["img"]), "rb").read()).decode()
            out.append(f'<figure class="photo" id="p-{p["img"][:-4]}"><img src="data:image/jpeg;base64,{b64}" alt="{esc(names[p["id"]])}" loading="lazy">'
                       f'<figcaption><a class="eid" href="#{p["id"]}">{p["id"]}</a> <b>{esc(names[p["id"]])}</b>'
                       f'{"：" + esc(p["caption"]) if p["caption"] else ""}<br><span class="cr">{credit(p)}</span></figcaption></figure>')
        out.append('</div>')
    return "".join(out)


def card(e):
    rows = []
    for k, lab in (("kind", "類型"), ("maker", "研製單位"), ("status", "狀態")):
        if e.get(k):
            rows.append(f"<div><dt>{lab}</dt><dd>{esc(e[k])}</dd></div>")
    body = []
    if e["specs"]:
        body.append(f'<p><b>主要性能</b>{esc(e["specs"])}</p>')
    if e["activity"]:
        body.append(f'<p><b>動態與部署</b>{esc(e["activity"])}</p>')
    if e["assess"]:
        body.append(f'<p><b>研判意涵</b><span class="tag {e["alabel"]}">{LABEL[e["alabel"]]}</span>{esc(e["assess"])}</p>')
    search = " ".join([e["id"], e["name"], e["alias"], e["kind"], e["maker"], e["sub"]] + e["tags"])
    tags = "".join(f'<span class="et">{esc(t)}</span>' for t in e["tags"])
    return (f'<article class="card" id="{e["id"]}" data-ch="{e["ch"]}" data-s="{esc(search.lower())}">'
            f'<header><span class="eid">{e["id"]}</span><h4>{esc(e["name"])}</h4>'
            f'{"<span class=alias>" + esc(e["alias"]) + "</span>" if e["alias"] else ""}'
            f'<span class="tag {e["label"]}">{LABEL[e["label"]]}</span></header>'
            f'<dl>{"".join(rows)}</dl>{"".join(body)}'
            f'<footer><span class="tags">{tags}</span><span class="src">{f'<a href="#p-{e["id"]}-1">圖片</a>　' if e["id"] in HAS_PHOTO else ""}出處{sup(e["refs"]) or "：無"}</span></footer></article>')


CSS = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
JS = open(os.path.join(HERE, "filter.js"), encoding="utf-8").read()


def build():
    n = {a: sum(1 for e in E if e["ch"] == a) for a, _, _, _ in CHAPTERS}
    out = []
    w = out.append
    w(f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
      f'<title>{TITLE}</title><style>{CSS}</style></head><body><div class="doc">')
    w('<p style="max-width:720px;margin:20px auto 0;font-size:14px"><a href="../../index.html">← 返回 West-TW 報告資料庫</a></p>')
    w(f'''<header class="cover"><div class="cls">公開資訊彙整 · OSINT 資料庫</div><h1>{TITLE}</h1>
<p class="sub">無人機、機器狗與無人地面載具、無人艇與潛航器、反無人機與電子干擾體系，以及可能危害直升機飛行的武器與作為</p>
<div class="meta"><span>資料截止：{DATE}</span><span>條目：{len(E)} 筆</span><span>出處：{len(REFS)} 筆</span><span>性質：公開資訊彙整，非機密情資</span></div></header>''')
    w('<div class="col">')
    w('<p class="lead">本資料庫彙整 2025 年北京閱兵受閱清單、台灣國防部與日本防衛省公布的共機動態、Janes、The War Zone、CNA、美國陸軍戰院等公開來源，逐筆整理解放軍無人系統與反無人機裝備，並另立一章整理可能危害直升機飛行的武器與實際事件。每筆條目標註判讀層級並以上標編號連結文末出處。</p>')
    w('''<div class="legend" role="note"><span><span class="tag fact">事實</span>已發生、公開可查證</span><span><span class="tag off">官方評估</span>官方或官媒之說法與研判</span><span><span class="tag est">推估</span>智庫、媒體或本報告之分析</span><span><span class="tag gap">資料缺口</span>公開資料未見</span></div>''')
    w('''<div class="keypts"><h3>摘要</h3><ul>
<li><span class="tag fact">事實</span>2025-09-03 北京閱兵首度以獨立方隊展示無人空中、地面、海上作戰系統與反無人機系統，包括攻擊-11、多型新式無人作戰機、機器狼、大型無人潛航器、LY-1 雷射與高功率微波武器。<sup><a href="#r1">1</a>,<a href="#r3">3</a>,<a href="#r5">5</a></sup></li>
<li><span class="tag fact">事實</span>對台最常見的是 BZK-005、TB-001、攻擊-2 等中空長航時無人機，已多次繞台或進入防空識別區；BZK-005 已有多種電子情報變型。<sup><a href="#r8">8</a>,<a href="#r10">10</a>,<a href="#r13">13</a></sup></li>
<li><span class="tag fact">事實</span>攻擊型無人系統正快速成形：東部戰區 2025-10 實射反輻射巡飛彈，九天母機 2025-12 首飛，衛星影像顯示殲-6 改裝無人機部署於福建基地。<sup><a href="#r14">14</a>,<a href="#r18">18</a>,<a href="#r21">21</a></sup></li>
<li><span class="tag est">推估</span>機器狗已由展示走向部隊試驗，外媒彙整指第 72 集團軍曾在登陸演練中用於灘岸破障與運補。<sup><a href="#r31">31</a></sup></li>
<li><span class="tag fact">事實</span>對直升機的威脅包括射高涵蓋貼地至 4 公里的便攜防空飛彈、彈砲合一系統，以及戰機在直升機前方施放熱焰彈（2023 加拿大、2024 澳洲）與艦艇雷射照射航空器等實際事件。<sup><a href="#r42">42</a>,<a href="#r45">45</a>,<a href="#r46">46</a>,<a href="#r47">47</a></sup></li>
<li><span class="tag gap">資料缺口</span>本次公開檢索未找到解放軍列裝反直升機地雷的可靠報導。</li>
</ul></div>''')
    toc = "".join(f'<li><a href="#{a}">{no} {t}</a></li>' for a, no, t, _ in CHAPTERS)
    w(f'<nav class="toc" aria-label="目錄"><ol><li><a href="#c0">總覽與條目索引</a></li>{toc}<li><a href="#c6">對台相關活動時間線</a></li><li><a href="#c7">研判與觀察指標</a></li>{'<li><a href="#photos">裝備圖片</a></li>' if PHOTOS_META else ''}<li><a href="#refs">參考資料</a></li></ol></nav>')
    # 總覽
    w('<h2 id="c0"><span class="no">總覽</span>分類與條目索引</h2>')
    w(f'<p>本資料庫共 {len(E)} 筆條目，分為五類：' + "、".join(f"{t} {n[a]} 筆" for a, _, t, _ in CHAPTERS) + '。下圖依任務細分，表格可點選跳至各條目。</p>')
    w('</div>')
    w(f'<figure id="fig01"><div class="scroll">{fig_overview()}</div><figcaption><b>圖 01</b>解放軍無人系統與直升機威脅分類總覽（括號內為條目數）。資料來源：本資料庫各條目。</figcaption></figure>')
    w('<div class="col">')
    rows = "".join(f'<tr><td class="num"><a href="#{e["id"]}">{e["id"]}</a></td><td>{esc(e["name"])}</td><td>{esc(e["kind"])}</td><td>{esc(e["status"])}</td></tr>' for e in E)
    w(f'<div class="tbl"><table><thead><tr><th>編號</th><th>名稱</th><th>類型</th><th>狀態</th></tr></thead><tbody>{rows}</tbody></table></div>')
    # 篩選列
    chips = "".join(f'<button type="button" data-ch="{a}" aria-pressed="false">{t}</button>' for a, _, t, _ in CHAPTERS)
    w(f'''<div class="filter" role="search"><input type="search" id="q" placeholder="搜尋條目：例如 雷射、巡飛彈、BZK、機器狗" aria-label="搜尋條目">
<div class="chiprow"><button type="button" data-ch="" aria-pressed="true">全部</button>{chips}</div><p class="count" id="cnt"></p></div>''')
    for a, no, t, intro in CHAPTERS:
        w(f'<h2 id="{a}"><span class="no">{no}</span>{t}</h2><p>{esc(intro)}</p>')
        if a == "c5":
            w('</div>')
            w(f'<figure id="fig02"><div class="scroll">{fig_range()}</div><figcaption><b>圖 02</b>可威脅直升機之主要武器最大射程與最低攔截高度（公開資料）。便攜防空飛彈與紅旗-17A 的資料取自出處 41 至 43，雷射與高功率微波取自出處 34、36；後兩者的設計目標為無人機，列出以供比較。直升機貼地飛行、懸停與著陸時通常低於 100 公尺，皆在便攜飛彈的攔截高度內。</figcaption></figure>')
            w('<div class="col">')
        subs = []
        for e in E:
            if e["ch"] == a and e["sub"] not in subs:
                subs.append(e["sub"])
        for s in subs:
            w(f'<h3 class="sub" data-ch="{a}">{esc(s)}</h3>')
            for e in E:
                if e["ch"] == a and e["sub"] == s:
                    w(card(e))
    w('<h2 id="c6"><span class="no">第六章</span>對台相關活動時間線</h2><p>依日期整理與台灣直接相關、或代表能力里程碑的公開事件。</p></div>')
    w(f'<figure id="fig03"><div class="scroll">{fig_timeline()}</div><figcaption><b>圖 03</b>解放軍無人系統對台相關活動時間線（2022 至 2026 年）。資料來源：見下表各列出處。</figcaption></figure><div class="col">')
    rows = "".join(f'<tr><td class="num">{d}</td><td>{esc(ev)}{sup(r)}</td></tr>' for d, ev, r in TIMELINE)
    w(f'<div class="tbl"><table><thead><tr><th>年月</th><th>事件</th></tr></thead><tbody>{rows}</tbody></table></div>')
    w('''<h2 id="c7"><span class="no">結論</span>研判與觀察指標</h2>
<h3>研判</h3><ul>
<li><span class="tag est">推估</span>解放軍無人系統已形成「高空偵察、中空長航時察打、隱身僚機、蜂群母機、巡飛彈、地面與水下無人載具」的完整譜系，多數仍在試驗或展示階段，但對台偵察與電子情報蒐集已常態化。</li>
<li><span class="tag est">推估</span>開戰初期可能以殲-6 改裝無人機、反輻射巡飛彈與蜂群消耗並壓制台灣防空雷達，再由有人機與攻擊-11 類無人機跟進打擊。</li>
<li><span class="tag est">推估</span>反無人機已升格為獨立作戰體系，雷射、高功率微波與干擾的目標是削弱台灣以無人機反登陸的效果。</li>
<li><span class="tag est">推估</span>直升機在灘頭、近岸與城鎮低空作業時，同時面對便攜防空飛彈、彈砲合一系統、FPV 與巡飛彈，以及大範圍電子干擾；平時則可能遭遇熱焰彈、近距離逼近與雷射照射等灰色地帶干擾。</li>
</ul>
<h3>觀察指標</h3><ul>
<li>BZK-005、TB-001、攻擊-2 以外的新機型（如攻擊-11、彩虹-7、九天）是否出現在台灣周邊空域。</li>
<li>殲-6 改裝無人機的部署基地與數量變化。</li>
<li>076 型艦服役與攻擊-21 上艦進度。</li>
<li>機器狗、無人車在東部戰區登陸演練中的運用頻率。</li>
<li>LY-1、颶風-3000 等反無人機系統是否部署到沿海機場、港口或兩棲艦。</li>
<li>解放軍艦機對外國直升機施放熱焰彈、雷射照射或危險逼近事件是否擴及台灣周邊。</li>
</ul>''')
    if PHOTOS_META:
        w(f'<h2 id="photos"><span class="no">附錄一</span>裝備圖片</h2><p>以下為本資料庫提及裝備中，可在 Wikimedia Commons 找到自由授權照片者，共 {len(PHOTOS_META)} 張、涵蓋 {len(HAS_PHOTO)} 筆條目。每張圖下方註明作者與授權，點選編號可回到條目。部分照片為航展或閱兵展示機，外觀可能與服役型號不同；未列出的條目為公開圖庫無自由授權照片。</p></div>')
        w(f'<div class="photowrap">{photo_appendix()}</div><div class="col">')
    w(f'<h2 id="refs"><span class="no">{"附錄二" if PHOTOS_META else "附錄"}</span>參考資料</h2><ol class="refs">')
    for k in sorted(REFS):
        t, u = REFS[k]
        host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        w(f'<li id="r{k}">{esc(t)}。<a href="{esc(u)}">{esc(host)}</a></li>')
    w('</ol><p class="note">本資料庫僅彙整公開資訊；部分外文來源係經新聞或百科轉述，正式引用前建議查閱原始報告。「推估」不代表已知作戰計畫。</p>')
    w(f'</div></div><script>{JS}</script></body></html>')
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write("".join(out))

    # 資料檔
    data = [{k: e[k] for k in ("id", "name", "alias", "kind", "maker", "status", "specs", "activity", "assess", "tags")} |
            {"category": dict((a, t) for a, _, t, _ in CHAPTERS)[e["ch"]], "subcategory": e["sub"], "label": LABEL[e["label"]],
             "assess_label": LABEL[e["alabel"]], "sources": [{"no": r, "title": REFS[r][0], "url": REFS[r][1]} for r in e["refs"]]} for e in E]
    json.dump({"title": TITLE, "date": DATE, "entries": data}, open(os.path.join(OUT, "entries.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "entries.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        cw = csv.writer(fh)
        cw.writerow(["編號", "類別", "小類", "名稱", "別名", "類型", "研製單位", "狀態", "主要性能", "動態與部署", "研判意涵", "判讀層級", "標籤", "出處"])
        for d in data:
            cw.writerow([d["id"], d["category"], d["subcategory"], d["name"], d["alias"], d["kind"], d["maker"], d["status"], d["specs"],
                         d["activity"], d["assess"], d["label"], "、".join(d["tags"]), " ".join(s["url"] for s in d["sources"])])
    print("ok", len(E), "entries")


if __name__ == "__main__":
    build()

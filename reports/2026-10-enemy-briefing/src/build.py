# -*- coding: utf-8 -*-
"""由簡報檔產生離線網頁 index.html 與 figures/*.png。
用法（於報告資料夾）：python3 src/build.py
"""
import base64, html, io, os
from pptx import Presentation
from PIL import Image

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.path.join(OUT, "敵情威脅簡報.pptx")
TITLE = "敵情威脅：中共對臺軍事行動與航空威脅研析"
DATE = "2026-10-22"
esc = html.escape

LABEL = {"fact": "事實", "off": "官方評估", "est": "推估"}
# 原簡報只在資料來源頁列出 5 筆出處；僅在投影片本身點名來源時加註編號
REFS = [
    "中華民國國防部，115 年 4 月與 7 月漢光 42 號新聞資料。",
    "中華民國國防部，115 年 10 月 20、21 日中共解放軍臺海周邊海、空域動態。",
    "中央社，2026 年 10 月 12 日共軍區域演訓報導。",
    "Janes，Type 071／075 兩棲艦能力研究。",
    "瑞典國防研究局（FOI），2025，《Studying China's Military Power》。",
]
# 投影片編號 → (判斷標註, 出處編號)；未列者為簡報作者依公開資料所作的研析歸納（推估）
SLIDE_META = {
    5: ("off", [1]), 11: ("fact", []), 12: ("fact", []), 13: ("fact", []), 14: ("fact", []),
    17: ("fact", [4]), 18: ("fact", []), 20: ("est", [4, 5]), 24: ("fact", [3]), 25: ("fact", [2]),
    35: ("fact", [1]), 38: ("fact", []), 39: ("fact", []), 40: ("fact", []), 41: ("fact", []),
    42: ("fact", []), 43: ("fact", []),
}
FOOTER_PREFIX = ("資料：", "公開資料參考")


def sup(refs):
    return "<sup>" + ",".join(f'<a href="#r{r}">{r}</a>' for r in refs) + "</sup>" if refs else ""


def slide_parts(slide):
    """回傳 (標題, 條列, 提醒句, 圖片 sha1)。"""
    texts, pic = [], None
    for sh in slide.shapes:
        if sh.shape_type == 13 and pic is None:
            pic = sh.image
        elif sh.has_text_frame and sh.text_frame.text.strip():
            texts.append(sh.text_frame.text.strip())
    texts = [t for t in texts if not t.isdigit() and not t.startswith(FOOTER_PREFIX)]
    title = texts[0] if texts else ""
    bullets, notes = [], []
    for t in texts[1:]:
        for line in t.splitlines():
            line = line.strip()
            if line.startswith("▸"):
                bullets.append(line.lstrip("▸ ").strip())
            elif line:
                notes.append(line)
    return title, bullets, notes, pic


def save_figures(prs):
    """各張概念圖只輸出一次，回傳 sha1 → (圖號, data URI)。"""
    figs = {}
    for slide in prs.slides:
        for sh in slide.shapes:
            if sh.shape_type != 13 or sh.image.sha1 in figs:
                continue
            n = len(figs) + 1
            img = Image.open(io.BytesIO(sh.image.blob)).convert("RGB")
            img.save(os.path.join(OUT, "figures", f"圖{n:02d}.png"))
            img.thumbnail((720, 720))
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=72, optimize=True)
            figs[sh.image.sha1] = (n, "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
    return figs


CSS = """
:root{--bg:#eef1f2;--paper:#fff;--ink:#172129;--muted:#56636e;--rule:#d3dadf;--accent:#a8322a;
  --fact:#2f6b43;--off:#1d5596;--est:#93620b;
  --f-display:"Noto Serif TC","Songti TC","PMingLiU",serif;
  --f-body:"Noto Sans TC","PingFang TC","Microsoft JhengHei","WenQuanYi Zen Hei",sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0e1316;--paper:#151c21;--ink:#e3e9ed;
  --muted:#98a5af;--rule:#2b363e;--accent:#ec7065;--fact:#72c08d;--off:#7eaee9;--est:#e0b259;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0e1316;--paper:#151c21;--ink:#e3e9ed;--muted:#98a5af;--rule:#2b363e;
  --accent:#ec7065;--fact:#72c08d;--off:#7eaee9;--est:#e0b259;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.8;margin:0;
  padding:0 max(16px,env(safe-area-inset-right,0px)) 64px max(16px,env(safe-area-inset-left,0px))}
.col{max-width:760px;margin:0 auto}
a{color:var(--off)}
header.cover{padding-block:48px 28px;border-bottom:2px solid var(--ink);margin-bottom:28px}
.cls{font-family:var(--f-mono);font-size:12px;letter-spacing:.12em;color:var(--accent)}
h1{font-family:var(--f-display);font-size:clamp(26px,5vw,38px);line-height:1.3;margin:10px 0 12px;text-wrap:balance}
.sub{color:var(--muted);font-size:15px;margin:0}
.meta{font-family:var(--f-mono);font-size:12.5px;color:var(--muted);margin-top:16px;display:flex;flex-wrap:wrap;gap:6px 20px}
.note{background:var(--paper);border-left:3px solid var(--accent);padding:12px 16px;font-size:14.5px;margin:20px 0}
nav.toc ol{padding-left:1.4em;margin:8px 0}
h2{font-family:var(--f-display);font-size:25px;line-height:1.4;margin:56px 0 6px;scroll-margin-top:16px}
h2 .no{font-family:var(--f-mono);font-size:14px;color:var(--accent);margin-right:12px}
.time{color:var(--muted);font-size:14px;margin:0 0 16px}
figure{margin:18px 0}
figure img{width:100%;height:auto;display:block;border-radius:4px}
figcaption{font-size:13px;color:var(--muted);margin-top:6px}
.slide{background:var(--paper);border:1px solid var(--rule);border-radius:6px;padding:14px 18px 10px;margin:14px 0}
.slide h3{font-size:17px;margin:0 0 6px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.slide h3 .pg{font-family:var(--f-mono);font-size:12px;color:var(--muted);font-weight:400}
.slide ul{margin:0 0 8px;padding-left:1.3em}
.slide li{margin:2px 0}
.slide .remark{font-size:14px;color:var(--muted);margin:0 0 6px}
.tag{display:inline-block;font-size:11.5px;font-weight:500;line-height:1;padding:4px 7px 3px;border-radius:3px;
  border:1px solid currentColor;white-space:nowrap;margin-left:auto}
.tag.fact{color:var(--fact)}.tag.off{color:var(--off)}.tag.est{color:var(--est)}
.refs{font-size:13.5px;line-height:1.65;padding-left:2.4em}
"""


def build():
    prs = Presentation(DECK)
    figs = save_figures(prs)
    slides = list(prs.slides)
    cover = next(figs[sh.image.sha1] for sh in slides[0].shapes if sh.shape_type == 13)
    chapters, cur = [], None
    for i, s in enumerate(slides, 1):
        title, bullets, notes, pic = slide_parts(s)
        if title.startswith("第") and "章" in title.split("\n")[0]:
            raw = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
            name = "".join(raw[1].split()) if len(raw) > 1 else title
            time = raw[2].strip() if len(raw) > 2 else ""
            cur = {"no": len(chapters) + 1, "name": name, "time": time, "slides": []}
            chapters.append(cur)
        elif cur is not None and i < len(slides):
            cur["slides"].append((i, title, bullets, notes, pic))

    out = [f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(TITLE)}</title>'
           f'<style>{CSS}</style></head><body><div class="col">',
           '<p style="margin:20px 0 0;font-size:14px"><a href="../../index.html">← 返回 West-TW 報告資料庫</a></p>',
           '<header class="cover"><div class="cls">敵情威脅簡報 · 公開資訊研析</div>',
           f'<h1>{esc(TITLE)}</h1><p class="sub">50 頁簡報的網頁版：七章、約 60 分鐘報告，涵蓋作戰理念、攻臺編組、輸具、年度演訓、階段劃分與對我直升機威脅武器。</p>',
           f'<div class="meta"><span>資料截點 {DATE}（民國 115 年 10 月 22 日）</span><span>{len(slides)} 頁</span>'
           f'<span>{len(figs)} 張概念圖</span><span>{len(REFS)} 筆出處</span></div>'
           f'<figure><img src="{cover[1]}" alt="封面概念圖"><figcaption>圖 1　封面，AI 生成概念示意圖（原圖：figures/圖01.png）</figcaption></figure></header>',
           '<div class="note">原始簡報可下載 <a href="敵情威脅簡報.pptx">PowerPoint</a> 或 <a href="敵情威脅簡報.pdf">PDF</a>。'
           '簡報中的圖像為 AI 生成概念圖，非實際軍事紀實照片。原簡報僅在文末列出出處，未逐頁註明；本頁只在投影片點名來源處加註編號，'
           '其餘標為「推估」的頁面是簡報作者依公開資料所作的研析歸納。</div>',
           '<nav class="toc"><strong>目錄</strong><ol>']
    out += [f'<li><a href="#c{c["no"]}">{esc(c["name"])}</a></li>' for c in chapters]
    out.append('<li><a href="#refs">資料來源</a></li></ol></nav>')

    shown = set()
    for c in chapters:
        out.append(f'<h2 id="c{c["no"]}"><span class="no">第 {c["no"]} 章</span>{esc(c["name"])}</h2>')
        if c["time"]:
            out.append(f'<p class="time">{esc(c["time"])}</p>')
        for i, title, bullets, notes, pic in c["slides"]:
            if pic is not None and pic.sha1 not in shown:
                shown.add(pic.sha1)
                n, uri = figs[pic.sha1]
                out.append(f'<figure><img src="{uri}" alt="概念圖 {n}：{esc(title)}" loading="lazy">'
                           f'<figcaption>圖 {n}　AI 生成概念示意圖（原圖：figures/圖{n:02d}.png）</figcaption></figure>')
            lab, refs = SLIDE_META.get(i, ("est", []))
            out.append(f'<section class="slide" id="p{i}"><h3><span class="pg">P{i}</span>{esc(title)}'
                       f'<span class="tag {lab}">{LABEL[lab]}</span></h3><ul>')
            out += [f'<li>{esc(b)}</li>' for b in bullets]
            out.append('</ul>')
            out += [f'<p class="remark">{esc(n)}{sup(refs) if k == len(notes) - 1 else ""}</p>' for k, n in enumerate(notes)]
            if not notes and refs:
                out.append(f'<p class="remark">{sup(refs)}</p>')
            out.append('</section>')

    out.append('<h2 id="refs"><span class="no">附錄</span>資料來源</h2><ol class="refs">')
    out += [f'<li id="r{k}">{esc(r)}</li>' for k, r in enumerate(REFS, 1)]
    out.append('</ol><p class="time">原簡報未附連結；正式引用前請查閱原始資料。規格數字需逐筆確認。</p></div></body></html>')
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write("".join(out))
    print("chapters", [(c["no"], c["name"], len(c["slides"])) for c in chapters], "figs", len(figs))


if __name__ == "__main__":
    build()

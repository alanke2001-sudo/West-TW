# -*- coding: utf-8 -*-
"""從 Wikimedia Commons 下載附錄裝備圖片並記錄作者與授權。
用法（於報告資料夾）：
  python3 src/photos.py search 關鍵字      列出 Commons 候選圖檔與授權
  python3 src/photos.py fetch              依 data.py 的 PHOTOS 下載縮圖至 figures/photos/，寫出 src/photos.json
只接受自由授權（CC0、公有領域、CC BY、CC BY-SA）；其他授權會報錯並略過。
"""
import html, io, time, json, os, re, sys, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "West-TW-OSINT-report/1.0 (https://github.com/alanke2001-sudo/West-TW)"}
FREE = re.compile(r"^(CC0|Public domain|PD|Attribution$|CC BY(-SA)? [0-9.]+|CC BY(-SA)?$)", re.I)
WIDTH = 960
TW = 1280  # Wikimedia 標準縮圖寬度之一


def urlget(url):
    for k in range(30):
        time.sleep(2)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == 29:
                raise
            print("  429, retry-after", e.headers.get("retry-after"), flush=True)
            time.sleep(min(int(e.headers.get("retry-after") or 10), 620) + 5)
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            if k == 29:
                raise
            print("  network error, retrying:", e, flush=True)
            time.sleep(20)


def get(params):
    q = urllib.parse.urlencode({"format": "json", "formatversion": 2, **params})
    return json.loads(urlget(f"{API}?{q}"))


def thumb(url):
    # 只使用 Wikimedia 建議的標準縮圖寬度，避免下載原圖遭限速
    base, name = url.rsplit("/", 1)
    return base.replace("/wikipedia/commons/", "/wikipedia/commons/thumb/") + f"/{name}/{TW}px-{name}"


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def info(titles):
    d = get({"action": "query", "titles": "|".join(titles), "prop": "imageinfo",
             "iiprop": "url|extmetadata|size", "iiurlwidth": WIDTH})
    out = {}
    for p in d["query"]["pages"]:
        if "imageinfo" not in p:
            out[p["title"]] = None
            continue
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        v = lambda k: plain(m.get(k, {}).get("value", ""))
        out[p["title"]] = {"file": p["title"], "page": ii["descriptionurl"], "thumb": thumb(ii["url"]) if ii.get("width", 0) > TW else ii["url"], "orig": ii["url"],
                           "author": v("Artist") or v("Credit"), "license": v("LicenseShortName"),
                           "license_url": v("LicenseUrl"), "date": v("DateTimeOriginal")[:10], "desc": v("ImageDescription")[:200]}
    return out


def search(q):
    if q.startswith("Category:"):
        d = get({"action": "query", "list": "categorymembers", "cmtitle": q, "cmlimit": 50})
        titles = [h["title"] for h in d["query"]["categorymembers"] if h["ns"] == 6]
        print("subcats:", [h["title"] for h in d["query"]["categorymembers"] if h["ns"] == 14])
    else:
        d = get({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": 20})
        titles = [h["title"] for h in d["query"]["search"]]
    for t, m in info(titles).items() if titles else []:
        if m:
            ok = "OK " if FREE.match(m["license"]) else "-- "
            print(ok, t, "|", m["license"], "|", m["author"][:40], "|", m["desc"][:80])


def fetch():
    from data import PHOTOS
    os.makedirs(os.path.join(OUT, "figures", "photos"), exist_ok=True)
    jp = os.path.join(HERE, "photos.json")
    done = {(x["id"], x["file"]): x for x in json.load(open(jp, encoding="utf-8"))} if os.path.exists(jp) else {}
    meta, titles = [], [f for _, f, _ in PHOTOS]
    got = {}
    for i in range(0, len(titles), 40):
        got |= info(titles[i:i + 40])
    from PIL import Image
    for eid, f, cap in PHOTOS:
        name = f"{eid}-{len([x for x in meta if x['id'] == eid]) + 1}.jpg"
        old = done.get((eid, f.replace("_", " ")))
        if old and old["img"] == name and os.path.exists(os.path.join(OUT, "figures", "photos", name)):
            meta.append(old | {"caption": cap}); continue
        m = got.get(f.replace("_", " "))
        if not m:
            print("MISSING", eid, f); continue
        if not FREE.match(m["license"]):
            print("NONFREE", eid, f, m["license"]); continue
        try:
            raw = urlget(m["thumb"])
        except urllib.error.HTTPError as e:
            if e.code != 400:
                raise
            print("  thumb rejected, using original", m["thumb"])
            raw = urlget(m.pop("orig"))
        m.pop("orig", None)
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        time.sleep(6)
        im.thumbnail((WIDTH, WIDTH))
        im.save(os.path.join(OUT, "figures", "photos", name), quality=78, optimize=True, progressive=True)
        meta.append({"id": eid, "img": name, "caption": cap} | m)
        print("ok", name, m["license"], m["author"][:40], flush=True)
        json.dump(meta, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(meta, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(meta), "photos")


if __name__ == "__main__":
    search(" ".join(sys.argv[2:])) if sys.argv[1] == "search" else fetch()

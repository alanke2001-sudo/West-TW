# West-TW

公開資訊研析報告資料庫。首頁 [`index.html`](index.html) 可依關鍵字標籤篩選所有報告與章節，下載整個儲存庫後不需網路即可用瀏覽器開啟。

## 目前收錄

| 日期 | 報告 | 檔案 |
|---|---|---|
| 2026-10-22 | [敵情威脅：中共對臺軍事行動與航空威脅研析（簡報）](reports/2026-10-enemy-briefing/index.html)（七章、50 頁、14 張概念圖） | [PowerPoint](reports/2026-10-enemy-briefing/敵情威脅簡報.pptx) · [PDF](reports/2026-10-enemy-briefing/敵情威脅簡報.pdf) · [概念圖](reports/2026-10-enemy-briefing/figures/) |
| 2026-10-22 | [解放軍無人系統與直升機威脅資料庫](reports/2026-10-pla-unmanned/index.html)（54 筆條目、3 張圖解、23 張裝備照片、51 筆出處，可篩選） | [Word](reports/2026-10-pla-unmanned/) · [CSV](reports/2026-10-pla-unmanned/entries.csv) · [JSON](reports/2026-10-pla-unmanned/entries.json) · [圖解](reports/2026-10-pla-unmanned/figures/) · [裝備照片](reports/2026-10-pla-unmanned/figures/photos/) |
| 2026-10-20 | [解放軍對台軍事行動態勢研析](reports/2026-10-pla-taiwan/index.html)（六章、13 張圖解、42 筆出處） | [Word](reports/2026-10-pla-taiwan/) · [圖解](reports/2026-10-pla-taiwan/figures/) |

## 結構

```
index.html                 標籤資料庫首頁（讀取 data/catalog.js）
data/catalog.json          資料庫內容：標籤分組、每份報告與各章節的摘要和標籤
data/catalog.js            由 tools/build_catalog.py 產生，勿手動修改
tools/build_catalog.py     檢查 catalog.json 並產生 catalog.js
reports/<YYYY-MM-主題>/     每份報告一個資料夾
  index.html               離線網頁版（單一檔案，含內嵌圖解）
  *.docx                   Word 版
  figures/                 圖解 PNG
  src/                     產生該報告的程式（選用）
```

## 新增報告

1. 建立 `reports/<YYYY-MM-主題>/`，放入離線網頁版 `index.html`、Word 檔與 `figures/`。網頁內各章標題需有 `id`，頁首加上 `<a href="../../index.html">← 返回 West-TW 報告資料庫</a>`。
2. 在 `data/catalog.json` 的 `reports` 加入一筆：`id`、`title`、`date`、`path`、`summary`、`files`、報告層級 `tags`，以及每章的 `sections`（`title`、`anchor`、`summary`、`tags`）。
3. 標籤只用 `tag_groups` 既有的詞（目前 4 組 23 個），讓不同報告能互相串連，首頁也不會被標籤淹沒。細項（裝備型號、城市、資料來源）留在報告內文，不另立標籤；確實需要新主題時才加到最適合的分組，總數維持在約 25 個以內。
4. 執行 `python3 tools/build_catalog.py`。它會檢查檔案與章節錨點是否存在、標籤是否在分組內，並重新產生 `data/catalog.js`。
5. 更新上方「目前收錄」表格，提交並開合併請求。

## 說明

各報告僅彙整公開資訊，標示為「推估」或「本報告推算」者不代表已知作戰計畫；地圖上的區塊與航線為示意位置。部分外文來源係經新聞或評論轉述，正式引用前建議查閱原始報告。

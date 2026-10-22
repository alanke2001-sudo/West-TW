# West-TW

## 解放軍對台軍事行動態勢研析

依台灣國防部、美國國防部、CSIS、CMSI、RAND 等公開資訊與新聞報導，彙整解放軍對台軍事行動的公開分析，共六章並附 13 張圖解：

1. 準備工作
2. 重大時間節點
3. 封鎖控制作為
4. 航渡規劃
5. 可能運用兵力
6. 登陸後縱深作戰可能行動

資料截止：2026-10-20。各段重點標註「事實／官方評估／推估／本報告推算」，並附 42 筆出處。

### 檔案

| 檔案 | 說明 |
|---|---|
| [`index.html`](index.html) | 離線網頁版，單一檔案，下載後用瀏覽器開啟即可，不需網路 |
| [`report/解放軍對台軍事行動態勢研析.docx`](report/) | Word 版 |
| [`report/figures/`](report/figures/) | 圖 01–13 圖解（PNG） |
| [`src/`](src/) | 產生網頁、圖解與 Word 檔的原始程式 |

### 重新產生

```bash
cd src
python3 figs.py                                # template.html → pla-taiwan-report.html（內嵌 SVG 圖解）
mkdir -p png && node shot.js pla-taiwan-report.html   # 以 Playwright 擷取各圖 PNG
python3 todocx.py                              # 產生 Word 檔（需 python-docx）
```

### 說明

本報告僅彙整公開資訊，標示為「推估」或「本報告推算」者不代表已知作戰計畫；地圖上的演習區塊與航線為示意位置。部分外文來源係經新聞或評論轉述，正式引用前建議查閱原始報告。

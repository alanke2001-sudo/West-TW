// 將網頁中的圖解存成 figures/圖NN.png，並另存整頁截圖供檢查
// 用法（於報告資料夾）：node src/shot.js [整頁截圖輸出資料夾]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 2 });
  await p.goto('file://' + process.cwd() + '/index.html');
  for (const f of await p.$$('figure[id^=fig]')) {
    const id = await f.getAttribute('id');
    await f.screenshot({ path: 'figures/圖' + id.slice(3) + '.png' });
  }
  const out = process.argv[2];
  if (out) {
    await p.screenshot({ path: out + '/full.png', fullPage: true });
    const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    await m.goto('file://' + process.cwd() + '/index.html#c4');
    await m.screenshot({ path: out + '/mobile.png' });
    const sw = await m.evaluate(() => document.documentElement.scrollWidth);
    console.log('mobile scrollWidth', sw);
    await m.fill('#q', '雷射'); console.log(await m.textContent('#cnt'));
  }
  await b.close();
})();

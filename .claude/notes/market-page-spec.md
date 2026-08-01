# 市場頁製作規格（Property Check）

這份是「新增一個市場」的完整規格，從泰國（`/th/report` + `/th/macro`）那一輪
提煉出來。要做杜拜、越南、菲律賓或任何新市場，照這份走。

搭配讀：`.claude/notes/echarts-spec.md`（圖表色彩與模式）、repo 根目錄 `CLAUDE.md`
（站點結構與 navbar）。

---

## 1 · 交付物

每個市場兩頁，互相引用：

| 頁面 | 路徑 | 結構 |
|---|---|---|
| 城市住宅市場報告 | `/{cc}/report.html` | 七部 · 25–30 張圖 |
| 國家總經 × 房產 | `/{cc}/macro.html` | 四部＋結論篇 · 13–15 張圖 |

參考範本：`th/report.html`、`th/macro.html`。**直接複製結構再換內容，不要從零寫。**

### report 七部
1. 市場現況（存量、利差、長期房價、跨市場定位）
2. 供給端形成機制（推案 vs 吸納、完工、二手供給）
3. 需求與可負擔性（過戶量、授信、家庭債務、房價所得比）
4. 分層市場（單價結構、關鍵價位帶、地價、外資准入、簽證）
5. 外資需求與催化因素（外資過戶、催化時間表）
6. 情境與展望（循環／結構拆解、三條路徑）
7. 十年帳（人口、所得、三個數字收斂）
＋ 配置建議 ＋ 追蹤指標 ＋ 可證偽條件 ＋ 可信度分層 ＋ 附錄比較表

### macro 四部
1. 週期篇（貨幣週期 × 房價、實質利率、實體經濟）
2. 經濟結構篇（所得天花板、人口、產業支柱、勞動結構、債務、匯率、財政、人力資本、正在運作的部分、自我強化迴圈）
3. 政治篇（權力架構、歷次事件、現任政府的政策取向）
4. 總合模型（一條方程式、交互作用、輸出表、可證偽條件）
＋ 結論篇（區位、產品、時點）＋ 順風／風險 ＋ 追蹤指標 ＋ 可信度分層

---

## 2 · 論點結構（最重要，不可省）

這是泰國那輪最後補上、效果最大的部分。

1. **論點總覽**：report 頁在總結（lede）之後、第一部之前，放「本報告的三個核心論點」。
   每條含四要素：**主張 → 關鍵證據 → 此論點錯誤的條件 → 對應章節指引**。
   用 `.thesis` 樣式（見 `th/report.html`）。
2. **可證偽條件**：兩頁都要，向上／向下各三到四項，每項標明推翻哪一條論點，
   且必須是**可在公開序列中觀察**的條件。放在結論之前，不是事後補述。
3. **標題一律是結論句，不是描述句**。
   - ✗「單價結構：每平方公尺價格帶」
   - ✓「總價越低，成交越依賴已失能的授信機制」
   讀者只讀目錄就要能串起整套論述。
4. **可信度分層**：兩頁末尾放「哪些數字撐得住」三層卡片：
   第一層原始統計（可據以決策）／第二層官方數字但二手轉述（方向可信、精確值近似）／
   第三層推導估計（圖上已標，不得當實績引用）。

---

## 3 · 資料規格

### 原則
- **長序列優先。** 2–3 個點的圖沒有說服力，能拿到 20–40 年就拿。
- **去找原始統計，不要停在新聞轉述。** 新聞常把「預測值」寫成「實際值」
  （泰國那輪就抓到 REIC 過戶量 322,500 是預測、實際是 316,000）。
- 回推值（依公布年增率反推）一律在圖上標 `*` 或「推導」，並在圖說寫明。
- 兩個來源打架時**兩個都列**，並解釋口徑差異——這本身就是有價值的段落
  （泰國：AREA 210,112 vs SCB EIC 213,000 vs Knight Frank 350,000）。

### FRED 取數技巧（關鍵，務必用）
WebFetch 抓 FRED 會 403。**改用瀏覽器同源 fetch**：

1. `navigate` 到 `https://fred.stlouisfed.org/series/{任一序列}`
2. 用 `javascript_tool` 在頁面內執行：
```js
const r = await fetch('/graph/fredgraph.csv?id=SERIES_ID', {credentials:'same-origin'});
const t = await r.text();   // CSV：observation_date,VALUE
```
3. 先用候選 ID 陣列批次測試哪些存在（不存在回 HTTP 404），再逐一取全序列。

泰國那輪取到的（換國家時把國碼替換再試）：
| 序列 | ID | 範圍 |
|---|---|---|
| BIS 城市住宅價格（名目） | `QTHN628BIS` | 1991Q1– 季頻 |
| BIS 城市住宅價格（實質） | `QTHR628BIS` | 1991Q1– 季頻 |
| BIS 家庭信用佔 GDP | `QTHHAM770A` | 1991Q4– 季頻 |
| BIS 民間非金融部門信用佔 GDP | `QTHPAM770A` | 1970Q4– |
| 匯率（聯準會 H.10） | `EXTHUS` | 1981– 月頻 |
| 世界銀行實質人均 GDP | `NYGDPPCAPKDTHA` | 1960– 年頻 |
| 通膨率 | `FPCPITOTLZGTHA` | 1960– 年頻 |

**BIS 房價的實質序列是全頁最有力的一張圖**：名目看起來漂亮，實質往往顯示
長期橫盤。泰國：實質指數 1993 年見頂，2015 年才收復，來回 22 年。

### 各國央行／統計局：先試「SPA 的資料端點」再放棄

FRED 只是起點。多數國家的長序列與城市級資料只在本國央行手上，而那些站
通常是 SPA。**SPA 的畫面抓不到，不代表它的資料端點抓不到**——前端要
拿資料一定得打某個 API，而那個 API 往往比搜尋／瀏覽端點寬鬆。

作法：瀏覽器開到該網域任一頁 → DevTools 或攔截 `fetch`／`XHR` 看前端
自己打哪個端點、送什麼 body → 用同源 fetch 重放，改參數即可批次取數。

**已驗證可用的例子——土耳其央行 EVDS3**（2026-08 取得，無需 API key；
只有搜尋／瀏覽端點要 `key` header，資料端點不要）：

```js
// 在 evds3.tcmb.gov.tr 任一頁執行
await fetch('/igmevdsms-dis/fe', {method:'POST', credentials:'same-origin',
  headers:{'Content-Type':'application/json'},
  body: JSON.stringify({type:'json', series:'TP.KFE.TR-TP.KFE.TR10',
    aggregationTypes:'avg-avg', formulas:'0-0',
    startDate:'01-01-2010', endDate:'01-08-2026',
    frequency:'5',            // 4=季 5=月
    decimalSeperator:'.', decimal:'2', dateFormat:'0',
    lang:'tr', yon:'0', sira:'0', ozelFormuller:[],
    groupSeperator:false, isRaporSayfasi:false})
}).then(r=>r.json());
```
序列以 `-` 串接，回傳的鍵改用 `_`。這一招解鎖了 TCMB 房價指數（含
**伊斯坦堡等 NUTS-2 分項**，2010-01 起月頻）、新租租金指數、單位價格與
單位租金（可直接算實質毛收益率）、政策與房貸利率、CPI／PPI。

**反例（已知打不開）**：杜拜土地局 `gateway.dubailand.gov.ae/open-data/*`
回 `INVALID_REQUEST_PARAMETERS`，三次後放棄，成交量序列因此留白。

### 重前端 SPA 抓不到就停手
REIC 官網（`reic.or.th`）是 SPA，統計頁內容擷取不出來。試兩三次就放棄，
在頁上標明資料區間，不要硬湊。**不要在這種站上耗超過幾輪。**

---

## 4 · 中文語域（研究報告，非財經專欄）

泰國那輪因為寫成專欄語感被整批打掉重寫，別再犯。

**規範**
- 人稱：**不用「你」**。主體為投資人／買方／持有人；作者判斷用「我們認為」「我們預估」。
- 句式：結論前置、短句、主詞明確。拆掉英文關係子句直譯造成的長前置修飾。
- 術語：去化、吸納、承作、貸放、授信、曝險、量能、劣化、傳導、邊際、
  結構性、下行風險、折價、溢價、成交結構、能見度。
- **禁止**：口語（說白了、翻成白話、其實、而已）、比喻抒情（塞車、擠在同一個
  出口、排好日期的違約通知、引擎、貨架）、反問句、感嘆句、自我標註。
- 破折號 `——` **只用於標題分隔**，正文改用冒號、逗號或句號。
- 全形標點；commit 前跑檢查：`[一-鿿][,.;:!?]` 與 `[,;:][一-鿿]` 應為 0。

**對照**
> ✗ 這道篩子解釋的事情，比任何一份供給統計都多。
> ✓ 我們認為此一授信篩選機制對本市場的解釋力，高於任何單一供給指標。

> ✗ 掉了九個百分點，看起來像在復原。但這不是還款還出來的。
> ✓ 九個百分點的降幅表面上構成去槓桿，惟其成因並非償還。

英文版走機構研究報告的英文，不是中文直譯。

---

## 5 · 技術規格

- 雙語：每段文字都要 `<span class="lang-en">…</span><span class="lang-zh" style="display:none">…</span>`。
  中英 span 數量必須相等（用腳本驗）。
- Navbar：只放兩行，**不要硬寫**：
  ```html
  <div id="nav-root"></div>
  <script src="/js/nav.js"></script>
  ```
  新市場要在 `js/nav.js` 的 `MARKETS` 陣列加一筆（含 `prefixes` 與 `links`），
  首頁 `index.html` 加一張市場卡。
- 圖表：沿用 `th/report.html` 底部的 chart engine（色彩變數 `C`、`mk()`、`allCharts`、
  `setLang()` 重建、resize handler）。**每張圖都要進 `allCharts`。**
- 語言鈕由 `nav.js` 綁定並呼叫頁面的 `window.setLang`；頁面不需另外綁
  （`nav.js` 用 `stopImmediatePropagation` 防止 setLang 跑兩次把圖表重建兩遍）。
- 標題：`頁名 | {國家} · Property Check`。

**驗證腳本（每次改完都跑）**
```bash
node -e "
const fs=require('fs');
for(const f of ['xx/report.html','xx/macro.html']){
  const s=fs.readFileSync(f,'utf8');
  const m=s.match(/<script>([\s\S]*)<\/script>\s*<\/body>/);
  let js='OK'; try{ new Function(m[1]); }catch(e){ js='ERR '+e.message; }
  const b=s.replace(/<script[\s\S]*?<\/script>/g,'').replace(/<style[\s\S]*?<\/style>/g,'');
  const bad=(b.match(/[一-鿿][,.;:!?]/g)||[]).concat(b.match(/[,;:][一-鿿]/g)||[]);
  console.log(f,'JS:',js,'punct:',bad.length,'pairs:',
    (s.match(/class=\"lang-en\"/g)||[]).length,(s.match(/class=\"lang-zh\"/g)||[]).length);
}"
```
再用瀏覽器實測：中英各切一次、確認 `allCharts.length` 等於預期、
無空白 canvas 容器、`document.documentElement.scrollWidth <= innerWidth`。
窄螢幕用 iframe 量（直接 resize 視窗在此環境不可靠）：
`380 / 760 / 1200px` 皆不得水平溢出。

---

## 6 · 部署

repo 可能有其他 session 或未提交的工作，**一律指名檔案**：

```bash
git add {新檔案}
git commit --only {明確檔案清單} -m "..."
# push 用隔離 worktree，避免踩到別人的暫存區
SHA=$(git rev-parse HEAD)
WT=$(mktemp -d)/wt
git worktree add -q "$WT" origin/main
git -C "$WT" cherry-pick "$SHA"
git -C "$WT" push --no-verify origin HEAD:main
git worktree remove --force "$WT"; git worktree prune
git fetch origin main -q && git reset --soft origin/main
```

**絕對不要用 `git reset --hard`**——我在泰國那輪用了一次（`--hard origin/main --`
沒接路徑），把別人未提交的 `.gitignore` 修改清掉且無法還原。收尾只用 `--soft`
或指名路徑的 `git checkout --`。

review 過就直接 commit + push，不用再問。

---

## 7 · 泰國那輪的未完成項（新市場別重蹈）

- 交易量與庫存的長序列沒拿到（REIC 是 SPA），仍只有 2021–2026。
- 所得長序列（國家統計局家庭收支調查）沒拿到。
- report 第四部塞了七個主題（單價、關鍵價位帶、地價、國籍條款、外資准入、
  簽證七張卡、區域市場），是全頁論述最鬆的地方，**新市場一開始就拆成兩部**。

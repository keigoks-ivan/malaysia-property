# CLAUDE.md — Property Check 開發規範
# 讀這個檔案後不需要再問結構問題，直接執行任務

## ⚠️ 關鍵禁止事項
- **絕對不能執行 build.py** — 那是舊多市場站的產生器，會覆蓋所有手工 HTML
- **不能直接編輯 templates/ 或 market_data/** — 舊站遺留，僅供參考
- **不能編輯 archive/** — 舊多市場站（tw/au/jp/nz/uk/us/ca/kr/th/vn…）已凍結封存，不更新、不修復
- **_redirects 千萬不能加 `/*` catch-all** — Cloudflare Pages 先評估 _redirects 再供靜態檔，會整站迴圈；舊網址一律由 404.html 客戶端導回 `/`
- **不要在頁面裡硬寫 navbar** — 一律用 `/js/nav.js`（見下方）
- 所有修改直接編輯 HTML 檔案

## 部署
- Repo: github.com/keigoks-ivan/malaysia-property
- 網站：myproperty.investmquest.com（Cloudflare Pages 自動 deploy）
- Push 到 main 後約 1-2 分鐘生效
- robots.txt 全站 Disallow，站點刻意不被搜尋引擎收錄 → 改標題／改品牌沒有 SEO 風險

## 現行站點結構（2026-07 改版：市場優先，品牌＝Property Check）
```
/                    ← 首頁：市場入口 hub（🇲🇾 馬來西亞 / 🇹🇭 泰國 卡片＋最新）
/kl-check            ← 馬來西亞：KL 建案評分卡總表
/my/report.html      ← 馬來西亞：市場報告（餘屋/供需，七部）
/my/macro.html       ← 馬來西亞：總經 × 房產（週期/結構/政治/總合模型）
/my/airbnb.html      ← 馬來西亞：短租 / STRA
/my/reit-vs-direct.html ← 馬來西亞：REITs vs 實體房產互動計算器
/my/clock.html       ← 馬來西亞：房產羅盤 Compass
/th/report.html      ← 泰國：曼谷住宅市場報告（七部）
/th/macro.html       ← 泰國：總經 × 房產（四部＋答案篇）
/th/clock.html       ← 泰國：房產羅盤 Compass
/ae/report.html      ← 阿聯：杜拜住宅市場報告（七部）
/ae/macro.html       ← 阿聯：總經 × 房產（四部＋結論篇）
/tr/report.html      ← 土耳其：伊斯坦堡住宅市場報告（七部、28 圖）
/tr/macro.html       ← 土耳其：總經 × 房產（四部＋結論篇、15 圖）
/ph/report.html      ← 菲律賓：馬尼拉住宅市場報告（七部、22 圖；NCR 全域口徑，無分區）
/ph/macro.html       ← 菲律賓：總經 × 房產（四部＋結論篇、14 圖）
/gr/report.html      ← 希臘：雅典住宅市場報告（七部、28 圖）
/gr/macro.html       ← 希臘：總經 × 房產（四部＋結論篇、15 圖）
/global/visa.html    ← 跨市場：買房換居留（44 套現行制度／24 個確認無途徑／6 套已關閉；資料 data/visa-property.json 內嵌於頁面）
/kl/SC_*.html        ← 建案評分卡（en/zh 成對；用 kl-property-scorecard skill 產生）
/kl/viewing.html     ← 看房檢核工具
/css/style.css       ← 基底樣式；/css/kl-theme.css ← 主題（navy-gold cream）
/js/nav.js           ← 全站共用導覽列（唯一來源）
/data/*.json         ← vetted 數據（markets-summary、prices、demand、macro、supply）
/_redirects          ← 只放「目標仍存在」的舊網址 301；見上方禁止事項
/404.html            ← 未匹配網址 → 客戶端導回 /
/archive/            ← 舊多市場站凍結封存（勿動）
```

## Navbar — 共用 `/js/nav.js`
兩層結構：第一列＝品牌＋市場切換（🇲🇾 馬來西亞 / 🇹🇭 泰國）＋EN/中文；第二列＝當前市場的子頁。

頁面只需要這兩行，放在 `<body>` 最上方、且在該頁自己的 `<script>` 之前：
```html
<div id="nav-root"></div>
<script src="/js/nav.js"></script>
```

- **新增市場／新增子頁＝只改 `nav.js` 裡的 `MARKETS` 陣列**，不要動任何 HTML。
- 語言：nav 用全站的 `.lang-en` / `.lang-zh` class，所以 kl-check 的 `body.zh` CSS 機制與其他頁的 `setLang()` inline 切換都能相容。
- nav 的語言鈕會呼叫該頁的 `window.setLang()`（沒有的話用內建 fallback），並以 `stopImmediatePropagation()` 擋掉頁面自己綁的 `.lang-btn` handler，避免 setLang 跑兩次把圖表重建兩遍。
- 評分卡 `/kl/SC_*.html` 與 `viewing.html` **刻意不掛共用 navbar**：它們是單篇文件，保留原本精簡的動作列（品牌 → `/`、← All Scores、Viewing、中文對照頁）。

## 現行利率
- Malaysia OPR: **2.75%**（BNM 2026 年 7 月會議維持；全站徽章一律用此值）

## ECharts 設計系統
寫圖表 / 改 chart 程式碼時 Read `.claude/notes/echarts-spec.md`。內含：色彩變數 `C`、`baseText/baseGrid/baseTooltip/baseLegend/mkAxis`、格式化函數、必須遵守的模式（allCharts / setLang / resize handler）、Chart ID 命名、標準規格。

## 雙語系統
所有文字必須提供中英文版本：
```html
<span class="lang-en">English text</span>
<span class="lang-zh" style="display:none">中文文字</span>
```
注意：kl-check.html 例外——它用頁級 CSS 切換（`.lang-zh{display:none}` + `body.zh`），span 不帶 inline style。修改該頁時跟隨其現有寫法。

中文內容標點一律全形（，。：；「」），數字/英文照原樣；commit 前跑檢查：
`[一-鿿][,.;:!?]` 與 `[,;:][一-鿿]`（去 script/style 後）應為 0。

## 內容規範
- my/macro 與 my/report 是一對「why + what」：跨頁引用數字必須同步（OPR、家庭債務 84.8%、中位收入 RM7,017、餘屋數、MHPI）
- M-REIT 配息稅一律用 YA2026 新制（10% 扣繳已落日：居民累進／非居民個人 30%）；外國人印花稅 8%（2026/1 起）
- 深度頁行文是「機制鏈＋數據＋對房市的意思」的因果分析，不是 stat dashboard

## Git 工作流程
```bash
# Mac Mini (主要工作機)
git add -A
git commit -m "feat/fix/update: 描述"
git push origin main

# MacBook Pro (第二台)
git pull --rebase origin main  # 先同步再工作
git push origin main
```

## 常用 commit 前綴
- `feat:` 新功能或新頁面
- `fix:` 修復問題
- `update:` 更新數據或文字
- `security:` 安全性相關
- `refactor:` 重構（不改功能）

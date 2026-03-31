# CLAUDE.md — Property Monitor 開發規範
# 讀這個檔案後不需要再問結構問題，直接執行任務

## ⚠️ 關鍵禁止事項
- **絕對不能執行 build.py** — 會覆蓋所有手工 HTML，回復 commit: 39543e8
- **不能直接編輯 templates/ 或 market_data/** — 僅供參考
- 所有修改直接編輯 HTML 檔案

## 部署
- Repo: github.com/keigoks-ivan/malaysia-property
- 網站: myproperty.investmquest.com（Cloudflare Pages 自動 deploy）
- Push 到 main 後約 1-2 分鐘生效

## 目錄結構
```
/                    ← Malaysia (MY) 頁面
/tw/                 ← Taiwan
/au/                 ← Australia
/jp/                 ← Japan
/nz/                 ← New Zealand
/uk/                 ← United Kingdom
/docs/dd/            ← 深度研究報告（獨立 HTML）
/css/style.css       ← 主樣式（所有頁面共用）
/tw/tw.css           ← 補丁 CSS（所有子目錄頁面都引用）
/_headers            ← Cloudflare Pages security headers
```

## 每個市場的標準頁面
- index.html（市場總覽 Dashboard）
- supply.html（供給分析）
- demand.html（需求分析）
- valuation.html（估值監測）
- risk.html（風險監測）
- report.html（深度報告）
- [city].html（城市深度分析，例如 sydney.html、taipei.html）

## ECharts 設計系統

### 色彩變數（所有頁面通用）
```js
var C = {
  navy:   '#1e3a5f',
  green:  '#16a34a',
  orange: '#d97706',
  red:    '#dc2626',
  blue:   '#2563eb',
  muted:  '#5a7a9a',
  grid:   '#e8f0f9',
  text:   '#1e3a5f'
};
```

### 基礎設定（所有頁面通用）
```js
var baseText    = {color:C.muted, fontFamily:'Inter, sans-serif', fontSize:11};
var baseGrid    = {left:50, right:20, top:40, bottom:30, containLabel:true};
var baseTooltip = {trigger:'axis', backgroundColor:'#fff', borderColor:'#ccd9e8', borderWidth:1, textStyle:{color:C.navy, fontSize:11, fontFamily:'Inter'}};
var baseLegend  = {top:8, textStyle:baseText, icon:'circle', itemWidth:8, itemHeight:8};
function mkAxis(o){return Object.assign({axisLine:{lineStyle:{color:C.grid}},axisTick:{show:false},axisLabel:baseText,splitLine:{lineStyle:{color:C.grid}}},o||{});}
```

### 格式化函數
```js
// Australia 頁面
function fmtAUD(v){if(v>=1000000)return 'A$'+(v/1000000).toFixed(2)+'M';if(v>=1000)return 'A$'+(v/1000).toFixed(0)+'K';return 'A$'+v;}
function fmtAUDShort(v){if(v>=1000000)return(v/1000000).toFixed(1)+'M';if(v>=1000)return(v/1000).toFixed(0)+'K';return v;}

// Taiwan 頁面
function fmtPrice(v,lang){var a=v*10000;if(lang==='zh')return 'NT$'+v+'萬';if(a>=1000000)return 'NT$'+(a/1000000).toFixed(2)+'M';return 'NT$'+Math.round(a/1000)+'K';}
function fmtPriceShort(v,lang){var a=v*10000;if(lang==='zh')return v+'萬';if(a>=1000000)return(a/1000000).toFixed(1)+'M';return Math.round(a/1000)+'K';}

// Malaysia 頁面（一般數字）
function fmtNum(v){if(v>=1000000)return(v/1000000).toFixed(1)+'M';if(v>=1000)return(v/1000).toFixed(0)+'K';return v;}
```

### 必須遵守的模式
```js
// 1. 所有圖表必須加入 allCharts
var allCharts = [];
function initCharts(lang) {
  allCharts.length = 0;
  var c = echarts.init(document.getElementById('chartXxx'));
  allCharts.push(c);
  c.setOption({...});
}

// 2. 語言切換（setLang）— 切換時 dispose 所有圖表再重新初始化
function setLang(lang) {
  document.querySelectorAll('.lang-en').forEach(function(e){e.style.display=lang==='en'?'':'none';});
  document.querySelectorAll('.lang-zh').forEach(function(e){e.style.display=lang==='zh'?'':'none';});
  document.querySelectorAll('.lang-btn').forEach(function(b){b.classList.toggle('active',b.dataset.lang===lang);});
  localStorage.setItem('lang',lang);
  if(typeof allCharts!=='undefined'){allCharts.forEach(function(c){if(c)c.dispose();});allCharts=[];}
  initCharts(lang);
}

// 3. resize handler
window.addEventListener('resize',function(){allCharts.forEach(function(c){if(c)c.resize();});});
window.addEventListener('load',function(){setLang(localStorage.getItem('lang')||'en');});
```

### Chart ID 命名規則
- Malaysia 根目錄頁面：`chartXxx`（如 `chartOhSeverity`）
- KL 頁面：`chart-kl-xxx` 或 `chartKLXxx`
- AU 頁面：`chartXxx`（如 `chartSydneyPrice`）
- AU 城市深度：`chartAUCity` 前綴（如 `chartBNEPrice`、`chartGCCliff`）
- TW 頁面：`chartTPEXxx`（如 `chartTPELTV`）
- Report 頁面：`rChartXxx`（如 `rChartAuPrice10y`）

### 圖表標準規格
- 高度：`220px`（預設），特殊圖表標注例外
- 2x2 grid 用 `.chart-grid.two-col` 或 `.report-chart-grid`
- axis label color：`C.muted`（#5a7a9a）
- bar border radius（水平）：`[0,3,3,0]`；垂直：`[3,3,0,0]`
- bar maxWidth：`35`（預設）

## 雙語系統
所有文字必須提供中英文版本：
```html
<span class="lang-en">English text</span>
<span class="lang-zh" style="display:none">中文文字</span>
```

## Navbar 結構
每個頁面的 navbar 包含：
1. Logo → 連回該市場 index.html
2. Market selector dropdown → 各市場的 report.html（不是 index.html）
3. 市場內頁面導覽 nav links
4. 語言切換按鈕（EN / 中文）
5. 利率 badge（`opr-badge`）
6. 漢堡選單（mobile）

## 各市場現行利率 badge
- Malaysia：`OPR: 3.00%`
- Taiwan：`CBC: 2.00%`
- Australia：`RBA: 4.10% ▲`
- Japan：`BOJ: 0.50%`
- New Zealand：`OCR: 4.25%`
- UK：`BOE: 4.75%`

## KPI Card 顏色類別
```html
<div class="kpi-card blue|green|orange|red">
  <div class="kpi-label">...</div>
  <div class="kpi-value">...</div>
  <span class="kpi-badge badge-blue|badge-green|badge-orange|badge-red">...</span>
</div>
```

## 版面元素
- `section-label`：大寫 section 標題
- `insight-box`：重點洞察文字框（深藍左邊框）
- `summary-card`：總結卡片（帶顏色左邊框）
- `micro-card`：三欄小型資訊卡
- `chart-card`：圖表容器
- `source-footer`：資料來源頁腳
- `page-header`：頁面標題區（含 updated 日期）

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

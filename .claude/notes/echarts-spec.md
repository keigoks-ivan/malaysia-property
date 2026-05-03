# ECharts 設計系統 — Property Monitor

寫圖表 / 改 chart 程式碼時 Read 這份。所有市場頁面（MY / TW / AU / JP / NZ / UK）共用此 spec。

## 色彩變數（所有頁面通用）
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

## 基礎設定（所有頁面通用）
```js
var baseText    = {color:C.muted, fontFamily:'Inter, sans-serif', fontSize:11};
var baseGrid    = {left:50, right:20, top:40, bottom:30, containLabel:true};
var baseTooltip = {trigger:'axis', backgroundColor:'#fff', borderColor:'#ccd9e8', borderWidth:1, textStyle:{color:C.navy, fontSize:11, fontFamily:'Inter'}};
var baseLegend  = {top:8, textStyle:baseText, icon:'circle', itemWidth:8, itemHeight:8};
function mkAxis(o){return Object.assign({axisLine:{lineStyle:{color:C.grid}},axisTick:{show:false},axisLabel:baseText,splitLine:{lineStyle:{color:C.grid}}},o||{});}
```

## 格式化函數
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

## 必須遵守的模式
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

## Chart ID 命名規則
- Malaysia 根目錄頁面：`chartXxx`（如 `chartOhSeverity`）
- KL 頁面：`chart-kl-xxx` 或 `chartKLXxx`
- AU 頁面：`chartXxx`（如 `chartSydneyPrice`）
- AU 城市深度：`chartAUCity` 前綴（如 `chartBNEPrice`、`chartGCCliff`）
- TW 頁面：`chartTPEXxx`（如 `chartTPELTV`）
- Report 頁面：`rChartXxx`（如 `rChartAuPrice10y`）

## 圖表標準規格
- 高度：`220px`（預設），特殊圖表標注例外
- 2x2 grid 用 `.chart-grid.two-col` 或 `.report-chart-grid`
- axis label color：`C.muted`（#5a7a9a）
- bar border radius（水平）：`[0,3,3,0]`；垂直：`[3,3,0,0]`
- bar maxWidth：`35`（預設）

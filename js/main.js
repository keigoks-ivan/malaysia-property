/* ── Chart.js Defaults (S&P Capital IQ light-blue style) ── */
function setChartDefaults() {
  if (typeof Chart === 'undefined') { console.error('Chart.js not loaded'); return; }
  Chart.defaults.color = '#8ba3c0';
  Chart.defaults.borderColor = '#e8f0f9';
  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.font.size = 11;
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.pointStyleWidth = 8;
  Chart.defaults.plugins.legend.labels.padding = 14;
  Chart.defaults.plugins.legend.labels.font = { size: 11 };
  Chart.defaults.elements.line.tension = 0.3;
  Chart.defaults.elements.line.borderWidth = 2;
  Chart.defaults.elements.point.radius = 2;
  Chart.defaults.elements.point.hoverRadius = 5;
  Chart.defaults.elements.bar.borderRadius = 2;
  Chart.defaults.scale.grid = { color: '#e8f0f9' };
  Chart.defaults.maintainAspectRatio = false;
  Chart.defaults.responsive = true;
}

/* ── Chart Registry ── */
const chartRegistry = {};

function createChart(canvasId, config) {
  const el = document.getElementById(canvasId);
  if (!el) { console.warn('Canvas not found: ' + canvasId); return null; }
  // Ensure parent has dimensions
  const parent = el.parentElement;
  if (parent && parent.offsetHeight === 0) {
    parent.style.height = '220px';
    parent.style.position = 'relative';
  }
  // Add barThickness + minBarLength to all bar datasets for reliable rendering
  if (config.data && config.data.datasets) {
    config.data.datasets.forEach(ds => {
      if (config.type === 'bar' || ds.type === 'bar') {
        if (!ds.barThickness) ds.barThickness = 18;
        if (!ds.minBarLength) ds.minBarLength = 4;
      }
    });
  }
  const chart = new Chart(el, config);
  chartRegistry[canvasId] = chart;
  // Force resize + redraw to handle any layout timing issues
  requestAnimationFrame(() => {
    chart.resize();
    chart.update('none');
    setTimeout(() => { chart.resize(); chart.update('none'); }, 100);
    setTimeout(() => { chart.resize(); chart.update('none'); }, 500);
  });
  return chart;
}

/* Resize all visible charts (call after tab switch) */
function resizeVisibleCharts() {
  Object.keys(chartRegistry).forEach(id => {
    const chart = chartRegistry[id];
    if (chart && chart.canvas && chart.canvas.offsetParent !== null) {
      chart.resize();
    }
  });
}

/* ── Chart Colors ── */
const C = {
  navy: '#1e3a5f', green: '#16a34a', orange: '#d97706',
  blue: '#2563eb', red: '#dc2626', muted: '#8ba3c0',
  navy_bg: 'rgba(30,58,95,0.08)', green_bg: 'rgba(22,163,74,0.08)',
  orange_bg: 'rgba(217,119,6,0.08)', blue_bg: 'rgba(37,99,235,0.08)',
};

/* ── Formatters ── */
function fmtNum(n) {
  if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
  if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
  return n.toLocaleString();
}
function fmtRM(n) {
  if (n >= 1e6) return 'RM ' + (n / 1e6).toFixed(1) + 'M';
  if (n >= 1e3) return 'RM ' + (n / 1e3).toFixed(0) + 'K';
  return 'RM ' + n.toLocaleString();
}

/* ── Tab switching ── */
function switchTab(container, tabName) {
  const wrap = document.getElementById(container);
  if (!wrap) return;
  wrap.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  wrap.querySelectorAll('.tab-bar button').forEach(b => b.classList.remove('active'));
  const panel = wrap.querySelector('#tab-' + tabName);
  if (panel) panel.classList.add('active');
  wrap.querySelectorAll('.tab-bar button').forEach(b => {
    if (b.dataset.tab === tabName) b.classList.add('active');
  });
  // Resize charts in newly visible tab after layout reflow
  requestAnimationFrame(() => { requestAnimationFrame(() => { resizeVisibleCharts(); }); });
}

/* ══════════════════════════════════════════════════════════════
   LANGUAGE SYSTEM
   ══════════════════════════════════════════════════════════════ */

/* Chart translation dictionary: { canvasId: { en: [...labels], zh: [...labels] } } */
const chartI18n = {};

function registerChartI18n(canvasId, enLabels, zhLabels, enDatasets, zhDatasets) {
  chartI18n[canvasId] = { enL: enLabels, zhL: zhLabels, enD: enDatasets, zhD: zhDatasets };
}

function setLanguage(lang) {
  localStorage.setItem('lang', lang);
  document.documentElement.lang = lang === 'zh' ? 'zh-Hant' : 'en';

  // Toggle text via data-en / data-zh
  document.querySelectorAll('[data-en][data-zh]').forEach(el => {
    el.textContent = lang === 'zh' ? el.dataset.zh : el.dataset.en;
  });

  // Toggle innerHTML via data-en-html / data-zh-html
  document.querySelectorAll('[data-en-html][data-zh-html]').forEach(el => {
    el.innerHTML = lang === 'zh' ? el.dataset.zhHtml : el.dataset.enHtml;
  });

  // Update lang buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });

  // Update charts
  updateChartLanguage(lang);

  // Page-specific callback
  if (typeof onLanguageChange === 'function') onLanguageChange(lang);
}

function updateChartLanguage(lang) {
  Object.keys(chartI18n).forEach(id => {
    const chart = chartRegistry[id];
    const t = chartI18n[id];
    if (!chart || !t) return;
    if (t.enD && t.zhD) {
      const ds = lang === 'zh' ? t.zhD : t.enD;
      chart.data.datasets.forEach((d, i) => { if (ds[i] !== undefined) d.label = ds[i]; });
    }
    if (t.enL && t.zhL) {
      chart.data.labels = lang === 'zh' ? [...t.zhL] : [...t.enL];
    }
    chart.update();
  });
}

function initLanguage() {
  setLanguage(localStorage.getItem('lang') || 'en');
}

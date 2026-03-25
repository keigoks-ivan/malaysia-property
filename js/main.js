/* ── Colors ── */
const C = {
  navy: '#1e3a5f', green: '#16a34a', orange: '#d97706',
  blue: '#2563eb', red: '#dc2626', muted: '#8ba3c0',
  navy_bg: 'rgba(30,58,95,0.08)', green_bg: 'rgba(22,163,74,0.08)',
  orange_bg: 'rgba(217,119,6,0.08)', blue_bg: 'rgba(37,99,235,0.08)',
};

function fmtNum(n) {
  if (n >= 1e6) return (n/1e6).toFixed(1)+'M';
  if (n >= 1e3) return (n/1e3).toFixed(1)+'K';
  return n.toLocaleString();
}
function fmtRM(n) {
  if (n >= 1e6) return 'RM '+(n/1e6).toFixed(1)+'M';
  if (n >= 1e3) return 'RM '+(n/1e3).toFixed(0)+'K';
  return 'RM '+n.toLocaleString();
}

const chartRegistry = {};
const chartI18n = {};

function setChartDefaults() {
  if (typeof Chart === 'undefined') return;
  Chart.defaults.color = '#8ba3c0';
  Chart.defaults.borderColor = '#e8f0f9';
  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.font.size = 11;
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.pointStyleWidth = 8;
  Chart.defaults.plugins.legend.labels.padding = 14;
  Chart.defaults.elements.line.tension = 0.3;
  Chart.defaults.elements.line.borderWidth = 2;
  Chart.defaults.elements.point.radius = 2;
  Chart.defaults.elements.point.hoverRadius = 5;
  Chart.defaults.elements.bar.borderRadius = 2;
  Chart.defaults.scale.grid = { color: '#e8f0f9' };
}

function createChart(id, config) {
  const el = document.getElementById(id);
  if (!el) return null;
  const parent = el.parentElement;
  if (parent) {
    if (!parent.style.height) parent.style.height = '220px';
    parent.style.position = 'relative';
  }
  config.options = config.options || {};
  config.options.responsive = true;
  config.options.maintainAspectRatio = false;
  const chart = new Chart(el, config);
  chartRegistry[id] = chart;
  return chart;
}

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
  setTimeout(() => {
    Object.keys(chartRegistry).forEach(id => {
      const c = chartRegistry[id];
      if (c && c.canvas && c.canvas.closest('.tab-panel.active')) c.resize();
    });
  }, 50);
}

function resizeVisibleCharts() {
  Object.keys(chartRegistry).forEach(id => {
    const c = chartRegistry[id];
    if (c && c.canvas && c.canvas.offsetParent !== null) c.resize();
  });
}

function registerChartI18n(canvasId, enLabels, zhLabels, enDatasets, zhDatasets) {
  chartI18n[canvasId] = { enL: enLabels, zhL: zhLabels, enD: enDatasets, zhD: zhDatasets };
}

function updateChartLanguage(lang) {
  Object.keys(chartI18n).forEach(id => {
    const chart = chartRegistry[id];
    const i18n = chartI18n[id];
    if (!chart || !i18n) return;
    if (lang === 'zh') {
      if (i18n.zhL) chart.data.labels = i18n.zhL;
      if (i18n.zhD) chart.data.datasets.forEach((ds, i) => { if (i18n.zhD[i]) ds.label = i18n.zhD[i]; });
    } else {
      if (i18n.enL) chart.data.labels = i18n.enL;
      if (i18n.enD) chart.data.datasets.forEach((ds, i) => { if (i18n.enD[i]) ds.label = i18n.enD[i]; });
    }
    chart.update('none');
  });
}

function setLanguage(lang) {
  document.querySelectorAll('[data-en]').forEach(el => {
    el.textContent = lang === 'zh' ? (el.dataset.zh || el.dataset.en) : el.dataset.en;
  });
  document.querySelectorAll('[data-en-html]').forEach(el => {
    el.innerHTML = lang === 'zh' ? (el.dataset.zhHtml || el.dataset.enHtml) : el.dataset.enHtml;
  });
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
  updateChartLanguage(lang);
  localStorage.setItem('lang', lang);
  if (typeof onLanguageChange === 'function') onLanguageChange(lang);
}

function initLanguage() {
  setLanguage(localStorage.getItem('lang') || 'en');
}

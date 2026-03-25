'use strict';

/* Colors */
const C = {
  navy: '#1e3a5f', green: '#16a34a', orange: '#d97706',
  blue: '#2563eb', red: '#dc2626', muted: '#8ba3c0',
  navy_bg: 'rgba(30,58,95,0.08)', green_bg: 'rgba(22,163,74,0.08)',
  orange_bg: 'rgba(217,119,6,0.08)', blue_bg: 'rgba(37,99,235,0.08)',
};

/* Formatters */
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

/* Chart defaults */
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
  Chart.defaults.responsive = true;
  Chart.defaults.maintainAspectRatio = false;
}

/* Tab switching */
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
}

/* Language */
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
  localStorage.setItem('lang', lang);
  if (typeof updateChartLanguage === 'function') updateChartLanguage(lang);
}

document.addEventListener('DOMContentLoaded', () => {
  const lang = localStorage.getItem('lang') || 'en';
  setLanguage(lang);
});

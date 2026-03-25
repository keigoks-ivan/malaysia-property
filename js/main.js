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

/* ── Safe chart creator: checks canvas exists before init ── */
function createChart(canvasId, config) {
  const el = document.getElementById(canvasId);
  if (!el) { console.warn('Canvas not found: ' + canvasId); return null; }
  return new Chart(el, config);
}

/* ── Chart Colors ── */
const C = {
  navy: '#1e3a5f',
  green: '#16a34a',
  orange: '#d97706',
  blue: '#2563eb',
  red: '#dc2626',
  muted: '#8ba3c0',
  navy_bg: 'rgba(30,58,95,0.08)',
  green_bg: 'rgba(22,163,74,0.08)',
  orange_bg: 'rgba(217,119,6,0.08)',
  blue_bg: 'rgba(37,99,235,0.08)',
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

/* ── Tab switching utility ── */
function switchTab(container, tabName) {
  const wrap = document.getElementById(container);
  if (!wrap) return;
  wrap.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  wrap.querySelectorAll('.tab-bar button').forEach(b => b.classList.remove('active'));
  const panel = wrap.querySelector('#tab-' + tabName);
  if (panel) panel.classList.add('active');
  const btns = wrap.querySelectorAll('.tab-bar button');
  btns.forEach(b => { if (b.dataset.tab === tabName) b.classList.add('active'); });
}

/* ── Navbar HTML (shared) ── */
function getNav(activePage) {
  const pages = [
    ['index.html', 'Dashboard'],
    ['supply.html', 'Supply'],
    ['demand.html', 'Demand'],
    ['valuation.html', 'Valuation'],
    ['risk.html', 'Risk'],
    ['kl.html', 'KL'],
  ];
  const links = pages.map(([href, label]) => {
    const cls = href === activePage ? ' class="active"' : '';
    return `<a href="${href}"${cls}>${label}</a>`;
  }).join('');
  return `<header class="navbar">
    <a href="index.html" class="logo">MALAYSIA PROPERTY MONITOR</a>
    <nav>${links}</nav>
    <span class="opr-badge">OPR: 2.75% ▼</span>
  </header>`;
}

/* ── Source Footer HTML ── */
function getSourceFooter() {
  return `<div class="source-footer">
    NAPIC Property Market Report 2024 &middot; NAPIC Q3 2025 Snapshot &middot; JPPH Q3 2025 &middot;
    Global Property Guide Malaysia Q1 2026 &middot; BNM Monetary Policy 2023–2025 &middot;
    DOSM Household Income Survey 2022 &middot; Juwai IQI Global Market Insights 2025 &middot;
    REHDA Property Industry Survey 2H2025 &middot; Bamboo Routes Malaysia 2025 &middot; PropCashflow Malaysia 2026<br>
    <em>Estimates marked * are directional approximations based on public data.
    This site is for informational purposes only and does not constitute investment advice.</em>
  </div>`;
}

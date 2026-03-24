/* ── Data Loading ── */
const DATA_BASE = 'https://raw.githubusercontent.com/keigoks-ivan/malaysia-property/main/data/';

async function loadData() {
  const [supply, demand, prices, macro] = await Promise.all([
    fetch(DATA_BASE + 'supply.json').then(r => r.json()),
    fetch(DATA_BASE + 'demand.json').then(r => r.json()),
    fetch(DATA_BASE + 'prices.json').then(r => r.json()),
    fetch(DATA_BASE + 'macro.json').then(r => r.json()),
  ]);
  return { supply, demand, prices, macro };
}

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

function last(arr) { return arr[arr.length - 1]; }

/* ── Chart.js Defaults ── */
function setChartDefaults() {
  Chart.defaults.color = '#8b91a8';
  Chart.defaults.borderColor = 'rgba(255,255,255,0.06)';
  Chart.defaults.font.family = "'DM Sans', sans-serif";
  Chart.defaults.font.size = 12;
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.pointStyleWidth = 8;
  Chart.defaults.plugins.legend.labels.padding = 16;
  Chart.defaults.elements.line.tension = 0.3;
  Chart.defaults.elements.point.radius = 2;
  Chart.defaults.elements.point.hoverRadius = 5;
}

/* ── Chart Colors ── */
const COLORS = {
  blue1: '#3b82f6',
  blue2: '#60a5fa',
  blue3: '#93c5fd',
  blue4: '#2563eb',
  gold: '#c9a84c',
  green: '#34d399',
  red: '#f87171',
  blue1_bg: 'rgba(59,130,246,0.15)',
  gold_bg: 'rgba(201,168,76,0.15)',
};

/* ── Update Badge ── */
function setUpdated(dateStr) {
  const el = document.getElementById('updated-date');
  if (el) el.textContent = 'Last Updated: ' + dateStr;
}

/* ── Dashboard (index.html) ── */
async function initDashboard() {
  setChartDefaults();
  const { supply, demand, prices, macro } = await loadData();
  setUpdated(macro.updated);

  // KPIs
  document.getElementById('kpi-opr').textContent = last(macro.opr).toFixed(2) + '%';
  document.getElementById('kpi-transactions').textContent = fmtNum(last(demand.transactions_volume));
  document.getElementById('kpi-overhang').textContent = fmtNum(last(supply.overhang));
  document.getElementById('kpi-kl-price').textContent = fmtRM(prices.regions.kl.median_price);

  // Chart 1: Supply vs Demand Trend
  new Chart(document.getElementById('chart-supply-demand'), {
    type: 'line',
    data: {
      labels: demand.quarters,
      datasets: [
        {
          label: 'Transaction Volume',
          data: demand.transactions_volume,
          borderColor: COLORS.blue1,
          backgroundColor: COLORS.blue1_bg,
          fill: true,
        },
        {
          label: 'New Completions',
          data: supply.completed,
          borderColor: COLORS.gold,
          backgroundColor: COLORS.gold_bg,
          fill: true,
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { title: { display: false } },
      scales: {
        y: { ticks: { callback: v => fmtNum(v) } }
      }
    }
  });

  // Chart 2: MHPI Trend
  new Chart(document.getElementById('chart-mhpi'), {
    type: 'line',
    data: {
      labels: prices.quarters,
      datasets: [{
        label: 'MHPI (Base 2010 = 100)',
        data: prices.mhpi,
        borderColor: COLORS.gold,
        backgroundColor: COLORS.gold_bg,
        fill: true,
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: false }
      }
    }
  });
}

/* ── Supply Page ── */
async function initSupply() {
  setChartDefaults();
  const { supply } = await loadData();
  setUpdated(supply.updated);

  // KPIs
  document.getElementById('kpi-construction').textContent = fmtNum(last(supply.under_construction));
  document.getElementById('kpi-completed').textContent = fmtNum(last(supply.completed));
  document.getElementById('kpi-overhang').textContent = fmtNum(last(supply.overhang));

  // Chart 1: Stacked bar by type
  new Chart(document.getElementById('chart-by-type'), {
    type: 'bar',
    data: {
      labels: supply.quarters,
      datasets: [
        { label: 'Condo', data: supply.by_type.condo, backgroundColor: COLORS.blue1 },
        { label: 'Landed', data: supply.by_type.landed, backgroundColor: COLORS.blue2 },
        { label: 'Commercial', data: supply.by_type.commercial, backgroundColor: COLORS.gold },
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { stacked: true },
        y: { stacked: true, ticks: { callback: v => fmtNum(v) } }
      }
    }
  });

  // Chart 2: By state (horizontal bar)
  const states = Object.keys(supply.by_state);
  const stateLabels = { selangor: 'Selangor', kl: 'Kuala Lumpur', penang: 'Penang', johor: 'Johor', sabah: 'Sabah' };
  new Chart(document.getElementById('chart-by-state'), {
    type: 'bar',
    data: {
      labels: states.map(s => stateLabels[s] || s),
      datasets: [{
        label: 'Overhang Units',
        data: states.map(s => supply.by_state[s]),
        backgroundColor: [COLORS.blue1, COLORS.gold, COLORS.blue2, COLORS.blue3, COLORS.green],
        borderRadius: 4,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      scales: {
        x: { ticks: { callback: v => fmtNum(v) } }
      }
    }
  });

  // Chart 3: Under construction trend
  new Chart(document.getElementById('chart-construction'), {
    type: 'line',
    data: {
      labels: supply.quarters,
      datasets: [{
        label: 'Under Construction',
        data: supply.under_construction,
        borderColor: COLORS.blue1,
        backgroundColor: COLORS.blue1_bg,
        fill: true,
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { ticks: { callback: v => fmtNum(v) } }
      }
    }
  });
}

/* ── Demand Page ── */
async function initDemand() {
  setChartDefaults();
  const { demand, macro } = await loadData();
  setUpdated(demand.updated);

  // KPIs
  document.getElementById('kpi-transactions').textContent = fmtNum(last(demand.transactions_volume));
  document.getElementById('kpi-loan-rate').textContent = last(demand.loan_approval_rate).toFixed(1) + '%';
  document.getElementById('kpi-pti').textContent = last(macro.price_to_income_ratio.values).toFixed(1) + 'x';

  // Chart 1: Transaction volume trend
  new Chart(document.getElementById('chart-transactions'), {
    type: 'bar',
    data: {
      labels: demand.quarters,
      datasets: [{
        label: 'Transaction Volume',
        data: demand.transactions_volume,
        backgroundColor: COLORS.blue1,
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { ticks: { callback: v => fmtNum(v) } }
      }
    }
  });

  // Chart 2: Loan approval vs OPR (dual axis)
  new Chart(document.getElementById('chart-loan-opr'), {
    type: 'line',
    data: {
      labels: demand.quarters,
      datasets: [
        {
          label: 'Loan Approval Rate (%)',
          data: demand.loan_approval_rate,
          borderColor: COLORS.blue1,
          backgroundColor: COLORS.blue1_bg,
          fill: true,
          yAxisID: 'y',
        },
        {
          label: 'OPR (%)',
          data: macro.opr,
          borderColor: COLORS.gold,
          borderWidth: 2,
          borderDash: [6, 3],
          pointRadius: 3,
          yAxisID: 'y1',
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      scales: {
        y: {
          type: 'linear',
          position: 'left',
          title: { display: true, text: 'Loan Approval %' },
        },
        y1: {
          type: 'linear',
          position: 'right',
          title: { display: true, text: 'OPR %' },
          grid: { drawOnChartArea: false },
          min: 0,
          max: 5,
        }
      }
    }
  });

  // Chart 3: Price to Income Ratio
  new Chart(document.getElementById('chart-pti'), {
    type: 'line',
    data: {
      labels: macro.price_to_income_ratio.years.map(String),
      datasets: [{
        label: 'Price-to-Income Ratio',
        data: macro.price_to_income_ratio.values,
        borderColor: COLORS.gold,
        backgroundColor: COLORS.gold_bg,
        fill: true,
        pointRadius: 5,
        pointBackgroundColor: COLORS.gold,
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: false }
      }
    }
  });
}

/* ── Regions Page ── */
async function initRegions() {
  setChartDefaults();
  const { prices } = await loadData();
  setUpdated(prices.updated);

  const regionNames = {
    kl: 'Kuala Lumpur',
    selangor: 'Selangor',
    penang: 'Penang',
    johor: 'Johor Bahru',
    sabah: 'Kota Kinabalu',
  };

  // Populate region cards
  const grid = document.getElementById('region-grid');
  for (const [key, name] of Object.entries(regionNames)) {
    const r = prices.regions[key];
    const yoyClass = r.yoy >= 0 ? 'positive' : 'negative';
    const yoySign = r.yoy >= 0 ? '+' : '';
    const lastTx = last(r.quarterly_transactions);

    const card = document.createElement('div');
    card.className = 'region-card';
    card.innerHTML = `
      <h3>${name}</h3>
      <div class="stat">
        <span class="stat-label">Median Price</span>
        <span class="stat-value">${fmtRM(r.median_price)}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Rental Yield</span>
        <span class="stat-value">${r.rental_yield}%</span>
      </div>
      <div class="stat">
        <span class="stat-label">Q4 Transactions</span>
        <span class="stat-value">${fmtNum(lastTx)}</span>
      </div>
      <div class="stat">
        <span class="stat-label">YoY Change</span>
        <span class="stat-value ${yoyClass}">${yoySign}${r.yoy}%</span>
      </div>
    `;
    grid.appendChild(card);
  }

  // Chart: median price comparison
  const keys = Object.keys(regionNames);
  new Chart(document.getElementById('chart-region-prices'), {
    type: 'bar',
    data: {
      labels: keys.map(k => regionNames[k]),
      datasets: [{
        label: 'Median Price (RM)',
        data: keys.map(k => prices.regions[k].median_price),
        backgroundColor: [COLORS.gold, COLORS.blue1, COLORS.blue2, COLORS.blue3, COLORS.green],
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: {
          ticks: { callback: v => fmtRM(v) },
          beginAtZero: true,
        }
      }
    }
  });
}

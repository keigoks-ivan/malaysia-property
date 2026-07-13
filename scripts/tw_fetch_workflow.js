export const meta = {
  name: 'tw-clock-data',
  description: 'Fan out agents to fetch Taiwan five-force macro/property series from official open sources',
  phases: [{ title: 'Fetch', detail: 'one agent per official TW series' }],
}

// common quarter axis 2001Q1..2026Q1 (matches the Sinyi price seed)
const QAXIS = []
for (let y = 2001; y <= 2026; y++) for (let q = 1; q <= 4; q++) { QAXIS.push(`${y}Q${q}`); if (y===2026 && q===1) break }

const OUTDIR = '/private/tmp/claude-501/-Users-ivanchang-malaysia-property/52542b53-2f2a-49e2-9a78-6dd7a75141c7/scratchpad/tw'

const SCHEMA = {
  type: 'object',
  properties: {
    key: { type: 'string' },
    available: { type: 'boolean' },
    q: { type: 'array', items: { type: 'string' } },
    v: { type: 'array', items: { type: ['number', 'null'] } },
    unit: { type: 'string' },
    source_url: { type: 'string' },
    sanity: { type: 'string' },
    notes: { type: 'string' },
  },
  required: ['key', 'available', 'q', 'v'],
}

const COMMON = `
You are fetching ONE official Taiwan statistical series and returning it as a clean quarterly array.

HARD RULES:
- Use ONLY legitimate official / open-data sources (主計總處 stat.gov.tw / nstatdb.dgbas.gov.tw, 中央銀行 cbc.gov.tw, 內政部 moi.gov.tw / 不動產資訊平台 pip.moi.gov.tw, 戶政司, 政府資料開放平臺 data.gov.tw, 台電). NEVER bypass any login, paywall, CAPTCHA, or bot-detection. If a source is walled, try another official source; if none work, return available:false honestly.
- Use Bash (curl) + python3 to download and parse (CSV / XLS / JSON / HTML tables). WebSearch/WebFetch to locate the right file URL first.
- Convert 民國/ROC years to Gregorian by +1911 (e.g. 民國90 = 2001).
- Frequency conversion to quarterly: monthly -> mean of the 3 months in the quarter; annual -> hold the year's value across its 4 quarters (or the reported value); already-quarterly -> map directly.
- ALIGN your output to EXACTLY this quarter axis (length ${QAXIS.length}): ${QAXIS.join(',')}
  Fill quarters before your data starts, or any gaps, with null. Do not shift or pad wrongly — index i of v must correspond to q[i].
- SANITY-CHECK against known Taiwan history and report it in \`sanity\` (e.g. unemployment ~6% in 2009 GFC and ~3.7% in 2021; real GDP negative in 2009 and high in 2021; CPI drifting up ~1-2%/yr; house-price-to-income rising secularly to ~9-10x nationally by 2020s). If numbers contradict history, say so.
- Also write your result JSON to a file: mkdir -p ${OUTDIR} && write ${OUTDIR}/<key>.json  (so the orchestrator can read it even if needed).
- Return the schema object. Put the source file URL in source_url and a one-line method + coverage span in notes.
`

const TASKS = [
  { key: 'gdp_real', title: 'real GDP', prompt: `Fetch Taiwan REAL GDP, quarterly level (實質GDP，季，經濟成長率的底層水準；chained 2021 or whatever base). Source: 主計總處 國民所得統計 (GDP-季). Longest history available (ideally back to 2001 or earlier). Return the quarterly real GDP level in v (used later for YoY).` },
  { key: 'unemp', title: 'unemployment', prompt: `Fetch Taiwan unemployment rate 失業率 (%), monthly, from 主計總處 人力資源調查. Convert to quarterly mean. Longest history (>=2001).` },
  { key: 'cpi', title: 'CPI', prompt: `Fetch Taiwan CPI 消費者物價指數 total index (level, not YoY), monthly, from 主計總處 物價統計. Convert to quarterly mean. Longest history (>=2000, so 2001Q1 YoY exists).` },
  { key: 'pop2554', title: 'prime-age pop', prompt: `Fetch Taiwan population aged 25-54 (壯年人口，人數 level). Source: 內政部戶政司 人口統計 (現住人口數按年齡/單齡別) — sum ages 25 through 54, or the 25-54 band. Monthly or year-end is fine (convert to quarterly). Longest history (>=2001). If only 5-year bands available, use 25-29+30-34+...+50-54.` },
  { key: 'pti', title: 'price-to-income', prompt: `Fetch Taiwan house-price-to-income ratio 房價所得比 (全國, 倍), quarterly. Source: 內政部 不動產資訊平台 (住宅資訊統計彙報 / 房價負擔能力). Available from ~2002. Return the ratio level in v.` },
  { key: 'credit_bal', title: 'mortgage credit', prompt: `Fetch Taiwan 購置住宅貸款餘額 (outstanding house-purchase loans, NT$ level), monthly, from 中央銀行 (CBC) 金融統計. Convert to quarterly (quarter-end or mean). Longest history (>=2001). This is the housing credit stock.` },
  { key: 'mortgage_rate', title: 'mortgage rate', prompt: `Fetch Taiwan 五大銀行新承做購屋貸款利率 (five major banks new house-purchase loan rate, %), monthly, from 中央銀行 (CBC). Convert to quarterly mean. Longest history (>=2001).` },
  { key: 'lowuse', title: 'low-use vacancy', prompt: `Fetch Taiwan 低度使用（用電）住宅比率 / 低度使用住宅宅數比率 (%), annual. Source: 內政部 不動產資訊平台 / 台電 low-electricity-use housing. Available from ~2009. Convert annual -> hold across the 4 quarters of each year. This is the vacancy proxy.` },
  { key: 'completions', title: 'housing completions', prompt: `Fetch Taiwan 住宅類 使用執照 核發宅數 or 住宅完工量 (housing completions / use-licenses, dwelling units), monthly or annual, from 內政部營建署 / 不動產資訊平台. Convert to quarterly (sum months in quarter, then annualise x4 if monthly). Longest history (>=2001). Used as the supply/absorption side.` },
]

phase('Fetch')
const results = await parallel(TASKS.map(t => () =>
  agent(COMMON + '\n\nTASK: ' + t.prompt + `\nSet key="${t.key}".`,
    { label: `tw:${t.key}`, phase: 'Fetch', schema: SCHEMA, agentType: 'general-purpose', model: 'sonnet', effort: 'high' })
    .then(r => r ? { ...r, key: r.key || t.key } : { key: t.key, available: false, q: QAXIS, v: QAXIS.map(()=>null), notes: 'agent returned null' })
))

const ok = results.filter(r => r && r.available)
log(`fetched ${ok.length}/${TASKS.length}: ${ok.map(r=>r.key).join(', ')}`)
log(`unavailable: ${results.filter(r=>!r||!r.available).map(r=>r.key).join(', ') || 'none'}`)
return { axis: QAXIS, results }

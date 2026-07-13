export const meta = {
  name: 'my-clock-data',
  description: 'Fan out agents to fetch Malaysia five-force macro/property series from official + international sources',
  phases: [{ title: 'Fetch', detail: 'one agent per Malaysia series' }],
}

const QAXIS = []
for (let y = 2000; y <= 2026; y++) for (let q = 1; q <= 4; q++) { QAXIS.push(`${y}Q${q}`); if (y===2026 && q===1) break }
const OUTDIR = '/private/tmp/claude-501/-Users-ivanchang-malaysia-property/52542b53-2f2a-49e2-9a78-6dd7a75141c7/scratchpad/my'

const SCHEMA = {
  type: 'object',
  properties: {
    key: { type: 'string' }, available: { type: 'boolean' },
    q: { type: 'array', items: { type: 'string' } },
    v: { type: 'array', items: { type: ['number', 'null'] } },
    unit: { type: 'string' }, source_url: { type: 'string' },
    sanity: { type: 'string' }, notes: { type: 'string' },
  },
  required: ['key', 'available', 'q', 'v'],
}

const COMMON = `
You are fetching ONE official Malaysia statistical series and returning it as a clean quarterly array.

HARD RULES:
- Use ONLY legitimate official / open sources. Best options for Malaysia (a member of IMF/World Bank/BIS, so international sources DO cover it):
    * OpenDOSM / DOSM (Dept of Statistics): https://open.dosm.gov.my , https://api.data.gov.my (modern JSON/parquet APIs — GDP, CPI, unemployment, population, income)
    * Bank Negara Malaysia (BNM): https://api.bnm.gov.my (OPR, interest rates); BNM monthly statistical bulletin
    * World Bank API: https://api.worldbank.org/v2/country/MYS/indicator/{CODE}?format=json&per_page=500 (annual, long history)
    * IMF IFS / DBnomics: https://api.db.nomics.world/v22/series/IMF/IFS/Q.MY.{code}
    * NAPIC (napic.jpph.gov.my) / data.gov.my for property (overhang, completions, transactions)
    * BIS bulk (data.bis.org) for household credit
- NEVER bypass any login, paywall, CAPTCHA, or bot-detection. If a source is walled, try another; if none work, return available:false.
- Use Bash (curl) + python3 to download and parse (JSON / CSV / XLS). WebSearch/WebFetch to locate the right endpoint first.
- Frequency -> quarterly: monthly -> mean of the 3 months; annual -> hold the year's value across its 4 quarters; quarterly -> map directly. Prefer the LONGEST series (ideally back to 2000 or earlier); annual is fine if quarterly unavailable.
- ALIGN output to EXACTLY this quarter axis (length ${QAXIS.length}): ${QAXIS.join(',')}
  Fill quarters before your data starts, or gaps, with null. Index i of v must correspond to q[i].
- SANITY-CHECK against known Malaysia history and report in \`sanity\` (e.g. GDP: deep contraction in 2020 COVID (~-17% YoY in 2020Q2) then rebound; 1998 Asian-crisis contraction if your series reaches back; unemployment ~3-3.5% normally, spiking to ~5% in 2020; CPI drifting ~2%/yr with a 2022-23 bump; OPR 3.5% pre-2008, cut to 2.0% in 2009, 3.25% by 2018, 1.75% in 2020 COVID, back to 3.0% by 2023-2024; house prices rose continuously — a "welded" market with almost no nominal declines).
- Write your result JSON to a file: mkdir -p ${OUTDIR} && write ${OUTDIR}/<key>.json
- Return the schema object. source_url = the data file/endpoint; notes = one-line method + coverage span.
`

const TASKS = [
  { key: 'gdp_real',   prompt: `Malaysia REAL GDP, quarterly level (constant prices). Source: OpenDOSM (gdp) or IMF IFS quarterly or World Bank NY.GDP.MKTP.KD (annual fallback). Longest history. Return level in v (for YoY).` },
  { key: 'unemp',      prompt: `Malaysia unemployment rate (%). Source: OpenDOSM labour force (monthly/quarterly) or World Bank SL.UEM.TOTL.ZS (annual). Convert to quarterly. Longest history.` },
  { key: 'cpi',        prompt: `Malaysia CPI total index (level, not YoY). Source: OpenDOSM (cpi_headline) monthly or IMF IFS. Convert to quarterly mean. Longest history (>=1999 so 2000Q1 YoY exists).` },
  { key: 'pop',        prompt: `Malaysia population — prime working-age if possible (25-54 or 15-64), else total population (level). Source: OpenDOSM population or World Bank SP.POP.1564.TO / SP.POP.TOTL (annual). Convert annual -> hold. Longest history. Used for demographic growth.` },
  { key: 'income',     prompt: `Malaysia household income proxy: median monthly household income (DOSM, published for select years — interpolate) OR GNI per capita (World Bank NY.GNP.PCAP.CD, annual). Return level in v; this is the valuation denominator (price/income). Longest history.` },
  { key: 'credit',     prompt: `Malaysia household / housing credit outstanding (level). Best: BIS long series of credit to households (data.bis.org, MY), or BNM loans for purchase of residential property, or total household debt. Convert to quarterly. Longest history. Used as the money/credit force.` },
  { key: 'rate',       prompt: `Malaysia policy / mortgage rate (%). Best: BNM Overnight Policy Rate OPR (from 2004; before that the 3-month intervention rate), or average lending rate / base rate. Source: BNM api.bnm.gov.my or OpenDOSM. Convert to quarterly mean. Longest history.` },
  { key: 'overhang',   prompt: `Malaysia residential property OVERHANG — unsold completed units (units). Source: NAPIC (napic.jpph.gov.my) property market reports / data.gov.my. Quarterly or annual/half-yearly. Longest history you can find (NAPIC has it back ~2004). This is the supply-glut / vacancy proxy (high = loose).` },
  { key: 'completions',prompt: `Malaysia residential COMPLETIONS or new housing supply (units, dwellings completed per period). Source: NAPIC / data.gov.my / DOSM construction. Quarterly or annual. Longest history. Supply-flow force.` },
]

phase('Fetch')
const results = await parallel(TASKS.map(t => () =>
  agent(COMMON + '\n\nTASK: ' + t.prompt + `\nSet key="${t.key}".`,
    { label: `my:${t.key}`, phase: 'Fetch', schema: SCHEMA, agentType: 'general-purpose', model: 'sonnet', effort: 'high' })
    .then(r => r ? { ...r, key: r.key || t.key } : { key: t.key, available: false, q: QAXIS, v: QAXIS.map(()=>null), notes: 'agent returned null' })
))

const ok = results.filter(r => r && r.available)
log(`fetched ${ok.length}/${TASKS.length}: ${ok.map(r=>r.key).join(', ')}`)
log(`unavailable: ${results.filter(r=>!r||!r.available).map(r=>r.key).join(', ') || 'none'}`)
return { axis: QAXIS, results }

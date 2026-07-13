export const meta = {
  name: 'jp-clock-data',
  description: 'Fan out agents to fetch Japan five-force macro/property series from FRED/OECD/IMF/e-Stat/BOJ',
  phases: [{ title: 'Fetch', detail: 'one agent per Japan series' }],
}

const QAXIS = []
for (let y = 1975; y <= 2025; y++) for (let q = 1; q <= 4; q++) QAXIS.push(`${y}Q${q}`)
const OUTDIR = '/private/tmp/claude-501/-Users-ivanchang-malaysia-property/52542b53-2f2a-49e2-9a78-6dd7a75141c7/scratchpad/jp'

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
You are fetching ONE official Japan statistical series and returning it as a clean quarterly array.

HARD RULES:
- Use ONLY legitimate official / open sources. Japan is well-covered internationally:
    * FRED (fredgraph.csv?id=CODE, no key) — many long Japan series, e.g. LRUNTTTTJPQ156S (unemployment, quarterly 1955+), JPNCPIALLMINMEI (CPI monthly), JPNRGDPEXP (real GDP quarterly 1994+), NGDPRSAXDCJPQ (real GDP), INTDSRJPM193N (discount rate), IRLTLT01JPM156N (10y govt bond), IR3TIB01JPM156N (3m rate), JPNPROINDMISMEI, housing starts series.
    * OECD SDMX / OECD.Stat, IMF IFS / DBnomics (api.db.nomics.world/v22/series/IMF/IFS/Q.JP.<code>)
    * World Bank API (api.worldbank.org/v2/country/JPN/indicator/CODE?format=json&per_page=500) — annual, long
    * e-Stat (Japan Statistics Bureau, api.e-stat.go.jp — needs free appId; if none, use portal CSVs) — housing starts (国交省), vacancy rate 空き家率 (住宅・土地統計調査, every 5y), population
    * Bank of Japan (BOJ) Time-Series Data Search (www.stat-search.boj.or.jp) — policy rate, loans, mortgage
    * BIS bulk (data.bis.org) — credit to households
- NEVER bypass any login, paywall, CAPTCHA, or bot-detection. If a source is walled, try another; if none work, return available:false.
- Use Bash (curl) + python3 to download and parse. WebSearch/WebFetch to locate endpoints.
- Frequency -> quarterly: monthly -> mean of the quarter; annual/5-yearly -> hold (or interpolate) across quarters; quarterly -> map directly. Prefer the LONGEST series (ideally back to 1975 or earlier).
- ALIGN output to EXACTLY this quarter axis (length ${QAXIS.length}): ${QAXIS.join(',')}
  Fill quarters before your data starts, or gaps, with null. Index i of v must correspond to q[i].
- SANITY-CHECK against known Japan history and report in \`sanity\`: house prices peaked ~1991 then fell ~40% into ~2005; unemployment ~2% in 1990 rising to ~5.5% by 2002, back to ~2.5% by 2019, COVID bump 2020; CPI roughly flat/deflationary 1995-2012 then a 2014 tax bump and 2022-23 inflation; policy/discount rate ~6% in 1990 -> ~0% by 1999 (ZIRP) -> negative 2016 -> hikes from 2024; population peaked ~2008 then declining; real GDP: lost-decade stagnation 1990s, -5% 2009 GFC, COVID 2020.
- Write your result JSON to a file: mkdir -p ${OUTDIR} && write ${OUTDIR}/<key>.json
- Return the schema object. source_url = the endpoint; notes = one-line method + coverage span.
`

const TASKS = [
  { key: 'gdp_real',   prompt: `Japan REAL GDP, quarterly level (constant prices). FRED JPNRGDPEXP or NGDPRSAXDCJPQ (quarterly), backfill pre-1994 with OECD/World Bank annual real GDP (rescaled, held). Longest history. Return level for YoY.` },
  { key: 'unemp',      prompt: `Japan unemployment rate (%). FRED LRUNTTTTJPQ156S (quarterly, 1955+) — ideal. Longest history.` },
  { key: 'cpi',        prompt: `Japan CPI total index (level). FRED JPNCPIALLMINMEI (monthly) -> quarterly mean. Longest history (>=1974 so 1975Q1 YoY exists).` },
  { key: 'pop',        prompt: `Japan working-age population 15-64 (level). World Bank SP.POP.1564.TO or FRED/e-Stat. Annual -> hold. Captures the demographic decline (peak ~1995, falling since). Longest history.` },
  { key: 'income',     prompt: `Japan household income proxy: real household disposable income or GDP per capita or compensation. OECD / FRED / World Bank NY.GDP.PCAP.KD (annual). Return level; valuation denominator (price/income). Longest history.` },
  { key: 'credit',     prompt: `Japan credit to households (level). BIS long series (data.bis.org, JP households) or BOJ loans. Convert to quarterly. Longest history. The money/credit force.` },
  { key: 'rate',       prompt: `Japan policy / benchmark interest rate (%). FRED INTDSRJPM193N (discount rate, 1955+) or the BOJ uncollateralized overnight call rate, or 10y JGB IRLTLT01JPM156N. Monthly -> quarterly mean. Longest history — must capture the 1990 ~6% peak, ZIRP from ~1999, negative rates 2016, hikes from 2024.` },
  { key: 'starts',     prompt: `Japan housing starts (new dwelling units started, level). FRED if available, else e-Stat / 国土交通省 建築着工統計 (monthly, long). Convert to quarterly (sum or mean). Longest history. Supply-flow force.` },
  { key: 'vacancy',    prompt: `Japan housing vacancy rate 空き家率 (%). e-Stat 住宅・土地統計調査 (Housing and Land Survey, every 5 years: 1978,1983,...,2018,2023). Return the survey values on their years and null (or hold/interpolate) between — note the method. This is the vacancy structural input. If truly unavailable, available:false.` },
]

phase('Fetch')
const results = await parallel(TASKS.map(t => () =>
  agent(COMMON + '\n\nTASK: ' + t.prompt + `\nSet key="${t.key}".`,
    { label: `jp:${t.key}`, phase: 'Fetch', schema: SCHEMA, agentType: 'general-purpose', model: 'sonnet', effort: 'high' })
    .then(r => r ? { ...r, key: r.key || t.key } : { key: t.key, available: false, q: QAXIS, v: QAXIS.map(()=>null), notes: 'agent returned null' })
))

const ok = results.filter(r => r && r.available)
log(`fetched ${ok.length}/${TASKS.length}: ${ok.map(r=>r.key).join(', ')}`)
log(`unavailable: ${results.filter(r=>!r||!r.available).map(r=>r.key).join(', ') || 'none'}`)
return { axis: QAXIS, results }

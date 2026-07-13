export const meta = {
  name: 'compass-content',
  description: 'Generate bilingual copy for the Compass + Report Card redesign (4 markets + methodology + how-to)',
  phases: [{ title: 'Copy', detail: 'market judgments, methodology, how-to' }],
}

const ctx = typeof args === 'string' ? JSON.parse(args) : (args || {})  // { us:{...}, ... }

const EVIDENCE = `
EMPIRICAL FINDINGS behind this redesign (the old page was a Structure×Flow 2×2 "property clock"):
- Per-factor test of forward-3y house-price return across US/TW/MY/JP: MOMENTUM (house-price trend) is the ONLY factor with consistent predictive power in all four markets (+7 to +14pp gap between its positive and negative states).
- VALUATION is unstable: it mean-reverts in cyclical markets but REVERSES in Japan (−18.9pp — cheap predicted WORSE, because Japan's cheapness was structural decay, not a bargain).
- The old framework's two composite axes (Structure, Flow) each reversed in some market (Structure reversed in Japan −7.5, Flow reversed in Taiwan). In Japan the old 2×2's four cells were ordered BACKWARDS (Melt-up best, Expansion worst).
- The old framework conflated two different questions: "where do prices go next" (prediction — momentum's job) and "is this market healthy/expensive" (diagnosis — fundamentals' job). Averaging 4-5 heterogeneous fundamentals into one axis, then slicing into four cells and calling it a cycle "clock", was the core mistake.
- NEW design = split into two instruments:
   COMPASS (predictive, trend-following): X=momentum, Y=credit-impulse → 4 cells: Uptrend·Fuelled(mom+cred+), Uptrend·Draining(mom+cred−), Downtrend·Reflating(mom−cred+), Downtrend·Starved(mom−cred−). Plus a SUPPLY-GLUT warning (vacancy/completions extreme).
   REPORT CARD (descriptive, NOT predictive): valuation, population, supply shown as transparent per-force gauges — never averaged, never used to predict.
- Compass 4-cell forward ordering validates in US/MY/JP (Fuelled>Starved) but NOT Taiwan — because Taiwan has only 101 quarters of almost single-directional bull market, so "downtrend" quarters are all followed by the next leg up. That is a DATA limitation (short, one-sided sample), disclosed, not a method flaw. Momentum still fixed Japan, the market that actually had a crash.
- Honest stance: the compass reads the CURRENT trend+money state (descriptive strong; predictive good in markets with real cycles); the report card reads health; forward returns are shown honestly, not oversold. Supply is in the compass as a warning overlay; demand/population/valuation are on the report card.`

const MSCHEMA = {
  type: 'object',
  properties: {
    judge_en: { type: 'string' }, judge_zh: { type: 'string' },
    warn_en: { type: 'string' }, warn_zh: { type: 'string' },
    card_val_en: { type: 'string' }, card_val_zh: { type: 'string' },
    card_pop_en: { type: 'string' }, card_pop_zh: { type: 'string' },
    card_sup_en: { type: 'string' }, card_sup_zh: { type: 'string' },
    traj_en: { type: 'string' }, traj_zh: { type: 'string' },
  },
  required: ['judge_en','judge_zh','warn_en','warn_zh','card_val_en','card_val_zh','card_pop_en','card_pop_zh','card_sup_en','card_sup_zh','traj_en','traj_zh'],
}
const STYLE = `STYLE: Traditional-Chinese uses FULL-WIDTH punctuation（，。：「」）; numbers/latin keep half-width. English is plain, precise, no hype, no self-labels. Every claim must match the data given — do NOT invent numbers. Keep each field to 1-3 sentences.`

const CELLNAME = { fuelled:'Uptrend·Fuelled 上行·有燃料', draining:'Uptrend·Draining 上行·資金退', reflating:'Downtrend·Reflating 下行·資金回流', starved:'Downtrend·Starved 下行·斷炊' }
const MKTNAME = { us:'United States 美國', tw:'Taiwan 台灣', my:'Malaysia 馬來西亞', jp:'Japan 日本' }

function marketPrompt(m) {
  const c = ctx[m]
  return `Write the bilingual copy for the ${MKTNAME[m]} panel of a property "trend compass + report card".
DATA for ${MKTNAME[m]} (quarter ${c.now}):
- Compass cell = ${CELLNAME[c.quad]}  (momentum z=${c.mom}, credit-impulse z=${c.cred}; + = up/expanding, − = down/contracting)
- Supply-glut warning = ${c.warn ? 'ON (vacancy or completions at an extreme — supply is loose)' : 'off'}
- House-price YoY now = ${c.hpi_yoy_now}%
- Report-card factors (z-scores; interpret the SIGN): valuation ${c.card_now.valuation} (+ = cheap vs own recent history, − = expensive), population ${c.card_now.population} (+ = growing, − = shrinking, absolute direction), supply-flow ${c.card_now.supply} (+ = tight/low completions, − = loose/high), vacancy ${c.card_now.vacancy} (+ = low vacancy/tight, − = high vacancy/loose)
- Forward-3y return by compass cell (median%, n): ${JSON.stringify(Object.fromEntries(Object.entries(c.qstat).map(([k,v])=>[k,`${v.med}% n=${v.n}`])))}
- Recent trajectory (compass cells): ${JSON.stringify(c.runs_last6)}

Market character to respect: US = a real cycle (bubble 2005, crash 2008, recovery). TW = short sample (from 2001), almost single-directional bull, so its forward numbers are unreliable — say the compass reads its current state, don't oversell prediction. MY = "welded" market, nominal prices ~never fall. JP = the one with a genuine bubble-and-crash (1991 peak, −40% to 2005) and a shrinking population.

Produce these fields (${STYLE}):
- judge_en / judge_zh: the current reading — name the compass cell in plain language, why (momentum + credit), and what it means for this market. 2-3 sentences.
- warn_en / warn_zh: one sentence on the supply-glut warning (what "supply loose" means here — e.g. NAPIC overhang for MY, 空き家率 for JP, low-electricity vacancy for TW, months-supply for US).
- card_val_en/zh, card_pop_en/zh, card_sup_en/zh: ONE plain sentence each reading the valuation / population / supply gauge for THIS market from its sign+value (report card = health, not prediction).
- traj_en / traj_zh: one sentence recapping the recent trajectory through the compass cells.`
}

phase('Copy')
const markets = ['us','tw','my','jp']
const jobs = [
  ...markets.map(m => () => agent(marketPrompt(m), { label:`copy:${m}`, phase:'Copy', schema:MSCHEMA, agentType:'general-purpose', model:'sonnet', effort:'high' }).then(r=>({kind:'market',m,...r}))),
  () => agent(`Write the methodology copy for a redesign that REPLACES a Structure×Flow four-quadrant "property clock" with a "trend Compass + Report Card". ${EVIDENCE}
Produce (${STYLE}, this is the intellectual core — be substantive, honest, a bit essayistic but tight):
- lede_en / lede_zh: a lede (~120-160 words each) introducing the two instruments and why the old single 2×2 was retired.
- why_en / why_zh: a longer "why we changed it" section (~180-240 words each) walking through the empirical findings: momentum is the only consistent predictor, valuation is unstable (reverses in Japan), the old framework conflated prediction with diagnosis, so we split them; be candid that the compass validated in 3/4 markets and Taiwan's failure is a short-sample artifact.`,
    { label:'copy:method', phase:'Copy', schema:{type:'object',properties:{lede_en:{type:'string'},lede_zh:{type:'string'},why_en:{type:'string'},why_zh:{type:'string'}},required:['lede_en','lede_zh','why_en','why_zh']}, agentType:'general-purpose', model:'sonnet', effort:'high' }).then(r=>({kind:'method',...r})),
  () => agent(`Write "how to read it" copy for a property "trend Compass + Report Card". ${EVIDENCE}
Produce (${STYLE}):
- compass_howto_en/zh: how to read the compass — X=momentum (price trend), Y=credit impulse; four cells Uptrend·Fuelled / Uptrend·Draining / Downtrend·Reflating / Downtrend·Starved; the glowing dot is the latest quarter; the supply-glut warning overlays a caution. 2-3 sentences.
- card_howto_en/zh: how to read the report card — valuation / population / supply as transparent gauges that describe HEALTH, deliberately NOT averaged into a score and NOT used to predict returns. 2 sentences.
- fwd_note_en/zh: an honest note on the forward-return table — the cells order best→worst in US/MY/JP but Taiwan's short one-sided sample breaks it; treat forward numbers as descriptive, not a promise. 2 sentences.`,
    { label:'copy:howto', phase:'Copy', schema:{type:'object',properties:{compass_howto_en:{type:'string'},compass_howto_zh:{type:'string'},card_howto_en:{type:'string'},card_howto_zh:{type:'string'},fwd_note_en:{type:'string'},fwd_note_zh:{type:'string'}},required:['compass_howto_en','compass_howto_zh','card_howto_en','card_howto_zh','fwd_note_en','fwd_note_zh']}, agentType:'general-purpose', model:'sonnet', effort:'high' }).then(r=>({kind:'howto',...r})),
]

const results = await parallel(jobs)
log(`generated ${results.filter(Boolean).length} copy blocks`)
return results

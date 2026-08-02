# 候選制度第二輪複核（5 筆）

複核日期：2026-08-02
方法：五組獨立 subagent 各自重查一筆，本文為彙整者對五份報告的最終裁決（非直接照搬 agent 建議；瓜地馬拉、保加利亞兩筆對 agent 的建議做了進一步收斂）。

## 查證方法與限制誠實揭露

- 本輪彙整者（非五組 subagent）自身的 WebSearch 額度已於任務開始前即顯示用罄（`this session has used its web search budget (200 of 200)`），**故彙整者對「巴西 BRL→USD 匯率」一項改用 `WebFetch` 直接呼叫 `open.er-api.com` 即時匯率 API 取得（2026-08-02 擷取，1 USD = 5.065913 BRL），未使用 WebSearch**。五組 subagent 各自的 session 額度與方法獨立，詳見各自報告內的「could not verify / 方法」段落——多組亦回報 WebSearch 於任務中途或開始前即耗盡，改用 DuckDuckGo HTML 版、`r.jina.ai` 文字代理、或直接 `curl`／`WebFetch` 打官方網域／PDF。
- 巴西一筆的 BRL→USD 換算為**編輯性換算**，比照 `data/visa-property.json` 現行 `fx_notes` 慣例處理（不是法定金額，正式入庫時應由持有 JSON 編輯權的那組 agent 依其 fx_notes 段落格式重新標註來源與擷取時間）。

## 裁決總表

| 法域 | 前輪主張 | 本輪裁決 | 理由一句話 |
|---|---|---|---|
| 🇧🇷 巴西 | RN 36/2018 現行，門檻 BRL 100萬／東北部 70萬 | **INCLUDE** | Tier 1 一手法條全文（含兩次修正）逐條核實，門檻、地區折扣、4 年期、14 天╱2 年停留規則全部verbatim確認；唯一需修正是「轉無限期」並非自動，是文件審核制 |
| 🇪🇨 厄瓜多 | 官方頁面確認，100 SBU（約 4.82 萬美元）之不動產投資人簽證 | **INCLUDE**（但 `route_type` 須由 property_is_route 改為 **property_one_of_several**，且制度名稱需更正） | Tier 1 核實 100 SBU 不動產路徑存在且可單獨達標，但同一簽證類別下不動產只是四種合格投資形式之一（另有銀行存款、公司股權、政府投資合約），並非專屬的「不動產簽證」；2026 年 SBU 金額本身僅達 tier 2/3 |
| 🇬🇹 瓜地馬拉 | IGM 官方表格確認 10 萬美元、「Certificaciones registrales」＝不動產登記證明 | **HOLD** | 表格本身與其引用之法源條號皆達 tier 1，但「Certificaciones registrales」是否確實涵蓋不動產——而非商業登記處或其他登記——本輪仍未能從母法或子法規原文直接證實，僅剩結構性推論與一個帶有法源矛盾的行銷類部落格佐證 |
| 🇵🇾 巴拉圭 | 官方公告，20 萬美元不動產或證券換十年永久居留 | **INCLUDE_WITH_CAVEAT** | 兩個官方網域（MIC、Migraciones）的公告頁一致證實制度與 20 萬美元門檻本身，但決議原文（Gaceta Oficial）未能取得；「十年」年限這個數字**在任何層級都查無依據**，應予撤除；實際受理狀況（申請入口網、規費、表單）亦未能確認，SUACE 官網對此制度的站內搜尋掛零 |
| 🇧🇬 保加利亞 | 《外國人法》第 24 條第 1 項第 19 款＋60 萬列弗延展居留，翻案既有「無途徑」結論 | **HOLD（維持原否定結論，加註警語，不翻轉）** | 本輪僅取得下位規範（實施細則第 29a 條）文字，且是透過不穩定、需重複嘗試才成功的替代管道（apis.bg 子網域＋dv.parliament.bg，其中一次同一 URL 重複請求出現「有內容／無內容」不一致）取得；母法第 24 條第 1 項第 19 款本身仍未被任何人直接讀到全文。依裁決標準明文規定「若真的攻不下 tier 1，就照實裁決為加警語但不翻轉結論」，本輪雖把 tier 2 佐證從 3 筆擴充到 13 筆（含多家保加利亞文執業律師事務所）且零矛盾，仍不足以達到翻轉一個**已公開刊登**之否定結論所需的門檻 |

**「44 套」→ 建議改為 47 套**（新增巴西、厄瓜多、巴拉圭三筆；瓜地馬拉維持排除、保加利亞維持「無途徑」但加註警語，兩者皆不計入分母）。

---

## 逐筆

### 巴西

**裁決**：INCLUDE

**tier 1 取得狀況**：完整取得。直接開啟 gov.br 官方 PDF（前輪提供的 URL 本身即可正常開啟，非被擋網站），且該 PDF 是司法部自己維護的**合併校訂版**，逐條標示經 RN 46/2021（2021-12-09）、RN 49/2024（2024-06-25）修正之處；另交叉核對司法部同網域下的現行決議索引頁，確認自 RN 49/2024 之後（最新至 RN 51/2025，與不動產無關）沒有任何決議再修正過 RN 36/2018。

**證據**：
- https://www.gov.br/mj/pt-br/assuntos/seus-direitos/migracoes/portal-de-imigracao-laboral/autorizacao-de-residencia-laboral-1/normas-de-imigracao-laboral/resolucoes-normativas/resolucao_normativa_no_36_de_9_de_outubro_de_2018.pdf（Tier 1，司法部官方 PDF，合併校訂版）

**與前輪的分歧**：
1. 前輪未特別強調「轉無限期並非自動」——本輪讀到第 5 條原文：4 年期滿後「得」（poderá）轉換為無限期，須另外提交投資條件仍維持之證明、外僑登記卡（CRNM）副本、居留期間之無犯罪紀錄證明。這是一個文件審核制的申請程序，不是自動轉換，站上文案若寫「4 年後自動轉永久」會不準確。
2. 新查得前輪未提及的第 6-B 條：投資條件在任何時點（含轉換為無限期之後）不再維持，均構成喪失居留身分之事由——換言之，賣掉該不動產不是「撐過 4 年後」就可以自由處分的安全期，而是持續性條件。
3. 前輪稱北部╱東北部折扣為「70 萬雷亞爾地板值」，本輪逐字核對第 2 條第 1 項：「投資最低金額得低於本條所訂總額至多 30%」——確認為折扣上限式表述，70 萬即為地板，75 萬的說法確認查無法條依據。
4. `route_type` 確認為 **property_is_route**：RN 36/2018 整份決議的主體就是不動產投資，非在更廣泛的多資產類別「投資人簽證」決議下的其中一款。

**入庫欄位資料**：

```json
{
  "id": "brazil",
  "region": "americas",
  "source_file": "visa-round2",
  "flag": "🇧🇷",
  "jurisdiction": "Brazil",
  "jurisdiction_zh": "巴西",
  "programme": "Real estate investor residence (RN 36/2018, as amended by RN 46/2021 and RN 49/2024)",
  "programme_zh": "不動產投資居留（RN 36/2018，經 RN 46/2021、RN 49/2024 修正）",
  "label_en": "Real Estate Investor Residence",
  "label_zh": "不動產投資居留",
  "route_type": "property_is_route",
  "confidence": "high",
  "outcome_class": "permanent",
  "established": {
    "threshold": "published",
    "term": "published",
    "stay": "published",
    "leads_to": "published"
  },
  "min_value": {
    "amount": 1000000,
    "currency": "BRL",
    "usd": 197000,
    "basis": "General threshold, urban real estate only (built or under construction; Art. 2 caput). May aggregate multiple properties to reach the threshold (Art. 2 §2). Co-ownership permitted but each co-owner must individually invest the full threshold (Art. 3 §1).",
    "tier": 1,
    "src": 0
  },
  "sort_usd": 197000,
  "extra_tiers": [
    {
      "label_en": "North and Northeast regions — the minimum investment value may be reduced by up to 30% below the standard threshold (Art. 2 §1: \"o valor mínimo do investimento poderá ser inferior até 30% do total\"), i.e. a floor of BRL 700,000, not a separate/conflicting figure.",
      "label_zh": "北部與東北部地區——投資最低金額得低於一般門檻至多 30%（第 2 條第 1 項），即地板值 BRL 700,000，並非另一個互相矛盾的數字。",
      "amount": 700000,
      "currency": "BRL",
      "usd": 138000,
      "tier": 1,
      "src": 0
    }
  ],
  "term": {
    "text_en": "4 years, fixed (Art. 3 §4 / Art. 4). If the investor misses the 14-day/2-year stay requirement or the conversion-application window, a fresh 4-year temporary term may be requested instead, provided the investment is still held (Art. 6-A).",
    "text_zh": "4 年固定期限（第 3 條第 4 項／第 4 條）。若錯過「14 天／2 年」停留規定或轉換申請窗口，得於投資仍維持之前提下重新申請一次 4 年期臨時居留（第 6-A 條）。",
    "tier": 1,
    "src": 0
  },
  "stay": {
    "text_en": "Minimum 14 days (continuous or split) per every rolling 2-year period, counted from Polícia Federal registration (Art. 6). Meeting this blocks the standard residency-abandonment clause.",
    "text_zh": "自聯邦警察局登記起算，每 2 年須累計在境內停留至少 14 天（可分次，第 6 條）。符合此規定可避免適用一般的居留放棄條款。",
    "tier": 1,
    "src": 0
  },
  "leads_to": {
    "text_en": "After the 4-year term, the permit MAY be converted to indefinite residence (Art. 5) — NOT automatic. Requires: proof the Art. 2 investment conditions are still maintained, a copy of the migrant registration card (CRNM), and clean criminal-record certificates covering the temporary-residence period. The investment must continue to be maintained even after conversion — ceasing to hold it at any point (fixed-term or indefinite) is cause for loss of status (Art. 6-B).",
    "text_zh": "4 年期滿後「得」轉換為無限期居留（第 5 條）——非自動轉換。須提交：投資條件仍維持之證明、外僑登記卡（CRNM）副本、居留期間之無犯罪紀錄證明。即使轉為無限期後，投資仍須持續維持——任何時點（固定期或無限期）不再持有投資即構成喪失居留身分之事由（第 6-B 條）。",
    "tier": 1,
    "src": 0
  },
  "ownership_form": {
    "text_en": "Urban real estate only (rural land does not qualify, Art. 2 caput). Multiple properties may be aggregated (Art. 2 §2). Co-ownership permitted, but each co-owner must individually invest the full threshold (Art. 3 §1).",
    "text_zh": "限都市不動產（農村土地不合格，第 2 條）。得合併多筆物件達標（第 2 條第 2 項）。允許共有，惟每位共有人須個別達到完整門檻金額（第 3 條第 1 項）。",
    "tier": 1,
    "src": 0
  },
  "offplan": {
    "text_en": "Qualifies. Accepted with a registered Promessa de Compra e Venda (purchase-and-sale promise), a construction permit (Alvará de Construção), and a registered Memorial de Incorporação (Art. 3 II).",
    "text_zh": "預售╱在建物件合格。須備已登記之「購售預約」（Promessa de Compra e Venda）、建照（Alvará de Construção）、已登記之「分割設立備忘錄」（Memorial de Incorporação）（第 3 條第 2 項）。",
    "tier": 1,
    "src": 0
  },
  "mortgage": {
    "text_en": "Financing/mortgage is allowed only on the portion of the price exceeding BRL 1,000,000 — the qualifying minimum itself must come from the investor's own external-origin funds and cannot be financed (Art. 3 §2).",
    "text_zh": "僅超過 BRL 1,000,000 之部分得以融資／貸款支應——達標所需之門檻金額本身須為投資人自有之境外來源資金，不得融資（第 3 條第 2 項）。",
    "tier": 1,
    "src": 0
  },
  "dependants": {
    "text_en": "Not established in this pass.",
    "text_zh": "本次查核未查證。",
    "tier": 1,
    "src": 0
  },
  "entry_tax": {
    "text_en": "Not established in this pass.",
    "text_zh": "本次查核未查證。",
    "tier": 1,
    "src": 0
  },
  "last_change": {
    "text_en": "Amended twice since original 2018 text: RN 46/2021 (9 Dec 2021) and RN 49/2024 (25 Jun 2024), both confirmed as amendments (not replacements) via the Ministry's own current resolutions index; no resolution newer than RN 49/2024 touches RN 36/2018 as of this pass (checked 2026-08-02 via the ministry's own listing page, not an exhaustive news search — a live search-engine sweep for any 2025/2026 amending announcement was not run).",
    "text_zh": "自 2018 年原文起經過兩次修正：RN 46/2021（2021-12-09）、RN 49/2024（2024-06-25），經司法部現行決議索引頁確認皆為「修正」而非「取代」；截至本次查核（2026-08-02），該索引頁未見任何晚於 RN 49/2024 之決議再修正 RN 36/2018（僅查核官方索引頁本身，未跑窮盡式新聞搜尋確認有無漏網的修法公告）。",
    "tier": 1,
    "src": 0
  },
  "short": {
    "term_en": "4 yrs, conversion to indefinite possible",
    "term_zh": "4 年，得轉無限期",
    "stay_en": "14 days / 2 yrs",
    "stay_zh": "每 2 年 14 天",
    "outcome_en": "Indefinite residence — conversion is discretionary and document-gated, not automatic",
    "outcome_zh": "無限期居留——轉換須另行申請並附證明文件，非自動轉換",
    "own_en": "Urban property only; qualifying minimum must be unmortgaged, external-origin funds",
    "own_zh": "限都市不動產；門檻金額須為境外來源資金，不得融資"
  },
  "notes_en": "Dedicated real-estate resolution (property_is_route), not a sub-option of a broader investor visa. Ongoing-maintenance condition (Art. 6-B) means there is no stated safe harbor for selling after N years — losing the underlying investment at any point risks loss of status, even post-conversion to indefinite residence. Funds must be transferred via a bank authorized/registered with the Banco Central do Brasil (Art. 3 I-b, II-b) — a hard documentary requirement. Government reserves the right to conduct on-site inspection of the investment (Art. 3 §3). Providing false or omitted information triggers a cancellation process (Art. 6-C). Health insurance and application fees were not found in RN 36/2018 itself and may exist under general immigration law (Decree 9.199/2017) — not checked in this pass, do not assume either way.",
  "notes_zh": "本決議為專屬不動產投資之獨立法源（非附屬於更廣泛投資人簽證下的其中一款）。持續維持條件（第 6-B 條）意味著法條並未明訂「持有滿 N 年後即可自由出售」的安全期——任何時點失去該投資標的均有喪失居留身分之風險，即使已轉為無限期居留亦然。資金須經巴西中央銀行核准／登記之銀行辦理跨境匯款（第 3 條第 1 項 b 款、第 2 項 b 款）——此為硬性文件要求。政府保留對投資標的進行實地查核之權利（第 3 條第 3 項）。提供不實或隱匿資訊將啟動撤銷程序（第 6-C 條）。健康保險與申請規費未見於 RN 36/2018 本文，可能規範於一般移民法規（2017 年第 9,199 號行政命令）內，本次未查證，不應假設有或沒有。",
  "sources": [
    {
      "url": "https://www.gov.br/mj/pt-br/assuntos/seus-direitos/migracoes/portal-de-imigracao-laboral/autorizacao-de-residencia-laboral-1/normas-de-imigracao-laboral/resolucoes-normativas/resolucao_normativa_no_36_de_9_de_outubro_de_2018.pdf",
      "publisher": "Ministério da Justiça e Segurança Pública (Brazil)",
      "tier": 1,
      "accessed": "2026-08-02"
    }
  ],
  "companion_requirements": [
    { "text_en": "Funds must be the applicant's own resources, of foreign/external origin (Art. 1 sole paragraph).", "text_zh": "資金須為申請人自有資源，且來源為境外（第 1 條唯一項）。", "tier": 1, "src": 0 },
    { "text_en": "Proof of international capital transfer via a bank authorized/registered with the Banco Central do Brasil (Art. 3 I-b, II-b).", "text_zh": "須提出經巴西中央銀行核准／登記之銀行辦理跨境匯款之證明（第 3 條第 1 項 b 款、第 2 項 b 款）。", "tier": 1, "src": 0 },
    { "text_en": "Clean-title proof (Registro Geral do Imóvel), free of liens/encumbrances, for completed properties (Art. 3 I-a).", "text_zh": "已完工物件須提出不動產登記處清潔產權證明，無任何負擔或抵押（第 3 條第 1 項 a 款）。", "tier": 1, "src": 0 },
    { "text_en": "At conversion to indefinite residence: clean criminal-record certificates covering the residence period, plus CRNM (migrant registration card) copy (Art. 5).", "text_zh": "申請轉換為無限期居留時：須提出居留期間之無犯罪紀錄證明，及外僑登記卡（CRNM）副本（第 5 條）。", "tier": 1, "src": 0 },
    { "text_en": "Government reserves the right to conduct on-site inspection of the investment (Art. 3 §3).", "text_zh": "政府保留對投資標的實地查核之權利（第 3 條第 3 項）。", "tier": 1, "src": 0 },
    { "text_en": "Ongoing condition: ceasing to meet the investment conditions at ANY point — during the fixed term or after conversion to indefinite — is cause for loss of status (Art. 6-B).", "text_zh": "持續性條件：任何時點（固定期間內或轉為無限期後）不再符合投資條件，均構成喪失居留身分之事由（第 6-B 條）。", "tier": 1, "src": 0 },
    { "text_en": "Not established in this pass: health insurance requirement, application/issuance fees (may fall under general Decree 9.199/2017, not checked).", "text_zh": "本次未查證：健康保險要求、申請／核發規費（可能規範於一般性之 2017 年第 9,199 號行政命令，本次未查核）。", "tier": 1, "src": 0 }
  ]
}
```

---

### 厄瓜多

**裁決**：INCLUDE（`route_type` 由前輪隱含之 property_is_route 修正為 **property_one_of_several**；制度名稱亦須修正，不宜稱為「不動產投資人簽證」）

**tier 1 取得狀況**：取得，但透過替代管道。直接 `WebFetch` `cancilleria.gob.ec` 因 SSL 憑證錯誤失敗；改用文字擷取代理 `r.jina.ai` 轉發，成功取得 `gob.ec/mremh`（厄瓜多外交暨人口流動部官方網域）之逐字西班牙文程序頁面內容——**內容本身是官方逐字條文轉述，非第三方摘要改寫**，故仍列為 Tier 1，但如實揭露取得管道非直接連線。

**證據**：
- https://www.gob.ec/mremh/tramites/concesion-visa-residencia-temporal-inversionista （Tier 1，MREMH 官方程序頁，經 r.jina.ai 代理取得）
- https://www.gob.ec/mremh/tramites/concesion-visa-residencia-permanente-tiempo-permanencia-mayor-21-meses （Tier 1，同上）
- https://www.cancilleria.gob.ec/blog/2020/06/16/visa-residencia-temporal/ （Tier 1，官方簽證類別索引）
- 2026 年 SBU＝482 美元／月：Tier 2/3，五個以上獨立網站一致引用 Acuerdo Ministerial MDT-2025-195（aldia.com.ec、concepto.com.ec、ecuadornoticias.com 等），本輪未能讀到該行政命令原文（PDF 下載為損毀檔案，無法解析）

**與前輪的分歧**（重要，須修正站上文案）：
1. **這不是一個專屬的「不動產投資人簽證」**。官方頁面上的正式類別是「Visa de Residencia Temporal – Inversionista」（投資人臨時居留簽證），其下有**四種**可各自單獨達標的合格投資形式：銀行存款證明（≥730 天期、100 SBU）、**不動產**（登記之購售契據、100 SBU）、公司股權（100 SBU）、政府投資合約。不動產只是四選一，非專屬途徑。`route_type` 應為 `property_one_of_several`。
2. 前輪稱查無獨立簽證代碼（如 "9-XI"），本輪同樣未查得——厄瓜多現行制度以類別名稱（"Inversionista"）而非數字代碼組織，前輪與本輪皆未確認舊制數字代碼在 2023 年《人口流動組織法》改制後是否仍沿用。
3. 「轉永久居留」的「連續居留 21 個月」規則是**適用於所有臨時居留類別的一般規則**，非本簽證專屬條款，且要求「實際持續居留」的行為要件——僅持有投資、不實際住在厄瓜多者，無法藉此規則轉永久居留，只能持續續簽 2 年期臨時簽證。

**入庫欄位資料**：

```json
{
  "id": "ecuador",
  "region": "americas",
  "source_file": "visa-round2",
  "flag": "🇪🇨",
  "jurisdiction": "Ecuador",
  "jurisdiction_zh": "厄瓜多",
  "programme": "Investor Temporary Residence Visa — real estate route (Visa de Residencia Temporal – Inversionista, Reglamento a la Ley Orgánica de Movilidad Humana)",
  "programme_zh": "投資人臨時居留簽證——不動產路徑（依《人口流動組織法施行細則》）",
  "label_en": "Investor Visa — real estate route",
  "label_zh": "投資人簽證——不動產路徑",
  "route_type": "property_one_of_several",
  "confidence": "medium",
  "outcome_class": "renewable",
  "established": {
    "threshold": "published",
    "term": "published",
    "stay": "not_established",
    "leads_to": "published"
  },
  "min_value": {
    "amount": 48200,
    "currency": "USD",
    "usd": 48200,
    "basis": "100x Salario Básico Unificado (SBU). Ecuador is dollarised, so the SBU and this threshold are already denominated in USD, not a converted figure. The '100 SBU' rule and the requirement that the deed be registered at the cantonal Property Registry are tier 1 (gob.ec). The 2026 SBU value itself (USD 482/month, per Acuerdo Ministerial MDT-2025-195) rests on five-plus agreeing tier-2/3 sources, not on the primary decree text (attempted fetch returned a corrupted file).",
    "tier": 2,
    "src": 0
  },
  "sort_usd": 48200,
  "term": {
    "text_en": "2 years, renewable, multiple entries permitted, no time limit on stays abroad.",
    "text_zh": "2 年，可續期，多次入境，境外停留天數無上限。",
    "tier": 1,
    "src": 0
  },
  "stay": {
    "text_en": "Not established. No explicit minimum-stay-in-Ecuador requirement was found for maintaining or renewing this temporary visa category itself — distinct from the general 21-month continuous-residence rule needed to CONVERT to permanent residence (see leads_to), which is a behavioral requirement for conversion, not a renewal requirement for the temporary status.",
    "text_zh": "未能確立。本簽證類別本身之續簽╱維持並未見任何明確的境內停留天數要求——這與「轉永久居留」所需之連續 21 個月居留規則（見 leads_to）不同，後者是轉換的行為要件，非臨時身分續簽的條件。",
    "tier": 1,
    "src": 1
  },
  "leads_to": {
    "text_en": "General LOMH rule (applies to any temporary-residence category, not specific to this one): 21 continuous months of ACTUAL temporary residence status permits application for permanent residence. Requires genuine residence behavior, not passive investment-holding — an investor who buys property but does not actually live in Ecuador would not satisfy this and would simply keep renewing the 2-year temporary visa.",
    "text_zh": "《人口流動組織法》一般規則（適用於所有臨時居留類別，非本簽證專屬）：連續 21 個月之「實際」臨時居留身分，即可申請轉永久居留。須有真實居住行為，非被動持有投資即可——僅購置不動產但未實際居住於厄瓜多者，無法滿足此條件，只能持續續簽 2 年期臨時簽證。",
    "tier": 1,
    "src": 1
  },
  "ownership_form": {
    "text_en": "Notarized deed (escritura de compraventa) registered at the cantonal Property Registry (Registro de la Propiedad) — registration is the qualifying event.",
    "text_zh": "已公證之購售契據（escritura de compraventa），須於所在市（canton）之不動產登記處完成登記——登記本身即為達標事件。",
    "tier": 1,
    "src": 0
  },
  "offplan": {
    "text_en": "Not established. The requirement for a deed 'inscrita en el Registro de la Propiedad' structurally implies a completed, titled property; off-plan/pre-construction purchases without a registered deed likely do not qualify, but no source states this exclusion explicitly.",
    "text_zh": "未能確立。「須於不動產登記處登記契據」之要求，結構上隱含須為已完工、已取得產權之物件；未交屋之預售案因無可登記之契據，可能不合格，惟未見任何來源明文排除。",
    "tier": 1,
    "src": 0
  },
  "mortgage": {
    "text_en": "Not established in this pass.",
    "text_zh": "本次查核未查證。",
    "tier": 1,
    "src": 0
  },
  "dependants": {
    "text_en": "Not established in this pass.",
    "text_zh": "本次查核未查證。",
    "tier": 1,
    "src": 0
  },
  "entry_tax": {
    "text_en": "Not established in this pass.",
    "text_zh": "本次查核未查證。",
    "tier": 1,
    "src": 0
  },
  "last_change": {
    "text_en": "Not established in this pass — could not confirm whether the visa category or its real-estate line-item has changed since last amended.",
    "text_zh": "本次查核未查證——未能確認此簽證類別或其不動產條款自上次修訂後有無變動。",
    "tier": 1,
    "src": 0
  },
  "short": {
    "term_en": "2 yrs, renewable",
    "term_zh": "2 年，可續期",
    "stay_en": "None for renewal; 21mo continuous residence needed for permanent conversion",
    "stay_zh": "續簽無天數要求；轉永久居留須連續居留 21 個月",
    "outcome_en": "Permanent residence after 21 continuous months of ACTUAL residence (general rule, behavioural)",
    "outcome_zh": "連續實際居留 21 個月後可轉永久居留（一般規則，須真實居住）",
    "own_en": "One of 4 qualifying investment types (bank deposit / real estate / company equity / govt investment contract); real estate alone satisfies the threshold",
    "own_zh": "為四種合格投資形式之一（銀行存款／不動產／公司股權／政府投資合約）；不動產本身即可單獨達標"
  },
  "notes_en": "IMPORTANT CORRECTION to the round-1 finding: this is NOT a dedicated real-estate investor visa. The official category is a general 'Inversionista' temporary residence visa with FOUR interchangeable qualifying investment types (bank deposit ≥730 days, real estate, company equity, government investment contract), each independently sufficient at 100 SBU. Publishing this as a real-estate-specific visa would misrepresent the underlying legal structure. Application fees: USD 50 + USD 270 issuance (50% discount age 65+, full exemption for ≥30% disability) — tier 1. Requires an apostilled criminal background certificate covering country of origin plus any country resided in during the last 5 years (180-day validity window), plus separate proof of lawful income under Acuerdo Ministerial No. 70 (2024-06-28) layered on top of the investment itself — tier 1.",
  "notes_zh": "對前輪重要修正：這**不是**專屬的不動產投資人簽證。官方類別是一般性「投資人」臨時居留簽證，下設四種可互換的合格投資形式（銀行存款≥730天、不動產、公司股權、政府投資合約），各自獨立達 100 SBU 即可。若站上刊登為「不動產專屬簽證」將誤述其法律結構。申請規費：50 美元＋核發費 270 美元（65 歲以上減免 50%，身心障礙 30% 以上全免）——Tier 1。須提出經公證認證之無犯罪紀錄證明（涵蓋原籍國及過去 5 年內曾居住之任何國家，效期 180 天），另須依 2024 年 6 月 28 日第 70 號部務命令另行證明合法所得來源，此為投資金額之外的獨立要求——Tier 1。",
  "sources": [
    { "url": "https://www.gob.ec/mremh/tramites/concesion-visa-residencia-temporal-inversionista", "publisher": "Ministerio de Relaciones Exteriores y Movilidad Humana (Ecuador)", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://www.gob.ec/mremh/tramites/concesion-visa-residencia-permanente-tiempo-permanencia-mayor-21-meses", "publisher": "Ministerio de Relaciones Exteriores y Movilidad Humana (Ecuador)", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://www.cancilleria.gob.ec/blog/2020/06/16/visa-residencia-temporal/", "publisher": "Cancillería del Ecuador", "tier": 1, "accessed": "2026-08-02" }
  ],
  "companion_requirements": [
    { "text_en": "Passport valid ≥6 months.", "text_zh": "護照效期須 6 個月以上。", "tier": 1, "src": 0 },
    { "text_en": "Apostilled/legalized criminal background certificate covering country of origin and any country resided in during the last 5 years (180-day validity window).", "text_zh": "須提出經公證認證之無犯罪紀錄證明，涵蓋原籍國及過去 5 年內曾居住之任何國家，效期 180 天。", "tier": 1, "src": 0 },
    { "text_en": "Proof of lawful income/source of funds per Acuerdo Ministerial No. 70 (2024-06-28) — a separate funds-legitimacy layer on top of the investment itself.", "text_zh": "須依 2024 年 6 月 28 日第 70 號部務命令另行證明合法所得來源——此為投資金額之外的獨立要求。", "tier": 1, "src": 0 },
    { "text_en": "5x5cm standard-format photo.", "text_zh": "5×5 公分標準規格照片。", "tier": 1, "src": 0 },
    { "text_en": "Application fee USD 50 + issuance fee USD 270 (50% discount age 65+, full exemption for ≥30% disability).", "text_zh": "申請規費 50 美元＋核發費 270 美元（65 歲以上減免 50%，身心障礙 30% 以上全免）。", "tier": 1, "src": 0 },
    { "text_en": "Not established: minimum holding period before resale; health insurance requirement.", "text_zh": "未能確立：轉售前最短持有期間；健康保險要求。", "tier": 1, "src": 0 }
  ]
}
```

---

### 瓜地馬拉

**裁決**：HOLD

**tier 1 取得狀況**：部分取得。本輪成功直接下載並讀取官方 PDF 申請表格本體（`igm.gob.gt/wp-content/uploads/2026/01/10.-Residencia-Temporal-para-inversionistas-1.pdf`，以 `pdftotext -layout` 解析），確認表格真實存在、表格編號 IGM 01-2026、10 萬美元門檻、五項可佐證文件類型、以及頁尾所引法源條號皆與前輪主張完全一致。**但**——`igm.gob.gt` 網站根目錄與「法源」（marco-legal）頁面本輪皆回傳 403（疑似 Cloudflare 機器人阻擋，僅 `/wp-content/uploads/...` 這種直接檔案路徑可通），`congreso.gob.gt`（國會，《移民法典》原文所在地）回傳 403，`web.archive.org` 在本次查核環境中被工具層整體阻擋（非網站本身拒絕，是查證工具本身連不到這個網域）。**《移民法典》第 27、75-77 條，以及 IGM-016-2025、IGM-017-2025 兩號協議的實際條文內容，本輪與前輪皆未能讀到。**

**證據**：
- https://igm.gob.gt/wp-content/uploads/2026/01/10.-Residencia-Temporal-para-inversionistas-1.pdf （Tier 1，官方申請表格本體，確認表格存在與其上列示之內容，但不等於法條原文）
- https://www.consortiumlegal.com （Tier 2，瓜地馬拉╱中美洲執業律師事務所，獨立佐證 10 萬美元門檻與 1-5 年期範圍，但未觸及「Certificaciones registrales」是否涵蓋不動產這個核心問題）
- srp.gob.gt（瓜地馬拉第二不動產登記處官方網站）——Tier 1 事實：確認「registral」「calificación registral」為該國不動產登記處的標準官方用語，用以佐證「Certificaciones registrales」在術語習慣上*可能*指向不動產登記證明，但這是**術語推論**，不是對本項居留制度本身的直接陳述
- livinginguatemala.com（移居╱仲介類部落格，非律師事務所）——明確主張不動產購置合格，但引用的法源（"Art. 48"、"Acuerdo Gubernativo 83-2019"）與官方表格現行引用之法源（第 27、75-77 條、IGM-016-2025）**不一致**，可能是描述已被取代的舊制，可信度存疑，依裁決標準（仲介／代辦網站不可採信）不予採用

**與前輪的分歧**：前輪已誠實標註「未如巴西、厄瓜多般直接點名『不動產』三個字」這個保留意見，本輪認為這個保留意見**才是決定性的**，而非邊際性的。核心問題「Certificaciones registrales」是否確實涵蓋不動產登記證明，本輪嘗試了母法（國會網站 403）、子法規（igm.gob.gt 法源頁 403）、Wayback Machine（工具層阻擋）、以及尋找第二家獨立律師事務所佐證（未找到），全數落空。目前僅有：(1) 一份官方表格的模糊列項，(2) 一個關於瓜地馬拉政府慣用術語的結構性推論，(3) 一個法源引用不一致、屬於仲介類的部落格主張。三者合計未達本資料集「一個 tier 1 或雙重一致 tier 2」的最低刊登門檻——因為 (2) 不是直接陳述本制度，(3) 依規則不可採信，故實質上只有 (1) 這一個薄弱證據獨撐全局。

**入庫欄位資料**：不適用（HOLD，不入庫）。若未來取得《移民法典》第 27、75-77 條或 IGM-016-2025 號協議原文，且原文明確將不動產登記列為合格投資形式之一，則本筆應立即重新評估，且 `route_type` 應設為 `property_one_of_several`（表格上五種佐證文件並列，不動產顯然非唯一途徑），並附上「表格列項＝一種而非全部，法源仍待完整條文核對」的警語。

---

### 巴拉圭

**裁決**：INCLUDE_WITH_CAVEAT（`confidence: medium`）

**tier 1 取得狀況**：取得官方發布頁，但未取得決議原文。直接開啟並讀取兩個官方網域的公告頁——工商部（MIC）與移民總局（Migraciones）——內容一致確認制度存在、決議字號、20 萬美元門檻、不動產可單獨達標。另找到 2026 年 7 月 2 日總統向國會提交之施政報告頁面，其中提及第 0283/2026 號決議為已施行政策。**但**：Gaceta Oficial（憲報）上決議本文之原始文字，本輪與前輪皆未能取得（`gacetaoficial.gov.py` 逾時，站內搜尋查無結果）；SUACE（此制度指定之單一窗口受理機關）官網站內搜尋「Investor Pass」查無任何結果，未見申請入口網、表單、規費表。

**證據**：
- https://www.mic.gov.py/mic-y-migraciones-lanzan-el-paraguay-investor-pass-para-facilitar-la-residencia-permanente-a-inversionistas-extranjeros/ （Tier 1 官方網域，公告頁，非決議原文）
- https://migraciones.gov.py/paraguay-investor-pass-nueva-herramienta-para-facilitar-la-inversion-extranjera-en-el-pais/ （同上）
- https://migraciones.gov.py/informe-presidencial-resalta-cifras-historicas-en-residencias-aumento-del-flujo-migratorio-y-avances-en-gestion-de-fronteras/ （Tier 1 官方網域，總統施政報告頁，佐證制度已施行但無具體申請數據）

**與前輪的分歧（重要，多處需修正）**：
1. **時序錯誤**：前輪稱此制度「約在資料集彙編日期前一週上線」，本輪查得官方公告日期為 2026 年 4 月 17 日（MIC）與 4 月 21 日（Migraciones）——距彙編日期（2026-08-01）**約 3.5 個月**，不是一週，前輪這個時效性主張需訂正。
2. **「十年永久居留」這個數字查無依據**：本輪窮盡官方頁面與 Tier 2/3 來源，**任何層級都找不到「10 年」這個具體數字的出處**——連仲介╱行銷類網站都沒有明確引註來源。極可能是與別的制度（例如某種身分卡續卡週期）混淆或前輪誤植。**建議站上不要刊登「10 年」這個數字**，若要描述期限只能寫「未能確立」。
3. 「直接永久居留、免臨時居留階段」這個結構性主張**本輪獨立查證後認為可信**（不是誤讀）：巴拉圭移民總局官網本身列出的「直接授予永久居留」類別中，本就已有一項「外國投資人永久居留」（Residencia Permanente para Inversionistas Extranjeros，經 SUACE），且查得 2025 年 9 月即有與南韓使館協調「外國投資人落籍」事宜的舊聞，顯示這不是一個全新發明的法律機制，而是既有直接永久居留類別的擴大╱改版。
4. **`route_type` 應為 property_one_of_several**：不動產與證券（亞松森證交所）為兩個各自可達標的選項，同一 20 萬美元門檻，非必須混合投資；另有一個 15 萬美元的觀光業專案投資選項（與不動產無關），以及一個未經證實是否屬於同一決議的 7 萬美元＋僱用 5 名當地員工的「生產性企業」選項（僅見於仲介來源，不予採用）。
5. **實際受理狀況存疑**：官方公告與總統施政報告本身足以證實制度「存在」且政府視為已施行政策，但沒有任何官方管道公布申請表單、規費、處理時程，SUACE 官網搜尋掛零——這與「已公告」和「已實際可申辦」是兩件不同的事，站上刊登時應明確區分，不宜呈現為已完全可操作的流程。

**入庫欄位資料**：

```json
{
  "id": "paraguay",
  "region": "americas",
  "source_file": "visa-round2",
  "flag": "🇵🇾",
  "jurisdiction": "Paraguay",
  "jurisdiction_zh": "巴拉圭",
  "programme": "Paraguay Investor Pass — direct permanent residence for foreign investors (Resolución 0283/2026, under Ley de Migraciones 6984/22)",
  "programme_zh": "巴拉圭投資人通行證——外國投資人直接永久居留（2026 年第 0283 號決議，框架法源《移民法》6984/22 號）",
  "label_en": "Paraguay Investor Pass",
  "label_zh": "巴拉圭投資人通行證",
  "route_type": "property_one_of_several",
  "confidence": "medium",
  "outcome_class": "permanent",
  "established": {
    "threshold": "published",
    "term": "not_established",
    "stay": "not_established",
    "leads_to": "published"
  },
  "min_value": {
    "amount": 200000,
    "currency": "USD",
    "usd": 200000,
    "basis": "Urban real estate investment OR Asunción Stock Exchange securities — two separate stand-alone options at the same USD 200,000 threshold, not required to be blended; real estate alone satisfies the full amount (confirmed on MIC's official page). A separate USD 150,000 tourism-sector-project track exists under the same announcement. A possibly-related USD 70,000 + 5-local-jobs 'productive enterprise' SUACE track was mentioned only by marketing sources — NOT confirmed at tier 1/2 as part of this same resolution, do not conflate.",
    "tier": 1,
    "src": 0
  },
  "sort_usd": 200000,
  "term": {
    "text_en": "NOT ESTABLISHED. The commonly repeated '10-year' duration claim could not be confirmed at any tier — not on official government pages, and not even in marketing/agency material with a traceable citation. Do not publish '10 years' as fact; state the term as unconfirmed.",
    "text_zh": "未能確立。坊間常見的「10 年」年限說法，本輪在任何層級（官方或坊間）都找不到可追溯的出處，不應刊登為事實；期限應標註為未能確立。",
    "tier": 1,
    "src": 0
  },
  "stay": {
    "text_en": "Not established. A marketing-only source claims a return-to-Paraguay-every-3-years maintenance requirement; not corroborated at tier 1 or 2 — do not publish.",
    "text_zh": "未能確立。僅有一個仲介類來源主張「每 3 年須返回巴拉圭一次」以維持身分，未獲 Tier 1 或 Tier 2 佐證，不應刊登。",
    "tier": 1,
    "src": 0
  },
  "leads_to": {
    "text_en": "Direct permanent residence (Residencia Permanente para Inversionistas Extranjeros, via the SUACE single-window channel), no prior temporary-residence stage required — confirmed via two independent official government pages (MIC and Migraciones), and structurally consistent with Migraciones' own listed direct-to-permanent categories, which already included an investor category before the April 2026 relaunch. The Investor Pass appears to be a reform/expansion of a pre-existing direct-to-permanent investor category, not a wholly new legal mechanism.",
    "text_zh": "直接授予永久居留（外國投資人永久居留，經 SUACE 單一窗口辦理），免臨時居留階段——經 MIC 與 Migraciones 兩個獨立官方網域確認，且與移民總局官網本身列出之「直接授予永久居留」類別架構一致，該類別在 2026 年 4 月改版前即已存在投資人選項。「投資人通行證」看起來是既有直接永久居留投資人類別之改版╱擴大，而非全新的法律機制。",
    "tier": 1,
    "src": 0
  },
  "ownership_form": {
    "text_en": "Urban real estate (per MIC's official page); no further detail on completed-vs-off-plan or title requirements confirmed at tier 1/2.",
    "text_zh": "都市不動產（依 MIC 官方頁面）；已完工與預售之區分、產權要求等細節，本輪未能於 Tier 1／2 確認。",
    "tier": 1,
    "src": 0
  },
  "offplan": {
    "text_en": "Not established at tier 1/2. One marketing source claims off-plan ('en pozo') purchases qualify with a 30%-down/USD 60,000-deposit structure — unconfirmed, do not publish as fact.",
    "text_zh": "Tier 1／2 未能確立。僅一個仲介類來源主張預售（「en pozo」）合格，並描述 30% 頭期／6 萬美元訂金之結構——未經證實，不應刊登為事實。",
    "tier": 1,
    "src": 0
  },
  "mortgage": {
    "text_en": "Not established in this pass.",
    "text_zh": "本次查核未查證。",
    "tier": 1,
    "src": 0
  },
  "dependants": {
    "text_en": "Not established in this pass.",
    "text_zh": "本次查核未查證。",
    "tier": 1,
    "src": 0
  },
  "entry_tax": {
    "text_en": "Not established in this pass.",
    "text_zh": "本次查核未查證。",
    "tier": 1,
    "src": 0
  },
  "last_change": {
    "text_en": "Program launched via official announcements dated 2026-04-17 (MIC) and 2026-04-21 (Migraciones) — NOT within days of this dataset's 2026-08-01 compile date as first claimed; the launch was roughly 3.5 months earlier. A 2026-07-02 presidential report to Congress references Resolución 0283/2026 as implemented policy 11 weeks post-launch, but gives no application/approval statistics specific to this program. SUACE's own site (the designated single-window intake channel) returns zero search results for 'Investor Pass' — operational maturity (live application portal, fee schedule, published forms) could not be confirmed either way.",
    "text_zh": "制度經官方公告上線，日期為 2026-04-17（MIC）與 2026-04-21（Migraciones）——並非彙編日期前一週，而是約 3.5 個月前，前一輪之時效性主張有誤。2026-07-02 總統向國會提交之施政報告，於上線 11 週後仍將第 0283/2026 號決議列為已施行政策，惟未提供本制度專屬之申請╱核准統計數字。SUACE（本制度指定之單一窗口受理機關）官網站內搜尋「Investor Pass」查無任何結果——實際受理成熟度（申請入口網、規費表、公告表單）本輪無法從正反兩面確認。",
    "tier": 1,
    "src": 0
  },
  "short": {
    "term_en": "Not established (avoid stating '10 years')",
    "term_zh": "未確立（避免刊登「10 年」）",
    "stay_en": "Not established",
    "stay_zh": "未確立",
    "outcome_en": "Direct permanent residence, no temporary stage",
    "outcome_zh": "直接永久居留，免臨時居留階段",
    "own_en": "Real estate OR securities, same USD 200,000 threshold; real estate alone suffices",
    "own_zh": "不動產或證券擇一，門檻皆為 20 萬美元；不動產本身即可單獨達標"
  },
  "notes_en": "Newly relaunched program (April 2026) built on a pre-existing direct-to-permanent investor residence category, not a novel mechanism — but operational maturity is unconfirmed: no fee schedule, application portal, or published forms found on any official domain, and the designated SUACE intake channel's own site search returns nothing for this program. The raw resolution text (Gaceta Oficial) was not reached in either round — sourcing rests on official government ANNOUNCEMENT pages, not the primary legal instrument. Drop the '10-year' duration claim entirely pending confirmation. A marketing-only, unconfirmed claim that owner-occupied residences do NOT qualify (investment/rental property only) should be flagged prominently if published at all, not stated as fact.",
  "notes_zh": "本制度為 2026 年 4 月新上線之改版，建立在既有的「直接永久居留投資人」類別之上，非全新機制——惟實際受理成熟度未經確認：所有官方網域均查無規費表、申請入口網或公告表單，指定受理窗口 SUACE 官網站內搜尋本制度亦查無結果。決議原文（憲報）兩輪皆未能取得——現有佐證僅止於官方「公告」頁面，非法規原文本身。「10 年」年限主張應完全撤除，待日後確認。另有一個僅見於仲介來源、未經證實的主張——自住不合格（限投資╱出租用不動產）——若要刊登應顯著標註為未經證實，不應陳述為事實。",
  "sources": [
    { "url": "https://www.mic.gov.py/mic-y-migraciones-lanzan-el-paraguay-investor-pass-para-facilitar-la-residencia-permanente-a-inversionistas-extranjeros/", "publisher": "Ministerio de Industria y Comercio (Paraguay)", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://migraciones.gov.py/paraguay-investor-pass-nueva-herramienta-para-facilitar-la-inversion-extranjera-en-el-pais/", "publisher": "Dirección General de Migraciones (Paraguay)", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://migraciones.gov.py/informe-presidencial-resalta-cifras-historicas-en-residencias-aumento-del-flujo-migratorio-y-avances-en-gestion-de-fronteras/", "publisher": "Dirección General de Migraciones (Paraguay)", "tier": 1, "accessed": "2026-08-02" }
  ],
  "companion_requirements": [
    { "text_en": "Not established at tier 1/2: source-of-funds documentation, criminal background check, minimum holding period, application fees — all mentioned only by marketing/agency sources, not confirmed on official pages.", "text_zh": "Tier 1／2 未能確立：資金來源文件、無犯罪紀錄查核、最短持有期間、申請規費——僅見於仲介╱代辦來源，官方頁面未確認。", "tier": 1, "src": 0 },
    { "text_en": "Possible restriction (UNCONFIRMED, marketing-only source): owner-occupied residences may NOT qualify — investment/rental property only. Flag prominently as unconfirmed if published at all; do not state as fact.", "text_zh": "可能限制（未經證實，僅見於仲介來源）：自住物業可能不合格——限投資╱出租用不動產。若要刊登應顯著標註未經證實，不應陳述為事實。", "tier": 1, "src": 0 }
  ]
}
```

---

### 保加利亞

**裁決**：HOLD——**維持現行「無途徑」之否定結論，不翻轉入庫，但強烈建議在現行文案加註警語**。

**tier 1 取得狀況**：仍未攻下。母法《外國人法》（ЗЧРБ）第 24 條第 1 項第 19 款本身的條文全文，本輪與前輪皆未有任何人直接讀到——`lex.bg` 對兩個文件 ID 的請求均回傳 403（含前輪已用過的 curl 直連方式，本輪重試同樣失敗）；`web.archive.org` 在本次查證工具環境中被**工具層本身**整體阻擋（不是網站拒絕存取，是查證工具回報「無法對 web.archive.org 發出請求」），使得 Wayback Machine 這條路徑本輪完全無法嘗試，這點應回報給查證工具的維護方。

本輪改而在 `apis.bg` 的子網域（`legislation.apis.bg`，成功，非前輪失敗過的 `apis.bg/p.php` 路徑）與國會官方公報網域 `dv.parliament.bg` 上，取得**下位規範**（《外國人法施行細則》第 29a 條）的條文內容，明確引用「依據《外國人法》第 24 條第 1 項第 19 款取得延展居留權」，並列出 60 萬列弗、持牌銀行資金到位證明、借款不得超過投資總額 25% 等具體機制細節。但：(1) 這是**施行細則**，不是母法第 24 條第 1 項第 19 款本身的文字；(2) `dv.parliament.bg` 對同一 URL 兩次請求，一次回傳空白、一次回傳完整內容，取得過程本身不穩定，難以視為與直接讀取原始 HTML 逐字核對同等可靠。

**證據**：
- https://legislation.apis.bg/doc/484342/0 （APIS，保加利亞主要商業法律資料庫，接近 Tier 1 但非官方公報本身；引用施行細則第 29a 條）
- https://dv.parliament.bg/DVWeb/showMaterialDV.jsp?idMat=81454 （保加利亞國會官方公報網域，但兩次請求結果不一致，可靠度打折）
- 13 個獨立 Tier 2 來源（含 5 個此前已知＋8 個本輪新增，多家為保加利亞文執業律師事務所，非英文行銷網站）：legex.bg、legalita.bg（自稱「Адвокатско дружество」律師事務所）、advokat-toncheva.com、advokatavramov.com、vakarelova.com、advokatshulev.com 等，條號（第 24 條第 1 項第 19 款）與金額（60 萬列弗）完全一致，零矛盾

**與前輪的分歧**：前輪已將此列為「本輪最關鍵發現」並建議「立即加註警語」，但也同樣承認未達 Tier 1。本輪的任務是**專門再試一次攻頂 Tier 1**——結果是把 Tier 2 證據從 3 個擴充到 13 個、且多出一份接近 Tier 1 的下位規範條文，但仍未讀到母法本身，且僅有的「接近 Tier 1」證據本身有一次不穩定重現的瑕疵。**依照本次任務裁決標準明文規定的例外規則**——保加利亞這一筆的性質是「翻轉一個已經在網站上公開刊登的否定結論」，門檻高於「新增一筆此前完全未刊登的候選」——「如果真的攻不下 tier 1，就照實裁決為加警語但不翻轉結論」。本輪judgment認為，即使 Tier 2 證據量與品質都已顯著優於前輪，仍應遵守這個預先寫死的例外規則，不擴大解釋為「證據夠多所以等同於 Tier 1」。

**入庫欄位資料**：不適用（HOLD，不翻轉、不入庫）。

**建議站上文案處理方式**：現行「保加利亞：不動產無法取得居留權」這類絕對表述的否定結論**不應繼續維持零保留的絕對語氣**，應在該筆旁加註類似以下但書（供文案人員參考，非直接可刊登之定稿）：

> 查證中：保加利亞《外國人法》第 24 條第 1 項第 19 款可能另設「延展居留」（非永久居留）之不動產購置門檻（約 60 萬列弗／30 萬歐元），多個獨立保加利亞文法律專業來源一致引用同一條號與金額，但截至最近一次查核（2026-08-02）仍未取得該條文之官方一手文字，故本站尚未將其列為現行制度。

若日後任何人成功打開 `lex.bg` 或取得 Wayback Machine 快照讀到第 24 條第 1 項第 19 款原文，應立即重新評估並比照本報告中巴西／厄瓜多的規格建檔，`route_type` 建議為 `property_is_route`（購置不動產或收購持有該不動產之公司股權，是同一件事的兩種結構方式，非不相關的另一投資選項）。

---

## 附：本輪對五組 subagent 建議的收斂調整

- 巴西、厄瓜多：基本採納 subagent 建議（INCLUDE），僅在欄位措辭與 `route_type`／`outcome_class` 上依現有資料集慣例（參照 `panama`、`greece` 等既有 entry 的欄位風格）做了規格化。
- 瓜地馬拉：subagent 本身建議即為 HOLD，本報告完全採納，並補充「三項證據合計仍不足」的量化說明。
- 巴拉圭：subagent 建議 INCLUDE_WITH_CAVEAT，本報告採納，但額外**強制刪除「10 年」這個查無依據的數字**（subagent 報告中雖已建議「不確定就別發表」，本報告把這點從「建議」提升為入庫 JSON 草稿中的明確 `not_established` 標記，避免後續編輯者疏忽帶入）。
- 保加利亞：subagent 建議 INCLUDE_WITH_CAVEAT（「建議從 HOLD 升級」），**本報告未採納這個升級建議**，改為嚴格套用任務指示中「攻不下 tier 1 就不翻轉既有否定結論」的明文例外規則——這是本報告與其中一組 subagent 建議唯一的實質分歧之處，特此標明供覆核者留意。

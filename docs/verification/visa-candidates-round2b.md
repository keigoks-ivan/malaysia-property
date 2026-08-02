# 候選制度第二輪複核（2b：沙烏地阿拉伯／埃及）

複核日期：2026-08-02 ｜ 對照 `docs/verification/visa-coverage-gaps.md`「二、DuckDuckGo 時期條目複核」段落（前輪，2026-08-02 同日稍早）

方法：兩組獨立 subagent 各自重查一筆（皆使用完整 WebSearch／WebFetch／瀏覽器能力，且皆在任務開始前即撞上 WebSearch 額度已用罄，改用替代管道，詳見各自「方法備註」），本文為彙整者對兩份報告的最終裁決——非直接照搬 agent 建議。彙整者本身未額外執行獨立查證動作（未重覆開啟來源 URL），裁決係基於批判性覆核兩份報告的證據鏈、追查其引用是否確實達到宣稱的 tier、並比對是否有未解決的矛盾或推論跳躍。**本報告未修改 `data/visa-property.json` 或 `global/visa.html`，僅供另一組正在編輯 JSON 的 agent 參考。**

---

## 裁決總表

| 法域 | 前輪主張 | 本輪裁決 | tier 1 攻克程度 | 理由一句話 |
|---|---|---|---|---|
| 🇸🇦 沙烏地阿拉伯 | 不動產持有人優質居留，門檻 SAR 400 萬，僅可續期永不轉永久 | **INCLUDE**（`confidence: high`） | **完全攻克**——直接以瀏覽器讀取官方站四份文件全文（產品頁、母法、實施條例、不動產專屬詳細條件文件），非透過摘要或代理 | 門檻、`property_is_route`、「僅可續期永不轉永久」（§7.2 明文「不適用」）、麥加／麥地那地理排除、現金限定、90 天替換規則，全部由官方一手文件逐字確認；唯二修正——Art. 4(8) 是五項自由裁量產品共用的授權條款而非不動產專屬、撤銷事由是九項不是六項 |
| 🇪🇬 埃及 | 購屋入籍，門檻 30 萬美元，法源 876/2023＋3562/2023 兩號總理令，五年處分鎖定 | **INCLUDE**（`confidence: medium-high`，`route_type` 修正為 **property_one_of_several**） | **核心事實攻克**——直接下載並讀取三份官方公報 PDF 掃描全文（3099/2019、876/2023、28/2023）＋ GAFI 官方頁（英／阿文雙版），但兩個次要欄位仍有未解決之處 | 入籍（非居留）此一最關鍵主張由 GAFI 官方頁英阿雙語逐字確認；但「3562/2023」號令查無此文號，實際刪除「限國有物業」限制的法源是**第 28/2023 號法律**（母法修正，非總理令）——前輪文號有誤；「五年不得處分」實為附條件保留條款（提前售出仍可保留公民權，但須另存 25 萬美元），非絕對禁止處分；本輪未取得任何 tier 2 次級來源交叉佐證（搜尋工具本身失能，非查無來源） |

**「47 套」→ 建議改為 49 套**（沙烏地阿拉伯、埃及各計入一套）。

---

## 逐筆

### 沙烏地阿拉伯

**裁決**：**INCLUDE**（`confidence: high`）

**tier 1 取得狀況**：完全攻克，且取得方式值得記錄——`pr.gov.sa` 是純前端 JS 單頁應用，`curl`／`WebFetch` 直連只會拿到空殼，本輪改用瀏覽器（`claude-in-chrome`）**現場點擊展開並逐字讀取**四份官方文件全文：不動產持有人居留產品頁、《優質居留許可法》（Royal Decree No. M/106）全文、其實施條例全文、以及「不動產持有人居留詳細條件與要求」文件全文。四份文件皆為 `pr.gov.sa` 官方網域，非摘要、非仲介轉述。

**證據**：
- https://pr.gov.sa/pr?id=pr_product_details_real_estate_owner （Tier 1，官方產品頁）——門檻 SAR 4,000,000，Category 1（既有物業）／Category 2（期房）二分，規費 SAR 4,000
- https://pr.gov.sa/pr?id=premium_residency_permit_law （Tier 1，母法全文）——第 2 條第 1 項：優質居留持有人得於「麥加、麥地那兩市及邊境地區以外」持有不動產；同項並列麥加／麥地那境內得以公證用益權契約持有不動產最長 99 年（所有權不可，僅用益權可）
- https://pr.gov.sa/pr?id=premium_residency_regulations （Tier 1，實施條例全文）——第 3 條列舉七項優質居留產品（永久／可續期一年／特殊人才／傑出人士／投資人／企業家／不動產）；第 4 條第 7 項逐一列出各產品之特殊資格條件，**唯獨不動產產品完全沒有任何「轉永久居留」條款**（其餘四項自由裁量產品皆有明文轉永久條款，或直接授予永久身分）；第 6 條規費對照表列出七項產品規費（永久 SAR 800,000／可續期一年 SAR 100,000／五項自由裁量產品含不動產皆為 SAR 4,000）
- https://pr.gov.sa/pr?id=conditions_controls （Tier 1，不動產持有人專屬「詳細條件與要求」文件全文，共 12 節）——第 3 節：資格條件與配套 KYC 要求；**第 7.1 節「不動產居留產品之續期條件」＝「不適用」；第 7.2 節「取得不動產居留產品之永久優質居留許可之條件」＝「不適用」**（逐字，非改寫）；第 9 節：產品轉換；第 10 節：出售後 90 天內須替換物件，否則許可撤銷；第 11 節：**九項**（非六項）撤銷事由 a–i
- https://www.ey.com/en_gl/technical/tax-alerts/saudi-arabia-approves-new-real-estate-ownership-law-by-non-saudis （Tier 2，安永全球稅務快訊）——確認 2025 年 7 月 25 日頒布之《非沙國籍人士不動產所有權法》（Royal Decree No. M/14），180 天後生效（即 2026 年 1 月底左右已生效），取代 2000 年舊法，由部長會議／REGA 指定得持有區域；麥加／麥地那僅限穆斯林自然人依特別條件持有。此為**另一套規範「外國人能否持有不動產本身」的一般性法律**，與本居留產品是各自獨立的法律工具（前者是持有資格的前提，後者是持有後換居留的機制），本輪查證兩者互不牴觸，且今日（2026-08）仍在線的官方居留產品頁仍列 SAR 4,000,000 門檻，未見金額因新法而調整

**與前輪的分歧**：
1. **Art. 4(8) 的引用性質須修正**。前輪引用「Implementing Regulations 第 4(8) 條」作為不動產產品的專屬法源，本輪交叉核對「特殊人才」產品自己的詳細條件文件，發現該文件**引用的也是同一個「Art. 4(8)」**——第 4 條第 8 項其實是「授權中心為五項自由裁量產品各自發布詳細條件文件」這個**共用授權條款**，不是不動產專屬的實體規則條款。這不影響門檻與規則本身的真實性，但站上文案若寫「依 Art. 4(8) 規定不動產門檻為 400 萬」會造成誤導，應改寫為「依 Art. 4(8) 授權發布之《不動產持有人居留詳細條件與要求》文件第 3 節規定」。
2. **「僅可續期，永不轉永久」得到比前輪更明確的字面確認**，但續期機制本身的細節仍不完全清楚——第 7.1 節「續期條件＝不適用」與第 7.2 節「永久轉換條件＝不適用」並列，可能代表這個產品根本沒有像「可續期居留」（獨立的一年期產品）那樣的定期續期程序，而是**只要持續持有合格不動產，許可即持續有效**（出售後 90 天內須替換，期房須 5 年內完成過戶，否則撤銷）——這是本輪基於條文結構的合理推論，但沒有一份文件明講「本許可無到期日、持續有效」這句話，站上文案應避免對續期機制本身寫得過於篤定，聚焦在「明文排除轉永久」這個已證實的核心事實即可。
3. **撤銷事由修正為九項（a–i），非前輪所稱六項**：刑事定罪、驅逐令、申請資訊不實、未遵守法規、自願放棄、死亡或喪失行為能力、出售後未於 90 天內替換、期房未於 5 年內完成過戶或未及時更換合約、理事會基於公共利益終止。
4. **地理限制確認於母法層級**（非僅實施條例），且細節比前輪更精確：麥加／麥地那兩市＋邊境地區排除**所有權**；麥加／麥地那境內另有一條獨立機制允許**用益權**（非所有權）最長 99 年。

**入庫欄位資料**：

```json
{
  "id": "saudi-arabia",
  "region": "meaf",
  "source_file": "visa-round2b",
  "flag": "🇸🇦",
  "jurisdiction": "Saudi Arabia",
  "jurisdiction_zh": "沙烏地阿拉伯",
  "programme": "Real Estate Owner Residency, one of seven Premium Residency products (Premium Residency Permit Law, Royal Decree No. M/106, and its Implementing Regulations Art. 3–4)",
  "programme_zh": "不動產持有人居留——優質居留制度七項產品之一（《優質居留許可法》Royal Decree No. M/106 及其實施條例第 3–4 條）",
  "label_en": "Real Estate Owner Residency",
  "label_zh": "不動產持有人居留",
  "route_type": "property_is_route",
  "confidence": "high",
  "outcome_class": "renewable",
  "established": {
    "threshold": "published",
    "term": "published",
    "stay": "absent_verified",
    "leads_to": "absent_verified"
  },
  "min_value": {
    "amount": 4000000,
    "currency": "SAR",
    "usd": 1066667,
    "basis": "Category 1 — full ownership or usufruct of an existing residential property (not land), unmortgaged. Category 2 — off-plan purchase at the same threshold, plus a deposit of not less than SAR 1,000,000 or 10% of the price (whichever is higher), developer must be REGA-approved. SAR pegged to USD at 3.75 (long-standing peg, not a floating-rate conversion). One-time fee SAR 4,000 for either category.",
    "tier": 1,
    "src": 0
  },
  "sort_usd": 1066667,
  "term": {
    "text_en": "No standard fixed-term/renewal cycle is documented for this specific product, distinct from the separate one-year 'Renewable Residency' product. The governing document's own 'Term' section states renewal conditions are 'Not applicable' (§7.1) — read together with §10/§11, the permit's validity appears tied continuously to maintaining the qualifying ownership: if the property is sold, it must be replaced within 90 days, and an off-plan purchase must complete (title transfer) within 5 years — failing either triggers revocation. Whether a separate periodic renewal application is additionally required beyond maintaining ownership is not stated either way.",
    "text_zh": "本產品未見標準的固定期限／續期週期規定，與另一項獨立的一年期「可續期居留」產品不同。治理文件本身「期限」一節載明續期條件「不適用」（第 7.1 節）——與第 10、11 節合看，許可效力似與持續持有合格不動產綁定：出售物件須於 90 天內替換，期房須於 5 年內完成過戶，未達成任一項即撤銷許可。除持續持有外，是否另需定期申請續期程序，兩種說法皆未見明文。",
    "tier": 1,
    "src": 3
  },
  "stay": {
    "text_en": "No minimum physical presence in the Kingdom requirement found anywhere in the governing documents (Law, Regulations, or the product's own Detailed Conditions) — internally consistent with there being no permanent-conversion pathway to build toward (contrast Special Talent/Gifted products, which require 30 months' cumulative presence specifically to convert to permanent residency).",
    "text_zh": "母法、實施條例、本產品專屬詳細條件文件，皆未見任何境內最低停留天數要求——與本產品無轉永久居留路徑一事內部一致（相對照，特殊人才／傑出人士產品要求累計 30 個月停留以轉換為永久居留）。",
    "tier": 1,
    "src": 3
  },
  "leads_to": {
    "text_en": "Explicitly and categorically excluded from converting to permanent residency. The product's Detailed Conditions document §7.2 ('Conditions for Obtaining the Permanent Premium Residency Permit for the Real Estate Owner Residency') states verbatim 'Not applicable' — not a partial exemption, an outright absence of any permanent-conversion pathway. Structurally corroborated: Implementing Regulations Art. 4(7) gives every one of the other four discretionary products (Special Talent, Gifted, Investor, Entrepreneur) an explicit permanent-conversion clause or grants permanent status outright; Real Estate alone has none.",
    "text_zh": "明文且絕對地排除轉換為永久居留。本產品「詳細條件與要求」文件第 7.2 節（「取得不動產居留產品之永久優質居留許可之條件」）逐字載明「不適用」——不是部分豁免，是完全沒有轉永久居留的路徑。結構上亦互相印證：實施條例第 4 條第 7 項為其餘四項自由裁量產品（特殊人才、傑出人士、投資人、企業家）逐一列出明確的轉永久條款或直接授予永久身分，唯獨不動產產品沒有。",
    "tier": 1,
    "src": 3
  },
  "ownership_form": {
    "text_en": "Full ownership or usufruct right over a completed residential property (land does not qualify), unmortgaged before and after acquisition, located anywhere in the Kingdom except the cities of Mecca and Medina and designated border areas (Premium Residency Permit Law Art. 2(1)). Within Mecca/Medina, a separate mechanism permits usufruct — not ownership — for up to 99 years via a notarized deed. If sold, must be replaced with another qualifying property within 90 days or the permit is revoked.",
    "text_zh": "須為已完工住宅不動產之完整所有權或用益權（土地不合格），取得前後皆不得有抵押，物件須位於王國境內、麥加與麥地那兩市及指定邊境地區以外（《優質居留許可法》第 2 條第 1 項）。麥加／麥地那境內另有獨立機制，允許以公證用益權契約持有（非所有權）最長 99 年。出售物件須於 90 天內替換為另一合格物件，否則許可撤銷。",
    "tier": 1,
    "src": 2
  },
  "offplan": {
    "text_en": "Qualifies (Category 2), at the same SAR 4,000,000 threshold. Requires: a deposit of not less than SAR 1,000,000 or 10% of the purchase price (whichever is higher); the developer must be REGA-approved; the purchase must complete (full title transfer) within 5 years, or the permit is revoked.",
    "text_zh": "合格（Category 2），門檻與既有物業相同，皆為 SAR 4,000,000。須：訂金不低於 SAR 1,000,000 或房價 10%（取高者）；開發商須經 REGA 核准；須於 5 年內完成過戶，否則許可撤銷。",
    "tier": 1,
    "src": 0
  },
  "mortgage": {
    "text_en": "Cash only, both categories. Existing-property route: property 'shall not be mortgaged and shall not be mortgaged thereafter.' Off-plan route: 'shall not be purchased through mortgage financing... shall not be mortgaged after transfer of ownership.' No financing is permitted at any point in either category.",
    "text_zh": "兩類皆限現金，不得融資。既有物業路徑：「取得前不得有抵押，取得後亦不得抵押」。期房路徑：「不得以貸款融資方式購入……過戶後亦不得抵押」。兩類在任何時點皆不得使用融資／貸款。",
    "tier": 1,
    "src": 3
  },
  "dependants": {
    "text_en": "Covered under the Premium Residency system's standard 'Family' definition applicable to all seven products: spouse, children under 25, and non-working parents. This is a general system-wide rule, not real-estate-specific — no product-specific variation was found.",
    "text_zh": "適用優質居留制度七項產品共用之「家庭」定義：配偶、25 歲以下子女、無業父母。此為制度層級之一般規則，非不動產產品專屬——未見任何產品別差異。",
    "tier": 1,
    "src": 2
  },
  "entry_tax": {
    "text_en": "Not established in this pass. The general Real Estate Transaction Tax (RETT, 5% on most transfers) and its interaction with foreign Premium Residency purchasers specifically was not checked this round.",
    "text_zh": "本次查核未查證。一般性不動產交易稅（RETT，多數過戶適用 5%）及其與外籍優質居留購屋者之互動，本輪未查核。",
    "tier": 1,
    "src": 0
  },
  "last_change": {
    "text_en": "A separate general foreign-ownership law — Royal Decree No. M/14 ('Real Estate Ownership Law by Non-Saudis'), published 25 July 2025, in force roughly 180 days later (≈late January 2026, i.e. currently in force) — repeals the 2000-era foreign-ownership law and lets non-Saudis own real estate in zones to be designated by the Council of Ministers/REGA (Mecca/Medina restricted to Muslim natural persons under special conditions). This is a DIFFERENT legal instrument governing whether a foreigner may own the underlying asset at all, not the Premium Residency law itself, and the live product page (checked 2026-08) still shows the SAR 4,000,000 residency threshold unchanged.",
    "text_zh": "另有一套與本居留產品不同的一般性外籍人士不動產所有權法——Royal Decree No. M/14（《非沙國籍人士不動產所有權法》），2025 年 7 月 25 日頒布，約 180 天後生效（即約 2026 年 1 月底，現已生效），取代 2000 年舊法，允許非沙國籍人士於部長會議／REGA 指定區域持有不動產（麥加／麥地那僅限穆斯林自然人依特別條件）。此為規範「外國人能否持有標的資產」之獨立法律工具，非優質居留法本身；本輪查核當下（2026-08）產品頁 SAR 4,000,000 門檻仍維持不變。",
    "tier": 1,
    "src": 4
  },
  "short": {
    "term_en": "Tied continuously to ownership; no defined renewal cycle documented",
    "term_zh": "與持有物件持續綁定；未見明確續期週期規定",
    "stay_en": "None",
    "stay_zh": "無",
    "outcome_en": "Renewable only — permanent conversion explicitly \"Not applicable\"",
    "outcome_zh": "僅可續期——永久居留條款明文「不適用」",
    "own_en": "Existing property (cash, unmortgaged) or off-plan (REGA-approved developer, ≥10%/SAR 1M deposit); replace within 90 days if sold, complete off-plan within 5 years",
    "own_zh": "既有物業（現金，不得抵押）或期房（開發商須經 REGA 核准，訂金≥10%或 SAR 100 萬）；出售須 90 天內替換，期房須 5 年內完成過戶"
  },
  "notes_en": "Correction to a prior verification round's citation: Implementing Regulations Art. 4(8) is the general empowering clause shared by all five discretionary Premium Residency products (confirmed by cross-checking the Special Talent product's own Detailed Conditions document, which cites the identical article for itself) — it is not a real-estate-specific substantive rule; the substantive SAR 4,000,000 rule lives in the product's own Detailed Conditions document. Revocation grounds are nine (a-i), not six as previously stated. The programme is one of seven Premium Residency products (Permanent; Renewable one-year; Special Talent; Gifted; Investor at SAR 7,000,000 in 'investment activities' — a separate product; Entrepreneur; Real Estate) — real estate ownership alone, at or above SAR 4,000,000, is sufficient and complete for this specific product, with no alternative qualifying assets bundled into it.",
  "notes_zh": "修正前一輪查證之引用：實施條例第 4 條第 8 項是五項自由裁量優質居留產品共用之授權條款（經交叉核對「特殊人才」產品自身之詳細條件文件、引用同一條號證實），非不動產專屬之實體規則；SAR 4,000,000 之實體規定載於本產品專屬之詳細條件文件本身。撤銷事由為九項（a–i），非前輪所稱六項。本制度為優質居留七項產品之一（永久／可續期一年／特殊人才／傑出人士／投資人〔SAR 7,000,000『投資活動』，為另一獨立產品〕／企業家／不動產）——不動產所有權本身達 SAR 4,000,000 以上即已足夠且完整，不搭配其他可選資產。",
  "sources": [
    { "url": "https://pr.gov.sa/pr?id=pr_product_details_real_estate_owner", "publisher": "Premium Residency Center (Saudi Arabia)", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://pr.gov.sa/pr?id=premium_residency_permit_law", "publisher": "Premium Residency Center (Saudi Arabia) — Premium Residency Permit Law, Royal Decree No. M/106", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://pr.gov.sa/pr?id=premium_residency_regulations", "publisher": "Premium Residency Center (Saudi Arabia) — Implementing Regulations", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://pr.gov.sa/pr?id=conditions_controls", "publisher": "Premium Residency Center (Saudi Arabia) — Detailed Conditions and Requirements of the Real Estate Owner Residency", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://www.ey.com/en_gl/technical/tax-alerts/saudi-arabia-approves-new-real-estate-ownership-law-by-non-saudis", "publisher": "EY Global Tax Alert", "tier": 2, "accessed": "2026-08-02" }
  ],
  "companion_requirements": [
    { "text_en": "Health insurance required (Premium Residency Permit Law Art. 6(1)(b)) — a system-wide requirement, not real-estate-specific.", "text_zh": "須具備健康保險（《優質居留許可法》第 6 條第 1 項 b 款）——制度層級之一般要求，非不動產產品專屬。", "tier": 1, "src": 1 },
    { "text_en": "Proof of financial solvency (recent bank statement or other documents required by the Center) — a generic requirement, not a separate income test.", "text_zh": "須提出財力證明（近期銀行對帳單或中心要求之其他文件）——為一般性要求，非獨立之收入門檻測試。", "tier": 1, "src": 2 },
    { "text_en": "Clean criminal record required — system-wide KYC requirement across all seven products.", "text_zh": "須無犯罪紀錄——七項產品共用之基本 KYC 要求。", "tier": 1, "src": 2 },
    { "text_en": "One-time application/issuance fee SAR 4,000 (Implementing Regulations Art. 6 fee table).", "text_zh": "一次性申請／核發規費 SAR 4,000（實施條例第 6 條規費對照表）。", "tier": 1, "src": 2 },
    { "text_en": "If the qualifying property is sold, it must be replaced with another qualifying property within 90 days, or the permit is revoked.", "text_zh": "若出售合格物件，須於 90 天內替換為另一合格物件，否則許可撤銷。", "tier": 1, "src": 3 },
    { "text_en": "Off-plan purchases must complete (full title transfer) within 5 years, or the permit is revoked.", "text_zh": "期房須於 5 年內完成過戶，否則許可撤銷。", "tier": 1, "src": 3 },
    { "text_en": "No minimum physical presence in the Kingdom is required to maintain the permit.", "text_zh": "維持許可不須任何最低境內停留天數。", "tier": 1, "src": 3 },
    { "text_en": "Not established: whether any additional recurring fee applies beyond the one-time SAR 4,000 issuance fee.", "text_zh": "未能確立：除一次性 SAR 4,000 核發規費外，是否另有經常性費用。", "tier": 1, "src": 2 }
  ]
}
```

---

### 埃及

**裁決**：**INCLUDE**（`confidence: medium-high`，`route_type` 修正為 **property_one_of_several**）

**tier 1 取得狀況**：核心事實攻克，但兩個次要欄位仍有未解決之處。本輪 WebSearch 於任務開始前即已用罄，改用 `manshurat.org`（埃及印刷總署官方公報之轉載鏡像站——內容為公報掃描原文，非第三方改寫摘要）站內搜尋，成功定位並**直接下載讀取三份官方公報 PDF 全文**：（1）2019 年第 3099 號總理令（原始版本，門檻 50 萬美元，限國有物業）；（2）2023 年第 876 號總理令（修正 3099/2019，門檻降至 30 萬美元，**仍維持**限國有物業之限制）；（3）**2023 年第 28 號法律**（總統簽署，修正《國籍法》母法第 4bis 條本身，刪除「限國有物業」限制，並於法律層級重新確認 1 萬美元規費）。另直接開啟 GAFI 官方頁英文與阿拉伯文雙版，逐字確認入籍（非居留）此一核心主張。

**證據**：
- https://manshurat.org/file/89139/download?token=wMUohaq2 （Tier 1，官方公報掃描 PDF 全文，2023 年第 876 號總理令，公報第 9 期續篇（ج），2023-03-02）
- https://manshurat.org/file/87121/download?token=K6c304oG （Tier 1，官方公報掃描 PDF 全文，2019 年第 3099 號總理令〔原始框架〕，公報第 50 期續篇（ج），2019-12-18）——載有五年條件式保留條款原文
- https://manshurat.org/file/88044/download?token=xdh8LzQF （Tier 1，官方公報掃描 PDF 全文，**2023 年第 28 號法律**〔總統簽署，修正《國籍法》母法〕，公報第 20 期續篇（د），2023-05-21）——刪除「限國有物業」限制，法律層級重新確認 1 萬美元規費
- https://www.gafi.gov.eg/English/Howcanwehelp/Pages/Egyptian-Citizenship.aspx （Tier 1，GAFI 官方英文頁）——逐字：「Egyptian citizenship is granted to the investor and their minor children up to the age of 21, by decision of the Prime Minister」；明文不設居留期間要求；審理約 3–6 個月
- https://www.gafi.gov.eg/Arabic/Howcanwehelp/Pages/Egyptian-Citizenship.aspx （Tier 1，阿拉伯文鏡像頁，內容一致）
- https://manshurat.org/node/74546/relations 、 https://manshurat.org/node/7358/relations （Tier 2——鏡像站之「修正關係樹」功能，用於窮盡搜尋「3562/2023」號令與任何 2024–2026 年後續修法，皆查無結果；惟此索引本身經證實不完整——連第 28/2023 號法律本身都未列在母法之修正歷史清單內，儘管該法律確實存在，故僅能作為「未查得」而非「已確認查無」之佐證）

**與前輪的分歧（重要，多處需修正）**：
1. **文號錯誤**：前輪主張的「2023 年第 3562 號總理令，公報第 37 期（مكرر），2023-09-18」，本輪以文號搜尋、日期搜尋、以及在 3099/2019 與《國籍法》母法各自的修正關係樹中逐一核對，**皆查無此文號**。前輪描述的實質變化（刪除「限國有物業」限制）**確有其事**，但達成此變化的實際法源是**2023 年第 28 號法律**（總統簽署之《國籍法》母法修正案，2023-05-21）——法律位階、文號、日期、簽署機關皆與前輪引用不同。這看起來是前輪的引用錯誤／文號混淆，不是憑空捏造實質內容。
2. **「入籍」（非居留）此一核心主張成立，且比前輪更明確**：前輪僅稱「制度存在性已於 GAFI 官網確認」，本輪取得 GAFI 官方頁**逐字**確認「Egyptian citizenship is granted... by decision of the Prime Minister」，且法條文字本身亦錨定於此——《國籍法》第 4bis 條規範對象是「طلب التجنس」（歸化／入籍申請），主管單位是隸屬總理府之「歸化申請審查小組」（GAFI 僅代為受理）。且明文**不**要求額外居留年限（區別於賽普勒斯／西班牙等須先居留數年之制度）：申請人僅取得 6 個月臨時居留以完成投資，其後即由總理決定直接授予公民身分，非分階段轉換。
3. **「五年處分鎖定」須重新定性為附條件保留條款，非絕對禁售**。本輪從 2019 年第 3099 號總理令原文（非 2023 年修正部分）讀到完整條文：「若第（1）項〔不動產〕之物業於取得後未滿五年即處分，或第（2）項〔投資項目〕之投資清算／停止……欲保留埃及公民身分，須存入第（4）項〔25 萬美元〕之金額，除非該處分係無償轉予國家」。這代表提前出售**並非違法**，而是「提前出售仍可保留公民身分，但須另外補繳 25 萬美元」的條件機制，且此條款同時適用於不動產路徑與投資項目路徑，非不動產專屬。此條款是否原文未變地延續進 2023 年後之現行文本，本輪未能取得後 2023 年文件直接重新確認——876/2023 僅取代「路徑列舉」該段，保留條款結構上屬於後續獨立段落，理論上應延續，但這是基於條文結構的合理推論，非直接重新確認。
4. **`route_type` 應為 property_one_of_several**：與厄瓜多結構類似，同一入籍制度下有四種各自可單獨達標的投資形式（不動產 ≥30 萬美元／投資項目 35 萬＋10 萬美元不可退還／50 萬美元三年期存款／25 萬美元不可退還存款），不動產只是四選一。
5. **未解決的張力（前輪未揭露）**：本輪找到的最新總理令層級文本（876/2023）字面上**仍寫**「限國有或其他公法人所有之不動產」，但兩個月後的母法修正（第 28/2023 號法律）已刪除此限制。本輪未能找到任何後續總理令將 876/2023 的文字更新至與母法一致。GAFI 官方頁本身將此路徑簡述為「購買不動產」，未附加「限國有」之限定語，暗示制度實務上已依母法之放寬版本運作——但這是從官方摘要頁推論，非直接確認之現行總理令文本。**站上刊登時應揭露此張力**，不宜無條件斷言「任何私人物業皆合格」。
6. **cc.gov.eg 引用修正**：前輪稱此為「最高憲法法院」資料庫，本輪查證其實際指向埃及**最高上訴法院**（Court of Cassation，محكمة النقض），非憲法法院——屬引用衛生問題，不影響實質結論。
7. **本輪未取得任何 Tier 2 次級來源交叉佐證**（國際律師事務所、四大會計師事務所、主流外媒），原因是搜尋工具本身失能（Bing 對此冷門主題持續回傳無關的埃及觀光／維基百科結果，DuckDuckGo／Mojeek 遭 CAPTCHA 阻擋），**不是查無此類來源**。這與資料集通常要求雙重來源確認的慣例有落差，若嚴格套用「單一 tier 1 亦可 INCLUDE，但雙重 tier 2 才能在 tier 1 缺席時 INCLUDE_WITH_CAVEAT」的規則，本筆的 tier 1（三份官方公報原文＋官方頁雙語版）本身已足夠支撐 INCLUDE，但信心度不宜給到最高等級，故裁定 `confidence: medium-high`（而非 high），並在 `ownership_form`／配偶配套等欄位個別標註未解決或未查證之處。

**入庫欄位資料**：

```json
{
  "id": "egypt",
  "region": "meaf",
  "source_file": "visa-round2b",
  "flag": "🇪🇬",
  "jurisdiction": "Egypt",
  "jurisdiction_zh": "埃及",
  "programme": "Citizenship by investment — real estate route (Nationality Law No. 26/1975 Art. 4bis, as amended by Law No. 28/2023; implemented via Prime Ministerial Decree No. 876/2023, amending Decree No. 3099/2019)",
  "programme_zh": "投資入籍——不動產路徑（《國籍法》1975 年第 26 號法律第 4bis 條，經 2023 年第 28 號法律修正；並依 2023 年第 876 號總理令〔修正 2019 年第 3099 號總理令〕施行）",
  "label_en": "Citizenship by Real Estate Investment",
  "label_zh": "不動產投資入籍",
  "route_type": "property_one_of_several",
  "confidence": "medium-high",
  "outcome_class": "citizenship",
  "established": {
    "threshold": "published",
    "term": "published",
    "stay": "absent_verified",
    "leads_to": "published"
  },
  "min_value": {
    "amount": 300000,
    "currency": "USD",
    "usd": 300000,
    "basis": "One of four interchangeable investment routes under Nationality Law Art. 4bis, as most recently restructured by PM Decree 876/2023 (2023-03-02), amending base Decree 3099/2019 (2019-12-18, which set the real-estate threshold at USD 500,000): (1) real estate purchase >= USD 300,000; (2) investment-project capital injection USD 350,000 + USD 100,000 non-refundable; (3) a USD 500,000 deposit held 3 years; (4) a USD 250,000 non-refundable deposit. Funds must be transferred from abroad through Central Bank of Egypt channels, or proven to have entered Egypt via a customs port with customs certification.",
    "tier": 1,
    "src": 0
  },
  "sort_usd": 300000,
  "term": {
    "text_en": "Not a fixed 'permit term' — this route grants citizenship directly, not a renewable/temporary residence permit. What is time-bound is a POST-GRANT retention condition: per the original 2019 decree text (Decree 3099/2019, Article One, trailing paragraph), if the qualifying property is disposed of before 5 years have passed since acquisition, retention of the citizenship requires depositing the Route-4 amount (USD 250,000) — unless the property is transferred to the state without consideration. This is a conditional retention mechanism, not an outright prohibition on selling, and it applies to both the real-estate route and the investment-project route, not real estate alone. Whether this clause was carried forward unchanged into the current 876/2023-amended text was not directly confirmed — Decree 876/2023 replaced only the routes-enumeration paragraph, and the retention clause is a separate, later paragraph structurally unaffected by that amendment, so its survival is a reasoned inference, not a re-confirmed current text.",
    "text_zh": "非固定的「許可期限」——本路徑直接授予公民身分，非可續期／臨時居留許可。真正與時間掛鉤的是一項**核准後之保留條件**：依原始 2019 年第 3099 號總理令（第一條後段）原文，若合格物件於取得後未滿 5 年即處分，欲保留公民身分須另存入第（4）項金額（25 萬美元）——除非該物業係無償轉予國家。此為條件式保留機制，非絕對禁止出售，且同時適用於不動產與投資項目兩條路徑，非不動產專屬。此條款是否原封不動延續進現行 876/2023 修正後文本，本輪未直接重新確認——876/2023 僅取代「路徑列舉」該段，保留條款屬結構上獨立之後段，理論上不受該次修正影響，惟此為合理推論，非重新確認之現行文本。",
    "tier": 1,
    "src": 1
  },
  "stay": {
    "text_en": "Confirmed absent. GAFI's own official program page states no residency-period requirement is imposed on the applicant (unlike programmes requiring years of prior residence) — the applicant receives a 6-month temporary residence permit solely to execute the chosen investment, after which citizenship is granted directly by Prime Ministerial decision, typically within 3-6 months of application.",
    "text_zh": "已確認不存在。GAFI 官方頁明文不對申請人設居留期間要求（有別於須先居留數年之其他制度）——申請人僅取得 6 個月臨時居留以完成所選投資，其後由總理決定直接授予公民身分，一般於申請後約 3–6 個月內完成。",
    "tier": 1,
    "src": 3
  },
  "leads_to": {
    "text_en": "Citizenship (naturalization), not residency — confirmed verbatim on GAFI's official English program page: 'Egyptian citizenship is granted to the investor and their minor children up to the age of 21, by decision of the Prime Minister,' mirrored identically on GAFI's Arabic page. Textually anchored in the Nationality Law itself: Art. 4bis governs the naturalization application (طلب التجنس), administered by the Naturalization Application Examination Unit affiliated with the Prime Minister's Office (GAFI merely hosts an intake office). Grant is direct, with no additional residence-period requirement layered on top.",
    "text_zh": "入籍（歸化），非居留——GAFI 官方英文頁逐字確認：「Egyptian citizenship is granted to the investor and their minor children up to the age of 21, by decision of the Prime Minister」，阿拉伯文版內容一致。法條文字本身亦錨定於此：《國籍法》第 4bis 條規範「歸化申請」，由隸屬總理府之「歸化申請審查小組」主管（GAFI 僅代為受理）。核准為直接授予，不另外疊加居留年限要求。",
    "tier": 1,
    "src": 3
  },
  "ownership_form": {
    "text_en": "UNRESOLVED TENSION between decree-level and law-level text — flag prominently if published. The most recent Prime Ministerial decree found (876/2023) still states the real-estate route requires property 'owned by the state or other public legal persons' — i.e. only property acquired FROM a state/public-sector seller, not any privately-owned real estate. But the parent statute (Nationality Law Art. 4bis, as amended by Law No. 28/2023, enacted two months after Decree 876/2023) deletes that qualifier. No decree-level text conforming 876/2023's wording to the broadened law-level definition was found. GAFI's own official page currently describes the route simply as 'purchasing real estate,' with no state-ownership qualifier, suggesting the programme operates in practice on the broadened law-level definition — but this is inference from an official summary page, not a directly confirmed current decree text.",
    "text_zh": "**總理令層級與法律層級文本存在未解決之張力，刊登時應顯著標註**。本輪找到最新之總理令（876/2023）字面上仍要求不動產路徑須為「國家或其他公法人所有」之物業——即僅限向公部門賣方購買，非任何私人物業。但母法（《國籍法》第 4bis 條，經 876/2023 兩個月後生效之第 28/2023 號法律修正）已刪除此限定語。本輪未能找到任何將 876/2023 文字更新至與母法一致之後續總理令。GAFI 官方頁本身將此路徑簡述為「購買不動產」，未附加限國有之限定語，暗示實務上已依母法放寬版本運作——但這是從官方摘要頁推論，非直接確認之現行總理令文本。",
    "tier": 2,
    "src": 0
  },
  "offplan": {
    "text_en": "Not established in this pass. No source reached addressed whether an off-plan/pre-completion real estate purchase qualifies for this route, as distinct from a completed, titled property.",
    "text_zh": "本次查核未查證。未見任何來源觸及期房／未完工不動產是否合格於本路徑，或是否須為已完工、已取得產權之物件。",
    "tier": 1,
    "src": 0
  },
  "mortgage": {
    "text_en": "Not established specifically for domestic financing/mortgage arrangements. What is confirmed: the qualifying USD 300,000 must be transferred from abroad through Central Bank of Egypt channels, OR proven to have physically entered Egypt via a customs port with customs certification — this governs the SOURCE of funds, not whether local Egyptian mortgage financing may cover part of the purchase price.",
    "text_zh": "本地融資／貸款安排未能確立。已確認者：達標所需之 30 萬美元須透過埃及中央銀行管道自境外匯入，或經海關查驗證明實體入境——此規範資金**來源**，非物業價金是否得以埃及本地房貸支應部分金額。",
    "tier": 1,
    "src": 0
  },
  "dependants": {
    "text_en": "Minor children up to age 21 are covered (GAFI's official page; Law No. 28/2023 also addresses minor children's nationality-inheritance/election rules). Spouse coverage was not confirmed in any source reached this round — this is a gap in the record, not a confirmed absence.",
    "text_zh": "涵蓋 21 歲以下未成年子女（GAFI 官方頁；第 28/2023 號法律亦處理未成年子女國籍隨同／選擇規則）。配偶是否納入，本輪未於任何來源中確認——屬記錄缺口，非已確認之排除。",
    "tier": 1,
    "src": 3
  },
  "entry_tax": {
    "text_en": "Not established in this pass. Egypt's general property-transfer tax/registration fee regime, independent of this citizenship programme's own USD 10,000 application fee, was not checked.",
    "text_zh": "本次查核未查證。埃及一般性不動產過戶稅／登記費制度（與本入籍制度自身之 1 萬美元申請規費為兩件事），本輪未查核。",
    "tier": 1,
    "src": 0
  },
  "last_change": {
    "text_en": "Most recent instrument found: Law No. 28/2023 (signed by President El-Sisi, Official Gazette Issue 20 bis(د), 2023-05-21), amending the base Nationality Law itself, not merely an implementing decree — removes the 'state/public-legal-person-owned property only' restriction from the real-estate route, and re-confirms the USD 10,000 application fee at statute level. No later decree or law (2024, 2025, or 2026) touching this programme was found, despite a dedicated search of the gazette mirror's document-relations trees for both the base decree and the base law — but that index is demonstrably incomplete (it does not even list Law 28/2023 itself under the base law's amendment history), so this is an unfound negative, not a confirmed one. CORRECTION to a prior verification round: a 'Decree No. 3562/2023, Gazette Issue 37(مكرر), dated 2023-09-18' cited as the instrument removing the state-ownership restriction could not be located anywhere by number, by date, or in either instrument's amendment-relations tree. The substantive change it described is real and confirmed; the actual instrument achieving it is Law No. 28/2023 (a presidential-signed statute) — different instrument type, date, and issuing authority than previously cited.",
    "text_zh": "已查得之最新法源：**第 28/2023 號法律**（總統 El-Sisi 簽署，公報第 20 期續篇（د），2023-05-21），修正《國籍法》母法本身，非僅為施行令——刪除不動產路徑「限國家或公法人所有物業」之限制，並於法律層級重新確認 1 萬美元申請規費。本輪窮盡搜尋公報鏡像站之修正關係樹（涵蓋原始總理令與母法兩者），未見任何 2024、2025 或 2026 年後續修法——惟該索引經證實不完整（連第 28/2023 號法律本身都未列於母法修正歷史中），故此為「未查得」而非「已確認查無」。**修正前一輪查證**：前輪引用之「2023 年第 3562 號總理令，公報第 37 期（مكرر），2023-09-18」，本輪以文號、日期、及兩份法源各自之修正關係樹逐一核對，皆查無此文號。其描述之實質變化確有其事，但實際法源是第 28/2023 號法律（總統簽署之法律，非總理令）——法源類型、日期、簽署機關皆與前輪引用不同。",
    "tier": 1,
    "src": 2
  },
  "short": {
    "term_en": "Direct citizenship grant, not a residence permit; 5-yr conditional retention clause post-grant",
    "term_zh": "直接授予公民身分，非居留許可；核准後另有 5 年條件式保留條款",
    "stay_en": "None — no residency-period requirement",
    "stay_zh": "無——不設居留期間要求",
    "outcome_en": "Citizenship (naturalization), direct grant, ~3–6 months processing",
    "outcome_zh": "入籍（歸化），直接授予，約 3～6 個月審理",
    "own_en": "One of 4 investment routes (real estate / investment project / 3-yr deposit / non-refundable deposit); real estate alone (≥ USD 300,000) suffices",
    "own_zh": "為四種投資路徑之一（不動產／投資項目／三年期存款／不可退還存款）；不動產單獨達 30 萬美元門檻即可"
  },
  "notes_en": "IMPORTANT CORRECTIONS to a prior verification round: (1) The cited 'Decree No. 3562/2023' could not be located under that number/date in the gazette mirror's index. The instrument that actually removed the state-ownership restriction is Law No. 28/2023 (a presidential-signed amendment to the Nationality Law itself, Official Gazette Issue 20 bis, 2023-05-21), not a Prime Ministerial decree. (2) The '5-year disposal lock' is not an outright prohibition on selling — it is a conditional citizenship-retention clause: sell before 5 years and citizenship remains valid only if the USD 250,000 Route-4 amount is then deposited (or the property is given to the state for free); this clause applies to the investment-project route as well, not real estate alone. (3) 'cc.gov.eg' resolves to Egypt's Court of Cassation, not the Supreme Constitutional Court as previously described (does not affect substantive findings). route_type is property_one_of_several: real estate is one of four interchangeable investment options under the same citizenship programme. An unresolved tension exists between the most recent decree-level text (876/2023, still says state-owned property only) and the law-level text (Law 28/2023, removes that restriction) — see ownership_form; do not assert unconditionally that any privately-owned property qualifies. Spouse coverage (as opposed to minor children) was not confirmed. No Tier 2 secondary-source corroboration (law firm, Big 4, international press) was obtained this round due to search-tooling failures (WebSearch exhausted before starting, Bing/DuckDuckGo/Mojeek unproductive or CAPTCHA-blocked for this niche topic) — the entry rests on Tier 1 primary-source text (three Official Gazette instruments read directly, plus GAFI's own official page in English and Arabic) without independent secondary corroboration. This absence should be disclosed if a stricter dual-source standard is later applied.",
  "notes_zh": "對前一輪查證之重要修正：（一）前輪引用之「2023 年第 3562 號總理令」，本輪於公報鏡像站索引中以文號、日期皆查無此文號。實際刪除限國有物業限制之法源，是**第 28/2023 號法律**（總統簽署之《國籍法》母法修正案，公報第 20 期續篇，2023-05-21），非總理令。（二）「五年處分鎖定」並非絕對禁止出售——實為條件式公民身分保留條款：五年內出售，仍可保留公民身分，惟須另存入第（4）項之 25 萬美元（或無償轉予國家）；此條款同時適用於投資項目路徑，非不動產專屬。（三）「cc.gov.eg」實際指向埃及最高上訴法院，非前輪所稱之最高憲法法院（不影響實質結論）。`route_type` 為 property_one_of_several：不動產僅為同一入籍制度下四種可互換投資選項之一。最新總理令層級文本（876/2023，仍寫限國有物業）與母法層級文本（第 28/2023 號法律，已刪除該限制）之間存在未解決之張力——見 `ownership_form` 欄位；不應無條件斷言任何私人物業皆合格。配偶（相對於未成年子女）是否納入配套未經確認。本輪因搜尋工具本身失能（WebSearch 任務開始前即已用罄，Bing／DuckDuckGo／Mojeek 對此冷門主題無效或遭 CAPTCHA 阻擋），未取得任何 Tier 2 次級來源交叉佐證——本筆係基於 Tier 1 一手文本（三份官方公報原文＋GAFI 官方頁英阿雙語版）獨立支撐，未經第二來源交叉確認。若日後套用更嚴格之雙重來源標準，應揭露此點。",
  "sources": [
    { "url": "https://manshurat.org/file/89139/download?token=wMUohaq2", "publisher": "Egyptian Government Printing Authority official gazette (via manshurat.org mirror) — PM Decree No. 876/2023", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://manshurat.org/file/87121/download?token=K6c304oG", "publisher": "Egyptian Government Printing Authority official gazette (via manshurat.org mirror) — PM Decree No. 3099/2019", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://manshurat.org/file/88044/download?token=xdh8LzQF", "publisher": "Egyptian Government Printing Authority official gazette (via manshurat.org mirror) — Law No. 28/2023", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://www.gafi.gov.eg/English/Howcanwehelp/Pages/Egyptian-Citizenship.aspx", "publisher": "General Authority for Investment and Free Zones (GAFI), Egypt", "tier": 1, "accessed": "2026-08-02" },
    { "url": "https://www.gafi.gov.eg/Arabic/Howcanwehelp/Pages/Egyptian-Citizenship.aspx", "publisher": "General Authority for Investment and Free Zones (GAFI), Egypt — Arabic mirror", "tier": 1, "accessed": "2026-08-02" }
  ],
  "companion_requirements": [
    { "text_en": "Application fee USD 10,000, confirmed independently at both GAFI's page and Law No. 28/2023's statutory text.", "text_zh": "申請規費 1 萬美元，經 GAFI 官方頁與第 28/2023 號法律條文雙重獨立確認。", "tier": 1, "src": 3 },
    { "text_en": "Funds must be transferred from abroad through Central Bank of Egypt channels, OR proven to have entered Egypt via a customs port with customs certification (cash physically carried in and declared).", "text_zh": "資金須經埃及中央銀行管道自境外匯入，或經海關查驗證明實體入境並申報。", "tier": 1, "src": 0 },
    { "text_en": "6-month temporary residence permit issued solely to execute the chosen investment, prior to citizenship being granted.", "text_zh": "核准公民身分前，先核發 6 個月臨時居留許可，僅供完成所選投資之用。", "tier": 1, "src": 3 },
    { "text_en": "Not established: property registration process (الشهر العقاري) requirements specific to this programme; spouse coverage; whether an off-plan purchase qualifies.", "text_zh": "未能確立：本制度專屬之不動產登記（الشهر العقاري）程序要求；配偶是否納入配套；期房是否合格。", "tier": 1, "src": 0 }
  ]
}
```

---

## 本輪查證方法與限制誠實揭露

- 兩組 subagent 各自的 WebSearch 額度皆在任務**開始前**即已顯示用罄（與同一 session 稍早的沙烏地／埃及第一輪查證共用額度池有關），皆改用替代管道：沙烏地一組發現瀏覽器（`claude-in-chrome`）已有前一輪殘留的 `pr.gov.sa` 分頁，改用瀏覽器現場讀取（`pr.gov.sa` 是純前端 JS 應用，`curl`／`WebFetch` 只能拿到空殼）；埃及一組改用 `manshurat.org`（官方公報鏡像站）站內搜尋＋直接下載 PDF，並改用 Bing／curl 替代 DuckDuckGo（DuckDuckGo／Mojeek 皆遭 CAPTCHA 阻擋）。
- **`web.archive.org` 依指示全程未使用**，兩組皆確認此為工具層本身阻擋，未浪費時間嘗試。
- 沙烏地一組因取得完整官方一手文件（母法＋實施條例＋產品專屬詳細條件文件三份全文），達到本任務所能取得的最高查證強度，`confidence: high`。
- 埃及一組雖取得三份官方公報 PDF 全文＋GAFI 官方頁雙語版（皆為 Tier 1），但（一）搜尋工具失能導致完全未取得任何 Tier 2 次級來源交叉佐證，（二）「不動產是否限國有」這個欄位存在總理令與母法兩個層級文本互相矛盾且未見後續調和文件，（三）「五年保留條款是否延續進現行文本」屬合理推論而非直接重新確認——三項合計，裁定 `confidence: medium-high` 而非 `high`，並要求下游文案在 `ownership_form` 與 `term` 欄位保留警語，不得寫成無保留的絕對陳述。
- 本彙整者（我）未重新開啟任一 URL 做獨立三驗，僅對兩份 subagent 報告做批判性覆核：逐一檢查其宣稱的 tier 是否真的達標（例如埃及一組宣稱「入籍」為 Tier 1，覆核後確認其引用的是官方頁逐字英阿雙語，成立；沙烏地一組宣稱「撤銷事由九項」係直接讀取原文列點計數，成立）、是否有未揭露的矛盾（找到埃及「限國有」欄位的總理令／母法張力，subagent 報告中雖已提及但本彙整者將其提升為欄位層級的顯著警語，而非僅在 notes 段落一筆帶過）、以及是否有可疑的推論跳躍（沙烏地「續期機制細節」、埃及「五年條款是否延續」，兩處皆在入庫欄位文字中明確標註為推論而非確認事實）。

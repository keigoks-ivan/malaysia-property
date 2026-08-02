# 中東非洲組查證報告（8 套）

查證日期：2026-08-02 ｜ 對照資料集 compiled：2026-08-01

查證方式：三組並行 agent 各自即時重新讀取一級來源（政府網站／官方公報／法規原文），逐欄位比對現有記載；對每一個已標 UNVERIFIED／not established／deliberately omitted 的欄位，本輪一律主動重查一次，並在下方區分「上一輪沒查」與「這輪查過確實查無」兩種情形。

## 摘要

- 確認無誤：1 筆（jordan）
- 有出入需修正：2 筆（uae、oman）
- 新發現的配套要求：3 筆（mauritius、qatar、bahrain）
- 無法確立（維持原判，本輪已主動重查）：2 筆（uae-2、cape-verde）

（註：多數筆同時落在不只一個類別，上面是依「最需要編輯注意的主線」歸類；細節見逐筆分節，每筆底下都有完整的欄位判定表。）

---

## 逐筆

### mauritius — 模里西斯

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| （無專屬欄位，屬新發現的配套要求） | 未提及醫療證明／品行證明 | EDB Guidelines PDF 逐字：「(v) Medical certificates for each applicant with a validity period of 6 months」「(vi) Morality certificates of applicants, above the age of 18, with a validity period of 6 months」——除購房外，每位申請人（含 18 歲以上受扶養人）都須另外提交 6 個月效期內的體檢證明與品行（無犯罪紀錄）證明 | 1 | https://edbmauritius.org/wp-content/uploads/2022/10/Guidelines-acquisition-of-apartments-incl.residency.pdf（今日重新下載、逐字核對） |
| `ownership_form`／`extra_tiers` | 只寫 G+2 購買門檻 MUR 6,000,000，未提購買本身的行政關卡 | 《非公民（財產限制）法》s.3(3)(c)(v) 原文：G+2 購買須「on production of an authorisation from the Economic Development Board granted after it has obtained the approval of the Minister」——即買房本身（非居留許可）就需經濟發展局＋部長裁量核准，不只是價格門檻 | 1 | https://lawsofmauritius.govmu.org/portal/viewlegislationdocument/web/?docnumber=&doctitle=Tm9uLUNpdGl6ZW5zIChQcm9wZXJ0eSBSZXN0cmljdGlvbikgQWN0&doctype=act（今日重新下載，文件時戳 2026-08-02） |
| 其餘欄位（`min_value`、`term`、`stay`、`leads_to`、`entry_tax`、`dependants`、`mortgage`、`offplan`） | — | 其餘欄位核對無誤：今日重新下載 Immigration Act 全文逐字比對，內容與現有記載完全一致，無 2026-08-01 後之修法跡象 | 1 | 同上兩份法規原文 |

**配套要求**：除買房外，還必須：(1) 每位申請人（含 18 歲以上受扶養人）提交 6 個月效期內的醫療證明；(2) 6 個月效期內的品行／無犯罪紀錄證明；(3) 標準公證登記＋登記稅（10%，2026/7/1 起生效，此點現有記載已正確捕捉）；(4) G+2 購買本身須經濟發展局＋部長裁量核准之授權，不是單純價格門檻即可購買。本輪逐條全文檢索未發現固定存款／保證金要求，也未發現購房路徑本身有額外收入門檻（退休非公民路徑才有 USD 1,500/月與 USD 200k/5 年，但那是不同路徑，現有記載已正確區分）——「無」是真的查過，不是漏查。

**建議修正**：於 notes 或新增專屬欄位補入醫療證明＋品行證明的強制要求，以及 G+2 購買須經 EDB＋部長授權一節；這正是站主要找的「買房不是充分條件」失效模式的典型案例。

**現有記載較可靠之處**：關於 EDB 自家指引 PDF 誤引「第 8 條」為 G+2 居留法源的警告，本輪獨立重新下載 PDF 逐字核對，確認原記錄完全正確（PDF 原文確實寫「Pursuant to Section 8 of the Immigration Act」，而第 8 條實為「禁止入境者」）——這個細節原記錄查得比本輪更細，予以保留。

---

### uae — 阿聯（黃金簽證：房產投資人路徑）

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `term` | DLD 稱 10 年可續期 vs ICP／u.ae 稱 5 年，兩者矛盾未解 | 矛盾依舊存在，今日即時重讀三個政府頁面，仍是同一組數字：DLD 寫「10-years renewable residence permit」（頁尾 Last Update: 13 July 2026）；ICP 寫「5 years (real estate investments)」（頁尾 23 March 2026）；u.ae 寫「5 years (real estate investments)」（頁尾 28 July 2026）。**這不是「沒查」，是查了兩次（原記錄＋本輪）都得到同一組矛盾**，維持「兩者並列，不發布單一數字」的處理方式 | 1 | https://dubailand.gov.ae/en/eservices/request-for-golden-visa-investor/ ；https://icp.gov.ae/en/services/golden-residency/ ；https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa |
| `min_value`／`mortgage`（新發現，原記錄未捕捉） | 原記錄只查過「已付 50%」謠言（查無實據），未查過「是否可設定抵押」這件事在 ICP 與 DLD 之間是否一致 | **新發現一級來源互相矛盾**：ICP 官網房產類別文件清單寫「A letter from the Real Estate Registration Department proving ownership of one or more properties valued at ≥ AED 2 million **(without loans)**」——即 ICP 官方文字要求物業完全無貸款；這與 DLD 明文接受抵押物件（「The property may be mortgaged, and a no-objection bank letter…」）直接矛盾。兩次獨立擷取（直連＋代理）拿到同一句，非誤讀 | 1（兩份來源皆一級，但彼此矛盾） | https://icp.gov.ae/en/services/golden-residency/（今日兩次獨立查證） |
| `offplan`／`mortgage`（2026 年 2 月「50%規則放寬」傳言） | 查無實據，DLD 前後 Wayback 快照逐字相同 | **本輪重新查證，結論不變，且是主動重查而非延續舊結論**：DLD 今日即時頁面仍是「a bank letter indicating 2 million AED paid amount as a proof」同一段文字；惟頁尾顯示「Last Update Date: 13 July 2026」，比原記錄查過的 2026-07-08 Wayback 快照更新，代表頁面在此之後確實被編輯過一次。逐句核對後，抵押相關條款文字未變，結論維持「未獲證實」 | 1 | 同上 DLD 今日即時頁 |
| `stay` | 未能自任何政府來源查證 | 本輪主動以新關鍵字重搜＋重讀 ICP/u.ae 頁面，除原記錄已引用的兩句模糊描述外，仍無任何一級或雙重二級來源給出具體天數；其餘搜尋結果全是仲介／代辦網站，依規定不採用。**確認為「查過仍查無」，非「沒查」** | — | 已查但無合格結果，故不予引用任何連結 |
| `leads_to`（歸化） | 無入籍途徑，未進一步查證 | 查到阿聯 2021 年 1 月確有投資人／專業人才裁量歸化提名制度，報導稱「投資人須擁有阿聯房產方符資格」，但這是酋長提名、總統批准的裁量制，非本簽證自動衍生的權利，與現有記載方向一致。惟此說法僅一則三級新聞來源，未達雙重二級標準，**不足以升級欄位，維持原判** | 3（不採用為結論依據，僅供背景） | 不引用為結論來源 |
| 其餘欄位（`ownership_form`、`dependants`、`entry_tax`） | — | 其餘欄位核對無誤：今日即時重讀 DLD 頁，文字與現有記錄逐句相同 | 1 | https://dubailand.gov.ae/en/eservices/request-for-golden-visa-investor/ |

**配套要求**：除 AED 2,000,000 房產外，DLD 頁面列出的必要條件另包含體檢（費用 AED 700，含在總費用 AED 9,884.75 內）；若為家屬（尤其父母）申請依親則需另附健康保險文件。未發現最低收入測試、固定存款、額外犯罪紀錄查核要求。

**uae 與 uae-2 是否被混用**：本輪確認為兩個獨立法源、獨立門檻、獨立申請管道的制度——`uae`＝2022 年第 65 號內閣決議附件（Article 77）之黃金簽證，AED 200 萬門檻，DLD／ICP 為申請管道；`uae-2`＝同一決議第 53 條「外籍不動產所有權人居留許可」，無最低房產金額、改採月收入 AED 10,000 測試，申請管道另見 GDRFA（杜拜）與 ICP 的獨立服務頁。兩筆記錄未見混淆或互相污染。

**建議修正**：`term`/`min_value` 欄位建議補上 ICP「(without loans)」與 DLD 接受抵押的新矛盾點，與既有 10年/5年矛盾並列說明，讓讀者知道「用貸款買房是否仍能申請」這件事，兩個一級來源本身就對不上；`offplan`/`last_change` 可補記「DLD 頁面於 2026-07-13 有一次編輯，但逐句核對後抵押條款文字未變」。

**現有記載較可靠之處**：50% 規則的 Wayback 逐字比對方法論本身很扎實，本輪延伸驗證同一結論，沒有找到推翻空間，予以保留。

---

### uae-2 — 阿聯（外籍不動產所有權人居留許可，第 53 條）

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `ownership_form`／`min_value` | 第 53 條逐字引用（月收入 AED 10,000、無房產金額門檻） | 今日透過代理重新繞過官網 403，取得第 53 條完整逐字文本，與現有記錄引用**完全一致**，五項條件（已完工、所有權證明、完全持有、可居住、月收入 AED 10,000 或財務能力證明）逐字相符 | 1 | https://uaelegislation.gov.ae/en/legislations/1601（今日重新取得全文） |
| `entry_tax`（原「本次研究未涵蓋」） | 未涵蓋 | 本輪主動查到實際申請服務頁——GDRFA 杜拜「Issuance of a residence permit for the owner of a property」（頁尾顯示「Website last updated on 02/08/2026」，即查證當日），費用清單：居留許可費 AED 200＋Knowledge Dirham AED 10＋Innovation Dirham AED 10＋境內受理費 AED 500＋送達費 AED 20，另有「居留超過 2 年後每年加收 AED 100」。**但**同一制度在 ICP 鏡像服務頁的費用拆項不同（申請 AED 100＋年度核發 AED 100＋智慧服務費 AED 100），兩份一級來源彼此對不上。**這是「查過但仍無法給出單一確定數字」，非未查**，建議發布前再對帳一輪，暫不刊登單一金額 | 1（兩份來源皆一級，但彼此不一致） | https://gdrfad.gov.ae/en/services/f52024e6-b812-11ed-5210-4cd98f768936 ；https://icp.gov.ae/en/services-details/?serviceid=64afe3c1035448005bd52e64 |
| `term`（原「第 53 條未載，他處亦未查證」） | 未查證 | 本輪主動查了第 53 條全文＋GDRFA 頁＋ICP 鏡像頁三處，**均未載明**固定年限。唯一線索：GDRFA 費用條款「居留超過 2 年後每年加收 AED 100」暗示基礎期限可能是 2 年，但這是從收費結構推論，非明文年限聲明。**不建議直接寫成「2 年」，仍維持 not_established**，但可在 notes 註記此推論線索 | 1（來源查了，結論仍空白） | 同上三個來源 |
| `dependants`（原「本許可未查證」） | 未查證 | 本輪查了 GDRFA／ICP 頁，網站結構上「家屬」是獨立於本許可之外的另一服務類別，暗示第 53 條許可本身可能不自動含依親——**但此判讀未經逐字原文覆核**，證據強度不足以升級欄位，維持 not_established 並註記待覆核 | 1（來源層級夠，但未逐字覆核） | 同上兩個來源 |
| `stay`／`leads_to`（原「未查證」） | 未查證 | 第 53 條全文、GDRFA 頁、ICP 鏡像頁三處逐一確認，**均完全未提及**最低居留天數或永居／入籍路徑。**這是本輪真的查了三個來源後的空白，不是延續舊結論未查** | 1 | 同上三個來源 |
| `mortgage` | 第 53 條對抵押未置一詞，不作推論 | 今日逐字重讀第 53 條全文，確認條文中確實無任何抵押相關文字，原記錄判斷正確 | 1 | 同上 |

**配套要求**：除完全持有、已完工、可居住的房產外，唯一額外條件是申請人本人月收入 ≥AED 10,000（或證明財務能力），加上少量行政規費（依 GDRFA 落在 AED 200–500 區間，但兩個一級來源金額拆項不一致，見上）。未發現健康保險、體檢、犯罪紀錄查核、最低持有期限要求——第 53 條全文＋GDRFA＋ICP 三處均無此類文字。

**建議修正**：`entry_tax` 可從「本次研究未涵蓋」改為「已找到費用區間但兩個一級來源金額拆項不一致，需再查一輪對帳」；`term`/`dependants` 建議在 notes 明確寫出「已主動查證 GDRFA＋ICP＋條文全文，term 無明文（費用結構暗示可能以 2 年為基礎但非明文）；dependants 有初步跡象但未逐字覆核」，而不是讓讀者以為沒查過。

**現有記載較可靠之處**：「confidence: medium，原因是 term/stay 無法確立而非條件本身有疑」這個判斷本輪完全站得住——三個新來源都查過一輪，term/stay 依然是空的，原記錄的謹慎程度正確。

---

### jordan — 約旦

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `last_change`（決議日期） | 決議編號與日期皆未確認 | **新增佐證**：約旦官方通訊社 Petra 於 2026-07-15 發稿描述「Wednesday session」，經換算 2026-07-15 確實是週三——日期部分現獲一級來源支持。**決議編號 9238 本輪仍完全查無**：追加查了 Jordan Times、ZAWYA、Jordan News 三篇報導，皆未列出任何決議編號 | 1（日期）／查無（編號） | https://petra.gov.jo/en/news/government-revamps-investor-citizenship-rules-to-funnel-capital-into-provinces |
| `entry_tax` | 「6% 規費、賣方為住宅公司降為 3%」查無依據，不予刊登 | 本輪主動查了約旦不動產過戶稅一般規定：PwC（二級）稱統一 6%；另一房仲入口網站（非合格來源，僅供參考）稱依坪數分級 3%/6%。兩者互相矛盾，**都不支持**「依賣方類型」的說法，也都屬一般過戶稅而非本方案專屬稅費。維持不刊登具體數字 | PwC＝2；房仲網站不採用 | https://taxsummaries.pwc.com/jordan/corporate/other-taxes |
| （新發現，未進入欄位） | 無 | 查到「整體投資人居留＋入籍框架設 500 人年度上限、須經安全審查與財力核實」，源自 2025 年 7 月的舊框架報導（Arab News），**但 2026-07-15 修訂後的三篇報導都未再提**，時間點對不上，無法確認是否延續到現版本。**誠實標記為「查了、但無法確認是否延續」**，不寫入現有欄位 | 2（且時效有落差） | https://www.arabnews.com/node/2592651/business-economy |
| `stay` | 未載明最低居留天數，不作斷言 | 本輪主動查了另一套不同機制（非置產者五年居留押金 2 萬→1 萬第納爾，已置產且住滿 2 年以上免押金），確認與本筆三檔購房居留（150k/200k/300k）無關，不能移用。**本路徑最低居留天數本輪確實查過、確實查無** | 查無（非本路徑） | https://www.arabnews.com/node/2592651/business-economy |
| 其餘欄位（`min_value`、`extra_tiers`、`term`、`leads_to`、`ownership_form`、`offplan`、`mortgage`、`dependants`、`route_type`、`confidence`、`outcome_class`） | — | 其餘欄位核對無誤：三檔門檻（JOD 150k/200k/300k）、五年持有期禁售禁抵押、僅居留不入籍（入籍走股市／建案路徑）、依親條件屬入籍路徑非本路徑，均與 Jordan Times、ZAWYA、Petra、Jordan News 多篇報導逐字吻合 | 1/2 多方一致 | https://petra.gov.jo/en/news/government-revamps-investor-citizenship-rules-to-funnel-capital-into-provinces ；https://www.zawya.com/en/economy/policy/jordan-cabinet-approves-new-investor-residency-citizenship-rules-393411 |

**配套要求**：本輪未找到任何一級或雙重二級來源證實「買房之外」的必要條件（無存款、無收入證明、無保險、無語言測試）。唯一疑似的配套要求（500 人年度上限＋安全審查＋財力核實）因時間點對不上 2026 年修訂，不建議寫入正式欄位，可在 notes 註記作為待觀察項。

**建議修正**：`last_change` 補一句「日期部分已獲 Petra 官方通訊社佐證；決議編號 9238 追加查證仍無法確認」；`entry_tax` 可註記「一般過戶稅另有 PwC（統一 6%）與坪數分級（3%/6%）兩種互相矛盾的二手說法，均與『依賣方類型降稅』的說法不符，且均屬一般稅制而非本方案專屬」。

**現有記載較可靠之處**：現有記載對「不得將入籍路徑的依親條件、6%/3% 規費說法移用到本居留路徑」的謹慎處理，本輪完全站得住——甚至又多驗證了一次「依親條件屬入籍路徑」在多篇 2026 年新聞稿中反覆出現、確實與居留路徑無關。這個判斷比本輪任何單一來源都更準確。

---

### qatar — 卡達

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`／`extra_tiers` | QAR 730,000／3,650,000 兩檔，逐字引用 | 今日即時重讀 aqarat.gov.qa，逐字重現，核對無誤 | 1 | https://www.aqarat.gov.qa/en/own-real-estate |
| `ownership_form`（9 vs 10 區內部矛盾） | 主管機關敘述文字寫 9 個，清單已含 Simaisma 成第 10 筆 | 今日即時重讀同一頁，逐字重現同一矛盾；另找到卡達旅遊局主辦的「2020 年第 28 號決議說明手冊」，全文只描述原始 9 區、完全未提 Simaisma 或 2026 年第 21 號決議——**間接佐證「9 是舊制原文、10 是 2026 修正後才加進清單」的判讀，強化而非推翻現有記載** | 1（即時）＋政府旁證 | https://www.aqarat.gov.qa/en/choose-your-project ；https://www.qatartourism.com/content/dam/qatar-tourism/non-qatari-realestate/instruction-manual.pdf |
| `stay`（90 天規則） | 二級來源（美國國務院＋Fragomen）一致，主管機關文本未載 | 本輪追查到第三個來源（土耳其移民律師事務所）具體宣稱「依 2020 年第 28 號決議第 7 條」規定須每年住滿 90 天；但全文檢索卡達旅遊局說明手冊的第 7 條原文（該條實際內容是「永久居留權益：醫療／教育／投資」），逐字檢索「90」「day」「annually」「per year」**全部掛零**。**這代表該律師事務所的條號歸屬很可能有誤**，是新增的負面證據，不是支持證據；建議在既有的「工作假設值、非法定規則」註記上，再加一句「一項第三來源將此規則歸於第 7 條，但該條實際內容經逐字核對並非天數規定，條號歸屬存疑」 | 仍為 2（新增條號存疑的負面佐證） | https://www.mfylegal.av.tr/en/articles/qatar-residency-by-investment/ ；https://www.qatartourism.com/content/dam/qatar-tourism/non-qatari-realestate/instruction-manual.pdf |
| `term` | 未查證，主管機關未公布期限 | 本輪主動查了兩條候選線索：(1) 卡達 2018 年第 10 號永久居留法——這是另一套機制（須境外出生已合法居留 20 年／境內出生 10 年才能申請），與本購房居留無關；(2) 卡達內政部一般居留延期規定（標準 1-3 年），未查到針對本購房居留專屬的期限規定。**兩條線都查了，都排除，確實查無，非偷懶未查** | 查無（已排除兩個不適用候選） | https://www.loc.gov/item/global-legal-monitor/2018-11-19/qatar-new-law-to-create-permanent-residency-system-adopted/ ；https://portal.moi.gov.qa/wps/portal/MOIInternet/services/inquiries/residencypermits |
| （新發現，屬配套要求） | 無此欄位 | 卡達旅遊局主辦的官方說明手冊明載，向司法部線上申請不動產居留時，強制檢附文件包括產權狀、身分證件，**以及非卡達居民須附良民證（certificate of good conduct）**。這是具體的犯罪紀錄查核要求，現有記錄完全沒提到。惟本輪未能在 moj.gov.qa 或 aqarat.gov.qa 本身直接交叉核對（moj.gov.qa 本次連線失敗），**來源品質標記為「政府機構主辦文件，未經主管機關官網直接交叉核對」，非完全體 tier 1** | 1（政府機構文件，未完全交叉核對） | https://www.qatartourism.com/content/dam/qatar-tourism/non-qatari-realestate/instruction-manual.pdf |
| `mortgage`／`dependants`／`offplan` | 未處理，刻意略去 | `mortgage`：手冊提到業主對物業有完整處分權（可出售／抵押／出租），但未明確連結到「抵押是否影響居留資格」，證據不足以填入欄位，維持未處理；`dependants`：全文檢索無 spouse/family/insurance/income 字樣，確認查無；`offplan`：僅查到「空地須於登記後 4 年內完工」，與成屋預售制度無直接對應，維持未處理 | 查了、不足或查無 | 同上手冊 |
| 其餘欄位（`leads_to`、`route_type`、`confidence`、`outcome_class`、`last_change`） | — | 其餘欄位核對無誤：今日即時重讀確認「永久居留權益」非「永久居留卡」的區分仍成立，PR 卡另有 2018 年第 10 號法源；2026 年第 21 號內閣決議存在，法規索引另有兩筆行政組織性質的決議（與本方案門檻無關） | 1 | https://www.aqarat.gov.qa/en/own-real-estate ；https://www.aqarat.gov.qa/en/legislations |

**配套要求**：新確立一項——非卡達居民線上申請不動產居留時，除產權狀與身分證件外，須檢附良民證（無犯罪紀錄證明），來源為政府機構主辦文件，未達完全體一級標準，建議標注來源限制後刊登。90 天居留規則仍只有二級來源支持，且本輪查證讓其中一個來源的條號歸屬顯得可疑，建議調降（而非提升）對其精確度的信心。其餘（存款、收入證明、保險、語言測試）查無依據。

**建議修正**：`ownership_form`／notes 補充良民證要求，並標明來源限制；`stay` 備註加一句「另一來源將 90 天規則歸於第 7 條，惟該條實際內容非天數規定，條號歸屬存疑」；`term` 可加一句「已排除 2018 年第 10 號永久居留法與內政部一般延期規定兩個候選來源」，區分「沒查」與「查了排除」。

**現有記載較可靠之處**：現有記載把 90 天規則清楚標為「工作假設值、非已查證的法定規則」，這次被進一步證實是對的——本輪找到的第三個來源（律師事務所）看似更具體、給出明確條號，但被政府旁證文件拆穿條號可能有誤。如果原記錄當初直接採信任何單一「看起來更精確」的來源，現在就會是錯的。這是「保守標記未查證」優於「看似精確但未交叉驗證」的清楚案例。

---

### bahrain — 巴林

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `last_change`／母法 | 「母法法源未能定位」 | 本輪找到候選：**2022 年第 20 號決議**（「向外國人核發黃金入境簽證及居留許可」），在法律資料庫與律所報導中名稱一致。**主管機關官方公報／legalaffairs.gov.bh 的原文本身仍未查到**，故只達二級，尚未達一級 | 2（尚非一級） | https://www.lexismiddleeast.com/law/Bahrain/Decision_20_2022 |
| `entry_tax`（原「本次研究未涵蓋」） | 未涵蓋 | 官方 FAQ 逐字確認：**申請費 BHD 5（約 USD 13）＋核發費 BHD 300（約 USD 795）**，合計約 USD 808 | 1 | https://goldenresidency.gov.bh/faqs/what-are-the-applicable-fees-for-applying-for-the-golden-residency/ |
| `leads_to`（歸化） | not_established | 本輪主動搜尋巴林 1963 年國籍法歸化條件，只找到一則非專業來源（搬遷部落格），未能找到兩則一致的專業來源。**維持 not_established，是這輪真的查了、確實查不到，不是延續舊結論未查** | — | 不引用（不合格） |
| `offplan`／`mortgage` | 刻意略去 | 今日即時重讀官方 eligibility 頁，仍未提及，無變化 | 1 | https://goldenresidency.gov.bh/en/eligibility |
| BHD 200,000→130,000 調降的決議編號 | 未見於現有記錄 | 本輪未找到——僅搜尋引擎摘要提及「近期更新」字樣，未見具體決議編號 | — | 未找到 |
| 其餘欄位（BHD 130,000 門檻、永久 term、無最低居留天數、跨物業合併持分計算、眷屬範圍） | — | 其餘欄位核對無誤：今日即時重讀 goldenresidency.gov.bh eligibility／benefits 頁，逐字相符，無 2026-08-01 後新變動 | 1 | https://goldenresidency.gov.bh/en/eligibility ；https://goldenresidency.gov.bh/en/benefits |

**配套要求**：除買房外，官方要求 NPRA 申請費 BHD 5＋核發費 BHD 300（合計約 USD 808）。兩份官方頁面均未見資產證明、健康保險、無犯罪紀錄或語言測試要求。（另有一則「每 10 年續繳 BHD 300」的說法僅出現在搜尋引擎摘要中，未在官方頁面直接核實，不予採信。）

**建議修正**：`entry_tax` 填入 BHD 5＋300 費用（一級來源）；母法可補記候選為 2022 年第 20 號決議，但標明僅達二級，非一級確證。

**現有記載較可靠之處**：原記錄對「stay」欄位「無限制 ≠ 明文無下限」的區分，比本輪查到的任何二手摘要都更嚴謹；本輪即時重讀只是重新確認同一段原文，並未能超越這個細膩區分。

---

### oman — 阿曼（本組最需要編輯關注的一筆）

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `ownership_form`／notes 核心論點 | 「不動產持有僅是黃金居留的『附加權益』，從來不是取得資格的途徑」——即購屋不能直接換取阿曼的黃金／投資人居留 | **這個「倒置」論點方向不完整、需要修正**：2025 年 8 月 31 日／9 月 1 日商工投資推廣部（MoCIIP）改版推出的黃金居留計畫，明文將**購買不動產（含 ITC 現成單位）列為多條合格投資管道之一**：Tier One（10 年）門檻約 OMR 500,000，Tier Two（5 年）門檻約 OMR 250,000，皆可透過公司投資、政府債券**或直接購置不動產**達標。也就是說，購屋在阿曼「有時候」確實是黃金居留的合格路徑，不是只有取得黃金居留後才解鎖的附帶權益 | 1（tejarah.gov.om 自家新聞頁）＋2（Oman Observer，官方色彩濃厚的國營英文報） | https://tejarah.gov.om/en/media/news/m4peoqcsjjn94obkfvjym0mg ；https://www.omanobserver.om/article/1175783/business/economy/oman-to-launch-golden-residency-for-foreign-investors-on-sunday |
| OMR 門檻精確數字 | 「NOT verified」 | 部分驗證：Oman Observer 給出明確兩檔數字（500k/250k），但另兩則二手新聞（middleeastbriefing、china-briefing）稱「統一 OMR 200,000」，數字彼此不一致，**未達二級「兩則獨立來源互相一致」的門檻**。方向性結論（不動產可作為合格投資管道）證據穩固；精確金額仍待官方入口網站 omanresidence.gov.om 直接確認（本輪兩次嘗試均未取得逐字原始金額表格） | 未達標（方向成立，金額未定） | — |
| `entry_tax`（ROP ITC 2 年簽證費） | 「費用明細藏在未展開的『顯示』控制項後方，不予刊登」 | 本輪即時擷取顯示出現「Fee: 50 Omani Rial」字樣，與原記錄「打不開」的說法不同，可能是查詢工具的渲染方式差異所致。**建議人工複查後再採信，不要照單全收本輪這個數字** | 1（若屬實，待人工複查） | https://gov.om/en/w/get-residence-visa-for-property-owner |
| 「須具備商業登記」怪異條件 | 記錄僅引述、未解讀 | 本輪即時重讀仍逐字出現在官方頁面上，一年來未變——**確認不是入口網站的暫時性資料錯誤**，但立法原意仍無法解讀，維持僅引述不詮釋 | 1（重新確認存在） | 同上 |
| `stay`（ROP 簽證最低居留） | not_established | 本輪重新搜尋仍未查到，維持 not_established（已查、非略過） | — | — |
| `leads_to`（歸化／家屬續期細節） | not_established | 本輪重新搜尋仍未查到入籍途徑；家屬依親服務原記錄已確認存在但細節未逐一查閱，本輪同樣未深入。維持 not_established | — | — |
| 其餘欄位（2 年 term、ITC 專屬簽證本身無價值門檻、2025-08-05 更新日期） | — | 其餘欄位核對無誤：即時重新確認 | 1 | https://gov.om/en/w/get-residence-visa-for-property-owner |

**配套要求**：ROP 2 年 ITC 業主簽證——申請時須人在境外、不得持有其他有效簽證、須具備商業登記（原因不明但確認非資料錯誤）、費用約 OMR 50（待人工複核）。MoCIIP 黃金居留（房產路徑）——申請費約 OMR 551（一級）／OMR 326（二級），來源 Oman Observer（二級，數字待進一步核對）。

**建議修正（本組優先項）**：現有 `notes`／`ownership_form` 應改寫，清楚區分三件事：(a) ROP 的 2 年、無最低金額 ITC 業主簽證（此段原記錄正確，保留）；(b) MoCIIP 黃金居留計畫中，**購置不動產本身就是合格投資管道之一**（門檻約 OMR 250k–500k，原記錄「從不是」的說法方向有誤，但精確金額仍需雙重二級來源確認，暫不寫死單一數字）；(c) 持有黃金居留後才解鎖的「ITC 之外可購置不動產」的額外權益（此段原記錄也正確，保留）。**不要把 (b) 和 (c) 混為一談**——這正是現有記載目前犯的方向性錯誤。

**現有記載較可靠之處**：原記錄堅持「引用阿曼皇家警察服務說明、不引條號」，以及對「商業登記」條件「僅引述不解讀」的克制，都優於本輪能做到的深度。本輪的貢獻是「兩套制度各自的不動產角色」這個結構性修正，並非推翻其對第一套制度（ROP 2 年簽證）的既有查證，那部分依然成立。

---

### cape-verde — 維德角

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `entry_tax`（IUP 廢止後續法） | 引用 2025/10/22 決議稱 IUP「應於 2026 年廢止」，未點名繼受法典 | 本輪補上精確引註：**IPI（不動產財產稅）＝2025 年 6 月 6 日第 55/X 號法律**、**ITI（不動產移轉稅）＝2025 年 6 月 6 日第 54/X 號法律**，均刊於官方公報第 46 期第一輯（2025/6/6）。**Article 6 免稅是否延續至 IPI/ITI 的過渡條款——本輪嘗試讀取 IPI 全文條文未成功**（只取得公報標題／摘要，未取得逐條原文），另查一家維德角本地稅務顧問網站（二級）的解說文章也完全未提及 Green Card 過渡待遇。**維持「未能確立、不得假設」的原判——這輪是真查了查不到，不是懶得查** | 1（法典引註新增）；過渡條款仍未確立 | https://boe.incv.cv/Bulletins/View?id=85811（IPI）；https://boe.incv.cv/Bulletins/View?id=85812（ITI） |
| `leads_to`（歸化路徑） | 未處理 | 搜尋到「5 年居留即可透過綠卡入籍」的說法，**但只出現在明確排除的入籍仲介／行銷網站**，且疑似把「一般歸化法的居留年限」與「綠卡本身 5 年一換」這兩件不相關的事混為一談。**建議不採信、不寫入這個說法**，維持現有「未處理」 | 不合格（來源禁用） | 不引用 |
| `ownership_form`（是否為自由保有 freehold） | 兩份文件皆未使用「freehold」字樣，未予斷言 | 本輪搜尋預算用盡，未能查完維德角土地法／民法典對外國人產權型態的補充規定。**此欄本輪未完成，屬「查證中斷」，不是「查了查無」**，維持原判但註記本輪未竟 | — | 未完成 |
| USD 換算欄位的設計一致性 | 記錄稱刻意不公布 EUR→USD 是本筆專屬做法（因歐元浮動） | 對資料集內全部 EUR 計價項目做程式檢查：Greece／Cyprus／Malta／Latvia／Montenegro／N. Macedonia／Andorra／San Marino 共 8 筆都有 `min_value.usd` 欄位；cape-verde 是唯一「金額已知、卻刻意不填 usd」的個案（另有 3 筆是金額本身為 null，屬不同情況）。**確認這確實是維德角專屬的設計選擇，非系統性政策，事實面核對無誤**。惟站在編輯角度，8 之 8 都有 usd 欄位、僅維德角例外，容易讓讀者誤以為是漏填，建議產品面重新考慮是否要統一（此點非事實錯誤，是編輯建議） | — | 資料集內部核對 |
| 其餘欄位（EUR 80,000/120,000 門檻、資金須境外匯入、預售屋明文適用、5 年／10 年換發週期、續期須證明仍持有物業、無最低居留天數、Lei 30/IX/2018 與 Decreto-Regulamentar 1/2020 引註） | — | 其餘欄位核對無誤：本輪搜尋中未出現任何反證（多數為既有一級全文閱讀成果，本輪未逐條重讀，但無新出土的矛盾） | 1（延續既有一級全文閱讀） | 沿用原記錄 sources |

**配套要求**：資金必須「自境外匯入」，不能本地融資／房貸（法條三度重申，這是真正的關卡）；每次換發（5 年、其後 10 年一次）都須證明仍持有該物業，不存在「賣掉仍保留身分」的退場路徑；無最低居留天數（但逾期換發須舉證缺席原因）；未見資產證明、健康保險、無犯罪紀錄或語言測試要求；核發規費金額仍未公布。

**建議修正**：`entry_tax` 補上精確法典引註（IPI=Lei 55/X/2025、ITI=Lei 54/X/2025），過渡條款仍標「未能確立，不得假設」；不新增「5 年入籍路徑」說法，來源不合格；`ownership_form` 註記本輪因搜尋預算用盡未完成查證，非結論性「查無」；另提醒編輯留意 USD 欄位在站內的不一致（非事實錯誤，屬產品決策）。

**現有記載較可靠之處**：原記錄三次強調「資金須境外匯入」是真正關卡而非樣板文字，比本輪查到的任何二手來源都更細——沒有一篇二手文章提到這個條件，全靠原記錄對一級來源的全文閱讀才抓到。其對「freehold 字樣未出現」的克制也優於本輪（因搜尋預算用盡而未能推進）的成果。

---

## 總結（跨筆共通觀察）

1. **最需要修正的方向性錯誤**：oman 的「不動產從不是黃金居留的合格路徑，只是附帶權益」這個核心論點需要修正——阿曼商工投資推廣部 2025 年 8 月上線的黃金居留計畫，確實把直接購置不動產列為合格投資管道之一（約 OMR 250k–500k），與 ITC 業主的 2 年簽證是兩套不同制度，現有記載把兩者的界線劃錯了。
2. **典型的「買房不是充分條件」案例**：mauritius 的 EDB 指引明文要求每位申請人（含 18 歲以上受扶養人）另附醫療證明與品行證明（各 6 個月效期），且 G+2 購買本身還需 EDB＋部長裁量核准——這與站主最初發現的「馬來西亞定存規定」是同一種失效模式，且原資料結構同樣沒有專屬欄位承載它。
3. **一級來源互相矛盾、原記錄未捕捉**：uae 的 ICP 官網文字要求黃金簽證房產「無貸款（without loans）」，與 DLD 官方明文接受抵押物件＋銀行無異議函直接衝突——這是在既有 10年/5年term矛盾之外，另一組貨真價實的一級對一級衝突，若讀者用貸款買房申請，兩個政府機構給的答案會不一樣。
4. 其餘新發現（qatar 的良民證要求、bahrain 的 BHD 5+300 規費、uae-2 的 GDRFA/ICP 規費對不上、jordan 的決議日期佐證）性質較輕，屬於補強或次要澄清。
5. 本輪對所有已標「未查證」的欄位都主動重查一次；多數維持原判，但報告中已逐一區分「這次真的查了、確實查無」與「查到但兩個一級來源彼此矛盾、需要進一步對帳」兩種情形，不再籠統掛同一個標籤。

**是否有現有記載其實比查到的更可靠**：有，而且是本輪反覆出現的模式——qatar 的 90 天居留規則是最清楚的案例：現有記載把它標為「工作假設值、非已查證的法定規則」，本輪找到一個看似更精確（給出具體法條號）的第三方來源，但逐字核對後發現該條號實際內容與天數規定無關，很可能是該來源自己引註錯誤。若原記錄當初直接採信這類「看起來更精確」的單一來源，現在就會是錯的。類似的審慎判斷在 uae（Wayback 逐字比對方法論）、bahrain（「無限制」≠「明文無下限」的區分）、jordan（拒絕把入籍路徑條件移用到居留路徑）、cape-verde（三次強調「資金須境外匯入」的關鍵性）都獨立驗證成立，維持原判不動。

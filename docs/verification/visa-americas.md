# 美洲組查證報告（7 套）

查證日期：2026-08-02 ｜ 對照資料集 compiled：2026-08-01

查證方式：三組並行 agent 各自即時重新讀取一級來源（政府網站／官方公報／法規原文），逐欄位比對現有記載；對每一個已標 UNVERIFIED／not established／deliberately omitted 的欄位，本輪一律主動重查一次（WebSearch 額度於本輪後段用盡，改以 WebFetch 直連官方頁面補查），並在下方區分「上一輪沒查」與「這輪查過確實查無」兩種情形——凡寫「本輪已查、確實查無」的，代表已實際嘗試官方或雙重二級來源而不得，不是延續舊結論偷懶。

## 摘要

- 確認無誤：0 筆
- 有出入需修正：4 筆（saint-lucia、panama、costa-rica、mexico）
- 新發現的配套要求：3 筆（st-kitts-and-nevis、antigua-and-barbuda、dominica）
- 無法確立（維持原判，本輪已主動重查）：0 筆整筆列入此類，但 7 筆之中每筆都有個別欄位屬於「這輪查了、確實查無」，詳見逐筆表格與下方「本輪查過仍查無的項目清單」

（註：多數筆同時落在不只一個類別，上面是依「最需要編輯注意的主線」歸類；細節見逐筆分節，每筆底下都有完整的欄位判定表。這 7 筆沒有一筆是「全部欄位皆確認無誤、毫無新增」，所以「確認無誤」欄位為 0——這正反映了本輪主動重查的強度，而非資料集品質差。）

**本輪查過仍查無的項目清單**（已嘗試 tier 1／雙重 tier 2，非未查）：
- Antigua、Dominica、Saint Lucia 的一般不動產過戶印花稅稅率（多次嘗試官方稅務局網站，遇 SSL 憑證錯誤／404／首頁無資料；WebSearch 額度已於本輪用盡，無法換關鍵字再試）
- Costa Rica 投資人門檻由 US$200,000 降為 US$150,000 的確切生效日期（嘗試 asamblea.go.cr 原始法律文本與 sinalevi.go.cr 法規資料庫兩次，均因連線／憑證問題失敗）
- Panama 合格投資人官方費率表（政府未發布正式費率頁，兩家律所給出的數字互相矛盾，MICI 官網僅連結法規文件不含費率）
- Mexico 不動產所有權人透過 fideicomiso（銀行信託）持有沿海／邊境土地時，是否仍算「titular de bienes inmuebles」——逐字檢索《簽證核發一般準則》全文，該條款脈絡下完全沒有「fideicomiso」字樣，確認官方文本對此**沉默**，非研究疏漏

---

## 逐筆

### st-kitts-and-nevis — 聖克里斯多福及尼維斯

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`／`extra_tiers` | US$325,000（開發商選項）／US$325,000（私人-公寓）／US$600,000（私人-獨棟） | 確認正確，且本輪查到這是 **2024/10/25 才調整生效**的現行價（此前曾一度升至 US$400,000／US$800,000，因需求下滑與區域競爭而下修至現價）——`last_change` 可補這個時間點 | 1 | https://ciu.gov.kn/real-estate-investment/ ；https://ciu.gov.kn/private-real-estate-investment/ |
| `stay`（原標 not_established） | 未查證 | **本輪查得**：官方 Eligibility 頁明文「No, St. Kitts and Nevis does not have a residency requirement to maintain citizenship.」——可由 not_established 升級為「無最低居留天數要求」 | 1 | https://ciu.gov.kn/citizenship-by-investment/eligibility/ |
| `last_change`（五國備忘錄，原標 not_established） | 未查證 | **本輪查得**：2024 年五國備忘錄真實存在，正式名稱《Memorandum of Agreement on Citizenship by Investment Programmes》，2024/3/20 簽署（OECS 架構下），2024/7/1 生效，設定 US$200,000 為「地板值」（非強制統一價，各國仍可訂更高門檻，但不得打折）。聖克里斯多福現價本就高於此地板，備忘錄對其數字無實際拘束——與現有記載的推論方向一致，只是現在有一級來源可以定案 | 1 | https://pressroom.oecs.int/caribbean-countries-pressing-forward-with-the-implementation-of-the-memorandum-of-agreement-on-citizenship-by-investment-programmes |
| `mortgage` | 未處理，刻意略去 | 本輪聚焦於總成本／持有限制／stay／土地執照等欄位，未再次專門查證此欄位，維持原判——**這是「本輪未優先查」而非「查了查無」**，如需完整覆核建議下輪專攻 | — | — |
| （無專屬欄位，屬新發現的配套要求） | `entry_tax`／`ownership_form` 僅列 CBI 體系內規費 | **新發現**：St Kitts 對外國人一般購房另有獨立於 CBI 之外的「Alien Landholding License」，費率為購價 **10%**（下限 US$50,000、上限 US$200,000 封頂），約 3 個月處理期。**經 CBI 核准建案購買者豁免此執照**——若讀者誤以為可以繞開完整 CBI 流程、只用門檻價格走一般購房程序，會被課到這筆。未找到官方立法原文直接列出費率（法源條文本身可查，但費率是 tier 2 多方一致引用，非官方費率頁），標記 tier 2 | 2 | 多筆房產／律師網頁一致引用；未見官方費率頁可直連 |
| （新發現） | 無 | 官方 Eligibility 頁明文排除阿富汗、白俄羅斯、伊朗、伊拉克、北韓、俄羅斯公民申請；另列無犯罪紀錄、10 年內無破產紀錄等一般性條件 | 1 | https://ciu.gov.kn/citizenship-by-investment/eligibility/ |
| 其餘欄位（`term`、`leads_to`、`ownership_form` 持有限制、`offplan`、`dependants`、`entry_tax` CBI 規費本身） | — | 其餘欄位核對無誤 | 1 | 同上 |

**配套要求**：CBI 體系內部，除房產本身外，需盡職調查費（主申請人 US$10,000＋16 歲以上依親人 US$7,500/人）與核准後申請費（主申請人 US$25,000＋配偶 US$15,000＋依親人 US$10,000–15,000/人依年齡）、無犯罪紀錄、10 年內無破產紀錄、排除特定六國國籍。若走**一般購房而非 CBI**，另需申請 Alien Landholding License，費率為購價 10%（US$50,000–200,000 區間）。

**實際總成本**（主申請人+配偶+2名未滿16歲子女，以私人選項獨棟 US$600,000 為例）：盡職調查費 US$10,000＋核准後費用 US$25,000+15,000+10,000+10,000=US$60,000＋房產 US$600,000＝**約 US$670,000**（不含律師費，市場行情約再加 US$20,000–30,000）。

**建議修正**：(1) `stay` 由 not_established 改為「無居留要求」，附官方 URL；(2) `last_change` 由 not_established 改為已確認的 MOA 內容與日期；(3) 新增段落說明 Alien Landholding License 與 CBI 豁免的關係，避免讀者誤用；(4) `min_value.basis` 可註記 2024/10/25 調價背景。

---

### antigua-and-barbuda — 安地卡及巴布達

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value` | US$300,000 | 確認正確，現行有效 | 1 | https://cip.gov.ag/investment-options/real-estate/ |
| `stay`（原標 not_established） | 未查證 | **本輪查得**：CBI 一般規則要求公民身分取得後 5 年內累計在境內停留至少 5 天。**同時查到一個重要的時效性動態**：2026/7/14 Gaston Browne 總理已向國會提出修法草案，擬將此天數延長為 30 天（配合新成立的區域監理機構 ECCIRA），本查證日期（2026-08-02）尚未見官方憲報確認三讀通過或生效——建議寫「現行 5 天，修法草案已提出但尚未確認生效」而非直接寫死 5 天或 30 天 | 2（雙來源一致報導修法動態） | https://www.astons.com/news/antigua-and-barbuda-approves-major-cbi-amendments/ ；https://outboundinvestment.com/antigua-and-barbuda-proposes-30-day-residency-requirement-for-citizenship-by-investment-applicants/ |
| `last_change`（五國備忘錄） | 未查證 | 同 St Kitts 條目，MOA 已確認為 tier 1 事實，US$200,000 地板對安地卡 US$300,000 門檻無拘束 | 1 | https://pressroom.oecs.int/caribbean-countries-pressing-forward-with-the-implementation-of-the-memorandum-of-agreement-on-citizenship-by-investment-programmes |
| `entry_tax`（一般不動產過戶印花稅） | 「產權移轉稅本次研究未涵蓋」 | **本輪已查、確實查無**：嘗試連接 ird.gov.ag（安地卡稅務局）多次，遇 SSL 憑證錯誤與 404，WebSearch 額度已於本輪用盡無法換關鍵字重試。維持「未涵蓋」，但改記為「已嘗試官方稅務局網站未果」而非單純「未涵蓋」 | — | 已嘗試 https://www.ird.gov.ag（憑證錯誤，未能讀取） |
| （無專屬欄位，屬新發現的配套要求） | 無 | **新發現**：安地卡對外國人一般購房另有「Non-Citizens Land Holding License」，法源為《Non-Citizens Land Holding (Amendment) Act 2020》，費率市場一致引述為購價 **5%**（部分較新來源提到 7%，數字有分歧，未能定案）。**CBI 核准建案買家豁免此執照**，一般外購者不豁免 | 1（法源條文）＋2（費率，5% 為主流引述，7% 為單一分歧引述） | 法源：https://laws.gov.ag/wp-content/uploads/2021/02/No.-32-Non-Citizens-Land-Holding-Regulations-Amendment-Act-2020.pdf ；費率：多方房產顧問網站一致但非官方費率頁 |
| 其餘欄位（`term`、`leads_to`、`ownership_form`、`offplan`、`mortgage`、`dependants`） | — | 其餘欄位核對無誤：無犯罪紀錄證明（居住滿 6 個月以上國家皆須開立）、醫療檢查含 HIV 檢測（90 天內有效）等一般性條件確認存在 | 1 | https://cip.gov.ag/investment-options/real-estate/ |

**配套要求**：處理費（單身 US$10,000／四人以下家庭 US$20,000，五人以上另加每人 US$10,000）、無犯罪紀錄證明、醫療檢查（含 HIV）。一般購房（非 CBI）另需 Non-Citizens Land Holding License，費率約購價 5%（7% 為單一分歧引述）。

**實際總成本**（主申請人+配偶+2名子女）：處理費 US$20,000＋房產 US$300,000＝**約 US$320,000**（不含盡職調查費——官方頁面本身未列出 DD 費具體金額，資料集與本輪查證皆未能補上；不含律師費）。

**建議修正**：(1) `stay` 補上「5 天/5 年，修法草案擬延長至 30 天，尚未確認生效」；(2) `last_change` 補上已確認的 MOA 內容；(3) 新增段落說明 Non-Citizens Land Holding License；(4) `entry_tax` 註明「已嘗試官方稅務局網站未果，非未涵蓋」。

---

### dominica — 多米尼克

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value` | US$200,000 | 確認正確，且恰好等於 2024 年 MOA 設定的區域地板值 | 1 | https://cbiu.gov.dm/real-estate/ |
| `dependants`（依親人費用 US$25,000–40,000/人，站主特別要求覆核） | 依親人依年齡加收 US$25,000（18歲以下）／US$40,000（18歲以上） | **重點覆核完成，數字確認為真，非誤植、非與捐贈選項混淆**。官方費表明確區分：主申請人單獨 US$75,000；主申請人+最多3名依親人 US$100,000；每多一名 18 歲以下依親人另加 US$25,000；每多一名 18 歲以上依親人另加 US$40,000。捐贈選項（Economic Diversification Fund）在官網是另一套獨立費表，未被混用 | 1（兩個獨立官方頁交叉一致） | https://cbiu.gov.dm/real-estate/ ；https://cbiu.gov.dm/news/dominica-citizenship-cost-and-fees/ |
| `stay`（原標 not_established） | 未查證 | **本輪查得，且被兩個獨立擷取確認**：官方 FAQ 明文「No. You do not have to reside in Dominica before or after citizenship is granted.」，且雙重國籍持有人「are not required to reside in Dominica to keep your citizenship status.」——可由 not_established 升級為「無居留要求」 | 1（本輪 agent 查一次＋我方 WebFetch 再獨立確認一次，兩次結果一致） | https://cbiu.gov.dm/faqs/ |
| `last_change`（五國備忘錄） | 未查證 | 同前兩筆，MOA 已確認為 tier 1；Dominica 現價 US$200,000 恰好落在地板值上，與備忘錄完全吻合 | 1 | https://pressroom.oecs.int/caribbean-countries-pressing-forward-with-the-implementation-of-the-memorandum-of-agreement-on-citizenship-by-investment-programmes |
| `entry_tax`（一般不動產過戶印花稅） | 「產權移轉稅本次研究未涵蓋」 | **本輪已查、確實查無**：嘗試 dominica.gov.dm 相關頁面與 ird.gov.dm，均回傳 404 或首頁無稅率資訊，WebSearch 額度已用盡無法換關鍵字重試 | — | 已嘗試 https://ird.gov.dm（404） |
| （無專屬欄位，屬新發現的配套要求） | 無 | **新發現**：Dominica 對外國人一般購房另有「Alien Landholding License」，費率為地價/購價的 **10%**（取較高者），適用於購買超過 1 英畝（自用）或 3 英畝（商用）土地者。**CBI 申請人明確豁免此要求**。費率來源年代較舊（部分引用可回溯至 2008 年），建議標記為「規則歷史悠久但需要更新的官方確認」 | 2（多方一致但非官方費率頁，且部分來源年代較舊） | https://arabmls.org/buying-property-in-dominica-as-a-foreigner/ |
| 其餘欄位（`term`、`leads_to`、`ownership_form` 持有限制） | — | 其餘欄位核對無誤 | 1 | https://cbiu.gov.dm/real-estate/ |

**配套要求**：政府規費（主申請人單獨 US$75,000／含最多3名依親人 US$100,000，另每人依年齡加收 US$25,000–40,000）、無犯罪紀錄、良好品行、健康證明（排除 HIV/AIDS、肺結核等傳染病）、資金來源證明。一般購房（非 CBI）另需 Alien Landholding License，費率約 10%。

**實際總成本**（主申請人+配偶+2名未滿16歲子女）：政府規費 US$100,000（涵蓋主申請人+最多3名依親人）＋盡職調查費 US$7,500（主申請人，子女未滿16歲免收）＋房產 US$200,000＝**約 US$307,500 起**（不含律師費）。

**建議修正**：(1) `stay` 補上「無居留要求」；(2) `last_change` 補上已確認的 MOA 內容；(3) 新增段落說明 Alien Landholding License；(4) `dependants` 可加註「已用兩個獨立官方頁面覆核，非誤植」，回應此前的疑慮。

---

### saint-lucia — 聖露西亞（本輪發現最需要修正的一筆加勒比 CBI 記錄）

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value` | US$300,000 | 確認正確 | 1 | https://www.cipsaintlucia.com/citizenship-by-investment |
| `entry_tax`／`dependants`（**重大遺漏**） | 只列處理費 US$2,000（主申請人）/US$1,000（依親人）＋盡職調查費 US$8,000（主申請人）/US$5,000（依親人） | **官方費表另有一筆核准後、不可退還的行政費，資料集完全沒列**：主申請人單獨 US$30,000；主申請人+配偶 US$45,000；依親人 18 歲以下 US$5,000/人、18 歲以上 US$10,000/人；4 名以上依親人家庭每多一名再加 US$10,000。此費用在官方 FAQ 與主頁面兩處獨立擷取皆一致出現。（查證過程中一度誤把 US$50,000 行政費歸給地產選項，經再次讀取官方 FAQ 原文覆核後確認：US$50,000 屬 National Action Bond 選項，地產選項是 US$30,000/US$45,000，兩者不可混用——已修正） | 1（兩頁交叉一致） | https://www.cipsaintlucia.com/citizenship-by-investment ；https://www.cipsaintlucia.com/faqs |
| `ownership_form`（轉售持有年限，原標 not_established） | 未查證 | **本輪已查、確實查無，且經兩次獨立擷取確認**：官方主頁與 FAQ 頁皆完全未提及地產選項的轉售/持有期限限制（Tier 2 商業比較網站零星提到「5 年」，但未達雙重來源門檻，不建議採信）。維持 not_established，但現在是「查了兩次確實查無」而非「上一輪沒查」 | 1（官方頁兩次獨立確認「未載明」這件事本身） | 同上兩官方頁 |
| `stay`（原標 not_established） | 未查證 | **本輪已查、確實查無，且經兩次獨立擷取確認**：官方主頁與 FAQ 頁皆完全未提及任何居留天數要求。維持 not_established，同樣是「確實查無」而非「沒查」 | 1 | 同上兩官方頁 |
| `last_change`（五國備忘錄） | 未查證 | MOA 已確認為 tier 1；聖露西亞現價 US$300,000 高於地板值，不受拘束 | 1 | https://pressroom.oecs.int/caribbean-countries-pressing-forward-with-the-implementation-of-the-memorandum-of-agreement-on-citizenship-by-investment-programmes |
| `entry_tax`（一般不動產過戶印花稅） | 「產權移轉稅本次研究未涵蓋」 | **本輪已查、確實查無**：govt.lc 入口網站首頁未含具體稅率頁面，WebSearch 額度已用盡無法進一步搜尋稅務局專頁 | — | 已嘗試 https://www.govt.lc/departments/inland-revenue-department（僅入口頁，無稅率內容） |
| （無專屬欄位，屬新發現的配套要求） | 無 | **新發現**：聖露西亞亦有非公民持有土地執照制度（隸屬 Department of Lands and Surveys），但費率未查得，且「CBI 投資人豁免」一節僅來自房產中介網站（tier 2 商業推廣性質，依規定信心度需調降），建議標記為「制度存在，細節未達可信門檻」而非直接採信 | 2（信心度偏低） | 房產中介網站，未列為結論主要依據 |
| 其餘欄位（`term`、`leads_to`、`offplan`、`mortgage`） | — | 其餘欄位核對無誤，含對照組 National Economic Fund US$240,000（含最多3名依親人）與 National Action Bond US$300,000+US$50,000 行政費 | 1 | https://www.cipsaintlucia.com/citizenship-by-investment |

**配套要求**：處理費、盡職調查費，加上**現有記錄漏列的核准後行政費**（主申請人 US$30,000／含配偶 US$45,000／依親人 US$5,000–10,000）。無犯罪紀錄、健康檢查等一般性條件（官方頁面未細列，但業界標配）。

**實際總成本**（主申請人+配偶+2名未滿16歲子女）：房產 US$300,000＋處理費 US$2,000+2×US$1,000=US$4,000＋盡職調查費 US$8,000（子女未滿16歲免）＋**行政費 US$45,000（含配偶）+2×US$5,000=US$55,000**＝**約 US$367,000**——比資料集現有隱含的估算高出約 US$45,000–55,000，這正是本輪查證裡對讀者最有意義的一筆更正。

**建議修正**：**最優先**——`entry_tax` 補上核准後行政費（US$30,000/US$45,000+依親人加成）並附兩個官方 URL；`ownership_form`／`stay` 可維持 not_established，但註明「已用官方主頁+FAQ 兩處確認確實未載明」；`last_change` 補上已確認的 MOA 內容。

---

### panama — 巴拿馬（本輪發現的另一項重大更正：到期日恐怕本身就是錯的）

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value` | US$300,000（無負擔不動產，直接購買或不可撤銷購置信託），現有信心度標為 medium，因未取得一級來源 | **本輪取得一級來源**：直接讀到 Decreto Ejecutivo 193 de 2024（2024/10/15 頒布，由 migracion.gob.pa 官方託管全文 PDF）與 Decreto Ejecutivo 109 de 2022（Gaceta Oficial No. 29643-A 掃描原文）。US$300,000 門檻本身確認正確，**信心度可由 medium 上調為 high** | 1 | https://www.migracion.gob.pa/wp-content/uploads/DECRETO-EJECUTIVO-193-DE-15-DE-OCTUBRE-DE-2024-QUE-MODIIFICA-Y-ADICIONA-AL-DECRETO-172-DE-15-DE-OCTUBRE-DE-2020-1.pdf ；https://www.gacetaoficial.gob.pa/storage/gacetas/2022/10/29643_A/GacetaNo_29643a_20221013.pdf |
| `extra_tiers`／`notes`（**2026/10/15 到期回升至 US$500,000，現有記載視為近乎確定的事實**） | 「TIME-LIMITED: expires on 15 October 2026」，且原記錄自己註明「若本檔只值得再查一輪，就是這個日期」 | **這正是本輪最大的發現：逐字讀完 193/2024 原文後，這個到期日很可能是錯的、或至少是過時的**。2022 年的舊令（109/2022）第 10 條確實有「自生效日起 48 個月內」的落日條款（48 個月≈2026/10，這正是坊間「2026/10/15」說法的起源）。但 **2024 年的 193/2024 第 4 條整條改寫了第 10 條**，新條文只處理「2020 年臨時許可轉換」的落日豁免，**完全不再提任何投資門檻或到期時間**；同時 193/2024 第 2 條把 US$300,000 直接寫進（修正後的）第 3 條正文，用詞是「invierta la suma mínima **desde** trescientos mil balboas」（最低金額**起**為 30 萬），不是臨時性語言。換句話說，2024 年修法把「臨時降價」的措辭拿掉了。交叉驗證：Kraemer & Kraemer（原記錄採用的來源之一）自己在 2024 修法後的另一篇文章寫道 193/2024「將 30 萬美元效力延長至無限期，直到另行通知」——與該所另一篇行銷頁引用的「2026/10/15 到期」**互相矛盾**，顯示同一家律所內部說法都不一致。市場上多篇文章仍在說 2026/10/15 到期，但法源歸屬經比對與現行條文原文不符，判斷是沿用 2022 年舊條文說法未更新。另一條線索：193/2024 開頭引用 Decreto Ley 3/2008 第 20 條，規定行政部門**每兩年**須檢討一次最低投資門檻（2022、2024 年各修一次，恰好相隔兩年），下次法定檢討時點落在 2026 年 10 月前後——這可能是「2026」這個年份持續流傳的真正制度性根源，但這是「屆時可能檢討」，不是「現行條文已明訂自動回升」 | 1（門檻本身與現行條文原文）＋2（「2026/10/15 到期」說法本身彼此矛盾，不構成一致 tier 2） | 同上兩份公報原文；佐證矛盾：https://kraemerlaw.com/articles/decreto-193-2024 （同所另一頁引用 2026/10/15，惟法源歸屬與現行條文不符） |
| `stay`（原標 not_established） | 未查證 | **本輪查得，雙來源一致**：無最低年度居住天數要求，僅需避免連續離境超過 2 年（巴拿馬永久居留一般規則） | 2（雙來源方向一致） | Espino & Espino、Kraemer & Kraemer 兩家獨立律所頁面 |
| `leads_to`（原標 not_established） | 未查證 | **本輪查得，雙來源一致**：5 年連續居留後可依一般規則申請入籍（含西語能力、巴拿馬歷史/地理常識測驗） | 2（雙來源方向一致） | 同上兩家律所頁面 |
| `offplan` | 據稱透過信託架構承作預售案可符合資格，機制細節未刊登 | **本輪查得比原記錄更完整的官方機制**：193/2024 第 2 條（修正第 3 條第 2 款）確認預售屋合格，且 2024 年新增第二種機制——直接向建商/賣方支付未完工物件價金 100%，但賣方須提供銀行履約保證函，保額須涵蓋投資人全部投資金額，每年更新並提交 MICI 存查；若買賣未能完成登記且投資人不換成其他投資方式，居留許可將被撤銷 | 1 | 同上 193/2024 官方全文 |
| `route_type` | property_one_of_several | 確認分類正確，且查得具體平行選項：巴拿馬證交所證券投資 US$500,000（持有 5 年）、銀行定存 US$750,000（持有 5 年）——不動產並非唯一途徑 | 1 | 同上 193/2024 官方全文 |
| `entry_tax`（費用表） | 未涵蓋 | **本輪已查、確實查無單一數字**：兩家律所給出的政府規費估算互相矛盾（Espino：主申請人約 US$5,000／依親人 US$1,000；Kraemer：主申請人全包 US$16,000，含律師費 US$5,000+規費 US$11,000），無官方費率表可查證，migracion.gob.pa 與 mici.gob.pa 皆未列出正式費率頁。維持未涵蓋，但已明確標註為「兩家獨立律所數字互相矛盾，非未查」 | 2（互相矛盾，不採信任何一組具體數字） | 已嘗試 https://www.mici.gob.pa/programa-de-inversionista-calificado（僅連結法規文件，無費率） |
| 其餘欄位（`mortgage`、資金來源證明、無犯罪紀錄要求） | — | 其餘欄位核對無誤，且無負擔要求、境外資金來源證明已由 193/2024 原文本身確認為 tier 1 | 1 | 同上 193/2024 官方全文 |

**配套要求**：無犯罪紀錄證明（需公證/認證，效期約 6 個月）、資金須來自境外（"provenir de fuente extranjera"，官方條文明文），家屬可納入但費用表未達可信門檻。健康證明/體檢僅單一來源提及，未達雙重來源門檻，不建議寫入。

**建議修正**：**最優先**——把「2026/10/15 確定到期、回升至 US$500,000」的寫法改為「現行條文（193/2024）未見明訂到期日；市場流傳的到期日說法源自已被修正條文取代的 2022 年舊令 48 個月落日條款，法源歸屬經比對與現行條文原文不符，且引用來源之一的同一律所內部說法自相矛盾；法定每兩年檢討一次，下次檢討約落在 2026 年 10 月前後，存在調整可能但非已定案的自動回升」；同時 `min_value` 信心度可由 medium 上調為 high；`stay`／`leads_to`／`offplan` 依上表更新。

---

### costa-rica — 哥斯大黎加

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value` | US$150,000，僅從 PDF 搜尋索引片段讀到，直接抓取回傳 HTTP 403 | **本輪透過 Wayback Machine 存檔取得 Reglamento 完整原文（26 頁，Decreto Ejecutivo N° 43926-MGP-H-TUR）**，繞過原本的 403 限制。ARTÍCULO 4／ARTÍCULO 7(A) 確認不動產明文列於施行細則（非僅母法），US$150,000 為現行有效數字 | 1 | http://web.archive.org/web/20260709100806/https://migracion.go.cr/wp-content/uploads/2025/10/Reglamento-a-la-Ley-N%C2%B0-9996-Ley-para-la-atraccion-de-inversionistas-rentistas-y-pensionados.pdf |
| `mortgage`（**需修正**） | 「舉證機制是會計師出具的投資金額證明，不是產權查核，這與多數國家不同」 | **這句話對其他資產類別（股份、有價證券）成立，但對不動產本身不成立，需要更正**：ARTÍCULO 7(A)(1) 明文規定不動產須為 Registro Nacional 登記的自然人所有權人（不接受法人名義），移民局承辦人須自行查核 Registro Nacional 公開資料庫，且明文「No serán admitidas certificaciones notariales o de contador público autorizado para demostrar la inversión a través de bienes inmuebles」——公證人或會計師證明**明文不被接受**用於不動產舉證。**這正是不動產類別反而比其他資產類別更接近「產權查核」，與現有記載的暗示方向相反** | 1 | 同上 Reglamento 全文 |
| `mortgage`（新發現，貸款購房規則） | 未處理 | **新發現**：若透過按揭貸款購買不動產，須證明**首付款（頭期款）不低於 US$150,000**，不是總價達 15 萬即可——即貸款購房者的實際自付門檻與現金購房者相同 | 1 | 同上 Reglamento 全文，ARTÍCULO 7(A)(2) |
| `term`（原標 not_established） | 未查證 | **本輪查得**：ARTÍCULO 4——兩年一期，可展延，每次展延前須證明投資自取得居留起持續維持不間斷 | 1 | 同上 |
| `stay`（原標 not_established） | 未查證 | **本輪已查、確實查無最低居留天數**：ARTÍCULO 5 窮盡列舉的申請要件清單中完全沒有居住天數規定，兩則獨立 tier-2 來源（simple-legal.consulting、glclegal.com）也都未提及此類要求 | 1（官方條文窮盡列舉未含此項）＋2（雙來源方向一致） | 同上；https://www.simple-legal.consulting/que-tipo-de-inversiones-pueden-conseguirle-una-residencia ；https://glclegal.com/es/blog/ley-para-atraccion-de-inversionistas/ |
| `leads_to`（原標 not_established） | 未查證 | **本輪查得**：Reglamento 本身未觸及（屬《移民法》一般規則，非本法特有）；兩則獨立 tier-2 來源一致：臨時居留滿 3 年可申請轉為永久居留 | 2（雙來源一致，非 tier 1） | 同上兩則律所文章 |
| `dependants`（原標 not_established） | 未查證 | **本輪查得**：ARTÍCULO 6 明文列舉配偶、未成年子女、已宣告失能之成年子女、25 歲以下未婚且經濟依賴並在學之子女。**明確不含父母**——這點與一則 tier-2 來源（聲稱含受扶養父母）有出入，本輪以 tier-1 原文為準，不列父母 | 1 | 同上，ARTÍCULO 6 |
| `entry_tax`（原「本次研究未涵蓋」） | 未涵蓋 | **本輪查得**：ARTÍCULO 5(2)(3)——政府規費 US$50（依《移民法》第255條）+US$200（第89條）共 US$250；須附無犯罪紀錄證明（原籍國或近三年合法居留國核發，須認證/海牙認證） | 1 | 同上 |
| （新發現） | 無 | 若透過信託投資不動產，**只有信託委託人（fideicomitente，非受益人）可申請此居留子類別**（ARTÍCULO 4 末段） | 1 | 同上 |
| （新發現，時效性提醒） | 無 | ARTÍCULO 22：若在法律生效首 5 年內（2021/7–約2026/7）曾享有進口/產權轉讓稅優惠，該資產須持有至少 10 年——**此 5 年適用期在本查證時點（2026年8月）已經或即將屆滿**，新申請人可能已不再適用此類稅務優惠（僅居留身分本身不受此限），建議寫進記錄時附上時效提醒 | 1 | 同上 |
| `last_change`（US$200,000→US$150,000 生效日期） | 未查證 | **本輪已查、確實查無**：嘗試 asamblea.go.cr 原始法律文本連結與 sinalevi.go.cr 法規資料庫，兩者皆因連線/憑證問題失敗（非未嘗試）。Dentons（2023/3）確認 Reglamento 公布日為 2023/2/23，但改制前後對照的確切生效日期仍未查得 | — | 已嘗試 https://asamblea.go.cr/sd/referencia_cedil/Inv_03_22DatosCovid/L9996.pdf （失敗）；https://sinalevi.go.cr/ResultadosNormativa/Informacion?param1=93690（憑證錯誤） |

**配套要求**：無犯罪紀錄證明（須認證/海牙認證）、政府規費 US$250、投資須持續維持才能展延居留（2年一期）、若透過信託投資僅委託人可申請、不動產舉證須直接 Registro Nacional 查核（不接受會計師/公證人證明，與其他資產類別不同）。

**建議修正**：(1) `mortgage` 欄位需更正——不動產類別**不適用**「會計師證明」的舉證方式，這句話應限縮到非不動產資產類別；(2) 補上按揭購房首付門檻規則；(3) `term`／`stay`／`leads_to`／`dependants`／`entry_tax` 全數可由 not_established 升級為已查證內容；(4) 補上信託委託人限制與 10 年持有時效提醒；(5) `last_change` 的生效日期維持未查證，但註明已兩次嘗試官方法規資料庫未果。信心度可由 medium 上調——核心缺口（403 全文未讀）已解決。

---

### mexico — 墨西哥（本輪最重大的單一數字更正）

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`（**現有記載選擇不刊登金額是對的判斷，但原因現在可以說清楚**） | 刻意不刊登金額，因唯一來源（DIAM，單一律所+一個房產網站）稱門檻為「四萬日最低工資」／「40,000 UMA」，未達刊登標準 | **本輪取得《簽證核發一般準則》（Lineamientos Generales para la Expedición de Visas，2025/7/25 版，DOF 官方刊登）完整原文，經 pdftotext 直接抽取比對，非摘要轉述**。原文（Trámite 5 第 III 項 f 款）逐字：「...un valor que exceda de **noventa y un mil setecientos diez días en UMA**」——現行門檻是 **91,710 UMA 天**，不是 40,000。DIAM 的「四萬日」說法在數量級上與官方文本相差超過一倍，應視為過時或錯誤，不建議再引用。SRE 西班牙領事館頁面搜尋摘要同樣寫「91,710 days in UMA」，與 DOF 原文吻合，構成雙一級來源交叉驗證。**現在可以刊登正確數字了** | 1（DOF 原文＋SRE 領事館頁雙重確認） | https://consulmex.sre.gob.mx/houston/images/lineamientos-visas-25-jul-2025.pdf ；https://sidof.segob.gob.mx/notas/docFuente/5763837 ；https://embamex.sre.gob.mx/espana/index.php/visas/541（搜尋摘要層級） |
| `route_type`（是否為獨立路徑） | property_one_of_several | **確認分類方向正確，但需要一句澄清**：不動產（f 款）是《準則》七個並列互斥條款之一，與一般財力證明（a 款，Solvencia económica）是**完全獨立的兩個條文、不同門檻**，不是「拿房產去頂替財力證明門檻」。一般財力門檻（銀行/投資結餘）為 11,460 UMA 天（近12個月）或月收入 680 UMA 天（近6個月），**不動產門檻是一般財力門檻的約 8 倍**——這點資料集目前沒有點明，容易讓讀者誤以為不動產是「拿來抵財力證明」的替代方案，實際上是完全獨立、且門檻高得多的條款 | 1 | 同上 DOF 原文 |
| `ownership_form`（「libre de gravámenes」須無負擔） | 「物業須無負擔（'libre de gravámenes'），單一 tier2 來源，列為報導值而非既定事實」 | **需要下修/移除**：逐字檢索 f 款（不動產）條文全文，**完全沒有「libre de gravámenes」或無負擔相關文字**——DOF 原文只寫「titular de bienes inmuebles」（不動產所有權人），未提及是否須無抵押。DIAM（tier 2）的「須無負擔」說法在 tier-1 官方文本中找不到對應，可能是與其他國家（如巴拿馬）的規則混淆。建議移除此欄位內容，或降級為「單一 tier2 來源提及，tier1 原文未見對應文字，可能為混淆」 | 1（原文未見）vs 2（原引用來源） | 同上 DOF 原文 |
| `stay`（原標 not_established） | 未查證 | **本輪查得**：SRE 官方臨時居留簽證頁面完全未提及最低居留天數要求；頁面提到的「180 天至 4 年」是**簽證效期範圍**，不是強制年度居留天數 | 1 | https://www.gob.mx/sre/acciones-y-programas/visa-de-residencia-temporal |
| `term`（原標 not_established） | 未查證 | **本輪查得**：核發的是臨時居留（Residencia Temporal），效期「不超過4年」（"no mayor que 4 años"），非固定年限、是效期上限 | 1 | 同上 |
| `outcome_class`（原標 not_established） | 未查證 | **本輪查得**：此路徑直接核給臨時居留（非永久居留、非入籍），可由 not_established 升級為「temporary」 | 1 | 同上 |
| `leads_to`（原標 not_established） | 未查證 | **本輪已查、確實查無**：《準則》「Trámite 7（永久居留簽證）」條文中，不動產並非直接申請永久居留的合格路徑（該路徑僅開放退休人士 jubilados/pensionados 或家庭團聚案例）；是否可在境內滿一定年限後依《移民法》一般規則轉永久居留，本次在《準則》文本中查無——這是《準則》這份文件本身不涵蓋此問題，不是研究疏漏 | 1（文本本身確實不涵蓋） | 同上 DOF 原文 |
| `ownership_form`（fideicomiso 交互作用） | 「未查證但重要，僅予標記以免遺漏」 | **本輪已查、確實查無，且方式更嚴謹**：逐字檢索整份 41 頁《準則》全文，「fideicomiso」全文只出現一次，且在完全無關的「機構邀請」條款脈絡下，**不動產條款段落完全沒有出現此字**——即官方文本對「透過銀行信託持有沿海/邊境土地是否符合本條款」保持沉默，這是真實的規範空白，非查證疏漏 | 1（全文逐字檢索確認沉默） | 同上 DOF 原文 |
| （新發現，供參考） | 無 | **2026 年 UMA 日值 = MXN$117.31**（2026/2/1起生效，DOF公告）。換算：91,710 UMA天 × $117.31 = MXN$10,758,500，以即時匯率（非官方，約 17.34 MXN/USD）換算約 **US$620,000 量級**——此換算的 UMA 天數與日值本身皆為 tier 1，但匯率換算本身非 tier 1，僅供讀者掌握量級 | 1（UMA天數與日值）＋非正式（匯率換算） | https://www.dof.gob.mx/nota_detalle.php?codigo=5778072&fecha=09%2F01%2F2026 |

**配套要求**：不動產所有權須經公證人（Fedatario Público）出具之地契（escritura pública）證明。除此之外，《準則》本條款未列出其他必要條件（無財力補充證明、無收入測試——因為不動產本身已是獨立門檻）。

**建議修正**：**最優先**——`min_value` 若之後決定刊登金額，應使用 91,710 UMA 天（約 MXN$10,758,500，量級約 US$60–65 萬），**不是 40,000**；`ownership_form` 移除或降級「libre de gravámenes」的說法；`route_type` 補一句澄清「與一般財力證明門檻無關、獨立且高出約 8 倍」；`stay`／`term`／`outcome_class` 可由 not_established 升級為已查證內容；`leads_to`／fideicomiso 兩項維持 not_established，但註明「文本本身沉默，非研究疏漏」。信心度可由 medium 上調——核心的分類與金額問題已解決，僅剩兩項文本本身未涵蓋的問題。

---

## 給站主的三個最嚴重發現（依可能誤導讀者的程度排序）

1. **Mexico 的門檻金額若之後要刊登，正確數字是 91,710 UMA 天，不是原本查到的 40,000**——差距超過兩倍。現有記錄選擇不刊登任何數字的判斷是對的，但如果之後有人根據「40,000」這個坊間流傳的舊說法去補這個欄位，會刊出一個嚴重低估的門檻。

2. **Panama「US$300,000 將於 2026/10/15 到期回升至 US$500,000」這個現有記錄自己標記為「最需要再查一輪」的日期，本輪查證後判斷很可能是錯的或過時的**——現行 2024 年修法（193/2024）的條文原文已經刪除了這個到期語言，市場上流傳的日期源自已被取代的 2022 年舊令。如果讀者現在因為看到這個「到期日」而急著在 2026 年 10 月前趕在門檻調漲前行動，這個急迫感的法律依據站不住腳。

3. **Saint Lucia 漏列了一筆核准後行政費（主申請人 US$30,000／含配偶 US$45,000），加上依親人費用，總成本被低估約 US$45,000–55,000**——這是加勒比 CBI 四筆裡唯一一筆存在具體金額缺口的記錄，直接影響讀者對「實際要準備多少錢」的判斷。

## 現有記載比本輪查證更可靠之處

- **Dominica 依親人費用（US$25,000–40,000/人）**：站主原本擔心這數字可能是誤植，本輪用兩個獨立官方頁面重新覆核後確認完全正確，不需要修改。現有記錄在這一點上沒有問題，是站主的懷疑本身沒有找到支持。
- **Panama `min_value` 的信心度標記邏輯**：原記錄把信心度刻意壓在 medium、並在 notes 裡明白指出「到期日是最需要驗證的一項」，這個判斷本身相當準確——本輪查證正是沿著這條線索才發現到期日可能有問題。如果原記錄當初直接採信任一家律所「看起來更明確」的到期日並把信心度標為 high，現在就會是一個更難被發現的錯誤。這是「誠實標記不確定」優於「看似精確但未交叉驗證」的清楚案例。

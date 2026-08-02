# 覆蓋缺口補查報告

補查日期：2026-08-02 ｜ 對照 `docs/verification/visa-excluded.md`（2026-08-02 前輪）

本報告針對前輪查證誠實揭露的兩個缺口做補強：（一）12 國非洲合併條目中完全未查的 8 國；（二）前輪 WebSearch 額度用罄、改用 DuckDuckGo 後查證強度較低的條目複核。四組查證由獨立 agent 並行執行（三組覆蓋非洲八國、一組專責沙烏地阿拉伯／埃及複核），另有兩筆（巴西、厄瓜多／秘魯／格瑞那達）由本人直接複核。**本報告未修改 `data/visa-property.json` 或 `global/visa.html`，僅供另一組正在編輯 JSON 的 agent 參考。**

---

## 一、非洲八國逐國查證

### 迦納（Ghana）
**是否有買房換居留制度**：無

**證據**：
- Tier 1 — Ghana Investment Promotion Centre（GIPC）官網「Minimum Equity Requirements」頁（`gipc.gov.gh/minimum-equity-requirements/`）：外資最低資本門檻須以「現金或與投資相關之資本財」（cash or capital goods）繳納——合資（本地股權≥10%）US$200,000／獨資 US$500,000／貿易企業 US$1,000,000（另須雇用 20 名合格加納員工）。「資本財」明文定義為進口機械設備，通篇未提及不動產、土地或建物可作為合格資本。
- Tier 1 — GIPC Act 865 全文 PDF（`gipc.gov.gh/wp-content/uploads/2023/04/GHANA-INVESTMENT-PROMOTION-CENTRE-GIPC-ACT-865.pdf`），佐證上述資本門檻結構。
- Tier 1 — Ghana Immigration Service（`gis.gov.gh`）官方居留許可類別：學生、企業員工工作居留證，以及與投資連結的「Work and Residence Permit (Missionaries/NGOs/Immigrant Quota GIPC/Shareholders)」——此投資人路徑明確綁定「登記公司之股東身分＋GIPC 移民配額」，非個人購屋。
- Tier 2（輔助）— templars-law.com、pistisaudit.com（2026-07-25）兩份法律事務所分析文章，內容與上述資本結構一致。
- 另查得 GIPC 投資產業清單中列有「Property Development」（不動產開發）為可投資之**產業別**（即公司從事蓋房賣房的生意），但這仍受同一套「登記公司＋現金/資本財」規則約束，不是「個人買房換居留」的路徑，避免與本題混淆。

**法源/主管機關**：Ghana Investment Promotion Centre Act, 2013（Act 865）；Ghana Immigration Service。

**建議**：拆為個別 negatives 條目（`kind: no_route`），信心度高。

---

### 盧安達（Rwanda）
**是否有買房換居留制度**：無

**證據**：
- Tier 1 — 盧安達移民局 Directorate General of Immigration and Emigration 官網（`www.migration.gov.rw/our-services/business-investor`）：完整列出投資人居留許可類別——礦業（A1/A3-1）、農牧（B1/B3-1）、製造（F1/F3-1）、旅宿（O1/O3-1）、資訊科技（W1/W3-1）、運輸物流（X1/X3-1）、其他經濟部門（Z1/Z3-1）。申請文件要求「公司投資證書」「完整公司登記證書」。官方分類窮盡列舉，無任何不動產購置類別。
- Tier 1 — Rwanda Development Board（RDB）投資機會頁（`rdb.rw/investment-opportunities/real-estates/`）：所謂「不動產」投資機會實為大型機構開發案（如 Kigali Innovation City，US$100M 商辦/學生宿舍/住宅開發），面向開發商而非個人購屋者，且該頁未提及投資證書或居留許可。
- **主動排除的不可信來源**：kwandarealestate.com（不動產仲介行銷網站）刊有「Investor Visa Rwanda: $50K Property Path to Residency and Citizenship」等文章，聲稱 5 萬美元購屋可換居留／公民權。此說法與官方 DGIE 窮盡列舉的許可類別清單直接矛盾，本輪判定為不可信的仲介行銷話術，不予採信。

**法源/主管機關**：Directorate General of Immigration and Emigration（DGIE）；Rwanda Development Board（RDB）。

**建議**：拆為個別 negatives 條目（`kind: no_route`），信心度高。建議在條目文字中主動註明「已查證並排除 kwandarealestate.com 等仲介網站『5 萬美元購屋換居留』的說法，與官方許可類別清單矛盾」，因為題目特別提醒盧安達是易被誤導的國家，未來若有人重新查證盧安達，這句話能防止同一噪音來源被誤採。

---

### 坦尚尼亞本土（mainland Tanzania，不含桑吉巴）
**是否有買房換居留制度**：無

**證據**：
- Tier 1（一手法條全文）— 《坦尚尼亞投資法》（The Tanzania Investment Act, Chapter 38，Act No. 10 of 2022），Government Notice No. 395B（2023-06-13，Special Supplement to Special Gazette No. 15 Vol. 104），司法部長辦公室官方版本：
  - 第 2 條：適用對象為「business enterprise」（企業），最低資本門檻外資／合資 US$500,000、純坦尚尼亞資本 US$50,000。
  - 第 3 條（定義）：「capital」定義包含「buildings」「land」等資產，**但前提是該資產屬於一個以營利為目的、依商業原則經營之企業（business enterprise）**，非個人自住不動產。
  - 第 19 條：申請文件要求公司名稱／法律形式／董事股東／管理資格／商業活動說明／資本結構——全屬企業登記資訊，非個人購屋文件。
  - 第 30 條（移民配額）：「凡獲本法核發激勵證書之**企業**，依相關聘僱非公民之法律享有移民配額」——這是投資人及員工取得居留／工作許可（Class A）的法律連結點，配額授予對象是企業本身，不是購屋的個人。

**法源/主管機關**：The Tanzania Investment Act, 2022（Chapter 38）；Tanzania Investment Centre（TIC）；Immigration Service Department（Class A 居留許可）。

**建議**：拆為個別 negatives 條目（`kind: no_route`），信心度高（一手法條全文直讀）。建議條目附註一句：「土地／建物在法條 capital 定義中技術上有列名，但前提是作為營利商業企業之資產（例如開發商蓋旅館出租），非個人購屋自住；避免被誤讀為『不動產可算 capital，故有途徑』。」

---

### 波札那（Botswana）
**是否有買房換居留制度**：無（就「購置不動產取得居留」而言）；但另有一項與不動產無關的新制度值得記錄追蹤

**證據**：
- Tier 1 — 波札那政府官網居留許可頁（`www.gov.bw/residency-and-work/residence-permit-application`）：僅列三類居留——受扶養親屬、一般移民、公民配偶。無投資人或不動產類別，亦未引用《移民法》條號。
- Tier 3（線索，非結論依據）— 多個移民顧問網站（M&J Consultants Africa、World Next Step、Desinri 等）一致描述波札那「投資人許可證」為約 BWP 100 萬（約 US$75,000）**新設事業或既有企業股權投資**，須向 CIPA（公司與智慧財產局）登記，無不動產購置選項。
- **新發現（非本題範圍，但應記錄追蹤）**：多方次級來源指出波札那國會通過《公民法》（Citizenship Act, No. 25 of 1982）新增第 15A 條「經濟公民權」，US$75,000 捐款至政府發展基金（涵蓋住房、再生能源、觀光、礦業多元化），據稱 2026 年初開放申請。**本輪未能取得國會官網或政府公報一手文件確認生效日期**（DuckDuckGo 摘要對生效日期本身有兩個不同說法，未消歧），此為捐款制公民權（類似加勒比海 CBI 的捐款選項），不是「個人購買特定不動產」模式，不符合本彙編定義，不建議收錄，但因制度極新，建議另立觀察項目追蹤未來是否加入不動產購置替代選項。

**法源/主管機關**：現行投資人許可證——Department of Immigration and Citizenship（移民局，隸屬勞動與內政部）；新經濟公民權——《公民法》第 15A 條（生效日期未經一手確認）。

**建議**：拆為個別 negatives 條目（`kind: no_route`），信心度高（官方居留許可頁本身窮盡列舉，無不動產類別）。經濟公民權新制不建議收錄，可在條目備註中提一句「另有 2025/2026 生效中之捐款制經濟公民權，與購屋無關，暫不收錄」。

---

### 阿爾及利亞（Algeria）
**是否有買房換居留制度**：無法確立（傾向「無」，但一手法源未能讀取）

**證據**：
- Tier 3（線索）— Sands of Wealth：外國人可依額外行政審批合法購置住宅不動產，但文中僅描述購屋流程本身，未提及任何居留權益。
- Tier 3（線索）— NestFainder：明確將「外國人不動產所有權限制」與「居留要件」列為兩件互不相關的法律事務，未見交叉引用。
- Tier 3（行銷聚合站，但立場為否定，可作反向佐證）— goldenvisas.com/algeria：明文寫「阿爾及利亞未提供正式投資入籍計畫」，居留僅透過就業、家庭團聚等既定管道。
- **關鍵缺口**：阿爾及利亞現行投資法《Loi n° 22-18 du 24 juillet 2022》全文（UNCTAD 投資法資料庫 `investmentpolicy.unctad.org` 與阿國商業部官網 `commerce.gov.dz` 均嘗試直接讀取原文）因**伺服器錯誤（503/500）本輪未能開啟**；另一項「投資者護照」（Passeport de l'investisseur，阿國總理府官網 `premier-ministre.gov.dz` 登記之行政快速通關文件）因 **SSL 憑證驗證失敗**（http／https 皆然）本輪未能開啟，僅能透過 DuckDuckGo 搜尋摘要間接得知其存在，無法確認其性質是否涉及不動產。聲稱「ANDI 投資者居留卡與不動產掛鉤」的來源（openshores.co）本身是移民行銷網站（Tier 3，且本輪嘗試直接開啟遭 403 拒絕，無法核實其原文），依規則不可採信為決定性依據。

**法源/主管機關**：Loi n° 22-18 du 24 juillet 2022（全文未能讀取）；AAPI（原 ANDI，阿爾及利亞投資促進署）；DGSN 核發一般居留卡。

**建議**：**不宜直接歸入 negatives（尚不足以稱「已查證為無」）**，應維持在 excluded／無法確立分類，條目文字誠實記載「多方次級來源方向一致指向無，但一手法條全文（Loi 22-18）與『投資者護照』官方頁面均因技術性存取問題（伺服器錯誤／SSL 憑證失敗）本輪未能讀取，非查無資料」。若要坐實結論，下一輪應改變網路路徑或改用官方公報（Journal Officiel）鏡像重新嘗試讀取法條全文。

---

### 塞內加爾（Senegal）
**是否有買房換居留制度**：無法確立（傾向「無」，證據強度優於阿爾及利亞，但一手法源仍未讀取）

**證據**：
- Tier 2 — Le Soleil（塞內加爾國家級官方色彩報紙，非商業移民網站）2025 年報導《新投資法典》（`lesoleil.sn/actualites/economie/nouveau-code-des-investissements-...`）：內容聚焦生產性投資之財稅優惠（進口/在地採購免稅、達喀爾/蒂耶斯 3 年關稅豁免、其他地區 5 年、單一窗口 10 個工作天內完成），通篇未提及居留許可、投資人身分卡或不動產。
- Tier 3（線索，但態度中立可信）— Desinri（移民顧問網站）：明確承認「未找到塞內加爾『投資人簽證』的公開統一最低投資門檻」「未發現不動產自動換居留的規則」——連有商業誘因去宣傳此類方案的仲介網站都找不到，屬有意義的反向訊號。
- **一手法源已定位但未讀取**：《2025-16 號法律》（Code des Investissements 2025）官方立法網站連結 `legi.sn/legislation/7853_1778275766882_3byja4` 已找到，但本輪未直接開啟讀取全文；APIX（塞內加爾投資促進署）官方 PDF 因 **DNS 解析失敗**（`investinsenegal.sn` 無法解析）本輪未能取得。

**法源/主管機關**：Loi n° 2025-16（Code des Investissements 2025，全文未讀）；APIX S.A.（投資促進署）。

**建議**：維持 excluded／無法確立分類，條目誠實記載「Le Soleil 官方色彩媒體報導之 2025 投資法典聚焦生產性投資，未提及不動產或居留；APIX 官方 PDF 因 DNS 失敗未能讀取，Loi 2025-16 全文已定位但未及讀取，為本輪殘留缺口」。優先順序可低於阿爾及利亞（證據已比阿爾及利亞更接近「無」），但仍不足以升級為 negatives。

---

### 尚比亞（Zambia）
**是否有買房換居留制度**：無

**證據**：
- Tier 1 — 尚比亞移民局官網（`www.zambiaimmigration.gov.zm/permit-types`）：列出 12 類許可（居留／聘僱／投資人／配偶／就學／外交／訪客／跨境／臨時聘僱／臨時／過境／庇護），投資人許可（Investor's Permit）明定為「意圖在尚比亞設立事業或投資」，門檻新設事業 US$250,000／加入既有公司 US$150,000，佐證文件為銀行對帳單、匯款證明、貨物設備價值申報表（ZRA Form CE20）。頁面雖要求「不動產所有權或租賃合約證明」，但查證確認這是**營業處所**證明，非投資門檻本身。
- Tier 1（一手法條）— 《移民與遞解出境法》（Immigration and Deportation Act No. 18 of 2010，經 2016 年修正），全文見尚比亞官方法律資訊機構 ZambiaLII（`zambialii.org/akn/zm/act/2010/18`）：
  - 第 20 條（居留許可）：合格類別包括通曉當地語言者、已持投資人許可滿 3 年者、既有定居者、尚比亞公民子女、退休人士（財力／年金或「規定最低淨值」存入境內帳戶）——「最低淨值」是財務資產門檻，非不動產購置。
  - 第 29 條（投資人許可）：合格條件為投入規定財務或資本於「事業」（business），須持有尚比亞發展署（ZDA）核發之投資許可證。條文語言全部圍繞事業投資，不含不動產購置類別。

**法源/主管機關**：Immigration and Deportation Act No. 18 of 2010（第 20、29 條）；Zambia Department of Immigration；Zambia Development Agency（ZDA）。

**建議**：拆為個別 negatives 條目（`kind: no_route`），信心度高（官網＋一手法條原文雙重確認）。

---

### 烏干達（Uganda）
**是否有買房換居留制度**：無法確立（傾向「無」，但官方一手來源本輪完全無法存取）

**證據**：
- **本輪嘗試存取的官方網域全數失敗**：`immigration.go.ug`（HTTP 403）、`eimmigration.go.ug`（DNS 失敗）、`uia.go.ug`（DNS 失敗，正確網域應為 `ugandainvest.go.ug`）、`ugandainvest.go.ug`（連續逾時）、ULII 烏干達官方法律資料庫 `ulii.org`（HTTP 403）、FAOLEX 聯合國糧農組織法律資料庫（DNS 失敗）——因此**本輪未能取得任何 Tier 1 來源**，這點需誠實標註，與尚比亞的查證強度明顯不同。
- Tier 2（多方法律事務所文章，非官方但具專業背景）：
  - m-smithadvocates.com（烏干達本地律師事務所）《Uganda Work Permit Guide 2026》：Class M 投資人許可佐證文件為 UIA 投資許可證、銀行對帳單、商業計畫書、公司登記證書、股權／董事證明；未列不動產購置。UIA 建議最低投資額約 US$100,000。
  - globalinvestments.net：Class G/M 投資人許可聚焦事業投資，未提及不動產。
  - worldnextstep.com：許可滿 5 年可申請永久居留，須提供「持續投資與納稅合規證明」，仍是事業投資導向。
  - 以多組關鍵字搜尋 2019 年《投資法典》（Investment Code Act）最低資本門檻，各來源數字略有出入（US$100,000 或 US$250,000 版本並存，因該法將具體金額授權部長以法定文書訂定），但所有版本一致將門檻定義為「投資資本」，非不動產購置。
  - **消極佐證**：以「Uganda golden visa property residency investment」查詢，連 immigrantinvest.com、globalcitizensolutions.com 這類最積極擴大行銷範圍的仲介網站都**完全沒有把烏干達列為有此類方案的國家**——這類網站的沉默是有意義的反向訊號，但不構成「已確認無」的充分證據。

**法源/主管機關**：《公民與移民管制法》（Citizenship and Immigration Control Act, Cap 66）及附屬規則；《2019 年投資法典》（Investment Code Act, 2019）；Directorate of Citizenship and Immigration Control；Uganda Investment Authority（UIA）。**以上法源引用僅為次級來源轉述，本輪未能直接核對原文。**

**建議**：**不宜歸入 negatives**，維持 excluded／無法確立分類，且應與「已查證為無」（如尚比亞）明確區隔呈現方式——條目文字建議寫「多方獨立次級來源一致指向無，但官方原文／官網因存取限制（403／DNS 失敗／逾時）本輪未能直接核對，建議下一輪換網路環境或改用烏干達駐外使館等其他管道補強至 Tier 1」。

---

### 合併條目拆分建議

現有 `data/visa-property.json` 的 `excluded` 陣列最後一筆把「塞席爾、迦納、肯亞、盧安達、坦尚尼亞本土、波札那、突尼西亞、阿爾及利亞、奈及利亞、塞內加爾、尚比亞、烏干達」12 國打包成一筆。本輪查證完成後，這 12 國的查證狀態已完全分化，不應再共用一句話。具體拆分建議：

| 國家 | 建議去向 | 理由 |
|---|---|---|
| 塞席爾 | 已移出（沿用既有紀錄） | 前輪已於亞太查證輪次移入 `negatives`，本輪未重查 |
| 肯亞 | `negatives`（`kind: no_route`） | 前輪已查：官方入口存在但無不動產連結制度 |
| 奈及利亞 | 維持 `excluded`（無法確立） | 前輪僅記載「未查得資料」，未達可歸入 negatives 之確認強度，建議下一輪比照本輪方法補強 |
| 突尼西亞 | 維持 `excluded`（無法確立） | 同上 |
| 迦納 | `negatives`（`kind: no_route`） | 本輪 Tier 1（GIPC、GIS 官網）確認 |
| 盧安達 | `negatives`（`kind: no_route`） | 本輪 Tier 1（DGIE、RDB 官網）確認，並已排除仲介網站誤導說法 |
| 坦尚尼亞本土 | `negatives`（`kind: no_route`） | 本輪 Tier 1（投資法全文）確認 |
| 波札那 | `negatives`（`kind: no_route`） | 本輪 Tier 1（政府居留許可頁窮盡列舉）確認 |
| 尚比亞 | `negatives`（`kind: no_route`） | 本輪 Tier 1（官網＋移民法原文）確認 |
| 阿爾及利亞 | 維持 `excluded`（無法確立，非「未查證」） | 本輪已查但一手法源存取失敗，需與「完全未查」的舊狀態區隔 |
| 塞內加爾 | 維持 `excluded`（無法確立，非「未查證」） | 同上，證據強度略優於阿爾及利亞 |
| 烏干達 | 維持 `excluded`（無法確立，非「未查證」） | 官方網域全數 403／DNS 失敗，僅有 Tier 2 次級來源 |

**核心原則**：即使 8 國查完後有 5 國可以升級為 negatives、3 國仍停在無法確立，也不應該再用一句話打包——本輪的分化結果本身就證明了前輪報告的方法論意見是對的：打包處理會讓「已查證」與「完全未查」被混在同一句話裡，讀者無法分辨。建議下一輪把 `merge_note` 機制保留給未來可能出現的新國家，但這 12 國本身應該全部拆成 12 個獨立條目（分別進 negatives 或 excluded）。

**本輪最重要的發現（跨八國）**：**沒有任何一國查得「購置不動產可換居留或公民權」的正面制度**。8 國中 5 國（迦納、盧安達、坦尚尼亞本土、波札那、尚比亞）已達 Tier 1 確信度的「無」；3 國（阿爾及利亞、塞內加爾、烏干達）方向上也是「無」，但受限於官方網站存取失敗（伺服器錯誤、SSL 憑證問題、DNS 失敗、403），未能達到 Tier 1，誠實標註為「無法確立」而非升級為肯定的「無」。

---

## 二、DuckDuckGo 時期條目複核

前輪報告在「查證方法與限制誠實揭露」一節指出，本次 session 的 WebSearch 額度於第 5 組搜尋起用罄（200/200），此後改用 DuckDuckGo HTML 搜尋，**可能造成搜尋深度不如前段的 6 筆條目**：沙烏地阿拉伯、埃及、格瑞那達、巴西、厄瓜多、秘魯。

依照指示的優先順序（「排除仍成立」但證據薄弱者優先），本輪對前兩筆——沙烏地阿拉伯、埃及——動用完整 WebSearch 能力重新查證，這兩筆原本都是「排除仍成立，但門檻金額本身未達 Tier 1」，屬於「錯誤維持排除」風險最高的類型。其餘四筆（巴西、厄瓜多、秘魯、格瑞那達）原結論已建立在 Tier 1 一手來源之上（巴西、厄瓜多、秘魯甚至已是前輪的★級發現或 Tier 1 確認負面結果），複核優先順序較低，本輪僅做輕量級的來源真實性複驗。

### 沙烏地阿拉伯（複核）——★ 重大升級，建議收錄

**原結論**：排除仍成立（制度存在性已確認，但居留門檻金額僅見於 Tier 3 仲介網站，未達 Tier 1）。

**本輪新查得證據**：
- Tier 1 — `pr.gov.sa`（Premium Residency Center 官方入口，經濟發展事務委員會轄下）「Real Estate Owner Residency」產品頁：門檻 **SAR 4,000,000**，分兩類——Category 1（既有不動產完全所有權／用益權，須為住宅、非土地、無抵押）；Category 2（期房購買，同額門檻，另須支付不低於 SAR 1,000,000 或房價 10%〔取高者〕，開發商須經 REGA 核准）。規費 SAR 4,000。
- Tier 1 — 同站《Detailed Conditions and Requirements of the Real Estate Owner Residency》全文（依《Premium Residency Permit Law》Royal Decree No. M/106 授權之 Implementing Regulations 第 4(8) 條發布）：第 3 條門檻原文與產品頁一致；第 7.2 條明文「取得永久優質居留之條件……不適用」，即此產品**僅為可續期許可，不通往永久居留**；第 10 條允許 90 天內置換另一不動產以維持許可；第 11 條窮盡列舉六項撤銷事由，未見最低停留天數要求。

**結論是否改變**：**是**。門檻金額已由「僅 Tier 3」升級為官方產品頁＋官方詳細規則文件雙重確認的 **Tier 1**。

**建議**：**應由 `excluded` 移至正文（`programmes`）收錄**——門檻 SAR 4,000,000（約 106 萬美元），法源《優質居留許可法》（Royal Decree No. M/106）及其 Implementing Regulations 第 4(8) 條，主管機關為 Premium Residency Center。應明確註記「僅為可續期居留許可，明文排除通往永久居留」這個重要限制，避免讀者誤以為等同一般投資移民的永久居留路徑。

---

### 埃及（複核）——★ 重大升級，建議收錄

**原結論**：排除仍成立（制度存在性已於 GAFI 官網確認，但門檻金額僅見於 Tier 2 美國國會圖書館報導轉述，未達 Tier 1）。

**本輪新查得證據**：
- Tier 1 — 埃及官方公報掃描原文（經 `manshurat.org` 轉載之官方印刷總署 الهيئة العامة لشئون المطابع الأميرية 掃描檔，非仲介轉述）：《2023 年第 876 號總理令》，刊於《埃及官方公報》第 9 期續篇（ج），2023-03-02，總理 Dr. Mostafa Kamal Madbouly 簽署。原文第一項：購置國家或公法人所有之不動產，門檻**美金 30 萬元**，須境外匯入或經海關查驗入境。
- Tier 1 — 《2023 年第 3562 號總理令》，刊於《埃及官方公報》第 37 期（مكرر），2023-09-18：修正 876/2023，**門檻維持 30 萬美元不變**，但移除「僅限國有物業」限制（改為一般不動產購置皆可），**新增第 5 項強制文件：五年內不得處分該不動產之聲明**（此點原僅見於 Tier 3 仲介網站，現已升級為 Tier 1 官方公報原文確認）。另修正入籍申請規費為美金 1 萬元或等值埃鎊。
- Tier 1（輔助）— `cc.gov.eg`（埃及最高法院官方法律資料庫）之立法條目頁，刊登資訊與上述掃描互相印證。
- 以多組關鍵字查核 2024–2026 年是否有後續修法，未見更新該金額之公報或報導，僅持續引用上述兩令。

**結論是否改變**：**是**。門檻金額已由 Tier 2（美國國會圖書館轉述）升級為官方公報原文的 **Tier 1**（兩道總理令互相確認）；五年閉鎖期由 Tier 3 升級為 Tier 1。原 Tier 3 流傳的「US$100k donation」「US$250k early exit」兩項數字，本輪判斷可能是把「投資項目路徑」條件誤植到「不動產路徑」，**不應採信**。

**建議**：**應由 `excluded` 移至正文（`programmes`）收錄**——門檻美金 30 萬元，法源《2023 年第 876 號總理令》（經《2023 年第 3562 號總理令》修正），主管機關 GAFI，並附帶「五年內不得處分」的持有限制、產權須完成公證登記（الشهر العقاري）或受國有機構監管。

---

### 巴西、厄瓜多、秘魯、格瑞那達（輕量複核）

這四筆原結論已建立在 Tier 1 一手來源之上（巴西、厄瓜多、秘魯屬前輪★級發現或 Tier 1 確認負面結果，格瑞那達則是前輪已直接複驗官方首頁），本輪僅做來源真實性複驗，非重新調查：

- **巴西**：本人直接以 Read 工具開啟前輪引用的 `gov.br` 官方 PDF（`resolucao_normativa_no_36_de_9_de_outubro_de_2018.pdf`），**逐字確認全文屬實**：第 2 條 caput 門檻 R$ 1,000,000；第 2 條第 1 項「北部及東北部地區得低於本條門檻至多 30%」（即地板值 R$ 700,000）；第 3 條第 4 項居留期限 4 年；第 5 條期滿可轉無限期；第 6 條每 2 年須境內累計停留 14 天。前輪★級發現**完全屬實，結論不變**，且細節比前輪報告更完整（新增第 6 條停留天數規定）。
- **厄瓜多**：嘗試直接開啟 `cancilleria.gob.ec` 官方頁面遭遇 SSL 憑證驗證失敗，改以 DuckDuckGo 搜尋確認頁面確實存在且描述「不動產投資人臨時居留簽證」，但本輪**未能重新讀到 100 SBU 這個具體數字的原文**。未發現任何與前輪結論矛盾的證據，判斷為存取技術問題而非制度不存在，原結論維持不變但本輪未能獨立重新驗證數字本身。
- **秘魯**：嘗試直接開啟 `gob.pe` 官方頁面遭遇 HTTP 418（機器人阻擋），改以 WebSearch 查證但本次 session 的 WebSearch 額度已用罄（提示「200/200」），未能完成複核。未發現任何與前輪結論矛盾的證據，原結論（投資人居留簽證僅受理公司投資，不含不動產）維持不變，但本輪未能獨立重新驗證。
- **格瑞那達**：嘗試直接開啟 `cbi.gov.gd` 官方首頁**成功**，內容與前輪記載完全一致：官網確認「An investment in an approved project (real estate) in Grenada」為公民入籍選項之一，但首頁仍未列出不動產途徑的具體金額（NTF 途徑門檻 15 萬美元仍清楚刊登，形成對比）。**前輪結論完全複驗屬實，結論不變**。

**小結**：本輪對 DuckDuckGo 時期 6 筆條目的複核，**2 筆（沙烏地阿拉伯、埃及）結論實質改變**——從「排除仍成立」升級為「應予收錄」，且升級依據是貨真價實的 Tier 1 官方一手來源（政府官網產品頁、官方公報原文），不是猜測；**4 筆（巴西、厄瓜多、秘魯、格瑞那達）結論未變**，其中巴西已用 Read 工具逐字複驗官方 PDF 全文屬實，厄瓜多與秘魯因本輪技術限制（SSL 憑證、418 阻擋、WebSearch 額度用罄）未能獨立重新驗證但也未發現矛盾證據，格瑞那達則完整複驗屬實。

---

## 三、本輪自己的限制

- **WebSearch 額度**：本次任務分派給四個獨立背景 agent，各自使用獨立 session 額度，多數在查證過程中仍用罄 WebSearch 額度（沙烏地阿拉伯／埃及那組尤其明顯，額度用罄後改用 Bing／Brave 及瀏覽器直接存取，最終仍成功取得官方公報原文）。本人自己直接操作的部分（複核巴西／厄瓜多／秘魯）也在查核秘魯時撞到「this session has used its web search budget (200 of 200)」，此後改用 WebFetch 直接開啟官方頁面或 DuckDuckGo HTML 替代，並在上文各筆註明。
- **DuckDuckGo HTML 本身在本輪多次遭遇 CAPTCHA 阻擋**（尤其在沙烏地阿拉伯／埃及那組與本人親自查證秘魯時），比前輪報告描述的情況更嚴重——這代表「WebSearch 用罄後改用 DuckDuckGo」這個備援方案本身的可靠度也在下降，下一輪若要複製本方法，建議準備第三種備援（如本輪成功使用的 Bing／Brave 或直接 curl 官方網域）。
- **多個官方網域本輪持續無法存取**，具體記錄於各國段落，包含：`ugandainvest.go.ug`（逾時）、`immigration.go.ug`／`ulii.org`（403）、`eimmigration.go.ug`／`uia.go.ug`／`faolex.fao.org`／`investinsenegal.sn`（DNS 失敗）、`investmentpolicy.unctad.org`（503）、`commerce.gov.dz`（500）、`premier-ministre.gov.dz`／`aapi.dz`（SSL 憑證驗證失敗）、`cancilleria.gob.ec`（SSL 憑證驗證失敗）、`gob.pe`（HTTP 418 機器人阻擋）。這些均如實記錄為「無法確立」而非猜測其內容，未對任何一筆使用移民中介網站作為唯一或決定性來源。
- **未查證項目**：奈及利亞、突尼西亞兩國本輪未重新查證（沿用前輪「未查得資料，維持無法確立」的記載），因任務範圍鎖定在完全未查的 8 國；若要把這兩國也升級到與迦納、盧安達同等的 Tier 1 確信度，需要額外一輪查證。
- **波札那新「經濟公民權」制度**（第 15A 條，US$75,000 捐款制）的生效日期本輪未能以一手來源消歧（DuckDuckGo 摘要出現兩個不同日期版本），如實標註為未確認，未寫入任何結論性日期。
- 本輪嚴格遵守「移民中介／投資移民代辦網站不可當唯一或決定性來源」原則；凡遇到此類網站的說法且無法以官方或 Tier 2 來源佐證，一律維持原排除或標註「無法確立」，未升級為「已確認」（例如盧安達 kwandarealestate.com 的說法即為一例，本輪主動查證後判定不可信並排除）。

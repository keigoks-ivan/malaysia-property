# 亞太組查證報告（11 套）

查證日期：2026-08-02 ｜ 對照資料集 compiled：2026-08-01

查證方式：兩輪並行 agent。第一輪按國家分組（泰國兩筆、馬來西亞單獨一組、萬那杜／菲律賓／香港／南韓一組、斯里蘭卡兩筆＋印尼兩筆一組），各自直連一級來源重新查核既有記載。站主中途特別提醒：**標 UNVERIFIED／not established／本次未涵蓋的欄位，要主動去查一輪，不是被動留著**——「上一輪沒查」跟「查過確實查無」是兩件事，資料集不該把它們混在同一個標籤底下。因此加開第二輪，專門針對第一輪仍空著的欄位（stay、leads_to、entry_tax、mortgage、offplan、dependants 等）逐一主動搜尋，並要求每一項寫明「查了什麼、為什麼還是查無」。下面每一筆的欄位判定，凡標「本輪已查、仍無法確立」的，代表確實嘗試過官方來源或雙重二級來源而不得；沒有這個標記、原本就是 NOT VERIFIED 又沒被本輪任務涵蓋到的極少數細節，會單獨註明。

## 摘要

- 確認無誤：3 筆（thailand、thailand-2、indonesia）
- 有出入需修正：1 筆（malaysia）
- 新發現的配套要求／可由未查證升級為已確認：5 筆（philippines、hong-kong-sar、sri-lanka、sri-lanka-2、indonesia-2）
- 無法確立（維持原判，本輪已主動重查）：2 筆（vanuatu、south-korea）

（註：分類是依「本輪最值得編輯注意的主線」歸類，並非互斥——例如 malaysia 除了要修正一處錯誤，也有全新發現的配套要求；indonesia 雖歸「確認無誤」，但其中一個欄位〔leads_to〕本輪從無到有補上了確認內容。細節見逐筆分節。）

**本輪查過仍查無的項目清單**（已嘗試 tier 1／雙重 tier 2，非未查）：
- 泰國兩筆的 `stay`：直接查證未再進一步突破，「無明定最低居住天數」維持原判但未獲得比現有記載更強的一級來源佐證
- 萬那杜 `mortgage`／`offplan`：直接讀取移民局官方申請檢核表全文（透過代理繞過官網 403），文件本身對融資與完工狀態全然沉默
- 菲律賓 `mortgage`：直接讀取 PRA 官網與轉換檢核表，僅查得「轉換後處分/設定負擔須經 PRA 核准」，未解決購入當下能否融資
- 香港 `entry_tax`／`mortgage`：直接讀取 New CIES 官方 Guidebook 全文（tier 1），全文未提及印花稅或按揭
- 南韓 `stay`：直接讀取 visa.go.kr 官方頁面（透過代理繞過空白渲染問題），頁面未列最低居住天數
- 南韓 `entry_tax`：僅查得韓國一般不動產取得稅（취득세）概略稅率，非投資移民專屬規則，且來源非法務部/國稅廳一級頁面
- 斯里蘭卡兩筆的 `stay`：Investor Visa Guideline PDF 解析多次失敗（含改用 curl+pdftotext），仍未取得可用文字
- 斯里蘭卡兩筆的 `leads_to`：直接讀取移民局官方 Residence Visa 索引頁（id=18），該頁完全未列「永久居留簽證」類別——尚不能證明「不通往 PR」，但這是一個新的、值得注意的負面訊號
- 印尼兩筆的 `stay`：對 Permenkumham 22/2023 全文逐句檢索（"wajib berada"、"paling sedikit...hari"、"hadir" 等關鍵詞），該條例本身完全沒有最低在境天數條款——這是讀完整部法規後的結果，不是沒查
- 印尼兩筆的 `offplan`／`mortgage`：條文僅寫「承諾購買價值達門檻之公寓」，對完工狀態與融資均沉默，另行搜尋僅查到杜拜黃金簽證的無關內容

---

## 逐筆

### thailand — 投資型延長居留：300 萬泰銖分項

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`（MOTS 證明函為強制要件、無函則門檻為 1,000 萬泰銖、另有 2006 年前入境者之封閉舊制） | 如現有記載 | 確認無誤。兩個獨立二級來源逐字一致，均引用第 237/2568、238/2568 號命令且日期一致（2025/10/1 生效） | 2（雙來源一致） | https://aimbangkok.com/thailand-3-million-baht-investment-visa/ ；https://thai-residence.com/en/info-guide/visa-thailand-3-million-baht/ |
| MOTS 證明函之核發程序／規費（原標「未查證」的 OPEN ITEM） | 未查證，程序與規費不明 | **可由未查證升級為已確認**：三個獨立來源一致，程序透過經授權之長住服務代理（Thailand Longstay Service, TLS）辦理，規費為一次性入會費 4,000 泰銖＋年度服務費 27,000 泰銖，處理時間約 7–10 個工作天，媒體報導確認 2025 年 10 月已上路且現行有效 | 2（三方一致，含 2026/3/13 媒體報導） | https://thethaiger.com/thai-life/property/thailands-3-million-baht-property-visa |
| 其餘欄位（`term`、`stay`、`leads_to`、`ownership_form`、`offplan`、`dependants`） | — | 其餘欄位核對無誤；`dependants` 額外查得一個排序細節可補充：依親人須待主申請人本人取得完整 12 個月延期後才能申請 | 2 | https://aimbangkok.com/thailand-3-million-baht-investment-visa/ |

**配套要求**：除購屋達門檻外，走 300 萬泰銖分項者，主申請人（及每一位依親人）皆須先取得觀光暨體育部證明暨請求函，且該函本身另有規費（4,000＋27,000 泰銖／年）；無此函者實際門檻升為 1,000 萬泰銖。

**建議修正**：`min_value.basis` 內的 OPEN ITEM 語句可從「未查證是否已公布程序」改寫為「已確認：透過 TLS 代理辦理，規費 4,000＋27,000 泰銖」，並附上述來源；`dependants` 可補充申請排序細節。

---

### thailand-2 — 長期居留 LTR：高資產全球公民

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`（USD 500,000 投資＋USD 1,000,000 資產測試可與投資額重疊＋保險/存款替代方案） | 如現有記載 | 確認無誤，直接讀取 BOI 官網逐項核對，「the USD 1m assets test 仍然有效」與「may overlap with the Thailand investment amount」原文皆與記載一致 | 1 | https://ltr.boi.go.th/ |
| `entry_tax`（17% 單一稅率僅適用高技術專業人才，不適用高資產全球公民） | 如現有記載 | 確認無誤，BOI 頁面該行文字僅出現在 Highly-Skilled Professionals 類別下 | 1 | https://ltr.boi.go.th/ |
| `last_change`（現行無所得要件，高技術專業人才類別仍保留年薪 8 萬美元門檻） | 如現有記載 | 確認無誤，BOI 頁面確認高技術專業人才需「USD 80,000/年（近兩年）」或碩士學位者 4 萬美元，高資產全球公民無此項 | 1 | https://ltr.boi.go.th/ |
| 其餘欄位（`term`、`leads_to`、`ownership_form`） | — | 其餘欄位核對無誤 | 1／2 | 同上；公寓 49% 上限見 https://library.siam-legal.com/thai-law/condominium-act-ownership-sections-19-1-19-11/ |

**配套要求**：除 50 萬美元投資（房產僅為其中一種合格資產）外，另須（a）全球或泰國資產總額達 100 萬美元（可與投資額重疊，故總承諾為 100 萬非 150 萬美元）；（b）保額 5 萬美元以上之健康保險，或泰國社會保險，或持有滿 12 個月、餘額 10 萬美元以上之銀行存款。此二者為現行記載已載明的硬性門檻，本輪查證確認仍然成立、未被取消。

**建議修正**：無，本筆通過查證。

---

### malaysia — MM2H 銀/ 金/ 白金級

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`／`extra_tiers`（RM600k/1m/2m＋USD150k/500k/1m 定存＋RM1,000/3,000/200,000 參與費） | 如現有記載 | 確認無誤，直接下載 PDF 全文比對逐字相符，定存確為美元計價非馬幣；白金級 RM200,000 參與費經確認**不是誤植**，數字真實但相對銀/金級確實異常偏高 | 1 | https://motac.gov.my/wp-content/uploads/2026/01/Terms-And-Regulations-For-New-Participants-Under-The-Malaysia-My-Second-Home-MM2H-.pdf（頁首標註 ACCURATE AS OF 22 JULY 2024） |
| **遺漏欄位：續證費**（現有記載未提及） | 無 | **新發現**：各級續證另收費，銀級 RM1,500／金級 RM3,000／白金級 RM5,000（主申請人＋依親人合計），每 5 年續證時繳納 | 1 | 同上 |
| `stay`（每年累計 90 天） | 如現有記載 | 確認無誤，含 25–49 歲可由主申請人或依親人代為履行的條款，逐字相符 | 1 | 同上 |
| `leads_to`（社交訪問准證，不通往永久居留或入籍） | 如現有記載 | 確認無誤，此為本筆最關鍵主張，本輪額外找到部長本人 2024/6/15 公開發言與國會書面答詢兩項旁證，均獨立指向同一結論；2026 年 5 月《申請指南手冊》全文亦以「Social Visit Pass (MM2H)」稱之，法律名稱確認一致 | 1（部長發言、手冊用語）＋2（媒體報導） | https://www.malaymail.com/news/malaysia/2024/06/15/new-mm2h-participants-not-eligible-for-pr-status-says-tourism-minister/139896 |
| `ownership_form`（檳城州最低價：MM2H 專屬優惠 RM500,000；一般外國人門檻威省分層/有地皆自 2012/7/1 起 RM100 萬） | 如現有記載 | **有出入需修正**：檳城 MM2H 專屬 RM500,000 優惠、島區門檻（分層 RM100萬自2012/7/1、有地 RM300萬自2017/4/1）皆確認無誤；但威省（大陸）分層房產部分需修正日期——**個人**外國買家門檻自 2012/7/1 起原為 RM500,000，直到 **2017/4/28** 才調高至 RM100 萬（現有記載援引的「RM100萬自2012/7/1」實為外資「公司」買家門檻，混用於個人買家不準確） | 1 | https://ptg.penang.gov.my/images/artikel/Pembangunan_Tanah/PerolehanTanahOlehWarganegaraAsing.pdf（2024/8/1 更新版） |
| `ownership_form`（吉隆坡 RM1,000,000 門檻） | 標記為 NOT VERIFIED，因 PTGWP／EPU 網站無法連線 | 本輪已查、仍無法確立：PTGWP（ptgwp.gov.my）與 EPU（ekonomi.gov.my）本輪再次連線失敗（連線被拒），維持原判 | — | 已嘗試 https://ptgwp.gov.my、https://ekonomi.gov.my（皆無法連線） |
| `entry_tax`（印花稅／州同意費） | 標記為 NOT VERIFIED | **有出入需修正／部分升級**：五個獨立來源一致（含一份引用《2025年財政法案／2026年財政預算案》的顧問公司說明），外國人／非公民住宅買方之產權移轉備忘錄印花稅自 **2026/1/1 起為 8%**（原 4%）——與本站 `/my/report.html` 既有記載的 8% 外國人印花稅口徑一致，可視為互相印證；商業地產是否維持 4% 僅見單一來源，未達雙重二級標準，不採信。州政府同意費部分本輪已查、仍無法確立：確認各州費率不一、聯邦直轄區走 EPU、其他州走各州土地局，但未查得任一州具體金額或百分比 | 2（印花稅 8%）／未達標準（商業稅率、州同意費金額） | 印花稅：多方顧問資料引用《2025年財政法案》，未能連上 hasil.gov.my 官方頁面取得一級確認，暫列 tier 2 |
| `dependants`（配偶、21 歲以下子女、21–34 歲須未婚未就業） | 如現有記載 | **本輪主動重查（非沿用上輪判斷）：確認無誤**，直接讀取 PDF 全文逐字相符，包含依親人免收參與費、外傭可另行申請 | 1 | 同上 PDF |
| `mortgage` | 標記為 NOT VERIFIED | **本輪主動重查（非沿用上輪判斷）：查證後仍無法確立**——直接通讀《新參與者條款與規則》全文，文件對房貸／融資議題完全沒有提及，屬「條文本身沉默」，非「未及查詢」 | 1（查證方式已升級，結論仍為未定） | 同上 PDF |
| `offplan` | 標記為 NOT VERIFIED | 同上，本輪主動通讀全文確認條文沉默，維持原判 | 1 | 同上 PDF |
| 其餘欄位（`term`、`last_change`、10 年鎖定期起算點爭議） | — | 其餘欄位核對無誤 | 1 | 同上 |

**配套要求（本輪新發現，現有記載完全未載）**：除購屋＋定存＋參與費外，法定必要條件還包括：（1）主申請人與依親人皆須至 MOTAC 指定體檢診所／醫院完成體檢，核准後方可辦理；（2）申請須透過 MOTAC 核發執照之 MM2H 旅遊代理商，經 One Stop Centre 送件，不可自行直接申辦；（3）申請人須年滿 25 歲，且來自與馬來西亞有邦交之國家；（4）每次續證皆須重新提交體檢報告、保險證明與有效護照影本；（5）續證／加保另須具結之個人保證書（Personal Bond）及 MFII 體檢報告。此外還有先前遺漏的續證費（銀 RM1,500／金 RM3,000／白金 RM5,000）。這些是站主原本擔心的「買到門檻價就能拿居留」失效模式的具體例證——比定存本身更容易被忽略。

**建議修正**：(1) 威省分層房產個人買家門檻日期由「2012/7/1」修正為「2017/4/28」（此前為 RM500,000）；(2) 新增續證費欄位或於 `term` 說明中補充；(3) `entry_tax` 由「未查證」改為「一般外國人住宅印花稅 8%（2026/1/1 起，tier 2），州同意費仍無法確立」；(4) 於配套要求新增一段完整列出體檢／代理商／年齡／續證文件等必要條件；(5) `dependants` 與 `mortgage` 維持現有記載，但註記本輪已直接通讀官方全文重新確認（前者確認相符、後者確認條文沉默），而非延續舊判斷。

---

### vanuatu — 居留簽證：租賃權持有人類別

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `entry_tax` | 標記為 NOT VERIFIED | **本輪已查、有部分進展**：萬那杜金融服務委員會（VFSC）2026/7/13 公告（由印花稅稽核官署名）確認《印花稅法》CAP.68 第 19 條下，買賣合約、租約移轉、租賃權轉讓均須課徵印花稅——「無印花稅」的說法確定是錯的。但**具體稅率仍無法確立**：僅查得單一非權威來源（myvanuatu.vu）引用 5%，未達雙重來源標準，不採信 | 1（稅捐確實存在）／無法確立（稅率） | https://www.vfsc.vu/wp-content/uploads/2026/07/Notice-Sales-Purchase-Agreement-must-be-Stamp-Duty.pdf |
| `mortgage`／`offplan` | 標記為 NOT VERIFIED | 本輪已查、仍無法確立：直接讀取移民局官方申請檢核表全文，僅要求「土地租約與租賃權所有權移轉」文件，對融資與完工狀態全然沉默 | 1（文件已讀，結論仍未定） | https://immigration.gov.vu/wp-content/uploads/2023/09/RESIDENCY_VISA-LEASEHOLD_HOLDER_CHECKLIST_V2.pdf |
| `term`／`stay`／`leads_to` | 標記為未查證／NOT VERIFIED | 本輪已查、仍無法確立。`leads_to` 新查得移民局另設獨立頁面「10-years-permanent-residency」，但因該頁同樣回傳 403，無法確認此頁與租賃權持有人途徑的關係，維持原判「未確立」 | — | https://immigration.gov.vu/10-years-permanent-residency/（無法直接讀取內容） |
| 99 年租期上限是否適用習俗地 | 現有記載刻意不刊載（僅單一二級來源談公有地） | 確認原判正確：本輪找到《土地租賃法》原始英文條文，一般預設為 75 年（http://extwprlegs1.fao.org/docs/html/van38130.htm），2024 年修正案提高至 99 年一事仍僅見單一二級來源（Daily Post）且明確僅涉及公有地，非習俗地，不宜升級為確定事實 | 1（75年一般規定）／2（99年修正，單一來源，僅公有地） | http://extwprlegs1.fao.org/docs/html/van38130.htm ；https://www.dailypost.vu/news/lands-ministry-to-roll-out-99-year-lease-amendment-next-week/article_edaa0e26-b0d6-565d-8f8b-94d95adea7f5.html |
| 其餘欄位（`dependants`、`ownership_form`、`min_value`） | — | 其餘欄位核對無誤 | 1 | https://immigration.gov.vu/live/ |

**配套要求**：除 VUV 1,000 萬租賃權不動產外，申請案內每人每月須有經認證所得至少 VUV 250,000（夫妻合計 VUV 500,000/月），且須持續維持，非一次性測試。

**建議修正**：`entry_tax` 可由「未查證」改為「稅捐確實存在（tier 1），稅率無法確立」；其餘維持原判不動，本筆多數欄位屬「條文本身沉默／官網封鎖」，非資料集判斷有誤，站主既有的 medium confidence 定位仍然正確。

---

### philippines — SRRV Classic 退休居留

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| 存款級距（現有記載刻意不刊載具體金額，僅稱「USD 15,000–50,000 依年齡/退休金狀態」） | 刻意不刊載 | **可由「刻意不刊載」升級為已確認**：PRA 官網本身即列出清楚級距——領退休金者 50 歲以上 USD 15,000／領退休金者 40–49 歲 USD 25,000／未領退休金者 50 歲以上 USD 30,000／未領退休金者 40–49 歲 USD 50,000。可直接刊載，取代原本因「表格擷取方向有歧義」而保留的空白 | 1 | https://pra.gov.ph/SRRVisa |
| `mortgage` | 標記為 NOT VERIFIED | 本輪已查、仍無法確立：官網與轉換檢核表 PDF 均未提及購入當下能否融資；唯一相關但非直接答案的旁證是「轉換後處分或設定負擔須經 PRA 核准」，這只說明轉換*之後*的限制，不回答融資能否計入門檻本身 | 1（旁證）／無法確立（核心問題） | https://pra.gov.ph/SRRVisa |
| `entry_tax` | 標記為 NOT VERIFIED | **本輪已查、可補充一般性資訊**：四個獨立來源一致，菲律賓印花稅（Documentary Stamp Tax）為成交價與 BIR 稅務區值兩者取高之 1.5%——但這是菲律賓一般不動產交易稅，非 SRRV 轉換專屬規則，且未能連上 bir.gov.ph 官方稅率頁確認為一級來源 | 2（四方一致，一般稅制非 SRRV 專屬） | https://ren.ph；https://taxify.ph；https://respicio.ph |
| 其餘欄位（`min_value`、`term`、`leads_to`、`ownership_form`、`offplan`、`dependants`、40 歲以上資格、「2023年改為50+」為誤傳） | — | 其餘欄位核對無誤 | 1 | https://pra.gov.ph/SRRVisa |

**配套要求**：SRRV 的門檻本質是「存款」而非「購屋」——存款須先存入滿 30 天才可轉換為房產投資；退休金證明每月至少 USD 800（單身）或 1,000 美元（含依親人）為獨立必要條件，與存款/房產門檻並行。

**建議修正**：`min_value.basis` 可補上四級存款金額表；`entry_tax` 可註明「菲律賓一般 DST 1.5%（tier 2，非 SRRV 專屬）」；`mortgage` 維持未定。

---

### hong-kong-sar — 新資本投資者入境計劃（New CIES）

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`／`extra_tiers`（HK$30m 總額、HK$15m 不動產上限、HK$10m 住宅上限、HK$3m 強制投資組合、兩次日期調整） | 如現有記載 | 結構性確認無誤（透過官方 Guidebook 全文與 eligibility 頁核對），惟兩次調整日期（2024/10/16、2025/9/17）本輪未能重新獨立核對到更明確的一級文字，維持原判但未進一步強化 | 1（結構）／無法進一步確立（兩個確切日期） | https://www.newcies.gov.hk/media/tehetmzy/guidebook-for-the-new-capital-investment-entrant-scheme-full-version-en.pdf |
| `term`／`stay` | 標記為 NOT VERIFIED | **可由未查證升級為已確認**：入境處官方 FAQ 明確說明——首次以訪客身分入境須於不超過 180 天內完成投資，其後獲發居留簽證，每次不超過 24 個月，其後每次續期約 3 年 | 1 | https://www.immd.gov.hk/eng/faq/newcies.html |
| `leads_to` | 標記為 NOT VERIFIED | **可由未查證升級為已確認**：並非自動取得永久居留，仍須依《入境條例》另行符合「通常居住」滿 7 年之連續居住測試，方具永久居民資格申請條件 | 1 | https://www.immd.gov.hk/eng/faq/newcies.html |
| `dependants` | 標記為 NOT VERIFIED | **可由未查證升級為已確認**：官方 Guidebook 註腳 2 明確定義為配偶（含同性伴侶關係）及未滿 18 歲之未婚子女——與入境處 FAQ 各自獨立敘述一致，可視為兩個一級來源互相印證 | 1（雙一級來源一致） | https://www.newcies.gov.hk/media/tehetmzy/guidebook-for-the-new-capital-investment-entrant-scheme-full-version-en.pdf ；https://www.immd.gov.hk/eng/faq/newcies.html |
| `entry_tax`／`mortgage` | 標記為 NOT VERIFIED | 本輪已查、仍無法確立：官方 Guidebook 全文完全未提及印花稅或按揭；另查得香港對「合資格輸入人才」有 BSD/NRSD 暫緩繳付機制，但無法確認 New CIES 是否包含在該機制範圍內，未採信作為結論 | 1（文件已讀，結論仍未定） | 同上 Guidebook |
| 其餘欄位（`ownership_form`、`offplan`） | — | 其餘欄位核對無誤 | 1 | https://www.newcies.gov.hk/en/application-procedures/application-to-investhk/investment-requirement/ |

**配套要求**：除 HK$30 百萬總投資外，其中 HK$3 百萬須強制投入由香港投資管理有限公司管理之 CIES 投資組合（無論不動產配置如何選擇，這筆錢無法迴避）；申請前 6 個月須持有淨資產達 HK$30 百萬（本輪未再獨立確認此點的具體文字，非否定其存在）。

**建議修正**：`term`、`stay`、`leads_to`、`dependants` 四欄可由「本次未查證」全部改寫為上述已確認內容並附來源；`entry_tax`、`mortgage` 維持未定。

---

### sri-lanka — 投資人簽證類別

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`／機制（匯款而非契據、五項合格用途、每2年覆核） | 如現有記載 | 確認無誤，直接讀取 Guideline PDF 逐條核對 | 1 | https://www.immigration.gov.lk/content/files/visa/Guideline%20Investor%20Visa%20Category%20doc%202.pdf |
| `ownership_form`（4 樓限制已於 2018 年廢除） | 如現有記載 | 確認無誤，直接讀取 2018 年第 21 號法公報原文核對 | 1 | https://www.srilankalaw.lk/gazette/2018_pdf/21-2018_E.pdf |
| `entry_tax`（土地租賃稅是否已因 2018 年修正而全免） | 標記為 NOT VERIFIED | **可由未查證升級為已確認**：《土地（讓與限制）法》2024 年整合版第 7(1)(b) 條——四樓以上、租期滿 35 年、簽約前已全額匯入者，**完全豁免**土地租賃稅；第 6(3)(c)/(d) 條對較短租期之公寓則為**優惠稅率 7.5%**（一般稅率為 15%）。實務上此議題對多數投資人簽證買家已無實益，因為四樓以上公寓本可依《公寓所有權法》取得完全所有權（非租賃），而土地租賃稅依定義僅課徵於租賃 | 1 | https://lankalaw.net（《土地（讓與限制）法》2024 年整合版 PDF） |
| `stay` | 標記為 NOT VERIFIED | 本輪已查、仍無法確立：Guideline PDF 多次解析失敗（含改用 curl+pdftotext），未能取得可用文字判讀續證/維持條件段落 | — | 同上 Guideline PDF（技術性解析失敗） |
| `leads_to` | 標記為 NOT VERIFIED | 本輪已查、仍無法確立，但有新的負面訊號：移民局官方 Residence Visa 索引頁（id=18）目前列出之 16 類簽證中，**完全沒有「永久居留簽證」這個類別**——這不足以證明投資人簽證不通往 PR，但顯示斯里蘭卡可能根本沒有一般性的 PR 簽證管道，值得繼續追查 | 1（索引頁本身，但屬間接推論） | https://www.immigration.gov.lk/pages_e.php?id=18 |
| 其餘欄位（`term`、`dependants`） | — | 其餘欄位核對無誤 | 1 | 同 Guideline PDF |

**配套要求**：Guideline 文件本身揭露現有記載未寫入的必要條件——體檢報告、3 個月內之無犯罪紀錄證明、安全審查表、投資計畫書；退出時須提前 2 個月書面通知，永久離境前 14 個工作天另行通知。文件全程未見最低實際居住天數要求。

**建議修正**：`entry_tax` 由「未查證」改為上述已確認的免稅/優惠稅率內容；配套要求段落補上體檢／良民證／安審表／退出通知等條件；`stay`、`leads_to` 維持未定。

---

### sri-lanka-2 — 黃金天堂簽證計畫

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `dependants`（站主特別要求釐清：核心答案可能是「可以，僅年齡上限未確認」） | 歸為未能查證年齡上限，framing 較模糊 | **釐清完成，可拆成兩個乾淨的判定**：（1）配偶及依親人本身**可以**納入申請——現行頁面明文「Spouses and dependents may be included」，並列出婚姻證明、良民證、子女出生證明等文件要求，此點**確認無誤（tier 1）**；（2）2022 年設立通函所定「子女須未滿 16 歲」的年齡上限，現行頁面**未重申**，故該細節**維持無法確立**——與站主提示的方向一致：核心資格是「可以」，未確立的只是年齡上限這個子細節，不應把整個 dependants 欄位都標成未查證 | 1（資格本身）／無法確立（年齡上限子細節） | https://eservices.immigration.gov.lk/golden-paradise-visa.html |
| `entry_tax` | 標記為 NOT VERIFIED | 與 sri-lanka 條目同一部法律規範所有公寓租賃，適用相同的第 7(1)(b) 全免／第 6(3) 優惠稅率結論 | 1 | 同 sri-lanka 條目之 lankalaw.net PDF |
| 計畫現行狀態（是否仍在運作） | Confidence 已標 medium，因官方訊號矛盾 | **本輪再次查證，強化而非推翻原判**：直接讀取移民局主站官方 Residence Visa 索引頁（id=18），確認**完全沒有列出「Golden Paradise」**——只存在於 eservices 子網域，主站索引不收錄。另查核「My Dream Home」（id=19）以排除「這是改名後的黃金天堂」的可能性——確認不是同一計畫（另一制度為 USD 15,000 存款＋按月匯款，僅供延期非新申請，與不動產無關）。這不足以證明黃金天堂已停辦，但確實是主管機關自身索引頁的缺席，站主原本的 medium confidence／狀態未定框架**本輪確認仍是正確判斷，不宜升級或降級** | 1（索引頁缺席為新訊號，非決定性證據） | https://www.immigration.gov.lk/pages_e.php?id=18 |
| `stay`／`leads_to`／`offplan` | 標記為 NOT VERIFIED | 本輪已查、仍無法確立：直接讀取現行黃金天堂頁面全文，頁面僅涵蓋資格條件、合格投資項目、10 年效期與申請步驟，完全未觸及這三項 | 1（頁面已讀，結論仍未定） | https://eservices.immigration.gov.lk/golden-paradise-visa.html |

**配套要求**：本輪未查得存款門檻之外的額外必要條件（如保費／收入證明），此點維持無法確立而非否定其存在。

**建議修正**：`dependants` 欄位建議拆寫為「配偶及依親人可納入（tier 1 確認）；子女年齡上限沿用 2022 年通函之未滿 16 歲抑或已鬆綁，未能確認」，取代目前較模糊的措辭；`entry_tax` 可比照 sri-lanka 條目補上稅務減免內容；confidence 維持 medium 不變。

---

### indonesia — 第二家園限期居留許可（rumah kedua）

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `term`（最長 5 年，第 105 條第 10 項第 a 款，先前草稿誤傳為 10 年） | 如現有記載 | **確認無誤，且本次為關鍵覆核**：另一組初步查證一度質疑「5年是硬上限還是5或10年可選」，本輪改以 curl＋pdftotext 直接下載條例全文兩個獨立官方鏡像重新比對，確認第 105 條第 10 項第 a 款確實是「最長 5 年」的硬性上限，「5或10年」的說法出自同條例下*其他*子類別（特殊技能人才 105(10)(b)、國際名人 105(10)(c)）的報導混淆所致，與第二家園（56 條）無關。現有記載原文正確，**無需修正** | 1（兩個獨立官方鏡像原文核對） | https://peraturan.bpk.go.id/Download/330147/Permenkumham%20Nomor%2022%20Tahun%202023.pdf |
| `leads_to` | 標記為 NOT VERIFIED | **可由未查證升級為已確認**：條例第 120 條第 1 項明定，第二家園許可持有人可經身分轉換取得永久居留許可（KITAP）——與投資人黃金簽證（39/40條）並列於同一條文的適用範圍內 | 1 | 同上 PDF |
| `stay` | 標記為 NOT VERIFIED | 本輪已查、確實查無：對條例全文逐句檢索最低在境天數相關用語，條例本身完全無此類條款——這是讀完整部法規後的結果，不排除規定藏在其他行政通函，但主管法規本身沉默 | 1（全文已讀，結論為條文沉默） | 同上 PDF |
| `offplan`／`mortgage` | 標記為 NOT VERIFIED | 本輪已查、仍無法確立：條文僅寫「承諾購買價值達門檻之公寓」，對完工狀態與融資均未觸及；另行搜尋僅查到杜拜黃金簽證的無關內容，未能找到印尼專屬答案 | 1（條文沉默）／無法確立 | 同上 PDF |
| `entry_tax` | 標記為 NOT VERIFIED | 本輪已查、可補充一般性資訊：三方二級來源一致，印尼房產轉讓稅（BPHTB）為成交價之 5%（扣除各地區免稅額後），另有 2.5% 之資本利得預扣稅（PPh）——但這是印尼一般稅制，非簽證專屬規則，非一級來源 | 2（一般稅制，非簽證專屬） | https://bektu.com；https://balizero.com；https://livenworkindonesia.com |
| 其餘欄位（`min_value`、`ownership_form`、`last_change`） | — | 其餘欄位核對無誤 | 1 | 同上 PDF |

**配套要求**：房產（100 萬美元）與存款（13 萬美元，須存於國營銀行、申請人本人名下）為互斥替代方案（"atau"），非必須疊加；房產須於核發後 90 天內完成承諾購買。

**建議修正**：`leads_to` 由「未查證」改為「經身分轉換可取得 KITAP 永久居留（第 120 條第 1 項）」；`entry_tax` 可補充一般性 BPHTB／PPh 稅率作為參考（註明非簽證專屬）；`term` 無需修正，本輪已強化其正確性。

---

### indonesia-2 — 黃金簽證：個人投資人

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`（10年檔僅公寓100萬美元一種房產選項，5年檔完全無房產選項僅證券35萬美元） | 如現有記載 | 確認無誤，直接讀取第 39/40 條原文核對 | 1 | https://peraturan.bpk.go.id/Download/330147/Permenkumham%20Nomor%2022%20Tahun%202023.pdf |
| `leads_to` | 標記為 NOT VERIFIED | **可由未查證升級為已確認**：與第二家園條目相同的第 120 條第 1 項，投資人（含此黃金簽證個人投資者檔）可經身分轉換取得 KITAP 永久居留 | 1 | 同上 PDF |
| `dependants` | 標記為 NOT VERIFIED | **可由未查證升級為已確認**：雖無投資人專屬之依親條款，但第 33 條第 2 項第 h 款／第 105 條第 8 項第 b 款設有適用**所有**限期或永久居留許可持有人之通用家庭團聚類 ITAS，涵蓋本檔個人投資人 | 1 | 同上 PDF |
| `stay`／`offplan`／`mortgage` | 標記為 NOT VERIFIED | 與 indonesia 條目同一部法規，結論相同：`stay` 為條文全文沉默（已通讀確認）；`offplan`／`mortgage` 條文未觸及，另行搜尋未果 | 1（條文已讀）／無法確立 | 同上 PDF |
| `entry_tax` | 標記為 NOT VERIFIED | 與 indonesia 條目相同的一般性 BPHTB 5%／PPh 2.5%，非簽證專屬 | 2 | 同 indonesia 條目來源 |
| 其餘欄位（`ownership_form`、`last_change`、總局長可行政調整門檻之保留條款） | — | 其餘欄位核對無誤 | 1 | 同上 PDF |

**配套要求**：與 indonesia 條目相同的土地限制（外國人不得取得 Hak Milik）；10 年檔之公寓選項與第二家園之公寓選項數字上重疊（皆為 100 萬美元），差異僅在期限與非房產替代方案門檻（第二家園存款 13 萬美元 vs. 本檔證券 70 萬美元起）。

**建議修正**：`leads_to`、`dependants` 由「未查證」改為上述已確認內容並附第 120 條、第 33/105 條來源；`entry_tax` 可比照 indonesia 條目補充一般性稅率參考。

---

### south-korea — 觀光休閒設施投資移民制

| 欄位 | 現有記載 | 查證結果 | 來源 tier | 來源 URL |
|---|---|---|---|---|
| `min_value`（KRW 10 億統一門檻、F-2→F-5）| 如現有記載 | 確認無誤，兩個獨立韓文媒體來源一致 | 2 | https://www.hanbitdaily.com/news/417094；http://www.jejudomin.co.kr/news/articleView.html?idxno=216512 |
| 地區指定與到期日衝突（現有記載已標記為未解決） | Confidence 已標 medium，因官方入口網與濟州道公告互相矛盾 | **本輪查證讓衝突更嚴重而非解決**：找到濟州投資入口網轉載之濟州道 2026/2/17 公告，內容與更早一篇報導的「延至 2026 年底」不同，改稱延至 **2027 年 12 月 31 日**——即市面上現在同時流通三個不同的到期日版本（官方入口網原始版：多數地區已於 2026/4/30 或 5/19 屆期；較早報導版：延至 2026 年底；濟州道最新公告版：延至 2027 年底），且該公告明確僅為**濟州道地方政府**發布，並非法務部全國性公告，法務部官報（고시）原文本輪仍未能定位。維持現有記載的 medium confidence 與「未解決」框架，且應在文字中加註「已出現第三個版本的日期」 | 2（濟州道公告，非法務部原文） | https://www.investkorea.org/jj-kr/bbs/i-1150/detail.do?ntt_sn=491731 |
| `stay` | 標記為 NOT VERIFIED | 本輪已查、仍無法確立：透過代理繞過官網空白渲染問題，直接讀取 visa.go.kr 該制度頁面全文，頁面描述投資與 5 年維持條件，但未列最低在境天數要求 | 1（頁面已讀，結論仍未定） | https://www.visa.go.kr/openPage.do?MENU_ID=1040202 |
| `dependants` | 標記為 NOT VERIFIED | 本輪已查、部分升級但未達一級標準：兩個移民代辦聚合網站聲稱引用 ifez.go.kr／visa.go.kr 內容，稱 F-2 涵蓋「投資人及其配偶與未婚子女」，但本輪直接讀取 visa.go.kr 官方頁面本身並未看到這段文字，屬轉引非親自核對，僅達 tier 2 且來源性質偏向移民代辦聚合站，未達本資料集的可信門檻，維持未查證 | 2（未達採信標準） | 未採信，維持未查證 |
| `entry_tax` | 標記為 NOT VERIFIED | 本輪已查、仍無法確立：僅查得韓國一般不動產取得稅（취得稅）約 1–4%（含附加稅約 4.6%），非投資移民專屬規則，且來源非法務部/國稅廳一級頁面，另查得研議中之外國買家額外附加稅（12–26%）目前仍為未立法的草案，切勿誤植為現行法 | 未達標準 | 未採信，維持未查證 |
| 其餘欄位（`ownership_form`、`leads_to`、`mortgage`） | — | 其餘欄位核對無誤 | 1 | https://www.visa.go.kr/openPage.do?MENU_ID=1040202 |

**配套要求**：投資標的須為法務部指定地區內之指定觀光休閒設施，非一般住宅；投資期間設定擔保、遭查封或以之借款皆會使 F-5 轉換所需之「維持投資」條件失效。

**建議修正**：地區到期日衝突段落建議加註「已出現第三個版本（2027年底）」，並明確提醒讀者這是地方政府公告，非法務部全國公告，任何據此投入資金者務必向主管出入境事務廳當面確認；其餘欄位維持未定不動。**本筆是本輪查證中最值得站主注意的個案之一：越查證，衝突越明顯，而非越清楚。**

---

## 附註：分類方式與資料集既有查證品質的評語

- **thailand-2、indonesia** 是本輪查得最乾淨的兩筆——尤其 indonesia 的「5年上限」爭議，本輪特意用兩個獨立官方鏡像重新核對條文原文，確認資料集原本的判斷是對的，值得記一筆：**這次不是資料集錯了，是查證過程本身曾經一度自我懷疑，後來證明多慮**。
- **vanuatu、south-korea** 的「confidence: medium／not_established」框架，本輪主動重查後**沒有被推翻，反而被強化**——尤其南韓的地區到期日問題，本輪找到的新資料讓衝突版本從兩個變成三個，站主現有的保守 confidence 判斷是正確的，不建議升級。
- **sri-lanka-2** 的「計畫是否仍在運作」同樣是本輪重查後維持原判的例子：移民局主站索引頁再次確認不收錄黃金天堂，但這仍不足以斷言計畫已停辦，medium confidence 是恰當的定位。

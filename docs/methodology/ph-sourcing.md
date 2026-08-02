# 菲律賓（馬尼拉 NCR）資料取數紀錄

**建立日**：2026-08-02 ｜ **產出檔**：`data/ph-market.json` ｜ **服務對象**：`/ph/report.html` 與 `/ph/macro.html`（規格見 `.claude/notes/market-page-spec.md`）

本文件記錄**實際取數過程**：路徑怎麼拼、哪些期別可得、解析踩到的坑、口徑校驗結果。取數範圍與各資料源的初步可行性判斷已由兩份偵察報告完成，本文件不重寫其內容，只在銜接處摘要：

- `docs/methodology/ph-manila-sourcing.md`——價格、租金、供給、空置、POGO 的可行性偵察
- `docs/methodology/ph-credit-macro-sourcing.md`——信貸、需求、總經、制度的可行性偵察

比照範本：`docs/methodology/napic-stock-sourcing.md`（本站對馬來西亞做同一件事的成果）。

---

## 一、範圍定案：放棄分區

站主決定不做 Makati CBD／BGC／Ortigas／Rockwell 的分區價格比較。官方住宅價格指數（BSP RPPI）與官方租金分項（PSA CPI 04.1）地理分層都只到 NCR／AONCR；唯一到位的分區資料來自 Colliers Philippines 一家民間顧問公司，且其未售存量數字在不同期報告間自相矛盾一個數量級（見第七節）。

因此：**價格與租金收 NCR 全域層級**；Makati／Taguig 的市級建照仍取，作為供給側細節，但不拿來做分區價格推論。

---

## 二、價格：BSP RPPI 與 RREPI

### 2.1 取數路徑

兩份偵察報告已確認 SharePoint REST API 路徑（`_api/web/lists/getByTitle('Prices')/items`）。本輪直接下載：

```
https://www.bsp.gov.ph/Statistics/Prices/RPPI.xlsx     （現行，2019=100）
https://www.bsp.gov.ph/Statistics/Prices/rrepi.xls      （已停用，appraised value 口徑，Q1 2014=100）
```

curl + 瀏覽器 UA 直接可下載（bsp.gov.ph 不在 Cloudflare 之後），無需瀏覽器。

### 2.2 RPPI.xlsx 結構解析

Table 1（指數本體）是一張寬表，**同一個 sheet 內左右並排兩個時間區塊**：欄位 D-Y 是 2023Q1-2026Q1（含年度均值欄），欄位 AA-AZ 是 2019Q1-2022Q4（同樣含年度均值欄）。七個地理區塊（Philippines / NCR / AONCR / Balance GMA / Metro Cebu / Metro Mindanao / Other Areas）縱向排列，每區塊固定 15 列間距，每區塊內 Index／YoY%／QoQ% 三個子區段各 3 列（All types／Condominium／Houses）。

解析腳本：`parse_rppi.py`（列出於 sources.rawFiles 路徑）。抽出結果：Philippines/NCR/AONCR/Balance GMA/Metro Cebu/Metro Mindanao/Other Areas 各自的 All types／Condominium unit／Houses 三個房型的季度指數與官方發布的 YoY%，2019Q1–2026Q1，共 29 期，無缺口。

**交叉驗證**：以 BSP RPPI Q4 2025 新聞稿（`RPPI-Report-2025-Q4.pdf`）與 Global Property Guide 引用數字逐項核對解析出的 2025Q4 全國 All types YoY，結果完全吻合（全國 +1.6%、NCR +2.3%、AONCR +1.0%）。三項數字精確到小數點後一位全部通過，解析邏輯視為驗證正確。

Table 2（同一份出版品附表）是每季新增房貸核准案件**筆數**（非金額），同一種寬表結構，同一個解析器換一組行號即可用，是本輪唯一取得的、有 NCR 地理分項的信貸相關資料——但要記得它衡量的是交易活躍度，不是信貸存量或金額。

### 2.3 RREPI（rrepi.xls）結構

xls（BIFF 格式，`xlrd` 讀取）。**只有年度資料**（2016-2024，9 年），不是季度——偵察報告原先寫「2016Q1-2024Q4 季頻」，實測後修正為年度。基期是 Q1 2014=100（與 RPPI 的 2019=100 不同基期）。地理層三個（Philippines/NCR/AONCR），房型五種（All types／Single detached-attached／Duplex／Townhouse／Condominium，**官方明文無 apartment 指數**：樣本數過少未生成）。

**口徑警語必須寫進頁面**：RPPI 是 acquisition cost（合約成交價），RREPI 是 appraised value（鑑價）。BSP 官方 metadata 原文對比："Unlike the RREPI, which was based solely on the appraised value per square meter of new building properties, the RPPI is constructed using the acquisition cost of residential properties." 兩者不得合併成單一長序列，`data/ph-market.json` 分開存放於 `price.rppi` 與 `price.rrepi_discontinued` 兩個獨立節點。

---

## 三、信貸

### 3.1 Real Estate Exposure（住宅／商業放款餘額）

檔案：`historical 8.xls`（透過 SharePoint RichText_Content 清單的 `$filter=Title eq 'Real Estate Exposure'` 取得下載連結，偵察報告已記載此路徑，本輪直接沿用）。

**結構坑**：欄位分成多個並排區塊（Bank Proper and Trust Department / Bank Proper / Trust Department），且早期年份（2013-2021）每年 4 個季度合併成一個 4 欄區塊、標籤只印在區塊首欄，2022 年起改為逐季獨立欄且每欄都有標籤。解析時不能只抓「標籤非空」的欄，要先用 row8（類別列）定位每個「Bank Proper and Trust Department」區塊的欄位範圍，再在範圍內用 row9（期別列）取有值的欄——否則會漏掉早期年份的 Q2-Q4。

解析結果：2013Q1–2026Q1，53 個季度，全國層級（Philippines Banking System），無缺口。含 Real Estate Loans／Residential／Commercial 的 Levels（十億披索）與 Current／Past Due／Gross NPL 三態，另附對應比率欄。**全國層級，無 NCR 分項**——偵察報告已指出這是本序列的邊界。

驗算（非本檔宣稱，僅供品質檢查）：2026Q1 住宅類 past-due/RREL 比率 8.83%，遠高於 2013Q1 的 3.85%，數字本身無異常（無負值、無爆量斷點），視為解析正確的間接佐證。

### 3.2 房貸利率與 Contracts to Sell

`monthlylendingratestype.xls`，月頻，2020-01 至 2025-10。欄位結構同樣是寬表並排，Housing Loans 類別起始欄第 73 欄（0-index），Contracts to Sell 起始欄第 17 欄，各自 4 個子欄（Indicative High/Low、Effective High/Low）。已解析完整 70 個月。

`Contracts to Sell`（銀行貼現開發商分期付款應收帳款）只有利率沒有金額——這印證了「開發商自帶分期融資規模無法量化」的既有缺口，本輪未能突破。

---

## 四、租金：PSA CPI 04.1 Actual Rentals for Housing

這是本輪**最關鍵的任務**：確認菲律賓 CPI 租金分項的採價方法論（新約 vs 續約存量），以及取得實際數值序列。兩者都完成。

### 4.1 方法論確認（站主提供兩份 PSA 一手文件，已親自核對頁碼）

- `/Users/ivanchang/Downloads/CPI User's Manual.pdf`（NSO 出版，2010 年，共 101 頁，2000-based CPI 系列技術文件，作者 NSO，`pdfinfo` 確認 CreationDate 2010-06-13）
- `/Users/ivanchang/Downloads/Technical Notes - CPI All Items_14.pdf`（現行 2018-based CPI 技術文件，11 頁；本輪也獨立從官方 URL 下載確認：`https://psa.gov.ph/system/files/psd/Technical%20Notes%20-%20CPI%20All%20Items_14.pdf?ver=2025-04-03-083030-400`，取得路徑是在 PSA OpenSTAT 表格頁的「Footnotes」彈窗裡點擊「Technical Notes on 2018-based Consumer Price Index for All Income Households」連結）

**逐字核對結果**（用真實瀏覽器直接讀取頁面文字，非轉述）：

CPI User's Manual p.41-42（Data Collection Procedures 段落）：
> "In the case of house rentals, the same addresses or the same housing unit regardless of its occupants must be the source of data in every survey period. If the structure is no longer existing or if it has ceased to be rented, an appropriate substitute should be selected. Thus, if the sample house which is to be replaced has only one bedroom then the replacement must also be a house with only one (1) bedroom. The amount of rental paid monthly by the households must exclude payments made on electricity and/or water. This survey of house rentals is done monthly."

同文件 p.57-58（Owner-Occupied Housing 段落）：
> "Imputed rents from owner-occupied housing are not included in the monthly price survey. Rental under the Housing and Repairs group is represented by a measure of actual rental rates. Rental rates are collected from fixed residential units that are actually rented at the time of the survey. The survey of rental rates is done monthly."

Technical Notes（現行 2018-based，p.3，Data Collection Procedures 段）：**逐字重複**上述第一段文字，證實現行 2018-based CPI 沿用同一套 1994 年以來未變的採價規則。

**判讀**：這是「固定住宅單位配對樣本」（matched/fixed panel）——同一地址每期追蹤，換房客時仍追同一物件並記錄新房客的實際租金（而非鎖定舊房客的續約價）。這一點優於原先擔心的「與馬來西亞 CPI 041 同型（鎖定續約存量）」情境：菲律賓的設計理論上會在住戶更替時把新約租金帶入指數。**但設計說明不等於實際行為**，所以本輪對實際月度資料跑了批次重訂價檢定（見 4.3）。

### 4.2 數值序列取得：PSA OpenSTAT PX-Web

`psa.gov.ph` 全站對 curl/WebFetch 回 Cloudflare 403，但真實瀏覽器可以正常穿透（兩份偵察報告已確認此結論）。本輪的新發現：**PSA OpenSTAT（`openstat.psa.gov.ph`）是獨立子網域，走 PX-Web 系統**，其表格互動介面（Choose table → Choose variable → Show table）可以逐步用滑鼠/鍵盤操作選出 Geolocation（Philippines/NCR/AONCR）、Commodity Description（04.1 - ACTUAL RENTALS FOR HOUSING）、Year（2018-2026）、Period（Jan-Dec）四個維度後產生資料表。

**操作坑**：
1. Commodity Description 清單有 354 個項目（COICOP 全分類樹狀展開成扁平清單），用搜尋框打「rental」會連「rental of communication equipment」都跳出來；改用瀏覽器 select 元素的原生 type-ahead（點擊清單後連續按鍵盤 `0` `4`）可以跳到「04 - HOUSING...」，再用方向鍵下移 3 格精確落在「04.1 - ACTUAL RENTALS FOR HOUSING」。
2. Geolocation／Commodity 的多選用一般 click 不會疊加選取，必須用 `cmd`（非 `ctrl`）修飾鍵點擊才能複選——這點在 macOS Chrome 上與一般網頁的 `ctrl`-click 慣例不同，需注意。
3. 顯示表格頁本身有「最多 1000 列 30 欄」的螢幕呈現上限，一次查全部 2018-2026 會被裁到只剩 30 欄（約 2.5 年）。解法：分批查詢，每批限制在 2-3 年份（year variable 逐次只勾選 2-3 個），跑 5 批分別涵蓋 2018-2020(Apr)／2020-2022(Apr)／2022-2024(Apr)／2024-2026(Apr)／2026(全年至 Jun)，批次間刻意重疊 1 個月份做交叉驗證（例如兩批都含 2020 年 1-4 月，兩次讀出的數字逐一核對完全一致）。
4. 表格內建的 CSV/Excel 匯出功能（Save table as → CSV）本輪測試回應 HTTP 520（伺服器端錯誤），改用直接讀取畫面呈現的 HTML 表格（`get_page_text`）取得數字，人工核對後轉存。

解析結果：Philippines／NCR／AONCR 三個地理層級，2018-01 至 2026-06，102 個月，完整無缺口，基期 2018=100。

### 4.3 批次重訂價檢定（實測，非文件說明）

方法論說明優於預期，但不能只信文件——馬來西亞 CPI 041 的教訓正是「文件看起來正常，實際行為是季頻批次重訂價」（197 個月只變動 68 次，其中 66 次集中在季度第二個月）。對菲律賓三個地理層級的月度序列跑同一套檢定：

| 指標 | Philippines | NCR | AONCR |
|:---|---:|---:|---:|
| 總期數 | 102 | 102 | 102 |
| 月度變動次數 / 總轉換數(101) | 86 (85.15%) | 60 (59.41%) | 88 (87.13%) |
| 變動月份分布 | 12個日曆月平均分散 | 同左 | 同左 |
| YoY 最低值 | +1.03%（2021-07） | +0.44%（2024-12） | +1.03%（2021-12） |
| YoY 曾轉負 | 否 | 否 | 否 |

計算口徑（method 與數字同檔存放，見 `data/ph-market.json` 的 `validation.rentalBatchRepricingTest.method`）：逐月變動次數除以總轉換數（相鄰兩月數值不同即計 1 次）；變動月份分布按發生的日曆月（1-12）分桶計數，若集中在特定月份即為批次重訂價訊號；YoY 逐月計算 (index[t]/index[t-12]-1)×100。腳本：`compile_and_test.py`（scratchpad）。

**結論**：三個層級的 change_rate（59%-87%）遠高於馬來西亞案例的約 34.5%（68/197），且變動月份在 12 個日曆月間分布平均，沒有出現「集中在特定月份」的批次重訂價訊號（對照馬來西亞 66/68 集中在單一月份的極端不均勻分布）。**未偵測到批次重訂價**，PSA CPI 04.1 的月頻標籤與其實際變動行為一致。

但也發現一個限制：三個層級的 YoY 在 2018-2026 全期間從未轉負，即使在 2020-2021 疫情期間（一般預期租賃需求驟降）仍維持正值。這**不是**批次重訂價的證據（變動月份分布依然平均），但可能反映配對樣本設計本質上比市場成交價序列更平滑、對市場轉折的反映有時間落差。使用建議寫入 `validation.rentalBatchRepricingTest.usageGuidance`：可用於存量租金水準與趨勢，不可用於精確轉折時點判斷。

NCR 的 change_rate（59.41%）明顯低於全國與 AONCR（85%+），這點在文件裡誠實記載為觀察但非定論——可能反映 NCR 樣本住宅單位換手/重新採價頻率較低，但不構成批次重訂價的證據。

---

## 五、總經：政策利率、CPI、匯率、外債

### 5.1 政策利率（RRP）

`bsprates.xls`，日頻原始資料回溯至 1986 年（4.2MB，10,608 列）。本檔 downsample 為月頻（每月最後一筆有效值），保留兩個制度轉換註記（2016-06-03 改採 IRC 系統；2023-09-08 改採 Target RRP 為主要政策利率）供跨期比較時警示。

### 5.2 CPI headline（非租金子項）

`prices2018.xls`（BSP 轉載 PSA 資料），三個 sheet（Monthly PHL/NCR/AONCR）。**解析踩到一個關鍵坑**：Year 欄位在 2025 年之後從數字型別（float 2025.0）改成字串型別（`'2025'`），若解析器只判斷 `isinstance(y, float)` 會直接漏掉 2025-2026 整整 18 個月的資料且不報錯（靜默失敗）——第一版解析結果 NCR/AONCR 只到 2023-12，加上字串型別判斷後補齊到 2026-06。這是本輪唯一一個「解析器邏輯錯誤導致資料靜默缺失」的案例，記錄下來提醒下一輪。

### 5.3 披索/美元匯率

`pesodollar.xlsx`，月頻回溯至 1945 年，本檔收 2013-01 起（與信貸序列對齊）。Average 與 End-of-Period 兩個口徑並存。近一年（2025-06 至 2026-06）從約 61.25 附近的貶值趨勢已在資料中呈現。

### 5.4 BIS 房價指數與有效匯率（FRED，本輪新增）

規格要求長序列優先，且 FRED 是取得跨國可比 BIS 序列的標準路徑。**WebFetch 對 fred.stlouisfed.org 一律回 403，Bash 環境的 curl 對此網域完全連不上（HTTP 000，判斷為環境層級的網路限制，非站台封鎖，因為同一輪對 bsp.gov.ph／psa.gov.ph／lawphil.net 的 curl 都正常）**，唯一可行路徑是瀏覽器同源 fetch：

```js
// 在 fred.stlouisfed.org 任一頁執行
const r = await fetch('/graph/fredgraph.csv?id=SERIES_ID', {credentials:'same-origin'});
const t = await r.text();
```

**取數技巧的技巧**：`javascript_tool` 的回傳值本身有截斷限制（實測約 1000-1500 字元即出現 `[TRUNCATED]`），對於數百筆的月頻序列（如 1994-2026 月頻的 REER，390 筆）完全不夠用。突破方法：把抓到的完整字串寫入當前頁面的 DOM（`document.body.innerHTML = '<pre>'+text+'</pre>'`），再改用 `get_page_text` 工具讀取——後者沒有同樣的截斷限制，本輪實測一次讀出 9334 字元的合併多序列文字完全無誤。

**候選 ID 實測結果**（依序把泰國那輪用的國碼 TH 換成 PH／PHL 逐一測試）：

| 候選 ID | 結果 | 說明 |
|:---|:---|:---|
| `QPHN628BIS` | ✅ 存在 | BIS 住宅價格指數（**名目**），標題為 "Residential Property Prices for **Makati**, Philippines"——BIS 對菲律賓的參考城市序列是 Makati，不是全國或 NCR 加總，2019=100，2008Q1-2026Q1，73 期 |
| `QPHR628BIS` | ✅ 存在 | 同上**實質**版（已用 CPI 平減），同期間 |
| `QPHHAM770A` | ❌ 404 | BIS 家戶信用占 GDP——菲律賓不在 BIS 此資料庫涵蓋範圍內（查證方式：FRED 搜尋介面確認，非工具限制） |
| `QPHPAM770A` | ❌ 404 | BIS 民間非金融部門信用占 GDP——同上，未被涵蓋 |
| `EXPHUS` | ❌ 404 | Fed H.10 口徑雙邊匯率——命名規則不適用菲律賓，已用 BSP 自有 `pesodollar.xlsx` 取代（品質更好，一手非轉載） |
| `RBPHBIS` | ✅ 存在（改搜尋找到） | BIS 實質有效匯率（REER），2020=100，1994-01 至 2026-06 月頻，390 期 |
| `NBPHBIS` | ✅ 存在 | 同上名目版（NEER） |
| `NYGDPPCAPKDPHA` → `NYGDPPCAPKDPHL` | ❌→✅ | ID 應為 ISO3 三碼 **PHL** 非 PHA，修正後可用。World Bank 實質人均 GDP（2010 美元），1960-2025 |
| `FPCPITOTLZGPHA` → `FPCPITOTLZGPHL` | ❌→✅ | 同上修正，World Bank CPI 通膨率，1960-2025 |
| `DDDI12PHA156NWDB` | ✅ 存在（改搜尋找到） | IMF/GFDD 民間信用占 GDP（替代 BIS 未涵蓋的空缺），1960-2021 |
| `DDOI11PHA156NWDB` | ✅ 存在 | World Bank 匯款流入占 GDP，1977-2020，與 BSP 匯款金額序列互補 |
| `POPTTLPHA148NRUG` | ✅ 存在 | UN/World Bank 總人口（百萬人），1950-2023 |

**BIS 房價實質序列的解讀價值**：規格點名這是最有力的一張圖。菲律賓（Makati）名目指數從 2008Q1 的 95.8 漲到 2026Q1 的 306.0（+219%），但實質指數（已扣除通膨）從 107.8 只漲到 183.4（+70%）——漲幅超過六成是通膨堆出來的名目幻覺，而非購買力累積。且實質指數在 2015Q1（102.05）附近曾經見頂又回落，2013-2015 一波急漲後橫盤了近十年才在 2024 年重新站上前高，這是一條完整的「補跌-橫盤-重新突破」敘事線，適合放進 report 第一部或 macro 週期篇。

### 5.5 外債（BSP，本輪新增，回應「政府財政與外債」需求）

`Statistics/External/extdebtratios.xls`（Sheet: `EDRatios_202604`）年度序列 1985-2025，41 年。取數路徑沿用第一輪已驗證的 BSP SharePoint 清單機制（`ph_external_api.json`，本輪重新檢視該清單找到 "External Debt Ratios"、"Total Philippine External Debt" 等條目）。

解析出：外債總額、公私部門拆分、國際準備（GIR）、外債占 GDP／GNI 比率、償債負擔（DSB）占 GDP 比率，1985-2025 逐年無缺口。**敘事線**：外債占 GDP 比率從 1985 年債務危機高點 75.5% 結構性去槓桿至 2025 年 30.3%，國際準備從 1985 年僅 10.9 億美元成長至 2025 年 1108 億美元——這是 macro 頁總經結構篇很強的長期去槓桿敘事。另外注意 `totalextdebt.xls`（Total Philippine External Debt）**只有單一期快照**（2026 年 3 月底），不是時間序列，不要誤用。

---

## 六、人口、家戶形成、所得分布（PSA OpenSTAT API，本輪新增）

### 6.1 逆向出 PX-Web 的 JSON-stat REST API

`openstat.psa.gov.ph` 除了互動式 UI 之外，本輪確認存在標準 PX-Web REST API，且**完全不需要另外處理 Cloudflare**（因為走同一個瀏覽器 session，已經通過 CPI 查詢時的驗證）：

```
GET  /PXWeb/api/v1/en/DB/{路徑}          逐層列出目錄，回傳 [{id,type,text}]，type='l'=資料夾、type='t'=表格
GET  /PXWeb/api/v1/en/DB/{路徑}/{表格id}  取得該表 metadata（variables 陣列，含每個變數的 values/valueTexts）
POST /PXWeb/api/v1/en/DB/{路徑}/{表格id}  帶 body {query:[{code,selection:{filter:"item",values:[...]}}], response:{format:"json"}}，取得 JSON-stat 資料
```

這條路徑比逐頁點擊 UI 快非常多，尤其對 population／FIES 這類目錄結構單純、變數少的表格。用法示範（於任一 openstat.psa.gov.ph 頁面用 `javascript_tool` 執行）：

```js
const query = {
  query: [
    {code: "Geographic Location", selection: {filter: "item", values: ["0","1","13","17"]}},
    {code: "Parameter", selection: {filter: "item", values: ["0","1","2"]}}
  ],
  response: {format: "json"}
};
const r = await fetch('/PXWeb/api/v1/en/DB/1A/PO/0011A6DPHH0.px', {
  method: 'POST', credentials: 'same-origin',
  headers: {'Content-Type':'application/json'},
  body: JSON.stringify(query)
});
```

`values` 陣列裡的數字是該變數 valueTexts 清單的**索引**（從 0 起算），不是實際的地名或年份字串，需要先 GET 該表 metadata 取得 valueTexts 對照表才能正確填值。

### 6.2 人口普查（2000/2010/2015/2020）

- 表格 `1A/PO/0081A6DTPG0.px`：Total population by geographic location（based on 2000, 2010 and 2015 Censuses）——Philippines／NCR／Makati／Taguig 三個普查年份的總人口
- 表格 `1A/PO/0011A6DPHH0.px`：Total Population, Household Population, and Number of Households: Philippines, 2020——2020 年普查另外拆出戶數，可算平均家戶規模

結果：Philippines 2000/2010/2015/2020 分別為 76,506,928／92,337,852／100,981,437／109,033,245；NCR 同期 9,932,560／11,855,975／12,877,253／13,484,462；Makati 471,379／529,039／582,602／629,616；Taguig 467,375／644,473／804,915／886,722（2020 普查另口徑略調整為 City of Taguig 獨立於 Pateros 之外，索引與 2000/2010/2015 版本略有差異，已在解析時逐一核對地名對齊，非直接假設索引一致）。2020 年戶數：Philippines 26,393,906／NCR 3,499,652／Makati 186,381／Taguig 246,873。

**非連續年頻**：普查五年一次，不是年度序列，2000-2010 與 2010-2015 之間的年度人口只能靠內插（本檔不內插，只給普查實測點）。

### 6.3 FIES（家庭所得與支出調查）2023

表格 `1E/IE/0011E3ANIE0.px`：家庭數（千戶）、平均家庭年所得、平均家庭年支出，Philippines／NCR／Makati／Taguig。結果：Philippines 27,480 千戶、平均所得 35.323 萬披索／年；NCR 3,633 千戶、51.352 萬；**Makati 206 千戶、79.954 萬（全國所有地理單位中最高，含省市層級）**；Taguig 289 千戶、51.960 萬。

**缺口**：OpenSTAT 上這個資料夾（`1E/IE`）本輪只列出 2023 年版的 12 張表（Table 1-12，涵蓋人均所得十分位、Gini 係數、支出結構、家庭規模別所得等），**沒有找到歷史年份（如 2015／2018／2021 等前幾輪 FIES）的對應表格**，所得長期序列本輪未能取得——與泰國那輪的已知缺口（`market-page-spec.md` 第七節記載）相同性質。下一輪如需歷史所得序列，建議查 PSA OpenSTAT 以外的舊版出版品系統，或 PSA 官網的 FIES 歷史新聞稿頁面。

Gini 係數表格（`0051E3AGCF0.px`）本輪已確認存在並可查詢，但受限於時間未及取值，留待下一輪。

---

## 七、供給：Makati／Taguig 建照

沿用兩份偵察報告已驗證的路徑：`rssoncr.psa.gov.ph` 對 curl/WebFetch 回 Cloudflare 403，真實瀏覽器可正常穿透。本輪透過該站內建 Google Custom Search（`/search/google?keys=...`）快速定位到 Makati 與 Taguig 2023-2024 逐季完整報告（Q1-Q4，共 8 篇 Special Release），逐篇讀取正文取得：核准建照總數、住宅／非住宅／增改建維修三類拆分、建設總值、平均每平方公尺造價，且每篇都附上一年前同季的比較數字（等於間接拿到 2023 年同期資料）。

另外用同一搜尋找到 **2026-07-21 剛發布的「Private Building Construction Statistics National Capital Region: 2025」年度彙總報告**——這是全 NCR 層級的 2025 年度總結，含 Makati 全年建案總數（1,159 件，全區佔比 9.3%）、Taguig 全年建設總值（156.5 億披索，佔比 11.7%）、Pasig 全年建設總值（202.6 億披索，佔比 15.2%）。這份報告的完整統計表附件（`Statistical Table_2025.xlsx`，17.94KB）本輪嘗試透過瀏覽器下載按鈕取得但未成功寫入本機檔案系統（下載動作未在 `~/Downloads` 產生檔案，判斷為執行環境的下載權限限制），故 2025 年 Makati/Taguig/Pasig 的完整月/季拆分未取得，只有年度報告正文提到的敘述性數字。

Pasig 建照本輪僅取得 2024Q4 與 2025 年度部分片段（透過搜尋結果摘要，未逐篇核對一手 PDF）。Pasay 本輪未及查證。

**口徑提醒**：核准建照（approved building permits）≠ 完工，也≠ 動工，PSA 官方限制條款逐篇皆有註明。Makati 2024 年逐季（Q1-Q4）核准建照數：63／399／409／346；Taguig 同期：237／243／268／222——兩市建照量高度季度波動，不宜只看單季推論趨勢。

---

## 八、空置與未售存量：Colliers（民間單一來源）

本節完全沿用 `ph-manila-sourcing.md` 第三節已核實的內容，本輪未新增瀏覽，只做結構化轉存至 `data/ph-market.json` 的 `data.vacancy.colliers`。關鍵事實照登：

- Metro Manila 整體空置率：2024 年底 23.9% → 2025 年底 24.7%（歷史新高）→ Colliers 預測 2026 年底 25.6%
- Bay Area（POGO 承租最集中處）：2025 年底官方原文「remains above 50%」，2026 年底 Colliers 預測「approaching 60%」
- **未售存量數字有一組未解的矛盾**：Colliers Q4 2025/Q1 2026 報告給出全區約 78,600-79,200 戶未售，但 2026-07-30 BusinessMirror 報導的 Colliers Q2 2026 簡報卻提到「remaining inventory」僅 27,900→32,600 戶，量級差約一個數量級，本輪未能釐清統計範疇是否不同（例如僅指某收入分層或某類已核准未動工量），**兩組數字不應被視為同一件事的更新值而混用**，已在 JSON 中並列存放並加註警語
- Makati CBD／BGC／Ortigas／Rockwell 個別空置率：**缺口**，只有社群媒體二手轉述 Colliers 簡報口頭數字（「Makati CBD 已售完零未售」「BGC 未售<1%」），這些是未售比例不是空置率，兩者定義不同，未列入 JSON 的可信數值

---

## 九、已知限制與缺口總表

| 項目 | 狀態 | 原因 |
|:---|:---|:---|
| Makati/BGC/Ortigas/Rockwell 分區房價 | 🔴 缺口 | 官方統計不到位，唯一來源 Colliers 口徑不明 |
| Makati/BGC/Ortigas/Rockwell 分區租金 | 🔴 缺口 | 同上 |
| Makati/BGC/Ortigas/Rockwell 分區空置率精確值 | 🔴 缺口 | 僅社群媒體二手轉述，未經一手核實 |
| 開發商自帶分期融資規模 | 🔴 缺口 | Contracts to Sell 只有利率沒有金額；三大開發商財報本輪未取得 |
| 政府公債殖利率（無風險利率） | 🔴 缺口 | Bureau of Treasury／PDS Group 皆為前端動態渲染，WebFetch/curl 未能取得內容 |
| 營建成本指數、地價序列 | 🔴 缺口 | PSA 掌管，本輪時間分配未觸及 |
| FIES 歷史所得序列（僅 2023 單期） | 🔴 缺口 | OpenSTAT 上只有 2023 年版表格，未見歷史年份 |
| Pasig/Pasay 建照完整逐季序列 | 🟡 部分 | 僅取得片段，未逐篇核對一手 PDF |
| 2025 年 Makati/Taguig/Pasig 建照逐季拆分 | 🟡 部分 | 僅有年度彙總報告的敘述性數字，附件 xlsx 下載未成功 |
| BIS 家戶信用/民間非金融部門信用占 GDP | 🔴 不存在 | 菲律賓不在 BIS 此資料庫涵蓋範圍，非查詢問題，已用 IMF/GFDD 替代序列補位 |
| Gini 係數（PSA OpenSTAT 已確認存在） | 🟡 待補 | 表格 ID 已找到（`0051E3AGCF0.px`），本輪未及取值 |

---

## 十、工具與方法論教訓（供下一輪參考）

1. **FRED 只能走瀏覽器同源 fetch，Bash curl 對 fred.stlouisfed.org 完全連不上**（HTTP 000），與 bsp.gov.ph/psa.gov.ph 等其他站台的行為不同——判斷是這個環境對特定網域的出網限制，不是通用規則，每個新網域都要先用 curl 探測一次再決定要不要上瀏覽器。
2. **`javascript_tool` 的回傳值有截斷限制（約 1000-1500 字元）**，抓長序列時務必先把資料寫入頁面 DOM，再用 `get_page_text` 讀取（後者沒有同樣限制，實測 9334 字元一次讀出無誤）。這個技巧同時解決了 PX-Web 表格資料的讀取問題。
3. **PX-Web 系統（BSP／PSA 都用）通常有一個未在 UI 明顯曝光的 JSON-stat REST API**（`/PXWeb/api/v1/{lang}/{path}`），比逐頁點擊互動介面快很多，且完全繼承瀏覽器 session 的 Cloudflare 通過狀態，值得作為所有 PX-Web 系統的預設優先路徑。
4. **macOS Chrome 上的多選修飾鍵是 `cmd` 不是 `ctrl`**，這點在網頁 `<select multiple>` 元素上與部分教學文件的預設假設不同，跨平台操作前先用單一元素測一次再批次操作。
5. **政府統計檔案的年份欄位型別可能在某個時間點從數字切成字串**（本輪 BSP CPI 檔案在 2025 年之後從 float 切成 str），純用 `isinstance(x, float)` 判斷會靜默漏資料且不報錯，務必同時處理兩種型別或用 regex 容錯解析。
6. 瀏覽器「下載」按鈕點擊在本環境未必會在 `~/Downloads` 產生實體檔案（測試過 PDF 與 xlsx 兩種情境皆未成功），需要檔案內容時優先用「讀取畫面呈現內容」或「curl 直連」，下載按鈕不可靠。

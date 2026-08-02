# 菲律賓信貸、總經與制度資料可行性偵察

偵察日期：2026-08-02 ｜ 目的：判斷菲律賓（馬尼拉精華區）能否開市場頁的前置作業，非分析 ｜ 範圍：信貸、需求側、總經與利率、制度與交易成本四類——**不含價格、租金、供給與空置**（另一組在查，本次刻意不碰）
服務對象：`four-quadrant-v1.md` §2 四象限恆等式、§5 資料需求規格格式沿用；狀態分級沿用 `br-credit-stock-sourcing.md` 慣例

**前提校正（來自 `data/visa-property.json` philippines 筆與 `docs/verification/visa-apac.md` 查證結論）**：SRRV Classic 的法律結構是「先以存款取得簽證，其後可將該存款轉換為不動產」，方向與「購屋換身分」相反——購屋是存款核發後的一項許可用途，不是取得簽證的手段。門檻依年齡與是否領退休金分四級（USD 15,000～50,000），不動產轉換的最低值是 USD 50,000（區分所有權狀，且 CCT 須已登記於主申請人名下，故排除預售屋）。本輪不動這個結論，市場頁若要引用 SRRV，必須維持這個方向性。

---

## 摘要裁決

### 四象限各格能填到什麼程度

| 象限 | 恆等式 | 本次涵蓋 | 能不能填滿 |
|:---|:---|:---|:---|
| **NW** 資產定價 `P=R/i` | i 的分解（房貸利率、政策利率、信貸） | ✅ 本次核心範圍 | **能，且信貸腿的資料深度優於馬來西亞**。BSP 有一個連續、按季更新的「Real Estate Exposure」官方統計（住宅／商業 REL 餘額、現時／逾期／不良分拆），2013Q1 至今無缺口；房貸利率月頻 IRLD 序列（2020 起）；政策利率日頻（1986 起）。P（成交價）本身不在本次範圍（另一組在查）。**但信貸序列只到全國層級，沒有 NCR 分項**——NCR 分項只存在於「貸款筆數」（flow，非餘額）與「新增貸款利率」兩類資料裡，不在餘額（stock）資料裡 |
| **SW** 開發決策 `C=f(P,K)` | K（重置成本）、C（完工量） | 🔴 本次未觸及 C；K 完全未查 | 本次任務範圍未涵蓋完工量與營造成本指數的直接取數（PSA 掌管，見下方 PSA 全站被擋）。**這是本輪最大的空白之一，需要下一輪專門查 PSA 的 Construction Statistics / BCI，以及地價序列（大概率跟馬來西亞、巴西一樣缺）** |
| **SE** 存量調整 `ΔS=C−δS` | S_total 序列 | 🔴 本次未觸及 | 存量、家戶數、普查資料由 PSA 掌管，PSA 全站（`psa.gov.ph`、`openstat.psa.gov.ph`、`psada.psa.gov.ph`）在本環境一律回傳 Cloudflare 機器人驗證頁（`Just a moment...` 攔截頁），無法取得任何內容，連測都測不到。`data.gov.ph`（開放資料入口）是 Angular SPA，資料經由前端 bundle 動態載入，本輪未能逆向出其 API 端點 |
| **NE** 空間市場 `D(R,X)=S_effective` | 需求側 X（匯款、人口、所得） | 🟡 部分能 | **OFW 匯款（NE 最重要的需求驅動之一）取得完整、高品質序列**——BSP 月頻 Personal Remittances，2005 年起（現金匯款年頻回溯至 1970 年），且 BSP 官方定義明文將「資本移轉（用於興建住宅）」列為 Personal Remittances 的構成之一，直接對應房產需求的因果鏈。**人口／家戶形成／所得分布（FIES）三項全部卡在 PSA 被擋**，本輪拿不到 |

### 最強的一塊
**BSP 的兩個未被大量使用的統計來源**：(1) SharePoint REST API——BSP 統計頁面背後是 SharePoint Online，可繞過前端頁籤直接用 `_api/web/lists/getByTitle('{ListName}')/items` 取得結構化的檔案清單（含每個表格的 EXCEL/PDF 直連網址），比逐頁點擊快得多，且沒有機器人驗證；(2) `Real Estate Exposure` 統計（Table 8/17/26/35/44）——按季更新、Residential/Commercial REL 分拆、含現時／逾期／不良（NPL）三態，2013Q1 至最新一期（本輪抓到 2026Q1）連續無缺口。**更重要的是制度與交易成本這一塊**：菲律賓央行的《外匯交易法規手冊》(MORFXT) 把「購買區分所有權單位」明文定性為外人直接投資（FDI），且**強制規定須向 BSP 直接登記**（非經銀行代辦），登記與否直接決定日後能否透過銀行體系兌換外匯匯出——這是一個有明確法源、可操作性極高、且過去坊間資料極少講清楚的制度細節，查證品質遠高於馬來西亞與巴西兩輪對制度面的掌握程度。

### 最弱的一塊
**開發商自帶分期付款（in-house financing）的規模完全查不到**。本輪嘗試從 Ayala Land、SM Prime、Megaworld 三家上市開發商的年報／SEC 17-A 抓「應收分期付款」（installment contracts receivable）數字，全部受阻：三家公司投資人關係網站均為 JS 前端渲染或觸發 403，PSE Edge（菲律賓交易所揭露系統）與 annualreports.com 的公司頁面均未能定位到具體 PDF 直連；本輪 WebSearch 配額已在其他任務中用盡，DuckDuckGo 與 Bing 的網頁爬取路徑先後被機器人驗證擋下。**唯一找到的旁證**是 BSP 月頻《新增貸款與放款利率》資料裡有一個獨立的「Contracts to Sell」放款類別——銀行向開發商購買「合約待售」應收帳款（即銀行貼現開發商的分期付款合約）——但這個表**只有利率，沒有金額**，無法用來估計規模。這印證了任務假設的方向（銀行信貸數據可能系統性低估真實槓桿），但本輪無法量化低估的幅度。次弱的是 PSA 掌管的所有資料（供給、存量、人口、所得、營造成本）——全站被 Cloudflare 擋死，是比馬來西亞、巴西都更徹底的封鎖（NAPIC、IBGE 至少能拿到部分內容）。

### 制度限制對「外國人可投資範圍」的實際界定
**沒有全面禁止，但範圍被壓縮到「僅區分所有權公寓、且有 40% 集合上限」這一個窄通道**。1987 年憲法第十二條第 7 節明文禁止私有土地移轉予不具資格者（繼承除外），第 8 節僅為喪失菲律賓籍之天生菲律賓公民留了例外。公寓法（RA 4726）第 5 條把 60% 菲律賓籍下限（即 40% 外資上限）掛在「區分所有權公司」的股權／會員權層級，而非直接掛在個別單位交易上——這是為什麼外國人能個別持有公寓單位所有權狀（CCT），因為限制作用在法人集合層級，不在個人交易層級。第 6(c) 條的**預設**計算基礎是「每單位一等分」（按戶數，非樓地板面積），但條文明寫「除非開發約定另有規定」，實務上多數建案的主契約會改用樓地板面積加權分配份額——這點本輪從統計而非逐案查證，是條文結構的推論，不是逐案驗證的事實。長期租地是唯一的替代持有形式，但有兩套互不相同的制度：一般外國人適用 1974 年第 471 號總統令（上限 25 年＋可續 25 年，共 50 年，不限用途），大型合格投資適用 1993 年投資人租賃法 RA 7652（上限 50 年＋可續 25 年，共 75 年，但僅限工業區／加工廠／觀光專案等達最低投資額門檻的合格投資，一般個人購屋不適用）——SRRV 轉換選項用的是前者（25＋25 年），不是後者，這是過去容易混淆的兩套法律。

---

## 逐來源

狀態分級：`✅ 已驗證`＝路徑實測可行且看到數值 ｜ `🟡 待驗證`＝來源已知、路徑未實測或僅次級來源佐證 ｜ `🔴 缺口`＝無直接來源或本輪被封鎖無法測試

### 一、信貸（NW 象限，T6 鏈環所需）

| 來源 | 機構 | 內容 | 期間 | 頻率 | 狀態 | 坑 |
|:---|:---|:---|:---|:---|:---|:---|
| Real Estate Exposure — Philippine Banking System (Table "8") | BSP | 不動產貸款（REL）餘額，拆 Residential／Commercial，各再拆現時／逾期／不良（NPL），另有比率欄（PDREL/REL 等） | 2013Q1 至 2026Q1（最新一期），單一快照檔另有 Mar-26 | 季 | ✅ | **有兩個檔案**：`8.xls`（僅最新一期快照）與 `historical 8.xls`（2013 起完整序列，206 欄）。**必須用 historical 版本**，快照版看起來像完整表但只有一期。單位為十億披索，全國層級（Philippine Banking System），無 NCR 分項 |
| Real Estate Exposure — 按銀行類別分拆（Table 17/26/35/44） | BSP | 同上指標，分別對應 Universal & Commercial／Universal／Commercial／Thrift Banking System | 同上 | 季 | ✅ | 只按銀行類別拆，**不按地區拆**，NCR 仍然拿不到 |
| KB Loans Outstanding to the Real Estate Sector（`rel.xls`，Table 26 舊版） | BSP | 商業銀行對不動產部門放款（按用途：住宅／商業，再細分社會住宅／其他） | 2008Q1–2012Q3，**之後未再更新** | 季 | 🟡（歷史值可信，但已停更） | **這是個陷阱檔**：檔名與 Financial System Accounts 頁籤上仍掛著同一個標題，容易誤以為是現行序列，實測發現三個分頁（in billions／complete／REF_2008_frp format）全部只到 2012Q3。真正接續此資料的是上面的「Real Estate Exposure」系列（不同檔案、不同分類方式），兩者口徑不完全對得上（此檔以 PSIC 用途分類，Real Estate Exposure 以放款狀態分類） |
| Number of Residential Real Estate Loans Granted — 按住宅類型／按產權狀態（RPPI.xlsx Table 2、Table 3） | BSP | 每季新增貸款**筆數**（非金額），拆 Condominium／Houses，另拆 New／Pre-owned／Foreclosed；有 Philippines／NCR／AONCR 三層地理分項 | 2023Q1–2025Q4（+2026Q1 部分），另有 2019–2022 年度檔 | 季 | ✅ | 這是**唯一有 NCR 分項的信貸相關資料**，但量的是「筆數」不是「金額」，不能直接當信貸存量的地理權重使用，只能當交易活躍度的代理指標 |
| Monthly New Loans Granted and Lending Rates, by Loan Type（IRLD） | BSP | 按貸款用途分類的月度放款利率（Indicative/Effective, High/Low），含「Housing Loans」與「Contracts to Sell」兩個獨立類別 | 2020-01 至 2025-10（p＝初步值），資料揭露「2020 年起才要求銀行依新版 IRLD 報表申報」 | 月 | ✅ | **兩個關鍵發現**：(1) 「Housing Loans」類別明確定義為「個人為取得／興建／改良住宅單位」之貸款——這是最乾淨的房貸利率序列，2025-10 Effective High 8.80%／Effective Low 7.17%；(2) 「Contracts to Sell」類別＝銀行向房產開發商購買（貼現）與購屋人簽訂之分期付款合約應收帳款——**這證實部分開發商自帶分期融資確實會流入銀行體系，但本表只有利率沒有金額**，無法據此估計規模 |
| Loans Outstanding for Production and Household Consumption, PSIC 2009（`kbloanspbs.xls`） | BSP | 按 PSIC 2009 經濟活動分類的放款餘額，含「12. Real Estate Activities」（產業放款）與消費貸款分類 | 長期序列（月頻 keystat 格式，152 欄） | 月 | ✅ | **住宅房貸（RREL）被明文排除在此表的消費貸款分類之外**（表內註腳 4/3：「Excludes residential real estate loans (RREL)」）。這意味著若只看這張表會完全漏掉住宅房貸，必須交叉用上面的「Real Estate Exposure」表才拿得到 RREL 數字——兩表互補、缺一不可 |
| 開發商應收分期付款（installment contracts receivable） | Ayala Land／SM Prime／Megaworld 年報或 SEC 17-A | 資產負債表附註中的分期應收帳款規模，用來直接量測繞開銀行體系的槓桿 | — | — | 🔴 | 本輪完全未取得。三家公司 IR 網站對自動化抓取回應空白／403；PSE Edge 與 annualreports.com 頁面均未定位到可下載 PDF；WebSearch 配額已耗盡，DuckDuckGo／Bing 網頁版搜尋先後遭機器人驗證擋下。**這是本輪最大的未解缺口**，直接對應任務假設「銀行信貸數據可能嚴重低估真實槓桿」，本輪確認了機制存在（見上方 Contracts to Sell 發現）但無法量化幅度 |

### 二、需求側

| 來源 | 機構 | 內容 | 期間 | 頻率 | 狀態 | 坑 |
|:---|:---|:---|:---|:---|:---|:---|
| Personal and Cash Remittances（`ofwp.xls`） | BSP | 海外菲律賓人個人匯款（現金匯款＋實物匯款＋資本移轉），美元計價，另有經季節調整版本（2022 起） | 個人匯款月頻 2005-01 至 2026-05；現金匯款年頻回溯至 1970 | 月／年 | ✅ | **BSP 官方定義明文將「用於興建住宅的資本移轉」列入 Personal Remittances 構成項之一**（見檔內附註 *），這是任務要找的「匯款→房產需求」因果鏈最直接的官方文字佐證，不必自行推論 |
| Cash Remittances, by Country and by Source（`ofw.xls`） | BSP | 按來源國別拆分的現金匯款 | 未逐項核對期間，檔案本身可下載（4.9MB） | 月 | 🟡 | 已下載但本輪未展開解析按國別的分項結構 |
| PSA 人口普查／家戶調查／FIES | PSA | 人口、家戶形成、所得分布 | — | — | 🔴 | **PSA 全站（`psa.gov.ph`、`openstat.psa.gov.ph`、`psada.psa.gov.ph`）在本環境一律回傳 Cloudflare「Just a moment...」機器人驗證攔截頁，回應碼 403，無法取得任何內容**。`data.gov.ph`（開放資料入口）回應 200，但是一個 Angular SPA（`main.28614807276661d4.js`），資料透過前端動態載入而非可直接命中的 REST 端點，本輪未能在時間內逆向出其 API 路徑。這是本輪查證流程中唯一完全空手而回的機構級來源 |

### 三、總經與利率

| 來源 | 機構 | 內容 | 期間 | 頻率 | 狀態 | 坑 |
|:---|:---|:---|:---|:---|:---|:---|
| Target Reverse Repurchase (RRP) Rate（`bsprates.xls`） | BSP | 政策利率（現制：Target Overnight RRP Rate，2023-09-08 起採用） | 日頻，回溯至 1986 年附近（10,608 列），現值 2026-07-15＝4.75% | 日 | ✅ | 序列內含兩次制度轉換註記（2016-06-03 改為 IRC 走廊系統；2023-09-08 改採 Target RRP 為主要政策利率、變動利率標售），**跨制度比較需注意口徑不連續**，不能當單一同質序列直接拉長期回歸 |
| Residential Property Price Index (RPPI) 隨附的貸款利率／CPI 等表 | BSP | 見上方信貸表；另 CPI（2000/2006/2012/2018 四種基期）與核心通膨已在同一個 SharePoint 清單（"Prices"）中列出，本輪未逐一下載驗證數值 | — | 月／季 | 🟡 | 清單存在、路徑已知（見下方「取數路徑實測」），但本輪聚焦信貸與匯款，CPI 具體數值未逐一核對 |
| Philippine Peso per US Dollar（`pesodollar.xlsx`） | BSP | 披索兌美元匯率，月／日／年三種頻率 | 月頻回溯至 1945 年；日頻另存一表 | 日／月／年 | ✅ | 近期趨勢明確：2025 年中約 55.6～57.4，2026 年 6 月已貶至約 61.25——**一年內約貶值 8～9%，這是外國買家美元計價報酬的重大變數**，任務點名的「披索計價與美元計價報酬可能差很多」在本輪取到的數字上已有初步驗證方向，但本輪未做完整換算 |
| 政府公債殖利率（無風險利率） | Bureau of Treasury／PDS Group | 國庫券／國庫債標售結果與次級市場殖利率（如 PDST-R2 基準） | — | — | 🔴 | `treasury.gov.ph` 與 `pds.com.ph` 皆回應 200，但頁面為前端動態渲染，WebFetch 未能取得實際內容；BSP 自家的「Selected Domestic Interest Rates」(`sdir.xls`) 只涵蓋銀行存放款利率與 BSP 自身工具（RRP／OLF／SDA／BSP Securities 等），**不含政府公債殖利率**，本輪未找到直接的無風險利率序列 |
| 營建成本指數 | PSA | 建材、人工成本指數，對應四象限 K（重置成本）的營造成本半邊 | — | — | 🔴 | 同上 PSA 全站封鎖，本輪完全未查得 |
| 地價序列 | — | K 的另一半 | — | — | 🔴 | 本輪未查（時間分配優先給信貸與制度面），且以馬來西亞／巴西兩輪的經驗判斷，此類序列在多數市場本就罕見公開 |

### 四、制度與交易成本

| 項目 | 結論 | 法源 | 來源 tier | 狀態 |
|:---|:---|:---|:---|:---|
| **私有土地外國人持有禁令** | 1987 年憲法第十二條第 7 節：除繼承外，私有土地不得移轉予不具資格取得公地者（即非菲律賓籍個人或非 60% 菲籍法人）；第 8 節：喪失菲籍之天生菲律賓公民為唯一例外，得依法律限制受讓私有土地 | 1987 年菲律賓憲法 Art. XII §7–8，逐字核對於 lawphil.net 原文 | 1 | ✅ 已驗證（補上視覺化資料集裡先前未能取得的憲法本文） |
| **公寓法 40% 外資上限的計算基礎** | 上限透過「區分所有權公司」股權／會員權層級運作，而非直接掛在個別單位交易上——第 5 條規定：若共有部分由業主直接共有，單位不得移轉予非菲籍人士或非 60% 菲籍法人（繼承除外）；若共有部分由區分所有權公司持有，凡會導致該公司外資比例超過法定上限之移轉一律無效。**計算基礎（樓地板面積 vs 單位數）：第 6(c) 條的預設規則是「每單位一等分」（按戶數均分，非按樓地板面積加權），但條文明寫「除非主契約／規約另有約定」——實務上多數建案的主契約會改採樓地板面積加權分配，惟本輪未逐案查證，此為條文結構推論** | 共和國第 4726 號法（公寓法）§5、§6(c)，逐字核對於 lawphil.net 原文 | 1（條文本身）／2（實務加權慣例，未逐案驗證） | ✅ 已驗證條文／🟡 實務慣例待驗證 |
| **超過上限時的實務處理** | 依 §5 文義，若移轉將導致區分所有權公司外資比例超過法定上限，該移轉**本身無效**（void），非僅遭行政駁回。業界慣例（未逐案驗證）是開發商／區分所有權公司追蹤外資持股累計比例，逼近 40% 上限時停止受理外國買家過戶 | 同上 §5 | 1（無效效果）／🟡（業界慣例，未逐案驗證） | 🟡 |
| **長期租地持有——兩套互不相同的制度** | (1) 一般外國人：1974 年第 471 號總統令，上限 25 年＋可續約 25 年（共 50 年），不限用途，適用於私有土地泛用租賃（含 SRRV 轉換選項採用此制）；(2) 合格投資人：1993 年投資人租賃法（RA 7652），上限 50 年＋可續約 25 年（共 75 年），但僅限工業區／加工廠／農工企業／觀光專案等達最低投資額門檻之合格投資，一般個人購屋／自住不適用 | PD 471（1974）§1；RA 7652（1993），逐字核對於 lawphil.net 原文 | 1 | ✅ 已驗證（並釐清坊間常混淆的兩套制度） |
| **印花稅（DST）** | 不動產移轉（買賣／贈與）：每 1,000 披索（或其零數）課徵 15 披索，即consideration 或公允市值兩者取高之 1.5%——2017 年 TRAIN 稅改（RA 10963）第 69 條將稅率從原稅率倍增至此數 | 國家內地稅法（NIRC, RA 8424）§196，經 RA 10963 §69 修正，逐字核對於 lawphil.net 原文 | 1 | ✅ 已驗證（較前一輪簽證資料集查證時的 tier 2／未確認官方一手文件狀態明確升級） |
| **資本利得稅（CGT）——僅限個人出售資本資產性質不動產** | 6%，稅基取成交價與公允市值兩者較高者；適用對象為「個人（含遺產與信託）」出售分類為資本資產之境內不動產，條文未限定居民身分，故非居民個人出售亦適用同一稅率。**開發商／公司出售分類為存貨（一般資產）之不動產不適用此 6% CGT**，另循一般公司所得稅＋預扣稅制度課徵，本輪未查得該預扣稅之具體稅率表 | NIRC §24(D)(1)，逐字核對於 lawphil.net 原文 | 1（6% CGT 本身）／🔴（開發商銷售適用之預扣稅率表未查） | ✅／🔴 |
| **移轉稅（地方稅，LGU 自訂）** | 省：上限為交易對價或公允市值兩者較高者之 0.5%（1% 之 50%）；市（含大馬尼拉都會區內之市，如 Makati、Taguig）：依地方政府法第 151 條，市得比照省/鎮上限再加徵至多 50%，故市轄移轉稅上限為 0.75%。**實際稅率由各市自訂稅則決定，本輪未取得 Makati、Taguig 兩市各自現行稅則的具體數字** | 地方政府法（RA 7160）§135、§151，逐字核對於 lawphil.net 原文 | 1（法定上限）／🔴（兩市各自實際稅率） | ✅（上限）／🔴（實際稅率） |
| **不動產稅（RPT，持有稅）——制度結構** | 基本稅：市（含大馬尼拉都會區內之市）上限為**核定價值（assessed value）**之 2%；另可加徵教育基金特別稅（SEF）上限 1%，兩者合計法定上限 3%。核定價值＝公允市值 × 核定率（assessment level），核定率依用途與價值級距分層——住宅用地上限 20%；住宅建物依公允市值級距 0%～60%（如 500 萬～1,000 萬披索區間為 50%）。**這代表「3% 上限」是對核定價值課徵，實際對市值的有效稅率遠低於表面稅率**（因核定率通常遠低於 100%），此為統計結構推導，非本輪對特定物件的實測計算 | 地方政府法（RA 7160）§233、§235、§218，逐字核對於 lawphil.net 原文 | 1 | ✅ 已驗證（制度結構）／🔴（Makati、Taguig 兩市各自現行實際稅率——兩市官方網站均為前端動態渲染或遭阻擋，本輪未取得） |
| **資金匯出——是否有 BSP 登記前置要求（任務點名的「大坑」）** | **有，且法源精確可引**。BSP《外匯交易法規手冊》(MORFXT) §32.2 明定：外人來台投資原則上不強制登記，**除非日後欲以銀行體系（AAB／AAB 換匯公司）之外匯資源辦理資本匯回或收益匯出**，此時登記即成為前提要件。§33.1(b) 明文將「取得或購買區分所有權單位」列為外人直接投資（FDI）的態樣之一。§36.1(a)(ii) 進一步規定「區分所有權單位之取得或購買」**必須直接向 BSP 登記**（經 BSP 線上系統、免費、須於法定起算日起 1 年內申請 Form W），屬於直接向 BSP 登記的第 36 條類別，而非經授權銀行代辦登記的第 37 條類別。§38.1 規定：經 BSP 登記之投資，有權以 AAB 外匯資源辦理資本與相關收益之**完全且立即匯回**。**換言之：若購入資金／投資未經 BSP 登記，法規並未明文禁止該投資本身，但銀行體系日後為其兌換外匯匯出時，登記文件（Bangko Sentral Registration Document, BSRD）是申請購買外匯的前提要件之一，未登記將難以透過正規銀行管道取得外匯完成資本匯回**——這正是任務描述的「實務上的大坑」 | BSP《外匯交易法規手冊》(Manual of Regulations on Foreign Exchange Transactions, MORFXT，2025 年 5 月版本)§32、§33.1(b)、§36.1(a)(ii)、§38，逐條核對於 BSP 官方 PDF 原文 | 1 | ✅ 已驗證（本輪制度面最強的發現） |
| SRRV 存款金額、轉換條件、持續要件 | 沿用視覺化資料集既有查證結論（詳前提校正段），本輪未重複查證 | PRA 官網、轉換檢核表 PDF（前一輪已核對） | 1 | ✅（沿用前輪） |

---

## 取數路徑實測

### 已驗證可行、可重複使用的路徑模式

**BSP SharePoint REST API**（統計頁面背後的隱藏端點，本輪最重要的方法論發現）：
```
GET https://www.bsp.gov.ph/_api/web/lists/getByTitle('{ListTitle}')/items?$top=200
Header: Accept: application/json;odata=verbose
```
- 免金鑰、免登入；每個「Statistics」頁籤背後對應一個 SharePoint 清單，清單名稱需先讀取頁面原始 HTML 找 `$pnp.sp.web.lists.getByTitle("...")` 字串取得（例如 Prices 頁對應清單 `Prices`，Financial System Accounts 頁對應 `Financial System Accounts`，External 頁對應 `External Accounts`）
- 回傳的每筆項目含 `Title`、`Category_x0020_1`、`Tab`、`PDF`、`EXCEL`、`HTML` 欄位，`EXCEL` 欄位即為可直接下載的檔案相對路徑（接在 `https://www.bsp.gov.ph` 之後）
- **坑**：`$select=*`（萬用字元）會被 WAF 判定為異常請求並回傳「Your requested page is not available」的封鎖頁，必須省略 `$select` 或明確列出欄位名稱
- **坑**：部分統計頁（如 Real Estate Exposure）的資料**不是**存在這種「清單項目含檔案連結」的結構，而是整段 HTML 表格直接存在一個共用的 `RichText_Content` 清單裡，需改用 `$filter=Title eq '{標題}'` 查詢該清單，回傳欄位 `Content` 內含完整 HTML 片段（內嵌真正的下載連結），需再解析一層

**BSP 統計檔案直連下載**：
```
https://www.bsp.gov.ph/Statistics/{子目錄}/{檔名}.xls(x)
```
- 免登入，UA 需為瀏覽器字串（`curl -A "Mozilla/5.0..."`），部分路徑大小寫與空白需 URL encode（`%20`）
- 多數檔案為 `.xls`（BIFF 格式，需 `xlrd` 而非 `openpyxl`），部分新檔為 `.xlsx`（RPPI、pesodollar 等，需 `openpyxl`）

**BSP《外匯交易法規手冊》(MORFXT) PDF**：
```
https://www.bsp.gov.ph/Regulations/MORFXT/MORFXT.pdf
```
- 找法：先讀取 `https://www.bsp.gov.ph/SitePages/Regulations/RegulationsList.aspx?TabId=1` 原始 HTML，搜尋 "Foreign Exchange Transactions" 字串即可定位到直連 PDF（此頁不走 SharePoint REST API 模式，是靜態內嵌連結）
- 93 頁，`pdftotext -layout` 可正確抽取條號與內文，本輪即以此逐條核對登記／匯出相關條文

**LawPhil Project**（菲律賓法律全文資料庫，非移民中介）：
```
https://lawphil.net/statutes/{repacts|presdecs}/{年份目錄}/{法案代碼}.html
```
- `curl -A "Mozilla/5.0"` 直接可讀，免登入、免機器人驗證
- **坑**：WebFetch 工具對長篇法條頁面常在段落中途截斷（回傳「未包含該條文」），需改用 `curl` 存原始 HTML 後以 Python `re.sub` 剝除標籤、`str.find` 定位條號逐段核對，比依賴 WebFetch 摘要可靠

### 完全測不到、需要人工介入或另尋路徑的

- **PSA 全站**（`psa.gov.ph`、`openstat.psa.gov.ph`、`psada.psa.gov.ph`）——Cloudflare 機器人驗證頁（`challenges.cloudflare.com`），`curl`／WebFetch 均回 403，無法繞過
- **`data.gov.ph`**——回應 200 但為 Angular SPA，資料經前端 bundle 動態載入，本輪未逆向出 API 路徑
- **Ayala Land／SM Prime／Megaworld 投資人關係網站**——JS 前端渲染（curl 拿到空殼或 403），annualreports.com 與 PSE Edge 均未能定位到具體年報 PDF 直連
- **Bureau of Treasury（`treasury.gov.ph`）／PDS Group（`pds.com.ph`）**——回應 200 但前端動態渲染，WebFetch 未能取得殖利率內容
- **Makati／Taguig 兩市官方網站**——`makati.gov.ph` 為前端渲染的入口頁；`taguig.gov.ph` 直接回 403
- **搜尋引擎**：本輪 WebSearch 配額於任務開始前已用盡（其他任務消耗）；DuckDuckGo HTML 版（`html.duckduckgo.com/html/`）觸發機器人驗證頁（「Select all squares containing a duck」）；Bing 網頁版（`www.bing.com/search`）初次查詢回傳與查詢完全無關的結果（懷疑查詢字串未被正確處理），後續查詢直接觸發驗證碼頁。**三條路徑全部失效，本輪僅能依賴已知官方網域的直接猜測與逐頁探索**，這是相較於巴西那一輪（尚有 CKAN／SIDRA API 與部分 DuckDuckGo 可用）明顯更差的檢索條件

---

## 已知限制與缺口

1. **NCR 層級的信貸「存量」（餘額）資料不存在，只有「流量」（新增筆數）有 NCR 分項。** BSP 的 Real Estate Exposure 系列（住宅／商業 REL 餘額，含現時／逾期／不良）只到全國層級；有 NCR／AONCR 分項的只有「每季新增貸款筆數」統計，且是筆數不是金額。若市場頁需要「NCR 信貸強度」的量化指標，本輪找到的資料只能支持用「NCR 佔全國新增房貸筆數之比重」做間接代理，不能直接算出 NCR 信貸餘額或信貸/GDP 一類的槓桿指標。

2. **開發商自帶分期付款規模完全未量到，這是四象限 NW 象限裡最大的未解問題。** 任務假設「銀行信貸數據可能嚴重低估真實槓桿」在本輪找到了機制性佐證（BSP「Contracts to Sell」放款類別的存在，證明銀行體系確實會貼現部分開發商應收帳款），但無法量化規模，因為唯一能直接量到規模的來源（三大開發商財報附註）本輪完全未取得。下一輪若要補這塊，建議：(a) 直接嘗試 SEC 菲律賓的 iView 系統（本輪未測試）；(b) 嘗試 Google Finance／Yahoo Finance 等財經聚合站是否轉載關鍵財務附註；(c) 待 WebSearch 配額重置後用更具體的查詢（如 `"installment contracts receivable" Ayala Land 2025 annual report site:ayalaland.com.ph`）。

3. **PSA 掌管的四類資料（供給／完工量、存量、人口與家戶形成、所得分布 FIES、營造成本指數）本輪全部拿不到。** 這比馬來西亞（NAPIC 部分可測）、巴西（IBGE SIDRA API 可測部分內容）都更徹底地被封鎖——PSA 全站的 Cloudflare 機器人驗證在這個環境無法繞過。這代表四象限的 SE（存量調整）與 SW（開發決策，除信貸外）兩格，以及 NE 象限的人口與所得兩個變數，目前完全空白，不是「弱」而是「無」。下一輪若要補齊，可能需要：(a) 換一個不同的出口 IP／環境重試；(b) 嘗試 PSA 是否有對等於 BSP SharePoint 那種可繞過前端的隱藏 API；(c) 退而求其次查詢 CountrySTAT-Philippines 或聯合國統計司等轉載 PSA 官方數字的國際機構資料庫（但須明確標註為二手轉載，非 PSA 一手）。

4. **地價序列與政府公債殖利率（無風險利率）兩項本輪完全未查。** K（重置成本）因此完全無法組出，i 的分解也缺無風險利率這一角——這兩項在時間分配上被排在信貸與制度面之後，本輪未觸及，不是查了查不到。

5. **Makati、Taguig 兩市實際的移轉稅稅率與不動產稅稅率，本輪只查到地方政府法設定的全國統一上限，查不到兩市各自現行稅則的具體數字。** 兩市官方網站均無法在本環境正常抓取內容（前端動態渲染或直接 403）。市場頁若要引用具體稅率數字，目前只能寫「法定上限 X%，實際稅率依各市稅則另定」，不能寫死一個數字。

6. **CGT／DST／移轉稅／RPT 四項交易成本的查證品質參差**：CGT（個人資本資產）與 DST 兩項本輪查到直接的一手法條文字，信賴度高；移轉稅與 RPT 只查到「法定上限」的一手條文，實際地方稅則（Makati、Taguig 各自的稅率）本輪未查到，也未查到開發商／公司出售不動產適用的預扣稅（creditable withholding tax）具體稅率表——這個缺口意味著「一手新成屋／預售屋交易」（多數外國買家的實際交易型態）的完整稅負結構，本輪只拼出了一半（DST 有，CGT 不適用於開發商銷售但替代稅制未查，移轉稅與 RPT 只有上限）。

7. **本輪的檢索工具鏈幾乎全滅**：WebSearch 配額於任務開始前已用盡（非本輪任務消耗，是同一 session 內先前工作累積），DuckDuckGo 與 Bing 的網頁爬取路徑先後遭機器人驗證擋下，`web.archive.org` 依既有工具限制本就被擋。本輪能取得的所有資料，全部來自「已知官方網域＋逐頁探索＋SharePoint REST API 逆向」這條路徑，沒有任何一步依賴通用搜尋引擎的結果。這代表本報告對「已知來源清單」的覆蓋率仍有相當大的補強空間——很可能還有本輪未觸及、但確實存在的官方統計來源（尤其 PSA 底下的具體資料集名稱與網址，本輪完全靠猜測，未經搜尋驗證窮舉）。

---

## 樣本檔案存放位置

以下樣本檔已存於 scratchpad，供正式取數階段複用（路徑：`/private/tmp/claude-501/-Users-ivanchang-malaysia-property/b1d2b60c-c4a2-467e-835a-97042652a9d2/scratchpad/`）：

**信貸**：`ph_realestate_exposure_8.xls`（最新一期快照，勿用於序列）、`ph_realestate_exposure_hist8.xls`（2013Q1 起完整序列，正確用這份）、`ph_realestate_exposure_content.html`（RichText 原始片段，含四個檔案的下載連結）、`rel.xls`（2008–2012 停更舊版 Table 26，僅供歷史對照）、`RPPI.xlsx`（含 Table 2/3 貸款筆數 NCR 分項）、`monthlylendingratestype.xls`（IRLD 月頻放款利率，含 Housing Loans／Contracts to Sell）、`kbloanspbs.xls`（PSIC 2009 產業放款，含 RREL 排除註記）

**需求側**：`ph_ofw_remit.xls`（Personal＋Cash Remittances，1970/2005 起）、`ph_ofw_cash.xls`（按國別／來源拆分現金匯款）

**總經與利率**：`ph_bsprates.xls`（RRP 政策利率日頻）、`ph_pesodollar.xlsx`（披索兌美元月／日／年頻）、`sdir.xls`（Selected Domestic Interest Rates，銀行利率與 BSP 工具利率，不含公債殖利率）、`bsp_prices_api2.json`（Prices 清單完整項目，含 CPI／RPPI／RREPI 檔案連結）、`bsp_fsa_api.json`（Financial System Accounts 清單完整項目）

**制度與交易成本**：`ph_MORFXT.pdf` ＋ `ph_MORFXT.txt`（外匯交易法規手冊全文，93 頁）、`ph_const1987.html`（1987 年憲法全文）、`ph_ra4726.html`（公寓法全文）、`ph_ra7160.html`（地方政府法全文，含 §135/151/218/233/235）、`ph_ra10963.html`（TRAIN 稅改法全文，含 §69 修正 DST）、`ph_nirc.html`（國家內地稅法全文，含 §24(D) CGT）

（Investor's Lease Act RA 7652 與總統令 PD 471 全文本輪透過 WebFetch 摘要取得關鍵條文，未另存原始檔；下一輪如需逐字核對，可循 `lawphil.net/statutes/repacts/ra1993/ra_7652_1993.html` 與 `lawphil.net/statutes/presdecs/pd1974/pd_471_1974.html` 直接重新抓取。）

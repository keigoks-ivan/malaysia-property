# 巴西房價與租金序列可行性偵察

偵察日期：2026-08-02

---

## 裁決（放最前面）

| 問題 | 答案 |
|:---|:---|
| **FipeZap 租金指數口徑** | **掛牌（anúncios）**。且明確是「新掛牌招租」樣本，不含既有租約續約調整——結構上與馬來西亞 CPI 041（續約存量）相反，但仍是掛牌，不是成交 |
| **FipeZap 房價指數口徑** | **掛牌（anúncios）**。FIPE 官方方法論文件原文承認「掛牌價與實際成交價之間有明顯距離」，並直陳這是有意識的取捨，不是資料瑕疵 |
| **是否存在成交口徑替代來源（租金）** | **沒有找到**。IPCA 租金分項疑似與馬來西亞 CPI 041 同型（存量續約），但本輪未能取得 IBGE 官方方法論原文確認，暫記 🟡；POF 家庭預算調查有「實際已付租金」欄位，但頻率是六到九年一次的橫斷面調查，不成連續序列 |
| **是否存在成交口徑替代來源（房價）** | **部分存在，但非「成交」而是「估值」層級**：BCB 的 IVG-R、FGV/ABECIP 的 IGMI-R 都是**融資鑑價（laudo de avaliação／valor de garantia）**基礎，比掛牌更接近真實市場，但仍不是「買賣雙方實際成交價」。**唯一疑似真正成交口徑的來源是聖保羅市政府的 ITBI（不動產移轉稅）完稅申報資料**——這是行政紀錄，但本輪取數路徑實測受阻（見下） |
| **對四象限的意涵** | **NE 象限（租金）填不滿，巴西撞的是馬來西亞同一堵牆。** FipeZap 租金掛牌口徑，違反「掛牌永不當錨」鐵律；IPCA 租金分項若真是存量續約型，等於重演 CPI 041 的結構性落後問題。**NW 象限（房價）比馬來西亞略有優勢**——聖保羅 ITBI 若可解析，會是比 NAPIC 成交表更細顆粒的逐筆行政紀錄，IGMI-R／IVG-R 至少優於純掛牌——但 NW 在馬來西亞本來就已經是 ✅（MHPI），巴西在這裡不是解決新問題，只是錦上添花。**巴西不能兩個象限都填滿，選巴西的核心理由不成立。** |

---

## 逐項

### 一、FipeZap 房價與租金指數

| 項目 | 內容 |
|:---|:---|
| 全名 | Índice FipeZap de Preços de Imóveis Anunciados（房價）／Índice FipeZAP de Locação Residencial（租金）——**官方全名本身就寫著「Anunciados」＝已掛牌** |
| 發布機構 | Fipe（Fundação Instituto de Pesquisas Econômicas，聖保羅大學附屬經濟研究基金會）與 Grupo OLX（旗下 Zap、Viva Real、OLX 三個房產分類廣告平台）合作 |
| **口徑** | **掛牌價（anúncios）**。方法論文件原文（2014 修訂版）第 1 頁：「大概是因為掛牌價與實際成交價之間有明顯距離……但假設中長期兩者走勢相近，掛牌價指數仍可視為房地產市場的可信指標。這是 Fipe 目前的選擇。」（原文：*"A grande desvantagem dessa fonte é a óbvia distância entre o preço ofertado e o preço de fato transacionado. Mas, sob a hipótese de que pelo menos no médio e longo prazo a evolução dos dois preços tenha tendências semelhantes, um índice de preços ofertados poderia ser considerado como um indicador confiável do mercado imobiliário. Essa foi a escolha feita pela Fipe."*）——**FIPE 自己承認這是掛牌，而且明講取捨理由，不是我們的推論** |
| 樣本來源 | 每日爬取 Zap Imóveis 網站與其他 13 個分類廣告網站（現整合進 Grupo OLX：Zap／Viva Real／OLX）的公開掛牌，2007-12-01 起每日採集存檔。月底彙整成「月度粗資料庫」，同一物件（同價格＋同坪數＋同房間數＋同街區）跨平台去重 |
| 過濾規則 | 坪數 20–2,000 m²；售價 R$20,000–R$18,500,000；租金 R$100–R$90,000；房間數 1–8 間，超出範圍者剔除，約 15–40% 掛牌被判無效或重複 |
| 產品範圍 | **僅公寓（apartamentos），且僅二手已完工（usados／prontos）**——不含連棟／獨立屋（casas）、不含預售／新建案 |
| 房間分層 | 有，分 1／2／3／4 房以上四級（原方法論設計即如此，2025 年報告仍逐月公布各房型子指數） |
| 地理涵蓋 | 房價指數（Venda）2025-08 涵蓋 56 個城市／22 個州會；租金指數（Locação）涵蓋 36 個城市／22 個州會。最早期（2010）僅 7 個城市：聖保羅、里約、貝洛奧里藏特、聯邦區（巴西利亞）、薩爾瓦多、福塔雷薩、累西腓；2012 年擴充到 16 個城市（Índice Ampliado） |
| 加權方式 | IBGE 普查「加權區」（área de ponderação，社經同質性分區）× 房間數 分格；用該分格的家戶所得加總作權重；Laspeyres 公式；分格內用**中位數**（非均值，抗極端值）；再取近 3 月移動平均 |
| 頻率 | 每月發布，但採價是每日累積、月底結算 |
| 基期 | 原始 7 城組成指數（Índice Composto）以 2010 年 8 月 = 100；擴大指數（Ampliado）以 2012 年 6 月 = 100；各別新納入城市以其自己序列起點 = 100 |
| **關鍵區別（租金指數的一個結構優點）** | 2025-08 月報腳註明文：**「所採價格為新出租掛牌，FipeZAP 住宅租金指數的計算不納入現行租約的調整。因此該指數能更動態地捕捉住房供需的演變。」**——這代表 FipeZap 租金指數採的是「新掛牌招租」樣本，**不是**馬來西亞 CPI 041 那種「續約中租約存量」，結構上不會有 CPI 041 的「換約才落後反映」問題。**但它仍然是掛牌價，不是成交價**——換句話說，FipeZap 解決了 MY 租金指數「滯後」的病，但沒解決「掛牌≠成交」的病，而後者是本專案鐵律明文禁止的 |
| 收益率換算 | 官方同時發布 rental yield（租售比）＝月租金掛牌中位 / 售價掛牌中位 × 12，2025-08 全國平均 5.94% a.a.——**兩腳都是掛牌，比值本身不能當成交收益率使用** |
| 取數路徑 | ✅ **已驗證**。方法論 PDF（`https://downloads.fipe.org.br/indices/fipezap/metodologia/fipezap_revmetodologia_v20140218.pdf`，2014-02 修訂版；`FipeZAP_Metodologia_v20110216.pdf` 為 2011 原始版）與月報 PDF（`https://downloads.fipe.org.br/indices/fipezap/fipezap-{YYYYMM}-residencial-{venda\|locacao}.pdf`）皆可用瀏覽器 UA 直接下載，無需登入。`fipe.org.br` 官網本身（HTML 頁面）對本工具的 User-Agent 回 403，但檔案主機 `downloads.fipe.org.br` 不擋 |

**狀態：✅ 已驗證（口徑＝掛牌，證據為 FIPE 官方一手文件原文）**

---

### 二、BIS Residential Property Price Database — 巴西序列

| 項目 | 內容 |
|:---|:---|
| BIS「detailed」資料集巴西來源 | BIS 官方來源清單（`Residential and commercial property prices - data sources`，最後更新 2026-07-31）逐字列出：**"BR Brazil — Banco Central do Brasil / Getúlio Vargas Foundation / Fipezap"**——三個來源並列收錄，**不是單一序列** |
| 意涵 | BIS 巴西的「detailed」資料集本身是三種不同口徑的序列拼盤：央行 BCB（鑑價／擔保值口徑，見下 IVG-R）、FGV（鑑價口徑，見下 IGMI-R）、FipeZap（掛牌口徑）。**BIS 沒有幫巴西生出一條獨立驗證的「成交」序列**——它只是把巴西國內已有的三個既有序列都收進資料庫，各自的口徑限制原封不動地繼承進 BIS 資料 |
| 「selected」同質可比序列 | BIS 另有跨國可比的 selected 資料集（每國取一條「最接近全國涵蓋」的代表序列）。FRED 上巴西對應代碼為 `QBRR368BIS`（名目）與 `QBRR628BIS`（實質），起自 2001 年前後、季頻。**本輪未能確認 selected 序列具體選的是三個來源中的哪一個**（`fred.stlouisfed.org` 對本工具 UA 回 403，`bcb.gov.br` 為 JS 前端頁面，工具無法取得渲染後內容）——標記 🟡 |
| 取數路徑 | 方法論與來源清單 PDF ✅ 已驗證可下載：`https://www.bis.org/statistics/pp_sources.pdf`、`https://www.bis.org/statistics/pp_selected_documentation.pdf`（皆需瀏覽器 UA，`data.bis.org` 網頁本身為互動式 dashboard，工具無法解析內文）。序列數值本身（FRED 或 BIS Data Portal 的實際數字）本輪未取，因兩個下游站台都被工具層擋下 |

**狀態：🟡 待驗證（來源清單已確認，但 selected 序列的口徑歸屬與實際數值未取）**

**這條本身是一個有用的負面結果**：連 BIS 這種國際機構彙編的巴西資料，成分也是「掛牌＋兩種鑑價」，沒有一條被標記為「transaction」。如果連 BIS 都找不到巴西的成交口徑序列，這件事本身就是證據。

---

### 三、IGMI-R（Índice Geral do Mercado Imobiliário Residencial）—— FGV／ABECIP

| 項目 | 內容 |
|:---|:---|
| 發布機構 | Fundação Getúlio Vargas（FGV）與 ABECIP（巴西住宅貸款協會，Associação Brasileira das Entidades de Crédito Imobiliário e Poupança）合作 |
| **口徑** | **鑑價（laudo de avaliação），不是掛牌，也不是成交價本身**。樣本是「向 ABECIP 會員金融機構申請住宅貸款時，銀行委託估價師出具的鑑價報告」——鑑價目的是核定貸款成數（LTV），鑑價值通常錨定在買賣合約價附近，但**鑑價值與合約成交價在定義上是兩件事**，鑑價師的獨立判斷可能偏離合約價（尤其在合約價明顯偏離市場行情時，鑑價會被壓回市場水準）。這使 IGMI-R 落在「比掛牌更貼近市場、但不等於逐筆成交價」的中間地帶 |
| 樣本規模 | 約 150 萬筆鑑價報告，滾動取最近 3 年 |
| 方法 | Hedonic（特徵價格法），62 個變數與屬性（坪數、房間數、衛浴數、屋齡、裝修、地段、街區特徵、大樓設施等），**不是重複銷售法（repeat-sales）** |
| 地理涵蓋 | 全國 4,000+ 市鎮的加總指數；**城市層級細分僅 9 個州會**：聖保羅、里約、貝洛奧里藏特、福塔雷薩、累西腓、庫里奇巴、阿雷格里港、薩爾瓦多、戈亞尼亞 |
| 頻率／起始 | 月頻，2014-01 起 |
| 未來規劃 | ABECIP 官方頁面提及未來將擴充到「主要城市不同區域」與「不同物件類型」分層，本輪未取的是規劃項目，非既有序列 |
| 取數路徑 | 🟡 **待驗證**。頁面內容（`www.abecip.org.br/igmi-r-abecip/caracteristicas-do-indice`、`www.biabecip.org.br`）本輪透過搜尋引擎快取摘要間接取得文字描述，**未直接對官網做逐字核對，也未下載到實際指數數值序列**。下一輪若要用，須直接訪問 `biabecip.org.br`（ABECIP 專用 IGMI-R 入口站）確認是否有公開下載的時間序列或僅供訂閱查詢 |

**狀態：🟡 待驗證（口徑判斷有一定把握，但未經一手文件逐字核對，數值序列未取）**

---

### 四、IVG-R（Índice de Valores de Garantia de Imóveis Residenciais Financiados）—— Banco Central do Brasil

| 項目 | 內容 |
|:---|:---|
| 發布機構 | Banco Central do Brasil（BCB，巴西央行）官方指數 |
| **口徑** | **融資擔保鑑價（valor de garantia）**，資料源頭是 BCB 的 SCR（Sistema de Informações de Crédito，全國信貸登記系統）——**金融機構對所有信貸的強制申報義務資料**，理論上涵蓋面比 IGMI-R（僅 ABECIP 會員申報）更完整，因為 SCR 是監理強制申報而非自願參與。但性質仍是「擔保品鑑價值」，不是買賣雙方合約上的成交金額本身 |
| 地理涵蓋 | 據多筆二手資料交叉描述，BCB 已將 IVG-R 的區域劃分**對齊 IPCA 的採價地理分區**（即 IBGE CPI 使用的約 16 個都會區），代表有都會層級的分項，但本輪未能取得 BCB 官方一手文件逐一列出涵蓋城市清單 |
| 已知限制 | 二手資料提及該指數「對樣本結構變化敏感」——2015–2016 年因低價位融資操作占比上升、新成屋／中古屋融資比例變化，一度扭曲趨勢判讀，屬於已知的方法論脆弱點 |
| 衍生工具 | BCB 另有 MVG-R，把 IVG-R 的指數值換算回雷亞爾水準金額（而非僅指數），可用於計算房價所得比等衍生指標 |
| 取數路徑 | 🔴 **本輪未能實測**。`bcb.gov.br` 的統計頁面是 JavaScript 前端渲染的單頁應用（SPA），本工具的 WebFetch 只能取得初始 HTML 骨架（僅顯示「Banco Central do Brasil」標題），無法取得渲染後內容；`dadosabertos.bcb.gov.br` 開放資料 API 端點本輪未嘗試呼叫（下一輪應直接測試 SGS API，例如 `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados`，需先查出 IVG-R 對應的 SGS 序列代碼） |

**狀態：🟡 待驗證（口徑判斷來自多筆一致的二手資料交叉印證，但未觸及 BCB 一手方法論文件；數值序列與確切城市清單本輪未取）**

---

### 五、聖保羅市 ITBI（Imposto de Transmissão de Bens Imóveis）完稅申報資料

| 項目 | 內容 |
|:---|:---|
| 性質 | **不動產移轉稅完稅申報的行政紀錄**——每一筆繳納 ITBI 的不動產交易都會產生一筆申報資料，理論上是「逐筆成交／移轉」層級的行政資料，性質上最接近本專案要求的「成交口徑」 |
| 發布機構 | Prefeitura de São Paulo（聖保羅市政府）財政局（Secretaria Municipal da Fazenda），開放資料頁：`prefeitura.sp.gov.br/web/fazenda/w/acesso_a_informacao/31501`，標題為「Dados das Transações Imobiliárias com recolhimento de ITBI」 |
| 涵蓋期間 | 2006 年至 2026 年（當年資料每月更新至上月），逐年一個檔案 |
| 格式 | Excel（.xlsx）與 ODS（OpenDocument）雙格式，逐年下載，**無 API、無 CSV** |
| 已知口徑警訊（重要，須標明） | ITBI 申報值是納稅義務人自行申報的交易金額，巴西多數市政府（含聖保羅）採「申報值與市府核定參考值（valor venal de referência）取兩者較高者」作課稅基礎，因此申報欄位**未必等於買賣雙方合約上的實際成交價**——存在低報誘因（節稅）與市府參考值下限的雙重扭曲。這比馬來西亞 NAPIC 的成交表（依印花稅申報、但馬來西亞印花稅稽核機制不同）需要單獨評估失真幅度，**不能未經檢驗就當「乾淨成交價」使用** |
| 取數路徑 | 🟡 **部分驗證**：透過官方頁面確認資料集存在、格式與涵蓋期間（下載連結範例：`https://drive.prefeitura.sp.gov.br/cidade/secretarias/upload/fazenda/arquivos/itbi/GUIAS%20DE%20ITBI%20PAGAS%20(28012026)%20XLS.xlsx`，HTTP 302 導向確認檔案存在）。**實際下載本輪受阻**：`drive.prefeitura.sp.gov.br` 在本沙箱環境下連線逾時（45 秒無回應，非 403，疑似該主機對外流量限制或網路路由問題，非本工具的 UA 阻擋），因此**欄位結構（地址、街區、坪數、物件類型、申報金額、完稅日期是否齊全）本輪完全未驗證**，需要下一輪在無網路限制的環境重試 |

**狀態：🟡 待驗證（資料集存在性與下載連結已確認，欄位內容與資料品質未驗證）——本輪唯一疑似「真成交口徑」的候選來源，優先順序最高**

---

### 六、IBGE — 官方統計局

| 候選 | 結論 |
|:---|:---|
| SINAPI（Sistema Nacional de Pesquisa de Custos e Índices da Construção Civil） | **不是房價指數**，是營造成本指數（水泥、鋼筋、人工等投入成本），對應四象限 SW 象限的 K（重置成本）候選，不對應 NE／NW。可作為巴西版「營造成本指數」候選來源，但本輪未深入取數 |
| 住宅價格指數 | **IBGE 本身未發布官方住宅價格指數**。與馬來西亞 NAPIC 的角色不同——馬來西亞的官方統計機構（NAPIC）發布 MHPI；巴西的「官方」房價指數其實來自央行（IVG-R）與半官方協會（IGMI-R），不是統計局 |
| POF（Pesquisa de Orçamentos Familiares，家庭預算調查） | 有「aluguel efetivo」（實付租金）欄位，作為家戶消費支出的一部分收集。**但頻率是六到九年一次的橫斷面調查**（2002–03、2008–09、2017–18、2024–25），**不是連續序列**，性質與馬來西亞 2020 年普查單點空置率資料同一類——只能當單點錨，不能當時間序列使用 |
| IPCA 租金分項 | IBGE CPI（IPCA）內含住宅租金子項，**懷疑與馬來西亞 CPI 041 同型**（統計局採價通常針對「目前正在執行的租約」而非「新簽約案例」，若屬實則會有同樣的換約滯後問題）。**本輪未能取得 IBGE 官方方法論原文逐字確認這一點**，只是基於「多數國家 CPI 房租分項的通例都是存量續約型」的先驗推斷——**不應被當成已驗證結論引用，須標記為推斷、下一輪需要一手驗證** |

**狀態：🔴 無直接房價來源缺口（IBGE 不發布房價指數）｜🟡 IPCA 租金分項口徑存疑，未驗證｜POF 為單點調查，已知限制與 MY 普查同類**

---

## 取數路徑實測

| URL / 端點 | 結果 | 備註 |
|:---|:---|:---|
| `www.fipezap.com.br` | 301 → `fipezap.zapimoveis.com.br` | 品牌網域已轉移 |
| `fipezap.zapimoveis.com.br` | 301 → `www.datazap.com.br/conteudos-fipezap/` | 二次轉移 |
| `www.datazap.com.br/conteudos-fipezap/` | 301 → `imoveis.grupoolx.com.br/datazap/fipezap/` | FipeZap 品牌已併入 Grupo OLX 的 DataZap 產品線；此頁為 JS 前端，WebFetch 只讀到落地頁殼，無方法論內容 |
| `www.fipe.org.br/pt-br/indices/fipezap/` | **403 Forbidden**（對本工具 UA） | FIPE 官網本體擋爬蟲；但檔案主機 `downloads.fipe.org.br` 不擋 |
| `downloads.fipe.org.br/indices/fipezap/metodologia/fipezap_revmetodologia_v20140218.pdf` | ✅ 200，896KB | 用瀏覽器 UA 透過 curl 直接下載成功；WebFetch 工具本身對此網域也回 403，須改用 Bash curl 加瀏覽器 UA |
| `downloads.fipe.org.br/indices/fipezap/metodologia/FipeZAP_Metodologia_v20110216.pdf` | ✅ 200，710KB | 2011 原始版方法論 |
| `downloads.fipe.org.br/indices/fipezap/fipezap-202508-residencial-locacao.pdf` | ✅ 200，1.76MB | 2025-08 租金月報 |
| `downloads.fipe.org.br/indices/fipezap/fipezap-202508-residencial-venda.pdf` | ✅ 200，2.50MB | 2025-08 房價月報 |
| `www.bis.org/statistics/pp_sources.pdf` | ✅ 200 | 用瀏覽器 UA 透過 curl 下載成功 |
| `www.bis.org/statistics/pp_selected_documentation.pdf` | ✅ 200 | 同上 |
| `data.bis.org/topics/RPP` | 可讀但無實質內容 | 互動式 dashboard，WebFetch 抓不到渲染後資料 |
| `fred.stlouisfed.org/series/QBRR368BIS` | **403 Forbidden** | 對 WebFetch UA 阻擋 |
| `www.bcb.gov.br/estatisticas/mercadoimobiliario` | 可連線但無內容 | JS SPA，僅取得標題殼，下一輪應改試 `api.bcb.gov.br` SGS 開放資料 API |
| `prefeitura.sp.gov.br/web/fazenda/w/acesso_a_informacao/31501` | 可讀，確認資料集存在 | 聖保羅 ITBI 開放資料頁 |
| `drive.prefeitura.sp.gov.br/.../GUIAS DE ITBI PAGAS (28012026) XLS.xlsx` | **連線逾時**（curl 45 秒無回應，非 403） | 302 導向本身有回應（確認檔案存在），但實際下載主機逾時，本沙箱環境的網路限制所致，非資料不存在 |
| `www.abecip.org.br/igmi-r-abecip/caracteristicas-do-indice` | 僅透過搜尋引擎摘要間接取得 | 未直接 WebFetch 逐字核對 |
| DuckDuckGo HTML 版（`html.duckduckgo.com/html/?q=...`） | 大部分查詢可用，少數觸發 CAPTCHA | 本輪主要替代搜尋管道，因 WebSearch 工具配額於任務開始前已用罄（`200/200`，屬本 session 共用配額，非本次任務耗用） |
| Bing、一般 duckduckgo.com（非 html 版） | 不可靠，曾回傳與查詢完全無關的結果 | 已放棄，改用 html.duckduckgo.com |

---

## 已知限制

1. **本輪最大的方法論限制：WebSearch 工具配額於任務開始前已耗盡**（`this session has used its web search budget 200 of 200`），改用 `html.duckduckgo.com` 與直接 `curl`／WebFetch 訪問已知或推測 URL 補位。這代表搜尋廣度不如正常配額下完整，部分候選來源（例如是否還有其他州會城市自己的 ITBI 開放資料、是否有學術論文直接比較 IGMI-R／IVG-R／FipeZap 三者的口徑差異）未窮盡搜索。

2. **BCB（巴西央行）官網為 JavaScript 單頁應用**，本工具的 WebFetch 無法取得渲染後內容，導致 IVG-R 的口徑判斷全部依賴二手資料交叉印證，**未觸及一手方法論文件**。下一輪應改用 BCB 的 SGS 開放資料 API（`api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados`）或直接下載其技術附注 PDF（若存在固定 URL）。

3. **聖保羅 ITBI 資料集的實際下載與欄位驗證完全未完成**。這是本輪唯一有機會提供「真成交口徑」的來源，但受限於本沙箱環境對 `drive.prefeitura.sp.gov.br` 的連線逾時，欄位內容、資料完整度、申報值與市場行情的落差幅度全部未知。**在有人於正常網路環境完成這一步之前，不能把 ITBI 列為「已驗證」的成交口徑來源**，只能維持 🟡。

4. **即使 ITBI 驗證成功，它也只解決 NW（房價）不解決 NE（租金）**。租賃合約不繳 ITBI（ITBI 是不動產移轉稅，只對買賣／贈與課徵），因此不存在租金版的 ITBI。巴西目前找不到任何城市層級、成交（而非掛牌／鑑價／續約存量）口徑的租金序列候選——這是本輪最關鍵的負面結果。

5. **IGMI-R 與 IVG-R 的「鑑價」口徑本身也需要更細緻的定性**，本輪只做到二手資料層級的確認，未取得能說明「鑑價值與合約成交價之間平均落差有多大」的官方文件（例如兩者的相關係數、迴歸估計）。若後續要用這兩條序列，這個問題必須先解決，否則等於把馬來西亞「掛牌 vs 成交」的老問題換了一個新面孔（「鑑價 vs 成交」）重演一次。

6. **IPCA 租金分項是否真的是「存量續約型」，本輪僅為推斷，未經 IBGE 一手方法論文件驗證。** 這點如果查證後發現不成立（例如 IBGE 其實採的是新簽約樣本），會改變 NE 象限「巴西也一樣填不滿」的判斷力度——但即使如此，IPCA 租金分項也只是一個變動率指數，不是水準值，且沒有城市／房型分層，用途上限仍然很低。

7. **未觸及的候選來源**（因時間與搜尋配額限制，本輪列為下一輪待辦，非已排除）：里約熱內盧市或其他州會是否有自己的 ITBI／不動產登記開放資料；Registro de Imóveis（不動產登記處）的全國性統計彙整（巴西登記處為去中心化的私人公證處體系，理論上比聖保羅單一市府更難彙整，但值得一查）；學術文獻中是否已有人直接比較 FipeZap／IGMI-R／IVG-R 三者對同一城市同期的價格落差幅度（若存在，可以直接引用其估計值作為口徑轉換的敏感度依據，不必自己重新估計）。

# S_shadow 可量測性偵察（馬來西亞）

**建立日**：2026-08-02 ｜ **狀態**：偵察結案 ｜ **產出檔**：`data/my-shadow-proxy.json`
**服務對象**：`four-quadrant-v1.md` §3（亞洲修改）、§5 SE 象限 🔴 缺口、§7 已知邊界

**問題**：`S_shadow` ＝ 已售、已交屋、但無人居住也未出租的單位。NAPIC 的 `S_overhang`（完工未售）抓不到這一層。MY 有沒有可量測的代理？

**一句話結論**：**沒有。** 五條候選路線四條完全不可用、一條（人口普查）只給得出 2020 年的單點水準錨，且該錨的分母與 NAPIC 存量不相容。§3 的亞洲修改在 MY 只能停留在定性機制。

**紀律**：寧缺勿假。查無可用代理是完全可接受的結論；不用估計值或國際平均填格子。學術估計只當參考點，不進 data JSON。二手媒體數字一律追到原始出處，追不到不採用。

**本檔的性質**：可行性偵察報告，不是取數紀錄。每條路線記「查到什麼／實測的 URL 與 HTTP 狀態／為什麼可用或不可用」，失敗路線寫得比成功路線詳細——目的是讓下一個人不必重做一次。

---

## 候選代理 1：公用事業零用量戶數（TNB／ST／SPAN／Air Selangor）— **不可用**

### 電力側：ST 只公佈「帳戶數」，不公佈「用量分布」

實測取得並解析：《Maklumat Prestasi dan Statistik Industri Pembekalan Elektrik di Malaysia 2014 ／ Performance and Statistical Information on Electricity Supply Industry in Malaysia 2014》，Suruhanjaya Tenaga。

取數路徑（實測 HTTP 200，6.11 MB）：
`https://www.st.gov.my/sites/default/files/2026-02/Performance-and-Statistical-Information-2014.pdf`

該報告確有 Jadual 6（TNB 用戶數 2010–2014）、Jadual 20（SESB）、Jadual 33（SEB），但**欄位只有「按關稅類別的用戶總數」**：

| 年 | Domestik | Komersil | Industri | 總計 |
|:---|---:|---:|---:|---:|
| 2010 | 6,128,224 | 1,224,414 | 25,580 | 7,431,655 |
| 2014 | 6,710,032 | 1,404,501 | 24,852 | 8,204,328 |

**沒有用量分級（consumption band）欄位，沒有零用量戶數，沒有州別的住宅帳戶分解。** 全報告掃過一次，`consumption band`／`kWh block`／零用量相關欄位皆不存在。

### TNB 年報：同樣只有總戶數

《TNB Integrated Annual Report 2024》（`https://www.tnb.com.my/assets/annual_report/TNB_IAR_2024.pdf`，19.1 MB，實測可下載解析）給的是 10.41 million customers（半島全部）、domestic 約 9.1 million。**無任何用量分布或零用量統計。**

值得記下的一件事：TNB 目標 2029 年前在半島裝設 910 萬具智慧電表——這代表**資料在 TNB 內部存在且顆粒度足夠**，只是不公佈。這是「不公開」的缺口，不是「不存在」的缺口；未來若 ST 開放或有研究單位取得授權，這條路會活過來。

### 水務側：SPAN 網站在本次偵察期間無法連線

`https://www.span.gov.my/` 與其文件路徑 `https://www.span.gov.my/document/upload/...pdf` 在本次偵察中連續逾時（`curl: (28) Failed to connect ... port 443`，75 秒與 60 秒兩次）。**取數失敗的原因是連線層，不是內容層**——不能據此斷定 SPAN 沒有資料。但即使 SPAN 的 Water Services Industry Performance Report 有「domestic connections」欄位，依電力側的先例判斷，**幾乎確定也只有帳戶數而無用量分布**（KPI 報告的體例是營運績效指標：NRW、供水覆蓋率、水壓合格率，不是用戶用量直方圖）。

Air Selangor 的公開刊物（Hydro Hub）為客服／永續敘事型，未見用量分布統計。

### 衍生想法的證偽：「NAPIC 存量 − 公用事業帳戶數」的缺口能不能當代理？

既然拿不到用量分布，退一步問：帳戶數本身能不能用？邏輯是「已完工但從未開戶＝從未有人入住」。

**實測結果：這個想法當場死亡。** 2014 年半島 TNB 住宅帳戶 6,710,032 戶，對照 `data/napic-stock.json` 同期半島 13 州住宅 existing stock 合計 4,441,210 戶——**帳戶數比存量多出 51%**。

原因是兩個母體根本不同：TNB 住宅關稅涵蓋甘榜住屋、園丘與機構宿舍、店屋樓上住居等大量 NAPIC 住宅存量不涵蓋的處所。缺口是負的、而且巨大，方向與想量的東西相反。**這條路不需要再驗證，直接否決。**

### 裁決（代理 1）

**不可用。** 效度上它是國際最佳代理（日、澳、法都用過），但 MY 的公開資料只到「帳戶數」這一層，缺的正是唯一有用的那一維（每戶用量分布）。衍生的帳戶數缺口法已被實測數字否決。

---

## 候選代理 2：人口普查空屋率（DOSM Banci 2020）— **部分可用（單點水準錨）**

### 存在性：✅ 官方、原始表格已取得

DOSM《Penemuan Utama Banci Penduduk dan Perumahan Malaysia 2020》系列有**兩個層級的分冊**，每冊都含一張「Jadual 10／Table 10：Data awalan tempat kediaman kosong mengikut sebab utama kekosongan（空置住所按主要空置原因的初步資料）」。

實測取數路徑（`curl` 直取，HTTP 200）：

| 分冊 | URL | 大小 |
|:---|:---|:---|
| 州層（W.P. Kuala Lumpur 卷） | `https://www.dosm.gov.my/uploads/publications/20221018092119.pdf` | 3.64 MB |
| 縣層（Kuantan, Pahang 卷） | `https://www.dosm.gov.my/uploads/publications/20221018135849.pdf` | 3.56 MB |

**取數坑**：`WebFetch` 對 `dosm.gov.my` 一律回 `unable to verify the first certificate`（憑證鏈不完整）。必須用 `curl -sSL` 下載後 `pdftotext -layout` 解析。這是 DOSM 全站的問題，不只這兩個檔。

### 已鎖定的數字（全部逐字出自上述 PDF，非二手）

**Malaysia 全國，Jadual 1（1970–2020 六個普查年）**：

| | 1970 | 1980 | 1991 | 2000 | 2010 | 2020 |
|:---|---:|---:|---:|---:|---:|---:|
| 住所總數 | 1,671,108 | 2,632,561 | 4,092,769 | 5,569,261 | 7,346,910 | 9,614,139 |
| 已居住 | 1,488,227 | 2,332,563 | 3,422,189 | 4,679,757 | 6,232,613 | 7,751,312 |
| **空置** | 156,411 | 227,072 | 638,753 | 867,311 | 1,102,558 | **1,862,827** |
| 空置率 | 9.5% | 8.9% | 15.7% | 15.6% | 15.0% | **19.4%** |

**W.P. Kuala Lumpur，Jadual 2**：

| | 1980 | 1991 | 2000 | 2010 | 2020 |
|:---|---:|---:|---:|---:|---:|
| 住所總數 | 169,776 | 264,585 | 354,731 | 468,325 | 634,639 |
| **空置** | 11,533 | 33,351 | 56,191 | 59,967 | **92,429** |
| 空置率 | 6.9% | 12.7% | 15.9% | 12.8% | **14.6%** |

**KL 空置原因分解（Jadual 10，2020）**——這是本次偵察最關鍵的一張表：

| 原因 | 戶數 | % |
|:---|---:|---:|
| Baru siap／untuk disewa atau dijual（新完工／待租或待售） | 43,204 | 46.8 |
| Rumah peranginan／persinggahan（度假屋／過境屋） | 18,036 | 19.6 |
| Untuk dibaiki／ubahsuai（待修繕／裝修） | 5,174 | 5.6 |
| Homestay | 1,571 | 1.7 |
| Rumah pekerja bermusim（季節工宿舍） | 842 | 0.9 |
| Hampir roboh（近乎倒塌） | 199 | 0.2 |
| **六項小計** | **69,026** | **74.7** |
| **未分類殘差**（92,429 − 69,026） | **23,403** | **25.3** |

表下原註：`Sebab TK Kosong: Data adalah berdasarkan pemerhatian di lapangan.`（空置原因係基於**實地觀察**）——這是效度評估的關鍵，見下。

**印刷四捨五入註**：由戶數重算，`Rumah peranginan／persinggahan` 為 18,036／92,429 ＝ 19.5%，表上印 19.6%，差 0.1pp；其餘五欄重算與印刷值一致。屬來源端捨入雜訊，**以戶數為準**。

（全國層的原因分解百分比見下方「補記」，已追到 DOSM 原始出處。）

### 這張表對 S_shadow 的意義

四象限的存量拆解要的是 `S_total − S_overhang − S_shadow = S_effective`。Jadual 10 的六個欄位可以對應過去：

- **`Baru siap／untuk disewa atau dijual` 混了兩層**：「待售」的部分＝ NAPIC 口徑的 `S_overhang`（開發商持有未售），「待租」的部分＝ 已售但尚未找到租客——**後者不是 S_shadow**（業主有意進入使用市場，只是摩擦性空置）。這一欄不能整欄當 shadow。
- **`Rumah peranginan／persinggahan` 才是 S_shadow 的核心**：已售、有主、不作常住、也不放租。KL 的 18,036 戶（占 KL 存量 2.84%）是本次偵察找到的**唯一一個有官方原始表支撐的 S_shadow 下界**。
- **`Homestay` 1,571 戶屬短租**——它進入了使用市場（只是短租而非長租），依 §3 定義應算在 `S_effective` 內或另立第三態，不算 shadow。
- **`Untuk dibaiki`／`Hampir roboh` 屬 δ（汰換）那一格**，不是 shadow。
- **25.3% 未分類殘差是最大的不確定源**。DOSM 未公佈這 23,403 戶的分類，而其中相當比例（依常識推斷）正是「買了空著、實地觀察看不出原因」的投資持有——但**這是推斷，不是資料，不得寫進 JSON**。

### 效度問題（照登）

1. **實地觀察法，不是行政紀錄**。普查員在門外判定「這戶空著、原因是度假屋」。度假屋 vs 純投資空置在門外幾乎無法區分，分類誤差方向未知。
2. **「住所（living quarters）」不等於 NAPIC 的「住宅存量」**。DOSM 定義是「結構上獨立、有獨立出入口」的居住單元，包含非正規住居、店屋樓上、宿舍；NAPIC Stock Table 的存量是「已發 CCC 的住宅單位」。**兩者不可相除**——用普查空置戶數除 NAPIC 存量會得到假的比率。KL 2020 普查住所 634,639 vs NAPIC 同期住宅存量（見 `napic-stock.json`）是兩個不同的母體。
3. **單一年度**。2020 是最近一次普查，下一次 2030。Jadual 10 的原因分解**只有 2020 有**（1970–2010 只有空置總數，無原因欄位）。所以它只能當**水準錨點**，不能當序列。
4. **普查日效應**。2020 普查日在 COVID 行動管制期間附近，人口流動異常（外勞返鄉、學生離校），空置判定可能系統性偏高。19.4% 相對 2010 的 15.0% 跳升 4.4pp，有多少是真實存量變化、多少是普查日效應，DOSM 未做分解。

### 裁決（代理 2）

**部分可用——僅作為 2020 年的水準錨點，且只有 `Rumah peranginan／persinggahan` 一欄能當 S_shadow 的下界代理。** 不得外推成序列進 §4 檢定。

### 補記：全國層原始表已追到

DOSM 新聞稿《Penemuan Utama Banci Penduduk dan Perumahan Malaysia 2020 — Daerah Pentadbiran》（禁載至 2022-05-29 11:00）內文給出全國層的原因分解，與 KL 卷欄位定義一致：

> 「Data awalan menunjukkan sebab utama kekosongan TK di peringkat Malaysia adalah berikutan ia baru siap／untuk disewa atau dijual (37.8%) dan kerana ia dijadikan rumah peranginan／persinggahan (23.3%). Lain-lain sebab kekosongan TK adalah untuk dibaiki／ubahsuai (5.4%), homestay (2.3%), rumah pekerja bermusim (2.2%) dan hampir roboh (2.0%).」

取數路徑：`https://www.dosm.gov.my/uploads/content-downloads/file_20221105172037.pdf`（實測 HTTP 200）。**先前搜尋結果中的 37.8%／23.3% 至此由二手升格為原始出處已驗證。**

同一份文件另給縣層極值，對判讀「度假屋」欄位很重要：
- 「新完工／待租售」占比最高的縣全在 Selangor：Sepang 71.3%、Gombak 62.9%、Petaling 62.9%
- 「度假屋／過境屋」占比最高的縣全在 Sarawak：Kanowit 87.0%、Pakan 76.4%、Tatau 69.3%
- 空置率最高的縣：Telang Usan, Sarawak 41.2%；Tanjung Manis, Sarawak 40.7%；Cameron Highlands, Pahang 40.2%

**這組極值揭露了一個效度陷阱**：Sarawak 內陸縣的「rumah peranginan／persinggahan」高占比顯然不是投資客的城市第二套房，而是**長屋／原鄉住屋**——屋主在城市工作、老家空著。同一個欄位在 KL 與在 Kanowit 指的是完全不同的東西。**因此這一欄只能在都會區使用，不能在全國層拿來當 S_shadow**。

---

## 候選代理 3：CCC 發出數 vs 評估稅活躍戶籍 — **不可用**

### 概念本身就有缺陷

先講結論再講查證：這條路即使拿到資料也**測不到想測的東西**。馬來西亞的評估稅（cukai taksiran／cukai pintu）是**按估值課徵，與是否有人居住無關**。房子空著照樣要繳。所以「CCC 發出數 vs 評估稅戶籍數」的落差反映的是稅籍建檔進度，不是入伙率。

DBKL 自己的 FAQ 把這點寫得很清楚（`https://www.dbkl.gov.my/en/departments/jabatan-penilaian-dan-pengurusan-harta`）：

> 「14. Bolehkah saya dikecualikan dari membayar cukai taksiran sekiranya harta saya kosong／tidak diduduki?
> Tidak boleh dikecualikan, namun tuan／puan boleh memohon untuk mendapatkan **elaun kekosongan**…」

### 但這裡有個 MY 特有的機制值得記一筆：elaun kekosongan（空置寬減）

《Akta Kerajaan Tempatan 1976》第 162 條規定：建築物若**空置且無租金收入**達一個曆月以上，業主可向地方政府申請按空置期間比例退還／寬減評估稅。這在制度上是一筆**業主自己申報的空置紀錄**——理論上是全 MY 唯一的行政空置登記。

**但它作為 S_shadow 代理有結構性的反向選擇問題**：申請條件要求業主證明**已作合理努力出租而未果**。也就是說，這個機制只捕捉「想出租但租不掉」的摩擦性空置，而 S_shadow 的定義是「**不打算出租**的持有空置」——後者根本沒有資格申請，也沒有動機申請。**它篩出來的正好是 S_shadow 的補集。**

### 查證：無論如何也沒有公開數據

- **DBKL Data Terbuka**（`https://www.dbkl.gov.my/data-statistik/data-terbuka`）實測列出 12 筆資料集，全部與房產稅籍無關：綠地清單、預算摘要、滯洪池、廁所評等、罰單統計、市場攤販清單、抽水站、路燈數、PPR 公共組屋住戶族群、PPR 入住率（按國會選區，2023）、活躍攤販。**沒有評估稅戶籍統計，沒有空置寬減統計。**
- 唯一與「入住」沾邊的是第 11 筆 PPR 公共組屋入住率——那是**補貼型公共租賃住宅**，與投資持有存量在母體上完全不重疊，對 S_shadow 零資訊量。
- DBKL 評估稅活躍戶約 784,151 戶的數字流通於媒體報導（2026 年度預算脈絡），**本次偵察未追到 DBKL 官方原始出處，依紀律不採用**。
- CCC 發出數：KPKT／CIDB 皆未見公佈全國或按地方政府的年度 CCC 發出單位數統計。真正的完工序列在 NAPIC Stock Table 的 `completions` 欄位（已取得，見 `napic-stock.json`），CCC 這條路無新增資訊。

### 裁決（代理 3）

**不可用，且概念本身應放棄。** 評估稅對占用狀態失明；第 162 條寬減機制的選擇方向與 S_shadow 相反；DBKL 開放資料無相關項目。

---

## 候選代理 4：租賃登記／租金所得申報（LHDN） — **不可用**

### MY 沒有租賃登記制度

馬來西亞**沒有強制的住宅租賃登記制度**（不像德、法或部分中國城市）。租約是私人契約，不須向任何機關登記，因此不存在「登記出租戶數」這個統計母體。這一條的前提在 MY 直接不成立。

### LHDN 側：發布的是徵管統計，不是所得結構統計

LHDN 確實出版《Laporan Tahunan》（2001 年起）與線上服務統計（`https://www.hasil.gov.my/mengenai-hasil/profil-korporat/laporan-tahunan/`、`https://www.hasil.gov.my/pautan-pantas/perkhidmatan/statistik/`）。但這兩個系列的內容是**徵管績效**：總徵收額（2023 RM183.3 bil、2024 RM203.991 bil）、活躍納稅人數（逾 800 萬）、e-Filing 使用量、稽查成效。

**未見任何按所得來源（B2 法定租金所得）分解的申報戶數或金額統計。** 本次偵察對 `hasil.gov.my` 的兩個入口皆嘗試取數；年報索引頁可達，但沒有所得來源分解的統計表。

即使拿得到，效度也有兩個致命問題：

1. **申報遵從率未知且必然低**。個人房東的租金所得漏報在 MY 是公開的秘密，LHDN 自 2025 年起推 e-Invoice 才開始收緊。用申報戶數估出租戶數會**系統性低估出租**，因而**系統性高估空置**——偏誤方向恰好會把 S_shadow 灌水。
2. **單位不對**。申報的是「有租金所得的納稅人」，一人可持多戶；沒有戶數對應。

### 替代路線：DOSM 住戶自置／租賃比例——查到了，但解不了

DOSM 的 Basic Amenities Survey 2024 有住戶居所權屬比例：自有 78.0%（2022 為 76.5%）、租賃 19.7%、宿舍 2.4%。這是**住戶端**的比例，分母是住戶，不是存量——它告訴你有多少家庭在租房，不告訴你有多少單位空著。要接上存量必須知道每戶對應幾個單位，而那正是普查才測得到的東西。

### 裁決（代理 4）

**不可用。** 制度前提（租賃登記）在 MY 不存在；LHDN 不發布所得來源分解；即使有，遵從率偏誤的方向會系統性高估 S_shadow。

---

## 候選代理 5：偵察中發現的其他路線

### 5a. OpenDOSM 逐年「住所數 vs 住戶數」序列 — **已實測證偽，不可用**

這是本次偵察中最接近成功的一條，值得完整記載失敗過程，以免下一個人重試。

OpenDOSM 有資料集 `hh_lq_state`（Number of Households and Living Quarters by State），**年頻、1970–2024、16 個州**，欄位正是 `households` 與 `living_quarters`，且說明白紙黑字寫 living quarters「also includes empty dwellings」。

實測取數（HTTP 200，10,257 bytes）：`https://storage.dosm.gov.my/demography/hh_lq_state.csv`

如果這個序列是獨立觀察，`1 − households／living_quarters` 就能給出**年頻的州別空置代理序列**——那會把普查的單點錨升級成可進 §4 的序列。

**實測結果：證偽。** 計算 KL／Selangor／Johor 的該比率：

| 年 | KL | Selangor | Johor |
|:---|---:|---:|---:|
| 2015 | 1.6% | 10.4% | 10.9% |
| 2016 | 0.7% | 9.8% | 10.6% |
| 2017 | **−0.2%** | 9.3% | 10.3% |
| 2018 | **−1.0%** | 8.9% | 10.0% |
| 2019 | **−1.7%** | 8.5% | 9.7% |
| **2020（普查基準年）** | **9.6%** | **12.6%** | **18.3%** |
| 2021 | 9.5% | 12.5% | 18.6% |
| 2022 | 9.5% | 12.3% | 18.9% |
| 2023 | 9.4% | 12.2% | 19.2% |
| 2024 | 9.3% | 12.1% | 19.5% |

兩個致命點：

1. **2017–2019 的 KL 值為負**——住戶數超過住所數，物理上不可能是空置率。這證明普查間年份的 `living_quarters` 是**人口推計外推出來的模型值**，不是觀察值，而且外推得不好。
2. **2019→2020 有巨大水準斷點**：KL 從 −1.7% 跳到 +9.6%（11.3pp），Johor 從 9.7% 跳到 18.3%（8.6pp）。斷點的位置恰好是普查年，說明非普查年的數字完全由外推決定；2020 以後的數列則是從普查基準單調機械延伸（KL 逐年 −0.1pp、Johor 逐年 +0.3pp），**沒有任何新增資訊**。

附帶還有一個口徑問題：`1 − HH/LQ` 本來就不等於空置率，因為一個住所可住多個住戶（2020 全國 8,234,644 戶 vs 7,751,312 個已居住住所，住戶比已居住住所多 6.2%）。

**結論：這個序列不能用來做任何跨年空置推論。普查年的值是普查值（已在代理 2 記載），非普查年的值是外推假象。**

### 5b. KRI《Curbing Overhang and Vacancy》（2023）— **最重要的旁證**

Khazanah Research Institute，Theebalakshmi Kunasekaran，2023-09-11。
取數路徑（實測 HTTP 200，493 KB）：`https://cdn.prod.website-files.com/684b55df28cddcbe52b406f2/68b7ee897c4a12ee1e797fc5_68a678f1f965e9ba4cce738e_KRI-20Views_Curbing-20Overhang-20and-20Vacancy_The-20Case-20for-20a-20Vacancy-20Tax-20in-20Malaysia.pdf`

這是馬來西亞討論空屋稅的代表性政策文件，出自準官方智庫。**它對本次偵察的價值不在它給的數字，而在它用了什麼資料。**

- 它衡量 vacancy **只用 2020 普查一個來源**。沒有用電力、水務、稅籍或任何其他代理。
- 它給出全國原因分解的絕對戶數：新完工／待租售 704,935、度假屋／過境 433,953、待修繕 100,978、homestay 42,767、季節工宿舍 40,594、近乎倒塌 37,729，並自註「the given data breakdown for vacancy reasons only totals to 1.3 million」（即 1,360,956 戶，相對 1,862,827 的殘差 501,871 戶＝26.9% 未分類）。
- 最關鍵的是它自己承認的限制，原文照錄：

> 「it is important to acknowledge that the data lacks a detailed breakdown between newly completed units and those intended for rental, making it difficult to ascertain whether the units are primarily for long term rental or purchased for speculative purposes.」

**一個推動空屋稅立法的智庫，在為政策辯護時仍然只能用普查、而且明講資料無法分辨投機持有——這是「MY 沒有更好的 S_shadow 代理」最強的旁證。** 如果存在可用的行政資料，這份文件不會不用。

（KRI 的絕對戶數與 DOSM 原始百分比相容：704,935／1,862,827 ＝ 37.84%，433,953／1,862,827 ＝ 23.30%，對得上 DOSM 的 37.8%／23.3%。但這些**絕對數本身出自 KRI 的呈現，不是 DOSM 新聞稿正文**，在資料檔中須標為衍生層。）

### 5c. KRI TEDUH 資料集 — **有價值，但打的是 overhang 不是 shadow**

`https://www.krinstitute.org/publications/teduh-housing-project-data`

KRI 從 KPKT 的 TEDUH 入口網爬取的授權房屋發展專案資料庫，parquet 格式，**每週快照，全國、州與縣層，含單位層級（unit-level）的銷售狀態**（avail／sold／booked／reserved），另有 SPA 與交屋時程、工程進度分項。

這是很好的資料——但它記的是**銷售狀態，不是占用狀態**。它能把 `S_overhang` 從 NAPIC 的季頻聚合值細化到週頻、單位層級，**對 §5 SE 象限的 overhang 那一格是升級，對 shadow 那一格是零**。已售之後的事情 TEDUH 不追蹤。

（另註：該頁 Files 區在本次偵察時顯示「No items found」，下載管道可能尚未開放。要用須另行確認。）

### 5d. 未能查證的項目（照登，不當成不存在）

- **SPAN《Water Services Industry Performance Report》**：`span.gov.my` 全站在本次偵察期間連續連線逾時（兩次，共 135 秒），**取數失敗屬連線層**。依電力側先例研判內容大概率只有帳戶數與營運 KPI，但**未經實測，不得寫成「已確認無資料」**。這是本檔唯一的未結項，重試成本低。

---

## 最終裁決

### 逐項

| # | 代理 | 裁決 | 一句話理由 |
|:---|:---|:---|:---|
| 1 | 公用事業零用量戶數 | **不可用** | ST／TNB 只公佈帳戶數，無用量分布；帳戶數缺口法已被實測否決（帳戶比存量多 51%） |
| 2 | 人口普查空屋率 | **部分可用（單點水準錨）** | 2020 普查有原因分解且到縣層，但只有一年、實地觀察法、母體與 NAPIC 不同 |
| 3 | CCC vs 評估稅戶籍 | **不可用** | 評估稅對占用狀態失明；第 162 條寬減的選擇方向與 S_shadow 相反；DBKL 無相關開放資料 |
| 4 | 租賃登記／LHDN 租金申報 | **不可用** | MY 無租賃登記制度；LHDN 不發布所得來源分解；遵從率偏誤會系統性高估 shadow |
| 5a | OpenDOSM 年頻住所／住戶序列 | **不可用（已實測證偽）** | 非普查年為外推模型值，KL 2017–2019 算出負空置率，2019→2020 有 11pp 斷點 |
| 5b | KRI 空屋稅政策文件 | **旁證，非代理** | 準官方智庫也只能用普查，並明講無法分辨投機持有 |
| 5c | KRI TEDUH 單位層資料 | **可用於 overhang，不可用於 shadow** | 有銷售狀態、無占用狀態 |

### 總裁決

**`S_shadow` 在 MY 無法量測成序列。它只有一個 2020 年的、口徑受限的單點水準錨。**

具體地說，能拿到的最好的東西是：**2020 年 KL 有 18,036 戶被普查員判定為「度假屋／過境屋」的空置住所（占 KL 普查住所存量 2.84%），這是 KL 都會區 S_shadow 的一個下界。** 除此之外沒有任何可用觀察。

三個必須同時記住的但書：

1. **它是下界，不是估計值。** 25.3% 的未分類殘差（KL 23,403 戶）與「新完工／待租售」欄裡混著的已售未租單位，都可能是 shadow，但無法拆分——這正是 KRI 明講的那個限制。真值在 18,036 與 92,429 之間，區間寬到沒有判別力。
2. **它是 2020 年的。** 下一次普查 2030。2020 又落在 COVID 行動管制的異常期。
3. **它的分母不是 NAPIC 的存量。** 普查「住所」與 NAPIC「住宅存量」是兩個母體（2020 全國 9,614,139 vs 5,845,580；KL 634,639 vs 495,996）。**不得把普查空置戶數除以 NAPIC 存量**，也不得把 2.84% 直接乘上 NAPIC 存量得出「KL 有 N 戶 shadow」。

### 對 §3 與 §4 的具體後果（建議，不逕行修改方法論）

**§3 亞洲修改：從「可量化拆解」降級為「定性機制 ＋ 單點錨」。**

`S_total − S_overhang − S_shadow = S_effective` 這條拆解在 MY **只有前兩項可量測**。建議把 §3 的地位改寫成：懸置釋放閥 Λ 與 S_shadow 是**機制假說**，它解釋「餘屋高企而租金未崩」這個觀察，但**在 MY 無法賦值**。這不推翻機制——F1 命題（租金轉折早於價格轉折 ≥1 季）是**排序型檢定，不需要知道 S_shadow 的水準就能跑**，因為它測的是 Λ 上升的後果，不是 S_shadow 的大小。**§6 的 F1 不受本次偵察影響，維持凍結。**

**§4 檢定 3：分母退回 `S_total − S_overhang`，並在輸出加註偏誤方向。**

檢定 3（隱含需求成長 ＝ `(C − δ·S_total) / S_effective`）的分母若用 `S_total − S_overhang`，等於**把 shadow 層錯誤地算進有效供給**，分母偏大，**隱含需求成長被系統性低估**。也就是說：**用退回版分母算出來的檢定 3 是偏樂觀的**。建議在 §4 的表格與任何輸出中固定加註這一句，讓偏誤方向永遠跟著數字走。

**§5 SE 象限：`S_shadow` 的狀態應由 🔴 改為 🔴（已偵察，確認無代理）**，並把本檔列為結案依據，避免日後重複偵察。

**§7 已知邊界：建議新增第 8 點**，大意為「S_shadow 在 MY 無可量測代理，本框架的亞洲修改在 MY 只能定性成立；檢定 3 的分母因此偏大、結果偏樂觀。此結論基於 2026-08-02 的取數偵察（本檔），若 ST 開放智慧電表用量分布、或 2030 普查改良分類、或 DBKL 公佈第 162 條寬減統計，應重啟」。

### 三個會讓這個結論翻盤的觸發條件（登記備查）

1. **ST／TNB 公佈住宅帳戶用量分布。** 半島 910 萬具智慧電表 2029 年前裝設完成——資料屆時必然存在，只差公佈。這是最有可能翻盤的一條。
2. **2030 普查改良空置分類。** 若把「新完工／待租售」拆成「未售」與「已售待租」，並把 25% 未分類殘差降下來，S_shadow 就能直接讀出。
3. **空屋稅立法。** 若 MY 真的立法課空屋稅（2025 年仍在研議、未立法），課稅本身會創造一個行政空置登記——那將是第一個真正的 S_shadow 觀察值。

---

## 產出的資料檔

`data/my-shadow-proxy.json` — 只收 2020 普查的觀察值（全國與 KL 的空置戶數、空置率、原因分解），每筆帶期別、口徑、來源層級（primary／derived）。檔內明列：**不得用於 §4 檢定當序列、不得與 NAPIC 存量相除**。

沒有其他代理產生任何可入檔的觀察值。


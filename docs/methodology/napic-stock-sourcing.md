# NAPIC 住宅存量與完工量取數紀錄

**建立日**：2026-08-01 ｜ **產出檔**：`data/napic-stock.json` ｜ **服務對象**：`four-quadrant-v1.md` §4 檢定 2／檢定 3、`forward-ledger.md` 條目 005（F2 州別 δ\* 排序）

本文件記錄取數路徑、欄位口徑、可得與缺失期別，以及解析過程踩到的每一個坑。**寫這份文件的目的是讓下一個人不必重做一次考古。**

---

## 一、找對出版品：Stock Table，不是 Status Table

這是本次取數最重要的一個發現，也是先前把 SE 象限卡在 🟡 的原因——**先前的取數路徑找錯了出版品**。

NAPIC 底下有兩個平行的季度出版品系列，名字像、內容完全不同：

| 出版品 | 馬來文 | 存放的東西 | 檔案入口 |
|:---|:---|:---|:---|
| **Property Stock Report** | Laporan Stok Harta Tanah | **存量、完工量、開工、在建、已核准未動工** | `/archives/inventori-harta-tanah` |
| Property Market Status Report | Laporan Jadual Status Harta Tanah | 成交量值、**餘屋 overhang**、未售、MHPI | `/archives/laporan-status-harta-tanah` |

四象限的 `S_total`（存量）與 `C`（完工量）**只在 Stock Report 裡**。Status Table 沒有存量欄位。

**推論**：方法論 §5 給的驗證錨點（MHPI 2010=100、住宅餘屋 30,471、SA 餘屋 18,752、Johor 9,477）全部出自 Status Table，因此**無法用來驗證本檔的任何數字**——它們是兩份不同的出版品，口徑也不同（Status Table 的餘屋是「完工未售」，Stock Table 的存量是「已發 CCC 的累計戶數」）。本檔改用內部一致性檢定驗證，見第五節。

## 二、URL 怎麼拼

檔案清單不在靜態 HTML 裡，`/archives/inventori-harta-tanah` 這頁預設只列**最新一期**。歷史期別要打 October CMS 的 AJAX filter：

```
POST https://napic.jpph.gov.my/ms/archives/inventori-harta-tanah
Headers:
  X-Requested-With: XMLHttpRequest
  X-OCTOBER-REQUEST-HANDLER: onFilterArchives
  X-OCTOBER-REQUEST-PARTIALS: archives/table&archives/paginate
Body: _session_key, _token（兩者從 GET 該頁的隱藏 input 取得，需帶 cookie jar）
      Filter[year]=2015, Filter[keyword]=, Filter[title]=, Filter[volume]=
```

**坑**：`X-OCTOBER-REQUEST-PARTIALS` 的分隔符是 `&`，不是逗號。用逗號會回 500 `Invalid partial name`。這一步卡住的話整個歷史序列都拿不到。

年份下拉選單提供 2005–2026，但住宅 Stock Table 實際只從 2008 起（2005–2007 該分頁只有 4 筆年報，無住宅季表）。

檔案 URL 沒有穩定規則，**三代路徑並存**，不要試圖用字串拼湊，一律從 AJAX 回傳的 `<a href>` 取：

```
2008–2023  /storage/app/media//3-penerbitan/inventori/{year}/{S1..S4}/{timestamp}{slug}.pdf
2023       /storage/app/media//3-penerbitan/inventori/2023/Q4/Jadual Stok Harta Kediaman Q4 2023.xls
2024–2026  /storage/app/media//3-penerbitan/Shahrul/Bahagian Inventori Harta Tanah/
           Laporan Jadual Stok Harta Tanah/Q1 2026/Jadual Stok Harta Kediaman Q1 2026.xlsx
```

注意路徑含**雙斜線** `media//3-penerbitan` 與空格，空格要 percent-encode，雙斜線要保留。檔名亦不規則（`Q1 2025_new.xls`、`q408residential_P.pdf`、`propertystockresidentialtableq42019.xls`）。

## 三、可得與缺失期別

| 項目 | 覆蓋 | 狀態 |
|:---|:---|:---|
| 檔案下載 | 2008Q1–2026Q1，73 個季度檔 | 全數成功，0 失敗 |
| `existing_stock` | **2007Q4–2026Q1，74 期** | 無缺口，17 個地區全滿 |
| `completions` | **2007Q4–2026Q1，74 期** | 無缺口，17 個地區全滿 |
| `starts` | 2007Q4–2026Q1，74 期 | 無缺口 |
| `planned_supply` | 2007Q4–2026Q1，74 期 | 無缺口 |
| `new_planned_supply` | 2007Q4–2026Q1，74 期 | 無缺口 |
| `incoming_supply` | 2008Q1–2026Q1，73 期 | 無缺口 |
| `under_construction` | 2007Q4–2017Q1，38 期 | **NAPIC 於 2017Q1 後停止單列此欄**（併入 incoming supply） |

2007Q4 是額外收穫：2008Q1 的檔案內同時印出前一季，一併收錄。

地區切面 **17 個全有**：MALAYSIA 總計＋16 個州／聯邦直轄區（含 Johor／KL／Selangor／Pulau Pinang）。

**未取**：州以下的縣／區層級。Stock Report 的 Table 2–17 有各州的縣級細分（KL 到 Section／Precinct 層級），本次只解析 Table 1。若日後需要 KL 分區，同一套 parser 換 sheet 即可，格式相同。

## 四、欄位對照表

### 4.1 供給段落（section）

住宅類別下實際有七個供給段落。定義**逐字引自 NAPIC 報告內的 Explanatory Notes**，不是推測：

| NAPIC 段落名 | 四象限對應 | 累計性質 | 官方定義（節錄） |
|:---|:---|:---|:---|
| EXISTING STOCK | `S_total` | 累計存量 | 於檢視期前已取得 CCC／CF／TCF 的戶數，加上檢視期內完工並取得 CCC 的戶數。含延遲通報、用途變更、拆除重建的調整 |
| COMPLETIONS | `C` | 期間流量 | 建築工程完成並核發 CCC |
| INCOMING SUPPLY | 未來供給（在建） | 累計 | 檢視期內實體工程進行中的戶數＝該期 starts ＋ under construction |
| UNDER CONSTRUCTION | incoming 的子項 | 累計 | 2017Q1 後停列 |
| STARTS | 動工 | 期間流量 | 低層建物基礎工程開始，或高層建物地面以下含打樁基礎工程開始 |
| PLANNED SUPPLY | 已核准未動工 | 累計 | 已取得建照但尚未動工；含建照失效與修訂的調整 |
| NEW PLANNED SUPPLY | 新增核准 | 期間流量 | 檢視期內取得建照的戶數 |

早期版本段落名為單數 `COMPLETION`，同一段落。

### 4.2 型別欄位（type columns）

**更正（2026-08-02）**：本節初版寫「欄位層級沒有馬來文對照可記」，**這是錯的**。季度**表**檔（Jadual）的欄頭確實是純英文，但同一個 archive 裡另有一份**年度敘述報告**（`Laporan Stok Harta Tanah`，獨立 PDF），內含完整雙語的 Catatan Teknikal／Technical Notes 章節，段落名與住宅型別名全部有官方馬來文。初版只解析了 Jadual 沒有下載 Laporan，因而下了錯誤結論。以下對照轉錄自 `Laporan Stok Harta Tanah 2025` 第 2.1–2.6、5.2、10.0 節。

段落層級：

| 馬來文 | 英文 |
|:---|:---|
| Inventori Sedia Ada（stok） | Existing Inventory（stock） |
| Siap Dibina | Completions |
| Penawaran Akan Datang | Incoming Supply |
| Dalam Pembinaan | Under Construction |
| Mula Dibina | Starts |
| Penawaran Dirancang | Planned Supply |
| Penawaran Baharu Dirancang | New Planned Supply |
| Penawaran Hadapan | Future Supply（＝incoming ＋ planned） |
| Harta Tanah Kediaman | Residential Property |
| Liputan Kajian／Tempoh Kajian | Coverage／Review Period |

住宅型別層級（Laporan §5.2）：

| 馬來文 | 英文 |
|:---|:---|
| teres | terraced |
| berkembar | semi-detached |
| sesebuah | detached |
| unit kos rendah | low-cost units |
| rumah pangsa | flats |
| pangsapuri／kondominium | condominium／apartment |
| unit berkelompok | clustered units |
| rumah bandar | town houses |

Jadual 的 11 欄在此之上再依樓層數細分（單層 vs 二至三層 teres／berkembar）並把 low-cost 拆成 house 與 flat，**這些細分只有英文**。

出版品名稱層級：

| 馬來文 | 英文 |
|:---|:---|
| Laporan Stok Harta Tanah | Property Stock Report |
| Jadual Stok Harta Kediaman | Residential Property Stock Table |
| Ringkasan Penawaran Unit Kediaman Mengikut Jenis Di Malaysia | Summary of Supply of Residential Units by Type in Malaysia |
| Sukuan／Tahun／Muat Turun | Quarter／Year／Download |

型別欄位本身**跨期不一致，有一次斷點**：

| 期間 | 欄數 | 欄位 |
|:---|:---|:---|
| 2007Q4–2015Q4 | 12 | Single Storey Terrace／2-3 Storey Terrace／Single Storey Semi-Detach／2-3 Storey Semi-Detach／Detach／Town House／Cluster／Low Cost House／Low Cost Flat／Flat／**Service Apartment**／Condominium-Apartment |
| 2016Q1–2026Q1 | 11 | 同上，**移除 Service Apartment** |

## 五、兩個必須知道的序列斷點

**不看這一節就拿去算成長率，會算出假的東西。**

### 斷點 1：2016Q1 服務式公寓改列商用

NAPIC Explanatory Note 2 原文：「Beginning Q1 2016, service apartments have been categorised as commercial properties as these property are built on commercial land.」

後果：全國存量 2015Q4 的 4,928,883 → 2016Q1 的 4,876,439，**在完工量為正的情況下掉了 52,444 戶**。這不是拆房子，是把 SA 整批移出住宅類別。

這也解釋了站內既有事實「SA 餘屋在 NAPIC 是分開統計的」——SA 從 2016 起就不在住宅口徑內了。**跨 2015Q4／2016Q1 不得計算存量成長率。**

### 斷點 2：2017Q1 補登舊案的重述

NAPIC 在 2017Q1 報告的每一列存量數字後面掛 `*Note 1`，原文：「Revised in Q1 2017 to include data on projects that have been completed and issued with CCC in the prior years but have only been captured in the current study period.」

後果：全國存量單季跳 **+355,289 戶，而該季申報完工量只有 20,325 戶**。這是積壓案件的補登，不是新蓋出來的房子。**2017Q1 的 ΔS 不得當作完工流量使用**，δ\* 用申報的 `completions` 欄算，不要用 ΔS 反推。

### 第三個坑：完工量從 2016 起改為年度累計

NAPIC Explanatory Note 3 原文：「Prior to Q1 2016, reported figures on 'Completions', 'Starts' and 'New Planned Supply' are non-accumulative and indicated totals within the review period. Starting Q1 2016, the reported figures are accumulative totals which include units recorded in the previous quarter plus units in the current quarter of the same year.」

也就是 2016 起 Q2／Q3／Q4 印的是 `Q1 - Qn` 的**年初至今累計**，期別標籤也真的寫成 `Q1 - Q3 2025`。直接當季度值用會把全年完工量灌水到近 2.5 倍。

`napic-stock.json` 存的是**還原後的季度流量**：`Qn = YTD(Qn) − YTD(Qn−1)`，Q1 照登。每一個還原值都帶 `basis: "derived_ytd_difference"` 與所用的兩個原始累計值（`ytd_cumulative`／`ytd_prior_cumulative`），可逐筆回溯。

## 六、驗證結果

因為第一節說明的原因，方法論 §5 的錨點不適用於本檔，改用四項內部檢定：

| 檢定 | 結果 |
|:---|:---|
| **列加總檢定**：各型別欄位加總 = 印出的 Total | **0 失敗**（74 期 × 17 地區 × 7 段落全數通過） |
| **YTD 還原檢定**：還原後的季度完工量不得為負 | **0 筆為負**（若假設錯，必然出現負值） |
| **年度交叉檢定**：四季還原值相加 = 該年 Q4 印出的 YTD 累計 | **完全相等**（2016／2019／2022／2025 逐一驗，全國 78,216／87,731／71,981／99,877） |

**這三項全部只是「解析正確性檢定」——證明我把檔案抄對了，不證明四象限 SE 恆等式成立。** 恆等式本身的檢定結果是**不成立**，見第七節。

另有 2,851 筆跨版次修訂。計數口徑：同一個（段落／期別／地區）在兩個以上季報檔中出現且數值不同，每一組差異計 1 筆；分布為 planned_supply 588、incoming_supply 527、under_construction 481、existing_stock 457、completions 308、new_planned_supply 302、starts 188。這是 NAPIC 的正常修訂行為（當期標 `P` ＝ preliminary，次期修訂），只發生在 2016 前的舊檔（一檔含 2–4 期）；2019Q4 起每檔只含自身一期，無跨版次比對。本檔採「**最終修訂版優先**」，每一格都記錄 `src` 指向實際取數的檔案期別，修訂清單留在 scratchpad `conflicts.json`。

## 七、SE 恆等式不成立：ΔS 系統性大於 C

### 7.1 現象

四象限 SE 象限寫 `ΔS = C − δ·S`，δ ≥ 0 因此要求 **ΔS ≤ C**。NAPIC 資料上這條**不成立，而且是單方向的**：

- 73 個季度裡 **65 季 ΔS > C**（5 季為負、3 季為零）；剔除 2016Q1／2017Q1 兩個已記錄斷點後仍是 71 季中 64 季為正
- 年度看，2018–2025 每一年 ΔS 都比 C 多出存量的 **0.59%–1.29%，八年無一例外、無一年反向**
- 2018–2025 累計：ΔS 1,099,803 戶 vs C 663,566 戶，**差 436,237 戶**

計算口徑：全部取 MALAYSIA 匯總列；季度殘差 ＝ [S(p) − S(p−1)] − C(p)；年度殘差 ＝ [S(y Q4) − S(y−1 Q4)] − 該年四季 C 加總，**百分比分母為年末存量 S(y Q4)**（改用年初存量各年最多差 0.04pp）；65／73 那個計數**含**兩個斷點季，64／71 則排除。

### 7.2 一項必須撤回的說法

本文件初版在驗證表裡寫「恆等式殘差中位數約 0.15%，與 NAPIC 自述的調整項量級相符」。**那個數字是季度殘差的中位絕對值，它把正負號藏掉了，把系統性單向偏誤說成了對稱雜訊。這個描述是錯的，予以撤回。** 正確的說法是：殘差不是雜訊，是持續同向的結構性缺口，年化約 0.6–1.3%。

### 7.3 殘差落在哪裡——四個假設，全部證偽

| 假設 | 檢定 | 結果 |
|:---|:---|:---|
| 集中在某一種住宅型別（例如 SA 回流） | 逐 11 欄拆 2018–2025 | **證偽**——11 欄全都有，各佔該欄 ΔS 的 20%–50% |
| 集中在某一州（特定行政作業問題） | 逐 16 州拆 | **證偽**——16 州全為正，佔 ΔS 的 9.7%（Putrajaya）至 60.6%（Terengganu） |
| 只是 2017Q1 那種一次性重述 | 逐季看符號 | **證偽**——71 個非斷點季裡 64 季為正 |
| 殘差在 NAPIC 調查覆蓋最弱處最大（以高層佔比低為代理） | 16 州 Spearman（高層佔比／殘差比） | **無法判定**——ρ = −0.415、p = 0.110、n = 16（見下方更正） |

前三個證偽成立，所以這不是某個局部的資料瑕疵。

**更正（2026-08-02）**：第四項本文件初版寫「ρ = +0.29，方向相反，證偽」。**那個係數是錯的。** 我當時用自寫的 Spearman，公式把平方秩差除以 `2·n(n²−1)/6` 而不是 `n(n²−1)/6`，多除了一個 2。改用 `scipy.stats.spearmanr` 重算，正確值是 **ρ = −0.415，符號與我報的相反**。

方向其實**符合**覆蓋假設（越少高層的州、殘差比越大），但 n = 16 時 p = 0.110 不到常規顯著水準。因此正確的結論是「**無法判定**，既不能確認也不能證偽」，而不是我原本寫的「證偽」——**這個假設從來沒有被有效證偽過**。第 7.4 節的官方定義解釋不依賴這一項，結論不受影響。

計算口徑：x ＝ 2025Q4 存量中（Low Cost Flat ＋ Flat ＋ Condominium／Apartment）佔該州總存量比；y ＝ 2018–2025 累計 (ΔS − C) / ΔS。

### 7.4 NAPIC 自己的說明（原因已記載，量化不可得）

原因寫在官方定義裡，不需要猜：

1. 季報 Explanatory Note 1.1：存量「comprises of adjustments made due to: **delayed data from previous review periods but received during the review period; change in category of use; destroyed/rebuilt**」。
2. `Laporan Stok Harta Tanah 2025` §2.3／§2.5：本調查「**has not reached a total population count**」（belum menyamai jumlah bilangan penduduk），並把「**an increase in coverage**」（pertambahan dalam kawasan liputan kajian）列為常設調整原因。
3. 同報告 §10.0 Liputan Kajian／Coverage：調查範圍限於「地方政府轄區內／住宅計畫（skim perumahan）／計畫外但已取得建照的建物」。

也就是說 **NAPIC 的存量是一份仍在擴張中的調查底冊，不是完整登記簿**。存量會吸收「本來就存在、只是這一季才被納入調查」的舊單位；完工量只計「這一季在既有調查範圍內取得 CF／TCF」的單位。兩欄涵蓋範圍本來就不同，缺口是**定義上的必然**，不是資料錯誤。

**查不到的部分照實說**：NAPIC 沒有公布調整項的分解，所以這 436,237 戶**無法拆成「延遲通報 / 覆蓋擴張 / 用途變更 / 拆除重建」各佔多少**。任何分解都是編的。結論是「原因已記載、各管道量級不明」。

## 八、δ\* 該用哪個口徑

### 8.1 裁決：兩個都要，當成上下界並列，不得單取其一

| 口徑 | 性質 | 為什麼不能單獨用 |
|:---|:---|:---|
| `C / S`（v1.0 凍結算式） | **下界** | 漏掉發生在調查範圍外的完工 |
| `ΔS / S`（帳面存量成長） | **上界** | 含入舊單位補登、覆蓋擴張、用途變更等非新建的帳務增量 |

真實的實體供給成長落在兩者之間。2025 年全國 `C/S` = 1.53%、`ΔS/S` = 2.82%——**差距近一倍，所以「取哪個」不是無關痛癢的細節**。

理由：兩個口徑各自的偏誤方向是**已知且相反**的，但偏誤幅度不可觀測（見 7.4）。在這種情況下報區間是唯一誠實的作法；挑一個報點估，等於假裝知道自己不知道的事。

`data/napic-stock.json` 新增 `derived.annual`，逐年逐州同時給 `delta_star_C_over_S` 與 `stock_growth_dS_over_S`，並附 `residual_units`。**原始申報值一格未動。**

### 8.2 §4 檢定 2 要不要改：分兩種用途看

**用途 A——比對汰換基準帶（水準型）**：檢定 2 拿 δ\* 對 0.5–1.5% 的汰換帶比。這個用途**對口徑高度敏感**：`C/S` 的 1.2–1.7% 剛好貼著帶子上緣，`ΔS/S` 的 2.8% 則遠遠超出。**結論會反轉，所以水準型用途必須報區間。**

**用途 B——州別排序（forward-ledger 條目 005／F2）**：兩個口徑對 16 州的排序**大致一致但不可互換**。

**更正（2026-08-02）**：本文件初版寫「Spearman 平均 0.855（區間 0.775–0.919），F2 不受影響」。**那組數字是錯的**，來自與 7.3 同一個 Spearman 少除以 2 的 bug。用 `scipy.stats.spearmanr` 重算：

| 年 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 平均 |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ρ | 0.629 | 0.838 | 0.550 | 0.815 | 0.721 | 0.747 | 0.729 | 0.652 | **0.710** |

計算口徑（寫下來才能被獨立重算）：Spearman 秩相關，`scipy.stats.spearmanr`，tie 取平均秩（本例無 tie）；A ＝ 當年四季完工加總 / S(y Q4)，B ＝ [S(y Q4) − S(y−1 Q4)] / S(y Q4)，**兩者分母同為年末存量**；**n = 16，排除 MALAYSIA 匯總列**；年份取 2018–2025 以完全避開兩個斷點。分母改用年初存量得平均 0.720、區間 0.550–0.862，結論不變。

**結論也跟著改**：平均 0.710，且 2020 年低到 0.550——低於 forward-ledger 對排序型預測的 ρ ≥ 0.6 及格線。因此**不能宣稱「F2 不受口徑影響」，這個說法予以撤回**。正確的作法是：**F2 評分時兩個口徑都算，若兩者在 −0.3 門檻的兩側分歧，記為無法判定。**

### 8.3 建議（不逕自修改凍結規格）

`four-quadrant-v1.md` §1 明文「本規格凍結……特別禁止：先看資料再改判準」。因此我**不修改** §4 檢定 2 的算式，只提出建議，由你決定是否開 v1.1：

- v1.0 下繼續用 `δ* = C / S_total`，但**必須標註為下界**，不得與 0.5–1.5% 汰換帶做單點比較後下「相容／不相容」的定論
- 建議 v1.1 把檢定 2 改寫為區間形式（`δ*_low = C/S`、`δ*_high = ΔS/S`），並把判準改成「區間是否整段落在基準帶內」
- **F2（條目 005）的命題與門檻不需要改**，但評分程序要求兩個口徑都算並在分歧時記為無法判定，理由見 8.2 用途 B（此處已依 2026-08-02 的重算更正，初版寫「F2 不受影響」是錯的）

### 8.4 順帶發現：F2 的門檻本身跑不動

用 F2 凍結的閘門「δ\* 連續 3 年 ≥3%」掃 2008–2025，**兩個口徑都只篩出 2 個州**（Putrajaya 與 Terengganu，窗口不同：`C/S` 為 2016–2021 與 2015–2017，`ΔS/S` 為 2021–2024 與 2023–2025）。n = 2 遠不足以做 F2 指定的 Spearman 檢定。

計算口徑：16 州逐年計算該口徑（分母為年末存量），找出 ≥3% 的最長連續年數，取 ≥3 年者。

這是**凍結命題本身的設計限制，不是資料的問題**。門檻已凍結，**不得為了湊樣本而調整**；評分日照實記為「樣本不足、無法評分」即可。

## 九、解析的坑（逐條）

1. **`.xls` 副檔名不保證是 Excel。** 直接 GET 出版品頁面拿到的「q42025.xls」其實是 HTML 導覽頁。先 `file` 驗真身再解析。
2. **三種檔案格式**：2008Q1–2019Q3 是 PDF（47 檔）、2019Q4–2025Q3 是真 `.xls`（BIFF，用 `xlrd`）、2025Q4 起 `.xlsx`（用 `openpyxl`）。PDF 全部是**文字型可直接抽取**，`pdftotext -layout` 即可，不需要 OCR。
3. **標題列位置不固定**，段落標題在 A 欄與 B 欄之間交替（2026Q1 的 xlsx：EXISTING STOCK 在 A7、COMPLETIONS 在 B28、INCOMING SUPPLY 在 A49……）。解析時把整列非空儲存格併起來比對，不要鎖定欄位。
4. **期別標籤會換行掉到資料列上。** 2016Q3 的 PDF 裡 `Q1 - Q3` 在第一列、年份 `2016P` 掉到 Putrajaya 那一列的行首。不處理就會少一格。
5. **期別標籤有時沒有年份**（`Q1 - Q3` 後面直接接州名），需用檔案本身的年份補。
6. **儲存格內容會被截斷**：2025 年兩個 `.xls` 檔的 KL 寫成 `W.P. Kuala`（少了 Lumpur）。州名比對要備妥別名表，否則整個 KL 序列會靜默消失。
7. **數字後面會掛註腳**：2017Q1 每列尾端有 `*Note 1`、`*Note1`、`* Note 1`、`238,198*1` 四種寫法。純數字正則會整列比對失敗。
8. **Table 1 的區間要明確切斷。** Table 2–17 是各州縣級細分，段落標題與 Table 1 一模一樣。切不乾淨的話，縣名不會誤判為州名，但期別會被帶著跑。本 parser 採「同一〔段落／期別／地區〕只取第一次出現」，Table 1 必定先出現。
9. **合併儲存格**：Table 1 的段落標題列是 `A7:G1` 之類的合併範圍。`openpyxl` 讀 `values_only=True` 時只有左上角有值，其餘為 `None`——照第 3 點的做法併列即可，不必展開合併範圍。
10. **單位是「戶」（units），不是 RM。** Stock Table 全表無金額欄位；金額只在 Status Table 有。

## 十、δ\* 現在算得出來嗎

**算得出來，全國與 16 州皆可，2008–2025 共 18 個完整年度。**

`δ* = C_年度 / S_total(年末)`，兩個欄位都是 NAPIC 直接申報值，不需要任何假設參數。算出來的全國區間約 **1.2%–3.0%**，落在方法論 §4 檢定 2 的住宅實際汰換基準帶（0.5–1.5%）之上——這正是檢定 2 想抓的訊號（存量膨脹快於正常汰換）。

對 `forward-ledger.md` 條目 005（F2）的**一個實務提醒**：F2 的門檻寫的是「δ\* 連續 3 年 ≥3%」。以實際資料看，僅 2008–2010 有少數州達到 3%，2011 之後幾乎沒有。**門檻於 2026-08-01 凍結，不得因為看到資料而調整**（§1 修訂規則明文禁止）；但評分時很可能面臨合格州數過少、Spearman 檢定樣本不足的情況，這是條目本身的設計限制，屆時照實記錄為「樣本不足、無法評分」，不要為了湊樣本而改門檻。

**尚未打通、仍為 🔴 的**：`S_shadow`（已售空置）在本出版品中沒有任何對應欄位，維持方法論 §5 的缺口判定不變。

## 十一、如何更新

NAPIC 每季發布，約落後 1.5–2 個月（Q1 2026 於 2026-05-15 發布並註明 amended）。更新流程：跑第二節的 AJAX 取當年檔案清單 → 下載新期別 → 用同一 parser 解析 Table 1 → 併入 `data/napic-stock.json` 的 `data` 與 `sources`。scratchpad 內留有 `crawl_archive.py`／`dl_stock.py`／`parse_stock.py`／`assemble.py`／`final.py` 五個腳本與全部 73 個原始檔。

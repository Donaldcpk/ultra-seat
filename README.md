# 終極課室座位表（Ultra Seat）

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-線上可用-brightgreen)](https://donaldcpk.github.io/ultra-seat/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v2.2.0-orange.svg)](CHANGELOG.md)

> **立即使用（免安裝）**：[https://donaldcpk.github.io/ultra-seat/](https://donaldcpk.github.io/ultra-seat/)

香港中學**班主任**用的排位＋課室管理網頁：誰不能坐一齊、擋壞桌、前排／SEN、列印課室門海報。開啟瀏覽器即可；學生資料只留在你的電腦。

## 為什麼需要這個？

CloudSAMS（前 WebSAMS）已有「編修座位表」、上傳相片、依班點名，但那主要是**畫座位圖**，不是日常課室管理。很多老師仍用 Word／Excel 做座位表。

本工具對標的是「座位表即課室管理面」的用法（類似海外 Class Charts／Seating Plan 的思路，但**只服務港校班主任、繁體中文、零安裝**）：

- 指定兩人不可同坐（四周／左右／前後）
- 擋壞桌、通道
- 前排／SEN 優先
- 一鍵列印 A4 貼課室門，代課老師也看得懂
- 課室布局模板存本機，不用每次重擋桌

**不是**考務／試場編排工具。梅花座等考務選項若存在，只放在「進階（少用）」，不是產品主軸。

## 已實作功能

- **CSV 匯入／匯出**：建議 `班別,班號/學號,姓名[,職務][,前排/SEN]`；相容舊格式 `學號,姓名,職務`
- **課室格網**：2×2 至 **12×12**（一般中學課室足夠）
- **阻擋座位**：壞桌、柱、通道
- **不可同坐**：兩位學生四周／左右／前後不可相鄰（相對純手編座位的主要差別）
- **智能分配**：回溯法 + MRV；約 40 人、數組限制可解；過密會**清楚失敗**（有搜尋上限，不宣稱 100%）
- **前排／SEN**：CSV 填「是」時優先試前兩排（**不會**從姓名猜性別）
- **課室模板**：名稱、行列、阻擋存於瀏覽器；重整後仍在；模板不含學生名單
- **A4 列印**：黑板在上、班名、日期、格內姓名、圖例；用瀏覽器列印即可

## 刻意不做

| 項目 | 說明 |
|------|------|
| 依姓名推斷性別 | 不做（港校不宜） |
| 班幹部自動前排、性別均衡、最小間距 | 舊文件曾寫、**未實作**；已不宣傳 |
| 試場／禮堂／考務為主產品 | 不做為主軸 |
| 英文介面／多語系／帳號雲端 | 本階段不做 |
| 遙測 | 不做；名單不上傳 |

## 快速開始（班主任）

1. 打開[線上版](https://donaldcpk.github.io/ultra-seat/)或本機雙擊 `index.html`
2. 填學校、班別、日期、行列 →「建立／套用課室」
3. 切「阻擋」點壞桌 →「儲存目前布局」成模板（下次直接載入）
4. 匯入 CSV，或按「建立班內範例」
5. 右側加「不可同坐」（例如兩人四周不可相鄰）
6. 「智能分配」→「列印 A4 座位表」→ 貼課室門

## CSV 欄位

建議標題列（UTF-8）：

```text
班別,班號,姓名,職務,前排
中三甲,01,陳志明,班長,
中三甲,04,黃嘉欣,,是
中三甲,05,張偉強,,
```

| 欄位 | 必填 | 說明 |
|------|------|------|
| 姓名 | 是 | |
| 班號 或 學號 | 是 | |
| 班別 | 建議 | 顯示與進階「同組分散」用 |
| 職務 | 否 | |
| 前排 或 SEN | 否 | 填 `是`／`1`／`SEN` |

仍支援舊檔：`學號,姓名,職務`。

## 如何列印課室門海報

1. 畫面上已有姓名分配
2. 按「列印 A4 座位表」
3. 選 **A4 直向**；若預覽幾乎空白，在列印設定打開「背景圖形」
4. 應見：校名／班名、日期、上方黑板、格內姓名、下方圖例

## 私隱

- 純前端；名單與座位只在瀏覽器
- 模板只含格網與阻擋，**不含**學生名單
- 公用電腦用完請關閉分頁

## 安裝與開發

```bash
git clone https://github.com/Donaldcpk/ultra-seat.git
cd ultra-seat
# 瀏覽器開啟 index.html，或：
python3 -m http.server 8080
```

```bash
node test_school_edition.js
```

## 架構

```text
index.html              # 單一網頁（介面、CSV、解算、列印、模板）
test_school_edition.js  # 核心邏輯單測
CHANGELOG.md            # 版本變更
```

解算器針對**一班約 40 人、少量不可同坐**；達節點或時間上限則回報失敗。

## 版本

- SemVer；變更見 [CHANGELOG.md](CHANGELOG.md)
- 目前：**v2.2.0**（班主任課室排位）

## 授權

[MIT License](LICENSE)｜問題：[GitHub Issues](https://github.com/Donaldcpk/ultra-seat/issues)

---

Repo 內 Python GUI／舊 HTML 備份僅供參考；**請以 `index.html` 為準**。

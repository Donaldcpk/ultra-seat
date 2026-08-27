# Ultra Seat 學校版｜終極智能教室座位表生成器

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-brightgreen)](https://donaldcpk.github.io/ultra-seat/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v2.2.0-orange.svg)](CHANGELOG.md)

> **立即使用（免安裝）**: [https://donaldcpk.github.io/ultra-seat/](https://donaldcpk.github.io/ultra-seat/)

香港中學可用的**課堂座位表**與**校內考試座位表**網頁工具。開啟瀏覽器即可，學生資料只留在你的電腦，不上傳、無帳號、無追蹤。

## 這是給誰用的？

班主任、科任老師、考試主任：匯入學生 CSV → 擋壞桌／通道 →（可選）設定「這兩人不要坐旁邊」→ 智能分配 → **列印 A4** 貼在課室門／試場。

## 主要功能（已實作）

- **CSV 匯入／匯出**：相容舊格式 `學號,姓名,職務`；建議港校格式見下方
- **自訂格網**：2×2 至 **25×20**（可應付約 20×15 考試禮堂；畫面會自動縮小格子）
- **阻擋座位**：壞桌、柱、通道
- **配對限制**（產品差異化）：兩位學生「四周／左右／前後」不可相鄰
- **智能分配**：回溯法 + MRV；過密限制會**明確失敗**，不會假裝成功（有節點／時間上限，不宣稱 100% 可解）
- **考試模式**
  - **梅花座**：已佔座位的上下左右不可再有人；阻擋格不算「有人」
  - **同班別／組別分散**（可選）：CSV 有「班別」或「組別」時，正交相鄰不同班
- **教室模板**：名稱、行列、阻擋座位存於瀏覽器 `localStorage`，重整後仍在
- **A4 列印**：瀏覽器列印樣式（黑板在上、姓名在格、圖例）；無需額外 PDF 軟體
- **前排標記**：CSV「前排／SEN」為「是」時，智能分配會優先試前兩排（不是從姓名猜性別）

## 刻意不做／已移除宣傳

| 項目 | 說明 |
|------|------|
| 依姓名推斷性別 | **未實作且不會做**（港校不宜） |
| 班幹部自動前排、性別均衡、最小間距 | 舊文件曾提及，**程式未實作**；已自 README 拿掉 |
| 帳號／雲端／遙測 | 不做；名單不送出伺服器 |
| 安裝 Python | 學校版以網頁為準；repo 內 Python GUI 僅作歷史參考 |

## 快速開始

1. 打開 [線上版](https://donaldcpk.github.io/ultra-seat/) 或本機雙擊 `index.html`
2. 填學校／班級名稱、日期、行列 →「建立／套用教室」
3. 切「阻擋」點壞桌 → 可「儲存目前布局」成模板
4. 匯入 CSV 或按「建立範例」
5. （可選）右側加配對限制
6. 「智能分配」→「列印 A4 座位表」

### 考試流程

1. 切換「考試」→ 勾選梅花座（預設開）與同班分散（有班別欄才有效）
2. 匯入兩班合併 CSV，或按「建立範例（兩班考試）」
3. 智能分配 → 列印

## CSV 欄位

建議標題列（UTF-8）：

```text
班別,學號,姓名,職務,前排
中三甲,01,陳志明,班長,
中三甲,04,黃嘉欣,,是
中三乙,01,李同學,,
```

| 欄位 | 必填 | 別名 |
|------|------|------|
| 姓名 | 是 | name |
| 學號 或 班號 | 是 | id |
| 班別 或 組別 | 考試分散用 | class / group |
| 職務 | 否 | |
| 前排 或 SEN | 否 | 填 `是` / `1` / `SEN` |

仍支援舊檔：`學號,姓名,職務`（無標題或舊標題皆可）。

## 如何列印

1. 先完成分配（畫面上要看得到姓名）
2. 按「列印 A4 座位表」
3. 列印對話框選 **A4直向**；若只有空白頁，請開啟「背景圖形」／「Background graphics」
4. 預覽應像課室門海報：校名／班名、日期、上方黑板、格內姓名、下方圖例

## 課堂 vs 考試

| | 課堂 | 考試 |
|--|------|------|
| 梅花座 | 關 | 可開 |
| 同班分散 | 關 | 可開（需班別欄） |
| 配對限制 | 可用 | 可用 |
| 用途 | 日常座位 | 試場隔開、兩班混坐 |

## 私隱

- 純前端；名單與座位只在瀏覽器記憶體／本機模板
- 模板**不含**學生名單，只含格網與阻擋
- 請勿在公用電腦留下含學生資料的分頁後不關閉

## 安裝與開發

```bash
git clone https://github.com/Donaldcpk/ultra-seat.git
cd ultra-seat
# 用瀏覽器開啟 index.html，或用任意靜態伺服器
python3 -m http.server 8080
```

核心單測（Node，不需瀏覽器）：

```bash
node test_school_edition.js
```

## 架構總覽

```text
index.html     # 學校版單一檔（UI + CSV + CSP 回溯 + 列印 CSS + localStorage）
test_school_edition.js  # 梅花座／限制／容量檢查
CHANGELOG.md   # 版本變更
```

解算器：回溯 + 最小剩餘值（MRV）；考試可加梅花座／同班正交分散；配對限制沿用四周／左右／前後。達節點或時間上限則回報失敗，**不保證**任意限制組合必有解。

## 版本與變更

- 版本規則：Semantic Versioning
- 變更日誌：[CHANGELOG.md](CHANGELOG.md)
- 目前：**v2.2.0** 學校版

## 授權與維護

- 授權：[MIT License](LICENSE)
- 問題與建議：[GitHub Issues](https://github.com/Donaldcpk/ultra-seat/issues)

---

舊版 Python GUI／`perfect_version.html` 仍留在 repo，**請以 `index.html` 學校版為準**。

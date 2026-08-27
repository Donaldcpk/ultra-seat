# Changelog

本專案遵循 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，版本號採 [Semantic Versioning](https://semver.org/lang/zh-TW/)。

## [Unreleased]

## [2.2.0] - 2026-08-27

### Added
- 學校版網頁：課堂／考試用途模式
- 考試梅花座（正交相鄰不可同時有人；阻擋格不算佔用）
- 可選同班別／組別正交分散（CSV 需有班別或組別）
- A4 直向瀏覽器列印海報（校名、班名、日期、黑板、格內姓名、圖例）
- 教室模板存於 `localStorage`（名稱、行列、阻擋座位）
- 港校 CSV：班別／組別、學號或班號、姓名、職務、前排／SEN；相容舊 `學號,姓名,職務`
- 回溯法 + MRV 智能分配；失敗時清楚提示（含節點／時間上限說明）
- 格網上限擴至 25×20；大格網自動縮小座位格子
- 課堂 40 人／兩班考試範例與範例 CSV 下載
- `test_school_edition.js` 核心邏輯單測

### Changed
- README 改為繁中誠實功能表；列印與考試／課堂說明
- 智能分配不再使用「最多 1000 次 shuffle + 貪婪」並宣稱 100%

### Removed
- 依姓名推斷性別的使用（不再寫入學生物件或演算法）
- README 中未實作的班幹部前排、性別均衡、最小間距宣傳

## [2.1.0] - 2024-12-19

### Added
- 三種配對限制：四周／左右／前後不可相鄰
- 限制清單可視化與刪除
- 網頁版智能分配（當時為 shuffle + 貪婪）

## [2.0.0] - 2024-12-18

### Added
- 三欄式布局、座位阻擋、統計、響應式

## [1.0.0] - 2024-12-17

### Added
- 初版 CSV、隨機分配、Python GUI

[Unreleased]: https://github.com/Donaldcpk/ultra-seat/compare/v2.2.0...HEAD
[2.2.0]: https://github.com/Donaldcpk/ultra-seat/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/Donaldcpk/ultra-seat/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/Donaldcpk/ultra-seat/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Donaldcpk/ultra-seat/releases/tag/v1.0.0

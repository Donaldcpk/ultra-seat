# Changelog

本專案遵循 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，版本號採 [Semantic Versioning](https://semver.org/lang/zh-TW/)。

## [Unreleased]

## [2.3.0] - 2026-08-27

### Added
- 週更／輪換：再次智能分配時優先換離上次座位（記憶於本機，依班別）；成功後顯示換位人數
- 分析 CSV：狀態、是否前排、左鄰、右鄰；含空位／阻擋列以便對應課室
- 分配檢查報告：每組不可同坐 → 已遵守／失敗；前排／SEN 未進前兩排會列出
- 班內範例自動加入 3 組不可同坐，方便示範

### Changed
- 智能分配按鈕標示「含週更」；隨機分配後若有限制亦顯示檢查報告

## [2.2.0] - 2026-08-27

### Added
- 班主任課室排位＋管理：A4 課室門海報列印（黑板、班名、日期、圖例）
- 課室模板存於 `localStorage`（名稱、行列、阻擋座位；不含學生名單）
- 港校 CSV：班別、班號／學號、姓名、職務、前排／SEN；相容舊 `學號,姓名,職務`
- 回溯法 + MRV 智能分配（約 40 人、數組不可同坐）；失敗訊息清楚
- 「進階（少用）」內可選梅花座／同組分散（非產品主軸）

### Changed
- 產品定位改為港校班主任課室管理面，而非考務／試場
- 格網上限維持課室尺度（12×12）
- README 繁中誠實功能表；拿掉考試為主的流程宣傳
- 介面文案全面繁中，不以英文 UI 為主

### Removed
- 依姓名推斷性別的使用
- README 中未實作的班幹部前排、性別均衡、最小間距宣傳
- 考試模式作為主介面切換（已降為進階勾選）

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

[Unreleased]: https://github.com/Donaldcpk/ultra-seat/compare/v2.3.0...HEAD
[2.3.0]: https://github.com/Donaldcpk/ultra-seat/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/Donaldcpk/ultra-seat/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/Donaldcpk/ultra-seat/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/Donaldcpk/ultra-seat/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/Donaldcpk/ultra-seat/releases/tag/v1.0.0

# 🎓 終極智能教室座位表生成器 (Ultra Seat)

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-brightgreen)](https://donaldcpk.github.io/ultra-seat/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v2.1.0-orange.svg)](https://github.com/Donaldcpk/ultra-seat/releases)

> 🚀 **立即體驗**: [https://donaldcpk.github.io/ultra-seat/](https://donaldcpk.github.io/ultra-seat/)

一個功能完整的智能教室座位表生成器，支援精準限制控制、智能約束分配和響應式設計。無需安裝任何軟體，開啟瀏覽器即可使用！

![Ultra Seat Preview](https://via.placeholder.com/800x400/4CAF50/FFFFFF?text=Ultra+Seat+Generator)

## ✨ 主要功能

### 🎯 核心功能
- **📊 CSV匯入匯出**: 支援學生名單批量匯入和座位表匯出
- **🏫 教室布局**: 自定義教室大小（2×2 到 12×12）
- **🎲 智能分配**: 使用約束滿足演算法進行最佳化分配
- **✋ 手動調整**: 拖拉式座位交換，即時調整
- **🚫 座位阻擋**: 設定特定座位為不可坐

### 🧠 精準限制控制
- **四周不可相鄰**: 包含對角線的完全隔離
- **左右不可相鄰**: 水平方向限制
- **前後不可相鄰**: 垂直方向限制
- **限制管理**: 可視化限制清單，支援單個刪除

### 📱 響應式設計
- **桌面版**: 三欄式布局，最佳使用體驗
- **平板版**: 自動調整為上下堆疊
- **手機版**: 優化觸控操作

## 🚀 快速開始

### 線上使用（推薦）
直接訪問：[https://donaldcpk.github.io/ultra-seat/](https://donaldcpk.github.io/ultra-seat/)

### 本地使用
1. 下載 `index.html` 文件
2. 雙擊開啟即可使用
3. 無需安裝任何軟體或依賴

## 📖 使用指南

### 1. 教室設定
```
1. 輸入班級名稱
2. 設定教室行數和列數
3. 點擊「建立教室」
```

### 2. 匯入學生資料
```
選項A: 點擊「建立範例資料」快速體驗
選項B: 準備CSV檔案後點擊「匯入學生資料」
```

### 3. 設定限制條件（可選）
```
1. 選擇第一個學生
2. 選擇限制類型（四周/左右/前後不可相鄰）
3. 選擇第二個學生
4. 點擊「新增限制」
```

### 4. 分配座位
```
🎲 隨機分配: 完全隨機分配（忽略限制）
🧠 智能分配: 嚴格遵守所有限制條件
```

### 5. 手動調整
```
1. 切換到「分配模式」
2. 點擊座位選中（粉紅色）
3. 再點擊另一座位進行交換
```

## 🎨 功能特色

### 智能約束滿足演算法
- 使用約束滿足問題(CSP)演算法
- 最多嘗試1000次找到最佳分配
- 100%遵守所有設定的限制條件

### 視覺化操作介面
- **座位狀態**：白色(空位)、藍色(已分配)、灰色(阻擋)、粉紅色(選中)
- **即時統計**：總學生數、已分配數、阻擋座位數、分配率
- **操作提示**：即時狀態提示和錯誤訊息

### 雙模式操作
- **分配模式**：分配學生座位、交換座位
- **阻擋模式**：設定座位為不可坐

## 📊 技術規格

### 支援範圍
- **教室大小**: 2×2 到 12×12
- **學生數量**: 無上限（受座位數限制）
- **檔案格式**: CSV (UTF-8編碼)
- **瀏覽器**: Chrome 60+, Firefox 55+, Safari 12+, Edge 79+

### 技術特點
- 純前端實現，無需後端服務
- 響應式設計，適應各種螢幕尺寸
- 記憶體使用最佳化
- 無網路連線需求

## 🎯 使用場景

### 教育場景
- **一般教室**: 智能分配 + 手動微調
- **實驗室**: 先阻擋設備區域，再分配座位
- **大型教室**: 設定限制條件保持適當距離
- **特殊需求**: 利用限制條件滿足特定要求

### 其他場景
- 會議室座位安排
- 活動場地規劃
- 考試座位分配
- 任何需要座位安排的場合

## 📁 專案結構

```
ultra-seat/
├── index.html              # 主頁面（完美版）
├── perfect_version.html     # 完美版備份
├── simple_main.py          # Python GUI版本
├── test_simple.py          # Python測試版本
├── PERFECT_GUIDE.md        # 完美版使用指南
├── WEB_GUIDE.md           # 網頁版使用指南
├── INSTALL.md             # Python版安裝指南
├── START_HERE.md          # 快速開始指南
├── development_log.md     # 開發日誌
├── requirements.txt       # Python依賴
├── run_gui.bat           # GUI啟動器
└── run_test.bat          # 測試啟動器
```

## 🔄 版本歷史

### v2.1.0 - 精準限制控制版 (2024-12-19)
- ✨ 全新限制系統：支援三種限制類型
- 🧠 智能約束滿足演算法
- 📏 座位表視覺優化：更大更清晰
- 🎛️ 限制管理功能：可視化管理

### v2.0.0 - 完美版 (2024-12-18)
- 🎨 全新三欄式布局
- 🚫 座位阻擋功能
- 📊 增強統計功能
- 📱 響應式設計優化

### v1.0.0 - 基礎版 (2024-12-17)
- 🎓 核心功能實現
- 📊 CSV匯入匯出
- 🎲 隨機分配功能
- 🖥️ Python GUI版本

## 🤝 貢獻指南

歡迎提交Issue和Pull Request！

### 開發環境設定
```bash
git clone https://github.com/Donaldcpk/ultra-seat.git
cd ultra-seat
# 直接開啟 index.html 即可開始開發
```

### 提交規範
- 🎨 `:art:` 改進代碼結構/格式
- ⚡ `:zap:` 提升性能
- 🐛 `:bug:` 修復bug
- ✨ `:sparkles:` 新功能
- 📝 `:memo:` 更新文檔

## 📄 授權條款

本專案採用 [MIT License](LICENSE) 授權。

## 📞 技術支援

- **GitHub Issues**: [提交問題](https://github.com/Donaldcpk/ultra-seat/issues)
- **功能建議**: [提交建議](https://github.com/Donaldcpk/ultra-seat/issues/new)
- **使用指南**: 查看 [PERFECT_GUIDE.md](PERFECT_GUIDE.md)

## 🌟 致謝

感謝所有使用者的回饋和建議，讓這個專案不斷改進！

---

⭐ 如果這個專案對您有幫助，請給我們一個星星！

**立即體驗**: [https://donaldcpk.github.io/ultra-seat/](https://donaldcpk.github.io/ultra-seat/) 
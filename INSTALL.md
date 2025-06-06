# 終極智能教室座位表生成器 - 安裝指南

## 系統需求
- Windows 10/11
- Python 3.7 或更高版本

## 安裝步驟

### 第一步：安裝Python

1. **下載Python**
   - 前往 [Python官方網站](https://www.python.org/downloads/)
   - 點擊 "Download Python 3.x.x" 按鈕下載最新版本

2. **安裝Python**
   - 執行下載的安裝檔
   - **重要**：勾選 "Add Python to PATH" 選項
   - 點擊 "Install Now" 進行安裝

3. **驗證安裝**
   - 開啟命令提示字元 (cmd) 或 PowerShell
   - 輸入 `python --version`
   - 應該顯示Python版本號

### 第二步：運行程式

#### 方法一：使用批次檔（推薦）

1. **測試版本**
   - 雙擊 `run_test.bat`
   - 程式會自動檢查Python環境並運行測試

2. **GUI版本**
   - 雙擊 `run_gui.bat`
   - 程式會啟動圖形化介面

#### 方法二：命令列運行

1. **開啟命令提示字元**
   - 按 Win+R，輸入 `cmd`，按Enter
   - 或在檔案總管中，按住Shift右鍵，選擇「在此處開啟PowerShell視窗」

2. **切換到專案目錄**
   ```
   cd C:\Users\user\Documents\Prog\seat
   ```

3. **運行程式**
   ```
   # 測試版本
   python test_simple.py
   
   # GUI版本
   python simple_main.py
   ```

## 程式功能說明

### 測試版本 (test_simple.py)
- 命令列介面
- 自動創建範例學生資料
- 演示基本座位分配功能
- 顯示座位表

### GUI版本 (simple_main.py)
- 圖形化使用者介面
- 支援CSV檔案匯入
- 互動式座位表顯示
- 完整的座位管理功能

## 使用流程

### 1. 準備學生資料
- 使用CSV格式
- 欄位：學號、姓名、職務
- 範例檔案會自動生成

### 2. 建立教室
- 設定教室行數和列數
- 輸入班級名稱

### 3. 匯入學生
- 選擇CSV檔案
- 系統會自動驗證資料

### 4. 分配座位
- 點擊「隨機分配」按鈕
- 或手動調整座位

### 5. 查看結果
- 座位表會即時更新
- 顯示統計資訊

## 常見問題

### Q: 雙擊批次檔沒有反應？
A: 請確認Python已正確安裝並加入PATH環境變數

### Q: 出現「無法辨識 'python' 詞彙」錯誤？
A: 
1. 重新安裝Python，確保勾選「Add Python to PATH」
2. 重新啟動電腦
3. 或使用完整路徑運行Python

### Q: 程式閃退？
A: 
1. 使用命令提示字元運行，查看錯誤訊息
2. 確認所有檔案都在同一目錄下
3. 檢查CSV檔案格式是否正確

### Q: 中文顯示亂碼？
A: 確保CSV檔案使用UTF-8編碼儲存

## 檔案說明

- `test_simple.py` - 測試版本程式
- `simple_main.py` - GUI版本程式
- `run_test.bat` - 測試版本啟動器
- `run_gui.bat` - GUI版本啟動器
- `sample_students.csv` - 範例學生資料（自動生成）
- `README.md` - 專案說明文件
- `development_log.md` - 開發日誌

## 技術支援

如果遇到問題，請檢查：
1. Python版本是否為3.7以上
2. 所有檔案是否在同一目錄
3. CSV檔案格式是否正確
4. 系統編碼設定

---
**版本**: v1.0.0
**更新日期**: 2024年12月 
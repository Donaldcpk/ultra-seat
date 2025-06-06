@echo off
echo 終極智能教室座位表生成器 - 測試版本
echo =====================================
echo.

REM 檢查Python是否安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤：未找到Python，請先安裝Python
    echo 請到 https://www.python.org/downloads/ 下載並安裝Python
    pause
    exit /b 1
)

echo 正在運行測試程式...
echo.
python test_simple.py

echo.
echo 程式執行完畢
pause 
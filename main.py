"""
終極智能教室座位表生成器
主程式入口
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# 新增 src 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.gui.main_window import MainWindow
except ImportError as e:
    print(f"匯入錯誤: {e}")
    print("請確保所有必要的套件都已安裝")
    print("執行: pip install -r requirements.txt")
    sys.exit(1)


def main():
    """主程式函數"""
    try:
        # 建立主視窗
        root = tk.Tk()
        app = MainWindow(root)
        
        # 設定視窗關閉事件
        def on_closing():
            if messagebox.askokcancel("退出", "確定要退出座位表生成器嗎？"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # 啟動主迴圈
        root.mainloop()
        
    except Exception as e:
        error_msg = f"程式啟動時發生錯誤: {str(e)}"
        print(error_msg)
        
        # 嘗試顯示錯誤對話框
        try:
            root = tk.Tk()
            root.withdraw()  # 隱藏主視窗
            messagebox.showerror("錯誤", error_msg)
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main() 
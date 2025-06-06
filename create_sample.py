"""
建立範例檔案的腳本
"""

import pandas as pd
import os

def create_sample_excel():
    """建立範例學生名單 Excel 檔案"""
    
    # 確保目錄存在
    os.makedirs('src/data', exist_ok=True)
    
    # 範例學生資料
    data = {
        '學號': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 
                'S009', 'S010', 'S011', 'S012', 'S013', 'S014', 'S015'],
        '姓名': ['王小明', '李小華', '張小美', '陳小強', '林小芳', '黃小龍', '吳小雯', '劉小傑',
                '蔡小玲', '鄭小偉', '楊小慧', '許小豪', '謝小婷', '周小宇', '蘇小琪'],
        '職務': ['班長', '副班長', '學藝股長', '', '風紀股長', '', '體育股長', '',
                '衛生股長', '', '總務股長', '', '康樂股長', '', '']
    }
    
    df = pd.DataFrame(data)
    
    # 儲存到 Excel 檔案
    file_path = 'src/data/sample_students.xlsx'
    df.to_excel(file_path, index=False)
    
    print(f"範例檔案已建立: {file_path}")
    print("檔案內容:")
    print(df.to_string(index=False))

if __name__ == "__main__":
    create_sample_excel() 
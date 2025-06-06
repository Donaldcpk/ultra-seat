"""
簡化版檔案處理工具
使用 CSV 格式，不依賴 pandas 和 openpyxl
"""

import csv
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from ..core.student import Student
from ..core.classroom import Classroom


class SimpleFileHandler:
    """
    簡化版檔案處理工具類別
    
    提供 CSV 檔案讀寫、JSON 資料處理等功能
    """
    
    @staticmethod
    def read_student_csv(file_path: str) -> Tuple[List[Student], List[str]]:
        """
        從 CSV 檔案讀取學生資料
        
        參數:
            file_path (str): CSV 檔案路徑
            
        回傳:
            Tuple[List[Student], List[str]]: (學生清單, 錯誤訊息清單)
        """
        students = []
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                # 讀取標題行
                headers = next(reader, None)
                if not headers:
                    errors.append("CSV 檔案為空")
                    return students, errors
                
                # 檢查必要欄位
                if len(headers) < 2:
                    errors.append("CSV 檔案至少需要兩欄（學號、姓名）")
                    return students, errors
                
                seen_ids = set()
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        if len(row) < 2:
                            continue  # 跳過空行或不完整的行
                        
                        # 讀取基本資料
                        student_id = row[0].strip() if row[0] else ""
                        name = row[1].strip() if row[1] else ""
                        position = row[2].strip() if len(row) > 2 and row[2] else ""
                        
                        # 驗證資料
                        if not student_id:
                            errors.append(f"第 {row_num} 行：學號不能為空")
                            continue
                        
                        if not name:
                            errors.append(f"第 {row_num} 行：姓名不能為空")
                            continue
                        
                        # 檢查學號唯一性
                        if student_id in seen_ids:
                            errors.append(f"第 {row_num} 行：學號 {student_id} 重複")
                            continue
                        
                        seen_ids.add(student_id)
                        
                        # 建立學生物件
                        student = Student(
                            student_id=student_id,
                            name=name,
                            position=position
                        )
                        
                        students.append(student)
                        
                    except Exception as e:
                        errors.append(f"第 {row_num} 行：處理資料時發生錯誤 - {str(e)}")
                
        except FileNotFoundError:
            errors.append(f"找不到檔案: {file_path}")
        except Exception as e:
            errors.append(f"讀取檔案時發生錯誤: {str(e)}")
        
        return students, errors
    
    @staticmethod
    def export_seating_chart_csv(classroom: Classroom, file_path: str) -> List[str]:
        """
        匯出座位表到 CSV 檔案
        
        參數:
            classroom (Classroom): 教室物件
            file_path (str): 輸出檔案路徑
            
        回傳:
            List[str]: 錯誤訊息清單
        """
        errors = []
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # 寫入標題
                writer.writerow(['學號', '姓名', '職務', '座位行', '座位列'])
                
                # 寫入學生資料
                for student in classroom.students.values():
                    row_data = [
                        student.student_id,
                        student.name,
                        student.position,
                        student.row + 1 if student.row is not None else '',
                        student.col + 1 if student.col is not None else ''
                    ]
                    writer.writerow(row_data)
            
        except Exception as e:
            errors.append(f"匯出 CSV 檔案時發生錯誤: {str(e)}")
        
        return errors
    
    @staticmethod
    def save_classroom_json(classroom: Classroom, file_path: str) -> List[str]:
        """
        儲存教室資料到 JSON 檔案
        
        參數:
            classroom (Classroom): 教室物件
            file_path (str): 檔案路徑
            
        回傳:
            List[str]: 錯誤訊息清單
        """
        errors = []
        
        try:
            # 確保目錄存在
            directory = os.path.dirname(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            # 轉換為字典格式
            data = classroom.to_dict()
            
            # 儲存到 JSON 檔案
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            errors.append(f"儲存 JSON 檔案時發生錯誤: {str(e)}")
        
        return errors
    
    @staticmethod
    def load_classroom_json(file_path: str) -> Tuple[Optional[Classroom], List[str]]:
        """
        從 JSON 檔案載入教室資料
        
        參數:
            file_path (str): 檔案路徑
            
        回傳:
            Tuple[Optional[Classroom], List[str]]: (教室物件, 錯誤訊息清單)
        """
        classroom = None
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            classroom = Classroom.from_dict(data)
            
        except FileNotFoundError:
            errors.append(f"找不到檔案: {file_path}")
        except json.JSONDecodeError as e:
            errors.append(f"JSON 格式錯誤: {str(e)}")
        except Exception as e:
            errors.append(f"載入檔案時發生錯誤: {str(e)}")
        
        return classroom, errors
    
    @staticmethod
    def create_sample_csv(file_path: str) -> List[str]:
        """
        建立範例 CSV 檔案
        
        參數:
            file_path (str): 輸出檔案路徑
            
        回傳:
            List[str]: 錯誤訊息清單
        """
        errors = []
        
        try:
            # 確保目錄存在
            directory = os.path.dirname(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # 寫入標題
                writer.writerow(['學號', '姓名', '職務'])
                
                # 寫入範例資料
                sample_data = [
                    ['S001', '王小明', '班長'],
                    ['S002', '李小華', '副班長'],
                    ['S003', '張小美', '學藝股長'],
                    ['S004', '陳小強', ''],
                    ['S005', '林小芳', '風紀股長'],
                    ['S006', '黃小龍', ''],
                    ['S007', '吳小雯', '體育股長'],
                    ['S008', '劉小傑', ''],
                    ['S009', '蔡小玲', '衛生股長'],
                    ['S010', '鄭小偉', ''],
                    ['S011', '楊小慧', '總務股長'],
                    ['S012', '許小豪', ''],
                    ['S013', '謝小婷', '康樂股長'],
                    ['S014', '周小宇', ''],
                    ['S015', '蘇小琪', '']
                ]
                
                for row in sample_data:
                    writer.writerow(row)
            
        except Exception as e:
            errors.append(f"建立範例檔案時發生錯誤: {str(e)}")
        
        return errors 
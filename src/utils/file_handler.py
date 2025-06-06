"""
檔案處理工具
負責 Excel 檔案讀寫、JSON 資料處理等檔案操作
"""

import pandas as pd
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from ..core.student import Student
from ..core.classroom import Classroom


class FileHandler:
    """
    檔案處理工具類別
    
    提供 Excel 檔案讀寫、JSON 資料處理等功能
    """
    
    @staticmethod
    def read_student_excel(file_path: str, format_type: int = 1) -> Tuple[List[Student], List[str]]:
        """
        從 Excel 檔案讀取學生資料
        
        參數:
            file_path (str): Excel 檔案路徑
            format_type (int): 格式類型 (1: 標準格式, 2: 座位表記錄格式)
            
        回傳:
            Tuple[List[Student], List[str]]: (學生清單, 錯誤訊息清單)
        """
        students = []
        errors = []
        
        try:
            # 讀取 Excel 檔案
            df = pd.read_excel(file_path)
            
            if format_type == 1:
                # 標準格式：學號、姓名、職務
                students, errors = FileHandler._parse_standard_format(df)
            elif format_type == 2:
                # 座位表記錄格式：學號、姓名、職務、座位行、座位列
                students, errors = FileHandler._parse_seating_record_format(df)
            else:
                errors.append("不支援的檔案格式類型")
                
        except FileNotFoundError:
            errors.append(f"找不到檔案: {file_path}")
        except Exception as e:
            errors.append(f"讀取檔案時發生錯誤: {str(e)}")
        
        return students, errors
    
    @staticmethod
    def _parse_standard_format(df: pd.DataFrame) -> Tuple[List[Student], List[str]]:
        """
        解析標準格式的學生資料
        
        參數:
            df (pd.DataFrame): 資料框
            
        回傳:
            Tuple[List[Student], List[str]]: (學生清單, 錯誤訊息清單)
        """
        students = []
        errors = []
        
        # 檢查欄位數量
        if len(df.columns) < 2:
            errors.append("Excel 檔案至少需要兩欄（學號、姓名）")
            return students, errors
        
        # 設定欄位名稱
        column_names = ['student_id', 'name', 'position']
        for i, col_name in enumerate(column_names):
            if i < len(df.columns):
                df.columns.values[i] = col_name
        
        # 如果沒有職務欄，新增空白職務欄
        if 'position' not in df.columns:
            df['position'] = ''
        
        seen_ids = set()
        
        for index, row in df.iterrows():
            try:
                # 檢查必要欄位
                student_id = str(row['student_id']).strip()
                name = str(row['name']).strip()
                position = str(row.get('position', '')).strip()
                
                # 驗證資料
                if not student_id or student_id == 'nan':
                    errors.append(f"第 {index + 2} 行：學號不能為空")
                    continue
                
                if not name or name == 'nan':
                    errors.append(f"第 {index + 2} 行：姓名不能為空")
                    continue
                
                # 檢查學號唯一性
                if student_id in seen_ids:
                    errors.append(f"第 {index + 2} 行：學號 {student_id} 重複")
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
                errors.append(f"第 {index + 2} 行：處理資料時發生錯誤 - {str(e)}")
        
        return students, errors
    
    @staticmethod
    def _parse_seating_record_format(df: pd.DataFrame) -> Tuple[List[Student], List[str]]:
        """
        解析座位表記錄格式的學生資料
        
        參數:
            df (pd.DataFrame): 資料框
            
        回傳:
            Tuple[List[Student], List[str]]: (學生清單, 錯誤訊息清單)
        """
        students = []
        errors = []
        
        # 檢查欄位數量
        if len(df.columns) < 5:
            errors.append("座位表記錄格式需要五欄（學號、姓名、職務、座位行、座位列）")
            return students, errors
        
        # 設定欄位名稱
        column_names = ['student_id', 'name', 'position', 'row', 'col']
        for i, col_name in enumerate(column_names):
            if i < len(df.columns):
                df.columns.values[i] = col_name
        
        seen_ids = set()
        
        for index, row in df.iterrows():
            try:
                # 檢查必要欄位
                student_id = str(row['student_id']).strip()
                name = str(row['name']).strip()
                position = str(row.get('position', '')).strip()
                
                # 驗證基本資料
                if not student_id or student_id == 'nan':
                    errors.append(f"第 {index + 2} 行：學號不能為空")
                    continue
                
                if not name or name == 'nan':
                    errors.append(f"第 {index + 2} 行：姓名不能為空")
                    continue
                
                # 檢查學號唯一性
                if student_id in seen_ids:
                    errors.append(f"第 {index + 2} 行：學號 {student_id} 重複")
                    continue
                
                seen_ids.add(student_id)
                
                # 處理座位資訊
                row_val = row.get('row')
                col_val = row.get('col')
                
                seat_row = None
                seat_col = None
                
                if pd.notna(row_val) and pd.notna(col_val):
                    try:
                        seat_row = int(row_val) - 1  # 轉換為 0-based index
                        seat_col = int(col_val) - 1  # 轉換為 0-based index
                        
                        if seat_row < 0 or seat_col < 0:
                            errors.append(f"第 {index + 2} 行：座位行列號必須大於 0")
                            seat_row = seat_col = None
                            
                    except ValueError:
                        errors.append(f"第 {index + 2} 行：座位行列號必須為數字")
                
                # 建立學生物件
                student = Student(
                    student_id=student_id,
                    name=name,
                    position=position,
                    row=seat_row,
                    col=seat_col
                )
                
                students.append(student)
                
            except Exception as e:
                errors.append(f"第 {index + 2} 行：處理資料時發生錯誤 - {str(e)}")
        
        return students, errors
    
    @staticmethod
    def export_seating_chart_excel(classroom: Classroom, file_path: str) -> List[str]:
        """
        匯出座位表到 Excel 檔案
        
        參數:
            classroom (Classroom): 教室物件
            file_path (str): 輸出檔案路徑
            
        回傳:
            List[str]: 錯誤訊息清單
        """
        errors = []
        
        try:
            # 準備資料
            data = []
            for student in classroom.students.values():
                row_data = {
                    '學號': student.student_id,
                    '姓名': student.name,
                    '職務': student.position,
                    '座位行': student.row + 1 if student.row is not None else '',
                    '座位列': student.col + 1 if student.col is not None else ''
                }
                data.append(row_data)
            
            # 建立 DataFrame
            df = pd.DataFrame(data)
            
            # 匯出到 Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # 學生清單工作表
                df.to_excel(writer, sheet_name='學生座位表', index=False)
                
                # 座位矩陣工作表
                seat_matrix = classroom.get_seat_matrix()
                matrix_df = pd.DataFrame(seat_matrix)
                matrix_df.to_excel(writer, sheet_name='座位矩陣', index=False, header=False)
                
                # 教室資訊工作表
                info_data = {
                    '項目': ['班級名稱', '教室行數', '教室列數', '學生總數', '已分配座位', '可用座位', '阻擋座位'],
                    '值': [
                        classroom.class_name,
                        classroom.rows,
                        classroom.cols,
                        len(classroom.students),
                        len([s for s in classroom.students.values() if s.has_seat]),
                        len(classroom.get_available_seats()),
                        len(classroom.blocked_seats)
                    ]
                }
                info_df = pd.DataFrame(info_data)
                info_df.to_excel(writer, sheet_name='教室資訊', index=False)
            
        except Exception as e:
            errors.append(f"匯出 Excel 檔案時發生錯誤: {str(e)}")
        
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
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
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
    def get_recent_files(data_dir: str = "src/data", max_files: int = 10) -> List[Dict[str, Any]]:
        """
        取得最近使用的檔案清單
        
        參數:
            data_dir (str): 資料目錄路徑
            max_files (int): 最大檔案數量
            
        回傳:
            List[Dict[str, Any]]: 檔案資訊清單
        """
        recent_files = []
        
        try:
            if not os.path.exists(data_dir):
                return recent_files
            
            # 取得所有 JSON 檔案
            json_files = []
            for file_name in os.listdir(data_dir):
                if file_name.endswith('.json'):
                    file_path = os.path.join(data_dir, file_name)
                    if os.path.isfile(file_path):
                        stat = os.stat(file_path)
                        json_files.append({
                            'name': file_name,
                            'path': file_path,
                            'modified_time': stat.st_mtime,
                            'size': stat.st_size
                        })
            
            # 按修改時間排序
            json_files.sort(key=lambda x: x['modified_time'], reverse=True)
            
            # 取得前 N 個檔案
            recent_files = json_files[:max_files]
            
            # 格式化時間
            import datetime
            for file_info in recent_files:
                file_info['modified_time_str'] = datetime.datetime.fromtimestamp(
                    file_info['modified_time']
                ).strftime('%Y-%m-%d %H:%M:%S')
                
        except Exception as e:
            print(f"取得最近檔案時發生錯誤: {str(e)}")
        
        return recent_files
    
    @staticmethod
    def create_sample_excel(file_path: str, format_type: int = 1) -> List[str]:
        """
        建立範例 Excel 檔案
        
        參數:
            file_path (str): 輸出檔案路徑
            format_type (int): 格式類型 (1: 標準格式, 2: 座位表記錄格式)
            
        回傳:
            List[str]: 錯誤訊息清單
        """
        errors = []
        
        try:
            if format_type == 1:
                # 標準格式範例
                data = {
                    '學號': ['S001', 'S002', 'S003', 'S004', 'S005'],
                    '姓名': ['王小明', '李小華', '張小美', '陳小強', '林小芳'],
                    '職務': ['班長', '副班長', '學藝股長', '', '風紀股長']
                }
            else:
                # 座位表記錄格式範例
                data = {
                    '學號': ['S001', 'S002', 'S003', 'S004', 'S005'],
                    '姓名': ['王小明', '李小華', '張小美', '陳小強', '林小芳'],
                    '職務': ['班長', '副班長', '學藝股長', '', '風紀股長'],
                    '座位行': [1, 1, 2, 2, 3],
                    '座位列': [1, 2, 1, 2, 1]
                }
            
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            
        except Exception as e:
            errors.append(f"建立範例檔案時發生錯誤: {str(e)}")
        
        return errors 
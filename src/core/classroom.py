"""
教室布局模型
定義教室的座位布局和相關操作
"""

from typing import List, Tuple, Optional, Dict, Any, Set
from .student import Student


class Classroom:
    """
    教室布局類別
    
    管理教室的座位布局、學生分配和座位限制
    """
    
    def __init__(self, rows: int, cols: int, class_name: str = ""):
        """
        初始化教室
        
        參數:
            rows (int): 教室行數
            cols (int): 教室列數
            class_name (str): 班級名稱
        """
        self.rows = rows
        self.cols = cols
        self.class_name = class_name
        
        # 座位網格：None 表示空座位，Student 物件表示已分配
        self.seats: List[List[Optional[Student]]] = [
            [None for _ in range(cols)] for _ in range(rows)
        ]
        
        # 不可坐的座位位置集合
        self.blocked_seats: Set[Tuple[int, int]] = set()
        
        # 學生清單
        self.students: Dict[str, Student] = {}
    
    def add_student(self, student: Student) -> bool:
        """
        新增學生到教室
        
        參數:
            student (Student): 學生物件
            
        回傳:
            bool: 是否成功新增
        """
        if student.student_id in self.students:
            return False  # 學號已存在
        
        self.students[student.student_id] = student
        return True
    
    def remove_student(self, student_id: str) -> bool:
        """
        從教室移除學生
        
        參數:
            student_id (str): 學號
            
        回傳:
            bool: 是否成功移除
        """
        if student_id not in self.students:
            return False
        
        student = self.students[student_id]
        if student.has_seat:
            self.clear_seat(student.row, student.col)
        
        del self.students[student_id]
        return True
    
    def get_student(self, student_id: str) -> Optional[Student]:
        """
        取得學生物件
        
        參數:
            student_id (str): 學號
            
        回傳:
            Optional[Student]: 學生物件或 None
        """
        return self.students.get(student_id)
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """
        檢查座位位置是否有效
        
        參數:
            row (int): 行號
            col (int): 列號
            
        回傳:
            bool: 位置是否有效
        """
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def is_seat_available(self, row: int, col: int) -> bool:
        """
        檢查座位是否可用
        
        參數:
            row (int): 行號
            col (int): 列號
            
        回傳:
            bool: 座位是否可用
        """
        if not self.is_valid_position(row, col):
            return False
        
        if (row, col) in self.blocked_seats:
            return False
        
        return self.seats[row][col] is None
    
    def assign_seat(self, student_id: str, row: int, col: int) -> bool:
        """
        分配座位給學生
        
        參數:
            student_id (str): 學號
            row (int): 行號
            col (int): 列號
            
        回傳:
            bool: 是否成功分配
        """
        if student_id not in self.students:
            return False
        
        if not self.is_seat_available(row, col):
            return False
        
        student = self.students[student_id]
        
        # 如果學生已有座位，先清除
        if student.has_seat:
            self.clear_seat(student.row, student.col)
        
        # 分配新座位
        self.seats[row][col] = student
        student.assign_seat(row, col)
        return True
    
    def clear_seat(self, row: int, col: int) -> bool:
        """
        清除座位
        
        參數:
            row (int): 行號
            col (int): 列號
            
        回傳:
            bool: 是否成功清除
        """
        if not self.is_valid_position(row, col):
            return False
        
        if self.seats[row][col] is not None:
            student = self.seats[row][col]
            student.clear_seat()
            self.seats[row][col] = None
            return True
        
        return False
    
    def swap_seats(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """
        交換兩個座位的學生
        
        參數:
            pos1 (Tuple[int, int]): 第一個座位位置
            pos2 (Tuple[int, int]): 第二個座位位置
            
        回傳:
            bool: 是否成功交換
        """
        row1, col1 = pos1
        row2, col2 = pos2
        
        if not (self.is_valid_position(row1, col1) and self.is_valid_position(row2, col2)):
            return False
        
        # 檢查是否有被阻擋的座位
        if (row1, col1) in self.blocked_seats or (row2, col2) in self.blocked_seats:
            return False
        
        student1 = self.seats[row1][col1]
        student2 = self.seats[row2][col2]
        
        # 交換座位
        self.seats[row1][col1] = student2
        self.seats[row2][col2] = student1
        
        # 更新學生的座位資訊
        if student1:
            student1.assign_seat(row2, col2)
        if student2:
            student2.assign_seat(row1, col1)
        
        return True
    
    def block_seat(self, row: int, col: int) -> bool:
        """
        阻擋座位（設為不可坐）
        
        參數:
            row (int): 行號
            col (int): 列號
            
        回傳:
            bool: 是否成功阻擋
        """
        if not self.is_valid_position(row, col):
            return False
        
        # 如果座位有學生，先清除
        if self.seats[row][col] is not None:
            self.clear_seat(row, col)
        
        self.blocked_seats.add((row, col))
        return True
    
    def unblock_seat(self, row: int, col: int) -> bool:
        """
        解除座位阻擋
        
        參數:
            row (int): 行號
            col (int): 列號
            
        回傳:
            bool: 是否成功解除
        """
        if (row, col) in self.blocked_seats:
            self.blocked_seats.remove((row, col))
            return True
        return False
    
    def get_available_seats(self) -> List[Tuple[int, int]]:
        """
        取得所有可用座位位置
        
        回傳:
            List[Tuple[int, int]]: 可用座位位置清單
        """
        available = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_seat_available(row, col):
                    available.append((row, col))
        return available
    
    def get_occupied_seats(self) -> List[Tuple[int, int]]:
        """
        取得所有已佔用座位位置
        
        回傳:
            List[Tuple[int, int]]: 已佔用座位位置清單
        """
        occupied = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.seats[row][col] is not None:
                    occupied.append((row, col))
        return occupied
    
    def get_unassigned_students(self) -> List[Student]:
        """
        取得未分配座位的學生
        
        回傳:
            List[Student]: 未分配座位的學生清單
        """
        return [student for student in self.students.values() if not student.has_seat]
    
    def clear_all_seats(self) -> None:
        """清除所有座位分配"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.seats[row][col] is not None:
                    self.seats[row][col].clear_seat()
                    self.seats[row][col] = None
    
    def get_seat_matrix(self) -> List[List[Optional[str]]]:
        """
        取得座位矩陣（學生姓名）
        
        回傳:
            List[List[Optional[str]]]: 座位矩陣
        """
        matrix = []
        for row in range(self.rows):
            row_data = []
            for col in range(self.cols):
                if (row, col) in self.blocked_seats:
                    row_data.append("X")  # 阻擋的座位
                elif self.seats[row][col] is not None:
                    row_data.append(self.seats[row][col].name)
                else:
                    row_data.append(None)  # 空座位
            matrix.append(row_data)
        return matrix
    
    def to_dict(self) -> Dict[str, Any]:
        """
        將教室資料轉換為字典格式
        
        回傳:
            Dict[str, Any]: 教室資料字典
        """
        return {
            'rows': self.rows,
            'cols': self.cols,
            'class_name': self.class_name,
            'blocked_seats': list(self.blocked_seats),
            'students': {sid: student.to_dict() for sid, student in self.students.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Classroom':
        """
        從字典建立教室物件
        
        參數:
            data (Dict[str, Any]): 教室資料字典
            
        回傳:
            Classroom: 教室物件
        """
        classroom = cls(
            rows=data['rows'],
            cols=data['cols'],
            class_name=data.get('class_name', '')
        )
        
        # 設定阻擋的座位
        for row, col in data.get('blocked_seats', []):
            classroom.block_seat(row, col)
        
        # 新增學生並分配座位
        for student_data in data.get('students', {}).values():
            student = Student.from_dict(student_data)
            classroom.add_student(student)
            
            if student.has_seat:
                classroom.assign_seat(student.student_id, student.row, student.col)
        
        return classroom
    
    def __str__(self) -> str:
        """字串表示"""
        return f"教室 {self.class_name} ({self.rows}x{self.cols}) - {len(self.students)} 位學生" 
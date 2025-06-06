"""
座位管理器
負責座位分配、歷史記錄、條件檢查等核心功能
"""

import random
import copy
from typing import List, Dict, Any, Optional, Tuple
from .classroom import Classroom
from .student import Student


class SeatManager:
    """
    座位管理器類別
    
    負責管理座位分配、歷史記錄和條件檢查
    """
    
    def __init__(self, classroom: Classroom):
        """
        初始化座位管理器
        
        參數:
            classroom (Classroom): 教室物件
        """
        self.classroom = classroom
        self.history: List[Dict[str, Any]] = []  # 操作歷史記錄
        self.max_history = 50  # 最大歷史記錄數量
    
    def save_state(self, operation: str) -> None:
        """
        儲存當前狀態到歷史記錄
        
        參數:
            operation (str): 操作描述
        """
        state = {
            'operation': operation,
            'classroom_state': self.classroom.to_dict(),
            'timestamp': self._get_timestamp()
        }
        
        self.history.append(state)
        
        # 限制歷史記錄數量
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def undo(self) -> bool:
        """
        撤銷上一次操作
        
        回傳:
            bool: 是否成功撤銷
        """
        if len(self.history) < 2:
            return False
        
        # 移除當前狀態
        self.history.pop()
        
        # 恢復到上一個狀態
        previous_state = self.history[-1]
        self.classroom = Classroom.from_dict(previous_state['classroom_state'])
        
        return True
    
    def random_assign(self, seed: Optional[int] = None) -> bool:
        """
        隨機分配所有學生座位
        
        參數:
            seed (Optional[int]): 隨機種子，用於重現結果
            
        回傳:
            bool: 是否成功分配
        """
        # 儲存當前狀態
        self.save_state("隨機分配前")
        
        # 設定隨機種子
        if seed is not None:
            random.seed(seed)
        
        # 清除所有現有座位分配
        self.classroom.clear_all_seats()
        
        # 取得可用座位和未分配學生
        available_seats = self.classroom.get_available_seats()
        unassigned_students = list(self.classroom.students.values())
        
        # 檢查座位數量是否足夠
        if len(available_seats) < len(unassigned_students):
            return False
        
        # 隨機打亂座位和學生順序
        random.shuffle(available_seats)
        random.shuffle(unassigned_students)
        
        # 分配座位
        success_count = 0
        for i, student in enumerate(unassigned_students):
            if i < len(available_seats):
                row, col = available_seats[i]
                if self._can_assign_seat(student, row, col):
                    self.classroom.assign_seat(student.student_id, row, col)
                    success_count += 1
        
        # 儲存分配後狀態
        self.save_state(f"隨機分配完成 - 成功分配 {success_count} 位學生")
        
        return success_count == len(unassigned_students)
    
    def manual_assign(self, student_id: str, row: int, col: int) -> bool:
        """
        手動分配學生座位
        
        參數:
            student_id (str): 學號
            row (int): 行號
            col (int): 列號
            
        回傳:
            bool: 是否成功分配
        """
        student = self.classroom.get_student(student_id)
        if not student:
            return False
        
        if not self._can_assign_seat(student, row, col):
            return False
        
        # 儲存當前狀態
        self.save_state(f"手動分配前 - {student.name}")
        
        # 分配座位
        success = self.classroom.assign_seat(student_id, row, col)
        
        if success:
            self.save_state(f"手動分配 - {student.name} 到 ({row+1}, {col+1})")
        
        return success
    
    def swap_students(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """
        交換兩個位置的學生
        
        參數:
            pos1 (Tuple[int, int]): 第一個位置
            pos2 (Tuple[int, int]): 第二個位置
            
        回傳:
            bool: 是否成功交換
        """
        row1, col1 = pos1
        row2, col2 = pos2
        
        # 取得兩個位置的學生
        student1 = self.classroom.seats[row1][col1] if self.classroom.is_valid_position(row1, col1) else None
        student2 = self.classroom.seats[row2][col2] if self.classroom.is_valid_position(row2, col2) else None
        
        # 檢查交換後是否符合限制條件
        if student1 and not self._can_assign_seat(student1, row2, col2):
            return False
        if student2 and not self._can_assign_seat(student2, row1, col1):
            return False
        
        # 儲存當前狀態
        name1 = student1.name if student1 else "空位"
        name2 = student2.name if student2 else "空位"
        self.save_state(f"交換前 - {name1} 與 {name2}")
        
        # 執行交換
        success = self.classroom.swap_seats(pos1, pos2)
        
        if success:
            self.save_state(f"交換完成 - {name1} 與 {name2}")
        
        return success
    
    def reset_all(self) -> None:
        """重置所有座位分配"""
        self.save_state("重置前")
        self.classroom.clear_all_seats()
        self.save_state("重置完成")
    
    def _can_assign_seat(self, student: Student, row: int, col: int) -> bool:
        """
        檢查學生是否可以分配到指定座位
        
        參數:
            student (Student): 學生物件
            row (int): 行號
            col (int): 列號
            
        回傳:
            bool: 是否可以分配
        """
        # 基本位置檢查
        if not self.classroom.is_seat_available(row, col):
            # 如果是學生自己的座位，允許
            if self.classroom.seats[row][col] == student:
                return True
            return False
        
        # 檢查學生的限制條件
        constraints = student.constraints
        
        # 檢查禁止的特定位置
        if 'forbidden_positions' in constraints:
            if (row, col) in constraints['forbidden_positions']:
                return False
        
        # 檢查禁止的行
        if 'forbidden_rows' in constraints:
            if row in constraints['forbidden_rows']:
                return False
        
        # 檢查禁止的列
        if 'forbidden_cols' in constraints:
            if col in constraints['forbidden_cols']:
                return False
        
        # 檢查角落限制
        if 'no_corner' in constraints and constraints['no_corner']:
            if self._is_corner_seat(row, col):
                return False
        
        # 檢查相鄰限制
        if 'forbidden_adjacent' in constraints:
            for forbidden_student_id in constraints['forbidden_adjacent']:
                if self._is_adjacent_to_student(row, col, forbidden_student_id):
                    return False
        
        # 檢查左右相鄰限制
        if 'forbidden_horizontal' in constraints:
            for forbidden_student_id in constraints['forbidden_horizontal']:
                if self._is_horizontally_adjacent_to_student(row, col, forbidden_student_id):
                    return False
        
        # 檢查前後相鄰限制
        if 'forbidden_vertical' in constraints:
            for forbidden_student_id in constraints['forbidden_vertical']:
                if self._is_vertically_adjacent_to_student(row, col, forbidden_student_id):
                    return False
        
        return True
    
    def _is_corner_seat(self, row: int, col: int) -> bool:
        """檢查是否為角落座位"""
        return ((row == 0 or row == self.classroom.rows - 1) and 
                (col == 0 or col == self.classroom.cols - 1))
    
    def _is_adjacent_to_student(self, row: int, col: int, student_id: str) -> bool:
        """檢查是否與指定學生相鄰（八個方向）"""
        student = self.classroom.get_student(student_id)
        if not student or not student.has_seat:
            return False
        
        student_row, student_col = student.row, student.col
        
        # 檢查八個方向
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if student_row + dr == row and student_col + dc == col:
                    return True
        
        return False
    
    def _is_horizontally_adjacent_to_student(self, row: int, col: int, student_id: str) -> bool:
        """檢查是否與指定學生左右相鄰"""
        student = self.classroom.get_student(student_id)
        if not student or not student.has_seat:
            return False
        
        student_row, student_col = student.row, student.col
        
        # 檢查左右相鄰
        return (student_row == row and abs(student_col - col) == 1)
    
    def _is_vertically_adjacent_to_student(self, row: int, col: int, student_id: str) -> bool:
        """檢查是否與指定學生前後相鄰"""
        student = self.classroom.get_student(student_id)
        if not student or not student.has_seat:
            return False
        
        student_row, student_col = student.row, student.col
        
        # 檢查前後相鄰
        return (student_col == col and abs(student_row - row) == 1)
    
    def validate_all_constraints(self) -> List[str]:
        """
        驗證所有學生的座位是否符合限制條件
        
        回傳:
            List[str]: 違反限制的錯誤訊息清單
        """
        errors = []
        
        for student in self.classroom.students.values():
            if student.has_seat:
                if not self._can_assign_seat(student, student.row, student.col):
                    errors.append(f"{student.name} 的座位 ({student.row+1}, {student.col+1}) 違反限制條件")
        
        return errors
    
    def get_constraint_conflicts(self) -> Dict[str, List[str]]:
        """
        取得所有限制條件衝突
        
        回傳:
            Dict[str, List[str]]: 學生ID對應的衝突清單
        """
        conflicts = {}
        
        for student in self.classroom.students.values():
            student_conflicts = []
            
            if student.has_seat:
                # 檢查各種限制條件
                constraints = student.constraints
                
                if 'forbidden_positions' in constraints:
                    if (student.row, student.col) in constraints['forbidden_positions']:
                        student_conflicts.append("坐在禁止的位置")
                
                if 'forbidden_rows' in constraints:
                    if student.row in constraints['forbidden_rows']:
                        student_conflicts.append(f"坐在禁止的第 {student.row+1} 行")
                
                if 'forbidden_cols' in constraints:
                    if student.col in constraints['forbidden_cols']:
                        student_conflicts.append(f"坐在禁止的第 {student.col+1} 列")
                
                if 'no_corner' in constraints and constraints['no_corner']:
                    if self._is_corner_seat(student.row, student.col):
                        student_conflicts.append("坐在角落位置")
                
                # 檢查相鄰限制
                if 'forbidden_adjacent' in constraints:
                    for forbidden_id in constraints['forbidden_adjacent']:
                        if self._is_adjacent_to_student(student.row, student.col, forbidden_id):
                            forbidden_student = self.classroom.get_student(forbidden_id)
                            if forbidden_student:
                                student_conflicts.append(f"與 {forbidden_student.name} 相鄰")
            
            if student_conflicts:
                conflicts[student.student_id] = student_conflicts
        
        return conflicts
    
    def _get_timestamp(self) -> str:
        """取得當前時間戳記"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_history_summary(self) -> List[str]:
        """
        取得歷史記錄摘要
        
        回傳:
            List[str]: 歷史記錄摘要清單
        """
        return [f"{record['timestamp']} - {record['operation']}" for record in self.history]
    
    def clear_history(self) -> None:
        """清除所有歷史記錄"""
        self.history.clear()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        取得座位分配統計資訊
        
        回傳:
            Dict[str, Any]: 統計資訊
        """
        total_students = len(self.classroom.students)
        assigned_students = len([s for s in self.classroom.students.values() if s.has_seat])
        available_seats = len(self.classroom.get_available_seats())
        blocked_seats = len(self.classroom.blocked_seats)
        total_seats = self.classroom.rows * self.classroom.cols
        
        return {
            'total_students': total_students,
            'assigned_students': assigned_students,
            'unassigned_students': total_students - assigned_students,
            'total_seats': total_seats,
            'available_seats': available_seats,
            'occupied_seats': assigned_students,
            'blocked_seats': blocked_seats,
            'assignment_rate': (assigned_students / total_students * 100) if total_students > 0 else 0
        } 
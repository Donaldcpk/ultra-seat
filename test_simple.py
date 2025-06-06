#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
終極智能教室座位表生成器 - 測試版本
用於驗證基本功能是否正常
"""

import csv
import os
import random
from typing import List, Dict, Optional, Tuple

class Student:
    """學生資料類別"""
    def __init__(self, student_id: str, name: str, position: str = ""):
        self.student_id = student_id
        self.name = name
        self.position = position
        self.row = None
        self.col = None
    
    def has_seat(self) -> bool:
        return self.row is not None and self.col is not None
    
    def assign_seat(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
    
    def clear_seat(self) -> None:
        self.row = None
        self.col = None
    
    def __str__(self):
        seat_info = f"({self.row},{self.col})" if self.has_seat() else "未分配"
        return f"{self.student_id} {self.name} {self.position} {seat_info}"

class Classroom:
    """教室布局類別"""
    def __init__(self, rows: int, cols: int, class_name: str = ""):
        self.rows = rows
        self.cols = cols
        self.class_name = class_name
        self.seats = [[None for _ in range(cols)] for _ in range(rows)]
        self.students = {}
    
    def add_student(self, student: Student) -> bool:
        if student.student_id in self.students:
            return False
        self.students[student.student_id] = student
        return True
    
    def assign_seat(self, student_id: str, row: int, col: int) -> bool:
        if student_id not in self.students:
            return False
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        if self.seats[row][col] is not None:
            return False
        
        student = self.students[student_id]
        if student.has_seat():
            self.clear_seat(student.row, student.col)
        
        self.seats[row][col] = student
        student.assign_seat(row, col)
        return True
    
    def clear_seat(self, row: int, col: int) -> bool:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        if self.seats[row][col] is not None:
            student = self.seats[row][col]
            student.clear_seat()
            self.seats[row][col] = None
            return True
        return False
    
    def get_available_seats(self) -> List[Tuple[int, int]]:
        available = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.seats[row][col] is None:
                    available.append((row, col))
        return available
    
    def clear_all_seats(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                if self.seats[row][col] is not None:
                    self.seats[row][col].clear_seat()
                    self.seats[row][col] = None
    
    def display_seating_chart(self):
        print(f"\n=== {self.class_name} 座位表 ===")
        print("黑板")
        print("-" * (self.cols * 8))
        
        for row in range(self.rows):
            row_display = []
            for col in range(self.cols):
                if self.seats[row][col] is None:
                    row_display.append("  空位  ")
                else:
                    student = self.seats[row][col]
                    row_display.append(f"{student.name:^6}")
            print(" | ".join(row_display))
        print("-" * (self.cols * 8))

def create_sample_csv(filename: str = "sample_students.csv"):
    """創建範例CSV檔案"""
    sample_data = [
        ['學號', '姓名', '職務'],
        ['S001', '王小明', '班長'],
        ['S002', '李小華', '副班長'],
        ['S003', '張小美', '學藝股長'],
        ['S004', '陳小強', '體育股長'],
        ['S005', '林小雅', '風紀股長'],
        ['S006', '黃小龍', ''],
        ['S007', '吳小鳳', ''],
        ['S008', '劉小傑', ''],
        ['S009', '蔡小慧', ''],
        ['S010', '許小偉', ''],
        ['S011', '鄭小芳', ''],
        ['S012', '謝小宇', ''],
        ['S013', '楊小琪', ''],
        ['S014', '洪小峰', ''],
        ['S015', '周小玲', ''],
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    
    print(f"已創建範例檔案: {filename}")

def read_students_from_csv(filename: str) -> List[Student]:
    """從CSV檔案讀取學生資料"""
    students = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            
            for row in reader:
                if len(row) >= 2:
                    student_id = row[0].strip()
                    name = row[1].strip()
                    position = row[2].strip() if len(row) > 2 else ""
                    
                    if student_id and name:
                        students.append(Student(student_id, name, position))
    
    except FileNotFoundError:
        print(f"檔案 {filename} 不存在")
    except Exception as e:
        print(f"讀取檔案錯誤: {e}")
    
    return students

def random_assign_seats(classroom: Classroom) -> bool:
    """隨機分配座位"""
    classroom.clear_all_seats()
    
    available_seats = classroom.get_available_seats()
    unassigned_students = list(classroom.students.values())
    
    if len(available_seats) < len(unassigned_students):
        print("座位數量不足！")
        return False
    
    random.shuffle(available_seats)
    random.shuffle(unassigned_students)
    
    for i, student in enumerate(unassigned_students):
        if i < len(available_seats):
            row, col = available_seats[i]
            classroom.assign_seat(student.student_id, row, col)
    
    return True

def main():
    """主程式"""
    print("=== 終極智能教室座位表生成器 - 測試版本 ===")
    
    # 創建範例檔案
    csv_file = "sample_students.csv"
    if not os.path.exists(csv_file):
        create_sample_csv(csv_file)
    
    # 讀取學生資料
    students = read_students_from_csv(csv_file)
    print(f"成功讀取 {len(students)} 位學生資料")
    
    # 創建教室
    classroom = Classroom(4, 4, "三年一班")
    
    # 加入學生
    for student in students:
        classroom.add_student(student)
    
    # 顯示學生清單
    print("\n學生清單:")
    for student in students:
        print(f"  {student}")
    
    # 隨機分配座位
    print("\n正在進行隨機分配...")
    if random_assign_seats(classroom):
        print("座位分配完成！")
        classroom.display_seating_chart()
        
        # 顯示統計資訊
        total = len(classroom.students)
        assigned = len([s for s in classroom.students.values() if s.has_seat()])
        print(f"\n統計資訊:")
        print(f"  總學生數: {total}")
        print(f"  已分配座位: {assigned}")
        print(f"  分配率: {assigned/total*100:.1f}%")
    else:
        print("座位分配失敗！")

if __name__ == "__main__":
    main() 
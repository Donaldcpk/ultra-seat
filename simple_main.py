"""
終極智能教室座位表生成器 - 簡化版
不依賴外部套件，使用 CSV 格式
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import json
import os
import random
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass


@dataclass
class Student:
    """學生資料類別"""
    student_id: str
    name: str
    position: str = ""
    row: Optional[int] = None
    col: Optional[int] = None
    
    @property
    def has_seat(self) -> bool:
        return self.row is not None and self.col is not None
    
    def assign_seat(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
    
    def clear_seat(self) -> None:
        self.row = None
        self.col = None


class Classroom:
    """教室布局類別"""
    
    def __init__(self, rows: int, cols: int, class_name: str = ""):
        self.rows = rows
        self.cols = cols
        self.class_name = class_name
        self.seats: List[List[Optional[Student]]] = [
            [None for _ in range(cols)] for _ in range(rows)
        ]
        self.students: Dict[str, Student] = {}
    
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
        if student.has_seat:
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


class SeatManager:
    """座位管理器"""
    
    def __init__(self, classroom: Classroom):
        self.classroom = classroom
        self.history: List[Dict] = []
    
    def random_assign(self) -> bool:
        self.save_state("隨機分配前")
        self.classroom.clear_all_seats()
        
        available_seats = self.classroom.get_available_seats()
        unassigned_students = list(self.classroom.students.values())
        
        if len(available_seats) < len(unassigned_students):
            return False
        
        random.shuffle(available_seats)
        random.shuffle(unassigned_students)
        
        for i, student in enumerate(unassigned_students):
            if i < len(available_seats):
                row, col = available_seats[i]
                self.classroom.assign_seat(student.student_id, row, col)
        
        self.save_state("隨機分配完成")
        return True
    
    def reset_all(self) -> None:
        self.save_state("重置前")
        self.classroom.clear_all_seats()
        self.save_state("重置完成")
    
    def save_state(self, operation: str) -> None:
        # 簡化版不實作歷史記錄
        pass
    
    def get_statistics(self) -> Dict[str, Any]:
        total_students = len(self.classroom.students)
        assigned_students = len([s for s in self.classroom.students.values() if s.has_seat])
        
        return {
            'total_students': total_students,
            'assigned_students': assigned_students,
            'assignment_rate': (assigned_students / total_students * 100) if total_students > 0 else 0
        }


class SimpleFileHandler:
    """簡化版檔案處理工具"""
    
    @staticmethod
    def read_student_csv(file_path: str) -> Tuple[List[Student], List[str]]:
        students = []
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                
                if not headers or len(headers) < 2:
                    errors.append("CSV 檔案格式錯誤")
                    return students, errors
                
                seen_ids = set()
                for row_num, row in enumerate(reader, start=2):
                    if len(row) < 2:
                        continue
                    
                    student_id = row[0].strip()
                    name = row[1].strip()
                    position = row[2].strip() if len(row) > 2 else ""
                    
                    if not student_id or not name:
                        continue
                    
                    if student_id in seen_ids:
                        errors.append(f"第 {row_num} 行：學號 {student_id} 重複")
                        continue
                    
                    seen_ids.add(student_id)
                    students.append(Student(student_id, name, position))
                    
        except Exception as e:
            errors.append(f"讀取檔案錯誤: {str(e)}")
        
        return students, errors
    
    @staticmethod
    def create_sample_csv(file_path: str) -> List[str]:
        errors = []
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['學號', '姓名', '職務'])
                
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
            errors.append(f"建立範例檔案錯誤: {str(e)}")
        
        return errors


class MainWindow:
    """主視窗類別"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.classroom: Optional[Classroom] = None
        self.seat_manager: Optional[SeatManager] = None
        
        self.setup_window()
        self.create_widgets()
        self.ensure_data_directories()
        self.create_sample_file()
    
    def setup_window(self):
        self.root.title("終極智能教室座位表生成器 v1.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
    
    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_toolbar()
        self.create_content_area()
        self.create_status_bar()
    
    def create_toolbar(self):
        toolbar_frame = ttk.Frame(self.main_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 檔案操作
        file_frame = ttk.LabelFrame(toolbar_frame, text="檔案操作")
        file_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(file_frame, text="匯入學生名單 (CSV)", 
                  command=self.import_students).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="新建教室", 
                  command=self.new_classroom).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 座位操作
        seat_frame = ttk.LabelFrame(toolbar_frame, text="座位操作")
        seat_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(seat_frame, text="隨機分配", 
                  command=self.random_assign).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(seat_frame, text="重置", 
                  command=self.reset_seats).pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_content_area(self):
        paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=2)
        
        self.create_left_panel(left_frame)
        self.create_right_panel(right_frame)
    
    def create_left_panel(self, parent):
        # 教室資訊
        info_frame = ttk.LabelFrame(parent, text="教室資訊")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.info_text = tk.Text(info_frame, height=8, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 學生清單
        students_frame = ttk.LabelFrame(parent, text="學生清單")
        students_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('學號', '姓名', '職務', '座位')
        self.students_tree = ttk.Treeview(students_frame, columns=columns, show='headings')
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=80)
        
        self.students_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_right_panel(self, parent):
        # 標題
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(title_frame, text="座位表", font=('Arial', 14, 'bold')).pack(side=tk.LEFT)
        
        self.class_name_var = tk.StringVar()
        ttk.Label(title_frame, text="班級:").pack(side=tk.RIGHT, padx=(10, 5))
        class_entry = ttk.Entry(title_frame, textvariable=self.class_name_var, width=15)
        class_entry.pack(side=tk.RIGHT)
        
        # 座位表
        seat_frame = ttk.LabelFrame(parent, text="座位配置")
        seat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.seat_canvas = tk.Canvas(seat_frame, bg='white')
        self.seat_canvas.pack(fill=tk.BOTH, expand=True)
        
        self.seat_content_frame = ttk.Frame(self.seat_canvas)
        self.seat_canvas.create_window((0, 0), window=self.seat_content_frame, anchor='nw')
    
    def create_status_bar(self):
        self.status_bar = ttk.Frame(self.main_frame)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_bar, text="就緒 - 請先建立教室或匯入學生名單")
        self.status_label.pack(side=tk.LEFT)
        
        self.stats_label = ttk.Label(self.status_bar, text="")
        self.stats_label.pack(side=tk.RIGHT)
    
    def ensure_data_directories(self):
        directories = ['data', 'data/exports']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def create_sample_file(self):
        sample_path = 'data/sample_students.csv'
        if not os.path.exists(sample_path):
            errors = SimpleFileHandler.create_sample_csv(sample_path)
            if not errors:
                self.update_status(f"已建立範例檔案: {sample_path}")
    
    def import_students(self):
        file_path = filedialog.askopenfilename(
            title="選擇學生名單檔案 (CSV 格式)",
            filetypes=[("CSV 檔案", "*.csv"), ("所有檔案", "*.*")],
            initialdir="data"
        )
        
        if not file_path:
            return
        
        try:
            self.update_status("正在匯入學生名單...")
            students, errors = SimpleFileHandler.read_student_csv(file_path)
            
            if errors:
                error_msg = "匯入時發現問題:\n" + "\n".join(errors[:5])
                if len(errors) > 5:
                    error_msg += f"\n... 還有 {len(errors)-5} 個問題"
                messagebox.showwarning("匯入警告", error_msg)
            
            if students:
                if not self.classroom:
                    self.new_classroom()
                
                added_count = 0
                for student in students:
                    if self.classroom.add_student(student):
                        added_count += 1
                
                self.seat_manager = SeatManager(self.classroom)
                self.update_display()
                
                self.update_status(f"成功匯入 {added_count} 位學生")
                messagebox.showinfo("匯入完成", f"成功匯入 {added_count} 位學生")
            else:
                messagebox.showerror("匯入失敗", "沒有找到有效的學生資料")
                
        except Exception as e:
            messagebox.showerror("匯入錯誤", f"匯入學生名單時發生錯誤:\n{str(e)}")
            self.update_status("匯入失敗")
    
    def new_classroom(self):
        dialog = ClassroomSetupDialog(self.root)
        if dialog.result:
            rows, cols, class_name = dialog.result
            self.classroom = Classroom(rows, cols, class_name)
            self.seat_manager = SeatManager(self.classroom)
            self.class_name_var.set(class_name)
            self.update_display()
            self.update_status(f"建立新教室: {class_name} ({rows}x{cols})")
    
    def random_assign(self):
        if not self.seat_manager:
            messagebox.showwarning("警告", "請先匯入學生名單")
            return
        
        try:
            self.update_status("正在隨機分配座位...")
            success = self.seat_manager.random_assign()
            
            if success:
                self.update_display()
                self.update_status("隨機分配完成")
                messagebox.showinfo("分配完成", "座位隨機分配完成！")
            else:
                messagebox.showwarning("分配失敗", "座位數量不足")
                self.update_status("分配失敗")
                
        except Exception as e:
            messagebox.showerror("分配錯誤", f"隨機分配時發生錯誤:\n{str(e)}")
            self.update_status("分配失敗")
    
    def reset_seats(self):
        if not self.seat_manager:
            return
        
        if messagebox.askyesno("確認重置", "確定要重置所有座位分配嗎？"):
            self.seat_manager.reset_all()
            self.update_display()
            self.update_status("座位已重置")
    
    def update_display(self):
        if not self.classroom:
            return
        
        self.update_classroom_info()
        self.update_students_list()
        self.update_seating_chart()
        self.update_statistics()
    
    def update_classroom_info(self):
        if not self.classroom:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, "尚未建立教室\n\n請點擊「新建教室」或「匯入學生名單」開始使用")
            return
        
        info = f"班級名稱: {self.classroom.class_name}\n"
        info += f"教室大小: {self.classroom.rows} 行 x {self.classroom.cols} 列\n"
        info += f"總座位數: {self.classroom.rows * self.classroom.cols}\n"
        info += f"學生人數: {len(self.classroom.students)}\n"
        info += f"已分配座位: {len([s for s in self.classroom.students.values() if s.has_seat])}\n"
        info += f"可用座位: {len(self.classroom.get_available_seats())}\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def update_students_list(self):
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        if not self.classroom:
            return
        
        for student in self.classroom.students.values():
            seat_info = f"({student.row+1}, {student.col+1})" if student.has_seat else "未分配"
            self.students_tree.insert('', 'end', values=(
                student.student_id,
                student.name,
                student.position,
                seat_info
            ))
    
    def update_seating_chart(self):
        for widget in self.seat_content_frame.winfo_children():
            widget.destroy()
        
        if not self.classroom:
            hint_label = tk.Label(self.seat_content_frame, 
                                text="請先建立教室或匯入學生名單",
                                font=('Arial', 12), fg='gray')
            hint_label.pack(expand=True)
            return
        
        # 黑板
        blackboard = tk.Label(self.seat_content_frame, text="黑板", 
                            bg='black', fg='white', font=('Arial', 12, 'bold'),
                            width=self.classroom.cols * 8, height=2)
        blackboard.grid(row=0, column=0, columnspan=self.classroom.cols, 
                       padx=2, pady=2, sticky='ew')
        
        # 座位
        for row in range(self.classroom.rows):
            for col in range(self.classroom.cols):
                self.create_seat_widget(row + 1, col, row, col)
        
        self.seat_content_frame.update_idletasks()
        self.seat_canvas.configure(scrollregion=self.seat_canvas.bbox("all"))
    
    def create_seat_widget(self, grid_row, grid_col, seat_row, seat_col):
        if self.classroom.seats[seat_row][seat_col] is not None:
            student = self.classroom.seats[seat_row][seat_col]
            display_name = student.name[:6] + "..." if len(student.name) > 6 else student.name
            seat = tk.Label(self.seat_content_frame, text=display_name, 
                          bg='lightblue', fg='black', font=('Arial', 9),
                          width=8, height=3, relief='raised', bd=2)
        else:
            seat = tk.Label(self.seat_content_frame, text=f"{seat_row+1},{seat_col+1}", 
                          bg='lightgray', fg='black', font=('Arial', 8),
                          width=8, height=3, relief='raised', bd=1)
        
        seat.grid(row=grid_row, column=grid_col, padx=1, pady=1)
        seat.bind('<Button-1>', lambda e: self.on_seat_click(seat_row, seat_col))
    
    def on_seat_click(self, row, col):
        if not self.classroom:
            return
        
        student = self.classroom.seats[row][col]
        if student:
            messagebox.showinfo("座位資訊", 
                              f"學號: {student.student_id}\n"
                              f"姓名: {student.name}\n"
                              f"職務: {student.position}\n"
                              f"座位: ({row+1}, {col+1})")
    
    def update_statistics(self):
        if not self.seat_manager:
            self.stats_label.config(text="")
            return
        
        stats = self.seat_manager.get_statistics()
        stats_text = f"學生: {stats['assigned_students']}/{stats['total_students']} | "
        stats_text += f"分配率: {stats['assignment_rate']:.1f}%"
        
        self.stats_label.config(text=stats_text)
    
    def update_status(self, message: str):
        self.status_label.config(text=message)
        self.root.update_idletasks()


class ClassroomSetupDialog:
    """教室設定對話框"""
    
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("新建教室")
        self.dialog.geometry("350x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 置中顯示
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 說明
        ttk.Label(main_frame, text="請設定教室參數:", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # 班級名稱
        ttk.Label(main_frame, text="班級名稱:").grid(row=1, column=0, sticky='w', pady=5)
        self.class_name_var = tk.StringVar(value="")
        ttk.Entry(main_frame, textvariable=self.class_name_var, width=20).grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # 行數
        ttk.Label(main_frame, text="行數:").grid(row=2, column=0, sticky='w', pady=5)
        self.rows_var = tk.StringVar(value="6")
        ttk.Entry(main_frame, textvariable=self.rows_var, width=20).grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # 列數
        ttk.Label(main_frame, text="列數:").grid(row=3, column=0, sticky='w', pady=5)
        self.cols_var = tk.StringVar(value="8")
        ttk.Entry(main_frame, textvariable=self.cols_var, width=20).grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # 提示
        hint_text = "建議:\n• 行數: 4-8 行\n• 列數: 6-10 列\n• 確保座位數量大於學生人數"
        ttk.Label(main_frame, text=hint_text, font=('Arial', 9), foreground='gray').grid(row=4, column=0, columnspan=2, pady=10)
        
        # 按鈕
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="確定", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def ok_clicked(self):
        try:
            class_name = self.class_name_var.get().strip()
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            
            if rows <= 0 or cols <= 0:
                messagebox.showerror("輸入錯誤", "行數和列數必須大於 0")
                return
            
            if rows > 20 or cols > 20:
                messagebox.showerror("輸入錯誤", "行數和列數不能超過 20")
                return
            
            self.result = (rows, cols, class_name)
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("輸入錯誤", "請輸入有效的數字")
    
    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()


def main():
    """主程式函數"""
    try:
        root = tk.Tk()
        app = MainWindow(root)
        
        def on_closing():
            if messagebox.askokcancel("退出", "確定要退出座位表生成器嗎？"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        error_msg = f"程式啟動時發生錯誤: {str(e)}"
        print(error_msg)
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("錯誤", error_msg)
        except:
            pass


if __name__ == "__main__":
    main() 
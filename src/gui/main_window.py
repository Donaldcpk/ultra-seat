"""
主視窗 GUI
座位表生成器的主要使用者介面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import Optional

from ..core.classroom import Classroom
from ..core.seat_manager import SeatManager
from ..utils.file_handler import FileHandler


class MainWindow:
    """主視窗類別"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.classroom: Optional[Classroom] = None
        self.seat_manager: Optional[SeatManager] = None
        
        self.setup_window()
        self.create_widgets()
        self.ensure_data_directories()
    
    def setup_window(self):
        """設定主視窗屬性"""
        self.root.title("終極智能教室座位表生成器 v1.0")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
    
    def create_widgets(self):
        """建立所有 GUI 元件"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_toolbar()
        self.create_content_area()
        self.create_status_bar()
    
    def create_toolbar(self):
        """建立工具列"""
        toolbar_frame = ttk.Frame(self.main_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 檔案操作
        file_frame = ttk.LabelFrame(toolbar_frame, text="檔案操作")
        file_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(file_frame, text="匯入學生名單", 
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
        ttk.Button(seat_frame, text="上一步", 
                  command=self.undo).pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_content_area(self):
        """建立內容區域"""
        paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=2)
        
        self.create_left_panel(left_frame)
        self.create_right_panel(right_frame)
    
    def create_left_panel(self, parent):
        """建立左側面板"""
        # 教室資訊
        info_frame = ttk.LabelFrame(parent, text="教室資訊")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.info_text = tk.Text(info_frame, height=6, wrap=tk.WORD)
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
        """建立右側面板"""
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
        """建立狀態列"""
        self.status_bar = ttk.Frame(self.main_frame)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_bar, text="就緒")
        self.status_label.pack(side=tk.LEFT)
        
        self.stats_label = ttk.Label(self.status_bar, text="")
        self.stats_label.pack(side=tk.RIGHT)
    
    def ensure_data_directories(self):
        """確保資料目錄存在"""
        directories = ['src/data', 'src/data/exports']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def import_students(self):
        """匯入學生名單"""
        file_path = filedialog.askopenfilename(
            title="選擇學生名單檔案",
            filetypes=[("Excel 檔案", "*.xlsx"), ("所有檔案", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.update_status("正在匯入學生名單...")
            students, errors = FileHandler.read_student_excel(file_path, 1)
            
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
        """建立新教室"""
        dialog = ClassroomSetupDialog(self.root)
        if dialog.result:
            rows, cols, class_name = dialog.result
            self.classroom = Classroom(rows, cols, class_name)
            self.seat_manager = SeatManager(self.classroom)
            self.class_name_var.set(class_name)
            self.update_display()
            self.update_status(f"建立新教室: {class_name} ({rows}x{cols})")
    
    def random_assign(self):
        """隨機分配座位"""
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
                messagebox.showwarning("分配失敗", "座位數量不足或存在限制條件衝突")
                self.update_status("分配失敗")
                
        except Exception as e:
            messagebox.showerror("分配錯誤", f"隨機分配時發生錯誤:\n{str(e)}")
            self.update_status("分配失敗")
    
    def reset_seats(self):
        """重置座位"""
        if not self.seat_manager:
            return
        
        if messagebox.askyesno("確認重置", "確定要重置所有座位分配嗎？"):
            self.seat_manager.reset_all()
            self.update_display()
            self.update_status("座位已重置")
    
    def undo(self):
        """撤銷操作"""
        if not self.seat_manager:
            return
        
        if self.seat_manager.undo():
            self.update_display()
            self.update_status("已撤銷上一步操作")
        else:
            messagebox.showinfo("無法撤銷", "沒有可撤銷的操作")
    
    def update_display(self):
        """更新顯示內容"""
        if not self.classroom:
            return
        
        self.update_classroom_info()
        self.update_students_list()
        self.update_seating_chart()
        self.update_statistics()
    
    def update_classroom_info(self):
        """更新教室資訊"""
        if not self.classroom:
            self.info_text.delete(1.0, tk.END)
            return
        
        info = f"班級名稱: {self.classroom.class_name}\n"
        info += f"教室大小: {self.classroom.rows} 行 x {self.classroom.cols} 列\n"
        info += f"總座位數: {self.classroom.rows * self.classroom.cols}\n"
        info += f"學生人數: {len(self.classroom.students)}\n"
        info += f"已分配座位: {len([s for s in self.classroom.students.values() if s.has_seat])}\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def update_students_list(self):
        """更新學生清單"""
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
        """更新座位表顯示"""
        for widget in self.seat_content_frame.winfo_children():
            widget.destroy()
        
        if not self.classroom:
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
        """建立座位小工具"""
        if (seat_row, seat_col) in self.classroom.blocked_seats:
            seat = tk.Label(self.seat_content_frame, text="X", 
                          bg='red', fg='white', font=('Arial', 10, 'bold'),
                          width=8, height=3, relief='raised', bd=2)
        elif self.classroom.seats[seat_row][seat_col] is not None:
            student = self.classroom.seats[seat_row][seat_col]
            seat = tk.Label(self.seat_content_frame, text=student.name, 
                          bg='lightblue', fg='black', font=('Arial', 9),
                          width=8, height=3, relief='raised', bd=2)
        else:
            seat = tk.Label(self.seat_content_frame, text=f"{seat_row+1},{seat_col+1}", 
                          bg='lightgray', fg='black', font=('Arial', 8),
                          width=8, height=3, relief='raised', bd=1)
        
        seat.grid(row=grid_row, column=grid_col, padx=1, pady=1)
    
    def update_statistics(self):
        """更新統計資訊"""
        if not self.seat_manager:
            self.stats_label.config(text="")
            return
        
        stats = self.seat_manager.get_statistics()
        stats_text = f"學生: {stats['assigned_students']}/{stats['total_students']} | "
        stats_text += f"分配率: {stats['assignment_rate']:.1f}%"
        
        self.stats_label.config(text=stats_text)
    
    def update_status(self, message: str):
        """更新狀態列"""
        self.status_label.config(text=message)
        self.root.update_idletasks()


class ClassroomSetupDialog:
    """教室設定對話框"""
    
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("新建教室")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 置中顯示
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 班級名稱
        ttk.Label(main_frame, text="班級名稱:").grid(row=0, column=0, sticky='w', pady=5)
        self.class_name_var = tk.StringVar(value="")
        ttk.Entry(main_frame, textvariable=self.class_name_var, width=20).grid(row=0, column=1, pady=5)
        
        # 行數
        ttk.Label(main_frame, text="行數:").grid(row=1, column=0, sticky='w', pady=5)
        self.rows_var = tk.StringVar(value="6")
        ttk.Entry(main_frame, textvariable=self.rows_var, width=20).grid(row=1, column=1, pady=5)
        
        # 列數
        ttk.Label(main_frame, text="列數:").grid(row=2, column=0, sticky='w', pady=5)
        self.cols_var = tk.StringVar(value="8")
        ttk.Entry(main_frame, textvariable=self.cols_var, width=20).grid(row=2, column=1, pady=5)
        
        # 按鈕
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
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
"""
學生資料模型
定義學生的基本資料結構和相關方法
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Student:
    """
    學生資料類別
    
    屬性:
        student_id (str): 學號，必須唯一
        name (str): 學生姓名
        position (str): 班級職務，如班長、副班長等
        row (Optional[int]): 座位行號（從1開始）
        col (Optional[int]): 座位列號（從1開始）
        constraints (Dict[str, Any]): 座位限制條件
    """
    
    student_id: str
    name: str
    position: str = ""
    row: Optional[int] = None
    col: Optional[int] = None
    constraints: Dict[str, Any] = None
    
    def __post_init__(self):
        """初始化後處理"""
        if self.constraints is None:
            self.constraints = {}
    
    @property
    def has_seat(self) -> bool:
        """檢查學生是否已分配座位"""
        return self.row is not None and self.col is not None
    
    @property
    def seat_position(self) -> Optional[tuple]:
        """取得座位位置 (row, col)"""
        if self.has_seat:
            return (self.row, self.col)
        return None
    
    def assign_seat(self, row: int, col: int) -> None:
        """
        分配座位給學生
        
        參數:
            row (int): 座位行號
            col (int): 座位列號
        """
        self.row = row
        self.col = col
    
    def clear_seat(self) -> None:
        """清除學生的座位分配"""
        self.row = None
        self.col = None
    
    def add_constraint(self, constraint_type: str, value: Any) -> None:
        """
        新增座位限制條件
        
        參數:
            constraint_type (str): 限制類型
            value (Any): 限制值
        """
        self.constraints[constraint_type] = value
    
    def remove_constraint(self, constraint_type: str) -> None:
        """
        移除座位限制條件
        
        參數:
            constraint_type (str): 要移除的限制類型
        """
        if constraint_type in self.constraints:
            del self.constraints[constraint_type]
    
    def has_constraint(self, constraint_type: str) -> bool:
        """
        檢查是否有特定限制條件
        
        參數:
            constraint_type (str): 限制類型
            
        回傳:
            bool: 是否有該限制條件
        """
        return constraint_type in self.constraints
    
    def to_dict(self) -> Dict[str, Any]:
        """
        將學生資料轉換為字典格式
        
        回傳:
            Dict[str, Any]: 學生資料字典
        """
        return {
            'student_id': self.student_id,
            'name': self.name,
            'position': self.position,
            'row': self.row,
            'col': self.col,
            'constraints': self.constraints
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """
        從字典建立學生物件
        
        參數:
            data (Dict[str, Any]): 學生資料字典
            
        回傳:
            Student: 學生物件
        """
        return cls(
            student_id=data['student_id'],
            name=data['name'],
            position=data.get('position', ''),
            row=data.get('row'),
            col=data.get('col'),
            constraints=data.get('constraints', {})
        )
    
    def __str__(self) -> str:
        """字串表示"""
        seat_info = f"({self.row}, {self.col})" if self.has_seat else "未分配"
        return f"{self.name}({self.student_id}) - {self.position} - 座位: {seat_info}"
    
    def __repr__(self) -> str:
        """詳細字串表示"""
        return f"Student(id='{self.student_id}', name='{self.name}', position='{self.position}', seat={self.seat_position})" 
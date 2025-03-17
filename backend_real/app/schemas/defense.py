from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class BaseDefense(BaseModel):
    student_id: int
    student_name: str
    teacher_name: str
    project_title: str
    defense_class: str
    defense_group: Optional[str]
    defense_phase: str
    defense_date: date
    status: Optional[str] = "未开始"
    class Config:
        from_attributes = True


class DefenseIn(BaseDefense):
    pass


class DefenseOut(BaseDefense):
    id: int
    created_time: Optional[datetime]
    update_time: Optional[datetime]
    class Config:
        from_attributes = True
        orm_mode = True

class DefenseUpdateStatus(BaseModel):
    status: str
    class Config:
        from_attributes = True

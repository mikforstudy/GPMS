from typing import Optional
from pydantic import BaseModel

class GroupOut(BaseModel):
    student_id: int
    student_name: str
    teacher_name1: str
    teacher_name2: str
    teacher_name3: str


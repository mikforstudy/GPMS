from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BaseSelection(BaseModel):
    student_id: int
    teacher_id: int
    username: Optional[str]
    major: Optional[str]
    title: Optional[str]
    description: Optional[str]



    class Config:
        from_attributes = True


class SelectionIn(BaseSelection):
    pass

class SelectionOut(BaseSelection):
    id: int
    status: Optional[str]
    created_time:Optional[datetime] = None
    update_time:Optional[datetime] = None
    class Config:
        from_attributes = True

class SelectionUpdateStatus(BaseModel):
    status: str
    class Config:
        from_attributes = True

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MiddleDocxModel(BaseModel):
    title: str
    teacher_name: str
    student_name: str
    student_id: int

class MiddleDocxIn(MiddleDocxModel):
    # 一、设计（论文）的进展情况：（课题工作量是否适中、已完成任务、未完成任务、完成课题存在问题和解决办法）
    content1: Optional[str] = None
    # 六、指导教师意见
    content6: Optional[str] = None
    # 七、备注
    content7: Optional[str] = None

class MiddleDocxOut(MiddleDocxModel):
    id: int
    mark: Optional[str]
    created_time: Optional[datetime]
    update_time: Optional[datetime]
    status: Optional[str]
    class Config:
        from_attributes = True
5

class MiddleDocxDetail(MiddleDocxOut):
    content1: Optional[str]
    content6: Optional[str]
    content7: Optional[str]
    class Config:
        from_attributes = True



class MiddleDocxUpdateStatus(BaseModel):
    status: str
    content6: Optional[str] = None
    class Config:
        from_attributes = True


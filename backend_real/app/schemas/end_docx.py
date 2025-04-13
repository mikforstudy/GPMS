from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EndDocxModel(BaseModel):
    title: str
    student_name: str
    student_id: int
    teacher_name: str


class EndDocxIn(EndDocxModel):
    # 一、主要内容
    content1: Optional[str] = None
    # 二、基本要求
    content2: Optional[str] = None
    # 三、进度安排
    content3: Optional[str] = None
    # 三、主要参考文献
    content4: Optional[str] = None


class EndDocxOut(EndDocxModel):
    id: int
    mark: Optional[str]
    created_time: Optional[datetime]
    update_time: Optional[datetime]
    status: Optional[str]

    class Config:
        from_attributes = True



class EndDocxDetail(EndDocxOut):
    content1: Optional[str]
    content2: Optional[str]
    content3: Optional[str]
    content4: Optional[str]

    class Config:
        from_attributes = True



class EndDocxUpdateStatus(BaseModel):
    status: str

    class Config:
        from_attributes = True
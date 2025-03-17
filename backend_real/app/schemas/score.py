from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class BaseScore(BaseModel):
    """
    评分基本信息
    """
    project_title: str
    student_id: int
    student_name: str
    teacher_name: str



class ScoreIn(BaseModel):
    """
    评分信息输入
    """
    score: str


class ScoreOut(BaseScore):
    """
    评分信息输出
    """
    id: int
    score: str
    created_time: Optional[datetime]
    update_time: Optional[datetime]
    class Config:
        from_attributes = True

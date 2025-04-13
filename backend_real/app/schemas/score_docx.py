from typing import Optional
from pydantic import BaseModel

class BaseScoreDocx(BaseModel):
    student_name: Optional[str]
    content1: Optional[str]
    score1: Optional[int]
    content2: Optional[str]
    score2: Optional[int]
    content3: Optional[str]
    score3: Optional[int]

    class Config:
        from_attributes = True

class ScoreDocxOut(BaseScoreDocx):
    score4: Optional[int]
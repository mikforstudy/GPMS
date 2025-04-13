from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class StartDocxModel(BaseModel):
    title: str
    teacher_name: str
    student_name: str
    student_id: int


class StartDocxIn(StartDocxModel):
    # 一、选题背景及意义
    content1: Optional[str] = None
    # 二、选题的国内外研究现状
    content2: Optional[str] = None
    # 三、选题的研究方法和技术路线
    content3: Optional[str] = None
    # 四、选题的研究内容
    content4: Optional[str] = None
    # 五、选题的研究方案
    content5: Optional[str] = None
    # 六、选题的预期成果
    content6: Optional[str] = None


class StartDocxOut(StartDocxModel):
    id: int
    mark: Optional[str]
    created_time: Optional[datetime]
    update_time: Optional[datetime]
    status: Optional[str]
    class Config:
        from_attributes = True
<<<<<<< HEAD
=======
        orm_mode = True
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645


class StartDocxDetail(StartDocxOut):
    content1: Optional[str]
    content2: Optional[str]
    content3: Optional[str]
    content4: Optional[str]
    content5: Optional[str]
    content6: Optional[str]
    class Config:
        from_attributes = True
<<<<<<< HEAD
=======
        orm_mode = True
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645

class StartDocxUpdateStatus(BaseModel):
    status: str
    content6: Optional[str] = None
    class Config:
<<<<<<< HEAD
        from_attributes = True
=======
        orm_mode = True
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645




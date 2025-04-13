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
<<<<<<< HEAD
        from_attributes = True
=======
        orm_mode = True
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645


class SelectionIn(BaseSelection):
    pass

class SelectionOut(BaseSelection):
    id: int
    status: Optional[str]
    created_time:Optional[datetime] = None
    update_time:Optional[datetime] = None
    class Config:
        from_attributes = True
<<<<<<< HEAD
=======
        orm_mode = True
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645

class SelectionUpdateStatus(BaseModel):
    status: str
    class Config:
<<<<<<< HEAD
        from_attributes = True
=======
        orm_mode = True
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645

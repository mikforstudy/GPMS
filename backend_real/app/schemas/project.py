from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr, Field, ConfigDict


class ProjectBase(BaseModel):
    title: str
    description: Optional[str]
    teacher_id: int
    student_id: int
    status: Optional[str]


class ProjectIn(ProjectBase):
    start_date: Optional[datetime]

class ProjectOut(ProjectBase):
    id: int
    start_date: Optional[datetime]
    update_time: Optional[datetime]
    teacher_name: Optional[str]
    class Config:
        from_attributes = True
<<<<<<< HEAD

=======
        orm_mode = True
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645


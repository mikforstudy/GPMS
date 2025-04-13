from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr, Field, ConfigDict


class BaseUser(BaseModel):

    username: Optional[str] = None
    role:Optional[str] = None
    student_id:Optional[int] = None
    teacher_id:Optional[int] = None
    # created_time:Optional[datetime] = None
    # update_time:Optional[datetime] = None

class UserIn(BaseUser):
    password: SecretStr


class UserOut(BaseUser):
    id:int
    created_time:Optional[datetime] = None
    update_time:Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
<<<<<<< HEAD
=======
        orm_mode=True
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645
    )


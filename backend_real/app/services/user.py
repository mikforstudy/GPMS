import asyncio
from datetime import datetime
from typing_extensions import deprecated
from watchfiles import awatch

from app.models.user import User
from app.schemas.user import UserIn, BaseUser

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    @staticmethod
    async def create_user(user:UserIn):
        # 对密码进行哈希处理
        hashed_password = pwd_context.hash(user.password.get_secret_value())

        user_data = user.model_dump()
        user_data.update(password=hashed_password)

        user_obj = await User.create(**user_data)
        return user_obj

    @staticmethod
    async def get_user(user_id:int):
        return await User.filter(id = user_id).first()

    @staticmethod
    async def update_user(user_id: int, user: BaseUser):
        user_data = user.model_dump()
        user_data['update_time'] = datetime.now()  # Set the update_time to the current time
        await User.filter(id=user_id).update(**user_data)
        return await User.filter(id=user_id).first()


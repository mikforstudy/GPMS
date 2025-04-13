from fastapi import APIRouter, status, HTTPException, Query, Depends
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserIn, UserOut, BaseUser
from app.services.user import UserService

router = APIRouter()

@router.post("/", response_model=UserOut, summary="创建用户", description="描述详细接口XXXX", responses={200: {"描述": "用户注册成功"}})
async def create_user(user:UserIn):
    user_obj = await UserService.create_user(user)
    return user_obj

@router.get("/{user_id}", response_model=UserOut, summary="获取用户详情", status_code=status.HTTP_200_OK)
async def get_user(user_id:int):
    return await UserService.get_user(user_id)

@router.get("/", response_model=list[UserOut], summary="获取用户列表", status_code=status.HTTP_200_OK)
async def get_users():
    # noinspection Pydantic
    return [UserOut.from_orm(user) for user in await User.all()]

@router.put("/{user_id}", response_model=UserOut, summary="更新用户信息", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: BaseUser):
    user_obj = await UserService.update_user(user_id, user)
    return user_obj

@router.delete("/{user_id}", response_model=UserOut, summary="删除用户", status_code=status.HTTP_200_OK)
async def delete_user(user_id:int):
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    await user.delete()
    return user


class PaginatedUserOut(BaseModel):
    page: int
    users: list[UserOut]
    total: int

@router.get("/users/paginate", response_model=PaginatedUserOut, summary="分页获取用户列表", status_code=status.HTTP_200_OK)
async def get_paginated_users(page: int = Query(1, ge=1)):
    page_size = 10
    offset = (page - 1) * page_size
    users = await User.all().offset(offset).limit(page_size)
    total_users = await User.all().count()
    print(total_users)
    return PaginatedUserOut(page=page, users=[UserOut.from_orm(user) for user in users], total=total_users)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str
    userType: str

@router.post("/login", response_model=UserOut, summary="用户登录", status_code=status.HTTP_200_OK)
async def login(login_request: LoginRequest):
    user = await User.filter(username=login_request.username, role=login_request.userType).first()
    if not user or not pwd_context.verify(login_request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    return UserOut.from_orm(user)


# 根据教师ID查询教师username
@router.get("/get_teacher_username/{teacher_id}", response_model=UserOut, summary="根据教师ID查询教师username", status_code=status.HTTP_200_OK)
async def get_teacher(teacher_id: int):
    teacher = await User.filter(teacher_id=teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="教师不存在")
    return UserOut.from_orm(teacher)


# 修改密码
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# 根据username修改密码
@router.put("/change_password/{username}", response_model=UserOut, summary="根据username修改密码", status_code=status.HTTP_200_OK)
async def change_password(username: str, change_password_request: ChangePasswordRequest):
    user = await User.filter(username=username).first()
    if not user or not pwd_context.verify(change_password_request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    new_password_hash = pwd_context.hash(change_password_request.new_password)
    await User.filter(username=username).update(password=new_password_hash)
    return UserOut.from_orm(user)




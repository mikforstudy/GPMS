from fastapi import APIRouter, HTTPException, status, Query
from datetime import datetime
from pydantic import BaseModel

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectIn, ProjectOut


router = APIRouter()
# 学生根据username查询学生id返回项目数据
@router.get("/student/{username}", response_model=list[ProjectOut], summary="学生查询项目", status_code=status.HTTP_200_OK)
async def get_projects(username: str):
    query_set = await User.filter(username=username).first()
    if not query_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    student_id = query_set.student_id
    projects = await Project.filter(student_id=student_id).all()
    return [ProjectOut.from_orm(project) for project in projects]

# 根据学生id查询项目（只会有一个项目）
@router.get("/base/student/{student_id}", response_model=ProjectOut, summary="学生查询项目", status_code=status.HTTP_200_OK)
async def get_project_base(student_id: int):
    project = await Project.filter(student_id=student_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")
    return ProjectOut.from_orm(project)


# 教师根据teacher_name查询项目
@router.get("/teacher/{teacher_name}", response_model=list[ProjectOut], summary="教师查询项目", status_code=status.HTTP_200_OK)
async def get_projects(teacher_name: str):
    projects = await Project.filter(teacher_name=teacher_name).all()
    return [ProjectOut.model_validate(project) for project in projects]





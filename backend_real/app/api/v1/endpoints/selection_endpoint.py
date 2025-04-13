from fastapi import APIRouter, HTTPException, status, Query
from datetime import datetime
from pydantic import BaseModel

from app.models.selection import Selection
from app.models.score import Score
from app.models.user import User
from app.schemas.selection import SelectionIn, SelectionOut, SelectionUpdateStatus
from app.schemas.score import BaseScore

from app.models.project import Project
from app.schemas.project import ProjectIn, ProjectOut

router = APIRouter()

# 获取所有选题
@router.get("/", response_model=list[SelectionOut], summary="获取选题列表", status_code=status.HTTP_200_OK)
async def get_selections():
    selections = await Selection.all()
    return [SelectionOut.from_orm(selection) for selection in selections]

# 学生申报选题
@router.post("/student/", response_model=SelectionOut, summary="申报选题", description="描述详细接口XXXX", responses={200: {"描述": "选题创建成功"}})
async def create_selection(selection: SelectionIn):
    # 验证学生用户是否存在
    user = await User.filter(username=selection.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    # 验证教师是否存在，并检查角色是否为teacher
    teacher = await User.filter(teacher_id=selection.teacher_id, role="teacher").first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="教师不存在")

    # 使用model_dump()替代已弃用的dict()方法
    selection_obj = await Selection.create(**selection.model_dump())
    return selection_obj

# 根据教师id获取选题列表
# @router.get("/teacher/{teacher_id}", response_model=list[SelectionOut], summary="获取选题列表", status_code=status.HTTP_200_OK)
# async def get_selections(teacher_id:int):
#     selections = await Selection.filter(teacher_id=teacher_id).all()
#     return [SelectionOut.from_orm(selection) for selection in selections]


# 根据username修改选题状态
@router.put("/{username}", response_model=SelectionOut, summary="教师更新选题状态", status_code=status.HTTP_200_OK)
async def update_selection_status(username: str, selection: SelectionUpdateStatus):
    await Selection.filter(username=username).update(status=selection.status)
    selection_obj = await Selection.filter(username=username).first()
    if not selection_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="选题不存在")
    return SelectionOut.from_orm(selection_obj)

# 根据username修改选题（学生）
@router.put("/student/{username}", response_model=SelectionOut, summary="学生修改选题", status_code=status.HTTP_200_OK)
async def update_selection(username: str, selection: SelectionIn):
    await Selection.filter(username=username).update(**selection.dict())
    selection_obj = await Selection.filter(username=username).first()
    if not selection_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="选题不存在")
    return SelectionOut.from_orm(selection_obj)

# 教师根据username查询教师id返回选题列表
@router.get("/teacher/{username}", response_model=list[SelectionOut], summary="教师查询选题", status_code=status.HTTP_200_OK)
async def get_selections(username: str):
    query_set = await User.filter(username=username).first()
    if not query_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    teacher_id = query_set.teacher_id
    selections = await Selection.filter(teacher_id=teacher_id).all()
    return [SelectionOut.from_orm(selection) for selection in selections]

# 教师根据学生id修改状态； 教师修改状态为通过后创建项目基本信息，创建成绩信息
@router.put("/teacher/{student_id}", response_model=SelectionOut, summary="教师修改选题状态", status_code=status.HTTP_200_OK)
async def update_selection_status(student_id: int, selection: SelectionUpdateStatus):
    await Selection.filter(student_id=student_id).update(status=selection.status, update_time=datetime.now())
    selection_obj = await Selection.filter(student_id=student_id).first()
    if not selection_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="选题不存在")

    # 根据Selection.teacher_id获取教师username
    teacher = await User.filter(teacher_id=selection_obj.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="教师不存在")



    # 如果状态为通过，则创建项目
    if selection.status == "通过":
        project_data = {
            "title": selection_obj.title,
            "description": selection_obj.description,
            "teacher_id": selection_obj.teacher_id,
            "student_id": selection_obj.student_id,
            "status": "开题",  # or any default status for a new project
            "start_date": datetime.now(),
            "teacher_name": teacher.username
        }
        await Project.create(**project_data)

        # 创建成绩信息
        score_data = {
            "project_title": selection_obj.title,
            "student_id": selection_obj.student_id,
            "student_name": selection_obj.username,
            "teacher_name": teacher.username,
            "score": "待评定"
        }
        await Score.create(**score_data)



    return SelectionOut.from_orm(selection_obj)



class PaginatedSelectionOut(BaseModel):
    page: int
    selections: list[SelectionOut]
    total: int

@router.get("/selections/paginate", response_model=PaginatedSelectionOut, summary="分页获取选题列表", status_code=status.HTTP_200_OK)
async def get_paginated_selections(page: int = Query(1, ge=1)):
    page_size = 10
    offset = (page - 1) * page_size
    selections = await Selection.all().offset(offset).limit(page_size)
    total_selections = await Selection.all().count()
    print(total_selections)
    return PaginatedSelectionOut(page=page, selections=[SelectionOut.from_orm(selection) for selection in selections], total=total_selections)

# 管理员根据id修改选题信息
@router.put("/admin/{selection_id}", response_model=SelectionOut, summary="管理员修改选题信息", status_code=status.HTTP_200_OK)
async def update_selection(selection_id: int, selection: SelectionIn):
    await Selection.filter(id=selection_id).update(**selection.dict())
    selection_obj = await Selection.filter(id=selection_id).first()
    if not selection_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="选题不存在")
    return SelectionOut.from_orm(selection_obj)

# 管理员根据id删除选题
@router.delete("/admin/{selection_id}", response_model=SelectionOut, summary="管理员删除选题", status_code=status.HTTP_200_OK)
async def delete_selection(selection_id:int):
    selection = await Selection.filter(id=selection_id).first()
    if not selection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="选题不存在")

    await selection.delete()
    return selection


# 学生根据username查询学生id返回选题列表
@router.get("/student/{username}", response_model=list[SelectionOut], summary="根据username查询学生id返回选题列表", status_code=status.HTTP_200_OK)
async def get_selections(username: str):
    query_set = await User.filter(username=username).first()
    if not query_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    student_id = query_set.student_id
    selections = await Selection.filter(student_id=student_id).all()
    return [SelectionOut.from_orm(selection) for selection in selections]
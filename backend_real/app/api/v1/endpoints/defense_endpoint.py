from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.models.defense import Defense
from app.schemas.defense import DefenseIn, DefenseOut, DefenseUpdateStatus

import os

router = APIRouter()

# 创建答辩信息
@router.post("/create/", response_model=DefenseOut, summary="创建答辩信息")
async def create_defense(defense: DefenseIn):
    defense_obj = await Defense.create(**defense.model_dump())
    return defense_obj


# 学生根据学生id查询答辩信息
@router.get("/student/{student_id}", response_model=list[DefenseOut], summary="学生查询答辩信息")
async def get_defenses(student_id: int):
    defenses = await Defense.filter(student_id=student_id).all()
    return [DefenseOut.model_validate(defense) for defense in defenses]


# 学生根据学生id和defense_phase修改答辩状态
@router.put("/{student_id}/{defense_phase}", response_model=DefenseOut, summary="学生修改答辩状态")
async def update_defense_status(student_id: int, defense_phase: str, defense: DefenseUpdateStatus):
    update_data = defense.model_dump()
    update_data['update_time'] = datetime.now()

    await Defense.filter(student_id=student_id, defense_phase=defense_phase).update(**update_data)
    defense_obj = await Defense.filter(student_id=student_id, defense_phase=defense_phase).first()
    if not defense_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="答辩信息不存在")
    return DefenseOut.model_validate(defense_obj)



# 教师根据username查询答辩信息
@router.get("/teacher/{username}", response_model=list[DefenseOut], summary="教师查询答辩信息")
async def get_defenses(username: str):
    defenses = await Defense.filter(teacher_name=username).all()
    return [DefenseOut.model_validate(defense) for defense in defenses]


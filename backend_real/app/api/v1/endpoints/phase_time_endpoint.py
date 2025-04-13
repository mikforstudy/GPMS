from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.phase_time import Phase
from app.schemas.phase_time import PhaseCreate, PhaseUpdate

router = APIRouter()


@router.post("/", summary="创建阶段时间")
async def create_phase(phase: PhaseCreate):
    """
    创建新的阶段时间设置
    """
    # 检查是否已存在记录
    existing_count = await Phase.all().count()
    if existing_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已存在阶段时间设置，请使用修改接口"
        )

    phase_obj = await Phase.create(**phase.model_dump(exclude_unset=True))
    return phase_obj


@router.put("/{phase_id}", summary="修改阶段时间")
async def update_phase(phase_id: int, phase: PhaseUpdate):
    """
    修改指定ID的阶段时间设置
    """
    phase_obj = await Phase.get_or_none(id=phase_id)
    if not phase_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到指定ID的阶段时间设置"
        )

    update_data = phase.model_dump(exclude_unset=True)
    await Phase.filter(id=phase_id).update(**update_data)

    updated_phase = await Phase.get(id=phase_id)
    return updated_phase


@router.get("/", summary="获取所有阶段时间")
async def get_phases():
    """
    获取所有阶段时间设置
    """
    phases = await Phase.first()
    print(phases)
    return phases


@router.get("/current", summary="获取当前阶段时间设置")
async def get_current_phase():
    """
    获取当前唯一的阶段时间设置（通常系统中只有一条记录）
    """
    phase = await Phase.first()
    if not phase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="系统中尚未设置阶段时间"
        )
    return phase


@router.delete("/{phase_id}", summary="删除阶段时间")
async def delete_phase(phase_id: int):
    """
    删除指定ID的阶段时间设置
    """
    deleted_count = await Phase.filter(id=phase_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到指定ID的阶段时间设置"
        )
    return {"message": "阶段时间设置已删除"}
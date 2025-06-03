from fastapi import APIRouter, HTTPException
from datetime import datetime
import asyncio
import sys

from app.models.project import Project
from app.models.defense import Defense
from app.models.user import User
from app.models.group import Group

# 创建路由器
router = APIRouter()


# 生成答辩数据的API端点
@router.get("/generate-defense-data", summary="生成答辩数据",
            description="从projects表中获取所有项目，为每个项目创建三条答辩信息")
async def generate_defense_data_endpoint():
    """
    生成答辩数据API端点

    从projects表中获取所有项目，为每个项目创建三条答辩信息（开题答辩、中期答辩、最终答辩）
    如果学生已有3条答辩记录，则跳过该学生

    返回:
        dict: 包含生成结果的信息
    """
    try:
        # 获取所有项目
        projects = await Project.all()

        if not projects:
            return {"status": "warning", "message": "未找到任何项目，请确认项目表已创建且包含数据"}

        # 定义答辩阶段
        defense_phases = ["开题答辩", "中期答辩", "最终答辩"]

        defense_count = 0
        processed_students = 0
        skipped_students = 0

        for project in projects:
            # 获取学生信息
            queryset = await User.filter(student_id=project.student_id).first()
            student_name = queryset.username if queryset else "未知学生"

            # 检查是否已有3条答辩安排
            existing_defenses = await Defense.filter(student_id=project.student_id).count()
            if existing_defenses >= 3:
                skipped_students += 1
                continue

            processed_students += 1
            n = 1
            for phase in defense_phases:
                # 创建答辩数据
                defense_data = {
                    "project_title": project.title,
                    "student_name": student_name,
                    "student_id": project.student_id,
                    "teacher_name": project.teacher_name,
                    "defense_phase": phase,
                    "defense_class": f"教室30{n}",
                    "defense_group": f"第{n}组",
                    "status": "未开始",  # 默认状态
                    "defense_date": datetime.now().strftime("%Y-%m-%d"),
                }

                # 创建答辩记录
                await Defense.create(**defense_data)
                defense_count += 1
                n += 1

        return {
            "status": "success",
            "message": f"已为{processed_students}个项目创建了{defense_count}组答辩安排",
            "detail": {
                "total_projects": len(projects),
                "processed_students": processed_students,
                "skipped_students": skipped_students,
                "created_records": defense_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成答辩数据失败: {str(e)}")


@router.post("/gen_group_data",summary="生成学生对应评分组数据")
async def gen_group_data_endpoint(student_id,teacher_name1,teacher_name2,teacher_name3):
    """
    生成学生对应评分组数据
    :param student_id: 学生ID
    :param student_name: 学生姓名
    :param teacher_name1: 教师姓名1(对应指导教师)
    :param teacher_name2: 教师姓名2（对应评阅教师）
    :param teacher_name3: 教师姓名3（对应答辩委员会）
    :return: 成功消息
    """
    query_set = await User.filter(student_id=student_id).first()
    try:
        # 创建评分组数据
        await Group.create(
            student_id=student_id,
            student_name=query_set.username,
            teacher_name1=teacher_name1,
            teacher_name2=teacher_name2,
            teacher_name3=teacher_name3
        )
        return {"message": "评分组数据创建成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建评分组数据失败: {str(e)}")

from app.models.group import Group
from fastapi import APIRouter, HTTPException
from app.schemas.group import GroupOut
from utlis.score_docx import replace_text_in_docx
from app.models.user import User
from app.models.project import Project
from app.models.score_docx import ScoreDocx
from app.schemas.score_docx import BaseScoreDocx, ScoreDocxOut

import os

router = APIRouter()


@router.get("/{username}", response_model=list[GroupOut], summary="获取教师相关小组信息")
async def get_teacher_groups(username: str):
    """
    根据教师username获取相关的小组信息
    只要记录中的teacher_name1、teacher_name2或teacher_name3之一与username匹配即可返回
    """
    # 使用OR条件查询三个字段
    groups = await Group.filter(
        teacher_name1=username
    ).all() + await Group.filter(
        teacher_name2=username
    ).all() + await Group.filter(
        teacher_name3=username
    ).all()

    # 去重（避免同一条记录在多个字段匹配的情况下重复）
    unique_groups = []
    unique_ids = set()
    for group in groups:
        if group.id not in unique_ids:
            unique_groups.append(group)
            unique_ids.add(group.id)

    if not unique_groups:
        raise HTTPException(status_code=404, detail=f"未找到与教师 {username} 相关的小组信息")

    return unique_groups


# 根据学生id获取ScoreDocx记录（1条）
@router.get("/student/{student_id}", response_model=BaseScoreDocx, summary="获取学生的ScoreDocx记录")
async def get_student_score_docx(student_id: int):
    """
    根据学生id获取ScoreDocx记录
    """
    score_docx = await ScoreDocx.filter(student_id=student_id).first()
    if not score_docx:
        raise HTTPException(status_code=404, detail=f"未找到学生ID为 {student_id} 的ScoreDocx记录")
    return score_docx


# 根据学生id创建ScoreDocx记录
@router.post("/student/{student_id}", response_model=BaseScoreDocx, summary="创建学生的ScoreDocx记录")
async def create_student_score_docx(student_id: int, score_docx: BaseScoreDocx):
    """
    根据学生id创建ScoreDocx记录
    """
    # 检查学生是否存在
    student = await User.filter(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"未找到ID为 {student_id} 的学生")

    # 创建ScoreDocx记录
    score_docx_obj = await ScoreDocx.create(**score_docx.dict(), student_id=student_id)
    return score_docx_obj



# 根据学生id更新ScoreDocx记录
@router.put("/student/{student_id}", response_model=BaseScoreDocx, summary="更新学生的ScoreDocx记录")
async def update_student_score_docx(student_id: int, score_docx: BaseScoreDocx):
    """
    根据学生id更新ScoreDocx记录
    """
    # 检查学生是否存在
    student = await User.filter(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"未找到ID为 {student_id} 的学生")

    # 获取现有的ScoreDocx记录
    score_docx_obj = await ScoreDocx.filter(student_id=student_id).first()
    if not score_docx_obj:
        raise HTTPException(status_code=404, detail=f"未找到ID为 {student_id} 的ScoreDocx记录")

    # 更新ScoreDocx记录
    for key, value in score_docx.dict().items():
        setattr(score_docx_obj, key, value)

    # 保存并计算综合分数
    await score_docx_obj.save()

    # 根据学生id从Project获取一下题目
    project = await Project.filter(student_id=student_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"未找到ID为 {student_id} 的项目")
    score_docx_obj.project_title = project.title

    # 调用replace_text_in_docx函数生成Word文档
    project_root = 'D:\\Code\\demo\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id), 'score_docx')
    os.makedirs(output_dir, exist_ok=True)
    input_file = os.path.join(project_root, 'template', '本科毕业设计成绩评审表.docx')
    output_path = os.path.join(output_dir, f'{student_id}_本科毕业设计成绩评审表.docx')
    print(f"Output path: {output_path}")
    replacements = {
        "{题目}": score_docx_obj.project_title,
        "{学生姓名}": str(score_docx_obj.student_name),
        "{content1}": score_docx_obj.content1,
        "{score1}": str(score_docx_obj.score1),
        "{content2}": score_docx_obj.content2,
        "{score2}": str(score_docx_obj.score2),
        "{content3}": score_docx_obj.content3,
        "{score3}": str(score_docx_obj.score3),
        "{score4}": str(score_docx_obj.score4),
    }
    replace_text_in_docx(input_file, output_path, replacements)

    return score_docx_obj


# 学生根据学生id返回对应的成绩数据
@router.get("/student/{student_id}/score", response_model=ScoreDocxOut, summary="获取学生的成绩数据")
async def get_student_score(student_id: int):
    """
    根据学生id获取成绩数据
    """
    score_docx = await ScoreDocx.filter(student_id=student_id).first()
    if not score_docx:
        raise HTTPException(status_code=404, detail=f"未找到ID为 {student_id} 的成绩数据")
    return score_docx


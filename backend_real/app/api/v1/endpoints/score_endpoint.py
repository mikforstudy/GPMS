from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.models.score import Score
from app.schemas.score import ScoreIn, ScoreOut, BaseScore

router = APIRouter()


# 创建评分信息
@router.post("/create/", response_model=ScoreOut, summary="创建评分信息")
async def create_score(score: ScoreIn):
    score_obj = await Score.create(**score.model_dump())
    return score_obj


# 学生根据学生id查询评分信息（只会有一条信息）
@router.get("/student/{student_id}", response_model=ScoreOut, summary="学生查询评分信息")
async def get_score(student_id: int):
    score = await Score.filter(student_id=student_id).first()
    if score is None:
        # 根据你的需求返回适当的响应
        # 例如，返回 404 错误
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="评分信息不存在")
    return ScoreOut.model_validate(score)


# 教师根据username查询名下的所有所有学生的评分信息
@router.get("/teacher/{username}", response_model=list[ScoreOut], summary="教师查询评分信息")
async def get_scores(username: str):
    scores = await Score.filter(teacher_name=username).all()
    return [ScoreOut.model_validate(score) for score in scores]


# 教师根据学生id修改评分信息
@router.put("/{student_id}", response_model=ScoreOut, summary="教师修改评分信息")
async def update_score(student_id: int, score: ScoreIn):
    update_data = score.model_dump()
    update_data['update_time'] = datetime.now()

    await Score.filter(student_id=student_id).update(**update_data)
    score_obj = await Score.filter(student_id=student_id).first()
    if not score_obj:
        raise HTTPException(status_code=404, detail="评分信息不存在")
    return ScoreOut.model_validate(score_obj)

























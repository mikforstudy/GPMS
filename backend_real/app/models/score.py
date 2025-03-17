from tortoise import fields
from tortoise.models import Model


class Score(Model):
    """
    成绩表，用于记录成绩信息。
    """
    id = fields.IntField(pk=True, description="主键")
    project_title = fields.CharField(max_length=100, description="项目标题")
    student_name = fields.CharField(max_length=50, description="学生姓名")
    student_id = fields.IntField(description="学生ID")
    teacher_name = fields.CharField(max_length=50, description="导师姓名")
    score = fields.CharField(max_length=50, description="成绩")
    created_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "scores"
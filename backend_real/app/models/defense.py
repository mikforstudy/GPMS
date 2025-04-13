from tortoise import fields
from tortoise.models import Model

class Defense(Model):
    """
    答辩表，用于记录答辩信息。
    """
    id = fields.IntField(pk=True, description="主键")
    project_title = fields.CharField(max_length=100, description="项目标题")
    defense_class = fields.CharField(max_length=50, description="答辩教室")
    defense_group = fields.CharField(max_length=50, description="答辩组")
    defense_phase = fields.CharField(max_length=50, description="答辩阶段")
    defense_date = fields.DateField(description="答辩日期")
    student_name = fields.CharField(max_length=50, description="学生姓名")
    student_id = fields.IntField(description="学生ID")
    teacher_name = fields.CharField(max_length=50, description="导师姓名")
    created_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)
    status = fields.CharField(max_length=20, description="状态", default="未开始")

    class Meta:
        table = "defenses"
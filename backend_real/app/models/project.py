from tortoise import fields
from tortoise.models import Model


class Project(Model):
    """
    项目表，用于记录项目信息。
    """
    id = fields.IntField(pk=True, description="主键ID")
    title = fields.CharField(max_length=100, description="项目标题")
    description = fields.TextField(null=True, description="项目描述")
    status = fields.CharField(max_length=20, description="项目状态（开题，中期，项目答辩，完成）")
    start_date = fields.DateField(auto_now=True, description="开始日期")
    update_time = fields.DatetimeField(auto_now=True, description="更新日期")
    end_date = fields.DateField(null=True, description="结束日期")
    teacher_id = fields.IntField(description="导师ID")
    student_id = fields.IntField(description="学生ID")
    teacher_name = fields.CharField(max_length=50, description="导师姓名")


    class Meta:
        table = "projects"


    def __str__(self):
        return self.title



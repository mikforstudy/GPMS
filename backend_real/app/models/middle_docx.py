from tortoise import fields
from tortoise.models import Model


class MiddleDocx(Model):
    """
    中期检查表，用于记录中期检查信息。
    """
    id = fields.IntField(pk=True, description="主键")
    mark = fields.CharField(max_length=50, description="标记", default="中期检查")
    title = fields.CharField(max_length=100, description="中期检查标题")
    student_name = fields.CharField(max_length=50, description="学生姓名")
    student_id = fields.IntField(description="学生ID")
    teacher_name = fields.CharField(max_length=50, description="导师姓名")
    content1 = fields.TextField(description="第一部分内容")
    content6 = fields.TextField(description="第六部分内容")
    content7 = fields.TextField(description="第七部分内容")
    created_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now_add=True)
    status = fields.CharField(max_length=20, description="状态", default="待审核")

    class Meta:
        table = "middle_docxs"
from tortoise import fields
from tortoise.models import Model


class StartDocx(Model):
    """
    开题报告表，用于记录开题报告信息。
    """
    id = fields.IntField(pk=True, description="主键")
    mark = fields.CharField(max_length=50, description="标记", default="开题报告")
    title = fields.CharField(max_length=100, description="开题报告标题")
    student_name = fields.CharField(max_length=50, description="学生姓名")
    student_id = fields.IntField(description="学生ID")
    teacher_name = fields.CharField(max_length=50, description="导师姓名")
    content1 = fields.TextField(description="第一部分内容")
    content2 = fields.TextField(description="第二部分内容")
    content3 = fields.TextField(description="第三部分内容")
    content4 = fields.TextField(description="第四部分内容")
    content5 = fields.TextField(description="第五部分内容")
    content6 = fields.TextField(description="第六部分内容")
    created_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now_add=True)
    status = fields.CharField(max_length=20, description="状态", default="待审核")

    class Meta:
        table = "start_docxs"


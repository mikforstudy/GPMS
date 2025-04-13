from tortoise import fields
from tortoise.models import Model

class Group(Model):
    id = fields.IntField(pk=True, description="主键")
    student_id = fields.IntField(description="学生ID")
    student_name = fields.CharField(max_length=50, description="学生姓名")
    teacher_name1 = fields.CharField(max_length=50, description="受邀评阅教师1")
    teacher_name2 = fields.CharField(max_length=50, description="受邀评阅教师2")
    teacher_name3 = fields.CharField(max_length=50, description="受邀评阅教师3")

    class Meta:
        table = "groups"
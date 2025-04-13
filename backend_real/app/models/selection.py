from tortoise import fields
from tortoise.models import Model


class Selection(Model):
    """
    选题表，用于记录选题信息。
    """
    id = fields.IntField(pk=True, description="主键")
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    major = fields.CharField(max_length=100, description="专业")
    student_id = fields.IntField()
    teacher_id = fields.IntField()
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    status = fields.CharField(max_length=50, default="待审核")
    created_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "selections"

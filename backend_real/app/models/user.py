from tortoise import fields
from tortoise.models import Model


class User(Model):
    """
    用户表，用于记录用户信息。
    """
    id = fields.IntField(pk=True, description="主键")
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)
    role = fields.CharField(max_length=100)
    student_id = fields.IntField()
    teacher_id = fields.IntField()
    created_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username

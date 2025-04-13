from tortoise import fields
from tortoise.models import Model


class ScoreDocx(Model):
    """
    成绩单文档模型
    """
    id = fields.IntField(pk=True, description="主键")
    student_id = fields.IntField(null=True, description="学生ID")
    student_name = fields.CharField(max_length=50, null=True, description="学生姓名")
    content1 = fields.CharField(max_length=50, null=True, description="评语1")
    score1 = fields.IntField(null=True, description="评语1分数")
    content2 = fields.CharField(max_length=50, null=True, description="评语2")
    score2 = fields.IntField(null=True, description="评语2分数")
    content3 = fields.CharField(max_length=50, null=True, description="评语3")
    score3 = fields.IntField(null=True, description="评语3分数")
    score4 = fields.IntField(null=True, description="综合分数")

    async def save(self, *args, **kwargs):
        # 计算综合分数
        if self.score1 is not None and self.score2 is not None and self.score3 is not None:
            self.score4 = (self.score1 + self.score2 + self.score3) // 3
        await super().save(*args, **kwargs)

    class Meta:
        table = "score_docx"
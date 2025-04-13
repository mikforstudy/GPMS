from tortoise import fields
from tortoise.models import Model

class Phase(Model):
    id = fields.IntField(pk=True, description="主键")
    time1_1 = fields.DateField(description="选题开始时间")
    time1_2 = fields.DateField(description="选题结束时间")
    time2_1 = fields.DateField(description="开题开始时间")
    time2_2 = fields.DateField(description="开题结束时间")
    time3_1 = fields.DateField(description="中期开始时间")
    time3_2 = fields.DateField(description="中期结束时间")
    time4_1 = fields.DateField(description="论文开始时间")
    time4_2 = fields.DateField(description="论文结束时间")
    time5_1 = fields.DateField(description="答辩开始时间")
    time5_2 = fields.DateField(description="答辩结束时间")


    class Meta:
        table = "phase"
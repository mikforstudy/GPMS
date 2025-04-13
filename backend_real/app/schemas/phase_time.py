from typing import Optional
from pydantic import BaseModel

from typing import Optional
from pydantic import BaseModel
from datetime import date


class PhaseBase(BaseModel):
    """基础阶段时间模型"""
    time1_1: Optional[date] = None
    time1_2: Optional[date] = None
    time2_1: Optional[date] = None
    time2_2: Optional[date] = None
    time3_1: Optional[date] = None
    time3_2: Optional[date] = None
    time4_1: Optional[date] = None
    time4_2: Optional[date] = None
    time5_1: Optional[date] = None
    time5_2: Optional[date] = None


class PhaseCreate(PhaseBase):
    """创建阶段时间模型"""
    pass


class PhaseUpdate(PhaseBase):
    """更新阶段时间模型"""
    pass


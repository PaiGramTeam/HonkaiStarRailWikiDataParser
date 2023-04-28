# 材料
from pydantic import BaseModel

from .enums import Quality, MaterialType


class Material(BaseModel):
    id: int
    """材料ID"""
    name: str
    """名称"""
    desc: str
    """介绍"""
    icon: str
    """图标"""
    quality: Quality
    """稀有度"""
    type: MaterialType
    """类型"""

# 敌对物种
from pydantic import BaseModel

from models.enums import MonsterType, Area


class Monster(BaseModel):
    id: int
    """怪物ID"""
    name: str
    """名称"""
    desc: str
    """介绍"""
    icon: str
    """图标"""
    big_pic: str
    """大图"""
    type: MonsterType
    """种类"""
    area: Area
    """地区"""
    resistance: str
    """抗性"""
    find_area: str
    """发现地点"""


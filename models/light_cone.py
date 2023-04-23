# 光锥
from pydantic import BaseModel

from typing import TYPE_CHECKING

from models.enums import Quality, Destiny

if TYPE_CHECKING:
    from models.material import Material


class LightConeItem(BaseModel):
    item: "Material"
    """物品"""
    count: int
    """数量"""


class LightConePromote(BaseModel):
    required_level: int = 0
    """突破所需等级"""
    promote_level: int = 0
    """突破等级"""
    max_level: int
    """解锁的等级上限"""

    coin: int = 0
    """信用点"""
    items: list[LightConeItem]
    """突破所需材料"""


class LightCone(BaseModel):
    id: int
    """"光锥ID"""
    name: str
    """名称"""
    desc: str
    """描述"""
    icon: str
    """图标"""
    big_pic: str
    """大图"""
    quality: Quality
    """稀有度"""
    destiny: Destiny
    """命途"""
    promote: list[LightConePromote]
    """晋阶信息"""

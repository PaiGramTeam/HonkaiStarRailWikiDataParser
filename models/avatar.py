from typing import List
from pydantic import BaseModel
from models.enums import Quality, Destiny, Element
from models.material import Material


class AvatarInfo(BaseModel):
    occupation: str = ""
    """所属"""
    faction: str = ""
    """派系"""


class AvatarItem(BaseModel):
    item: Material
    """物品"""
    count: int
    """数量"""


class AvatarPromote(BaseModel):
    required_level: int
    """突破所需等级"""
    promote_level: int = 0
    """突破等级"""
    max_level: int
    """解锁的等级上限"""

    coin: int = 0
    """信用点"""
    items: list[AvatarItem]
    """突破所需材料"""


class AvatarSoul(BaseModel):
    name: str
    """ 名称 """
    desc: str
    """ 介绍 """


class Avatar(BaseModel):
    id: int
    """角色ID"""
    name: str
    """名称"""
    quality: Quality
    """品质"""
    destiny: Destiny
    """命途"""
    element: Element
    """属性"""
    information: AvatarInfo
    """角色信息"""
    promote: List[AvatarPromote]
    """角色突破数据"""
    soul: List[AvatarSoul]
    """角色星魂数据"""

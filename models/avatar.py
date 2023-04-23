from typing import List, TYPE_CHECKING
from pydantic import BaseModel
from models.enums import Quality, Destiny, Element


if TYPE_CHECKING:
    from models.material import Material


class AvatarInfo(BaseModel):
    occupation: str
    """所属"""
    faction: str
    """派系"""


class AvatarItem(BaseModel):
    item: "Material"
    """物品"""
    count: int
    """数量"""


class AvatarPromote(BaseModel):
    required_level: int = 0
    """突破所需等级"""
    promote_level: int = 0
    """突破等级"""
    max_level: int
    """解锁的等级上限"""
    before_hp: int
    """突破前生命值"""
    after_hp: int
    """突破后生命值"""
    before_attack: int
    """突破前攻击力"""
    after_attack: int
    """突破后攻击力"""
    before_defense: int
    """突破前防御力"""
    after_defense: int
    """突破后防御力"""

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

from typing import List

from pydantic import BaseModel


class AvatarName(BaseModel):
    Hash: int


class AvatarConfig(BaseModel):
    name: str = ""
    AvatarID: int
    AvatarName: AvatarName
    AvatarVOTag: str
    Release: bool


class AvatarIcon(BaseModel):
    id: int
    """角色ID"""
    name: str
    """名称"""
    icon: List[str]
    """图标（从小到大）"""

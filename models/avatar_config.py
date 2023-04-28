from typing import List, Optional

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

    @property
    def gacha(self) -> str:
        return self.icon[3]

    @property
    def icon_(self) -> str:
        return self.icon[0]

    @property
    def square(self) -> Optional[str]:
        return self.icon[1]

    @property
    def normal(self) -> str:
        return self.icon[2]

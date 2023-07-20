from typing import List, Optional

from pydantic import BaseModel

from .enums import Destiny, Element


class YattaAvatarPath(BaseModel):
    id: str
    name: str


class YattaAvatarTypes(BaseModel):
    pathType: YattaAvatarPath
    combatType: YattaAvatarPath


class YattaAvatarCV(BaseModel):
    CV_CN: str
    CV_JP: str
    CV_KR: str
    CV_EN: str


class YattaAvatarFetter(BaseModel):
    faction: Optional[str]
    description: Optional[str]
    cv: Optional[YattaAvatarCV]


class YattaAvatarEidolon(BaseModel):
    id: int
    rank: int
    name: Optional[str]
    description: Optional[str]
    icon: str

    @property
    def icon_url(self) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/skill/{self.icon}.png"


class YattaAvatar(BaseModel):
    id: int
    """ 角色ID """
    name: str
    """ 名称 """
    rank: int
    """ 星级 """
    types: YattaAvatarTypes
    """ 角色类型 """
    icon: str
    """ 图标 """
    release: int
    """ 上线时间 """
    route: str
    fetter: YattaAvatarFetter
    eidolons: List[YattaAvatarEidolon]

    @property
    def destiny(self) -> Destiny:
        """ 命途 """
        return Destiny(self.types.pathType.name)

    @property
    def element(self) -> Element:
        """ 属性 """
        return Element(self.types.combatType.name)

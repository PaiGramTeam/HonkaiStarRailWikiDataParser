from typing import List, Optional

from pydantic import BaseModel, root_validator

from res_func.url import avatar_skill_url


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
    name: str
    description: str
    icon: str

    @property
    def icon_url(self) -> str:
        return f"{avatar_skill_url}{self.icon}.png"


class YattaAvatar(BaseModel):
    id: int
    name: str
    rank: int
    types: YattaAvatarTypes
    icon: str
    release: int
    route: str
    fetter: YattaAvatarFetter
    eidolons: List[YattaAvatarEidolon]

    @root_validator(pre=True)
    def validate(cls, values):
        if values.get("eidolons") is None:
            values["eidolons"] = []
        else:
            eidolons = []
            for eidolon in values["eidolons"].values():
                eidolons.append(eidolon)
            values["eidolons"] = eidolons
        return values

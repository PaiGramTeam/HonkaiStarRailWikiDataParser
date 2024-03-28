from typing import List, Optional

from pydantic import BaseModel


class HeadIcon(BaseModel):
    id: int
    name: str
    desc: str
    bg_desc: str
    avatar_id: Optional[int] = None
    icons: List[str]

    @property
    def webp(self) -> str:
        return self.icons[0]

    @property
    def png(self) -> str:
        return self.icons[1]


# 原始数据


class ForHash(BaseModel):
    Hash: str


class ItemPlayerCard(BaseModel):
    ID: int
    ItemSubType: str
    ItemName: ForHash
    ItemDesc: ForHash
    ItemBGDesc: ForHash


class PlayerIcon(BaseModel):
    ID: int
    ImagePath: str


class AvatarPlayerIcon(PlayerIcon):
    AvatarID: int

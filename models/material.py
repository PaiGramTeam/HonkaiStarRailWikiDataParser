# 材料

from pydantic import BaseModel


class MaterialSource(BaseModel):
    description: str


class MaterialMType(BaseModel):
    id: int
    name: str


class YattaMaterial(BaseModel):
    id: int
    """材料ID"""
    name: str
    """名称"""
    description: str
    """描述"""
    story: str | None = None
    """故事"""
    rank: int
    """稀有度"""
    source: list[MaterialSource]
    """来源"""
    type: MaterialMType | None = None
    """类型"""
    route: str

    @property
    def icon(self) -> str:
        return f"https://sr.yatta.moe/hsr/assets/UI/item/{self.id}.png"

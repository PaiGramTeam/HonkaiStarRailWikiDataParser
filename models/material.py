# 材料
from typing import List, Optional

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
    story: str
    """故事"""
    rank: int
    """稀有度"""
    source: List[MaterialSource]
    """来源"""
    type: Optional[MaterialMType] = None
    """类型"""
    route: str

    @property
    def icon(self) -> str:
        return f"https://api.yatta.top/hsr/assets/UI/item/{self.id}.png"

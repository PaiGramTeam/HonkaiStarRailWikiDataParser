# 光锥
from pydantic import BaseModel


class YattaLightConePath(BaseModel):
    id: str
    name: str


class YattaLightConeTypes(BaseModel):
    pathType: YattaLightConePath


class YattaLightCone(BaseModel):
    id: int
    """"光锥ID"""
    name: str
    """名称"""
    description: str
    """描述"""
    icon: str = ""
    """图标"""
    big_pic: str = ""
    """大图"""
    rank: int
    """稀有度"""
    types: YattaLightConeTypes
    """命途"""
    route: str


from pydantic import BaseModel


class PhoneTheme(BaseModel):
    id: int
    """ID"""
    name: str
    """名称"""
    description: str
    """描述"""
    story: str | None = None
    """故事"""
    urls: list[str]


# 原始数据


class PhoneThemeConfig(BaseModel):
    ID: int
    PhoneThemeMain: str

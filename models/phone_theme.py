from typing import Optional, List

from pydantic import BaseModel


class PhoneTheme(BaseModel):
    id: int
    """ID"""
    name: str
    """名称"""
    description: str
    """描述"""
    story: Optional[str] = None
    """故事"""
    urls: List[str]


# 原始数据


class PhoneThemeConfig(BaseModel):
    ID: int
    PhoneThemeMain: str

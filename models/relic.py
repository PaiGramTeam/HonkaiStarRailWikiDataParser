# 遗器套装
from typing import List

from pydantic import BaseModel


class YattaRelic(BaseModel):
    id: int
    """遗器套装ID"""
    name: str
    """套装名称"""
    icon: str
    """套装图标"""
    image_list: List[str] = []
    """套装子图"""
    route: str

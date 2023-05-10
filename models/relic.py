# 遗器套装
from typing import List

from pydantic import BaseModel


class Relic(BaseModel):
    id: int
    """遗器套装ID"""
    bbs_id: int
    """WIKI ID"""
    name: str
    """套装名称"""
    icon: str
    """套装图标"""
    affect: str
    """套装效果"""
    image_list: List[str]
    """套装子图"""

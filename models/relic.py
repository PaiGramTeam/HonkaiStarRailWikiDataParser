# 遗器套装
from pydantic import BaseModel


class Relic(BaseModel):
    id: int
    """遗器套装ID"""
    name: str
    """套装名称"""
    icon: str
    """套装图标"""
    affect: str
    """套装效果"""

from typing import List

from pydantic import BaseModel


class LightConeIcon(BaseModel):
    id: int
    """光锥ID"""
    name: str
    """名称"""
    icon: List[str]
    """图标（从小到大）"""

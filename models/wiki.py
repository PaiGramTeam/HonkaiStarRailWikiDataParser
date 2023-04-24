from typing import List, Dict

import ujson
from pydantic import BaseModel


class Content(BaseModel):
    content_id: int
    """内容ID"""
    ext: str
    """扩展信息"""
    icon: str
    """图标"""
    summary: str
    """摘要"""
    title: str
    """标题"""
    article_user_name: str = ""
    """作者"""
    bbs_url: str = ""
    """BBS对应地址"""

    @property
    def data(self) -> Dict:
        return ujson.loads(self.ext)


class Children(BaseModel):
    id: int
    """分类ID"""
    name: str
    """分类名称"""
    list: List[Content]
    """内容列表"""

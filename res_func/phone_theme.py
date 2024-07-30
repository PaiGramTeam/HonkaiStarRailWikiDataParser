from pathlib import Path
from typing import List

import aiofiles
import ujson

from models.phone_theme import PhoneTheme, PhoneThemeConfig
from func.data import all_materials_map, read_materials

from .base_data import get_base_data
from .client import client
from .url import phone_theme_url, hoyoverse_game_url, mihoyo_game_url

data_path = Path("data")


async def get_phone_theme() -> List[PhoneThemeConfig]:
    data = await get_base_data(phone_theme_url)
    datas = []
    for i in data:
        datas.append(PhoneThemeConfig(**i))
    return datas


async def test_url(base: str, path: str) -> str:
    url = f"{base}{path}"
    data = await client.head(url)
    if data.status_code != 200:
        return ""
    return url


async def gen_phone_theme(themes: List[PhoneThemeConfig]) -> List[PhoneTheme]:
    await read_materials()
    datas = []
    for theme in themes:
        info = all_materials_map.get(theme.ID)
        name, desc, story = "", "", ""
        if info:
            name = info.name
            desc = info.description
            story = info.story
        h_url = await test_url(hoyoverse_game_url, theme.PhoneThemeMain)
        m_url = await test_url(mihoyo_game_url, theme.PhoneThemeMain)
        urls = [h_url, m_url]
        datas.append(
            PhoneTheme(
                id=theme.ID,
                name=name,
                description=desc,
                story=story,
                urls=urls,
            )
        )
    return datas


async def dump_themes(path: Path, datas: List[PhoneTheme]):
    data = [theme.dict() for theme in datas]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def get_phone_themes():
    print("获取手机主题数据")
    themes = await get_phone_theme()
    datas = await gen_phone_theme(themes)
    await dump_themes(data_path / "phone_themes.json", datas)
    print("手机主题数据获取完成")

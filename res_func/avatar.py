import asyncio
from pathlib import Path
from typing import Dict, List

import aiofiles
import ujson
from bs4 import BeautifulSoup, Tag

from func.fetch_avatars import read_avatars, all_avatars_name, dump_avatars
from .client import client
from .url import avatar_config, text_map, base_station_url, avatar_url
from models.avatar_config import AvatarConfig, AvatarIcon


async def fetch_text_map() -> Dict[str, str]:
    res = await client.get(text_map)
    return res.json()


async def fetch_config(text_map_data: Dict[str, str]) -> List[AvatarConfig]:
    res = await client.get(avatar_config)
    data = res.json()
    datas = []
    for i in data.values():
        a = AvatarConfig(**i)
        a.name = text_map_data[str(a.AvatarName.Hash)]
        datas.append(a)
    return datas


async def parse_station(datas, name: str, tag: Tag, avatar: AvatarConfig):
    second_pic = ""
    if avatar_model := all_avatars_name.get(name):
        second_pic = avatar_model.icon
    third_pic = f'{base_station_url}{tag.find("img").get("src")}'
    html = await client.get(f'{base_station_url}{tag.get("href")}')
    soup = BeautifulSoup(html.text, "lxml")
    text = soup.find("div", {"class": "a6678 a4af5"}).get("style")
    four_pic = f'{base_station_url}{text[text.find("(") + 2:text.find(")") - 1]}' if text else ""
    first_pic = f'{base_station_url}{soup.find("img", {"class": "ac39b a6602"}).get("src")}'
    datas.append(
        AvatarIcon(
            id=avatar.AvatarID,
            name=avatar.name,
            icon=[first_pic, second_pic, third_pic, four_pic],
        )
    )


async def dump_icons(path: Path, datas: List[AvatarIcon]):
    data = [icon.dict() for icon in datas]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def fetch_station(configs_map: Dict[str, AvatarConfig]) -> List[AvatarIcon]:
    print("开始获取角色素材")
    html = await client.get(avatar_url)
    soup = BeautifulSoup(html.text, "lxml")
    avatars = soup.find_all("a", {"class": "char-entry-select-option"})
    tasks = []
    datas: List[AvatarIcon] = []
    ktz = False
    for avatar in avatars:
        name = avatar.find("span").get_text().strip()
        if name == "开拓者" and ktz:
            continue
        if avatar_model := configs_map.get(name):
            tasks.append(parse_station(datas, name, avatar, avatar_model))
            if name == "开拓者":
                ktz = True
        else:
            print(f"未找到角色 {name} 的数据")
    await asyncio.gather(*tasks)
    return datas


async def fix_avatar_config(text_map_data: Dict[str, str]):
    configs = await fetch_config(text_map_data)
    configs_map: Dict[str, AvatarConfig] = {config.name: config for config in configs}
    configs_map["开拓者"] = configs_map["{NICKNAME}"]
    print(f"读取到原始数据：{list(configs_map.keys())}")
    data_path = Path("data")
    await read_avatars(data_path / "avatars.json")
    for key, value in all_avatars_name.items():
        if key.startswith("开拓者"):
            config = configs_map["{NICKNAME}"]
            config.name = "开拓者"
        else:
            config = configs_map.get(key)
        if config is None:
            print(f"错误：未找到角色 {key} 的配置")
            continue
        value.id = config.AvatarID
    icons = await fetch_station(configs_map)
    await dump_icons(data_path / "avatar_icons.json", icons)
    await dump_avatars(data_path / "avatars.json")

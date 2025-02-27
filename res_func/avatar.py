import asyncio
import re
from pathlib import Path
from typing import Dict, List, Optional

import aiofiles
import ujson
from bs4 import BeautifulSoup, Tag

from func.data import all_avatars_map, all_avatars_name, read_avatars, dump_avatars
from models.avatar_config import AvatarConfig, AvatarIcon
from .base_data import get_base_data
from .client import client
from .url import avatar_config, text_map, base_station_url, avatar_url

TRAVER_DATA_MAP = {
    "开拓者·毁灭": (8001, 8002),
    "开拓者·存护": (8003, 8004),
    "开拓者·同谐": (8005, 8006),
    "开拓者·记忆": (8007, 8008),
}


async def fetch_text_map() -> Dict[str, str]:
    return await get_base_data(text_map)


async def fetch_config() -> List[AvatarConfig]:
    text_map_data = await get_base_data(text_map)
    data = await get_base_data(avatar_config)
    datas = []
    for i in data:
        a = AvatarConfig(**i)
        a.name = text_map_data[str(a.AvatarName.Hash)]
        datas.append(a)
    return datas


async def parse_station(datas, name: str, tag: Tag, cid: int):
    html = await client.get(f"{base_station_url}{tag.get('href')}")
    if not cid:
        reg = r'skillTreePoints":\[{"id":(\d+),'
        cid = int(re.findall(reg, html.text)[0][:-3])
    soup = BeautifulSoup(html.text, "lxml")
    second_pic = ""
    if avatar_model := all_avatars_map.get(cid):
        second_pic = avatar_model.icon
    elif avatar_model := all_avatars_name.get(name):
        second_pic = avatar_model.icon

    def get_third_pic():
        _tag = tag.find("div", {"class": "a69d1"})
        style = _tag.get("style")
        return f"{style[style.find('(') + 1 : style.find(')')]}"

    third_pic = get_third_pic()
    text = soup.find_all("div", {"class": "a4af5"})[1].get("style")
    four_pic = f"{text[text.find('(') + 2 : text.find(')') - 1]}" if text else ""
    first_pic = f"{soup.find('img', {'class': 'ac39b a6602'}).get('src')}"
    datas.append(
        AvatarIcon(
            id=cid,
            name=name,
            icon=[first_pic, second_pic, third_pic, four_pic],
        )
    )


async def dump_icons(path: Path, datas: List[AvatarIcon]):
    data = [icon.dict() for icon in datas]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def load_icons(path: Path) -> List[AvatarIcon]:
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        data = await f.read()
    return [AvatarIcon(**i) for i in ujson.loads(data)]


async def fetch_station_ktz(tasks, datas, player_avatars: List[Tag]):
    idx = 0
    for key, value in TRAVER_DATA_MAP.items():
        tasks.append(parse_station(datas, key, player_avatars[idx], value[0]))
        tasks.append(parse_station(datas, key, player_avatars[idx + 1], value[1]))
        idx += 2


async def fetch_station(configs_map: Dict[str, AvatarConfig]) -> List[AvatarIcon]:
    print("开始获取角色素材")
    html = await client.get(avatar_url)
    soup = BeautifulSoup(html.text, "lxml")
    avatars = soup.find_all("a", {"class": "a7916"})
    tasks = []
    datas: List[AvatarIcon] = []
    player_avatars = []
    for avatar in avatars:
        name = avatar.find("div", {"class": "ellipsis"}).get_text().strip()
        if name == "开拓者":
            player_avatars.append(avatar)
            continue
        avatar_model = configs_map.get(name)
        tasks.append(
            parse_station(
                datas, name, avatar, avatar_model.AvatarID if avatar_model else None
            )
        )
    await fetch_station_ktz(tasks, datas, player_avatars)
    await asyncio.gather(*tasks)
    return datas


async def fix_avatar_config_ktz():
    for key, value in TRAVER_DATA_MAP.items():
        for i in value:
            all_avatars_map[i].name = key


async def fix_mult_avatar_config(configs_map: Dict[str, Optional[AvatarConfig]]):
    configs_map["三月七"] = None


async def fix_avatar_config():
    configs = await fetch_config()
    configs_map: Dict[str, Optional[AvatarConfig]] = {
        config.name: config for config in configs
    }
    await fix_mult_avatar_config(configs_map)
    print(f"读取到原始数据：{list(configs_map.keys())}")
    data_path = Path("data")
    await read_avatars()
    await fix_avatar_config_ktz()
    icons = await fetch_station(configs_map)
    await dump_icons(data_path / "avatar_icons.json", icons)
    await dump_avatars()

from pathlib import Path
from typing import List, Dict

import aiofiles
import ujson
from bs4 import BeautifulSoup

from models.head_icon import HeadIcon, ItemPlayerCard, PlayerIcon, AvatarPlayerIcon

from .avatar import load_icons
from .base_data import get_base_data
from .client import client
from .url import avatar_player_icon_url, player_icon_url, item_player_card_url, text_map, icons_url, base_enka_url

data_path = Path("data")


async def get_text_map() -> dict[str, str]:
    return await get_base_data(text_map)


async def get_avatar_player_icon() -> List[AvatarPlayerIcon]:
    data = await get_base_data(avatar_player_icon_url)
    datas = []
    for i in data.values():
        datas.append(AvatarPlayerIcon(**i))
    return datas


async def get_player_icon() -> List[PlayerIcon]:
    data = await get_base_data(player_icon_url)
    datas = []
    for i in data.values():
        datas.append(PlayerIcon(**i))
    return datas


async def get_item_player_card() -> List[ItemPlayerCard]:
    data = await get_base_data(item_player_card_url)
    datas = []
    for i in data.values():
        datas.append(ItemPlayerCard(**i))
    return datas


async def parse_station_urls() -> Dict[str, str]:
    data = await client.get(icons_url)
    soup = BeautifulSoup(data.text, "lxml")
    a_s = soup.find_all("a", {"class": "a4041 af418 a4294"})
    datas = {}
    for a in a_s:
        img = a.find("img")
        span = a.find("span")
        datas[span.get_text().strip()] = img.get("src")
    return datas


async def test_enka_url(path: str) -> str:
    url = f"{base_enka_url}{path}"
    data = await client.head(url)
    if data.status_code != 200:
        return ""
    return url


async def extra_head_icons(item_player_card: List[ItemPlayerCard], player_icon: List[PlayerIcon]) -> List[HeadIcon]:
    player_icon_map: Dict[int, PlayerIcon] = {i.ID: i for i in player_icon}
    text_map_ = await get_text_map()
    station_urls = await parse_station_urls()
    datas = []
    for item in item_player_card:
        if item.ItemSubType != "HeadIcon":
            continue
        id_ = item.ID
        name = text_map_[item.ItemName.Hash]
        desc = text_map_.get(item.ItemDesc.Hash, "")
        bg_desc = text_map_.get(item.ItemBGDesc.Hash, "")
        icon = player_icon_map[id_].ImagePath
        station_url = station_urls.get(name, "")
        enka_url = await test_enka_url(icon)
        icons = [station_url, enka_url]
        datas.append(HeadIcon(id=id_, name=name, desc=desc, bg_desc=bg_desc, icons=icons))
    return datas


async def dump_icons(path: Path, datas: List[HeadIcon]):
    data = [icon.dict() for icon in datas]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def avatar_head_icons(avatar_player_icon: List[AvatarPlayerIcon]):
    avatar_icons = await load_icons(data_path / "avatar_icons.json")
    avatar_icons_map = {i.id: i for i in avatar_icons}
    datas = []
    for i in avatar_player_icon:
        avatar = avatar_icons_map.get(i.AvatarID)
        name = avatar.name
        station_url = avatar.icon_ or ""
        enka_url = await test_enka_url(i.ImagePath)
        icons = [station_url, enka_url]
        datas.append(HeadIcon(id=i.ID, name=name, desc="", bg_desc="", avatar_id=i.AvatarID, icons=icons))
    return datas


async def get_head_icons():
    print("开始获取头像素材")
    item_player_card = await get_item_player_card()
    player_icon = await get_player_icon()
    avatar_player_icon = await get_avatar_player_icon()
    print("开始获取特殊头像")
    datas = await extra_head_icons(item_player_card, player_icon)
    print("开始获取角色头像")
    datas.extend(await avatar_head_icons(avatar_player_icon))
    await dump_icons(data_path / "head_icons.json", datas)
    print("头像素材获取完毕")

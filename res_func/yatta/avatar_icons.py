from pathlib import Path
from typing import Any

import aiofiles
import ujson

from func.client import retry
from func.data import read_avatars, dump_avatars, all_avatars_map, all_avatars_name
from models.avatar_config import AvatarIcon
from res_func.client import client
from res_func.url import avatar_yatta_url, avatar_assets_url

TRAVER_DATA_MAP = {
    "开拓者·毁灭": (8001, 8002),
    "开拓者·存护": (8003, 8004),
    "开拓者·同谐": (8005, 8006),
    "开拓者·记忆": (8007, 8008),
    "开拓者·欢愉": (8009, 8010),
}


async def dump_icons(path: Path, datas: list[AvatarIcon]):
    data = [icon.dict() for icon in datas]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def load_icons(path: Path) -> list[AvatarIcon]:
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        data = await f.read()
    return [AvatarIcon(**i) for i in ujson.loads(data)]


@retry
async def get_all_avatar() -> dict[str, Any]:
    req = await client.get(avatar_yatta_url)
    return req.json()["data"]["items"]


async def parse_data(cid: int, name: str, second_pic: str) -> "AvatarIcon":
    first_pic = f"{avatar_assets_url}/round/{cid}.png"
    third_pic = f"{avatar_assets_url}/medium/{cid}.png"
    four_pic = f"{avatar_assets_url}/large/{cid}.sm.png"

    return AvatarIcon(
        id=cid,
        name=name,
        icon=[first_pic, second_pic, third_pic, four_pic],
    )


async def fetch_data() -> list[AvatarIcon]:
    datas: list[AvatarIcon] = []
    avatar_map = all_avatars_map.copy()
    for k, v in avatar_map.items():
        cid = k
        name = v.name
        second_pic = v.icon
        data = await parse_data(cid, name, second_pic)
        datas.append(data)
    return datas


async def fix_avatar_config():
    data_path = Path("data")
    await read_avatars()
    icons = await fetch_data()
    await dump_icons(data_path / "avatar_icons.json", icons)
    await dump_avatars()

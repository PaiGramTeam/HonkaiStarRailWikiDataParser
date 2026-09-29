from pathlib import Path
from typing import List

import aiofiles
import ujson

from func.data import all_light_cones_map, read_light_cones, dump_light_cones
from models.light_cone_config import LightConeIcon
from res_func.url import light_cone_assets_url


async def dump_icons(path: Path, datas: List[LightConeIcon]):
    data = [icon.dict() for icon in datas]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def parse_data(cid: int, name: str) -> "LightConeIcon":
    first_pic = f"{light_cone_assets_url}/medium/{cid}.png"
    second_pic = f"{light_cone_assets_url}/large/{cid}.png"

    return LightConeIcon(
        id=cid,
        name=name,
        icon=[first_pic, second_pic],
    )


async def fetch_data() -> list[LightConeIcon]:
    datas: list[LightConeIcon] = []
    avatar_map = all_light_cones_map.copy()
    for k, v in avatar_map.items():
        cid = k
        name = v.name
        data = await parse_data(cid, name)
        v.icon = data.icon_
        v.big_pic = data.gacha
        datas.append(data)
    return datas


async def fix_light_cone_config():
    data_path = Path("data")
    await read_light_cones()
    icons = await fetch_data()
    await dump_icons(data_path / "light_cone_icons.json", icons)
    await dump_light_cones()

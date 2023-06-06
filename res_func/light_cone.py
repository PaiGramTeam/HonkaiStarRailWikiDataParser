import asyncio
from pathlib import Path
from typing import List

import aiofiles
import ujson
from bs4 import BeautifulSoup, Tag

from func.fetch_light_cones import read_light_cones, all_light_cones_name, dump_light_cones
from .client import client
from .url import base_station_url, light_cone_url
from models.light_cone_config import LightConeIcon


async def parse_station(icon: LightConeIcon, tag: Tag):
    html = await client.get(f'{base_station_url}{tag.get("href")}')
    soup = BeautifulSoup(html.text, "lxml")
    first_pic = f'{base_station_url}{soup.find("img", {"class": "standard-icon a6602"}).get("src")}'
    second_pic = f'{base_station_url}{soup.find("img", {"class": "a2b16 mobile-only-elem ab8c3"}).get("src")}'
    icon.icon = [first_pic, second_pic]


async def dump_icons(path: Path, datas: List[LightConeIcon]):
    data = [icon.dict() for icon in datas]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def fetch_station() -> List[LightConeIcon]:
    print("开始获取光锥素材")
    html = await client.get(light_cone_url)
    soup = BeautifulSoup(html.text, "lxml")
    light_cones = soup.find_all("a", {"class": "a4041"})
    tasks = []
    datas: List[LightConeIcon] = []
    for light_cone in light_cones:
        name = light_cone.find("span").get_text().strip()
        url = light_cone.get("href")
        if not url:
            continue
        if "lightcone/" not in url:
            continue
        nid = int(url.split("/")[-1])
        if light_cone_model := all_light_cones_name.get(name):
            light_cone_model.id = nid
        else:
            print(f"wiki 未找到光锥数据 {name} ，修复 id 失败")
        icon = LightConeIcon(
            id=nid,
            name=name,
            icon=[]
        )
        datas.append(icon)
        tasks.append(parse_station(icon, light_cone))
    await asyncio.gather(*tasks)
    return datas


async def fix_light_cone_config():
    data_path = Path("data")
    await read_light_cones(data_path / "light_cones.json")
    icons = await fetch_station()
    await dump_icons(data_path / "light_cone_icons.json", icons)
    await dump_light_cones(data_path / "light_cones.json")

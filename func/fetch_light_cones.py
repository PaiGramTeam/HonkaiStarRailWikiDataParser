import asyncio
import re
from pathlib import Path
from typing import List, Dict

import aiofiles
import ujson
from bs4 import BeautifulSoup

from func.client import client
from func.fetch_materials import all_materials_map, all_materials_name
from func.url import info_url
from models.enums import Quality, Destiny
from models.light_cone import LightCone, LightConePromote, LightConeItem
from models.wiki import Children

all_light_cones: List[LightCone] = []
all_light_cones_name: Dict[str, LightCone] = {}


async def fetch_light_cones(data: Children):
    for content in data.list:
        m_destiny = Destiny(re.findall(r'命途/(.*?)\\', content.ext)[0])
        m_quality = Quality(re.findall(r'星级/(.*?)\\', content.ext)[0])
        light_cone = LightCone(
            id=content.content_id,
            name=content.title,
            desc=content.summary,
            icon=content.icon,
            big_pic="",
            quality=m_quality,
            destiny=m_destiny,
            promote=[],
        )
        all_light_cones.append(light_cone)
        all_light_cones_name[light_cone.name] = light_cone


def parse_promote(light_cone: LightCone, soup: BeautifulSoup) -> None:
    """解析光锥突破数据"""
    mater = soup.find("div", {"data-part": "material"})
    trs = mater.find_all("tr")
    required_levels = [20, 30, 40, 50, 60, 70]
    max_level = [30, 40, 50, 60, 70, 80]
    for i in range(0, min(len(trs), 6)):
        promote = LightConePromote(
            required_level=required_levels[i],
            max_level=max_level[i],
            items=[],
        )
        materials = trs[i].find_all("li", {"class": "obc-tmpl__material-item"})
        for material in materials:
            try:
                mid = int(re.findall(r"content/(\d+)/detail", material.find("a").get("href"))[0])
            except AttributeError:
                continue
            name = material.find("p", {"class": "obc-tmpl__material-name"}).text
            item = all_materials_map.get(mid)
            if not item:
                item = all_materials_name.get(name)
            try:
                count = int(material.find("span", {"class": "obc-tmpl__material-num"}).text)
            except (AttributeError, ValueError):
                count = 1
            if name == "信用点":
                promote.coin = count
            elif item:
                promote.items.append(
                    LightConeItem(
                        item=item,
                        count=count,
                    )
                )
            else:
                print(f"unknown material: {mid}: {name}")
        light_cone.promote.append(promote)


async def fetch_info(light_cone: LightCone):
    print(f"Fetch light_cone info: {light_cone.id}: {light_cone.name}")
    params = {
        'app_sn': 'sr_wiki',
        'content_id': str(light_cone.id),
    }
    resp = await client.get(info_url, params=params)
    data = resp.json()["data"]["content"]["contents"][0]["text"]
    soup = BeautifulSoup(data, "lxml")
    table = soup.find("table", {"class": "obc-tml-light-table--pc"})
    tr = table.find_all("tr")[-1]
    td = tr.find_all("td")[-1]
    light_cone.desc = td.get_text().strip()
    pic_td = soup.find("td", {"class": "obc-tmpl-character__avatar"})
    light_cone.big_pic = pic_td.find("img").get("src")
    parse_promote(light_cone, soup)


async def fetch_light_cones_infos():
    tasks = []
    for light_cone in all_light_cones:
        tasks.append(fetch_info(light_cone))
    await asyncio.gather(*tasks)


async def dump_light_cones(path: Path):
    data = [light_cone.dict() for light_cone in all_light_cones]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_light_cones(path: Path):
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    all_light_cones.clear()
    all_light_cones_name.clear()
    for light_cone in data:
        m = LightCone(**light_cone)
        all_light_cones.append(m)
        all_light_cones_name[m.name] = m

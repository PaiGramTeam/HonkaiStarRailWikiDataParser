import re
import asyncio
from pathlib import Path
from typing import List, Dict

import aiofiles
import ujson
from bs4 import BeautifulSoup

from func.client import client
from func.url import info_url
from models.wiki import Children
from models.enums import Quality, MaterialType
from models.material import Material

star_map = {
    1: Quality.One,
    2: Quality.Two,
    3: Quality.Three,
    4: Quality.Four,
    5: Quality.Five,
}
all_materials: List[Material] = []
all_materials_map: Dict[int, Material] = {}
all_materials_name: Dict[str, Material] = {}


async def fetch_materials(data: Children, default: str = "其他材料"):
    for content in data.list:
        quality: Quality = Quality.Three
        if result := re.search(r"(\d+)星", content.ext):
            quality: Quality = star_map[int(result[1])]
        try:
            m_type = re.findall(r'用途/(.*?)\\', content.ext)[0]
        except IndexError:
            m_type = default
        if m_type == "角色晋阶":
            m_type = "角色晋阶材料"
        m_type = MaterialType(m_type)
        material = Material(
            id=content.content_id,
            name=content.title,
            desc=content.summary,
            icon=content.icon,
            quality=quality,
            type=m_type,
        )
        all_materials.append(material)
        all_materials_map[material.id] = material
        all_materials_name[material.name] = material


async def fetch_info(material: Material):
    print(f"Fetch material info: {material.id}: {material.name}")
    params = {
        'app_sn': 'sr_wiki',
        'content_id': str(material.id),
    }
    resp = await client.get(info_url, params=params)
    data = resp.json()["data"]["content"]["contents"][0]["text"]
    soup = BeautifulSoup(data, "lxml")
    table = soup.find("table", {"class": "material-table--pc"})
    if result := re.search(r"(\d+)星", table.text):
        material.quality = star_map[int(result[1])]
    ps = table.find_all("p", {"style": "white-space: pre-wrap;"})
    text = ""
    for p in ps:
        text += f"{p.get_text()}\n"
    material.desc = text.strip()


async def fetch_materials_infos():
    tasks = []
    for material in all_materials:
        tasks.append(fetch_info(material))
    await asyncio.gather(*tasks)


async def dump_materials(path: Path):
    data = [material.dict() for material in all_materials]
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_materials(path: Path):
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    for material in data:
        m = Material(**material)
        all_materials.append(m)
        all_materials_map[m.id] = m
        all_materials_name[m.name] = m

import asyncio
import re
from pathlib import Path
from typing import List

import aiofiles
import ujson
from bs4 import BeautifulSoup

from func.client import client
from func.url import info_url
from models.enums import MonsterType, Area
from models.monster import Monster
from models.wiki import Children

all_monsters: List[Monster] = []


async def fetch_monsters(data: Children):
    for content in data.list:
        m_type = MonsterType(re.findall(r'类型/(.*?)\\', content.ext)[0])
        try:
            m_area = Area(re.findall(r'区域/(.*?)\\', content.ext)[0])
        except IndexError:
            m_area = Area.NULL
        monster = Monster(
            id=content.content_id,
            name=content.title,
            desc=content.summary,
            icon=content.icon,
            big_pic="",
            type=m_type,
            area=m_area,
            resistance="",
            find_area="",
        )
        all_monsters.append(monster)


async def fetch_info(monster: Monster):
    print(f"Fetch monster info: {monster.id}: {monster.name}")
    params = {
        'app_sn': 'sr_wiki',
        'content_id': str(monster.id),
    }
    resp = await client.get(info_url, params=params)
    data = resp.json()["data"]["content"]["contents"][0]["text"]
    soup = BeautifulSoup(data, "lxml")
    table = soup.find("table", {"class": "obc-tml-light-table--pc"})
    trs = table.find_all("tr")
    monster.big_pic = trs[0].find("img").get("src")
    monster.resistance = trs[2].find("p").get_text().strip()
    monster.desc = trs[4].find_all("td")[-1].get_text().strip()
    monster.find_area = trs[5].find_all("td")[-1].get_text().strip()


async def fetch_monsters_infos():
    tasks = []
    for monster in all_monsters:
        tasks.append(fetch_info(monster))
    await asyncio.gather(*tasks)


async def dump_monsters(path: Path):
    data = [monster.dict() for monster in all_monsters]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_monsters(path: Path):
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    for monster in data:
        m = Monster(**monster)
        all_monsters.append(m)

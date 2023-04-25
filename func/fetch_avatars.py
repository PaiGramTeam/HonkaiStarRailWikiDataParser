import asyncio
import re
from pathlib import Path
from typing import List, Dict

import aiofiles
import ujson
from bs4 import BeautifulSoup

from func.client import client
from func.url import info_url
from func.fetch_materials import all_materials_map, all_materials_name
from models.enums import Quality, Element, Destiny
from models.avatar import Avatar, AvatarInfo, AvatarSoul, AvatarItem, AvatarPromote
from models.wiki import Children

all_avatars: List[Avatar] = []
all_avatars_map: Dict[int, Avatar] = {}
all_avatars_name: Dict[str, Avatar] = {}


async def fetch_avatars(data: Children):
    for content in data.list:
        m_element = Element(re.findall(r'属性/(.*?)\\', content.ext)[0])
        m_destiny = Destiny(re.findall(r'命途/(.*?)\\', content.ext)[0])
        m_quality = Quality(re.findall(r'星级/(.*?)\\', content.ext)[0])
        avatar = Avatar(
            id=content.content_id,
            name=content.title,
            icon=content.icon,
            quality=m_quality,
            element=m_element,
            destiny=m_destiny,
            information=AvatarInfo(),
            promote=[],
            soul=[],
        )
        all_avatars.append(avatar)
        all_avatars_map[avatar.id] = avatar
        all_avatars_name[avatar.name] = avatar


def parse_promote(avatar: Avatar, soup: BeautifulSoup) -> None:
    """解析角色突破数据"""
    lis = soup.find_all("li", {"class": "obc-tmpl__switch-item"})
    required_levels = [0, 20, 30, 40, 50, 60, 70, 80]
    max_level = [0, 30, 40, 50, 60, 70, 80, 90]
    for i in range(1, 8):
        promote = AvatarPromote(
            required_level=required_levels[i],
            max_level=max_level[i],
            items=[],
        )
        materials = lis[i].find_all("li", {"data-target": "breach.attr.material"})
        for material in materials:
            try:
                mid = int(re.findall(r"content/(\d+)/detail", material.find("a").get("href"))[0])
            except AttributeError:
                continue
            name = material.find("span", {"class": "obc-tmpl__icon-text"}).text
            item = all_materials_map.get(mid)
            if not item:
                item = all_materials_name.get(name)
            try:
                count = int(material.find("span", {"class": "obc-tmpl__icon-num"}).text.replace("*", ""))
            except AttributeError:
                count = 1
            if name == "信用点":
                promote.coin = count
            elif item:
                promote.items.append(
                    AvatarItem(
                        item=item,
                        count=count,
                    )
                )
            else:
                print(f"unknown material: {mid}: {name}")
        avatar.promote.append(promote)


async def fetch_info(avatar: Avatar):
    print(f"Fetch avatar info: {avatar.id}: {avatar.name}")
    params = {
        'app_sn': 'sr_wiki',
        'content_id': str(avatar.id),
    }
    resp = await client.get(info_url, params=params)
    data = resp.json()["data"]["content"]["contents"][0]["text"]
    soup = BeautifulSoup(data, "lxml")
    items = soup.find_all("div", {"class": "obc-tmp-character__item"})
    avatar.information.faction = items[2].find("div", {"class": "obc-tmp-character__value"}).text
    avatar.information.occupation = items[3].find("div", {"class": "obc-tmp-character__value"}).text
    parse_promote(avatar, soup)
    # 星魂
    table = soup.find_all("table")[-1]
    trs = table.find_all("tr")[1:]
    for tr in trs:
        ps = tr.find_all("p")
        desc = ps[2].text.strip() if len(ps) > 2 else ps[1].text.strip()
        avatar.soul.append(
            AvatarSoul(
                name=ps[0].text.strip(),
                desc=desc,
            )
        )


async def fetch_avatars_infos():
    tasks = []
    for avatar in all_avatars:
        tasks.append(fetch_info(avatar))
    await asyncio.gather(*tasks)


async def dump_avatars(path: Path):
    data = [avatar.dict() for avatar in all_avatars]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_avatars(path: Path):
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    for avatar in data:
        m = Avatar(**avatar)
        all_avatars.append(m)
        all_avatars_map[m.id] = m
        all_avatars_name[m.name] = m

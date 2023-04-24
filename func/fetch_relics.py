import asyncio
from pathlib import Path
from typing import List

import aiofiles
import ujson
from bs4 import BeautifulSoup

from func.client import client
from func.url import info_url
from models.relic import Relic
from models.wiki import Children

all_relics: List[Relic] = []


async def fetch_relics(data: Children):
    for content in data.list:
        relic = Relic(
            id=content.content_id,
            name=content.title,
            icon=content.icon,
            affect="",
        )
        all_relics.append(relic)


async def fetch_info(relic: Relic):
    print(f"Fetch relic info: {relic.id}: {relic.name}")
    params = {
        'app_sn': 'sr_wiki',
        'content_id': str(relic.id),
    }
    resp = await client.get(info_url, params=params)
    data = resp.json()["data"]["content"]["contents"][0]["text"]
    soup = BeautifulSoup(data, "lxml")
    relic.affect = soup.find("div", {"class": "obc-tmpl-relic__story"}).get_text().strip()


async def fetch_relics_infos():
    tasks = []
    for relic in all_relics:
        tasks.append(fetch_info(relic))
    await asyncio.gather(*tasks)


async def dump_relics(path: Path):
    data = [relic.dict() for relic in all_relics]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_relics(path: Path):
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    for monster in data:
        m = Relic(**monster)
        all_relics.append(m)

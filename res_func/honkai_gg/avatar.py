import asyncio
import aiofiles
import re
from typing import List

import ujson
from bs4 import BeautifulSoup
from res_func.client import client
from res_func.url import avatar_honkai_url, avatar_icon_honkai_url

avatar_data = {}


async def get_all_avatar() -> List[str]:
    req = await client.get(avatar_honkai_url)
    html = req.text
    pattern = re.compile(r'href="/characters/(.*?)">')
    result = pattern.findall(html)
    return [f"{avatar_honkai_url}/{i}" for i in result if i != ""]


async def get_single_avatar(url: str) -> None:
    req = await client.get(url)
    html = req.text
    soup = BeautifulSoup(html, "lxml")
    div = soup.find_all("div", {"class": "character_skills__FL3Dn"})[-1]
    pattern = re.compile(r'skillicons/(.*?)/skillicon(.*?).webp')
    result = pattern.findall(str(div))
    if len(result) != 6:
        print(f"{url} 获取星魂图片失败")
        return
    urls = [f"{avatar_icon_honkai_url}/{i[0]}/skillicon{i[1]}.webp" for i in result]
    avatar_data[result[0][0]] = urls


async def dump_icons():
    final_data = dict(sorted(avatar_data.items(), key=lambda x: x[0]))
    async with aiofiles.open("data/avatar_eidolon_icons.json", "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(final_data, indent=4, ensure_ascii=False))


async def get_all_avatars() -> None:
    print("开始获取星魂图片")
    urls = await get_all_avatar()
    tasks = []
    for url in urls:
        tasks.append(get_single_avatar(url))
    await asyncio.gather(*tasks)
    # 修复开拓者
    avatar_data["8002"] = avatar_data["8001"]
    avatar_data["8004"] = avatar_data["8003"]
    await dump_icons()
    print("获取星魂图片成功")

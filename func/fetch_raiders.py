import asyncio

import aiofiles
from pathlib import Path

import ujson

from func.fetch_all import get_list
from modules.apihelper.client.components.hyperion import Hyperion

data_path = Path("data/raiders")
data_path.mkdir(exist_ok=True, parents=True)
hyperion = Hyperion()


async def fetch_and_save_photo(name: str, url: str):
    print(f"Fetch raider photo: {name} {url}")
    pid = int(url.split("/")[-1])
    img_list = await hyperion.get_images_by_post_id(6, pid)
    if not img_list:
        return
    if len(img_list) < 3:
        return
    img = img_list[2]
    async with aiofiles.open(data_path / f"{name}.png", "wb") as f:
        await f.write(img.data)


async def get_raiders():
    lists = await get_list("63")
    maps = {}
    for children in lists:
        char_name = children.name
        final_content = None
        for content in children.list:
            if content.article_user_name == "初始镜像OriginMirror":
                final_content = content
                break
        if not final_content:
            continue
        if not final_content.bbs_url:
            continue
        maps[char_name] = final_content.bbs_url
    tasks = []
    for key, value in maps.items():
        tasks.append(fetch_and_save_photo(key, value))
    await asyncio.gather(*tasks)
    async with aiofiles.open(data_path / "info.json", "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(list(maps.keys()), ensure_ascii=False, indent=4))

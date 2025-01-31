import asyncio
import json
from pathlib import Path
from typing import List

import aiofiles
import ujson

from func.client import retry
from func.data import all_avatars
from models.avatar import YattaAvatar
from res_func.avatar import TRAVER_DATA_MAP
from res_func.client import client
from res_func.url import avatar_skill_url

avatar_data = {}
avatars_skills_icons = {}
avatars_skills_path = Path("data/skill")
avatars_skills_path.mkdir(exist_ok=True, parents=True)


@retry
async def get_single_avatar_skill_icon(url: str, real_path: str) -> None:
    req = await client.get(url)
    try:
        req.raise_for_status()
    except Exception as e:
        print(f"{url} 获取技能图片失败")
        raise e
    async with aiofiles.open(f"data/skill/{real_path}", "wb") as f:
        await f.write(req.content)
    for k, v in TRAVER_DATA_MAP.values():
        if str(k) in real_path:
            real_path = real_path.replace(str(k), str(v))
            async with aiofiles.open(f"data/skill/{real_path}", "wb") as f:
                await f.write(req.content)


async def dump_icons():
    final_data = dict(sorted(avatar_data.items(), key=lambda x: x[0]))
    async with aiofiles.open(
        "data/avatar_eidolon_icons.json", "w", encoding="utf-8"
    ) as f:
        await f.write(ujson.dumps(final_data, indent=4, ensure_ascii=False))


async def get_all_avatars() -> None:
    print("开始获取星魂图片")
    for avatar in all_avatars:
        urls = [i.icon_url for i in avatar.eidolons]
        avatar_data[str(avatar.id)] = urls
    await dump_icons()
    print("获取星魂图片成功")
    print("开始获取技能图片")
    await get_all_avatars_skills_icons(all_avatars)
    print("获取技能图片成功")


async def get_all_avatars_skills_icons(avatars: List[YattaAvatar]):
    traver_ids = [i[1] for i in TRAVER_DATA_MAP.values()]
    remote_path = ["Normal", "BP", "Passive", "Maze", "Ultra"]
    local_path = ["basic_atk", "skill", "talent", "technique", "ultimate"]
    tasks = []
    for avatar in avatars:
        if avatar.id in traver_ids + [1311]:
            continue
        for i in range(len(remote_path)):
            tasks.append(
                get_single_avatar_skill_icon(
                    f"{avatar_skill_url}SkillIcon_{avatar.id}_{remote_path[i]}.png",
                    f"{avatar.id}_{local_path[i]}.png",
                )
            )
        await asyncio.gather(*tasks)
        tasks.clear()
    datas = [file.name.split(".")[0] for file in avatars_skills_path.glob("*")]
    async with aiofiles.open(
        avatars_skills_path / "info.json", "w", encoding="utf-8"
    ) as f:
        await f.write(json.dumps(datas, indent=4, ensure_ascii=False))

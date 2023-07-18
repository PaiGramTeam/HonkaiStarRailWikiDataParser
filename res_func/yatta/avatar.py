import asyncio
import json
from pathlib import Path
from typing import List

import aiofiles
import ujson

from res_func.client import client
from res_func.url import avatar_yatta_url, avatar_skill_url
from res_func.yatta.model import YattaAvatar

avatar_data = {}
avatars_skills_icons = {}
avatars_skills_path = Path("data/skill")
avatars_skills_path.mkdir(exist_ok=True, parents=True)


async def get_all_avatar() -> List[str]:
    req = await client.get(avatar_yatta_url)
    return list(req.json()["data"]["items"].keys())


async def get_single_avatar(url: str) -> None:
    req = await client.get(url)
    try:
        avatar = YattaAvatar(**req.json()["data"])
    except Exception:
        print(f"{url} 获取星魂数据失败")
        return
    if len(avatar.eidolons) != 6:
        print(f"{url} 获取星魂图片失败")
        return
    urls = [i.icon_url for i in avatar.eidolons]
    avatar_data[str(avatar.id)] = urls


def retry(func):
    async def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                await func(*args, **kwargs)
                break
            except Exception:
                print(f"重试 {func.__name__} {i + 1} 次")
                await asyncio.sleep(1)

    return wrapper


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
    if "8001" in real_path:
        real_path = real_path.replace("8001", "8002")
        async with aiofiles.open(f"data/skill/{real_path}", "wb") as f:
            await f.write(req.content)
    elif "8003" in real_path:
        real_path = real_path.replace("8003", "8004")
        async with aiofiles.open(f"data/skill/{real_path}", "wb") as f:
            await f.write(req.content)


async def dump_icons():
    final_data = dict(sorted(avatar_data.items(), key=lambda x: x[0]))
    async with aiofiles.open("data/avatar_eidolon_icons.json", "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(final_data, indent=4, ensure_ascii=False))


async def get_all_avatars() -> None:
    print("开始获取星魂图片")
    avatar_ids = await get_all_avatar()
    for avatar_id in avatar_ids:
        await get_single_avatar(f"{avatar_yatta_url}/{avatar_id}")
    await dump_icons()
    print("获取星魂图片成功")
    await get_all_avatars_skills_icons(avatar_ids)


async def get_all_avatars_skills_icons(avatar_ids: List[str]):
    remote_path = ["Normal", "BP", "Passive", "Maze", "Ultra"]
    local_path = ["basic_atk", "skill", "talent", "technique", "ultimate"]
    print("开始获取技能图片")
    tasks = []
    for avatar_id in avatar_ids:
        if avatar_id in ["8002", "8004"]:
            continue
        for i in range(len(remote_path)):
            tasks.append(
                get_single_avatar_skill_icon(
                    f"{avatar_skill_url}SkillIcon_{avatar_id}_{remote_path[i]}.png",
                    f"{avatar_id}_{local_path[i]}.png"
                )
            )
        await asyncio.gather(*tasks)
        tasks.clear()
    datas = [file.name.split(".")[0] for file in avatars_skills_path.glob("*")]
    async with aiofiles.open(avatars_skills_path / "info.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(datas, indent=4, ensure_ascii=False))
    print("获取技能图片成功")

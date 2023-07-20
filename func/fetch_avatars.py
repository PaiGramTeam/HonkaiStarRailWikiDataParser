import asyncio
from pathlib import Path
from typing import List, Dict

import aiofiles
import ujson
from httpx import TimeoutException
from pydantic import ValidationError

from func.client import client
from models.avatar import YattaAvatar
from models.wiki import Content, Children
from res_func.url import avatar_yatta_url

all_avatars: List[YattaAvatar] = []
all_avatars_map: Dict[int, YattaAvatar] = {}
all_avatars_name: Dict[str, YattaAvatar] = {}


def retry(func):
    async def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return await func(*args, **kwargs)
            except TimeoutException:
                print(f"重试 {func.__name__} {i + 1} 次")
                await asyncio.sleep(1)

    return wrapper


def fix_avatar_eidolons(values: Dict) -> Dict:
    if values.get("eidolons") is None:
        values["eidolons"] = []
    else:
        eidolons = []
        for eidolon in values["eidolons"].values():
            eidolons.append(eidolon)
        values["eidolons"] = eidolons
    return values


@retry
async def get_single_avatar(url: str) -> None:
    req = await client.get(url)
    try:
        avatar = YattaAvatar(**fix_avatar_eidolons(req.json()["data"]))
    except Exception as e:
        print(f"{url} 获取角色数据失败")
        raise e
    all_avatars.append(avatar)
    all_avatars_map[avatar.id] = avatar
    all_avatars_name[avatar.name] = avatar


@retry
async def get_all_avatar() -> List[str]:
    req = await client.get(avatar_yatta_url)
    return list(req.json()["data"]["items"].keys())


async def fix_avatar_icon(content: Content):
    avatar = all_avatars_name.get(content.title)
    if not avatar:
        return
    avatar.icon = content.icon


async def fetch_avatars(child: Children):
    print("获取角色数据")
    avatars = await get_all_avatar()
    for avatar_id in avatars:
        try:
            await get_single_avatar(f"{avatar_yatta_url}/{avatar_id}")
        except ValidationError:
            print(f"{avatar_yatta_url}/{avatar_id} 获取角色数据失败，角色格式异常")
    print("修复角色图标")
    for content in child.list:
        await fix_avatar_icon(content)
    for avatar in all_avatars:
        if not avatar.icon.startswith("http"):
            avatar.icon = ""
    print("获取角色数据完成")


async def dump_avatars(path: Path):
    data = [avatar.dict() for avatar in all_avatars]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_avatars(path: Path):
    all_avatars.clear()
    all_avatars_map.clear()
    all_avatars_name.clear()
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    for avatar in data:
        m = YattaAvatar(**avatar)
        all_avatars.append(m)
        all_avatars_map[m.id] = m
        all_avatars_name[m.name] = m

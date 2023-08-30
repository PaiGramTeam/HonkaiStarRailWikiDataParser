from typing import List, Dict

from pydantic import ValidationError

from func.client import client, retry
from func.data import all_avatars, all_avatars_map, all_avatars_name, dump_avatars
from models.avatar import YattaAvatar
from models.wiki import Content, Children
from res_func.url import avatar_yatta_url


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
    avatar = all_avatars_name.get(content.title.replace("·", "•"))
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
    await dump_avatars()

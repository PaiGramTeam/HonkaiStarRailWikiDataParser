from typing import List

from pydantic import ValidationError

from func.client import client, retry
from func.data import all_light_cones, all_light_cones_name, dump_light_cones
from models.light_cone import YattaLightCone
from res_func.url import light_cone_yatta_url


@retry
async def get_single_light_cone(url: str) -> None:
    req = await client.get(url)
    try:
        light_cone = YattaLightCone(**(req.json()["data"]))
    except Exception as e:
        print(f"{url} 获取光锥数据失败")
        raise e
    all_light_cones.append(light_cone)
    all_light_cones_name[light_cone.name] = light_cone


@retry
async def get_all_light_cones() -> List[str]:
    req = await client.get(light_cone_yatta_url)
    return list(req.json()["data"]["items"].keys())


async def fetch_light_cones():
    print("获取光锥数据")
    light_cones = await get_all_light_cones()
    for light_cone_id in light_cones:
        try:
            await get_single_light_cone(f"{light_cone_yatta_url}/{light_cone_id}")
        except ValidationError:
            print(f"{light_cone_yatta_url}/{light_cone_id} 获取光锥数据失败，数据格式异常")
    print("获取光锥数据完成")
    await dump_light_cones()

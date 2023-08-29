from typing import List, Dict

from pydantic import ValidationError

from func.client import client, retry
from func.data import all_relics, dump_relics
from models.relic import YattaRelic
from res_func.url import relic_yatta_url


@retry
async def get_all_relics() -> List[Dict]:
    req = await client.get(relic_yatta_url)
    return list(req.json()["data"]["items"].values())


async def fetch_relics():
    print("获取遗器数据")
    relics = await get_all_relics()
    for relic in relics:
        try:
            relic_ = YattaRelic(**relic)
            all_relics.append(relic_)
        except ValidationError as e:
            raise e
            print(f"{relic} 解析遗器数据失败，数据格式异常")
    print("获取遗器数据完成")
    await dump_relics()

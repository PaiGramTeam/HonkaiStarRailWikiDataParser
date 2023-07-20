from pathlib import Path
from typing import Dict, Tuple, List

from bs4 import BeautifulSoup

from func.fetch_relics import all_relics, read_relics, dump_relics
from res_func.client import client
from res_func.url import relic_url, base_station_url

relics_path = Path("data") / "relics.json"


async def fix_set_image():
    print("开始修复遗器套装图片")
    await read_relics(relics_path)
    req = await client.get(relic_url)
    soup = BeautifulSoup(req.text, "lxml")
    divs = soup.find_all("a", {"class": "aff5a"})
    data_map: Dict[int, Tuple[str, List[str]]] = {}
    for div in divs:
        url = div.get("href")
        if not url:
            continue
        if "relics/" not in url:
            continue
        sid = int(url.split("/")[-1])
        images = div.find_all("img")
        images = [f"{base_station_url}{i.get('src')}" for i in images]
        if len(images) not in {3, 5}:
            print(f"套装 {sid} 图片数量异常")
            continue
        data_map[sid] = (images[0], images[1:])
    for relic in all_relics:
        if relic.id in data_map:
            relic.icon = data_map[relic.id][0]
            relic.image_list = data_map[relic.id][1]
        else:
            print(f"套装 {relic.id} 没有找到对应的图片")
    await dump_relics(relics_path)
    print("遗器套装图片修复完毕")

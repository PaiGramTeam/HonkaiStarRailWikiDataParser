import asyncio
from pathlib import Path

import aiofiles

from func.client import client, retry
from func.url import mihomo_map_url

data_dir = Path("data") / "mihomo_map"
data_dir.mkdir(exist_ok=True, parents=True)
file_set = {
    "characters.json",
    "character_ranks.json",
    "character_skills.json",
    "character_skill_trees.json",
    "character_promotions.json",
    "light_cones.json",
    "light_cone_ranks.json",
    "light_cone_promotions.json",
    "relics.json",
    "relic_sets.json",
    "relic_main_affixes.json",
    "relic_sub_affixes.json",
    "paths.json",
    "elements.json",
    "properties.json",
    "avatars.json",
}


@retry
async def fetch_file(filename: str) -> None:
    req = await client.get(mihomo_map_url + filename)
    async with aiofiles.open(data_dir / filename, "wb") as f:
        await f.write(req.content)


async def fetch_files():
    print("获取 mihomo map 文件")
    tasks = [fetch_file(file) for file in file_set]
    await asyncio.gather(*tasks)

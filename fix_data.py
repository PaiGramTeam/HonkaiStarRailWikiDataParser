import asyncio

from res_func.avatar import fix_avatar_config, fetch_text_map
from res_func.light_cone import fix_light_cone_config
from res_func.relic import fetch_relic_config
from res_func.relic_res import fix_set_image
from res_func.yatta.avatar import get_all_avatars


async def main():
    text_map_data = await fetch_text_map()
    await fix_avatar_config(text_map_data)
    await fix_light_cone_config()
    await fetch_relic_config()
    await fix_set_image()
    await get_all_avatars()


if __name__ == "__main__":
    asyncio.run(main())

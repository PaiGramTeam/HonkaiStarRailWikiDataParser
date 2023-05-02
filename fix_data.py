import asyncio

from res_func.avatar import fix_avatar_config, fetch_text_map
from res_func.light_cone import fix_light_cone_config


async def main():
    text_map_data = await fetch_text_map()
    await fix_avatar_config(text_map_data)
    await fix_light_cone_config()


if __name__ == '__main__':
    asyncio.run(main())

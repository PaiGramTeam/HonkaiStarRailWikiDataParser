import asyncio

from func.fetch_all import get_list
from func.fetch_avatars import fetch_avatars
from func.fetch_light_cones import fetch_light_cones
from func.fetch_materials import fetch_materials
from func.fetch_relics import fetch_relics
from func.fetch_src import move_files
from func.fetch_mihomo_map import fetch_files


async def wiki():
    main_data = await get_list()
    await fetch_avatars(main_data[0])
    await fetch_light_cones()
    await fetch_materials()
    await fetch_relics()


async def bbs_photos():
    await move_files()


async def main():
    await wiki()
    await bbs_photos()
    await fetch_files()


if __name__ == "__main__":
    asyncio.run(main())

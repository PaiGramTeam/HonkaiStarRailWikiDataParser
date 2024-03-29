import asyncio

from res_func.avatar import fix_avatar_config
from res_func.light_cone import fix_light_cone_config
from res_func.relic import fetch_relic_config
from res_func.relic_res import fix_set_image
from res_func.yatta.avatar import get_all_avatars
from res_func.head_icon import get_head_icons
from res_func.phone_theme import get_phone_themes


async def main():
    await fix_avatar_config()
    await fix_light_cone_config()
    await fetch_relic_config()
    await fix_set_image()
    await get_all_avatars()
    await get_head_icons()
    await get_phone_themes()


if __name__ == "__main__":
    asyncio.run(main())

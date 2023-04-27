import asyncio

from res_func.avatar import fix_avatar_config
from res_func.light_cone import fix_light_cone_config


async def main():
    await fix_avatar_config()
    await fix_light_cone_config()


if __name__ == '__main__':
    asyncio.run(main())

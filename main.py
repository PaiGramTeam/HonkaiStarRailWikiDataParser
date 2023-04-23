import asyncio
from pathlib import Path
from func.fetch_all import get_list
from func.fetch_avatars import fetch_avatars, fetch_avatars_infos, dump_avatars, read_avatars
from func.fetch_materials import fetch_materials, fetch_materials_infos, dump_materials, read_materials

data_path = Path("data")
data_path.mkdir(exist_ok=True)


async def main(override: bool = True):
    main_data = await get_list()
    if override:
        await fetch_materials(main_data[4])
        await fetch_materials(main_data[5], "消耗品")
        await fetch_materials(main_data[8], "任务道具")
        await fetch_materials(main_data[9], "贵重物")
        await fetch_materials(main_data[10])
        await fetch_materials_infos()
        await dump_materials(data_path / "materials.json")
    else:
        await read_materials(data_path / "materials.json")
    await fetch_avatars(main_data[0])
    await fetch_avatars_infos()
    await dump_avatars(data_path / "avatars.json")


if __name__ == '__main__':
    asyncio.run(main())

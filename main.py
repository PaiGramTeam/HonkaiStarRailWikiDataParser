import asyncio
from pathlib import Path
from func.fetch_all import get_list
from func.fetch_avatars import fetch_avatars, fetch_avatars_infos, dump_avatars, read_avatars
from func.fetch_light_cones import fetch_light_cones, fetch_light_cones_infos, dump_light_cones, read_light_cones
from func.fetch_materials import fetch_materials, fetch_materials_infos, dump_materials, read_materials

data_path = Path("data")
data_path.mkdir(exist_ok=True)


async def main(
    override_materials: bool = True,
    override_avatars: bool = True,
    override_light_cones: bool = True,
):
    main_data = await get_list()
    if override_materials:
        await fetch_materials(main_data[4])
        await fetch_materials(main_data[5], "消耗品")
        await fetch_materials(main_data[8], "任务道具")
        await fetch_materials(main_data[9], "贵重物")
        await fetch_materials(main_data[10])
        await fetch_materials_infos()
        await dump_materials(data_path / "materials.json")
    else:
        await read_materials(data_path / "materials.json")
    if override_avatars:
        await fetch_avatars(main_data[0])
        await fetch_avatars_infos()
        await dump_avatars(data_path / "avatars.json")
    else:
        await read_avatars(data_path / "avatars.json")
    if override_light_cones:
        await fetch_light_cones(main_data[1])
        await fetch_light_cones_infos()
        await dump_light_cones(data_path / "light_cones.json")
    else:
        await read_light_cones(data_path / "light_cones.json")


if __name__ == '__main__':
    override_materials = True
    override_avatars = True
    override_light_cones = True
    asyncio.run(main(override_materials, override_avatars, override_light_cones))

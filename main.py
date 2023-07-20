import asyncio
from pathlib import Path
from func.fetch_all import get_list
from func.fetch_avatars import fetch_avatars, dump_avatars, read_avatars
from func.fetch_light_cones import fetch_light_cones, fetch_light_cones_infos, dump_light_cones, read_light_cones
from func.fetch_materials import fetch_materials, fetch_materials_infos, dump_materials, read_materials
from func.fetch_monsters import fetch_monsters, fetch_monsters_infos, dump_monsters, read_monsters
from func.fetch_relics import fetch_relics, fetch_relics_infos, dump_relics, read_relics
from func.fetch_src import move_files

data_path = Path("data")
data_path.mkdir(exist_ok=True)


async def wiki(
    override_materials: bool = True,
    override_avatars: bool = True,
    override_light_cones: bool = True,
    override_monsters: bool = True,
    override_relics: bool = True,
):
    main_data = await get_list()
    if override_materials:
        await fetch_materials(main_data[4])
        await fetch_materials(main_data[5], "消耗品")
        await fetch_materials(main_data[9], "任务道具")
        await fetch_materials(main_data[10], "贵重物")
        await fetch_materials(main_data[12])
        await fetch_materials_infos()
        await dump_materials(data_path / "materials.json")
    else:
        await read_materials(data_path / "materials.json")
    if override_avatars:
        await fetch_avatars(main_data[0])
        await dump_avatars(data_path / "avatars.json")
    else:
        await read_avatars(data_path / "avatars.json")
    if override_light_cones:
        await fetch_light_cones(main_data[1])
        await fetch_light_cones_infos()
        await dump_light_cones(data_path / "light_cones.json")
    else:
        await read_light_cones(data_path / "light_cones.json")
    if override_monsters:
        await fetch_monsters(main_data[2])
        await fetch_monsters_infos()
        await dump_monsters(data_path / "monsters.json")
    else:
        await read_monsters(data_path / "monsters.json")
    if override_relics:
        await fetch_relics(main_data[3])
        await fetch_relics_infos()
        await dump_relics(data_path / "relics.json")
    else:
        await read_relics(data_path / "relics.json")


async def bbs_photos():
    await move_files()


async def main(
    override_materials: bool = True,
    override_avatars: bool = True,
    override_light_cones: bool = True,
    override_monsters: bool = True,
    override_relics: bool = True,
    override_bbs_photos: bool = True,
):
    await wiki(override_materials, override_avatars, override_light_cones, override_monsters, override_relics)
    if override_bbs_photos:
        await bbs_photos()


if __name__ == '__main__':
    override_material_ = True
    override_avatar_ = True
    override_light_cone_ = True
    override_monster_ = True
    override_relic_ = True
    override_bbs_photo_ = True
    asyncio.run(main(
        override_material_,
        override_avatar_,
        override_light_cone_,
        override_monster_,
        override_relic_,
        override_bbs_photo_,
    ))

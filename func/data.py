from pathlib import Path
from typing import List, Dict

import aiofiles
import ujson

from models.avatar import YattaAvatar
from models.light_cone import YattaLightCone
from models.material import YattaMaterial
from models.relic import YattaRelic

data_path = Path("data")
data_path.mkdir(exist_ok=True)

avatars_path = data_path / "avatars.json"
all_avatars: List[YattaAvatar] = []
all_avatars_map: Dict[int, YattaAvatar] = {}
all_avatars_name: Dict[str, YattaAvatar] = {}

light_cones_path = data_path / "light_cones.json"
all_light_cones: List[YattaLightCone] = []
all_light_cones_map: Dict[int, YattaLightCone] = {}
all_light_cones_name: Dict[str, YattaLightCone] = {}

materials_path = data_path / "materials.json"
all_materials: List[YattaMaterial] = []
all_materials_map: Dict[int, YattaMaterial] = {}
all_materials_name: Dict[str, YattaMaterial] = {}

relics_path = data_path / "relics.json"
all_relics: List[YattaRelic] = []


async def dump_avatars():
    data = [avatar.dict() for avatar in all_avatars]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(avatars_path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_avatars():
    all_avatars.clear()
    all_avatars_map.clear()
    all_avatars_name.clear()
    async with aiofiles.open(avatars_path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    for avatar in data:
        m = YattaAvatar(**avatar)
        all_avatars.append(m)
        all_avatars_map[m.id] = m
        all_avatars_name[m.name] = m


async def dump_light_cones():
    data = [light_cone.dict() for light_cone in all_light_cones]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(light_cones_path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_light_cones():
    async with aiofiles.open(light_cones_path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    all_light_cones.clear()
    all_light_cones_map.clear()
    all_light_cones_name.clear()
    for light_cone in data:
        m = YattaLightCone(**light_cone)
        all_light_cones.append(m)
        all_light_cones_map[m.id] = m
        all_light_cones_name[m.name] = m


async def dump_materials():
    data = [material.dict() for material in all_materials]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(materials_path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_materials():
    async with aiofiles.open(materials_path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    for material in data:
        m = YattaMaterial(**material)
        all_materials.append(m)
        all_materials_map[m.id] = m
        all_materials_name[m.name] = m


async def dump_relics():
    data = [relic.dict() for relic in all_relics]
    data.sort(key=lambda x: x["id"])
    async with aiofiles.open(relics_path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(data, indent=4, ensure_ascii=False))


async def read_relics():
    all_relics.clear()
    async with aiofiles.open(relics_path, "r", encoding="utf-8") as f:
        data = ujson.loads(await f.read())
    for relic in data:
        m = YattaRelic(**relic)
        all_relics.append(m)

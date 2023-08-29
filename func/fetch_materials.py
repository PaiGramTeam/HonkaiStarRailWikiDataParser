from typing import List, Dict

from pydantic import ValidationError

from func.client import client, retry
from func.data import (
    all_materials,
    all_materials_map,
    all_materials_name,
    dump_materials,
)
from models.material import YattaMaterial
from res_func.url import material_yatta_url


def fix_material(values: Dict) -> Dict:
    if values.get("source") is None:
        values["source"] = []
    return values


@retry
async def get_single_material(url: str) -> None:
    req = await client.get(url)
    try:
        material = YattaMaterial(**fix_material(req.json()["data"]))
    except Exception as e:
        print(f"{url} 获取材料数据失败")
        raise e
    all_materials.append(material)
    all_materials_map[material.id] = material
    all_materials_name[material.name] = material


@retry
async def get_all_materials() -> List[str]:
    req = await client.get(material_yatta_url)
    return list(req.json()["data"]["items"].keys())


async def fetch_materials():
    print("获取材料数据")
    materials = await get_all_materials()
    for material_id in materials:
        try:
            await get_single_material(f"{material_yatta_url}/{material_id}")
        except ValidationError:
            print(f"{material_yatta_url}/{material_id} 获取材料数据失败，数据格式异常")
    print("获取材料数据完成")
    await dump_materials()

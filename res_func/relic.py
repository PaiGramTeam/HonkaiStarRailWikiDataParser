from pathlib import Path
from typing import List, Dict

import aiofiles
import ujson

from models.enums import RelicAffix, RelicPosition
from models.relic_affix import RelicAffixAll, SingleRelicAffix
from res_func.base_data import get_base_data
from res_func.url import relic_config, relic_main_affix_config, relic_sub_affix_config

final_datas: List[RelicAffixAll] = []
final_datas_map: Dict[str, RelicAffixAll] = {}


async def fetch_all_relic():
    print("开始获取遗器配置")
    relic_data = await get_base_data(relic_config)
    for value in relic_data:
        key = value["ID"]
        relic_affix_all = RelicAffixAll(
            id=int(key),
            set_id=value["SetID"],
            type=RelicPosition(value["Type"]),
            rarity=int(value["Rarity"].replace("CombatPowerRelicRarity", "")),
            main_affix_group=value["MainAffixGroup"],
            sub_affix_group=value["SubAffixGroup"],
            max_level=value["MaxLevel"],
            main_affix={},
            sub_affix={},
        )
        final_datas.append(relic_affix_all)
        final_datas_map[key] = relic_affix_all
    print("遗器配置获取完毕")


async def fetch_main_affix():
    print("开始获取遗器主词条配置")
    main_affix_data = await get_base_data(relic_main_affix_config)
    main_affix_groups_map: Dict[str, Dict[str, SingleRelicAffix]] = {}
    for value in main_affix_data:
        key = str(value["GroupID"])
        data: Dict[str, SingleRelicAffix] = main_affix_groups_map.get(key, {})

        value2 = value
        key2 = str(value2["AffixID"])
        data[key2] = SingleRelicAffix(
            id=value2["AffixID"],
            property=RelicAffix(value2["Property"]),
            base_value=value2["BaseValue"]["Value"],
            level_value=value2["LevelAdd"]["Value"],
            is_main=True,
        )

        main_affix_groups_map[key] = data
    for final_data in final_datas:
        final_data.main_affix = main_affix_groups_map[str(final_data.main_affix_group)]
    print("遗器主词条配置获取完毕")


async def fetch_sub_affix():
    print("开始获取遗器副词条配置")
    sub_affix_data = await get_base_data(relic_sub_affix_config)
    sub_affix_groups_map: Dict[str, Dict[str, SingleRelicAffix]] = {}
    for value in sub_affix_data:
        key = str(value["GroupID"])
        data: Dict[str, SingleRelicAffix] = sub_affix_groups_map.get(key, {})

        value2 = value
        key2 = str(value2["AffixID"])
        data[key2] = SingleRelicAffix(
            id=value2["AffixID"],
            property=RelicAffix(value2["Property"]),
            base_value=value2["BaseValue"]["Value"],
            step_value=value2["StepValue"]["Value"],
            is_main=False,
            max_step=value2["StepNum"],
        )

        sub_affix_groups_map[key] = data
    for final_data in final_datas:
        final_data.sub_affix = sub_affix_groups_map[str(final_data.sub_affix_group)]
    print("遗器副词条配置获取完毕")


async def dump_relic_config(path: Path):
    final_data = [data.dict() for data in final_datas]
    final_data.sort(key=lambda x: x["id"])
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(ujson.dumps(final_data, indent=4, ensure_ascii=False))


async def fetch_relic_config():
    await fetch_all_relic()
    await fetch_main_affix()
    await fetch_sub_affix()
    data_path = Path("data") / "mihomo_map"
    data_path.mkdir(exist_ok=True, parents=True)
    await dump_relic_config(data_path / "relic_config.json")

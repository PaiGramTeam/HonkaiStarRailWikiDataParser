import base64

base_data_url = base64.b64decode(
    "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0RpbWJyZWF0aC9TdGFyUmFpbERhdGEvbWFzdGVyLw=="
).decode("utf-8")
avatar_config = f"{base_data_url}ExcelOutput/AvatarConfig.json"
text_map = f"{base_data_url}TextMap/TextMapCHS.json"
relic_config = f"{base_data_url}ExcelOutput/RelicConfig.json"
relic_main_affix_config = f"{base_data_url}ExcelOutput/RelicMainAffixConfig.json"
relic_sub_affix_config = f"{base_data_url}ExcelOutput/RelicSubAffixConfig.json"
base_station_url = "https://starrailstation.com"
avatar_url = f"{base_station_url}/cn/characters"
light_cone_url = f"{base_station_url}/cn/equipment"
relic_url = f"{base_station_url}/cn/relics"
base_yatta_url = "https://api.yatta.top"
avatar_yatta_url = f"{base_yatta_url}/hsr/v2/cn/avatar"
avatar_skill_url = f"{base_yatta_url}/hsr/assets/UI/skill/"
light_cone_yatta_url = f"{base_yatta_url}/hsr/v2/cn/equipment"
material_yatta_url = f"{base_yatta_url}/hsr/v2/cn/item"
relic_yatta_url = f"{base_yatta_url}/hsr/v2/cn/relic"

import base64

base_data_url = base64.b64decode(
    "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0RpbWJyZWF0aC9TdGFyUmFpbERhdGEvbWFzdGVyLw=="
).decode("utf-8")
avatar_config = f"{base_data_url}ExcelOutput/AvatarConfig.json"
text_map = f"{base_data_url}TextMap/TextMapCN.json"
base_station_url = "https://starrailstation.com"
avatar_url = f"{base_station_url}/cn/characters"
light_cone_url = f"{base_station_url}/cn/equipment"

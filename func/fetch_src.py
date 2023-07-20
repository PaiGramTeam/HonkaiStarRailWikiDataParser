import shutil
from pathlib import Path

import aiofiles
import ujson as jsonlib

src_dir = Path("src")
data_dir = Path("data")
pic_lists = ["avatar_gacha", "destiny", "element"]


async def move_files():
    for i in pic_lists:
        print(f"Moving: {i}")
        src_dir_ = src_dir / i
        data_dir_ = data_dir / i
        datas = [file.name.split(".")[0] for file in src_dir_.glob("*")]
        if data_dir_.exists():
            shutil.rmtree(data_dir_)
        shutil.copytree(src_dir_, data_dir_)
        async with aiofiles.open(data_dir_ / "info.json", "w", encoding="utf-8") as f:
            await f.write(jsonlib.dumps(datas, indent=4, ensure_ascii=False))

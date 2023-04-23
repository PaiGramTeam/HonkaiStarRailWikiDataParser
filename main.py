import asyncio
import aiofiles
from pathlib import Path
from func.fetch_all import get_list
from func.fetch_materials import fetch_materials, fetch_materials_infos, dump_materials

data_path = Path("data")
data_path.mkdir(exist_ok=True)


async def main():
    main_data = await get_list()
    await fetch_materials(main_data[4])
    await fetch_materials_infos()
    await dump_materials(data_path / "materials.json")


if __name__ == '__main__':
    asyncio.run(main())

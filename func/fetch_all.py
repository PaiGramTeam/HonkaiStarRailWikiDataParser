from typing import List

from func.client import client
from func.url import list_url

from models.wiki import Children


async def get_list(channel_id: str = '17') -> List[Children]:
    params = {
        'app_sn': 'sr_wiki',
        'channel_id': channel_id,
    }
    resp = await client.get(list_url, params=params)
    children = resp.json()["data"]["list"][0]["children"]
    return [Children(**child) for child in children]

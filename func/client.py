import asyncio

from httpx import AsyncClient, TimeoutException, HTTPStatusError

headers = {
    "authority": "api-static.mihoyo.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,zh-Hans;q=0.8,und;q=0.7,en;q=0.6,zh-Hant;q=0.5,ja;q=0.4",
    "dnt": "1",
    "origin": "https://bbs.mihoyo.com",
    "referer": "https://bbs.mihoyo.com/",
    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}
client = AsyncClient(headers=headers, timeout=120.0)


def retry(func):
    async def wrapper(*args, **kwargs):
        for i in range(5):
            try:
                return await func(*args, **kwargs)
            except HTTPStatusError as exc:
                if exc.response.status_code == 522:
                    print(f"重试 {func.__name__} {i + 1} 次")
                    await asyncio.sleep(1)
                else:
                    raise exc
            except TimeoutException:
                print(f"重试 {func.__name__} {i + 1} 次")
                await asyncio.sleep(1)

    return wrapper

from contextlib import AbstractAsyncContextManager
from types import TracebackType

import httpx

__all__ = ("HTTPXRequest",)
timeout = httpx.Timeout(
    timeout=120.0,
    read=120.0,
    write=120.0,
    connect=120.0,
    pool=120.0,
)


class HTTPXRequest(AbstractAsyncContextManager):
    def __init__(self, *args, headers=None, **kwargs):
        self._client = httpx.AsyncClient(
            headers=headers, timeout=timeout, *args, **kwargs
        )

    async def __aenter__(self):
        try:
            await self.initialize()
            return self
        except Exception:
            await self.shutdown()
            raise

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.initialize()

    async def initialize(self):
        if self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=timeout)

    async def shutdown(self):
        if self._client.is_closed:
            return
        await self._client.aclose()

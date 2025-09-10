from typing import Any, Protocol


class BaseHttpClient(Protocol):
    async def get(
        self, url: str, params: dict | None = None, headers: dict | None = None
    ) -> dict[str, Any]: ...

from typing import Optional


class CacheService:
    def __init__(self) -> None:
        self._store: dict[str, tuple[bytes, int]] = {}

    def set(self, key: str, value: bytes, ttl_seconds: int = 60) -> None:
        self._store[key] = (value, ttl_seconds)

    def get(self, key: str) -> Optional[bytes]:
        item = self._store.get(key)
        if not item:
            return None
        return item[0]







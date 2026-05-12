from __future__ import annotations

class InMemoryDedupe:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def add_once(self, key: str) -> bool:
        if key in self._seen:
            return False
        self._seen.add(key)
        return True

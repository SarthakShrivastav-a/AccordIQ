from __future__ import annotations

import hashlib

def deterministic_embedding(text: str, dimensions: int = 16) -> list[float]:
    digest = hashlib.sha256(text.encode()).digest()
    return [digest[i % len(digest)] / 255 for i in range(dimensions)]
